import numpy as np
import math

# Constants from Root42_93Solid_vFinal.py
CONST = {
    "r42": np.sqrt(42),
    "r51": np.sqrt(51),
    "r60": np.sqrt(60),
    "overpack_delta": 0.0005855308,
    "phi": (1 + np.sqrt(5)) / 2,
    "shear_angle": np.arctan(14/17),
    "vertex_count": 93,
}

POLY_ROOTS = [
    np.sqrt(93 - 2*np.sqrt(2142)),  # ≈ 0.658
    np.sqrt(93 + 2*np.sqrt(2142)),  # ≈ 13.638
]

def generate_and_sort_vertices():
    np.random.seed(42)
    CAM_SEQ = [0.1, 0.4, 0.2, 0.8, 0.5, 0.7]
    u = np.linspace(0, 2 * np.pi, 400)
    v = np.linspace(0, np.pi, 400)
    U, V = np.meshgrid(u, v)
    
    # Interference field
    field = np.abs(
        np.sin(CONST["r42"] * U) * np.sin(CONST["r51"] * V) +
        np.sin(CONST["r51"] * U) * np.sin(CONST["r42"] * V)
    )
    
    flat_field = field.flatten()
    indices = np.argpartition(flat_field, -CONST["vertex_count"])[-CONST["vertex_count"]:]
    peak_indices = np.unravel_index(indices, field.shape)
    
    raw_data = []
    for i, j in zip(peak_indices[0], peak_indices[1]):
        raw_data.append({
            "theta": U[i, j],
            "phi_coord": V[i, j],
            "field_val": field[i, j]
        })
    
    # SORT VERTICES BY THETA (Temporal/Angular order)
    raw_data.sort(key=lambda x: x['theta'])
    
    vertices = []
    metadata = []
    
    for idx, data in enumerate(raw_data):
        theta = data['theta']
        phi_coord = data['phi_coord']
        
        cycle = idx // 42
        cam_step = idx % 6
        promotion_factor = (1.0 + CONST["overpack_delta"]) ** cycle
        cam_kick = CAM_SEQ[cam_step] * 0.05
        
        x_base = np.sin(phi_coord) * np.cos(theta)
        y_base = np.sin(phi_coord) * np.sin(theta)
        z_base = np.cos(phi_coord)
        
        triadic_mod = (
            np.sin(CONST["r42"] * theta) +
            np.sin(CONST["r51"] * theta) +
            np.sin(CONST["r60"] * theta)
        ) / 3
        phi_buckle = CONST["overpack_delta"] * np.sin(5 * theta) * np.cos(5 * phi_coord)
        
        shear_rot = np.array([
            [np.cos(CONST["shear_angle"]), -np.sin(CONST["shear_angle"]), 0],
            [np.sin(CONST["shear_angle"]),  np.cos(CONST["shear_angle"]), 0],
            [0,                             0,                            1]
        ])
        
        base_radius = (1.0 + 0.3 * triadic_mod + phi_buckle + cam_kick) * promotion_factor
        radius = np.clip(base_radius, POLY_ROOTS[0]/10, POLY_ROOTS[1]/10)
        
        vec = np.array([x_base, y_base, z_base]) * radius
        vec = shear_rot @ vec
        
        vertices.append(vec)
        metadata.append({
            "idx": idx,
            "theta": theta,
            "radius": radius,
            "field_val": data['field_val']
        })
        
    return np.array(vertices), metadata

def surgical_audit():
    vertices, meta = generate_and_sort_vertices()
    
    print("--- SURGICAL FORENSIC AUDIT: Root 42 (Sorted by Theta) ---")
    
    # Audit 1: Ghost Symmetry (Radial alignment across cycles)
    print("\n[AUDIT 1] Radial Alignment (mod 2pi):")
    for i in [0, 42, 84]:
        if i < len(meta):
            print(f"Index {i:2d}: {meta[i]['theta']:.6f} rad")
            
    # Audit 2: The "Handoff" Jump at 42
    print("\n[AUDIT 2] The Step-42 Promotion:")
    v41_r = meta[41]['radius']
    v42_r = meta[42]['radius']
    print(f"Index 41 Radius: {v41_r:.8f}")
    print(f"Index 42 Radius: {v42_r:.8f}")
    print(f"Promotion Jump:  {v42_r - v41_r:.8f}")
    print(f"Expected Delta:  {CONST['overpack_delta']:.8f}")

    # Audit 3: Symmetry Residue (v[i] vs v[i+42])
    print("\n[AUDIT 3] Residue (v[i+42] / v[i]):")
    for i in [0, 1, 2, 7]: # Checking indices and prime factors
        v_low = vertices[i]
        v_high = vertices[i+42]
        ratio = v_high / v_low
        print(f"i={i} | Ratio: {ratio}")
        
    # Audit 4: Precision Lock (Field Values)
    print("\n[AUDIT 4] Field Intensity at Cycle Bounds:")
    for i in [41, 42, 43]:
        print(f"Index {i}: {meta[i]['field_val']:.8f}")

if __name__ == "__main__":
    surgical_audit()
