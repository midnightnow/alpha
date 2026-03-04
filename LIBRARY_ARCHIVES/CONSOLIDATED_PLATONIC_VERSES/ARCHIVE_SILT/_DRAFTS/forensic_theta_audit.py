import numpy as np
import math

# Constants from Root42_93Solid_vFinal.py
CONST = {
    "r42": np.sqrt(42),
    "r51": np.sqrt(51),
    "vertex_count": 93,
}

def hunt_for_minima():
    np.random.seed(42)
    
    # Generate the field and find peaks
    u = np.linspace(0, 2 * np.pi, 400)
    v = np.linspace(0, np.pi, 400)
    U, V = np.meshgrid(u, v)
    field = np.abs(
        np.sin(CONST["r42"] * U) * np.sin(CONST["r51"] * V) +
        np.sin(CONST["r51"] * U) * np.sin(CONST["r42"] * V)
    )
    
    flat_field = field.flatten()
    indices = np.argpartition(flat_field, -CONST["vertex_count"])[-CONST["vertex_count"]:]
    peak_indices = np.unravel_index(indices, field.shape)
    
    all_thetas = sorted([U[i, j] for i, j in zip(peak_indices[0], peak_indices[1])])
    
    errors = []
    for i, actual_theta in enumerate(all_thetas):
        theoretical = (i * 2 * math.pi / 42)
        # Handle wrap-around for theta
        error = abs(actual_theta - (theoretical % (2 * math.pi)))
        # Adjust for 2pi wrap-around
        error = min(error, 2 * math.pi - error)
        errors.append((i, error))
        
    print("--- SEARCH FOR THE SMOKING GUN: ANGULAR ERROR MINIMA ---")
    
    # Find and print only the local minima
    found_minima = []
    for j in range(1, len(errors)-1):
        if errors[j][1] < errors[j-1][1] and errors[j][1] < errors[j+1][1]:
            found_minima.append(errors[j])
            print(f"Local minimum at i={errors[j][0]:2d}, error={errors[j][1]:.2e}")

    # Check for clustering at factors or multiples of 42
    print("\n[VERDICT]")
    multiples_of_42 = [m for m, err in found_minima if m > 0 and (m % 42 == 0)]
    divisors_of_42 = [d for d, err in found_minima if d > 0 and (42 % d == 0)]
    
    if multiples_of_42:
        print(f"✓ ALIGNMENT: Minima found at multiples of 42: {multiples_of_42}")
    if divisors_of_42:
        print(f"✓ STRUCTURE: Minima found at divisors of 42: {divisors_of_42}")
    if not (multiples_of_42 or divisors_of_42):
        print("✗ NO CLUSTERING: The effect is likely simpler or the resolution is insufficient.")

if __name__ == "__main__":
    hunt_for_minima()
