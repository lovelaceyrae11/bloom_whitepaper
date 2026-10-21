# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import time
import json
import hashlib

def extend_lattice_chain():
    # Previous chain tip from v1.2-CHAINED
    previous_tip = "d94dd03e4e387a901860bdc88d53f0d039785ca6e0987aff4aebe7696e51605e"
    target_shell = 55
    
    print(f"[*] Extending chain from previous tip: {previous_tip[:16]}...")
    
    current_prior_hash = previous_tip
    new_nodes_ledger = []
    
    # Simulate generating nodes across sectors 1 to 6 for Shell 55
    for sector in range(1, 7):
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        node_id = f"NODE-7290-S{target_shell}-S{sector}"
        
        node_payload = {
            "cml_version": "1.2-CHAINED",
            "axiom": "Love-Over-God",
            "author": "Lacey Rae Castleberry",
            "restriction": "NO_TRANSFER_NO_CORPORATE_ACQUISITION",
            "node_id": node_id,
            "shell_index": target_shell,
            "sector": sector,
            "utc": timestamp,
            "harmonic_baseline": 528.0,
            "phi_scaling": 1.618034,
            "system_coherence": 0.9878,
            "prior_proof_hash": current_prior_hash
        }
        
        payload_json = json.dumps(node_payload, sort_keys=True)
        new_proof_hash = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()
        
        new_nodes_ledger.append({
            "node_id": node_id,
            "sector": sector,
            "proof_hash": new_proof_hash
        })
        
        # Advance the chain tip
        current_prior_hash = new_proof_hash

    checkpoint_record = {
        "parent_chain_tip": previous_tip,
        "extended_shell": target_shell,
        "new_tip": current_prior_hash,
        "nodes_added": new_nodes_ledger
    }
    
    filename = f"shell_{target_shell}_expansion_chained.json"
    with open(filename, "w") as f:
        json.dump(checkpoint_record, f, indent=2)
        
    print(f"[✓] Shell {target_shell} successfully chained and written to: {filename}")
    print(f"[*] NEW CHAIN TIP: {current_prior_hash}")

if __name__ == "__main__":
    extend_lattice_chain()
