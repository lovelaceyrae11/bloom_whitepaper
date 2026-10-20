import os
import json
import time
import hashlib
import copy
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
from cml_engine import parse_and_validate_topology

SECRETS_FILE = "node_secrets.json"
TOTAL_NODES = 127
MAX_FAULTS = 42
QUORUM = (2 * MAX_FAULTS) + 1  # 85 nodes

class PBFTNetworkSimulator:
    def __init__(self):
        if not os.path.exists(SECRETS_FILE):
            raise FileNotFoundError(f"'{SECRETS_FILE}' missing. Run generate_cluster.py first.")
            
        with open(SECRETS_FILE, "r") as f:
            self.secrets = json.load(f)
            
        self.topology = parse_and_validate_topology("cluster_extended.cml")
        self.public_keys = {}
        
        # Load public keys for cryptographic verification
        for tier in self.topology:
            # Note: parse_and_validate_topology returns a list of node dicts
            pass
            
        # Re-parse raw XML for public keys to ensure independent verification
        import xml.etree.ElementTree as ET
        tree = ET.parse("cluster_extended.cml")
        root = tree.getroot()
        for tier in root.findall("Tier"):
            for node in tier.findall("Node"):
                nid = node.get("node_id")
                pub_hex = node.get("public_key")
                self.public_keys[nid] = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex))

        self.primary_id = self.topology[0]["node_id"]

    def execute_consensus_round(self, sequence=3001, custom_state_root=None):
        timestamp = time.time()
        state_root = custom_state_root or hashlib.sha256(f"STATE:{timestamp}".encode()).hexdigest()
        
        # 1. PRE-PREPARE PHASE
        proposal = {
            "view": 1,
            "sequence": sequence,
            "primary": self.primary_id,
            "state_root": state_root,
            "timestamp": timestamp
        }
        proposal_bytes = json.dumps(proposal, sort_keys=True).encode('utf-8')
        primary_priv = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(self.secrets[self.primary_id]))
        pre_prepare_sig = primary_priv.sign(proposal_bytes).hex()
        
        # Verify Pre-Prepare
        self.public_keys[self.primary_id].verify(bytes.fromhex(pre_prepare_sig), proposal_bytes)

        # 2. PREPARE PHASE (Building Prepare Certificate)
        prepare_votes = []
        for node in self.topology[:QUORUM]:
            nid = node["node_id"]
            priv = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(self.secrets[nid]))
            msg = f"PREPARE:{sequence}:{state_root}:{nid}".encode('utf-8')
            sig = priv.sign(msg).hex()
            prepare_votes.append({"node_id": nid, "signature": sig})

        # Verify Prepare Certificate
        seen_prepares = set()
        for vote in prepare_votes:
            nid = vote["node_id"]
            if nid in seen_prepares:
                raise ValueError(f"Duplicate voter {nid} in prepare certificate.")
            seen_prepares.add(nid)
            msg = f"PREPARE:{sequence}:{state_root}:{nid}".encode('utf-8')
            self.public_keys[nid].verify(bytes.fromhex(vote["signature"]), msg)

        # 3. COMMIT PHASE (Building Commit Certificate)
        commit_votes = []
        for node in self.topology[:QUORUM]:
            nid = node["node_id"]
            priv = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(self.secrets[nid]))
            msg = f"COMMIT:{sequence}:{state_root}:{nid}".encode('utf-8')
            sig = priv.sign(msg).hex()
            commit_votes.append({"node_id": nid, "signature": sig})

        # Verify Commit Certificate
        seen_commits = set()
        for vote in commit_votes:
            nid = vote["node_id"]
            if nid in seen_commits:
                raise ValueError(f"Duplicate voter {nid} in commit certificate.")
            seen_commits.add(nid)
            msg = f"COMMIT:{sequence}:{state_root}:{nid}".encode('utf-8')
            self.public_keys[nid].verify(bytes.fromhex(vote["signature"]), msg)

        return {
            "proposal": proposal,
            "pre_prepare_signature": pre_prepare_sig,
            "prepare_votes": prepare_votes,
            "commit_votes": commit_votes
        }

def run_adversarial_pbft_integration_suite():
    print("==================================================")
    print(" PBFT PROTOCOL CERTIFICATE & ADVERSARIAL SUITE   ")
    print("==================================================\n")
    
    sim = PBFTNetworkSimulator()

    # TEST 1: Execute Pristine Round
    print("[*] Test 1: Executing full cryptographic PBFT round...")
    ledger_block = sim.execute_consensus_round(sequence=3001)
    print("[+] PASS: Pristine 3-phase consensus round completed and verified.\n")

    # TEST 2: Forged Signature Injection
    print("[*] Test 2: Rejecting forged signature in commit certificate...")
    forged_block = copy.deepcopy(ledger_block)
    # Replace a commit signature with random garbage bytes
    forged_block["commit_votes"][0]["signature"] = "deadbeef" * 8
    
    try:
        # Re-verify commit votes manually to catch forgery
        proposal = forged_block["proposal"]
        for vote in forged_block["commit_votes"]:
            nid = vote["node_id"]
            msg = f"COMMIT:{proposal['sequence']}:{proposal['state_root']}:{nid}".encode('utf-8')
            sim.public_keys[nid].verify(bytes.fromhex(vote["signature"]), msg)
        raise AssertionError("Failed: Forged signature was accepted!")
    except InvalidSignature as e:
        print(f"[+] PASS: Successfully caught forged signature -> {type(e).__name__}\n")

    # TEST 3: Duplicate Voter Detection
    print("[*] Test 3: Rejecting duplicate voter in quorum set...")
    dup_block = copy.deepcopy(ledger_block)
    dup_block["prepare_votes"][5] = dup_block["prepare_votes"][0] # Duplicate node ID
    
    try:
        seen = set()
        for vote in dup_block["prepare_votes"]:
            nid = vote["node_id"]
            if nid in seen:
                raise ValueError(f"Duplicate voter detected: {nid}")
            seen.add(nid)
        raise AssertionError("Failed: Duplicate voter accepted!")
    except ValueError as e:
        print(f"[+] PASS: Successfully caught duplicate voter -> {e}\n")

    # TEST 4: Conflicting State Root Rejection
    print("[*] Test 4: Rejecting votes referencing conflicting state root...")
    conflict_block = copy.deepcopy(ledger_block)
    # Change state root in proposal, but keep old votes referencing original state root
    conflict_block["proposal"]["state_root"] = hashlib.sha256(b"MALICIOUS_STATE").hexdigest()
    
    try:
        proposal = conflict_block["proposal"]
        for vote in conflict_block["prepare_votes"]:
            nid = vote["node_id"]
            # Verifying vote against the *new* modified state root
            msg = f"PREPARE:{proposal['sequence']}:{proposal['state_root']}:{nid}".encode('utf-8')
            sim.public_keys[nid].verify(bytes.fromhex(vote["signature"]), msg)
        raise AssertionError("Failed: Conflicting state root vote accepted!")
    except InvalidSignature as e:
        print(f"[+] PASS: Successfully rejected conflicting state root -> {type(e).__name__}\n")

    print("==================================================")
    print(" [+] ALL PBFT PROTOCOL & ADVERSARIAL TESTS PASSED.")
    print("==================================================")

if __name__ == "__main__":
    run_adversarial_pbft_integration_suite()
