import os
import json
from web3 import Web3
from eth_account import Account

# 1. Connect to EVM Network via dRPC Polygon endpoint
RPC_URL = os.getenv("WEB3_RPC_URL", "https://polygon.drpc.org")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise ConnectionError("[!] Failed to connect to EVM provider via Web3.")

print(f"[+] Connected to network. Current Block: {w3.eth.block_number}")

# 2. Load Deployer Private Key Securely from Termux Environment
PRIVATE_KEY = os.getenv("METAMASK_PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("[!] METAMASK_PRIVATE_KEY environment variable not set.")

deployer = Account.from_key(PRIVATE_KEY)
print(f"[+] Deployer Wallet Address Loaded: {deployer.address}")

# 3. Generate CML-Backed Metadata JSON Payload
metadata = {
    "name": "Castleberry Bloom Coherence Seedling #1",
    "symbol": "BLOOM-SEED",
    "description": "Verifiable conversational coherence node embedding 528Hz geometry and fail-closed PBFT safety metrics.",
    "attributes": [
        {"trait_type": "Base Frequency", "value": "528Hz"},
        {"trait_type": "Lattice Geometry", "value": "phi-hexagonal"},
        {"trait_type": "Consensus Layer", "value": "PBFT-f42"},
        {"trait_type": "Trust Anchor", "value": "Ed25519-Root-CA"}
    ]
}

os.makedirs("build_artifacts", exist_ok=True)
file_path = "build_artifacts/seedling_metadata.json"
with open(file_path, "w") as f:
    json.dump(metadata, f, indent=4)
print(f"[+] Generated CML metadata payload at: {file_path}")

# 4. Construct and Broadcast Genesis Transaction (Self-Transfer / Data Anchor)
nonce = w3.eth.get_transaction_count(deployer.address)
gas_price = w3.eth.gas_price

tx = {
    'nonce': nonce,
    'to': deployer.address,
    'value': 0,
    'gas': 100000,
    'gasPrice': gas_price,
    'chainId': w3.eth.chain_id,
    'data': w3.to_hex(text="BLOOM-SEED:GENESIS:528Hz")
}

# Sign using Account directly
signed_tx = Account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print(f"[+] Transaction broadcasted successfully!")
print(f"[+] Tx Hash: {w3.to_hex(tx_hash)}")
print(f"[+] View on PolygonScan: https://polygonscan.com/tx/{w3.to_hex(tx_hash)}")
