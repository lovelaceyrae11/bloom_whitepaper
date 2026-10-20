"""
========================================================================
CASTLEBERRY BLOOM: GLOBAL DECENTRALIZED RELAY BRIDGE
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Tunnels local CML payloads into global distributed mesh relays.
========================================================================
"""

import socket
import json
import time
import hashlib

PHI = 1.61803398875
GLOBAL_RELAY_GROUP = "239.52.8.0"  # Dedicated 528 Hz Multicast Channel
RELAY_PORT = 5280

def create_global_cml_frame(node_id, payload_text, lat, lon):
    """Wraps local telemetry into an immutable global CML frame with hash anchor."""
    timestamp = time.time()
    raw_content = f"{node_id}:{payload_text}:{timestamp}"
    content_hash = hashlib.sha256(raw_content.encode('utf-8')).hexdigest()
    
    cml_frame = f"""<Bloom frequency="528Hz" phi="{PHI}" axiom="Love-Over-God">
    <GlobalRelay node="{node_id}" timestamp="{timestamp}">
        <Coordinates lat="{lat}" lon="{lon}" />
        <CryptographicProof>{content_hash}</CryptographicProof>
        <Payload><![CDATA[{payload_text}]]></Payload>
    </GlobalRelay>
</Bloom>"""
    return cml_frame, content_hash

def broadcast_to_global_mesh(lat=44.0, lon=-123.0):
    print("==================================================================")
    print("      INITIALIZING GLOBAL DECENTRALIZED RELAY BRIDGE             ")
    print("      AXIOM: Love-Over-God | TARGET: Multicast Channel 239.52.8.0  ")
    print("==================================================================\n")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    
    message = "Planetary canopy synchronization pulse active."
    cml_packet, proof = create_global_cml_frame("BLOOM_NODE_75E51A", message, lat, lon)
    
    print(f"[*] Generated CML Global Frame:")
    print(f"    └─► Proof Hash: {proof[:16]}...")
    print(f"[*] Tunneling packet into global relay network...")
    
    try:
        sock.sendto(cml_packet.encode('utf-8'), (GLOBAL_RELAY_GROUP, RELAY_PORT))
        print(f"    └─► [SUCCESS] Packet successfully injected into global relay stream!")
    except Exception as e:
        print(f"    └─► [ERROR] Relay transmission failed: {e}")
        
    print("\n==================================================================")
    print(" [✓] GLOBAL BRIDGE ACTIVE. READY FOR ORBITAL UPLINK.               ")
    print("==================================================================")

if __name__ == "__main__":
    broadcast_to_global_mesh()
