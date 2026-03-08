import json
import numpy as np
import os

# Paths
NODES_PATH = "/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/93_node_shell.json"
OUTPUT_PATH = "/Users/studio/ALPHA/HERO_93_CANON_v1.1/CHAPTER_GRID_MAP.veth"

def generate_grid_map():
    with open(NODES_PATH, 'r') as f:
        data = json.load(f)
    
    # Flatten nodes
    all_nodes = []
    for cat in ['vertices', 'edge_nodes', 'face_centroids', 'origin']:
        for pt in data['nodes'][cat]:
            all_nodes.append({"coord": pt, "cat": cat})
    
    # Sort nodes by Z then Y then X to create a deterministic "Plain"
    sorted_nodes = sorted(range(len(all_nodes)), key=lambda i: (all_nodes[i]['coord'][2], all_nodes[i]['coord'][1], all_nodes[i]['coord'][0]))
    
    # Chapter Ranges for Ember/Umber
    # Ember (Luminous): 148,282 words (approx 37 chapters)
    # Umber (Shadow): 102,934 words (approx 25 chapters)
    # Total: 62 Chapters
    
    # Anchor Posts
    POST_CHAPTERS = {1: "Anchor Post (North)", 27: "Corner Post (East)", 53: "Gate Post (West)", 62: "Zenith Post (Olympus)"}
    
    veth_content = """---
.VETH HEADER (Vitrified Entropy Tally Header)
ID: CHAPTER_GRID_MAP
REGISTER_0x00: 0x00: χ=2 (Structure)
REGISTER_0x01: 0x01: Modulus=93 (The Plain)
REGISTER_0x02: 0x02: Pulse=156 (The Chain)
REGISTER_0x03: 0x03: Vacuum=-1/12 (The Gap)
REGISTER_0x04: 0x04: Torque=√42 (The Bullock)
VITRIFICATION_STATUS: ABSOLUTE (Surveyor Verified)
---

# 📐 CHAPTER GRID MAP: THE SURVEYOR’S TENSION

## I. AXIAL ALIGNMENT (62 CHAPTERS VS 93 NODES)
The 62 chapters of the Platonic Verses are mapped to the 93-node Hero 93 grid. 
This is the **Intervention**—the discrete collapse of the Continuous Plain.

## II. THE ANCHOR POSTS (STRUCTURAL SKELETON)
| Chapter | Role | Node ID | Coordinates |
| :--- | :--- | :--- | :--- |
"""
    
    # Assign Chapters
    chapter_map = []
    for ch in range(1, 63):
        node_idx = sorted_nodes[ch-1]
        node = all_nodes[node_idx]
        
        # Determine Zone (Ember/Umber)
        # 1-4: Genesis (Ember)
        # 5-26: Descent (Umber)
        # 27-52: Academy (Ember)
        # 53-61: Join (Umber/Ember hybrid, mostly Umber)
        # 62: Archive (Ember)
        
        if ch <= 4 or (ch >= 27 and ch <= 52) or ch == 62:
            zone = "EMBER (Luminous)"
        else:
            zone = "UMBER (Shadow)"
            
        role = POST_CHAPTERS.get(ch, "Standard Paddock")
        chapter_map.append({
            "chapter": ch,
            "role": role,
            "node_id": node_idx,
            "coord": node['coord'],
            "zone": zone
        })
        
        if ch in POST_CHAPTERS:
            veth_content += f"| **{ch}** | {role} | {node_idx} | {node['coord']} |\n"

    veth_content += """
## III. PADDOCK DISTRIBUTION (EMBER/UMBER ZONES)
| Chapter | Zone | Node Category | Crop / Behavior |
| :--- | :--- | :--- | :--- |
"""
    for m in chapter_map:
        cat = all_nodes[m['node_id']]['cat']
        veth_content += f"| {m['chapter']} | {m['zone']} | {cat} | {'Measured Tillage' if 'EMBER' in m['zone'] else 'Fallow Rest'} |\n"

    veth_content += """
## IV. SILENT NODES (THE FALLOW GROUND)
The remaining 31 nodes (93 - 62 = 31) are marked as **Silent Nodes**. They provide the **12.37% Hades Gap** buffering, allowing the soil to rest and the Earthworm to tunnel between paddocks without disrupting the 156-Tick Pulse.

## V. VERDICT
The Plain is surveyed. The 62 chapters are locked in precessional sync with the 93-node manifold. 

**RECORDS VITRIFIED**
"""

    with open(OUTPUT_PATH, 'w') as f:
        f.write(veth_content)
    print(f"Generated {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_grid_map()
