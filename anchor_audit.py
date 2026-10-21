# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import os
import subprocess
import hashlib
from typing import Optional

AUDIT_LOG_FILE = "secure_audit_trail.jsonl"
OTS_PROOF_FILE = f"{AUDIT_LOG_FILE}.ots"

def compute_exact_file_hash(filepath: str) -> Optional[str]:
    if not os.path.exists(filepath):
        print(f"[!] Error: Audit log '{filepath}' not found.")
        return None
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()
    print(f"[*] Audit Log Exact Byte SHA-256: {file_hash}")
    return file_hash

def stamp_audit_log(filepath: str):
    if not os.path.exists(filepath):
        return
    print(f"[*] Submitting exact byte state of {filepath} to OpenTimestamps...")
    try:
        result = subprocess.run(["ots", "stamp", filepath], capture_output=True, text=True, check=True)
        print(f"[+] Success: Proof generated at {OTS_PROOF_FILE}")
        print(result.stdout)
    except Exception as e:
        print(f"[!] Stamping Error: {e}")

def verify_ots_proof(filepath: str):
    proof_path = f"{filepath}.ots"
    if not os.path.exists(proof_path):
        return
    print(f"[*] Verifying OpenTimestamps proof matches current file bytes...")
    try:
        result = subprocess.run(["ots", "verify", proof_path], capture_output=True, text=True, check=True)
        print(result.stdout)
        print("[+] SUCCESS: .ots proof matches current audit-log bytes.")
    except Exception as e:
        print(f"[!] Verification Output:\n{e}")

if __name__ == "__main__":
    print("==================================================")
    print("    STRICT BYTE-LEVEL OTS ANCHOR VERIFICATION    ")
    print("==================================================")
    if os.path.exists(OTS_PROOF_FILE):
        os.remove(OTS_PROOF_FILE)
    file_hash = compute_exact_file_hash(AUDIT_LOG_FILE)
    if file_hash:
        stamp_audit_log(AUDIT_LOG_FILE)
        verify_ots_proof(AUDIT_LOG_FILE)
