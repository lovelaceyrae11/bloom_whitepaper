# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import tarfile
import time
import os

def package_offline_backup():
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
    archive_name = f"castleberry_bloom_offline_backup_{timestamp}.tar.gz"
    
    # Critical sovereign assets to include
    target_files = [
        "Certificate_of_Ownership.txt",
        "signed_chain_checkpoint.json",
        "castleberry_bloom_dilithium_private.b64",
        "castleberry_bloom_dilithium_private.b64.enc",
        "castleberry_bloom_dilithium_public.key",
        "shell_12_hybrid_expansion.json"
    ]
    
    # Also grab any cml logs or json ledgers present in the directory
    for f in os.listdir("."):
        if (f.endswith(".cml") or f.endswith(".json") or f.endswith(".log")) and f not in target_files:
            target_files.append(f)
            
    print(f"[*] Packaging {len(target_files)} sovereign files into secure archive...")
    
    with tarfile.open(archive_name, "w:gz") as tar:
        for file in target_files:
            if os.path.exists(file):
                tar.add(file)
                print(f"  [+] Added: {file}")
            else:
                print(f"  [-] Skipped (not found): {file}")
                
    archive_size = os.path.getsize(archive_name)
    print(f"\n[✓] Offline backup archive successfully created!")
    print(f"[*] Filename: {archive_name}")
    print(f"[*] Size: {archive_size} bytes")

if __name__ == "__main__":
    package_offline_backup()
