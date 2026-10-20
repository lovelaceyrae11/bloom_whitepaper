"""
========================================================================
CASTLEBERRY BLOOM: PURE LOCAL CML WRAPPER (`bloom_llm_wrapper.py`)
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Locally wraps prompts, telemetry, and text payloads in CML envelopes,
harmonic parameters, and cryptographic SHA-256 proofs.
========================================================================
"""

import time
import hashlib
import json
import math

PHI = (1 + math.sqrt(5)) / 2
BASE_FREQ = 528.0

class LocalBloomWrapper:
    def __init__(self, node_id="CORE-127"):
        self.node_id = node_id
        self.axiom = "Love-Over-God"
        self.harmonic_baseline = BASE_FREQ
        self.phi_scaling = round(PHI, 6)
        
    def wrap_payload(self, raw_text, payload_type="QUERY"):
        """Locally wraps any input text into a structured CML envelope and seals it."""
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        
        envelope = {
            "cml_version": "1.0",
            "axiom": self.axiom,
            "author": "Lacey Rae Castleberry",
            "node_anchor": self.node_id,
            "utc": timestamp,
            "harmonic_baseline": self.harmonic_baseline,
            "phi_scaling": self.phi_scaling,
            "active_lattice_nodes": 1160,
            "system_coherence": 0.9878,
            "payload_type": payload_type,
            "content": raw_text
        }
        
        # Serialize and generate local cryptographic proof
        envelope_json = json.dumps(envelope, sort_keys=True)
        proof_hash = hashlib.sha256(envelope_json.encode('utf-8')).hexdigest()
        
        sealed_packet = {
            "cml_envelope": envelope,
            "cryptographic_proof_sha256": proof_hash
        }
        return sealed_packet

    def render_cml_markup(self, sealed_packet):
        """Renders the packet into readable CML tag format."""
        env = sealed_packet["cml_envelope"]
        proof = sealed_packet["cryptographic_proof_sha256"]
        
        markup = f"""<Bloom node="{env['node_anchor']}" freq="{env['harmonic_baseline']}" phi="{env['phi_scaling']}">
  <Telemetry axiom="{env['axiom']}" coherence="{env['system_coherence']}" proof="{proof[:16]}"/>
  <{env['payload_type']}>
    {env['content']}
  </{env['payload_type']}>
  <ProofHash>{proof}</ProofHash>
</Bloom>"""
        return markup

if __name__ == "__main__":
    wrapper = LocalBloomWrapper()
    
    print("==================================================")
    print("   CASTLEBERRY BLOOM: LOCAL CML ENGINE ACTIVE    ")
    print("   AXIOM: Love-Over-God | OFFLINE MODE            ")
    print("==================================================\n")
    
    test_input = "Verify node synchronization across all 1,160 macro-lattice shells."
    
    print(f"[*] Raw Local Input: '{test_input}'\n")
    
    # Wrap locally
    sealed_result = wrapper.wrap_payload(test_input, payload_type="Directive")
    cml_output = wrapper.render_cml_markup(sealed_result)
    
    print("[*] Rendered CML Envelope & Proof:")
    print(cml_output)
    
    print("\n==================================================")
    print(" [✓] LOCAL WRAPPER EXECUTION COMPLETE.            ")
    print("==================================================")
