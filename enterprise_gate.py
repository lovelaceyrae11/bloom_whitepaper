# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import os
import sys

def verify_commercial_license():
    key = os.environ.get("BLOOM_ENTERPRISE_KEY", "")
    if key != "GKV-MASTER-DEV-2026":
        print("\n" + "="*72)
        print("🛡️  CASTLEBERRY BLOOM SOVEREIGN ENGINE — COMMERCIAL LICENSE GATE")
        print("="*72)
        print("You are running the Open-Core Evaluation Edition (AGPLv3).")
        print("The 127-Node PBFT Consensus Engine, Multi-View Primary Rotation, and")
        print("SHA-256 Certified Compliance PDF Generator are locked in the Commercial Vault.")
        print("\nTO UNLOCK PRODUCTION DEPLOYMENT & CLOSED-SOURCE EXEMPTION:")
        print("  • Tier 1 ($499)       : Single Certified Network & AI Pipeline SHA-256 Audit PDF")
        print("  • Tier 2 ($5,000/yr)  : Commercial Dual-License Exemption + Guardrail Kit Key")
        print("  • Tier 3 ($25,000/yr) : Full 127-Node Sovereign Telemetry & PBFT Deployment")
        print("\n👉 Request License Key / Invoice : loveovergod@gmail.com")
        print("👉 Storefront & Documentation    : https://github.com/lovelaceyrae11/bloom_store")
        print("="*72 + "\n")
        return False
    return True

if __name__ == "__main__":
    verify_commercial_license()
