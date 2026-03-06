import numpy as np
from scipy.spatial import KDTree

def count_points(eps):
    STEP_SIZE = 5
    MOD = 24
    steps = 120
    
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
            # Shift v_local to be centered or use as is
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
    print("Searching for 93-point basin in Appendix A code...")
    for eps in np.linspace(0.1, 5.0, 100):
        c = count_points(eps)
        if c <= 120:
            print(f"ε = {eps:.2f} -> Count: {c}")
        if c == 93:
            print(f"FOUND 93 AT ε = {eps:.4f}")
            break
        elif c < 93:
            print(f"Passed 93. Closest was {c}")
            break
