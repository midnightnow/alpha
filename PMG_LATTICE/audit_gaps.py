import numpy as np
from scipy.spatial import KDTree

def count_points(eps, steps=120):
    STEP_SIZE = 5
    MOD = 24
    
    A0 = np.array([0.0, 0.0, 0.0])
    B0 = np.array([5.0, 0.0, 0.0])
    C0 = np.array([0.0, 12.0, 0.0])
    P0 = np.array([2.5, 6.0, 13 * np.sqrt(3) / 2])
    tetra_base = np.array([A0, B0, C0, P0])

    all_verts = []
    for n in range(steps):
        theta = 2 * np.pi * (STEP_SIZE * n % MOD) / MOD
        z = n * 0.1
        helix_pt = np.array([np.cos(theta), np.sin(theta), z])
        u = np.array([-np.sin(theta), np.cos(theta), 0])
        v = np.array([0, 0, 1])
        for v_local in tetra_base:
            pt = helix_pt + u * (v_local[0] - 2.5) + v * (v_local[1] - 6.0)
            all_verts.append(pt)
    all_verts = np.array(all_verts)

    tree = KDTree(all_verts)
    merged_indices = set()
    unique_verts = []
    for i, v in enumerate(all_verts):
        if i in merged_indices:
            continue
        idx = tree.query_ball_point(v, r=eps)
        merged_indices.update(idx)
        unique_verts.append(v)
    return len(unique_verts)

if __name__ == "__main__":
    tolerances = [1e-6, 1e-5, 1e-4]
    print("--- SENSITIVITY AUDIT ---")
    for eps in tolerances:
        count = count_points(eps)
        print(f"ε = {eps:.1e} -> Count: {count}")
    
    print("\n--- 52-STEP TEST ---")
    count_52 = count_points(1e-5, steps=52)
    print(f"Steps = 52, ε = 1e-5 -> Count: {count_52}")
