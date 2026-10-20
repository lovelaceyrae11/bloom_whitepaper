import json
import hashlib
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

CML_FILE = "cluster_extended.cml"
LEDGER_FILE = "pbft_consensus_ledger.jsonl"

EXPECTED_NODES = 127
MAX_FAULTS = 42
EXPECTED_QUORUM = 2 * MAX_FAULTS + 1

EXPECTED_VIEW = 1
EXPECTED_SEQUENCE = 1001

PINNED_ROOT_SHA256 = (
    "9745b5840660bb48166ff142968fa90469df9606e1836e3255ac3d51bef8bea9"
)


def fail(message):
    raise ValueError(message)


def load_pem(value):
    if not value:
        fail("Missing certificate PEM.")
    return value.replace("\\n", "\n").encode("utf-8")


def verify_sig(public_key, signature_hex, message, label):
    try:
        signature = bytes.fromhex(signature_hex)
        public_key.verify(signature, message)
    except Exception as exc:
        fail(f"Invalid signature for {label}: {exc}")


def check_time(cert, now, label):
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        fail(f"{label}: certificate is outside its validity period")


def require_positive_int(value, label):
    # bool is a subclass of int in Python, so reject it explicitly.
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        fail(f"{label} must be a positive integer.")


def main():
    print("CASTLEBERRY BLOOM: INDEPENDENT VERIFIER V3")

    if EXPECTED_QUORUM != 85:
        fail("Internal quorum configuration is unexpected.")

    if EXPECTED_NODES < (3 * MAX_FAULTS + 1):
        fail("Node count does not satisfy the configured 3f+1 condition.")

    xml_root = ET.parse(CML_FILE).getroot()

    root_pem = load_pem(xml_root.get("root_ca_pem"))
    root_cert = x509.load_pem_x509_certificate(root_pem)

    fingerprint = root_cert.fingerprint(hashes.SHA256()).hex()
    if fingerprint != PINNED_ROOT_SHA256:
        fail("Root CA fingerprint does not match the pinned value.")

    now = datetime.now(timezone.utc)
    check_time(root_cert, now, "Root CA")

    if root_cert.subject != root_cert.issuer:
        fail("Root CA is not self-issued.")

    ca_key = root_cert.public_key()
    if not isinstance(ca_key, ed25519.Ed25519PublicKey):
        fail("Root CA key is not Ed25519.")

    # V3 addition: verify the root certificate's self-signature.
    verify_sig(
        ca_key,
        root_cert.signature.hex(),
        root_cert.tbs_certificate_bytes,
        "root CA self-signature",
    )
    print("[OK] Root CA fingerprint, validity, and self-signature")

    nodes = {}
    topology_order = []

    for tier in xml_root.findall("Tier"):
        for node in tier.findall("Node"):
            nid = node.get("node_id")

            if not nid or nid in nodes:
                fail(f"Missing or duplicate node ID: {nid}")

            cert_pem = load_pem(node.get("ek_certificate"))
            cert = x509.load_pem_x509_certificate(cert_pem)
            check_time(cert, now, f"Node {nid}")

            if cert.issuer != root_cert.subject:
                fail(f"Wrong certificate issuer for {nid}")

            common_names = cert.subject.get_attributes_for_oid(
                x509.oid.NameOID.COMMON_NAME
            )
            if len(common_names) != 1 or common_names[0].value != nid:
                fail(f"Certificate identity mismatch for {nid}")

            verify_sig(
                ca_key,
                cert.signature.hex(),
                cert.tbs_certificate_bytes,
                f"certificate {nid}",
            )

            cert_key = cert.public_key()
            if not isinstance(cert_key, ed25519.Ed25519PublicKey):
                fail(f"Certificate key is not Ed25519 for {nid}")

            try:
                cml_key = ed25519.Ed25519PublicKey.from_public_bytes(
                    bytes.fromhex(node.get("public_key", ""))
                )
            except Exception as exc:
                fail(f"Invalid CML public key for {nid}: {exc}")

            cert_raw = cert_key.public_bytes(
                Encoding.Raw, PublicFormat.Raw
            )
            cml_raw = cml_key.public_bytes(
                Encoding.Raw, PublicFormat.Raw
            )

            if cert_raw != cml_raw:
                fail(f"Certificate public key mismatch for {nid}")

            nodes[nid] = cml_key
            topology_order.append(nid)

    if len(nodes) != EXPECTED_NODES:
        fail(f"Expected {EXPECTED_NODES} nodes; found {len(nodes)}")

    if len(set(topology_order)) != EXPECTED_NODES:
        fail("Topology contains duplicate node IDs.")

    expected_primary = topology_order[0]
    print(f"[OK] {len(nodes)} unique node certificates checked")
    print(f"[OK] First topology node: {expected_primary}")

    with open(LEDGER_FILE, encoding="utf-8") as f:
        ledger = json.load(f)

    if not isinstance(ledger, dict):
        fail("Ledger must be a JSON object.")

    if ledger.get("total_nodes") != EXPECTED_NODES:
        fail("Unexpected node count in ledger.")

    if ledger.get("quorum_threshold") != EXPECTED_QUORUM:
        fail("Unexpected quorum threshold in ledger.")

    proposal = ledger.get("proposal")
    if not isinstance(proposal, dict):
        fail("Missing or invalid proposal.")

    required_fields = {
        "view", "sequence", "primary", "state_root", "timestamp"
    }
    if not required_fields.issubset(proposal):
        fail("Proposal is missing required fields.")

    view = proposal["view"]
    sequence = proposal["sequence"]

    require_positive_int(view, "Proposal view")
    require_positive_int(sequence, "Proposal sequence")

    if view != EXPECTED_VIEW:
        fail(f"Unexpected proposal view: {view}")

    if sequence != EXPECTED_SEQUENCE:
        fail(f"Unexpected proposal sequence: {sequence}")

    primary = proposal["primary"]
    if primary not in nodes:
        fail("Unknown proposal primary.")

    if primary != expected_primary:
        fail(
            f"Unexpected primary: {primary}; "
            f"topology expects {expected_primary}"
        )

    state_root = proposal["state_root"]
    if not isinstance(state_root, str) or not re.fullmatch(
        r"[0-9a-f]{64}", state_root
    ):
        fail("Proposal state_root must be a 64-character lowercase SHA-256 hex value.")

    timestamp = proposal["timestamp"]
    import math

    if (
        isinstance(timestamp, bool)
        or not isinstance(timestamp, (int, float))
        or not math.isfinite(timestamp)
        or timestamp <= 0
    ):
        fail("Proposal timestamp must be a finite, positive Unix timestamp.")

    proposal_bytes = json.dumps(
        proposal, sort_keys=True
    ).encode("utf-8")

    verify_sig(
        nodes[primary],
        ledger.get("pre_prepare_signature", ""),
        proposal_bytes,
        "PRE-PREPARE",
    )
    print("[OK] Proposal structure, view, sequence, and primary")
    print("[OK] PRE-PREPARE signature verified")

    for phase in ("prepare", "commit"):
        votes = ledger.get(f"{phase}_votes")

        if not isinstance(votes, list):
            fail(f"Missing or invalid {phase} votes.")

        seen = set()

        for index, vote in enumerate(votes):
            if not isinstance(vote, dict):
                fail(f"Invalid {phase} vote entry at index {index}.")

            nid = vote.get("node_id")
            if not isinstance(nid, str) or nid not in nodes:
                fail(f"Unknown node in {phase} votes: {nid}")

            if nid in seen:
                fail(f"Duplicate {phase} vote from {nid}")

            seen.add(nid)

            # Existing engine signs sequence and state_root, but not view.
            message = (
                f"{phase.upper()}:{sequence}:{state_root}:{nid}"
            ).encode("utf-8")

            verify_sig(
                nodes[nid],
                vote.get("signature", ""),
                message,
                f"{phase} vote from {nid}",
            )

        if len(seen) < EXPECTED_QUORUM:
            fail(
                f"{phase.upper()} quorum not met: "
                f"{len(seen)} unique voters"
            )

        if ledger.get(f"{phase}_votes_count") != len(votes):
            fail(f"{phase}_votes_count does not match vote list.")

        print(
            f"[OK] {phase.upper()}: {len(seen)} unique valid votes; "
            f"quorum {EXPECTED_QUORUM} met"
        )

    block = {
        key: value
        for key, value in ledger.items()
        if key != "ledger_hash"
    }

    calculated = hashlib.sha256(
        json.dumps(block, sort_keys=True).encode("utf-8")
    ).hexdigest()

    if ledger.get("ledger_hash") != calculated:
        fail("Ledger hash mismatch.")

    print(f"[OK] Ledger hash: {calculated}")
    print("PASS: V3 prototype ledger integrity checks completed.")
    print("LIMIT: This does not prove independent multi-machine consensus.")
    print("LIMIT: Existing PREPARE/COMMIT signatures do not bind the view number.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
