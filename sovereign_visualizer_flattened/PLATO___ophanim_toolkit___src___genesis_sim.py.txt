import math

def derive_log_spiral_constant():
    """
    Derives the stable growth constant 'b' for the PMG Voronoi-361 partition.
    Formula: b = ln(361/360) / (2 * pi)
    """
    b = math.log(361 / 360) / (2 * math.pi)
    return b

if __name__ == "__main__":
    b = derive_log_spiral_constant()
    print(f"Derived Log-Spiral Constant (b): {b:.10f}")
    # Academic check: matches approx 0.000441
    if abs(b - 0.000441) < 1e-6:
        print("[STATUS]: Log-Spiral Constant b Validated")
