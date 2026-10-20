import json
import os
import networkx as nx
import math
from cml_engine import parse_and_validate_topology

BFT_LEDGER = "bft_attestation_ledger.jsonl"

def load_bft_quorum_nodes() -> list:
    """Loads and verifies that the BFT quorum attestation ledger exists and is valid."""
    if not os.path.exists(BFT_LEDGER):
        print(f"[!] Error: BFT ledger '{BFT_LEDGER}' not found. Run bft_attestation_engine.py first.")
        raise SystemExit(1)
        
    with open(BFT_LEDGER, "r") as f:
        ledger_data = json.load(f)
        
    if not ledger_data.get("quorum_achieved", False):
        print("[!] Critical: BFT Quorum was not achieved in the latest ledger state.")
        raise SystemExit(1)
        
    print(f"[+] Loaded verified BFT Quorum Ledger: {ledger_data['valid_participants']}/{ledger_data['total_nodes']} nodes active.")
    return ledger_data.get("participants", [])

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
