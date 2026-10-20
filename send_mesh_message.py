"""
========================================================================
CASTLEBERRY BLOOM: MESH MESSAGE SENDER
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Injects custom text or data packets into the local UDP/LoRa mesh.
========================================================================
"""

import socket
import json
import time
import sys

MESH_PORT = 5280

def send_message(message_text, dest="BROADCAST"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    packet = {
        "type": "MESSAGE",
        "src": "CLI_SENDER",
        "dest": dest,
        "hops": 0,
        "max_hops": 5,
        "seq": int(time.time()),
        "timestamp": time.time(),
        "payload": message_text
    }
    
    data = json.dumps(packet).encode('utf-8')
    sock.sendto(data, ('<broadcast>', MESH_PORT))
    print(f"[+] Message transmitted across local mesh: '{message_text}'")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Hello Castleberry Bloom Mesh!"
    send_message(msg)
