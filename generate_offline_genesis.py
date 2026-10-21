# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import os
import json
from eth_account import Account
from eth_account.messages import encode_defunct

# Load Deployer Key from Environment
PRIVATE_KEY = os.getenv("METAMASK_PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("[!] METAMASK_PRIVATE_KEY not set.")

deployer = Account.from_key(PRIVATE_KEY)

# Construct Offline Genesis Block Proof
genesis_payload = {
    "node_address": deployer.address,
    "symbol": "BLOOM-SEED",
    "base_frequency": "528Hz",
    "lattice_geometry": "phi-hexagonal",
    "consensus": "PBFT-f42",
    "status": "locally_anchored"
}

# Sign the message correctly using defunct encoding
message_text = json.dumps(genesis_payload, sort_keys=True)
signable_message = encode_defunct(text=message_text)
signed_message = Account.sign_message(signable_message, private_key=PRIVATE_KEY)

os.makedirs("build_artifacts", exist_ok=True)
output_path = "build_artifacts/offline_genesis_proof.json"

output_data = {
    "payload": genesis_payload,
    "signature": signed_message.signature.hex(),
    "signer": deployer.address
}

with open(output_path, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"[+] Offline Coherence Genesis Proof generated successfully at: {output_path}")
print(f"[+] Signed by Sovereign Address: {deployer.address}")
