import numpy as np
import math

# Root 51 Architecture (3 x 17)
CONST = {
    "r51": math.sqrt(51),
    "r17": 17,
    "phi": (1 + math.sqrt(5)) / 2,
    "hades_gap": 0.1237
}

def analyze_anchor():
    print("--- FORENSIC RECEIVER: ROOT 51 (3x17) LENS ---")
    
    # We follow the "Refinement" logic (3 -> 17)
    # Phase 1: The Circle Definition (Index 0-2)
    # Phase 2: The Measurement (Index 3+)
    # Phase 3: The Anchor Lock (Index 17)
    
    radii = []
    angular_velocity = []
    precisions = [] # Measuring distance to the nearest "Ideal" 17-gon node
    
    for i in range(52):
        # We simulate the 1/17 lens refinement
        phase = (i * 2 * np.pi / 17)
        
        # Generative growth from the 5-fold interruption
        growth = (CONST["phi"] ** (i / 17)) * 0.1
        
        # The 1/17 reciprocal remainder (period 16)
        # We measure how the "slop" behaves over the period
        remainder = (1/17 * 10**i) % 1
        
        radius = 1.0 + growth + (remainder * 0.01)
        radii.append(radius)
        
        if i > 0:
            # Velocity: How fast does the definition move?
            angular_velocity.append(radius / i)
            
        # Precision check: How close are we to a "True Closure"?
        # 17 should be the lowest error
        precision_error = abs(math.sin(17 * phase / 2)) 
        precisions.append(precision_error)

    # 1. The Measurement Break (Index 3 -> 4)
    print(f"\n[MEASUREMENT SHOCK] Index 3 (Def) to 4 (Measure):")
    shock = radii[4] - radii[3]
    print(f"Radial Shift: {shock:.6f} (The First pi-remainder)")

    # 2. The Anchor Lock (Index 17)
    print(f"\n[ANCHOR LOCK] Index 17 Analysis:")
    print(f"Index 17 Precision Error: {precisions[17]:.10f}")
    if precisions[17] < precisions[16]:
        print("SIGNAL: ANCHOR SPIKE DETECTED. The 17-gon is self-correcting.")
    else:
        print("SIGNAL: Floating drift persists.")

    # 3. The 1/17 Period (16 steps)
    period_start = radii[1]
    period_end = radii[17]
    print(f"\n[1/17 RECIPROCAL] Period 16 Check:")
    print(f"Cycle Start: {period_start:.6f} | Cycle End: {period_end:.6f}")
    print(f"Drift over 16 steps: {abs(period_end - (period_start * CONST['phi'])) :.6f}")

    # 4. The "Hiding" 13 (The Temporal Shift)
    # Checking for any correlation at 13 (The Hired Man)
    print(f"\n[HIRED MAN] Index 13 Signature:")
    print(f"Velocity at 13: {angular_velocity[12]:.6f}")

if __name__ == "__main__":
    analyze_anchor()
