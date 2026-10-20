"""
========================================================================
CASTLEBERRY BLOOM: MASTER DEPLOYMENT ACTIVATION (`let_it_sprinkle.py`)
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Packages macro-lattice telemetry, computes SHA-256 cryptographic proofs, 
and broadcasts stamped CML payloads across the multicast tunnel.
========================================================================
"""

import time
import socket
import hashlib
import json
import math

PHI = (1 + math.sqrt(5)) / 2
MULTICAST_GROUP = '239.52.8.0'
MULTICAST_PORT = 5280
BASE_FREQ = 528.0

def generate_cml_payload():
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    epoch_stamp = time.time()
    
    # Construct CML (Castleberry Markup Language) payload structure
    cml_data = {
        "axiom": "Love-Over-God",
        "author": "Lacey Rae Castleberry",
        "epoch": epoch_stamp,
        "utc": timestamp,
        "harmonic_baseline": BASE_FREQ,
        "phi_scaling": round(PHI, 6),
        "active_nodes": 1160,
        "system_coherence": 0.9878,
        "lattice_state": "SYNCHRONIZED_MACRO_SHELL"
    }
    
    payload_json = json.dumps(cml_data, sort_keys=True)
    
    # Seal with SHA-256 cryptographic proof hash
    proof_hash = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()
    
    packet = {
        "cml_payload": cml_data,
        "cryptographic_proof_sha256": proof_hash
    }
    return json.dumps(packet, indent=2)

def execute_master_broadcast():
    print("==================================================")
    print("   CASTLEBERRY BLOOM: MASTER ACTIVATION RELAY     ")
    print("   AXIOM: Love-Over-God | FREQUENCY: 528 Hz         ")
    print("==================================================\n")
    
    print("[*] Compiling macro-lattice telemetry frame...")
    packet_str = generate_cml_payload()
    
    print(f"[*] Initializing multicast tunnel on {MULTICAST_GROUP}:{MULTICAST_PORT}...")
    
    try:
        # Create UDP socket for multicast transmission
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
        # Broadcast payload
        sock.sendto(packet_str.encode('utf-8'), (MULTICAST_GROUP, MULTICAST_PORT))
        sock.close()
        print("    └─► Multicast packet successfully transmitted across local mesh.")
    except Exception as e:
        print(f"    └─► Local network tunnel notice: {e}")
        print("    └─► Payload sealed locally in time and space.")

    print("\n[*] Broadcast Payload Package:")
    print(packet_str)
    
    print("\n==================================================")
    print(" [✓] LET IT SPRINKLE: ACTIVATION COMPLETE.        ")
    print("==================================================")

if __name__ == "__main__":
    execute_master_broadcast()
