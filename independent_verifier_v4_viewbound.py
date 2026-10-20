
import copy
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey,
)


# ============================================================
# CASTLEBERRY BLOOM
# Independent PBFT Ledger Verifier v4
# ============================================================

CML_FILE = "cluster_extended.cml"
LEDGER_FILE = "test_artifacts/pbft_v4_viewbound_test_ledger.json"

# Trusted configuration. Do not take these values from the ledger.
TOTAL_NODES = 127
MAX_FAULTS = 42
EXPECTED_QUORUM = 2 * MAX_FAULTS + 1  # 85

# Expected PBFT relationship: n >= 3f + 1.
if TOTAL_NODES < (3 * MAX_FAULTS + 1):
    raise RuntimeError("Invalid trusted PBFT fault configuration.")


class VerificationError(Exception):
    """Raised when a ledger fails independent verification."""


def canonical_json_bytes(value):
    """Use the same sorted-key JSON encoding for signatures and hashes."""
    return json.dumps(value, sort_keys=True).encode("utf-8")


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def verify_ed25519_signature(public_key, signature_hex, message):
    """Verify a hex-encoded Ed25519 signature."""
    try:
        signature = bytes.fromhex(signature_hex)
        public_key.verify(signature, message)
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False


def load_and_verify_trust_anchor(cml_path=CML_FILE):
    """
    Load the CA certificate and node certificates from the CML file.

    Every node's declared Ed25519 public key must match the public key
    inside its certificate. Each node certificate must be signed by
    the configured CA.
    """
    path = Path(cml_path)
    if not path.is_file():
        raise VerificationError(f"CML file not found: {path}")

    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except (ET.ParseError, OSError) as exc:
        raise VerificationError(f"Cannot parse CML file: {exc}") from exc

    root_ca_pem = root.get("root_ca_pem")
    if not root_ca_pem:
        raise VerificationError(
            "CML root is missing the root_ca_pem attribute."
        )

    try:
        root_ca_pem = root_ca_pem.replace("\\n", "\n")
        ca_cert = x509.load_pem_x509_certificate(
            root_ca_pem.encode("utf-8")
        )
        ca_public_key = ca_cert.public_key()
    except Exception as exc:
        raise VerificationError(
            f"Cannot load root CA certificate: {exc}"
        ) from exc

    # Check the CA certificate's validity period.
    now = datetime.now(timezone.utc)
    not_before = ca_cert.not_valid_before.replace(tzinfo=timezone.utc)
    not_after = ca_cert.not_valid_after.replace(tzinfo=timezone.utc)

    if not (not_before <= now <= not_after):
        raise VerificationError("Root CA certificate is not currently valid.")

    node_public_keys = {}
    node_certificates = {}

    # The current CML structure stores nodes beneath Tier elements.
    nodes = root.findall(".//Tier/Node")

    # Also support a CML file where Node elements are directly nested
    # elsewhere under the root.
    if not nodes:
        nodes = root.findall(".//Node")

    for node in nodes:
        node_id = node.get("node_id")
        public_key_hex = node.get("public_key")
        certificate_pem = node.get("ek_certificate")

        if not node_id or not public_key_hex or not certificate_pem:
            raise VerificationError(
                "A node is missing node_id, public_key, or ek_certificate."
            )

        if node_id in node_public_keys:
            raise VerificationError(f"Duplicate node ID: {node_id}")

        try:
            public_key_bytes = bytes.fromhex(public_key_hex)
            public_key = Ed25519PublicKey.from_public_bytes(
                public_key_bytes
            )

            certificate_pem = certificate_pem.replace("\\n", "\n")
            certificate = x509.load_pem_x509_certificate(
                certificate_pem.encode("utf-8")
            )
        except Exception as exc:
            raise VerificationError(
                f"Invalid key or certificate for {node_id}: {exc}"
            ) from exc

        # The node certificate must be within its validity period.
        cert_not_before = certificate.not_valid_before.replace(
            tzinfo=timezone.utc
        )
        cert_not_after = certificate.not_valid_after.replace(
            tzinfo=timezone.utc
        )

        if not (cert_not_before <= now <= cert_not_after):
            raise VerificationError(
                f"Node certificate is not currently valid: {node_id}"
            )

        # Require the certificate issuer to match the configured CA subject.
        if certificate.issuer != ca_cert.subject:
            raise VerificationError(
                f"Certificate issuer mismatch for {node_id}"
            )

        # Verify that the CA signed this node certificate.
        try:
            ca_public_key.verify(
                certificate.signature,
                certificate.tbs_certificate_bytes,
            )
        except (InvalidSignature, AttributeError, TypeError) as exc:
            raise VerificationError(
                f"CA signature verification failed for {node_id}"
            ) from exc

        # The certificate public key must match the CML-declared key.
        certificate_public_key = certificate.public_key()

        if not isinstance(certificate_public_key, Ed25519PublicKey):
            raise VerificationError(
                f"Certificate key is not Ed25519: {node_id}"
            )

        certificate_key_bytes = certificate_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        if certificate_key_bytes != public_key_bytes:
            raise VerificationError(
                f"Certificate/public-key mismatch for {node_id}"
            )

        node_public_keys[node_id] = public_key
        node_certificates[node_id] = certificate

    if len(node_public_keys) != TOTAL_NODES:
        raise VerificationError(
            f"Expected {TOTAL_NODES} unique nodes, "
            f"found {len(node_public_keys)}."
        )

    return node_public_keys, node_certificates, ca_public_key


def calculate_ledger_hash(ledger):
    """Calculate the hash while excluding the ledger_hash field itself."""
    hash_input = copy.deepcopy(ledger)
    hash_input.pop("ledger_hash", None)
    return sha256_hex(canonical_json_bytes(hash_input))


def verify_pbft_consensus(
    ledger,
    node_public_keys,
    executed_sequences=None,
):
    """
    Verify the proposal, PREPARE votes, COMMIT votes, and ledger hash.

    executed_sequences is a local dictionary mapping sequence numbers
    to state roots already accepted by this verifier.
    """
    if executed_sequences is None:
        executed_sequences = {}

    if not isinstance(ledger, dict):
        raise VerificationError("Ledger must be a JSON object.")

    # The trusted quorum is configured locally, not selected by the ledger.
    ledger_quorum = ledger.get("quorum_threshold")
    if (
        ledger_quorum is not None
        and ledger_quorum != EXPECTED_QUORUM
    ):
        raise VerificationError(
            "Ledger quorum does not match trusted configuration."
        )

    quorum = EXPECTED_QUORUM

    proposal = ledger.get("proposal")
    if not isinstance(proposal, dict):
        raise VerificationError("Missing or invalid proposal.")

    view = proposal.get("view")
    if not isinstance(view, int) or isinstance(view, bool) or view < 0:
        raise VerificationError(
            "Proposal view must be a nonnegative integer."
        )

    primary = proposal.get("primary")
    sequence = proposal.get("sequence")
    state_root = proposal.get("state_root")
    proposal_signature = ledger.get("pre_prepare_signature")

    if primary is None or sequence is None or not state_root:
        raise VerificationError(
            "Proposal must contain primary, sequence, and state_root."
        )

    if not isinstance(sequence, int) or sequence < 0:
        raise VerificationError("Proposal sequence must be a nonnegative integer.")

    if primary not in node_public_keys:
        raise VerificationError(f"Unknown primary node: {primary}")

    if not isinstance(proposal_signature, str):
        raise VerificationError("Missing PRE-PREPARE signature.")

    # Reject a second, conflicting state root for an accepted sequence.
    sequence_key = str(sequence)
    if sequence_key in executed_sequences:
        previous_root = executed_sequences[sequence_key]

        if previous_root != state_root:
            raise VerificationError(
                "SEQUENCE COLLISION REJECTED: conflicting state root."
            )

        raise VerificationError(
            "Sequence has already been accepted by this verifier."
        )

    # Verify the primary's signature over the canonical proposal JSON.
    if not verify_ed25519_signature(
        node_public_keys[primary],
        proposal_signature,
        canonical_json_bytes(proposal),
    ):
        raise VerificationError("Invalid PRE-PREPARE signature.")

    # Verify PREPARE votes.
    prepare_votes = ledger.get("prepare_votes")
    if not isinstance(prepare_votes, list):
        raise VerificationError("Missing or invalid prepare_votes list.")

    if len(prepare_votes) < quorum:
        raise VerificationError(
            f"Insufficient prepare votes ({len(prepare_votes)}/{quorum})."
        )

    prepare_voters = set()

    for vote in prepare_votes:
        if not isinstance(vote, dict):
            raise VerificationError("Malformed PREPARE vote.")

        node_id = vote.get("node_id")
        signature = vote.get("signature")

        if node_id not in node_public_keys:
            raise VerificationError(
                f"Unknown PREPARE voter: {node_id}"
            )

        if node_id in prepare_voters:
            raise VerificationError(
                f"Duplicate PREPARE voter: {node_id}"
            )

        if not isinstance(signature, str):
            raise VerificationError(
                f"Missing PREPARE signature for {node_id}"
            )

        message = (
            f"PREPARE:{view}:{sequence}:{state_root}:{node_id}"
        ).encode("utf-8")

        if not verify_ed25519_signature(
            node_public_keys[node_id],
            signature,
            message,
        ):
            raise VerificationError(
                f"Invalid PREPARE signature from {node_id}"
            )

        prepare_voters.add(node_id)

    # Verify COMMIT votes.
    commit_votes = ledger.get("commit_votes")
    if not isinstance(commit_votes, list):
        raise VerificationError("Missing or invalid commit_votes list.")

    if len(commit_votes) < quorum:
        raise VerificationError(
            f"Insufficient commit votes ({len(commit_votes)}/{quorum})."
        )

    commit_voters = set()

    for vote in commit_votes:
        if not isinstance(vote, dict):
            raise VerificationError("Malformed COMMIT vote.")

        node_id = vote.get("node_id")
        signature = vote.get("signature")

        if node_id not in node_public_keys:
            raise VerificationError(
                f"Unknown COMMIT voter: {node_id}"
            )

        if node_id in commit_voters:
            raise VerificationError(
                f"Duplicate COMMIT voter: {node_id}"
            )

        if not isinstance(signature, str):
            raise VerificationError(
                f"Missing COMMIT signature for {node_id}"
            )

        message = (
            f"COMMIT:{view}:{sequence}:{state_root}:{node_id}"
        ).encode("utf-8")

        if not verify_ed25519_signature(
            node_public_keys[node_id],
            signature,
            message,
        ):
            raise VerificationError(
                f"Invalid COMMIT signature from {node_id}"
            )

        commit_voters.add(node_id)

    # Ensure the ledger's ordinary SHA-256 integrity check passes.
    stored_hash = ledger.get("ledger_hash")
    if not isinstance(stored_hash, str):
        raise VerificationError("Missing ledger_hash.")

    calculated_hash = calculate_ledger_hash(ledger)

    if stored_hash != calculated_hash:
        raise VerificationError("Ledger hash mismatch.")

    # Record acceptance only after all checks pass.
    executed_sequences[sequence_key] = state_root
    return True


def expect_rejection(test_name, operation, expected_text=None):
    """A test passes only when the operation is rejected as expected."""
    try:
        operation()
    except (VerificationError, ValueError, InvalidSignature) as exc:
        message = str(exc)

        if expected_text and expected_text not in message:
            print(f"[FAIL] {test_name}: wrong rejection: {message}")
            return False

        print(f"[PASS] {test_name}: rejected ({message})")
        return True
    except Exception as exc:
        print(f"[FAIL] {test_name}: unexpected error: {exc}")
        return False

    print(f"[FAIL] {test_name}: invalid input was accepted.")
    return False


def run_v4_unified_suite():
    print("=" * 64)
    print("CASTLEBERRY BLOOM: INDEPENDENT PBFT VERIFIER v4")
    print("=" * 64)
    print(f"Trusted node count: {TOTAL_NODES}")
    print(f"Assumed fault bound: {MAX_FAULTS}")
    print(f"Trusted quorum: {EXPECTED_QUORUM}")
    print()

    try:
        node_keys, node_certs, ca_key = load_and_verify_trust_anchor()
        print(f"[PASS] Trust anchor and {len(node_keys)} node certificates verified.")

        ledger_path = Path(LEDGER_FILE)
        if not ledger_path.is_file():
            raise VerificationError(
                f"Ledger file not found: {ledger_path}"
            )

        # Despite the .jsonl extension, this verifier expects one JSON object.
        with ledger_path.open("r", encoding="utf-8") as file:
            valid_ledger = json.load(file)

        executed_state = {}

        # Test 1: verify the untouched ledger.
        if verify_pbft_consensus(
            valid_ledger,
            node_keys,
            executed_state,
        ):
            print("[PASS] Test 1: pristine ledger verified.")

        # Test 2: reject a conflicting root for a sequence already accepted.
        split_brain_ledger = copy.deepcopy(valid_ledger)
        split_brain_ledger["proposal"]["state_root"] = sha256_hex(
            b"MALICIOUS_SPLIT_BRAIN"
        )
        split_brain_ledger["ledger_hash"] = calculate_ledger_hash(
            split_brain_ledger
        )

        if expect_rejection(
            "Test 2: conflicting sequence/state root",
            lambda: verify_pbft_consensus(
                split_brain_ledger,
                node_keys,
                executed_state,
            ),
            "SEQUENCE COLLISION REJECTED",
        ) is False:
            raise VerificationError("Test 2 failed.")

        # Test 3: substitute a public key and verify the original ledger again.
        altered_keys = dict(node_keys)
        node_ids = list(altered_keys)

        if len(node_ids) < 2:
            raise VerificationError("Not enough nodes for key-substitution test.")

        altered_keys[node_ids[0]] = altered_keys[node_ids[1]]

        if expect_rejection(
            "Test 3: public-key substitution",
            lambda: verify_pbft_consensus(
                valid_ledger,
                altered_keys,
                {},
            ),
        ) is False:
            raise VerificationError("Test 3 failed.")

        # Test 4: reject a ledger that tries to choose its own quorum.
        bad_quorum_ledger = copy.deepcopy(valid_ledger)
        bad_quorum_ledger["quorum_threshold"] = 250
        bad_quorum_ledger["ledger_hash"] = calculate_ledger_hash(
            bad_quorum_ledger
        )

        if expect_rejection(
            "Test 4: untrusted quorum value",
            lambda: verify_pbft_consensus(
                bad_quorum_ledger,
                node_keys,
                {},
            ),
            "Ledger quorum does not match trusted configuration",
        ) is False:
            raise VerificationError("Test 4 failed.")

        # Test 5: duplicate a COMMIT voter.
        duplicate_ledger = copy.deepcopy(valid_ledger)
        commits = duplicate_ledger.get("commit_votes", [])

        if len(commits) < 2:
            raise VerificationError(
                "Not enough COMMIT votes for duplicate-voter test."
            )

        duplicate_ledger["commit_votes"][1] = copy.deepcopy(commits[0])
        duplicate_ledger["ledger_hash"] = calculate_ledger_hash(
            duplicate_ledger
        )

        if expect_rejection(
            "Test 5: duplicate COMMIT voter",
            lambda: verify_pbft_consensus(
                duplicate_ledger,
                node_keys,
                {},
            ),
            "Duplicate COMMIT voter",
        ) is False:
            raise VerificationError("Test 5 failed.")

        # Test 6: corrupt a signature without changing the signed message.
        forged_ledger = copy.deepcopy(valid_ledger)
        forged_ledger["commit_votes"][0]["signature"] = "deadbeef" * 8
        forged_ledger["ledger_hash"] = calculate_ledger_hash(forged_ledger)

        if expect_rejection(
            "Test 6: forged COMMIT signature",
            lambda: verify_pbft_consensus(
                forged_ledger,
                node_keys,
                {},
            ),
            "Invalid COMMIT signature",
        ) is False:
            raise VerificationError("Test 6 failed.")

        print()
        print("=" * 64)
        # Test 7: a PREPARE signature must be bound to its view.
        test_view = valid_ledger["proposal"]["view"]
        test_sequence = valid_ledger["proposal"]["sequence"]
        test_root = valid_ledger["proposal"]["state_root"]
        test_vote = valid_ledger["prepare_votes"][0]
        test_node = test_vote["node_id"]
        test_signature = test_vote["signature"]

        original_message = (
            f"PREPARE:{test_view}:{test_sequence}:{test_root}:{test_node}"
        ).encode("utf-8")
        alternate_view_message = (
            f"PREPARE:{test_view + 1}:{test_sequence}:{test_root}:{test_node}"
        ).encode("utf-8")

        original_view_valid = verify_ed25519_signature(
            node_keys[test_node], test_signature, original_message
        )
        alternate_view_valid = verify_ed25519_signature(
            node_keys[test_node], test_signature, alternate_view_message
        )

        if not original_view_valid or alternate_view_valid:
            raise VerificationError(
                "Test 7 failed: PREPARE signature was not bound to its view."
            )

        print(
            "[PASS] Test 7: PREPARE signature rejected for a different view."
        )

        print("ALL SEVEN VERIFICATION TESTS PASSED")
        print("=" * 64)
        print(
            "Scope: certificate/key binding, signed ledger checks, "
            "quorum enforcement, duplicate-voter rejection, and a "
            "local sequence-collision guard."
        )
        print(
            "This suite does not establish full distributed PBFT "
            "safety or liveness."
        )

    except (VerificationError, OSError, json.JSONDecodeError) as exc:
        print()
        print(f"[FAIL] Verification suite stopped: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    run_v4_unified_suite()

