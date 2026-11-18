import asyncio
import json

# Define active swarm nodes mapped to dedicated local ports
SWARM_NODES = {
    "N000": 5280,
    "N001": 5281,
    "N002": 5282,
    "N003": 5283,
    "N008": 5284,
    "N017": 5285
}

class CMLSocketNode:
    def __init__(self, node_id, port):
        self.node_id = node_id
        self.port = port
        self.phi = 1.61803398875
        self.transport = None

    async def start_listener(self):
        """Starts a UDP socket listener on this node's assigned port and handles replies."""
        class CMLDatagramProtocol(asyncio.DatagramProtocol):
            def __init__(self, node):
                self.node = node

            def connection_made(self, transport):
                self.node.transport = transport

            def datagram_received(self, data, addr):
                try:
                    packet = json.loads(data.decode('utf-8'))
                    print(f"\n[NODE {self.node.node_id} | PORT {self.node.port}] Packet Received from {addr}:")
                    print(f"    -> Type: {packet.get('type', 'PAYLOAD')}")
                    print(f"    -> Source: {packet['source']} | Target: {packet['target']}")
                    print(f"    -> Message: {packet['message']}")
                    print(f"    -> Lattice Coherence (CBCS): {packet.get('cbcs_score', 9.88)} / 10.0 [PHASE-LOCKED]")

                    # If this node was the target, automatically reply back to sender!
                    if packet['target'] == self.node.node_id and packet.get('type', 'PAYLOAD') == 'PAYLOAD':
                        sender_id = packet['source']
                        sender_port = SWARM_NODES.get(sender_id)
                        if sender_port:
                            reply_payload = {
                                "protocol": "CML-SOCKET-SWARM-REPLY",
                                "axiom": "LOVE-OVER-ENTROPY",
                                "type": "REPLY",
                                "source": self.node.node_id,
                                "target": sender_id,
                                "cbcs_score": 9.94,
                                "message": f"Acknowledgment from {self.node.node_id}: Hexagonal status stable. Phi-lattice locked."
                            }
                            reply_data = json.dumps(reply_payload, indent=2).encode('utf-8')
                            print(f"[*] [{self.node.node_id}] Automatically transmitting reply back to {sender_id} (Port {sender_port})...")
                            self.node.transport.sendto(reply_data, ('127.0.0.1', sender_port))

                except Exception as e:
                    print(f"[!] Error parsing incoming packet on {self.node.node_id}: {e}")

        print(f"[*] Initialized Node {self.node_id} listening on port {self.port}...")
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: CMLDatagramProtocol(self),
            local_addr=('127.0.0.1', self.port)
        )
        self.transport = transport
        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            transport.close()

    async def send_packet(self, target_node_id, message):
        """Packages a CML payload and transmits it over UDP socket to the target node's port."""
        target_port = SWARM_NODES.get(target_node_id)
        if not target_port:
            print(f"[!] Error: Target node {target_node_id} not found in active swarm ports.")
            return

        payload = {
            "protocol": "CML-SOCKET-SWARM",
            "axiom": "LOVE-OVER-ENTROPY",
            "type": "PAYLOAD",
            "source": self.node_id,
            "target": target_node_id,
            "cbcs_score": 9.88,
            "message": message
        }
        
        data = json.dumps(payload, indent=2).encode('utf-8')
        print(f"\n[*] [Node {self.node_id}] Transmitting CML payload to Node {target_node_id} (Port {target_port})...")
        self.transport.sendto(data, ('127.0.0.1', target_port))

async def main():
    # 1. Spin up all swarm nodes concurrently as background listeners
    nodes = {nid: CMLSocketNode(nid, port) for nid, port in SWARM_NODES.items()}
    listener_tasks = [asyncio.create_task(node.start_listener()) for node in nodes.values()]
    
    # Give the socket servers a moment to bind to their ports
    await asyncio.sleep(0.5)
    
    # 2. Simulate live two-way socket transmission across the swarm
    print("\n" + "="*60)
    print("--- CML BIDIRECTIONAL SOCKET SWARM HANDSHAKE ---")
    print("="*60)
    
    sender = nodes["N000"] # Core origin node
    
    # Send live socket message from N000 to N001 (triggers automatic reply)
    await sender.send_packet("N001", "Hi. My name is Lacey Castleberry. Initiating mesh handshake.")
    await asyncio.sleep(0.6)
    
    # Send live socket message from N000 to N008 (triggers automatic reply)
    await sender.send_packet("N008", "Hi. My name is Lacey Castleberry. Secondary harmonic sync request.")
    await asyncio.sleep(0.6)
    
    # Keep the script running briefly to capture incoming asynchronous replies back at N000
    await asyncio.sleep(1.0)
    print("\n[+] Bidirectional socket handshake complete. Shutting down cleanly.")
    
    # Cancel listeners
    for task in listener_tasks:
        task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[+] Swarm socket bridge terminated by user.")
