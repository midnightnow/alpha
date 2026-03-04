import numpy as np
import math

CONST = {
    "r42": np.sqrt(42),
    "r51": np.sqrt(51),
    "count": 93
}

def analyze_51_anchor():
    np.random.seed(42)
    u = np.linspace(0, 2 * np.pi, 400)
    v = np.linspace(0, np.pi, 400)
    U, V = np.meshgrid(u, v)
    
    # The 93-Solid field
    field = np.abs(
        np.sin(CONST["r42"] * U) * np.sin(CONST["r51"] * V) +
        np.sin(CONST["r51"] * U) * np.sin(CONST["r42"] * V)
    )
    
    flat_field = field.flatten()
    indices = np.argpartition(flat_field, -CONST["count"])[-CONST["count"]:]
    peak_indices = np.unravel_index(indices, field.shape)
    
    thetas = sorted([U[i, j] for i, j in zip(peak_indices[0], peak_indices[1])])
    
    # Audit: Grid Lock Check
    # We test alignment against 17-fold (Anchor) and 7-fold (Cam)
    print("--- FORENSIC AUDIT: 93 PEAKS VS 17/7 GRID ---")
    
    errors_17 = []
    errors_42 = [] # 42 is 6*7
    
    for i, t in enumerate(thetas):
        # 17-fold error (The Anchor)
        theoretical_17 = (i * 2 * math.pi / 17) % (2 * math.pi)
        e17 = abs(t - theoretical_17)
        e17 = min(e17, 2 * math.pi - e17)
        errors_17.append(e17)
        
        # 42-fold error (The Cam/Structural)
        theoretical_42 = (i * 2 * math.pi / 42) % (2 * math.pi)
        e42 = abs(t - theoretical_42)
        e42 = min(e42, 2 * math.pi - e42)
        errors_42.append(e42)

    # Search for minima at the prime indices
    print("\n[ANCHOR CHECK] i=17 analysis:")
    print(f"Index 16 error: {errors_17[16]:.4f}")
    print(f"Index 17 error: {errors_17[17]:.4f}")
    print(f"Index 18 error: {errors_17[18]:.4f}")
    
    print("\n[CAM CHECK] i=42 analysis:")
    print(f"Index 41 error: {errors_42[41]:.4f}")
    print(f"Index 42 error: {errors_42[42]:.4f}")
    print(f"Index 43 error: {errors_42[43]:.4f}")

    # Finding actual minima for 17-fold
    print("\nLocal minima (17-fold grid):")
    for j in range(1, len(errors_17)-1):
        if errors_17[j] < errors_17[j-1] and errors_17[j] < errors_17[j+1]:
            if errors_17[j] < 0.1: # Threshold for high alignment
                print(f"Index {j:2d}: error={errors_17[j]:.2e}")

    # Finding actual minima for 42-fold
    print("\nLocal minima (42-fold grid):")
    for j in range(1, len(errors_42)-1):
        if errors_42[j] < errors_42[j-1] and errors_42[j] < errors_42[j+1]:
            if errors_42[j] < 0.1:
                print(f"Index {j:2d}: error={errors_42[j]:.2e}")

if __name__ == "__main__":
    analyze_51_anchor()
