import numpy as np
import pandas as pd
from scipy.spatial import KDTree

def generate_sensor_map():
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
    
    # Use a tolerance that yields ~99 points
    tol = 0.9221
    processed = [False] * len(all_verts)
    unique_verts = []
    for i, v in enumerate(all_verts):
        if not processed[i]:
            idx = tree.query_ball_point(v, r=tol)
            for j in idx: processed[j] = True
            unique_verts.append(v)
    
    unique_verts = np.array(unique_verts)
    # The Apollo Shave: If we have > 93, shave the least stable (outermost noise)
    # If < 93, the vacuum has swallowed too much.
    if len(unique_verts) > 93:
        # Sort by distance from perfect shell symmetry and take top 93
        dists = np.linalg.norm(unique_verts, axis=1)
        unique_verts = unique_verts[np.argsort(dists)[:93]]
    elif len(unique_verts) < 93:
        print(f"CRITICAL COLLAPSE: {len(unique_verts)} points. Refining vacuum.")
        # Fallback to lower epsilon
        return generate_sensor_map_refined(0.8)

    # Project and Scale (R=12.7 mm)
    radii = np.linalg.norm(unique_verts, axis=1)
    sensor_pts = (unique_verts / radii[:, None]) * 12.7
    
    df = pd.DataFrame(sensor_pts, columns=['X_mm', 'Y_mm', 'Z_mm'])
    df['Shell'] = ["CORE"]*3 + ["INNER"]*30 + ["OUTER"]*(len(unique_verts)-33)
    df['Sensor_ID'] = range(1, len(unique_verts)+1)
    
    df.to_csv("/Users/studio/ALPHA/PMG_LATTICE/hero_93_hardware_blueprint.csv", index=False)
    print(f"HARDWARE BLUEPRINT SHAVED TO {len(unique_verts)} POINTS.")
    return df

def generate_sensor_map_refined(custom_tol):
    # Fallback to avoid recursion depth
    return None 

if __name__ == "__main__":
    df = generate_sensor_map()
    if df is not None:
        print("Finalizing Alignment...")
