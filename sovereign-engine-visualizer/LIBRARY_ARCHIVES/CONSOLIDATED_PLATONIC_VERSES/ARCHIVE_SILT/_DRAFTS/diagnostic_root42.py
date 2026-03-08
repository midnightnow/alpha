import numpy as np
import math

# Replicating the logic from Root42_93Solid_vFinal.py
CONST = {
    "r42": math.sqrt(42),
    "r51": math.sqrt(51),
    "r60": math.sqrt(60),
    "vertex_count": 93,
    "overpack_delta": 0.000585,
    "shear_angle": math.radians(39.47),
}

POLY_ROOTS = [
    np.sqrt(93 - 2*np.sqrt(2142)),  # ≈ 0.658
    np.sqrt(93 + 2*np.sqrt(2142)),  # ≈ 13.638
]

def analyze_vertices():
    np.random.seed(42)
    CAM_SEQ = [0.1, 0.4, 0.2, 0.8, 0.5, 0.7]
    
    # Mocking the peak detection indices for forensic analysis
    # In the real script, indices are pulled from a meshgrid.
    # Here, we will analyze the "Phase Logic" applied to those indices.
    
    radii = []
    vectors = []
    
    # We iterate through the indices as if we're generating them
    for idx in range(CONST["vertex_count"]):
        # Mimicking the coordinate selection (simulated for diagnostic)
        theta = (idx * 0.1) # Simplified linear walk to see the "kicks"
        phi_coord = (idx * 0.05)
        
        cycle = idx // 42
        cam_step = idx % 6
        promotion_factor = (1.0 + CONST["overpack_delta"]) ** cycle
        cam_kick = CAM_SEQ[cam_step] * 0.05
        
        triadic_mod = (
            np.sin(CONST["r42"] * theta) +
            np.sin(CONST["r51"] * theta) +
            np.sin(CONST["r60"] * theta)
        ) / 3
        
        phi_buckle = CONST["overpack_delta"] * np.sin(5 * theta) * np.cos(5 * phi_coord)
        base_radius = (1.0 + 0.3 * triadic_mod + phi_buckle + cam_kick) * promotion_factor
        radius = np.clip(base_radius, POLY_ROOTS[0]/10, POLY_ROOTS[1]/10)
        radii.append(radius)
        
        # Calculate crude vector for distance analysis
        vec = np.array([
            np.sin(phi_coord) * np.cos(theta),
            np.sin(phi_coord) * np.sin(theta),
            np.cos(phi_coord)
        ]) * radius
        vectors.append(vec)

    # Forensic Analysis
    print("--- FORENSIC ANALYSIS: ROOT 42 VERTEX ARRAY ---")
    
    # 1. Delta Analysis (Distance between consecutive vertices)
    deltas = []
    for i in range(1, len(vectors)):
        dist = np.linalg.norm(vectors[i] - vectors[i-1])
        deltas.append(dist)
    
    print(f"\n[SIGNATURE] Mean Delta: {np.mean(deltas):.4f}")
    
    # 2. Threshold Check: Teens (11-19)
    teen_deltas = deltas[10:19]
    unit_deltas = deltas[0:9]
    print(f"[TEEN THRESHOLD] Units(1-9) Mean: {np.mean(unit_deltas):.4f} | Teens(11-19) Mean: {np.mean(teen_deltas):.4f}")
    
    # 3. The 42nd Index Handoff
    print(f"\n[42nd INDEX] Analysis:")
    print(f"Index 41 Radius: {radii[41]:.6f}")
    print(f"Index 42 Radius: {radii[42]:.6f}")
    print(f"Jump: {radii[42] - radii[41]:.6f}")
    
    # 4. Cam Rhythm Check (Period 6)
    print(f"\n[CAM RHYTHM] Period 6 Variance:")
    first_6 = radii[0:6]
    second_6 = radii[6:12]
    print(f"Cycle 1 Variance: {np.var(first_6):.6f}")
    print(f"Cycle 2 Variance: {np.var(second_6):.6f}")
    
    # 5. First Discontinuity Search
    # We look for a significant deviation in the delta trend
    slopes = np.diff(deltas)
    discontinuity_idx = np.argmax(np.abs(slopes)) + 1
    print(f"\n[FIRST DISCONTINUITY] Peak Slope Change at Index: {discontinuity_idx}")

if __name__ == "__main__":
    analyze_vertices()
