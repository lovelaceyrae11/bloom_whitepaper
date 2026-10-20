import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import json
from pathlib import Path

import independent_verifier_v5_rotation_experimental as verifier
from cml_engine import parse_and_validate_topology

# Read existing inputs only. Never print private key material.
ledger_path = Path("test_artifacts/pbft_v4_viewbound_test_ledger.json")
ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
secrets = json.loads(Path("node_secrets.json").read_text(encoding="utf-8"))
node_order = [
    node["node_id"]
    for node in parse_and_validate_topology("cluster_extended.cml")
]
public_keys, _, _ = verifier.load_and_verify_trust_anchor()

# Provisional rule: primary(view) = node_order[view % node_count].
view = 0
expected_primary = node_order[view % len(node_order)]
wrong_primary = next(
    node for node in node_order if node != expected_primary
)

# Build a fully re-signed in-memory ledger with a trusted but wrong primary.
ledger["proposal"]["view"] = view
ledger["proposal"]["primary"] = expected_primary
proposal = ledger["proposal"]

from cryptography.hazmat.primitives.asymmetric import ed25519

primary_key = ed25519.Ed25519PrivateKey.from_private_bytes(
    bytes.fromhex(secrets[expected_primary])
)
ledger["pre_prepare_signature"] = primary_key.sign(
    verifier.canonical_json_bytes(proposal)
).hex()

for phase in ("prepare", "commit"):
    votes = ledger[f"{phase}_votes"]
    for vote in votes:
        node_id = vote["node_id"]
        message = (
            f"{phase.upper()}:{view}:{proposal['sequence']}:"
            f"{proposal['state_root']}:{node_id}"
        ).encode("utf-8")
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
            bytes.fromhex(secrets[node_id])
        )
        vote["signature"] = private_key.sign(message).hex()

ledger["ledger_hash"] = verifier.calculate_ledger_hash(ledger)

print("Expected primary for test view:", expected_primary)
print("Test proposal primary:", expected_primary)
print("Existing ledger file left unchanged.")

try:
    verifier.verify_pbft_consensus(ledger, public_keys, {})
except verifier.VerificationError as exc:
    print("RESULT: REJECTED:", exc)
else:
    print("RESULT: ACCEPTED")
    print("FINDING: correctly selected primary accepted for view 0.")
