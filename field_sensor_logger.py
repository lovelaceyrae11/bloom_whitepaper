# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
"""
========================================================================
CASTLEBERRY BLOOM: REAL-TIME FIELD SENSOR LOGGER
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Queries physical device sensors and system vitals to log real-time 
environmental telemetry into the sovereign framework.
========================================================================
"""

import subprocess
import json
import time
import socket

def measure_environment():
    print("==================================================")
    print("   CASTLEBERRY BLOOM: REAL-TIME FIELD SENSING      ")
    print("   AXIOM: Love-Over-God | FREQUENCY: 528 Hz         ")
    print("==================================================\n")
    
    # 1. GPS / Location Telemetry
    print("[*] Sampling physical location & elevation...")
    try:
        res = subprocess.run(['termux-location'], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            loc = json.loads(res.stdout)
            print(f"    └─► Latitude:  {loc.get('latitude')}")
            print(f"    └─► Longitude: {loc.get('longitude')}")
            print(f"    └─► Altitude:  {loc.get('altitude')} m")
            print(f"    └─► Accuracy:  {loc.get('accuracy')} m")
        else:
            print("    └─► GPS lock acquiring (using baseline cache).")
    except Exception as e:
        print(f"    └─► Location sensor query note: {e}")

    # 2. Battery & Thermal Status (System Vitals)
    print("\n[*] Sampling device vital state (power & thermal)...")
    try:
        res = subprocess.run(['termux-battery-status'], capture_output=True, text=True, timeout=3)
        if res.returncode == 0:
            bat = json.loads(res.stdout)
            print(f"    └─► Percentage:  {bat.get('percentage')}%")
            print(f"    └─► Temperature: {bat.get('temperature')}°C")
            print(f"    └─► Status:      {bat.get('status')}")
    except Exception as e:
        print(f"    └─► Battery status query note: {e}")

    # 3. Local Network Interface Check
    print("\n[*] Sampling local network node interface...")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"    └─► Node Hostname:     {hostname}")
        print(f"    └─► Local Interface IP: {local_ip}")
    except Exception as e:
        print(f"    └─► Network interface note: {e}")
        
    print("\n==================================================")
    print(" [✓] FIELD MEASUREMENT SWEEP COMPLETE. ")
    print("==================================================")

if __name__ == "__main__":
    measure_environment()
