#!/usr/bin/env python3
"""
Fibonacci Spiral Prime Mapping
==============================
Visualizes primes and subprimes on a Fibonacci/Ulam-style spiral to reveal:
- The characteristic geometry of each "species" (primes, biprimes, triprimes)
- The 3-4-5 triangle harmonic overlays
- The "stacks of balls" topology dominated by 4, 10, 24
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon, Wedge
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm

# ─────────────────────────────────────────────────────────────────────────────
# NUMBER ANALYSIS UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

def factorize(n):
    """Return list of prime factors with multiplicity."""
    if n < 2:
        return []
    factors = []
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        while n % p == 0:
            factors.append(p)
            n //= p
    if n > 1:
        factors.append(n)
    return factors

def omega(n):
    """Number of distinct prime factors."""
    return len(set(factorize(n)))

def Omega(n):
    """Total number of prime factors (with multiplicity)."""
    return len(factorize(n))

def classify(n):
    """
    Classify number by species:
    0 = Unit (1)
    1 = Prime
    2 = Semiprime (biprime: p*q or p²)
    3 = Triprime (p*q*r or p²*q or p³)
    etc.
    """
    return Omega(n)

# ─────────────────────────────────────────────────────────────────────────────
# SPIRAL COORDINATE SYSTEMS
# ─────────────────────────────────────────────────────────────────────────────

def ulam_coords(n):
    """Get (x, y) coordinates for number n on Ulam spiral."""
    if n == 1:
        return (0, 0)
    
    # Which "ring" are we on?
    k = int(np.ceil((np.sqrt(n) - 1) / 2))
    
    # Position within the ring
    d = n - (2*k - 1)**2
    
    if d <= 2*k:
        return (k, -k + d)
    elif d <= 4*k:
        return (k - (d - 2*k), k)
    elif d <= 6*k:
        return (-k, k - (d - 4*k))
    else:
        return (-k + (d - 6*k), -k)

def fibonacci_spiral_coords(n, scale=0.5):
    """
    Approximate Fibonacci spiral coordinates.
    Golden angle ≈ 137.5°
    """
    golden_angle = np.pi * (3 - np.sqrt(5))  # ~2.4 radians
    theta = n * golden_angle
    r = scale * np.sqrt(n)
    return (r * np.cos(theta), r * np.sin(theta))

# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def create_spiral_visualization():
    """Create multi-panel spiral visualization."""
    
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("Fibonacci Spiral Prime Mapping: Polygons All The Way Down",
                 fontsize=14, fontweight='bold', y=0.98, color='white')
    fig.patch.set_facecolor('#0d0d1a')
    
    primes_set = set(sieve(2500))
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 1: Ulam Spiral with Species Colors
    # ─────────────────────────────────────────────────────────────────────────
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_facecolor('#0d0d1a')
    
    # Color map for species
    species_colors = {
        0: '#1a1a2e',    # Unit (1)
        1: '#00ff88',    # Prime
        2: '#4a90d9',    # Biprime
        3: '#ffd700',    # Triprime
        4: '#ff6b35',    # Quadprime
        5: '#ff4444',    # 5+
    }
    
    max_n = 1600
    for n in range(1, max_n + 1):
        x, y = ulam_coords(n)
        species = min(classify(n), 5)
        color = species_colors[species]
        size = 20 if species == 1 else 8
        ax1.scatter(x, y, c=color, s=size, alpha=0.8)
    
    ax1.set_xlim(-25, 25)
    ax1.set_ylim(-25, 25)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x', color='white')
    ax1.set_ylabel('y', color='white')
    ax1.set_title('Ulam Spiral: Species Coloring\nGreen=Prime, Blue=Biprime, Gold=Triprime', 
                  fontsize=10, color='white')
    ax1.tick_params(colors='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 2: Fibonacci Spiral with Polygonal Markers
    # ─────────────────────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_facecolor('#0d0d1a')
    
    patches = []
    colors_list = []
    
    for n in range(1, 500):
        x, y = fibonacci_spiral_coords(n, scale=0.8)
        species = min(classify(n), 5)
        
        if species == 0:  # Unit
            continue
        elif species == 1:  # Prime = vertex (small circle)
            patch = Circle((x, y), 0.15, fill=True)
        elif species == 2:  # Biprime = digon (line/ellipse)
            patch = Circle((x, y), 0.12, fill=True)
        elif species == 3:  # Triprime = triangle
            patch = RegularPolygon((x, y), numVertices=3, radius=0.15)
        elif species == 4:  # Quadprime = square
            patch = RegularPolygon((x, y), numVertices=4, radius=0.15)
        else:  # Higher = pentagon
            patch = RegularPolygon((x, y), numVertices=5, radius=0.15)
        
        patches.append(patch)
        colors_list.append(species_colors[species])
    
    for patch, color in zip(patches, colors_list):
        patch.set_facecolor(color)
        patch.set_edgecolor('white')
        patch.set_linewidth(0.3)
        patch.set_alpha(0.8)
        ax2.add_patch(patch)
    
    ax2.set_xlim(-20, 20)
    ax2.set_ylim(-20, 20)
    ax2.set_aspect('equal')
    ax2.set_xlabel('x', color='white')
    ax2.set_ylabel('y', color='white')
    ax2.set_title('Fibonacci Spiral: Polygonal Signatures\n●=Prime, ●=Biprime, △=Triprime, □=4+', 
                  fontsize=10, color='white')
    ax2.tick_params(colors='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 3: The 3-4-5 Harmonic Overlay
    # ─────────────────────────────────────────────────────────────────────────
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor('#0d0d1a')
    
    # Draw the "stacks of balls" at radii 3, 4, 5 (and 6, 12, 24)
    key_radii = [3, 4, 5, 6, 12, 24]
    for r in key_radii:
        circle = Circle((0, 0), r, fill=False, edgecolor='cyan', 
                        linewidth=1, alpha=0.5, linestyle='--')
        ax3.add_patch(circle)
        ax3.text(r * 0.9, 0.2, str(r), color='cyan', fontsize=8)
    
    # Plot primes on radial position = distance to nearest 6k±1
    for n in range(2, 150):
        if n in primes_set:
            # Position on circle at angle = n * golden_angle
            angle = n * np.pi * (3 - np.sqrt(5))
            r = 5 + (n % 24) / 4  # Vary radius based on mod 24
            x, y = r * np.cos(angle), r * np.sin(angle)
            ax3.scatter(x, y, c='#00ff88', s=40, alpha=0.8, zorder=5)
    
    # Draw the 3-4-5 triangle
    triangle_x = [0, 3, 3, 0]
    triangle_y = [0, 0, 4, 0]
    ax3.plot(triangle_x, triangle_y, color='#ffd700', linewidth=2, 
             label='3-4-5 Triangle')
    ax3.fill(triangle_x, triangle_y, color='#ffd700', alpha=0.2)
    
    ax3.set_xlim(-30, 30)
    ax3.set_ylim(-30, 30)
    ax3.set_aspect('equal')
    ax3.set_xlabel('x', color='white')
    ax3.set_ylabel('y', color='white')
    ax3.set_title('3-4-5 Harmonic Overlay\nCircles at r=3,4,5,6,12,24', 
                  fontsize=10, color='white')
    ax3.tick_params(colors='white')
    ax3.legend(loc='upper right', fontsize=8, facecolor='#1a1a2e', labelcolor='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 4: Spherical Packing Density (24-Grid Torus Cross-Section)
    # ─────────────────────────────────────────────────────────────────────────
    ax4 = fig.add_subplot(2, 2, 4, projection='polar')
    ax4.set_facecolor('#0d0d1a')
    
    # Show the "alive lanes" as wedges on a polar plot
    alive_residues = [1, 5, 7, 11, 13, 17, 19, 23]
    
    for res in range(24):
        angle = 2 * np.pi * res / 24
        width = 2 * np.pi / 24
        
        if res in alive_residues:
            color = '#00ff88'
            alpha = 0.6
        else:
            color = '#ff4444'
            alpha = 0.2
        
        wedge = Wedge(center=(0, 0), r=1, theta1=np.degrees(angle - width/2),
                      theta2=np.degrees(angle + width/2))
        ax4.bar(angle, 1, width=width, bottom=0.3, color=color, alpha=alpha,
                edgecolor='white', linewidth=0.5)
    
    # Mark primes on the wheel
    for p in sieve(100):
        if p > 3:
            angle = 2 * np.pi * (p % 24) / 24
            r = 0.8 + (p % 100) / 200
            ax4.scatter(angle, r, c='white', s=20, marker='*', zorder=5)
    
    ax4.set_ylim(0, 1.3)
    ax4.set_title('24-Grid Torus Cross-Section\nGreen=Alive Lanes, *=Prime positions', 
                  fontsize=10, color='white', pad=15)
    ax4.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('/Users/studio/00 Constellation/Reiman/fibonacci_spiral_analysis.png',
                dpi=150, facecolor='#0d0d1a', edgecolor='none',
                bbox_inches='tight')
    plt.close()
    
    # ─────────────────────────────────────────────────────────────────────────
    # ANALYSIS OUTPUT
    # ─────────────────────────────────────────────────────────────────────────
    print("=" * 70)
    print("FIBONACCI SPIRAL PRIME ANALYSIS")
    print("=" * 70)
    
    print("\n🌀 SPIRAL PATTERNS")
    print("-" * 70)
    print("""
On the Ulam Spiral:
  • Primes form diagonal lines (not random!)
  • These diagonals correspond to quadratic polynomials
  • The 24-grid constraint creates 8 preferred directions

On the Fibonacci Spiral:
  • Primes appear at golden-angle intervals
  • The phyllotactic pattern minimizes overlap
  • Each "species" has characteristic spacing
    """)
    
    print("\n🔺 THE 3-4-5 CONNECTION")
    print("-" * 70)
    print("""
The 3-4-5 triangle encodes:
  • Perimeter: 3 + 4 + 5 = 12 (the harmonic hub)
  • Area: ½ × 3 × 4 = 6 (the 6k±1 symmetry)
  • Hypotenuse²: 5² = 25 = 24 + 1 (first composite in prime lane)

Circles at r = 3, 4, 5, 6, 12, 24 reveal:
  • 6 = LCM(2,3) → first sieve layer
  • 12 = 2×6 → "zodiac" completion
  • 24 = 4×6 → the "second circle" where p² ≡ 1 (mod 24)
    """)
    
    print("\n🔵 SPHERE PACKING ANALOGY")
    print("-" * 70)
    print("""
Numbers as "stacked balls":
  • Primes = outer vertices (only touch 1 and ∞)
  • Biprimes = lens intersections (two spheres touch)
  • Triprimes = triangular voids (three spheres meet)
  
The Leech Lattice (24-dimensional optimal packing) connects:
  • 24 columns of the grid
  • 24 in the Dedekind eta function: η(τ) = q^(1/24) ∏(1-q^n)
  • 24 as the "resonant frequency" of number space
    """)
    
    print("\n✓ Visualization saved to: Reiman/fibonacci_spiral_analysis.png")

if __name__ == "__main__":
    create_spiral_visualization()
