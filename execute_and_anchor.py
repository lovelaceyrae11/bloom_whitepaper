import json
import os
import time
import math
import hashlib
import subprocess
import networkx as nx
from cml_engine import parse_and_validate_topology

BFT_LEDGER = "bft_attestation_ledger.jsonl"
EXEC_LOG_FILE = "swarm_execution_log.jsonl"
OTS_PROOF_FILE = f"{EXEC_LOG_FILE}.ots"

def load_bft_quorum_reference() -> str:
    if not os.path.exists(BFT_LEDGER):
        print(f"[!] Error: BFT ledger '{BFT_LEDGER}' not found.")
        raise SystemExit(1)
        
    with open(BFT_LEDGER, "r") as f:
        ledger_data = json.load(f)
        
    if not ledger_data.get("quorum_achieved", False):
        print("[!] Critical: BFT Quorum not achieved.")
        raise SystemExit(1)
        
    return ledger_data.get("ledger_hash")

def get_last_exec_chain_hash(filepath: str) -> str:
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            if not lines:
                return "0" * 64
            last_entry = json.loads(lines[-1].strip())
            return last_entry.get("hash", "0" * 64)
    except FileNotFoundError:
        return "0" * 64

def run_execution_and_anchor():
    print("==================================================")
    print("    SWARM EXECUTION & BLOCKCHAIN ANCHORING       ")
    print("==================================================")
    
    # 1. Reference verified BFT state
    bft_hash = load_bft_quorum_reference()
    print(f"[*] Referenced BFT Quorum Ledger Hash: {bft_hash[:16]}...")
    
    # 2. Parse topology & build execution graph
    nodes = parse_and_validate_topology("cluster_extended.cml")
    G = nx.Graph()
    PHI = (1 + math.sqrt(5)) / 2
    
    for node in nodes:
        G.add_node(node["node_id"], tier=node["tier"], frequency=node["target_freq"])
        
    core_nodes = [n for n, d in G.nodes(data=True) if d["tier"] == "core"]
    shell_nodes = [n for n, d in G.nodes(data=True) if d["tier"] == "shell"]
    
    for i in range(len(core_nodes)):
        for j in range(i + 1, len(core_nodes)):
            if abs(i - j) <= 2 or abs(i - j) == len(core_nodes) - 1:
                G.add_edge(core_nodes[i], core_nodes[j], weight=1.0 / PHI)
                
    for i, shell_node in enumerate(shell_nodes):
        target_core = core_nodes[i % len(core_nodes)]
        G.add_edge(shell_node, target_core, weight=PHI)
        
    # 3. Compute execution metrics
    core_resonance = sum(G.nodes[n]["frequency"] for n in core_nodes) / len(core_nodes)
    shell_resonance = sum(G.nodes[n]["frequency"] for n in shell_nodes) / len(shell_nodes)
    global_coherence = (core_resonance * (1 / PHI)) + (shell_resonance * (1 - (1 / PHI)))
    
    exec_results = {
        "bft_reference_hash": bft_hash,
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "core_mean_freq_hz": core_resonance,
        "shell_mean_freq_hz": shell_resonance,
        "golden_ratio_coherence_vector": global_coherence,
        "status": "SUCCESS"
    }
    
    # 4. Hash-chain record into execution log
    prev_hash = get_last_exec_chain_hash(EXEC_LOG_FILE)
    log_payload = {
        "prev_hash": prev_hash,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        "execution_results": exec_results
    }
    
    canonical_str = json.dumps(log_payload, sort_keys=True)
    record_hash = hashlib.sha256(canonical_str.encode()).hexdigest()
    
    final_entry = {
        **log_payload,
        "hash": record_hash
    }
    
    with open(EXEC_LOG_FILE, "a") as f:
        f.write(json.dumps(final_entry) + "\n")
        
    print(f"\n--- EXECUTION RECORD COMMITTED ---")
    print(f"Coherence Vector: {global_coherence:.4f}")
    print(f"Execution Log Hash: {record_hash}")
    
    # 5. Anchor execution log to Bitcoin via OpenTimestamps
    if os.path.exists(OTS_PROOF_FILE):
        os.remove(OTS_PROOF_FILE)
        
    print(f"\n[*] Initiating Bitcoin OpenTimestamps attestation for execution log...")
    try:
        result = subprocess.run(["ots", "stamp", EXEC_LOG_FILE], capture_output=True, text=True, check=True)
        print(f"[+] Success: Execution proof generated at {OTS_PROOF_FILE}")
        print(result.stdout)
    except Exception as e:
        print(f"[!] Stamping Error: {e}")

if __name__ == "__main__":
    run_execution_and_anchor()
