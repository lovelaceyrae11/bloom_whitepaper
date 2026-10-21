# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import json
import os
from datetime import datetime, timezone

# Load local offline genesis proof
proof_path = "build_artifacts/offline_genesis_proof.json"
if not os.path.exists(proof_path):
    raise FileNotFoundError("[!] Offline genesis proof not found.")

with open(proof_path, "r") as f:
    proof_data = json.load(f)

# Construct local node registry entry using timezone-aware UTC datetime
registry_entry = {
    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "node_id": proof_data["signer"],
    "symbol": proof_data["payload"]["symbol"],
    "base_frequency": proof_data["payload"]["base_frequency"],
    "lattice_geometry": proof_data["payload"]["lattice_geometry"],
    "consensus_mode": proof_data["payload"]["consensus"],
    "signature_status": "verified",
    "signature": proof_data["signature"]
}

ledger_path = "build_artifacts/lattice_node_registry.jsonl"
with open(ledger_path, "a") as f:
    f.write(json.dumps(registry_entry) + "\n")

print(f"[+] Node successfully registered to local lattice ledger: {ledger_path}")
