# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import os
import json
import xml.etree.ElementTree as ET
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ed25519

CML_FILE = "cluster_extended.cml"
LEDGER_FILE = "pbft_consensus_ledger.jsonl"

def verify_pki_and_pbft():
    print("==================================================")
    print(" INDEPENDENT PKI & PBFT CONSENSUS VERIFIER       ")
    print("==================================================")
    
    if not os.path.exists(CML_FILE) or not os.path.exists(LEDGER_FILE):
        print(f"[!] Error: Artifacts missing.")
        raise SystemExit(1)
        
    # 1. Parse Root CA and EK Certificates from CML
    print(f"[*] Parsing Root CA and EK certificates from '{CML_FILE}'...")
    tree = ET.parse(CML_FILE)
    root = tree.getroot()
    
    root_ca_attr = root.get("root_ca_pem")
    if not root_ca_attr:
        print("[!] Error: 'root_ca_pem' missing from CML root. Re-run generate_cluster.py.")
        raise SystemExit(1)
        
    root_ca_pem = root_ca_attr.replace("\\n", "\n").encode('utf-8')
    root_ca_cert = x509.load_pem_x509_certificate(root_ca_pem)
    ca_pub_key = root_ca_cert.public_key()
    
    node_public_keys = {}
    
    for tier in root.findall("Tier"):
        for node in tier.findall("Node"):
            nid = node.get("node_id")
            pub_hex = node.get("public_key")
            ek_pem = node.get("ek_certificate").replace("\\n", "\n").encode('utf-8')
            
            # Verify EK Certificate chain against Root CA
            cert = x509.load_pem_x509_certificate(ek_pem)
            ca_pub_key.verify(cert.signature, cert.tbs_certificate_bytes)
                
            node_public_keys[nid] = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex))
            
    print(f"[*] Successfully validated EK certificate trust chains for all {len(node_public_keys)} nodes.")

    # 2. Inspect PBFT Consensus Ledger
    print(f"[*] Verifying Multi-Phase PBFT consensus ledger '{LEDGER_FILE}'...")
    with open(LEDGER_FILE, "r") as f:
        ledger = json.load(f)
        
    quorum = ledger.get("quorum_threshold")
    proposal = ledger.get("proposal")
    primary = proposal["primary"]
    
    # Verify Pre-Prepare Signature
    proposal_bytes = json.dumps(proposal, sort_keys=True).encode('utf-8')
    node_public_keys[primary].verify(bytes.fromhex(ledger["pre_prepare_signature"]), proposal_bytes)
    print(f"[*] Pre-Prepare phase verified for primary '{primary}'.")
    
    # Verify Prepare Phase Quorum
    prepares = ledger.get("prepare_votes")
    if len(prepares) < quorum:
        print("[!] Prepare quorum failed.")
        raise SystemExit(1)
        
    for vote in prepares:
        nid = vote["node_id"]
        vote_msg = f"PREPARE:{proposal['sequence']}:{proposal['state_root']}:{nid}".encode('utf-8')
        node_public_keys[nid].verify(bytes.fromhex(vote["signature"]), vote_msg)
    print(f"[*] Verified {len(prepares)} valid cryptographic PREPARE votes.")

    # Verify Commit Phase Quorum
    commits = ledger.get("commit_votes")
    if len(commits) < quorum:
        print("[!] Commit quorum failed.")
        raise SystemExit(1)
        
    for vote in commits:
        nid = vote["node_id"]
        commit_msg = f"COMMIT:{proposal['sequence']}:{proposal['state_root']}:{nid}".encode('utf-8')
        node_public_keys[nid].verify(bytes.fromhex(vote["signature"]), commit_msg)
    print(f"[*] Verified {len(commits)} valid cryptographic COMMIT votes.")

    # 3. Verify Ledger State Hash
    stored_hash = ledger.get("ledger_hash")
    ledger_copy = {k: v for k, v in ledger.items() if k != "ledger_hash"}
    computed_hash = hashlib.sha256(json.dumps(ledger_copy, sort_keys=True).encode()).hexdigest()
    
    if stored_hash != computed_hash:
        print("[!] Ledger hash mismatch!")
        raise SystemExit(1)
        
    print(f"[*] Ledger Hash Verified: {stored_hash}")
    print("\n[+] SUCCESS: FULL PKI & MULTI-PHASE PBFT INDEPENDENT VERIFICATION PASSED.")

if __name__ == "__main__":
    verify_pki_and_pbft()
