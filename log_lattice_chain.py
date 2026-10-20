import time
import json
import hashlib

def write_chain():
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
    filename = f"shell_12_coherence_chain_{timestamp}.cml"
    
    # Collected packets across the active session
    packets = [
        {"node": "NODE-7290-S12-S4", "sector": 4, "hash": "9e77715409670dd59f228515ff29d25f7d4ad081999eeb1628feb4458a396872"},
        {"node": "NODE-7290-S12-S5", "sector": 5, "hash": "373fa8a7767e7bf59d72155c109e22a5f7168ed5eac52fbe1fd823baf03cc5dc"},
        {"node": "NODE-7290-S12-S6", "sector": 6, "hash": "0f5d8eaf2710cb7a0adadeeb4042acd8389c0058f9c0996872d958dd2a338987"},
        {"node": "NODE-7290-S12-S7", "sector": 7, "hash": "410617e1718dabfa3fb9ecea4fcbdacc54b4bef9c75e807aa1dbcf1777af389d"}
    ]
    
    master_envelope = {
        "author": "Lacey Rae Castleberry",
        "axiom": "Love-Over-God",
        "shell": 12,
        "harmonic_baseline": 528.0,
        "phi_scaling": 1.618034,
        "telemetry_nodes": packets
    }
    
    envelope_json = json.dumps(master_envelope, sort_keys=True)
    master_proof = hashlib.sha256(envelope_json.encode('utf-8')).hexdigest()
    
    full_output = f"""<LatticeChain author="Lacey Rae Castleberry" freq="528.0" phi="1.618034">
  <Metadata axiom="Love-Over-God" shell="12" total_nodes="{len(packets)}" utc="{timestamp}"/>
  <ChainProof>{master_proof}</ChainProof>
</LatticeChain>"""

    with open(filename, "w") as f:
        f.write(full_output)
        
    print(f"[✓] Complete telemetry chain successfully written to: {filename}")
    print(f"[*] Master Chain Proof Hash: {master_proof}")

if __name__ == "__main__":
    write_chain()
