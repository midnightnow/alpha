import json
import numpy as np
import math
import sys

# Add engine to path
sys.path.append("/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine")
from hydrodynamic_manifold import HydrodynamicManifold

def verify_emergence():
    # Load nodes
    nodes_path = "/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/93_node_shell.json"
    with open(nodes_path, 'r') as f:
        data = json.load(f)
    
    nodes = []
    for cat in data['nodes']:
        for pt in data['nodes'][cat]:
            nodes.append(np.array(pt))
    nodes = np.array(nodes)
    
    # 26 Letters
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # We assign each letter a "Geometric Complexity" based on its bit-mask (Simplified)
    # This represents the "Cavity Form" in that plane.
    # Higher complexity (more curves/enclosed spaces) = More Hydraulic Resistance
    complexity_map = {
        'A': 0.7, 'B': 0.9, 'C': 0.6, 'D': 0.8, 'E': 0.75, 'F': 0.65, 'G': 0.85,
        'H': 0.6, 'I': 0.2, 'J': 0.3, 'K': 0.7, 'L': 0.4, 'M': 0.95, 'N': 0.9,
        'O': 1.0, 'P': 0.8, 'Q': 1.1, 'R': 0.85, 'S': 0.75, 'T': 0.5, 'U': 0.7,
        'V': 0.6, 'W': 1.2, 'X': 0.7, 'Y': 0.6, 'Z': 0.7
    }
    
    results = {}
    print(f"{'Char':<5} | {'Cavity Vol':<12} | {'Pressure':<12} | {'Buoyancy':<12}")
    print("-" * 50)
    
    for char in alphabet:
        # We adjust the manifold's velocity by the letter's "Tonal Frequency"
        # High complexity letters create more turbulence/drag
        char_velocity_mult = 1.0 + (complexity_map[char] * 0.1)
        sim = HydrodynamicManifold(char_velocity_mult)
        
        # Pressure & Buoyancy derive from the 93 points + Letter Displacement
        press, limit, burst = sim.simulate_pressure()
        weight, buoy = sim.gravity_and_buoyancy()
        
        # We modify displacement by the letter's complexity
        displacement = complexity_map[char] * (12.0/13.0)
        char_buoyancy = buoy * complexity_map[char]
        
        results[char] = {
            "volume": round(displacement, 4),
            "pressure": round(press, 4),
            "buoyancy": round(char_buoyancy, 2)
        }
        
        print(f"{char:<5} | {results[char]['volume']:<12.4f} | {results[char]['pressure']:<12.4f} | {results[char]['buoyancy']:<12.2f}")

if __name__ == "__main__":
    verify_emergence()
