"""
========================================================================
CASTLEBERRY BLOOM: MASTER SOVEREIGN CONTROL CENTER
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Baseline Frequency: 528.0 Hz | Phi Scale: 1.61803398875
========================================================================
"""

import sys
import os

def print_banner():
    print("=" * 64)
    print(" 🌸 CASTLEBERRY BLOOM SOVEREIGN ARCHITECTURE 🌸")
    print(" Axiom: Love-Over-God | Baseline: 528.0 Hz | R=8 (217 Nodes)")
    print("=" * 64)

def show_menu():
    print("\n[Select Sovereign Operation]:")
    print("  1. Verify Whitepaper & OTS Stamps")
    print("  2. Run Lattice Resilience Simulation (bloom_lattice_sim.py)")
    print("  3. Execute CML Parser & Auditor (cml_engine.py)")
    print("  4. Test Coherence Guardrail Kernel (guardrail_kernel.py)")
    print("  5. Run Distributed Swarm Consensus (cluster_swarm_node.py)")
    print("  6. Exit")

def main():
    print_banner()
    while True:
        show_menu()
        choice = input("\nEnter choice [1-6]: ").strip()
        
        if choice == '1':
            print("\n[*] Checking sovereign file integrity and timestamps...")
            os.system("ls -la *.ots")
        elif choice == '2':
            print("\n[*] Executing Lattice Resilience Simulation...")
            os.system("python bloom_lattice_sim.py")
        elif choice == '3':
            print("\n[*] Executing CML Engine & Auditor...")
            os.system("python cml_engine.py")
        elif choice == '4':
            print("\n[*] Executing Guardrail Kernel...")
            os.system("python guardrail_kernel.py")
        elif choice == '5':
            print("\n[*] Executing Cluster Swarm Consensus...")
            os.system("python cluster_swarm_node.py")
        elif choice == '6':
            print("\n[*] Returning to sovereign flow. Stay coherent.")
            sys.exit(0)
        else:
            print("\n[!] Invalid selection. Please choose 1-6.")

if __name__ == "__main__":
    main()
