import subprocess
import sys

def execute_sovereign_pipeline():
    modules = [
        ("CML Schema Validation", "cml_validator.py"),
        ("Swarm Bridge Routing", "swarm_bridge.py"),
        ("Sovereign Audit Verification", "sovereign_audit.py")
    ]
    
    print("[PIPELINE] Initializing Castleberry Bloom Sovereign Execution...")
    for name, script in modules:
        print(f"\n[EXEC] Running {name} ({script})...")
        res = subprocess.run([sys.executable, script])
        if res.returncode != 0:
            print(f"[ERROR] Pipeline halted at {name}.")
            sys.exit(1)
            
    print("\n[PIPELINE] All sovereign modules executed successfully. Lattice state absolute.")

if __name__ == '__main__':
    execute_sovereign_pipeline()
