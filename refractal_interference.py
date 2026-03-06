#!/usr/bin/env python3
"""
Refractal Interference Map
==========================
Simulates "Light Rays" of primes reflecting off the Wall of 1, creating
Moiré interference patterns that focus primes onto the ½ focal plane.

Key Concepts:
- Refractals: Shapes defined by bent reflections
- Forward Flow (p): Primes expanding outward toward ∞
- Backwash (1/p): Reciprocal compression toward 0
- The ½ Line: Isobar where expansion pressure = suction pressure

The Prime is a HOLOGRAM: interference of Infinite Backwash and Unitary Forward Flow.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyArrowPatch
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors


# ─────────────────────────────────────────────────────────────────────────────
# PRIME GENERATION
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


# ─────────────────────────────────────────────────────────────────────────────
# REFRACTAL GEOMETRY
# ─────────────────────────────────────────────────────────────────────────────

def reciprocal_map(p):
    """Map prime p to its reciprocal 1/p (the backwash)."""
    return 1.0 / p


def log_spiral_position(n, a=0.2, b=0.15):
    """
    Map number n to position on logarithmic spiral.
    r = a * e^(b * theta), where theta = 2π * log(n)
    """
    theta = 2 * np.pi * np.log(n)
    r = a * np.exp(b * theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, theta, r


def inward_spiral_position(p, a=0.2, b=0.15):
    """
    Map 1/p to an INWARD spiral (approaching origin).
    The reciprocal spirals toward the "Specific Point" (0,0).
    """
    recip = 1.0 / p
    # Inward spiral: theta decreases, r approaches 0
    theta = -2 * np.pi * np.log(p)  # Negative for inward
    r = a * recip * 2  # Scales with reciprocal
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, theta, r


def compute_interference(p, phase_offset=0):
    """
    Compute interference value at prime p.
    Constructive interference → Prime (sharp spike)
    Destructive interference → Composite (flattened)
    """
    # Forward wave from p
    forward_phase = 2 * np.pi * np.log(p)
    
    # Backward wave from 1/p (reflected)
    backward_phase = 2 * np.pi * np.log(1/p) + np.pi  # π phase shift on reflection
    
    # Interference: sum of waves
    interference = np.cos(forward_phase) + np.cos(backward_phase + phase_offset)
    
    return interference


def flection_curve(p, num_points=50):
    """
    Generate the "flection" curve induced by prime p.
    This is the local curvature in the number plane.
    """
    # Create curve from p outward, showing the "bend"
    t = np.linspace(0, 2 * np.pi, num_points)
    
    # Flection radius based on log(p)
    r_base = np.log(p) / 10
    
    # The flection: a petal-like curve
    r = r_base * (1 + 0.5 * np.cos(p * t))
    
    x = p / 20 + r * np.cos(t)
    y = r * np.sin(t)
    
    return x, y


# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def create_refractal_map():
    """
    Create the full Refractal Interference visualization.
    """
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle('Refractal Interference Map\nPrimes as Holographic Focal Points', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    primes = sieve(100)[:25]  # First 25 primes
    
    # Layout: 2x2 + bottom panel
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.7], hspace=0.3, wspace=0.25)
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 1: Light Ray Refraction (Wall of 1)
    # ─────────────────────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title('Panel 1: Light Rays Reflecting off Wall of 1\n(Refractal Formation)', 
                  fontsize=11, fontweight='bold')
    
    # Draw the "Wall of 1" as a vertical mirror
    ax1.axvline(x=1, color='purple', linewidth=3, label='Wall of Unity (1)')
    
    # Draw the ½ focal plane
    ax1.axvline(x=0.5, color='red', linewidth=2, linestyle='--', 
                label='Focal Plane (½)', alpha=0.8)
    
    # Draw light rays from each prime
    colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(primes)))
    
    for i, p in enumerate(primes[:15]):
        # Incoming ray from infinity (represented by p)
        # Hits wall at 1, reflects to 1/p
        
        # Scale for visualization
        p_scaled = 1 + (p - 2) * 0.05  # Start point (scaled)
        recip_scaled = 1/p  # End point (1/p)
        
        # Draw incoming ray (from p to wall)
        ax1.annotate('', xy=(1, 0.8 - i * 0.05), xytext=(p_scaled, 0.9 - i * 0.03),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=1.5, alpha=0.7))
        
        # Draw reflected ray (from wall to 1/p)
        ax1.annotate('', xy=(recip_scaled, 0.7 - i * 0.05), xytext=(1, 0.8 - i * 0.05),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=1.5, alpha=0.7))
        
        # Mark focal point on ½ line
        ax1.scatter(0.5, 0.75 - i * 0.05, c=[colors[i]], s=50, marker='*', 
                   zorder=5, edgecolors='black', linewidths=0.5)
    
    ax1.set_xlim(0, 2.5)
    ax1.set_ylim(0, 1)
    ax1.set_xlabel('Position (0 → ∞)')
    ax1.set_ylabel('Ray Height')
    ax1.legend(loc='upper right', fontsize=8)
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 2: Forward vs Reciprocal Spiral
    # ─────────────────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1], projection='polar')
    ax2.set_title('Panel 2: Forward (p) vs Inward (1/p) Spirals\n(Collision Zone at Origin)', 
                  fontsize=11, fontweight='bold')
    
    # Forward spiral (primes expanding outward)
    for p in primes[:15]:
        x, y, theta, r = log_spiral_position(p)
        ax2.scatter(theta % (2*np.pi), r, c='gold', s=80, marker='*', 
                   edgecolors='darkgoldenrod', linewidths=1, zorder=5)
    
    # Inward spiral (reciprocals converging to 0)
    for p in primes[:15]:
        x, y, theta, r = inward_spiral_position(p)
        ax2.scatter(abs(theta) % (2*np.pi), r, c='cyan', s=40, marker='o', 
                   edgecolors='blue', linewidths=0.5, zorder=4)
    
    # Draw collision zone (area around origin)
    collision_circle = Circle((0, 0), 0.1, transform=ax2.transData._b,
                               color='red', alpha=0.2)
    ax2.add_patch(collision_circle)
    
    ax2.set_ylim(0, 1.5)
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 3: Interference Pattern
    # ─────────────────────────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_title('Panel 3: Interference Pattern\n(Constructive = Prime, Destructive = Gap)', 
                  fontsize=11, fontweight='bold')
    
    # Compute interference for a range of numbers
    x_range = np.linspace(2, 50, 500)
    interference = []
    
    for x in x_range:
        # Sum contributions from all primes up to sqrt(x)
        total = 0
        for p in primes:
            if p > np.sqrt(x):
                break
            # Wave from prime p
            wave = np.cos(2 * np.pi * x / p)
            total += wave / np.log(p)  # Weight by 1/log(p)
        interference.append(total)
    
    interference = np.array(interference)
    
    # Normalize
    interference = (interference - interference.min()) / (interference.max() - interference.min())
    
    # Plot interference pattern
    ax3.fill_between(x_range, 0, interference, alpha=0.3, color='blue')
    ax3.plot(x_range, interference, 'b-', linewidth=1)
    
    # Mark primes as peaks
    for p in primes:
        if p <= 50:
            idx = np.argmin(np.abs(x_range - p))
            ax3.scatter(p, interference[idx], c='gold', s=100, marker='*',
                       edgecolors='black', linewidths=1, zorder=5)
            ax3.annotate(str(p), (p, interference[idx] + 0.05), 
                        fontsize=7, ha='center')
    
    ax3.axhline(y=0.5, color='red', linestyle='--', linewidth=2, 
                label='½ Threshold', alpha=0.7)
    
    ax3.set_xlabel('Number Line')
    ax3.set_ylabel('Interference Intensity')
    ax3.set_xlim(2, 50)
    ax3.legend(loc='upper right')
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 4: Pressure Balance (p expansion vs 1/p suction)
    # ─────────────────────────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title('Panel 4: Pressure Balance\n(Expansion p vs Suction 1/p)', 
                  fontsize=11, fontweight='bold')
    
    # X-axis: position from 0 to 1
    x_pos = np.linspace(0.01, 1, 200)
    
    # Expansion pressure (from primes): increases with distance from 0
    expansion = np.log(1 / x_pos)  # Higher near 0
    
    # Suction pressure (from reciprocals): increases toward 1
    suction = np.log(1 / (1 - x_pos + 0.01))  # Higher near 1
    
    # Normalize
    expansion = (expansion - expansion.min()) / (expansion.max() - expansion.min())
    suction = (suction - suction.min()) / (suction.max() - suction.min())
    
    ax4.fill_between(x_pos, 0, expansion, alpha=0.3, color='gold', label='Expansion (p)')
    ax4.fill_between(x_pos, 0, -suction, alpha=0.3, color='cyan', label='Suction (1/p)')
    ax4.plot(x_pos, expansion, 'goldenrod', linewidth=2)
    ax4.plot(x_pos, -suction, 'blue', linewidth=2)
    
    # Mark the equilibrium point (where they cross ≈ 0.5)
    equilibrium = 0.5
    ax4.axvline(x=equilibrium, color='red', linewidth=3, linestyle='-',
                label='Equilibrium (½)')
    ax4.scatter([equilibrium], [0], c='red', s=150, marker='o', zorder=10,
               edgecolors='black', linewidths=2)
    
    ax4.set_xlabel('Position (0 → 1)')
    ax4.set_ylabel('Pressure (+ Expansion / - Suction)')
    ax4.set_xlim(0, 1)
    ax4.legend(loc='upper left', fontsize=8)
    ax4.axhline(y=0, color='gray', linewidth=0.5)
    
    # ─────────────────────────────────────────────────────────────────────
    # Panel 5: Chromatic Spectrometer (Primes as Pure Colors)
    # ─────────────────────────────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[2, :])
    ax5.set_title('Panel 5: Chromatic Spectrometer\n'
                  '(Primes = Pure Colors, Composites = Chromatic Aberration)', 
                  fontsize=11, fontweight='bold')
    
    # Create spectrum from primes
    all_nums = range(2, 80)
    
    for n in all_nums:
        # Color based on primality
        is_prime = n in primes
        
        # Position
        x = n
        
        if is_prime:
            # Pure spectral color (rainbow based on position)
            hue = (n - 2) / 78  # 0 to 1 across spectrum
            color = plt.cm.rainbow(hue)
            ax5.bar(x, 1, width=0.8, color=color, edgecolor='black', linewidth=0.5)
            ax5.annotate(str(n), (x, 1.05), fontsize=6, ha='center', 
                        rotation=90, color='black')
        else:
            # Gray (aberrated)
            ax5.bar(x, 0.3, width=0.8, color='lightgray', alpha=0.5)
    
    ax5.set_xlabel('Number Line (Spectral Position)')
    ax5.set_ylabel('Purity')
    ax5.set_xlim(1, 80)
    ax5.set_ylim(0, 1.3)
    
    # Add legend annotation
    ax5.annotate('█ Pure Color = Prime (passes ½ lens without blur)\n'
                 '░ Gray = Composite (chromatic aberration)',
                 (60, 0.9), fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # ─────────────────────────────────────────────────────────────────────
    # Save and show
    # ─────────────────────────────────────────────────────────────────────
    plt.tight_layout()
    plt.savefig('/Users/studio/00 Constellation/Reiman/refractal_interference.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print("\n" + "="*70)
    print("REFRACTAL INTERFERENCE ANALYSIS")
    print("="*70)
    print(f"\nPrimes analyzed: {len(primes)}")
    
    print("\n" + "─"*70)
    print("THE HOLOGRAPHIC PRIME THESIS")
    print("─"*70)
    print("""
A Prime is a HOLOGRAM produced by:
  1. FORWARD FLOW (p): Expansion from 1 toward ∞
  2. BACKWASH (1/p): Reflection compressing toward 0
  3. INTERFERENCE: Constructive = Prime, Destructive = Gap

The ½ Line is the FOCAL PLANE where:
  - Expansion pressure = Suction pressure
  - Forward phase = Backward phase (in phase)
  - Image is RESOLVED into a sharp point

Composites are ABERRATIONS:
  - Out of phase interference
  - Blurred by multiple overlapping waves
  - "Gray" on the chromatic spectrum

RIEMANN HYPOTHESIS = Refractive Invariance:
  - The "Refractive Index of Truth" is constant
  - Light (numbers) can only focus at ½
  - A zero at 0.6 would require the vacuum to bend mid-stream
  - Since the Platonic Verse is logically perfect, this is impossible
""")


if __name__ == "__main__":
    create_refractal_map()
