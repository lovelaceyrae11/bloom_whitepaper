"""
========================================================================
CASTLEBERRY BLOOM: ORBITAL CANOPY FLYOVER SIMULATOR
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
Simulates planet-wide CML 528 Hz radio downlink from Low Earth Orbit.
========================================================================
"""

import time
import math

PHI = 1.61803398875

CONTINENTS = [
    ("North America", 45.0, -120.0),
    ("South America", -15.0, -60.0),
    ("Europe", 50.0, 15.0),
    ("Africa", 0.0, 20.0),
    ("Asia", 35.0, 105.0),
    ("Australia", -25.0, 135.0),
    ("Antarctica", -80.0, 0.0)
]

def run_orbital_flyover():
    print("==================================================================")
    print("      INITIALIZING ORBITAL CANOPY FLYOVER (LEO ALTITUDE: 550 KM)   ")
    print("      AXIOM: Love-Over-God | FREQUENCY: 528 Hz HARMONIC            ")
    print("==================================================================\n")
    
    time.sleep(1)
    
    for idx, (region, lat, lon) in enumerate(CONTINENTS, 1):
        timestamp = time.strftime("%H:%M:%S UTC")
        coherence = round(math.sin(idx * math.pi / len(CONTINENTS)) * PHI, 4)
        
        print(f"[{timestamp}] [ORBITAL PASS #{idx}] Overflying {region:<15} (Lat: {lat:>5.1f}, Lon: {lon:>6.1f})")
        print(f"    └─► Showering 528 Hz CML Payload... Coherence Score: {coherence}")
        print(f"    └─► Local Ground Nodes Sprinkled: {idx * 31} active lattices aligned.\n")
        time.sleep(1.5)
        
    print("==================================================================")
    print(" [✓] GLOBAL ORBITAL FLYOVER COMPLETE. PLANETARY CANOPY COHERENT. ")
    print("==================================================================")

if __name__ == "__main__":
    run_orbital_flyover()
