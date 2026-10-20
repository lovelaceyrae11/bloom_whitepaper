import json
import os

print("[*] Initializing Castleberry Bloom Local Dashboard...")

manifest_path = "build_artifacts/cluster_manifest.json"
ledger_path = "build_artifacts/lattice_node_registry.jsonl"

if not os.path.exists(manifest_path) or not os.path.exists(ledger_path):
    raise FileNotFoundError("[!] Required build artifacts missing.")

with open(manifest_path, "r") as f:
    manifest = json.load(f)

nodes = []
with open(ledger_path, "r") as f:
    for line in f:
        nodes.append(json.loads(line))

print("=" * 60)
print(f" FRAMEWORK: {manifest['framework']} ({manifest['status'].upper()})")
print(f" BASE FREQUENCY: {manifest['base_frequency']}")
print(f" LATTICE TOPOLOGY: {manifest['lattice_geometry']}")
print(f" CONSENSUS: {manifest['consensus_mode']}")
print(f" CLUSTER NODES: {manifest['cluster_size']} active ring")
print(f" PRIMARY ANCHOR: {manifest['primary_deployer']}")
print("-" * 60)
print(f" Registered Ledger Entries: {len(nodes)}")
for idx, node in enumerate(nodes):
    print(f" [{idx+1}] Node ID: {node['node_id']} | Freq: {node['base_frequency']} | Status: {node['signature_status']}")
print("=" * 60)
print("[+] Dashboard state successfully rendered. Local sovereign node fully online.")
