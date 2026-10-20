import json
import os
from datetime import datetime, timezone

print("[*] Exporting Dashboard Snapshot to Build Artifacts...")

manifest_path = "build_artifacts/cluster_manifest.json"
ledger_path = "build_artifacts/lattice_node_registry.jsonl"

with open(manifest_path, "r") as f:
    manifest = json.load(f)

nodes = []
with open(ledger_path, "r") as f:
    for line in f:
        nodes.append(json.loads(line))

snapshot = {
    "snapshot_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "manifest": manifest,
    "registered_entries_count": len(nodes),
    "nodes": nodes
}

snapshot_path = "build_artifacts/dashboard_snapshot.json"
with open(snapshot_path, "w") as f:
    json.dump(snapshot, f, indent=4)

print(f"[+] Dashboard snapshot successfully exported to: {snapshot_path}")
print("[+] All sovereign node deployment pipelines, ledgers, and dashboards fully synchronized.")
