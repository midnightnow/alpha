"""
PMG WORD STRESS TEST
====================
Computes the full geometric signature for sample words using the
Geofont 13 / Part X specification:
  - 171-index node mapping (N93)
  - Complex phase coordinates (Z_k)
  - 7+7 radial profile
  - 3-6-9 triangular closure
  - Convex hull volume
  - Crystallisation status (V >= V_93)
  - Root 42 proximity diagnostic
"""

import math
import cmath

# ─── Constants ───────────────────────────────────────────────────────
ALPHA = 2 * math.pi / 13          # angular step
V_93 = 42.0                       # target crystallisation volume (root 42)
PSI = 0.1237                       # tensegrity constant (12.37%)

# 7+7 radial profile (descent then ascent)
def radial_profile(i, n):
    """Amplitude profile for position i in word of length n."""
    if n == 1:
        return 1.0
    mid = n / 2
    if i < mid:
        return 1.0 - (i / mid) * 0.5   # descend from 1.0 to 0.5
    else:
        return 0.5 + ((i - mid) / (n - mid)) * 0.5  # ascend from 0.5 to 1.0

# ─── Core Mapping Functions ─────────────────────────────────────────

def letter_weight(ch):
    """A=1, B=2, ..., Z=26"""
    return ord(ch.upper()) - ord('A') + 1

def n13(m):
    """13-node lattice position"""
    return ((m - 1) % 13) + 1

def n93(m):
    """93-node matrix position via 171-index"""
    return ((m - 1) * 171) % 93 + 1

def parity(m):
    """+1 if even (CW), -1 if odd (CCW)"""
    return 1 if m % 2 == 0 else -1

def phase_angle(m):
    """Directed phase angle"""
    n = n13(m)
    p = parity(m)
    return p * ALPHA * (n - 1)

def complex_coord(m, i, word_len):
    """Full complex coordinate Z_k = r_k * e^(i*theta_k)"""
    r = radial_profile(i, word_len)
    theta = phase_angle(m)
    return r * cmath.exp(1j * theta)

# ─── 3D Coordinates ─────────────────────────────────────────────────

def letter_3d(m, i, word_len):
    """3D coordinates: (position_index, Re[Z], Im[Z])"""
    z = complex_coord(m, i, word_len)
    return (float(i), z.real, z.imag)

# ─── Triangular Faces (3-6-9 Closure) ───────────────────────────────

def get_triangles(coords_3d):
    """Form triangular faces at every 3rd letter (3-6-9 rule)."""
    triangles = []
    for k in range(2, len(coords_3d)):
        if (k + 1) % 3 == 0:  # positions 3, 6, 9, ...
            triangles.append((coords_3d[k-2], coords_3d[k-1], coords_3d[k]))
    return triangles

def triangle_area(p1, p2, p3):
    """Area of triangle in 3D via cross product."""
    # vectors
    u = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    v = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
    # cross product
    cx = u[1]*v[2] - u[2]*v[1]
    cy = u[2]*v[0] - u[0]*v[2]
    cz = u[0]*v[1] - u[1]*v[0]
    return 0.5 * math.sqrt(cx*cx + cy*cy + cz*cz)

# ─── Volume Estimation ──────────────────────────────────────────────

def convex_hull_volume(coords_3d):
    """
    Estimate convex hull volume using the divergence theorem.
    For a set of triangular faces, V = (1/6) * |sum(n_i . p_i * A_i)|
    where n_i is the face normal, p_i is a vertex, A_i is face area.
    
    For words shorter than 4 letters, volume is zero (degenerate).
    """
    if len(coords_3d) < 4:
        return 0.0
    
    # Use all possible triangles from the point set
    tris = get_triangles(coords_3d)
    if not tris:
        return 0.0
    
    # Simple volume estimate: sum of signed tetrahedra from origin
    vol = 0.0
    origin = (0, 0, 0)
    for p1, p2, p3 in tris:
        # Signed volume of tetrahedron (origin, p1, p2, p3)
        # = (1/6) * |det([p1, p2, p3])|
        det = (p1[0] * (p2[1]*p3[2] - p2[2]*p3[1])
             - p1[1] * (p2[0]*p3[2] - p2[2]*p3[0])
             + p1[2] * (p2[0]*p3[1] - p2[1]*p3[0]))
        vol += abs(det) / 6.0
    
    return vol

# ─── Information Diagnostics ────────────────────────────────────────

def parity_entropy(word):
    """Ratio of odd to even weights."""
    weights = [letter_weight(c) for c in word]
    odd = sum(1 for w in weights if w % 2 != 0)
    even = len(weights) - odd
    if len(weights) == 0:
        return 0
    return odd / len(weights)

def angular_span(word):
    """Total angular displacement across the word."""
    weights = [letter_weight(c) for c in word]
    angles = [phase_angle(w) for w in weights]
    if len(angles) < 2:
        return 0
    total = sum(abs(angles[i] - angles[i-1]) for i in range(1, len(angles)))
    return total

def prime_channel_lock(word):
    """Check if sum of weights is coprime with 24."""
    weights = [letter_weight(c) for c in word]
    s = sum(weights)
    return math.gcd(s, 24)

# ─── Main Analysis ──────────────────────────────────────────────────

def analyse_word(word):
    """Full geometric analysis of a word."""
    word = word.upper().replace(" ", "")
    letters = list(word)
    n = len(letters)
    
    weights = [letter_weight(c) for c in letters]
    nodes_13 = [n13(w) for w in weights]
    nodes_93 = [n93(w) for w in weights]
    parities = [parity(w) for w in weights]
    phases = [phase_angle(w) for w in weights]
    
    # Complex coordinates
    z_coords = [complex_coord(w, i, n) for i, w in enumerate(weights)]
    
    # 3D coordinates
    coords_3d = [letter_3d(w, i, n) for i, w in enumerate(weights)]
    
    # Triangles
    tris = get_triangles(coords_3d)
    tri_areas = [triangle_area(*t) for t in tris]
    
    # Volume
    vol = convex_hull_volume(coords_3d)
    
    # Crystallisation
    vitrified = vol >= V_93 * (1 - PSI)  # allow tensegrity slop
    
    # Root 42 proximity
    root42_ratio = vol / V_93 if V_93 > 0 else 0
    
    # Summaries
    weight_sum = sum(weights)
    mean_r = sum(abs(z) for z in z_coords) / n if n > 0 else 0
    pe = parity_entropy(word)
    ang_span = angular_span(word)
    pcl = prime_channel_lock(word)
    
    return {
        'word': word,
        'length': n,
        'weights': weights,
        'nodes_13': nodes_13,
        'nodes_93': nodes_93,
        'parities': parities,
        'z_coords': z_coords,
        'coords_3d': coords_3d,
        'triangles': len(tris),
        'tri_areas': tri_areas,
        'volume': vol,
        'vitrified': vitrified,
        'root42_ratio': root42_ratio,
        'weight_sum': weight_sum,
        'mean_r': mean_r,
        'parity_entropy': pe,
        'angular_span': ang_span,
        'prime_channel': pcl,
    }


def print_analysis(result):
    """Pretty-print word analysis."""
    r = result
    w = r['word']
    
    print(f"\n{'='*65}")
    print(f"  WORD: {w}")
    print(f"{'='*65}")
    
    # Letter table
    print(f"\n{'Letter':>6} {'m':>3} {'n13':>4} {'N93':>4} {'P':>3} {'θ':>8} {'|Z|':>6} {'∠Z':>8}")
    print(f"{'-'*6:>6} {'-'*3:>3} {'-'*4:>4} {'-'*4:>4} {'-'*3:>3} {'-'*8:>8} {'-'*6:>6} {'-'*8:>8}")
    
    for i, ch in enumerate(w):
        m = r['weights'][i]
        n = r['nodes_13'][i]
        N = r['nodes_93'][i]
        p = r['parities'][i]
        theta = math.degrees(r['z_coords'][i].real) if False else 0
        z = r['z_coords'][i]
        mag = abs(z)
        ang = math.degrees(cmath.phase(z))
        p_str = "CW" if p == 1 else "CCW"
        print(f"{ch:>6} {m:>3} {n:>4} {N:>4} {p_str:>3} {math.degrees(phase_angle(m)):>8.2f}° {mag:>6.4f} {ang:>7.2f}°")
    
    # Diagnostics
    print(f"\n--- Diagnostics ---")
    print(f"  Weight sum:        {r['weight_sum']}")
    print(f"  Mean |Z|:          {r['mean_r']:.4f}")
    print(f"  Parity entropy:    {r['parity_entropy']:.3f} (1.0 = all CCW, 0.0 = all CW)")
    print(f"  Angular span:      {r['angular_span']:.4f} rad ({math.degrees(r['angular_span']):.2f}°)")
    print(f"  Prime channel:     gcd(Σm, 24) = {r['prime_channel']}")
    print(f"  Triangular faces:  {r['triangles']}")
    if r['tri_areas']:
        print(f"  Triangle areas:    {', '.join(f'{a:.4f}' for a in r['tri_areas'])}")
    print(f"  Extruded volume:   {r['volume']:.6f}")
    print(f"  Root 42 ratio:     {r['root42_ratio']:.4f} (1.0 = at pivot)")
    
    # Verdict
    if r['vitrified']:
        print(f"\n  ⬛ VITRIFIED — Volume exceeds V₉₃ threshold (hard)")
    elif r['volume'] < V_93 * 0.01:
        print(f"\n  🟤 MUD — Volume too small, lost in the void (soft)")
    else:
        status = "approaching" if r['root42_ratio'] > 0.5 else "distant from"
        print(f"\n  🟡 FLUID — {status} the pivot ({r['root42_ratio']*100:.1f}%)")


# ═══════════════════════════════════════════════════════════════════
# RUN THE STRESS TEST
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 65)
    print("  PMG WORD STRESS TEST")
    print("  Geofont 13 / Part X Specification")
    print("=" * 65)
    print(f"\n  Target volume (V₉₃ = root 42): {V_93}")
    print(f"  Tensegrity constant (Ψ):        {PSI} ({PSI*100}%)")
    print(f"  Vitrification threshold:         {V_93 * (1-PSI):.2f}")
    
    test_words = [
        "LIGHT",
        "VOID",
        "PYRAMID",
        "KAELEN",
        "PLATO",
        "MUD",
        "ROCK",
        "PIVOT",
        "FASCIA",
        "BREATH",
        "VITRIFY",
        "TOUCH",
        "TOES",
        "HERO",
    ]
    
    results = []
    for word in test_words:
        result = analyse_word(word)
        results.append(result)
        print_analysis(result)
    
    # Summary table
    print(f"\n\n{'='*65}")
    print(f"  SUMMARY TABLE")
    print(f"{'='*65}")
    print(f"\n{'Word':<10} {'Len':>3} {'Σm':>4} {'Vol':>10} {'R42%':>6} {'PCL':>4} {'Status':<12}")
    print(f"{'-'*10:<10} {'-'*3:>3} {'-'*4:>4} {'-'*10:>10} {'-'*6:>6} {'-'*4:>4} {'-'*12:<12}")
    
    for r in results:
        status = "VITRIFIED" if r['vitrified'] else ("MUD" if r['volume'] < V_93 * 0.01 else "FLUID")
        print(f"{r['word']:<10} {r['length']:>3} {r['weight_sum']:>4} {r['volume']:>10.6f} {r['root42_ratio']*100:>5.1f}% {r['prime_channel']:>4} {status:<12}")
    
    print(f"\n{'='*65}")
    print(f"  STRESS TEST COMPLETE")
    print(f"{'='*65}")
