import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt

def generate_target_distribution(rows, tol_range):
    target_count = rows * 4 + 1
    STEP_SIZE = 5
    MOD = 24
    steps = 120
    apex_height = 13 * np.sqrt(3) / 2
    
    all_verts = []
    for n in range(steps):
        theta = 2 * np.pi * (STEP_SIZE * n % MOD) / MOD
        z = n * 0.08
        helix_pt = np.array([np.cos(theta), np.sin(theta), z])
        offsets = [np.array([-0.5,-0.5,0]), np.array([0.5,-0.5,0]), np.array([0.5,0.5,0]), np.array([-0.5,0.5,0]), np.array([0,0,apex_height/13])]
        for o in offsets: all_verts.append(helix_pt + o)
    all_verts = np.array(all_verts)
    tree = KDTree(all_verts)
    
    basin_counts = []
    for t in tol_range:
        processed = [False]*len(all_verts)
        unique = 0
        for i, v in enumerate(all_verts):
            if not processed[i]:
                idx = tree.query_ball_point(v, r=t)
                for j in idx: processed[j] = True
                unique += 1
        basin_counts.append(unique)
    return np.array(basin_counts)

if __name__ == "__main__":
    tols = np.linspace(0.4, 2.0, 100)
    variants = {
        19: {"count": 77, "label": "Vipera (19-row)", "color": "green"},
        21: {"count": 85, "label": "Vipera (21-row)", "color": "orange"},
        23: {"count": 93, "label": "Hero (23-row)", "color": "red"},
        25: {"count": 101, "label": "Vipera (25-row)", "color": "purple"}
    }
    
    plt.figure(figsize=(12, 8))
    
    for row_count, data in variants.items():
        counts = generate_target_distribution(row_count, tols)
        plt.plot(tols, counts, label=data["label"], color=data["color"], alpha=0.7)
        plt.axhline(y=data["count"], color=data["color"], linestyle='--', alpha=0.3)
        
        # Check for stability basin (where count == target)
        match_idx = np.where(counts == data["count"])[0]
        if len(match_idx) > 0:
            basin_width = tols[match_idx[-1]] - tols[match_idx[0]]
            print(f"Variant {row_count}-row: Basin found at eps ~ {tols[match_idx[0]]:.2f}, Width: {basin_width:.3f}")
        else:
            print(f"Variant {row_count}-row: No stable basin found for target {data['count']}")

    plt.xlabel("Tolerance (ε)")
    plt.ylabel("Distinct Points")
    plt.title("Phase II: Comparative Vitrification of Herpetological Lattices")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig("/Users/studio/ALPHA/PMG_LATTICE/p2_comparative_lattices.png")
    print("PNG SAVED: p2_comparative_lattices.png")
