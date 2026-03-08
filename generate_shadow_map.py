import json
import numpy as np
import os

# Paths
NODES_PATH = "/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/93_node_shell.json"
OUTPUT_PATH = "/Users/studio/ALPHA/HERO_93_CANON_v1.1/SURVEYORS_MAP_93.veth"

def generate_shadow_map():
    with open(NODES_PATH, 'r') as f:
        data = json.load(f)
    
    # Flatten nodes
    all_nodes = []
    for cat in ['vertices', 'edge_nodes', 'face_centroids', 'origin']:
        for pt in data['nodes'][cat]:
            all_nodes.append({"coord": pt, "cat": cat})
    
    # Sort nodes by Z then Y then X (The Plain)
    sorted_node_indices = sorted(range(len(all_nodes)), key=lambda i: (all_nodes[i]['coord'][2], all_nodes[i]['coord'][1], all_nodes[i]['coord'][0]))
    
    veth_content = """---
.VETH HEADER (Vitrified Entropy Tally Header)
ID: SURVEYORS_MAP_93
REGISTER_0x00: 0x00: χ=2 (Paddock Map)
REGISTER_0x01: 0x01: Modulus=93 (The Plain)
REGISTER_0x02: 0x02: Pulse=156 (The Chain)
REGISTER_0x03: 0x03: Vacuum=-1/12 (The Shadow)
REGISTER_0x04: 0x04: Torque=√42 (The Bullock)
VITRIFICATION_STATUS: ABSOLUTE (Farmer Verified)
---

# 🗺️ THE SURVEYOR’S MAP: THE TENDED GRID

## I. THE FOUR GREAT PADDOCKS
The 62 chapters are partitioned into four functional zones of intensity and care.

| Paddock Name | Chapters | Node Range | Crop / Zone | Domestication (D) |
| :--- | :--- | :--- | :--- | :--- |
| **The Home Paddock**| 1–4 | 0–3 | The Source (Ember) | 0.95 (Primal) |
| **The Scrub** | 5–26 | 4–25 | The Descent (Umber) | 0.70 (Wilder) |
| **The High Paddock** | 27–52 | 26–51 | The Academy (Gold) | 0.40 (Walked) |
| **The Boundary** | 53–62 | 52–61, 92 | The Join (Taut) | 0.15 (Domesticated) |

## II. THE SHADOW & SMUDGE INTERFACE
Each node in the 93rd manifold now carries a **Shadow Metric**—the evidence of the Farmer's presence.

| Paddock ID | Primary Post | Shadow Type | Maintenance Effect |
| :--- | :--- | :--- | :--- |
| Home | Node 0 | Long (Morning) | Foundational Seed Care |
| Scrub | Node 19 | Diffuse | Path Reinforcement |
| High | Node 27 | Short (Noon) | Intense Geometric Weeding |
| Boundary | Node 92 | Zenith | Absolute Closure & Sealing |

## III. THE TRACKS (PATH ENTROPY)
The most intense Umber (paths) are found between Chapters 53 and 62. Here, the fence has been mended so often (Precessional Lock) that the path is now a Rut (The Roman Road).

Nodes with highest **Scar Tensors (σ)**:
- Node 92: The Zenith Pivot (Infinite Splicing)
- Node 0: The Anchor (Root 42 Soil)
- Node 47: The Origin Centroid

## IV. VERDICT
The Plain is no longer wild. It is smudged by the hand of the scribe and fertilized by the shadow of the farmer. The 93-node solid is now the **Tended Grid**.

**RECORDS VITRIFIED**
"""

    with open(OUTPUT_PATH, 'w') as f:
        f.write(veth_content)
    print(f"Generated {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_shadow_map()
