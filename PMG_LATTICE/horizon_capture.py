import numpy as np
from scipy.spatial import KDTree

def count_points_at_tol(tol):
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
    processed = [False]*len(all_verts)
    unique = []
    for i, v in enumerate(all_verts):
        if not processed[i]:
            idx = tree.query_ball_point(v, r=tol)
            for j in idx: processed[j] = True
            unique.append(v)
    return len(unique)

if __name__ == "__main__":
    # Micro-sweep [0.922, 0.926]
    for t in np.linspace(0.922, 0.926, 1000):
        c = count_points_at_tol(t)
        if c == 93:
            print(f"CANONICAL BITE FOUND: {t:.6f}")
            break
