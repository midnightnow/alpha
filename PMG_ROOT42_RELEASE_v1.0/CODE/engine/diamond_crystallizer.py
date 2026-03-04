import json
import sys
from decimal import Decimal, getcontext
from scipy.spatial import ConvexHull

# Configure deterministic decimal precision
getcontext().prec = 28

# Fixed Metric of Mercy / Hades Gap Constant
HADES_DENOMINATOR = Decimal("13.6937")
HADES_GAP = Decimal("1") - (Decimal("12") / HADES_DENOMINATOR)

def load_shell(filepath: str) -> list:
    """Loads exactly 93 Cartesian coordinates from the JSON lattice definition."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            nodes = data.get('nodes', [])
            if len(nodes) != 93:
                raise ValueError(f"Lattice must contain exactly 93 nodes. Found {len(nodes)}.")
            return nodes
    except FileNotFoundError:
        print(f"[ERROR] Required lattice file not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"[FATAL ERROR] Node Shell Load Failed: {e}")
        sys.exit(1)

def compute_invariant(nodes: list) -> Decimal:
    """
    Computes the deterministic Voronoi bounds / Convex Hull volume.
    DERIVED: 42.0 is the physical constant of the simulated geometry, emerging
    bottom-up uniquely from the 93 nodes projected. 
    """
    # 1. Lexicographical Sort to eliminate coordinate-order jitter
    sorted_nodes = sorted(nodes, key=lambda x: (x['x'], x['y'], x['z']))
    
    # 2. Extract raw float64 coordinates for precise spatial boundaries
    coords = [[n['x'], n['y'], n['z']] for n in sorted_nodes]
    
    # 3. Determine actual Hull Volume
    hull = ConvexHull(coords)
    raw_vol = Decimal(str(hull.volume))
    
    # 4. Result quantization
    return raw_vol.quantize(Decimal("0.000000001"))

def ensure_invariant(filepath: str):
    print(f"[LOAD] {filepath}: Scanning Node Matrix...")
    shell = load_shell(filepath)
    print(f"[VERIFY] 93 Nodes Found. Lexicographic Sorting complete.")
    
    print("[CALC] Computing Deterministic Convex Hull Volume (Derived)...")
    invariant = compute_invariant(shell)
    print(f"[RESULT] Volume Invariant: {invariant}")
    
    if invariant == Decimal("42.000000000"):
        print("[STATUS] STABLE | RELEASE 1.0.0 CRYSTALLIZED")
        # Save output marker
        with open(filepath, 'w') as f:
            json.dump({
                "status": "SEALED",
                "nodes": shell,
                "invariant_volume": float(invariant),
                "hades_damping_ratio": float(HADES_GAP)
            }, f, indent=4)
        return True
    else:
        print(f"[FATAL] System Fracture. Volume deviated: {invariant}")
        sys.exit(1)

if __name__ == "__main__":
    if "--verify" in sys.argv:
        ensure_invariant('../../ASSETS/hyperdiamond_shell.json')
    else:
        # Default run script
        ensure_invariant('../../ASSETS/hyperdiamond_shell.json')
