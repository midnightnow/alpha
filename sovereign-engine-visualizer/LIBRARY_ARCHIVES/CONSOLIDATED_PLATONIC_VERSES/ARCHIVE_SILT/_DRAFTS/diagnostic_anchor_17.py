import numpy as np
import math

CONST = {
    "r42": np.sqrt(42),
    "r51": np.sqrt(51),
    "count": 93
}

def diagnostic_anchor_stability():
    np.random.seed(42)
    u = np.linspace(0, 2 * np.pi, 500) # Slightly higher resolution
    v = np.linspace(0, np.pi, 500)
    U, V = np.meshgrid(u, v)
    
    # The interference field
    field = np.abs(
        np.sin(CONST["r42"] * U) * np.sin(CONST["r51"] * V) +
        np.sin(CONST["r51"] * U) * np.sin(CONST["r42"] * V)
    )
    
    flat_field = field.flatten()
    # Pulling more points to see the neighborhood
    indices = np.argpartition(flat_field, -CONST["count"])[-CONST["count"]:]
    peak_indices = np.unravel_index(indices, field.shape)
    
    raw_data = []
    for i, j in zip(peak_indices[0], peak_indices[1]):
        raw_data.append({
            "theta": U[i, j],
            "field_val": field[i, j]
        })
    
    # SORT BY THETA for angular sequence
    raw_data.sort(key=lambda x: x['theta'])
    
    print("--- FORENSIC DIAGNOSTIC: INDEX 17 ANCHOR STABILITY ---")
    
    # Analysis points
    target_idx = 17
    indices_to_test = [target_idx - 1, target_idx, target_idx + 1]
    
    # 1. Field Intensity (Precision of the Peak)
    print("\n[1] Field Intensity (Precision):")
    for i in indices_to_test:
        print(f"Index {i:2d}: {raw_data[i]['field_val']:.8f}")

    # 2. Angular Variance (Step stability)
    print("\n[2] Angular Step Stability (Delta Theta):")
    deltas = []
    for i in range(1, len(raw_data)):
        deltas.append(raw_data[i]['theta'] - raw_data[i-1]['theta'])
    
    # Variance of the step ending at index i
    # We look at the window around 17
    for i in indices_to_test:
        if i > 0 and i < len(deltas):
            # Window of 5 steps around the index
            window = deltas[max(0, i-2):min(len(deltas), i+3)]
            print(f"Index {i:2d} Step Variance (window of 5): {np.var(window):.8e}")

    # 3. Fermat Grid Error
    print("\n[3] 17-fold Grid Error:")
    for i in indices_to_test:
        theoretical = (i * 2 * np.pi / 17) % (2 * np.pi)
        error = abs(raw_data[i]['theta'] - theoretical)
        error = min(error, 2 * np.pi - error)
        print(f"Index {i:2d} Error: {error:.6f}")

if __name__ == "__main__":
    diagnostic_anchor_stability()
