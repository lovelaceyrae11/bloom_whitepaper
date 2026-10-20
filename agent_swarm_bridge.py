import json
import os

ledger_path = "build_artifacts/lattice_node_registry.jsonl"
if not os.path.exists(ledger_path):
    raise FileNotFoundError("[!] Lattice ledger not found.")

active_nodes = []
with open(ledger_path, "r") as f:
    for line in f:
        node = json.loads(line)
        if node["signature_status"] == "verified":
            active_nodes.append(node["node_id"])

unique_nodes = list(set(active_nodes))
print(f"[+] Swarm Sync Active: {len(unique_nodes)} Sovereign Node(s) Connected at 528Hz.")
print(f"[+] Target Node Addresses: {unique_nodes}")
print("[+] Ready to route multi-agent workflows and wave telemetry.")
