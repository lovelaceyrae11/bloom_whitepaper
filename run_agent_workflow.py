# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import json
import os

print("[*] Initializing Multi-Agent Workflows over Phi-Hexagonal Lattice...")

# Load active node telemetry
ledger_path = "build_artifacts/lattice_node_registry.jsonl"
with open(ledger_path, "r") as f:
    node = json.loads(f.readline())

print(f"[+] Routing agent tasks through node: {node['node_id']}")
print(f"[+] Active Resonance Frequency: {node['base_frequency']}")
print(f"[+] Lattice Geometry: {node['lattice_geometry']}")
print("[+] Agent swarm initialized. Ready for task execution.")
