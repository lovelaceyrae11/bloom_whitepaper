# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import subprocess
import os

print("[*] Staging and committing CML specification artifact...")

if not os.path.exists(".git"):
    subprocess.run(["git", "init"], check=True)

# Explicitly add files inside build_artifacts/
subprocess.run(["git", "add", "build_artifacts/bloom_spec.cml", "build_artifacts/dashboard_snapshot.json", "build_artifacts/cluster_manifest.json", "build_artifacts/lattice_node_registry.jsonl", "build_artifacts/offline_genesis_proof.json"], check=True)
subprocess.run(["git", "commit", "-m", "chore: seal sovereign node deployment and compile CML Bloom specification"], check=True)

print("[+] Git commit complete. Sovereign artifacts locked to local version history.")
