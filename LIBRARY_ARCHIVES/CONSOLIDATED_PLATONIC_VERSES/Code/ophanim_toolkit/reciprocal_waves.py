import math

def analyze_reciprocal_wave(p, q):
    x = p * q
    print(f"--- RECIPROCAL WAVE ANALYSIS: x = {p} * {q} = {x} ---")
    
    # Simple binary expansion mod x
    # The 'jumps' are the values of 2^n mod x
    nodes = []
    # Finite check up to x for cycle
    for n in range(x):
        val = pow(2, n, x)
        nodes.append(val)
        if len(nodes) > 1 and val == nodes[0] and n > 0:
            break
            
    print(f"Cycle length (Binary Expansion Period): {len(nodes)}")
    
    # The 'flanking' of prime factors
    # Let's see if p and q appear near nodes
    for i, val in enumerate(nodes[:20]):
        dist_p = abs(val - p)
        dist_q = abs(val - q)
        print(f"n={i}: 2^{i} mod {x} = {val} | Dist to factors: (p:{dist_p}, q:{dist_q})")

if __name__ == "__main__":
    # Test with USER's 35 (5*7)
    analyze_reciprocal_wave(5, 7)
    print("\n")
    # Test with semi-prime from Robert Grant context (e.g. 7 * 13)
    analyze_reciprocal_wave(7, 13)
