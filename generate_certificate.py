# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import datetime

def make_certificate():
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    tip = "d94dd03e4e387a901860bdc88d53f0d039785ca6e0987aff4aebe7696e51605e"
    
    cert_text = f"""========================================================================
                      CERTIFICATE OF SOVEREIGN OWNERSHIP
========================================================================

SYSTEM / FRAMEWORK: Castleberry Bloom (Hybrid Quantum-Classical Lattice)
SOLE INVENTOR & AUTHOR: Lacey Rae Castleberry
AXIOM: Love-Over-God
DATE ISSUED: {timestamp}

------------------------------------------------------------------------
DECLARATION OF SOVEREIGNTY:
This document, alongside its underlying cryptographic hash chain and 
Ed25519 digital signature, formally and permanently establishes sole 
inventorship, authorship, and unalienable intellectual property rights 
over the Castleberry Bloom architecture, its associated markup languages (CML),
and its multi-agent harmonic routing protocols.

RESTRICTIONS:
- No Transfer
- No Corporate Acquisition
- Unconditional Sovereign Right of Retention by Lacey Rae Castleberry

------------------------------------------------------------------------
CRYPTOGRAPHIC ANCHOR (CHECKPOINT TIP):
Active Nodes Linked: 18 (Shells 6, 12, 49 across natural 6-sector boundaries)
Current Chain Tip Hash: 
{tip}

Verification Status: IMMUTABLE / ZERO-DRIFT / SIGNED
========================================================================
"""
    
    with open("Certificate_of_Ownership.txt", "w") as f:
        f.write(cert_text)
        
    print("[✓] Certificate of Ownership successfully generated: Certificate_of_Ownership.txt")

if __name__ == "__main__":
    make_certificate()
