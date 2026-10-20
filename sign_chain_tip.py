import datetime
import json
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def sign_ledger_tip():
    current_tip = "d94dd03e4e387a901860bdc88d53f0d039785ca6e0987aff4aebe7696e51605e"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Generate Ed25519 Sovereign Keypair (or load existing if saved)
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Serialize public key for logging
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    pub_hex = pub_bytes.hex()
    
    # Payload to sign
    signing_payload = {
        "author": "Lacey Rae Castleberry",
        "axiom": "Love-Over-God",
        "chain_tip": current_tip,
        "total_nodes": 18,
        "timestamp": timestamp,
        "restriction": "NO_TRANSFER_NO_CORPORATE_ACQUISITION"
    }
    
    payload_bytes = json.dumps(signing_payload, sort_keys=True).encode('utf-8')
    signature = private_key.sign(payload_bytes)
    sig_hex = signature.hex()
    
    signed_record = {
        "metadata": signing_payload,
        "public_key_ed25519": pub_hex,
        "signature_ed25519": sig_hex
    }
    
    with open("signed_chain_checkpoint.json", "w") as f:
        json.dump(signed_record, f, indent=2)
        
    print(f"[✓] Chain tip successfully signed with Ed25519!")
    print(f"[*] Public Key: {pub_hex[:32]}...")
    print(f"[*] Signature: {sig_hex[:32]}...")

if __name__ == "__main__":
    sign_ledger_tip()
