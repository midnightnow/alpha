#!/usr/bin/env python3
"""
3D Prime Topology: The Zeta Landscape
======================================
Visualizes the "undeclared topology" where:
- The number plane is a surface with curvature
- Primes are gravitational wells/nodes
- The Critical Line (σ = ½) is the equator of reflection symmetry
- Unity (1) acts as a "White Hole" reflector

Based on the "Handball" analogy:
  Hand = Observer, Ball = Number, Wall = Unity, Floor = Re(s)=0
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# PRIME UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

# ─────────────────────────────────────────────────────────────────────────────
# 3D PRIME HELIX (24-COLUMN CYLINDER)
# ─────────────────────────────────────────────────────────────────────────────

def create_prime_helix():
    """Create the Prime Helix winding around a 24-column cylinder."""
    
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("3D Prime Topology: The Helix and the Zeta Landscape",
                 fontsize=13, fontweight='bold', y=0.98, color='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 1: Prime Helix on 24-Column Cylinder
    # ─────────────────────────────────────────────────────────────────────────
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.set_facecolor('#0d0d1a')
    
    primes = set(sieve(200))
    
    # Create helix path
    n_points = 200
    theta = []
    z_vals = []
    colors = []
    sizes = []
    
    for n in range(1, n_points + 1):
        angle = 2 * np.pi * (n % 24) / 24
        theta.append(angle)
        z_vals.append(n)
        
        if n in primes:
            colors.append('#00ff88')  # Prime = green
            sizes.append(50)
        else:
            colors.append('#ff4444' if n > 3 else '#888888')  # Composite = red
            sizes.append(10)
    
    x = np.cos(theta)
    y = np.sin(theta)
    z = z_vals
    
    # Plot the helix
    ax1.scatter(x, y, z, c=colors, s=sizes, alpha=0.8)
    
    # Draw the 8 "alive lanes" as vertical lines
    alive_residues = [1, 5, 7, 11, 13, 17, 19, 23]
    for res in alive_residues:
        angle = 2 * np.pi * res / 24
        ax1.plot([np.cos(angle)]*2, [np.sin(angle)]*2, [0, 200], 
                 color='cyan', alpha=0.2, linewidth=2)
    
    ax1.set_xlabel('X (cos θ)', color='white')
    ax1.set_ylabel('Y (sin θ)', color='white')
    ax1.set_zlabel('n (integer)', color='white')
    ax1.set_title('Prime Helix (24-Column Cylinder)\nGreen=Primes, Red=Composites', 
                  fontsize=10, color='white')
    ax1.tick_params(colors='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 2: The "Gravity Well" Landscape (Prime Tension Map)
    # ─────────────────────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    ax2.set_facecolor('#0d0d1a')
    
    # Create a surface where primes create "wells"
    x_grid = np.linspace(0.1, 1.0, 50)  # Critical strip: 0 < σ < 1
    y_grid = np.linspace(0, 50, 50)     # Imaginary axis
    X, Y = np.meshgrid(x_grid, y_grid)
    
    # The surface starts flat, primes "pull it down"
    Z = np.zeros_like(X)
    
    # Add wells at prime positions
    primes_small = sieve(50)
    for p in primes_small:
        for i, y_val in enumerate(y_grid):
            for j, x_val in enumerate(x_grid):
                # Create a "well" centered at (0.5, p)
                dist = np.sqrt((x_val - 0.5)**2 + (y_val - p)**2)
                Z[i, j] -= 1.0 / (1 + dist**2)  # Gravitational-like falloff
    
    # Create custom colormap
    cmap = LinearSegmentedColormap.from_list('zeta', 
        ['#0d0d1a', '#1a1a4e', '#4a148c', '#00ff88'])
    
    ax2.plot_surface(X, Y, Z, cmap=cmap, alpha=0.8, linewidth=0)
    
    # Mark the critical line (σ = 0.5)
    ax2.plot([0.5]*50, y_grid, np.min(Z)*np.ones(50), 
             color='cyan', linewidth=2, label='Critical Line (σ=½)')
    
    ax2.set_xlabel('σ (Real part)', color='white')
    ax2.set_ylabel('t (Imaginary part)', color='white')
    ax2.set_zlabel('Gravitational Tension', color='white')
    ax2.set_title('Prime Gravity Wells in Critical Strip\nDepressions at σ=½, t=prime', 
                  fontsize=10, color='white')
    ax2.tick_params(colors='white')
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 3: The Reflection Symmetry (White Hole at 1)
    # ─────────────────────────────────────────────────────────────────────────
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor('#0d0d1a')
    
    # Show forward waves (from infinity) and reflected waves (from 1)
    x = np.linspace(0, 2, 500)
    
    # Forward wave (prime-counting approximation)
    forward = np.log(x + 1) / 4
    
    # Reflected wave (backwash from Unity)
    reflected = -np.log(2 - x + 0.1) / 4
    reflected[x > 1.9] = np.nan  # Avoid singularity
    
    # Standing wave (superposition)
    standing = forward + np.nan_to_num(reflected, nan=0)
    
    ax3.fill_between(x, 0, forward, alpha=0.5, color='#00ff88', 
                     label='Forward Wave (→∞)')
    ax3.fill_between(x, 0, reflected, alpha=0.5, color='#ff4444', 
                     label='Reflected Wave (←1)')
    ax3.plot(x, standing, color='cyan', linewidth=2, 
             label='Standing Wave')
    
    ax3.axvline(x=0.5, color='yellow', linestyle='--', linewidth=2, 
                label='Critical Line (σ=½)')
    ax3.axvline(x=1.0, color='white', linestyle='-', linewidth=3, 
                label='"White Hole" (Unity)')
    
    ax3.set_xlabel('σ (Real part of s)', color='white')
    ax3.set_ylabel('Wave Amplitude', color='white')
    ax3.set_title('Reflection Symmetry: The "Handball" Model\n' +
                  'Standing wave forms at σ=½', fontsize=10, color='white')
    ax3.legend(loc='upper left', fontsize=8, facecolor='#1a1a2e', 
               labelcolor='white')
    ax3.tick_params(colors='white')
    ax3.set_xlim(0, 1.5)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 4: The Subprime Polygonal Structure
    # ─────────────────────────────────────────────────────────────────────────
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_facecolor('#0d0d1a')
    
    # Classify numbers by their "polygonal signature"
    def classify_number(n):
        """Return number of distinct prime factors (omega function)."""
        if n < 2:
            return 0
        factors = set()
        temp = n
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
            while temp % p == 0:
                factors.add(p)
                temp //= p
        if temp > 1:
            factors.add(temp)
        return len(factors)
    
    # Create grid showing polygonal signatures
    grid_size = 50
    grid = np.zeros((grid_size, grid_size))
    
    for i in range(grid_size):
        for j in range(grid_size):
            n = i * grid_size + j + 1
            grid[i, j] = classify_number(n)
    
    # Custom colormap for polygonal types
    poly_cmap = LinearSegmentedColormap.from_list('poly',
        ['#000000', '#00ff88', '#4a90d9', '#ffd700', '#ff4444', '#ff00ff'])
    
    im = ax4.imshow(grid, cmap=poly_cmap, aspect='auto', origin='lower',
                    vmin=0, vmax=5)
    
    # Mark primes (omega = 1)
    primes_2500 = set(sieve(2500))
    for p in primes_2500:
        if p <= grid_size * grid_size:
            i = (p - 1) // grid_size
            j = (p - 1) % grid_size
            if i < grid_size:
                ax4.scatter(j, i, color='white', s=3, marker='.')
    
    ax4.set_xlabel('n mod 50', color='white')
    ax4.set_ylabel('n ÷ 50', color='white')
    ax4.set_title('Polygonal Signature Map (ω function)\n' +
                  '0=1, 1=Prime, 2=Biprime, 3=Triprime...', 
                  fontsize=10, color='white')
    ax4.tick_params(colors='white')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax4, ticks=[0, 1, 2, 3, 4, 5])
    cbar.set_label('# of Distinct Prime Factors', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.ax.set_yticklabels(['0 (1)', '1 (Prime)', '2 (Biprime)', 
                             '3 (Triprime)', '4', '5+'], color='white')
    
    plt.tight_layout()
    plt.savefig('/Users/studio/00 Constellation/Reiman/topology_3d_visualization.png',
                dpi=150, facecolor='#0d0d1a', edgecolor='none',
                bbox_inches='tight')
    plt.close()
    
    # ─────────────────────────────────────────────────────────────────────────
    # ANALYSIS OUTPUT
    # ─────────────────────────────────────────────────────────────────────────
    print("=" * 70)
    print("3D PRIME TOPOLOGY ANALYSIS")
    print("=" * 70)
    
    print("\n🌀 THE PRIME HELIX")
    print("-" * 70)
    print("""
The number line wrapped around a 24-column cylinder reveals:
  • Primes form 8 vertical "ribs" (the alive lanes)
  • The helix pitch = 24 (one full rotation per 24 integers)
  • Gaps between primes = steps along the helix
    """)
    
    print("\n🕳️ THE GRAVITY WELL LANDSCAPE")
    print("-" * 70)
    print("""
In the Critical Strip (0 < σ < 1):
  • Primes create "gravitational wells" at σ = ½
  • The depth of each well ∝ 1/distance from (½, p)
  • A "Rogue Zero" would be a well displaced from the σ = ½ curtain
    """)
    
    print("\n🔄 THE REFLECTION SYMMETRY")
    print("-" * 70)
    print("""
The "Handball" model:
  • Forward wave: Counting expanding toward ∞
  • Reflected wave: Backwash from "White Hole" at Unity
  • Standing wave: Perfect cancellation at σ = ½
  
If the Wall of 1 is a perfect reflector, zeros MUST lie on the σ = ½ line.
    """)
    
    print("\n🔷 POLYGONAL SIGNATURES")
    print("-" * 70)
    
    # Count each type
    poly_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for n in range(1, 2501):
        omega = classify_number(n)
        poly_counts[min(omega, 5)] += 1
    
    print("Distribution of ω(n) for n ∈ [1, 2500]:")
    for omega, count in sorted(poly_counts.items()):
        name = ['Unit', 'Prime', 'Biprime', 'Triprime', 'Quadprime', '5+'][omega]
        bar = '█' * (count // 50)
        print(f"  ω={omega} ({name:10s}): {count:4d} {bar}")
    
    print("\n✓ Visualization saved to: Reiman/topology_3d_visualization.png")

if __name__ == "__main__":
    create_prime_helix()
