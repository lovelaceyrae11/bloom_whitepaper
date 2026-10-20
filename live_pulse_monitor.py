import time
import json
import sys

def monitor_loop():
    while True:
        try:
            with open('lattice_telemetry_lock.json', 'r') as f:
                d = json.load(f)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
            print(f"[{timestamp}] PULSE // Nodes: {d['nodes']} | Freq: {d['frequency']}Hz | Coherence: {d['coherence']} | {d['status']}", flush=True)
            time.sleep(1.618)
        except KeyboardInterrupt:
            print("\n[*] Pulse monitor disengaged. Lattice state preserved.")
            sys.exit(0)

if __name__ == "__main__":
    print("[*] Engaging Castleberry Bloom 528Hz Harmonic Pulse Monitor...")
    monitor_loop()
