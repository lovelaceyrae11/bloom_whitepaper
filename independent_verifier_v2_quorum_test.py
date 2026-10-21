# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import json
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

CML_FILE = "cluster_extended.cml"
LEDGER_FILE = "test_artifacts/ledger_quorum_test.json"
EXPECTED_NODES = 127
EXPECTED_QUORUM = 85
PINNED_ROOT_SHA256 = "9745b5840660bb48166ff142968fa90469df9606e1836e3255ac3d51bef8bea9"


def fail(message):
    raise ValueError(message)


def load_pem(value):
    if not value:
        fail("Missing certificate PEM.")
    return value.replace("\\n", "\n").encode("utf-8")


def check_time(cert, now, label):
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        fail(f"{label}: certificate is outside its validity period")


def verify_sig(public_key, signature_hex, message, label):
    try:
        public_key.verify(bytes.fromhex(signature_hex), message)
    except Exception as exc:
        fail(f"Invalid signature for {label}: {exc}")


def main():
    print("CASTLEBERRY BLOOM: INDEPENDENT VERIFIER V2")

    xml_root = ET.parse(CML_FILE).getroot()
    root_cert = x509.load_pem_x509_certificate(
        load_pem(xml_root.get("root_ca_pem"))
    )

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

    nodes = {}
    for tier in xml_root.findall("Tier"):
        for node in tier.findall("Node"):
            nid = node.get("node_id")
            if not nid or nid in nodes:
                fail(f"Missing or duplicate node ID: {nid}")

            cert = x509.load_pem_x509_certificate(
                load_pem(node.get("ek_certificate"))
            )
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

            cml_key = ed25519.Ed25519PublicKey.from_public_bytes(
                bytes.fromhex(node.get("public_key", ""))
            )
            cert_raw = cert_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
            cml_raw = cml_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
            if cert_raw != cml_raw:
                fail(f"Certificate public key mismatch for {nid}")

            nodes[nid] = cml_key

    if len(nodes) != EXPECTED_NODES:
        fail(f"Expected {EXPECTED_NODES} nodes; found {len(nodes)}")

    print(f"[OK] Pinned root fingerprint: {fingerprint}")
    print(f"[OK] {len(nodes)} unique node certificates checked")

    with open(LEDGER_FILE, encoding="utf-8") as f:
        ledger = json.load(f)

    if ledger.get("total_nodes") != EXPECTED_NODES:
        fail("Unexpected node count in ledger.")
    if ledger.get("quorum_threshold") != EXPECTED_QUORUM:
        fail("Unexpected quorum threshold in ledger.")

    proposal = ledger.get("proposal")
    if not isinstance(proposal, dict):
        fail("Missing proposal.")

    primary = proposal.get("primary")
    if primary not in nodes:
        fail("Unknown proposal primary.")

    proposal_bytes = json.dumps(proposal, sort_keys=True).encode("utf-8")
    verify_sig(
        nodes[primary],
        ledger.get("pre_prepare_signature", ""),
        proposal_bytes,
        "PRE-PREPARE",
    )
    print("[OK] PRE-PREPARE signature verified")

    for phase in ("prepare", "commit"):
        votes = ledger.get(f"{phase}_votes")
        if not isinstance(votes, list):
            fail(f"Missing {phase} votes.")

        seen = set()
        for vote in votes:
            nid = vote.get("node_id")
            if nid not in nodes:
                fail(f"Unknown node in {phase} votes: {nid}")
            if nid in seen:
                fail(f"Duplicate {phase} vote from {nid}")
            seen.add(nid)

            message = (
                f"{phase.upper()}:{proposal['sequence']}:"
                f"{proposal['state_root']}:{nid}"
            ).encode("utf-8")
            verify_sig(
                nodes[nid], vote.get("signature", ""), message,
                f"{phase} vote from {nid}",
            )

        if len(seen) < EXPECTED_QUORUM:
            fail(f"{phase.upper()} quorum not met: {len(seen)}")

        if ledger.get(f"{phase}_votes_count") != len(votes):
            fail(f"{phase}_votes_count does not match vote list.")

        print(f"[OK] {phase.upper()}: {len(seen)} unique valid votes")

    block = {k: v for k, v in ledger.items() if k != "ledger_hash"}
    calculated = hashlib.sha256(
        json.dumps(block, sort_keys=True).encode("utf-8")
    ).hexdigest()

    if ledger.get("ledger_hash") != calculated:
        fail("Ledger hash mismatch.")

    print(f"[OK] Ledger hash: {calculated}")
    print("PASS: prototype ledger integrity checks completed.")
    print("LIMIT: this does not prove independent multi-machine consensus.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
