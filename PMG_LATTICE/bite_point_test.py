import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt

def count_points_at_tol(tol, steps=120):
    STEP_SIZE = 5
    MOD = 24
    apex_height = 13 * np.sqrt(3) / 2
    
    all_verts = []
    for n in range(steps):
        theta = 2 * np.pi * (STEP_SIZE * n % MOD) / MOD
        z = n * 0.08
        helix_pt = np.array([np.cos(theta), np.sin(theta), z])
        
        base_offsets = [
            np.array([-0.5, -0.5, 0]),
            np.array([ 0.5, -0.5, 0]),
            np.array([ 0.5,  0.5, 0]),
            np.array([-0.5,  0.5, 0])
        ]
        apex_offset = np.array([0, 0, apex_height / 13])
        
        for offset in base_offsets + [apex_offset]:
            v = helix_pt + offset
            all_verts.append(v)

    all_verts = np.array(all_verts)
    tree = KDTree(all_verts)
    processed = [False] * len(all_verts)
    unique_verts = []
    
    for i, v in enumerate(all_verts):
        if not processed[i]:
            idx = tree.query_ball_point(v, r=tol)
            for j in idx:
                processed[j] = True
            unique_verts.append(v)
    return len(unique_verts)

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def analyze_primes(count=1000):
    primes = []
    i = 2
    while len(primes) < count:
        if is_prime(i):
            primes.append(i)
        i += 1
    
    residues = [p % 24 for p in primes]
    # Check interference with 7-cycle digits: 1, 4, 2, 8, 5, 7
    cycle_7 = [1, 4, 2, 8, 5, 7]
    match_count = sum(1 for r in residues if r % 9 in cycle_7)
    return residues, match_count

if __name__ == "__main__":
    # 1. Tolerance Sweep (Search for the 93 Point Basin)
    tols = np.linspace(0.4, 2.0, 50)
    counts = [count_points_at_tol(t) for t in tols]
    
    # Identify the 'Bite Point'
    bite_tol = None
    for i, c in enumerate(counts):
        if c == 93:
            bite_tol = tols[i]
            break
            
    print(f"BITE POINT SEARCH COMPLETE.")
    if bite_tol:
        print(f"CANONICAL BITE TOLERANCE FOUND: {bite_tol:.4f}")
    else:
        # If not exact, find closest
        closest_idx = np.argmin(np.abs(np.array(counts) - 93))
        print(f"NEAREST BITE TOLERANCE: {tols[closest_idx]:.4f} yielding {counts[closest_idx]} points")

    # 2. Prime Mapping
    residues, matches = analyze_primes(1000)
    print(f"PRIME RESIDUE ANALYSIS: {matches}/1000 primes align with 7-cycle interference.")

    # 3. Visualization: The Vitrification Curve
    plt.figure(figsize=(10, 6))
    plt.plot(tols, counts, 'b-', linewidth=2)
    plt.axhline(y=93, color='r', linestyle='--', label='The Hero 93 Target')
    if bite_tol:
        plt.axvline(x=bite_tol, color='g', alpha=0.5, label=f'Bite Point: {bite_tol:.2f}')
    
    plt.xlabel("Tolerance (ε) - The Vacuum Reach")
    plt.ylabel("Point Count (Distinct Vertices)")
    plt.title("The Vitrification Curve: Finding the Hero 93 Basin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("/Users/studio/ALPHA/PMG_LATTICE/vitrification_curve.png")
    print("PNG SAVED: vitrification_curve.png")
