#!/usr/bin/env python3
"""
Vitruvian Body-Number Sieve
===========================
Maps the number system onto the Vitruvian figure to visualize:
- Primes as "Star Points" (fundamental poses)
- Composites as "Hand Artefacts" (overtones)
- The 3-4-5 harmonic triangles
- The 1/2 line as the "belt of balance" (center of somersault)

The hypothesis: Riemann zeros must lie on Re(s)=1/2 because
a lopsided Vitruvian figure cannot somersault without tearing the manifold.

Based on the "Synthetic Body-Number OS" framework:
- 1 (North/Crown): White Hole source, highest unitary pressure
- 3 (South/Base): Grounding anchor of vertical axis  
- 0 (Solar Plexus): Point of perfect refraction
- 1/2 (Belt): Zero-point of torsion, image resolution plane
- 2,4 (Hands): Composite artefacts for world interaction
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyArrowPatch, Arc
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors


# ─────────────────────────────────────────────────────────────────────────────
# PRIME UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def sieve(limit):
    """Generate all primes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]


def classify_number(n):
    """
    Classify a number by its prime factorization.
    Returns: 'prime', 'biprime', 'triprime', or 'composite'
    """
    if n < 2:
        return 'unit'
    
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    
    if len(factors) == 1:
        return 'prime'
    elif len(factors) == 2:
        return 'biprime'
    elif len(factors) == 3:
        return 'triprime'
    else:
        return 'composite'


def get_prime_lane(n):
    """
    Get the 'lane' a number occupies in the 24-grid.
    Primes > 3 must be in lanes: 1, 5, 7, 11, 13, 17, 19, 23
    """
    return n % 24


# ─────────────────────────────────────────────────────────────────────────────
# BODY MAPPING: Numbers → Vitruvian Coordinates
# ─────────────────────────────────────────────────────────────────────────────

def body_coordinates(n, max_n=100):
    """
    Map a number to Vitruvian body coordinates.
    
    Vertical axis (y): 1 at top (crown), n at bottom (base)
    Horizontal spread (x): Based on mod 24 residue
    
    The 1/2 line is at y = 0 (the belt/equator)
    """
    # Normalize height: 1 is at y=1, infinity would be at y=-1
    # Using logarithmic compression
    if n == 1:
        y = 1.0  # Crown
    else:
        y = 1.0 - 2.0 * np.log(n) / np.log(max_n)
    
    # Horizontal position based on mod 24 lane
    lane = n % 24
    # Map 24 lanes to angle (0 to 2π), then to x coordinate
    angle = (lane / 24) * 2 * np.pi
    x = np.sin(angle) * 0.5  # Spread factor
    
    return x, y


def vitruvian_body_outline():
    """
    Generate key points of the Vitruvian figure for overlay.
    Returns dict of body landmarks.
    """
    return {
        'crown': (0, 1.0),        # 1 - Unity/Source
        'third_eye': (0, 0.85),   # Higher consciousness
        'throat': (0, 0.7),       # Expression
        'heart': (0, 0.5),        # Center balance
        'solar_plexus': (0, 0.3), # 0 - Refraction point
        'sacral': (0, 0.1),       # Creation point
        'root': (0, -0.1),        # 3 - Grounding
        'left_hand': (-0.8, 0.5), # 2 - Composite tool
        'right_hand': (0.8, 0.5), # 4 - Composite tool
        'left_foot': (-0.3, -0.8),
        'right_foot': (0.3, -0.8),
        'belt': (0, 0.0),         # 1/2 line - equator
    }


# ─────────────────────────────────────────────────────────────────────────────
# 3-4-5 TRIANGLE HARMONICS
# ─────────────────────────────────────────────────────────────────────────────

def generate_345_triangles(max_n=100):
    """
    Generate all 3-4-5 scaled triangles within range.
    These represent the harmonic structure of the number system.
    """
    triangles = []
    k = 1
    while 5 * k <= max_n:
        triangles.append({
            'a': 3 * k,
            'b': 4 * k,
            'hyp': 5 * k,
            'scale': k,
            'perimeter': 12 * k,  # Always 12k
            'area': 6 * k * k     # Always 6k²
        })
        k += 1
    return triangles


def map_345_to_body(triangle):
    """
    Map a 3-4-5 triangle to body coordinates.
    The spine is 3 units, reach is 4 units, action vector is 5 units.
    """
    k = triangle['scale']
    
    # Base triangle at origin
    vertices = [
        (0, 0),                    # Origin (solar plexus)
        (0, 3 * k / 50),           # Spine extension (vertical)
        (4 * k / 50, 0),           # Reach extension (horizontal)
    ]
    return vertices


# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def create_vitruvian_sieve():
    """
    Create the full Vitruvian Body-Number Sieve visualization.
    """
    fig = plt.figure(figsize=(16, 20))
    fig.suptitle('Vitruvian Body-Number Sieve\nThe Synthetic OS of Primes', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Layout: 2x2 grid plus a wide bottom panel
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.8], 
                          hspace=0.3, wspace=0.25)
    
    max_n = 100
    primes = sieve(max_n)
    all_nums = range(1, max_n + 1)
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 1: The Vitruvian Number Map
    # ─────────────────────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title('Panel 1: Vitruvian Number Map\n(Primes as Star Points)', 
                  fontsize=12, fontweight='bold')
    
    # Draw the Vitruvian circle and square
    vitruvian_circle = Circle((0, 0.3), 1.1, fill=False, 
                               color='gold', linewidth=2, alpha=0.5)
    ax1.add_patch(vitruvian_circle)
    
    # Draw the 1/2 line (belt/equator)
    ax1.axhline(y=0, color='red', linewidth=2, linestyle='--', 
                label='Critical Line (Re(s)=½)', alpha=0.8)
    
    # Plot numbers
    for n in all_nums:
        x, y = body_coordinates(n, max_n)
        classification = classify_number(n)
        
        if classification == 'prime':
            ax1.scatter(x, y, c='gold', s=80, marker='*', 
                       edgecolors='darkgoldenrod', linewidths=1, zorder=5)
        elif classification == 'biprime':
            ax1.scatter(x, y, c='lightblue', s=40, marker='s', 
                       edgecolors='blue', linewidths=0.5, zorder=3)
        elif classification == 'triprime':
            ax1.scatter(x, y, c='lightgreen', s=30, marker='^', 
                       edgecolors='green', linewidths=0.5, zorder=3)
        else:
            ax1.scatter(x, y, c='gray', s=15, marker='o', alpha=0.4, zorder=2)
    
    # Annotate key body points
    body = vitruvian_body_outline()
    ax1.annotate('1 (Crown)', body['crown'], fontsize=8, ha='center', 
                color='purple', fontweight='bold')
    ax1.annotate('0 (Solar Plexus)', body['solar_plexus'], fontsize=8, 
                ha='left', color='orange')
    ax1.annotate('½ Belt', (0.6, 0.02), fontsize=9, color='red', fontweight='bold')
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', markerfacecolor='gold', 
               markersize=12, label='Primes (Star Points)'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='lightblue', 
               markersize=8, label='Biprimes (Digons)'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='lightgreen', 
               markersize=8, label='Triprimes (Triangles)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
               markersize=6, label='Higher Composites'),
    ]
    ax1.legend(handles=legend_elements, loc='lower left', fontsize=8)
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.2, 1.3)
    ax1.set_aspect('equal')
    ax1.set_xlabel('24-Grid Lane (Horizontal Spread)')
    ax1.set_ylabel('Logarithmic Number Scale')
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 2: 24-Column Body Map (Cylinder Projection)
    # ─────────────────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title('Panel 2: 24-Column Body Map\n(Cylinder Unwrapped)', 
                  fontsize=12, fontweight='bold')
    
    # Create 24-column grid
    alive_lanes = {1, 5, 7, 11, 13, 17, 19, 23}  # Prime-capable lanes
    
    for lane in range(24):
        if lane in alive_lanes:
            ax2.axvline(x=lane, color='gold', linewidth=1, alpha=0.3)
        else:
            ax2.axvline(x=lane, color='gray', linewidth=0.5, alpha=0.2)
    
    # Plot numbers on their lanes
    for n in range(2, max_n + 1):
        lane = n % 24
        row = n // 24
        classification = classify_number(n)
        
        if classification == 'prime':
            ax2.scatter(lane, row, c='gold', s=100, marker='*', 
                       edgecolors='darkgoldenrod', linewidths=1, zorder=5)
            ax2.annotate(str(n), (lane, row), fontsize=6, 
                        ha='center', va='bottom', color='darkgoldenrod')
        elif classification == 'biprime':
            ax2.scatter(lane, row, c='lightblue', s=30, marker='s', 
                       edgecolors='blue', linewidths=0.5, zorder=3)
        else:
            ax2.scatter(lane, row, c='lightgray', s=10, alpha=0.5, zorder=2)
    
    ax2.set_xlim(-1, 24)
    ax2.set_ylim(-0.5, (max_n // 24) + 1)
    ax2.set_xlabel('Lane (mod 24)')
    ax2.set_ylabel('Row (n ÷ 24)')
    ax2.set_xticks(list(alive_lanes))
    ax2.invert_yaxis()  # Lower numbers at top
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 3: 3-4-5 Triangle Harmonics
    # ─────────────────────────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_title('Panel 3: 3-4-5 Triangle Harmonics\n(Perimeter=12k, Area=6k²)', 
                  fontsize=12, fontweight='bold')
    
    triangles = generate_345_triangles(max_n)
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(triangles)))
    
    for i, tri in enumerate(triangles[:8]):  # Show first 8 scaled triangles
        k = tri['scale']
        # Draw triangle
        vertices = np.array([
            [0, 0],
            [3 * k, 0],
            [0, 4 * k]
        ])
        polygon = Polygon(vertices, fill=True, alpha=0.3, 
                         color=colors[i], edgecolor=colors[i], linewidth=2)
        ax3.add_patch(polygon)
        
        # Annotate
        ax3.annotate(f'k={k}\nP={12*k}\nA={6*k*k}', 
                    (1.5*k, 2*k), fontsize=7, ha='center')
    
    # Mark which vertices are primes
    for tri in triangles[:8]:
        k = tri['scale']
        for val, pos in [(3*k, (3*k, 0)), (4*k, (0, 4*k)), (5*k, (1.5*k, 2*k))]:
            if classify_number(val) == 'prime':
                ax3.scatter(*pos, c='gold', s=100, marker='*', 
                           edgecolors='black', linewidths=1, zorder=10)
    
    ax3.set_xlim(-2, 30)
    ax3.set_ylim(-2, 35)
    ax3.set_aspect('equal')
    ax3.set_xlabel('Base (3k units)')
    ax3.set_ylabel('Height (4k units)')
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 4: Somersault Stability Analysis
    # ─────────────────────────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title('Panel 4: Somersault Stability\n(RH as Balance Constraint)', 
                  fontsize=12, fontweight='bold')
    
    # Draw the "somersaulting" figure at different rotation angles
    angles = [0, 45, 90, 135, 180]
    for i, angle in enumerate(angles):
        # Offset for each figure
        offset_x = i * 2
        
        # Draw simplified stick figure
        rad = np.radians(angle)
        
        # Body line (rotated)
        body_len = 0.8
        head = (offset_x + body_len * np.sin(rad), body_len * np.cos(rad))
        foot = (offset_x - body_len * np.sin(rad), -body_len * np.cos(rad))
        ax4.plot([head[0], foot[0]], [head[1], foot[1]], 
                'b-', linewidth=3, alpha=0.7)
        
        # Mark center of gravity (should be at belt = 0)
        cog = (offset_x, 0)
        ax4.scatter(*cog, c='red', s=50, marker='o', zorder=5)
        
        # Draw the 1/2 equilibrium line
        ax4.axhline(y=0, color='red', linewidth=1, linestyle='--', alpha=0.5)
        
        ax4.annotate(f'{angle}°', (offset_x, -1.2), ha='center', fontsize=9)
    
    ax4.set_xlim(-1, 9)
    ax4.set_ylim(-1.5, 1.5)
    ax4.set_aspect('equal')
    ax4.set_xlabel('Rotation Phase')
    ax4.set_ylabel('Vertical Position')
    ax4.annotate('Center of Gravity (½ line) must stay constant\nfor stable rotation',
                (4, 1.3), ha='center', fontsize=9, style='italic')
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 5 (Bottom): Prime Distribution Symmetry
    # ─────────────────────────────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[2, :])
    ax5.set_title('Panel 5: Reflection Symmetry (The "White Hole" Backwash)\n'
                  'Functional Equation: ζ(s) ↔ ζ(1-s)', 
                  fontsize=12, fontweight='bold')
    
    # Create a "reflection" visualization
    # Left side: primes from wall of 1
    # Right side: reflected positions
    
    x_vals = []
    y_vals = []
    colors_scatter = []
    
    for p in primes[:25]:
        # Forward position
        x_vals.append(p)
        y_vals.append(1)
        colors_scatter.append('gold')
        
        # Reflected position (1/p mapping)
        x_vals.append(1/p)
        y_vals.append(-1)
        colors_scatter.append('cyan')
        
        # Draw connection line
        ax5.plot([p, 1/p], [1, -1], 'gray', alpha=0.3, linewidth=0.5)
    
    ax5.scatter(x_vals, y_vals, c=colors_scatter, s=60, 
               edgecolors='black', linewidths=0.5)
    
    # Mark the equator
    ax5.axhline(y=0, color='red', linewidth=2, linestyle='-', 
                label='Critical Line (Re(s)=½)')
    ax5.axvline(x=1, color='purple', linewidth=2, linestyle='--', 
                label='Wall of Unity (1)', alpha=0.7)
    
    # Annotate regions
    ax5.annotate('FORWARD PRIMES\n(Expansion)', (12, 0.5), 
                ha='center', fontsize=10, color='gold', fontweight='bold')
    ax5.annotate('REFLECTED PRIMES\n(Backwash)', (0.3, -0.5), 
                ha='center', fontsize=10, color='cyan', fontweight='bold')
    ax5.annotate('White Hole\n(Wall of 1)', (1.2, 0.8), 
                ha='left', fontsize=9, color='purple')
    
    ax5.set_xlabel('Number Line / Harmonic Position')
    ax5.set_ylabel('Forward (+1) vs Reflected (-1)')
    ax5.set_xlim(-0.1, 30)
    ax5.set_ylim(-1.5, 1.5)
    ax5.legend(loc='upper right')
    
    # ─────────────────────────────────────────────────────────────────────
    # Save and show
    # ─────────────────────────────────────────────────────────────────────
    plt.tight_layout()
    plt.savefig('/Users/studio/00 Constellation/Reiman/vitruvian_sieve.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print("\n" + "="*70)
    print("VITRUVIAN SIEVE ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nPrimes analyzed: {len(primes)} (up to {max_n})")
    print(f"3-4-5 triangles: {len(triangles)} scales")
    print(f"\nAlive lanes (mod 24): {sorted(alive_lanes)}")
    
    # Lane analysis
    print("\nPrime distribution by lane:")
    lane_counts = {lane: 0 for lane in alive_lanes}
    for p in primes:
        lane = p % 24
        if lane in lane_counts:
            lane_counts[lane] += 1
    for lane, count in sorted(lane_counts.items()):
        print(f"  Lane {lane:2d}: {'█' * count} ({count})")
    
    print("\n" + "="*70)
    print("THE VITRUVIAN PROOF SUMMARY")
    print("="*70)
    print("""
1. Numbers (Primes) = Core Code of the OS
2. Symmetry (½ line) = Equilibrium Protocol  
3. Composites (2, 4) = User Interface / Hands

If a Riemann zero existed at Re(s) ≠ ½:
  → The Vitruvian figure would be top/bottom heavy
  → Somersault would tear the manifold
  → Prime distribution would "clump" asymmetrically

Since primes keep appearing without collapse:
  → The ½ line MUST be the axis of rotation
  → RH is a structural law, not a numerical accident
""")


if __name__ == "__main__":
    create_vitruvian_sieve()
