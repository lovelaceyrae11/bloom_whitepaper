"""
========================================================================
CASTLEBERRY BLOOM: ADVANCED MULTI-HOP LORA MESH ROUTER
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Enables dynamic peer discovery, multi-hop packet relay, and lattice routing.
========================================================================
"""

import socket
import json
import time
import threading
import hashlib
import uuid

# Configuration
MESH_PORT = 5280
NODE_ID = f"BLOOM_NODE_{uuid.uuid4().hex[:6].upper()}"
MAX_HOPS = 7
FREQUENCY_HZ = 528.0

class DynamicMeshRouter:
    def __init__(self):
        self.node_id = NODE_ID
        self.routing_table = {}  # {node_id: {"next_hop": str, "hops": int, "last_seen": float}}
        self.seen_packets = set() # Prevent duplicate packet flooding loops
        self.running = True
        
    def generate_packet_hash(self, packet):
        payload_str = f"{packet['src']}_{packet['dest']}_{packet['seq']}_{packet['timestamp']}"
        return hashlib.sha256(payload_str.encode('utf-8')).hexdigest()[:16]

    def broadcast_heartbeat(self, sock):
        """Periodically broadcasts node presence to discover neighboring peers."""
        print(f"[*] Starting local heartbeat broadcast as {self.node_id}...")
        while self.running:
            try:
                heartbeat = {
                    "type": "HEARTBEAT",
                    "src": self.node_id,
                    "dest": "BROADCAST",
                    "hops": 0,
                    "max_hops": 1,
                    "seq": int(time.time()),
                    "timestamp": time.time(),
                    "frequency": FREQUENCY_HZ
                }
                data = json.dumps(heartbeat).encode('utf-8')
                sock.sendto(data, ('<broadcast>', MESH_PORT))
                time.sleep(15)
            except Exception as e:
                print(f"[!] Heartbeat error: {e}")
                time.sleep(5)

    def listen_and_route(self, sock):
        """Listens for radio packets, updates routing tables, and relays payloads."""
        print(f"[*] Dynamic Mesh Listening active on port {MESH_PORT}...")
        while self.running:
            try:
                data, addr = sock.recvfrom(4096)
                packet = json.loads(data.decode('utf-8'))
                
                # Check for duplicate packets to break infinite loops
                packet_id = self.generate_packet_hash(packet)
                if packet_id in self.seen_packets:
                    continue
                self.seen_packets.add(packet_id)

                src_node = packet.get("src")
                dest_node = packet.get("dest")
                hops = packet.get("hops", 0)

                # Skip self-generated packets
                if src_node == self.node_id:
                    continue

                # Update routing table with incoming node info
                self.routing_table[src_node] = {
                    "next_hop": addr[0],
                    "hops": hops + 1,
                    "last_seen": time.time()
                }

                print(f"[RADIO RX] From: {src_node} | Dest: {dest_node} | Hops: {hops}")

                # Handle packet destination logic
                if dest_node in (self.node_id, "BROADCAST"):
                    print(f"  └─► [RECEIVED] Payload processed at local node {self.node_id}.")
                
                # Multi-hop forward if message is meant for another node
                if dest_node != self.node_id and hops < packet.get("max_hops", MAX_HOPS):
                    packet["hops"] += 1
                    forward_data = json.dumps(packet).encode('utf-8')
                    print(f"  └─► [RELAYING] Multi-hop forward -> Hop count: {packet['hops']}")
                    sock.sendto(forward_data, ('<broadcast>', MESH_PORT))

            except Exception as e:
                print(f"[!] Processing error: {e}")

    def display_topology(self):
        """Displays real-time mesh routing topology."""
        while self.running:
            time.sleep(30)
            print("\n" + "="*50)
            print(f" CASTLEBERRY BLOOM: MESH TOPOLOGY TABLE ({self.node_id})")
            print("="*50)
            if not self.routing_table:
                print(" No active peer nodes detected in range yet.")
            else:
                for peer, info in list(self.routing_table.items()):
                    age = int(time.time() - info["last_seen"])
                    print(f" Peer: {peer:<18} | Next Hop IP: {info['next_hop']:<15} | Distance: {info['hops']} hops | Age: {age}s")
            print("="*50 + "\n")

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('0.0.0.0', MESH_PORT))

        t1 = threading.Thread(target=self.broadcast_heartbeat, args=(sock,), daemon=True)
        t2 = threading.Thread(target=self.listen_and_route, args=(sock,), daemon=True)
        t3 = threading.Thread(target=self.display_topology, daemon=True)

        t1.start()
        t2.start()
        t3.start()

if __name__ == "__main__":
    router = DynamicMeshRouter()
    router.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down Mesh Router.")
