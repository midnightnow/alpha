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
        z = n * 0.1 # User's z in Appendix A
        helix_pt = np.array([np.cos(theta), np.sin(theta), z])
        u = np.array([-np.sin(theta), np.cos(theta), 0])
        v = np.array([0, 0, 1])
        for v_local in tetra_base:
            # User's centering in Appendix A
            pt = helix_pt + u * (v_local[0] - 2.5) + v * (v_local[1] - 6.0)
            all_verts.append(pt)
    all_verts = np.array(all_verts)

    tree = KDTree(all_verts)
    processed = [False] * len(all_verts)
    unique_verts = []
    for i, v in enumerate(all_verts):
        if not processed[i]:
            idx = tree.query_ball_point(v, r=eps)
            for j in idx:
                processed[j] = True
            unique_verts.append(v)
    return len(unique_verts)

if __name__ == "__main__":
    print("Searching for 93-point basin for Appendix A v4.1 (z=0.1)...")
    for eps in np.linspace(0.5, 2.5, 200):
        c = count_points(eps)
        if c == 93:
            print(f"FOUND 93 AT EPS = {eps:.5f}")
            break
        elif c < 93:
            print(f"Passed 93. Closest was {c} at {eps:.5f}")
            break
