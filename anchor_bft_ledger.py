# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import os
import subprocess
import hashlib
from typing import Optional

BFT_LEDGER_FILE = "bft_attestation_ledger.jsonl"
OTS_PROOF_FILE = f"{BFT_LEDGER_FILE}.ots"

def compute_bft_ledger_hash(filepath: str) -> Optional[str]:
    if not os.path.exists(filepath):
        print(f"[!] Error: Ledger file '{filepath}' not found.")
        return None
    
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
            
    file_hash = sha256.hexdigest()
    print(f"[*] BFT Consensus Ledger SHA-256: {file_hash}")
    return file_hash

def stamp_bft_ledger(filepath: str):
    if not os.path.exists(filepath):
        return

    print(f"[*] Submitting BFT quorum consensus state to OpenTimestamps...")
    try:
        result = subprocess.run(["ots", "stamp", filepath], capture_output=True, text=True, check=True)
        print(f"[+] Success: BFT proof generated at {OTS_PROOF_FILE}")
        print(result.stdout)
    except Exception as e:
        print(f"[!] Stamping Error: {e}")

def verify_bft_proof(filepath: str):
    proof_path = f"{filepath}.ots"
    if not os.path.exists(proof_path):
        return

    print(f"[*] Verifying BFT OpenTimestamps proof...")
    try:
        result = subprocess.run(["ots", "verify", proof_path], capture_output=True, text=True, check=True)
        print(result.stdout)
    except Exception as e:
        print(f"[!] Verification Output:\n{e}")

if __name__ == "__main__":
    print("==================================================")
    print("    BFT LEDGER BITCOIN TIMESTAMP ANCHORING       ")
    print("==================================================")
    
    ledger_hash = compute_bft_ledger_hash(BFT_LEDGER_FILE)
    if ledger_hash:
        stamp_bft_ledger(BFT_LEDGER_FILE)
        verify_bft_proof(BFT_LEDGER_FILE)
