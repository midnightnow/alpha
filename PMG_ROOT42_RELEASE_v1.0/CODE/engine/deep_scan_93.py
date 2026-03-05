import json
from decimal import Decimal, getcontext
import math

getcontext().prec = 28

def deep_scan():
    filepath = '../../ASSETS/hyperdiamond_shell.json'
    with open(filepath, 'r') as f:
        data = json.load(f)
        nodes = data['nodes']
    
    # Node 1 (index 0) and Node 93 (index 92)
    n1 = nodes[0]
    n93 = nodes[92]
    
    # Zenith Axis (Root 51) - for this check we assume it's the Z axis inversion
    print(f"--- DEEP SCAN: 93rd NODE REFLECTION ---")
    print(f"NODE 01 (Zenith Candidate): x={n1['x']:.9f}, y={n1['y']:.9f}, z={n1['z']:.9f}")
    print(f"NODE 93 (Nadir Candidate):  x={n93['x']:.9f}, y={n93['y']:.9f}, z={n93['z']:.9f}")
    
    # Check for point reflection (mirroring across origin)
    dx = abs(n1['x'] + n93['x'])
    dy = abs(n1['y'] + n93['y'])
    dz = abs(n1['z'] + n93['z'])
    
    print(f"\nReflection Delta: Δx={dx:.9f}, Δy={dy:.9f}, Δz={dz:.9f}")
    
    if dx < 1e-5 and dy < 1e-5 and dz < 1e-5:
        print("\n[STATUS] MIRROR LOCK: ACTIVE")
        print("Result: Node 93 is a perfect rotational reflection of Node 1.")
    else:
        print("\n[STATUS] ASYMMETRIC OFFSET DETECTED")
        print("Note: The 108-degree torsion shift or Hades Gap may be inducing a prime-phase offset.")

if __name__ == "__main__":
    deep_scan()
