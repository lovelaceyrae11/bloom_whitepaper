# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import json
import os
import networkx as nx
import math
from pathlib import Path
from cml_engine import parse_and_validate_topology
from independent_verifier_v4 import (
    VerificationError,
    load_and_verify_trust_anchor,
    verify_pbft_consensus,
)

# Separate production ledger. Never use the staged test ledger here.
BFT_LEDGER = Path(__file__).with_name("pbft_v4_ledger.json")
CML_FILE = Path(__file__).with_name("cluster_extended.cml")
_EXECUTED_SEQUENCES = {}  # In-memory replay guard only.

def load_bft_quorum_nodes() -> list:
    """Return COMMIT voters only after independent cryptographic verification."""
    if not BFT_LEDGER.is_file():
        raise SystemExit(
            f"SECURITY STOP: verified PBFT ledger not found: {BFT_LEDGER}. "
            "Legacy and staged test ledgers are not accepted."
        )

    try:
        with BFT_LEDGER.open("r", encoding="utf-8") as ledger_file:
            ledger_data = json.load(ledger_file)

        node_public_keys, _, _ = load_and_verify_trust_anchor(CML_FILE)
        verify_pbft_consensus(
            ledger_data,
            node_public_keys,
            executed_sequences=_EXECUTED_SEQUENCES,
        )

        participants = sorted({
            vote["node_id"] for vote in ledger_data["commit_votes"]
        })
        print(
            f"[+] Independently verified PBFT ledger: "
            f"{len(participants)}/127 valid COMMIT voters."
        )
        return participants

    except (OSError, json.JSONDecodeError, VerificationError) as exc:
        raise SystemExit(
            f"SECURITY STOP: PBFT ledger verification failed: {exc}"
        ) from None

def build_phi_hexagonal_execution_graph():
    print("==================================================")
    print("    PHI-HEXAGONAL SWARM EXECUTION BRIDGE         ")
    print("==================================================")
    
    # 1. Verify BFT quorum state before executing topology
    quorum_participants = load_bft_quorum_nodes()
    
    # 2. Parse base CML topology
    nodes = parse_and_validate_topology("cluster_extended.cml")
    
    # 3. Initialize NetworkX graph for multi-agent routing
    G = nx.Graph()
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio scaling factor
    
    print(f"[*] Constructing NetworkX graph with phi-scaled edges (Phi = {PHI:.4f})...")
    
    for node in nodes:
        node_id = node["node_id"]
        tier = node["tier"]
        freq = node["target_freq"]
        
        G.add_node(node_id, tier=tier, frequency=freq, state="ACTIVE")
        
    # 4. Establish phi-hexagonal lattice connections
    core_nodes = [n for n, d in G.nodes(data=True) if d["tier"] == "core"]
    shell_nodes = [n for n, d in G.nodes(data=True) if d["tier"] == "shell"]
    
    # Wire Core mesh
    for i in range(len(core_nodes)):
        for j in range(i + 1, len(core_nodes)):
            if abs(i - j) <= 2 or abs(i - j) == len(core_nodes) - 1:
                G.add_edge(core_nodes[i], core_nodes[j], weight=1.0 / PHI)
                
    # Wire Shell lattice to Core anchor points
    for i, shell_node in enumerate(shell_nodes):
        target_core = core_nodes[i % len(core_nodes)]
        G.add_edge(shell_node, target_core, weight=PHI)

    print(f"[*] Graph constructed successfully: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    
    # 5. Execute Harmonic Workload Propagation
    print("[*] Executing distributed harmonic resonance propagation across swarm...")
    
    core_resonance = sum(G.nodes[n]["frequency"] for n in core_nodes) / len(core_nodes)
    shell_resonance = sum(G.nodes[n]["frequency"] for n in shell_nodes) / len(shell_nodes)
    
    global_coherence = (core_resonance * (1 / PHI)) + (shell_resonance * (1 - (1 / PHI)))
    
    print(f"\n--- EXECUTION RESULTS ---")
    print(f"Core Tier Mean Frequency: {core_resonance:.2f} Hz")
    print(f"Shell Tier Mean Frequency: {shell_resonance:.2f} Hz")
    print(f"Calculated Golden-Ratio Swarm Coherence Vector: {global_coherence:.4f}")
    print("\n[+] STATUS: SWARM COMPUTATIONAL PIPELINE EXECUTED SUCCESSFULLY.")

if __name__ == "__main__":
    build_phi_hexagonal_execution_graph()
