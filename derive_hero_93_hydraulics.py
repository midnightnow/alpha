import json
import numpy as np
import math

def derive_hydraulics_from_hero_93():
    nodes_path = "/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/93_node_shell.json"
    with open(nodes_path, 'r') as f:
        data = json.load(f)
    
    # Flatten nodes
    nodes = []
    for cat in data['nodes']:
        for pt in data['nodes'][cat]:
            nodes.append(np.array(pt))
    
    nodes = np.array(nodes)
    
    # Map Alphabet (26) to nodes using the same spiral logic as TonalAlphabetCalculator
    def get_angle(p):
        return math.atan2(p[1], p[0])
    
    # Sort by angle to find the 'Linguistic Ring'
    sorted_indices = sorted(range(len(nodes)), key=lambda i: get_angle(nodes[i]))
    
    # Pick 26 nodes (simplified mapping for emergence test)
    # The 13th node is already designated as the pivot [0,0,0]
    alphabet_indices = [sorted_indices[i * (len(nodes)//26)] for i in range(26)]
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    hydraulic_report = {}
    
    for i, char in enumerate(alphabet):
        node = nodes[alphabet_indices[i]]
        
        # CALCULATE CAVITY VOLUME
        # We define the 'cavity' as the distance to the nearest 3 neighbor nodes
        # reflecting the 'displacement' this letter causes in the 93-point field.
        dists = np.linalg.norm(nodes - node, axis=1)
        nearest_dists = sorted(dists)[1:4] # skip self
        
        # Approximate volume of the local Voronoi-like cell (the cavity)
        avg_radius = np.mean(nearest_dists)
        cavity_volume = (4/3) * math.pi * (avg_radius ** 3)
        
        # Calculate Pressure Effect
        # P = F/A. If the cavity is larger, the 'data liquid' slows down (Bernoulli)
        pressure_effect = 1.0 / (cavity_volume + 1e-6)
        
        hydraulic_report[char] = {
            "coordinate": node.tolist(),
            "cavity_volume": round(cavity_volume, 4),
            "pressure_signature": round(pressure_effect, 6)
        }
    
    return hydraulic_report

if __name__ == "__main__":
    report = derive_hydraulics_from_hero_93()
    print(json.dumps(report, indent=4))
