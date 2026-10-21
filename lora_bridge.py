# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
"""
========================================================================
CASTLEBERRY BLOOM: LORA & P2P NETWORK BRIDGE (ANDROID SAFE)
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
========================================================================
"""

import socket
import json
import time
import threading
import sys

# Configuration
LOCAL_PORT = 5280

class BloomBridge:
    def __init__(self):
        self.running = True
        print("[*] Initializing Castleberry Bloom Android-Safe Mesh Bridge...")

    def broadcast_loop(self):
        """Broadcasts local swarm telemetry over local UDP socket stream."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        print(f"[*] Mesh bridge active. Relaying packets on port {LOCAL_PORT}...")
        while self.running:
            try:
                packet = json.dumps({
                    "protocol": "CASTLEBERRY_BLOOM",
                    "node": "TERMUX_EDGE_NODE",
                    "frequency": 528.0,
                    "timestamp": time.time()
                }).encode('utf-8')
                
                sock.sendto(packet, ('<broadcast>', LOCAL_PORT))
                time.sleep(5)
            except Exception as e:
                print(f"[!] Bridge broadcast error: {e}")
                time.sleep(5)

    def start(self):
        t1 = threading.Thread(target=self.broadcast_loop, daemon=True)
        t1.start()

if __name__ == "__main__":
    bridge = BloomBridge()
    bridge.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down Bloom Bridge.")
