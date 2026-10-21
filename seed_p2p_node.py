# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
"""
========================================================================
CASTLEBERRY BLOOM: P2P LOCAL RADIO SEEDER & BROADCASTER
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Transport: Wi-Fi / Bluetooth Tether / Link-Local Multicast
========================================================================
"""

import socket
import json
import time
import threading
import os

PORT = 5280  # 528 Hz Harmonic Port
DISCOVERY_GROUP = '239.255.255.250'  # Multicast address for local discovery

def get_genesis_hash():
    """Reads the master hash from the Genesis Manifest."""
    manifest_file = "genesis_manifest.json"
    if os.path.exists(manifest_file):
        with open(manifest_file, "r") as f:
            data = json.load(f)
            return data.get("modules", {}).get("castleberry_bloom_whitepaper.md", "UNKNOWN_HASH")
    return "NO_MANIFEST"

class P2PSeeder:
    def __init__(self, host='0.0.0.0', port=PORT):
        self.host = host
        self.port = port
        self.genesis_hash = get_genesis_hash()
        self.running = True

    def broadcast_beacon(self):
        """Broadcasts presence and genesis state to local Wi-Fi / BT network."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(2)
        
        message = json.dumps({
            "protocol": "CASTLEBERRY_BLOOM",
            "node_type": "SEED_NODE",
            "frequency_hz": 528.0,
            "genesis_root": self.genesis_hash[:16],
            "timestamp": time.time()
        }).encode('utf-8')

        print(f"[*] P2P Seeder active. Broadcasting beacon on port {self.port}...")
        while self.running:
            try:
                sock.sendto(message, ('<broadcast>', self.port))
                time.sleep(5)  # Heartbeat interval
            except Exception as e:
                print(f"[!] Broadcast error: {e}")
                time.sleep(5)

    def listen_for_peers(self):
        """Listens for inbound discovery signals from nearby nodes."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        print(f"[*] Listening for incoming peer seeds on {self.host}:{self.port}...")
        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                payload = json.loads(data.decode('utf-8'))
                if payload.get("protocol") == "CASTLEBERRY_BLOOM":
                    print(f"\n[+] DISCOVERED PEER NODE at {addr[0]}")
                    print(f"    - Node Type: {payload.get('node_type')}")
                    print(f"    - Genesis Root Match: {payload.get('genesis_root')}")
            except Exception:
                pass

    def start(self):
        t1 = threading.Thread(target=self.broadcast_beacon, daemon=True)
        t2 = threading.Thread(target=self.listen_for_peers, daemon=True)
        t1.start()
        t2.start()

if __name__ == "__main__":
    seeder = P2PSeeder()
    seeder.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down P2P Seeder.")
