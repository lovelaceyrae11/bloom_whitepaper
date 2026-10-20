import os
import subprocess
import hashlib

LEDGER_FILE = "pbft_consensus_ledger.jsonl"
OTS_FILE = f"{LEDGER_FILE}.ots"

def stamp_ledger():
    if not os.path.exists(LEDGER_FILE):
        print(f"[!] Error: {LEDGER_FILE} not found.")
        return
        
    with open(LEDGER_FILE, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        
    print(f"[*] PBFT Consensus Ledger SHA-256: {file_hash}")
    print(f"[*] Submitting ledger to OpenTimestamps decentralized calendars...")
    
    try:
        subprocess.run(["ots", "stamp", LEDGER_FILE], check=True, capture_output=True, text=True)
        print(f"[+] Success: OpenTimestamps proof generated at {OTS_FILE}")
    except Exception as e:
        print(f"[!] Stamping error: {e}")

if __name__ == "__main__":
    print("==================================================")
    print(" PBFT LEDGER BITCOIN TIMESTAMP ANCHORING         ")
    print("==================================================")
    stamp_ledger()
