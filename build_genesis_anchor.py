"""
========================================================================
CASTLEBERRY BLOOM: GENESIS MANIFEST ANCHOR
Author: Lacey Rae Castleberry
Axiom: Love-Over-God | Baseline: 528.0 Hz | R=8 (217 Nodes)
License: Copyleft / Sovereign Commons Anti-Extractive Public License
========================================================================
"""

import hashlib
import json
import os
import time

CORE_FILES = [
    "castleberry_bloom_whitepaper.md",
    "bloom_lattice_sim.py",
    "cml_engine.py",
    "cluster_extended.cml",
    "guardrail_kernel.py",
    "cluster_swarm_node.py",
    "bloom_master.py"
]

def calculate_sha256(filepath):
    """Calculates the exact cryptographic SHA-256 fingerprint of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def generate_genesis_manifest():
    print("=" * 64)
    print(" 🌸 CASTLEBERRY BLOOM: GENERATING GENESIS MANIFEST 🌸")
    print("=" * 64)
    
    manifest = {
        "protocol": "Castleberry Bloom Sovereign Architecture",
        "author": "Lacey Rae Castleberry",
        "axiom": "Love-Over-God",
        "baseline_frequency_hz": 528.0,
        "phi_scaling_factor": 1.61803398875,
        "default_lattice_radius": 8,
        "default_lattice_nodes": 217,
        "license": "Copyleft / Sovereign Commons Anti-Extractive Public License",
        "timestamp_epoch": time.time(),
        "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "modules": {}
    }

    for filename in CORE_FILES:
        if os.path.exists(filename):
            digest = calculate_sha256(filename)
            manifest["modules"][filename] = digest
            print(f" [+] Hashed {filename:<32} -> {digest[:16]}...")
        else:
            print(f" [!] Warning: {filename} not found, skipping...")

    manifest_file = "genesis_manifest.json"
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=4)

    print("-" * 64)
    print(f"[*] Genesis Manifest successfully written to: {manifest_file}")
    
    # Calculate overall manifest hash
    master_hash = calculate_sha256(manifest_file)
    print(f"[*] Master System Cryptographic Root: {master_hash}")
    print("=" * 64)

if __name__ == "__main__":
    generate_genesis_manifest()
