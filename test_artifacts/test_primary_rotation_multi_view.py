import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import independent_verifier_v5_rotation_experimental as verifier
from cml_engine import parse_and_validate_topology
from cryptography.hazmat.primitives.asymmetric import ed25519

ledger_path = Path("test_artifacts/pbft_v4_viewbound_test_ledger.json")
original = json.loads(ledger_path.read_text(encoding="utf-8"))
secrets = json.loads(Path("node_secrets.json").read_text(encoding="utf-8"))
nodes = [
    item["node_id"]
    for item in parse_and_validate_topology("cluster_extended.cml")
]
public_keys, _, _ = verifier.load_and_verify_trust_anchor()
views = [0, 1, 2, 126]

def make_case(view, primary):
    ledger = copy.deepcopy(original)
    ledger["proposal"]["view"] = view
    ledger["proposal"]["primary"] = primary
    proposal = ledger["proposal"]

    key = ed25519.Ed25519PrivateKey.from_private_bytes(
        bytes.fromhex(secrets[primary])
    )
    ledger["pre_prepare_signature"] = key.sign(
        verifier.canonical_json_bytes(proposal)
    ).hex()

    for phase in ("prepare", "commit"):
        for vote in ledger[f"{phase}_votes"]:
            node_id = vote["node_id"]
            message = (
                f"{phase.upper()}:{view}:{proposal['sequence']}:"
                f"{proposal['state_root']}:{node_id}"
            ).encode("utf-8")
            vote_key = ed25519.Ed25519PrivateKey.from_private_bytes(
                bytes.fromhex
                (secrets[node_id])
            )
            vote["signature"] = vote_key.sign(message).hex()

    ledger["ledger_hash"] = verifier.calculate_ledger_hash(ledger)
    return ledger

passed = 0
failed = 0

print("EXPERIMENTAL PRIMARY ROTATION MULTI-VIEW TEST")
print("Provisional rule: primary(view) = nodes[view % node_count]")
print("Cases are re-signed in memory; this is not distributed consensus.")
print()

for view in views:
    expected = nodes[view % len(nodes)]
    wrong = next(node for node in nodes if node != expected)

    try:
        verifier.verify_pbft_consensus(make_case(view, expected), public_keys, {})
        print(f"PASS view={view}: expected primary accepted ({expected})")
        passed += 1
    except Exception as exc:
        print(f"FAIL view={view}: expected primary rejected: {exc}")
        failed += 1

    try:
        verifier.verify_pbft_consensus(make_case(view, wrong), public_keys, {})
        print(f"FAIL view={view}: wrong primary accepted ({wrong})")
        failed += 1
    except verifier.VerificationError as exc:
        if "Primary rotation violation" in str(exc):
            print(f"PASS view={view}: wrong primary rejected ({wrong})")
            passed += 1
        else:
            print(f"FAIL view={view}: unexpected rejection: {exc}")
            failed += 1

print()
print(f"SUMMARY: {passed} passed, {failed} failed, {passed + failed} total")
print("Original test ledger was read only; test cases were in memory.")
