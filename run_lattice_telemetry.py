import json
import os

ledger_path = "build_artifacts/lattice_node_registry.jsonl"
if not os.path.exists(ledger_path):
    raise FileNotFoundError("[!] Lattice ledger not found.")

print("[*] Scanning Active Lattice Node Registry...")
with open(ledger_path, "r") as f:
    for line in f:
        node = json.loads(line)
        print(f" -> Node: {node['node_id']} | Freq: {node['base_frequency']} | Status: {node['signature_status']}")

print("[+] Lattice telemetry sync complete. Ready for agent swarm integration.")
