import subprocess
import time
import os

def package_release():
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    archive_name = f"castleberry_bloom_sovereign_{timestamp}.tar.gz"
    
    print(f"[*] Packaging Sovereign Release: {archive_name}")
    subprocess.run(["tar", "-czf", archive_name, 
                    "kairoth_morphogenesis.py", 
                    "live_pulse_monitor.py", 
                    "cml_validator.py", 
                    "swarm_bridge.py", 
                    "sovereign_audit.py", 
                    "run_sovereign_lattice.py", 
                    "app.py", 
                    "lattice_telemetry_lock.json"])
    
    print(f"[SUCCESS] Archive generated successfully: {os.path.abspath(archive_name)}")

if __name__ == '__main__':
    package_release()
