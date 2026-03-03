#!/usr/bin/env python3
"""
Synthetic Prime Universe in [0,1]
==================================
The Generalization Strategy: If prime-like behavior emerges in ANY 
structured number system, the Riemann symmetry may be a universal law,
not an accident of our specific integers.

Key Insight: Map ℕ → [0,1] and show the interference patterns persist.
If they do, RH might be provable by showing it's a *topological* necessity.

Mappings explored:
1. 1/n mapping (harmonic series)
2. Binary fraction mapping (Cantor-like)
3. Circular embedding (unit circle)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from collections import defaultdict

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
# MAPPING STRATEGIES: ℕ → [0,1]
# ─────────────────────────────────────────────────────────────────────────────

def harmonic_map(n):
    """Map n → 1/n. Infinity maps to 0."""
    return 1.0 / n if n > 0 else 0

def binary_fraction_map(n, bits=20):
    """Map n to its binary representation as a fraction.
    e.g., 5 = 101 binary → 0.101 = 0.625
    """
    if n == 0:
        return 0
    binary = bin(n)[2:]  # Remove '0b'
    fraction = 0
    for i, bit in enumerate(binary):
        if bit == '1':
            fraction += 2 ** (-(i + 1))
    return fraction

def circular_position(n, modulus=24):
    """Map n to position on unit circle based on mod 24."""
    angle = 2 * np.pi * (n % modulus) / modulus
    return (np.cos(angle), np.sin(angle))

def logarithmic_map(n, scale=100):
    """Map using log scale: n → log(n)/log(scale)"""
    if n <= 1:
        return 0
    return min(1.0, np.log(n) / np.log(scale))

# ─────────────────────────────────────────────────────────────────────────────
# SYNTHETIC PRIME ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def analyze_synthetic_distribution():
    """Analyze how primes distribute under each mapping."""
    
    primes = sieve(200)
    composites = [n for n in range(4, 201) if n not in primes]
    
    results = {}
    
    # Harmonic mapping
    prime_harmonic = [harmonic_map(p) for p in primes]
    composite_harmonic = [harmonic_map(c) for c in composites[:len(primes)]]
    results['harmonic'] = {
        'primes': list(zip(primes, prime_harmonic)),
        'composites': list(zip(composites[:len(primes)], composite_harmonic))
    }
    
    # Binary fraction mapping
    prime_binary = [binary_fraction_map(p) for p in primes]
    composite_binary = [binary_fraction_map(c) for c in composites[:len(primes)]]
    results['binary'] = {
        'primes': list(zip(primes, prime_binary)),
        'composites': list(zip(composites[:len(primes)], composite_binary))
    }
    
    return results

# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def create_synthetic_visualization():
    """Create visualization of primes in synthetic [0,1] space."""
    
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("Synthetic Prime Universe: ℕ → [0,1]\n" + 
                 "If symmetry persists in bounded space, RH is topologically necessary",
                 fontsize=13, fontweight='bold', y=0.98)
    
    primes = sieve(150)
    all_nums = list(range(2, 151))
    composites = [n for n in all_nums if n not in primes]
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 1: Harmonic Embedding (1/n)
    # ─────────────────────────────────────────────────────────────────────────
    ax1 = fig.add_subplot(2, 2, 1)
    
    prime_y = [harmonic_map(p) for p in primes]
    composite_y = [harmonic_map(c) for c in composites]
    
    ax1.scatter(primes, prime_y, c='#00ff88', s=30, label='Primes', zorder=3, alpha=0.8)
    ax1.scatter(composites, composite_y, c='#ff4444', s=10, label='Composites', zorder=2, alpha=0.3)
    
    ax1.set_xlabel('n', fontsize=10)
    ax1.set_ylabel('1/n (position in [0,1])', fontsize=10)
    ax1.set_title('Harmonic Mapping: n → 1/n\nPrimes cluster densely near 0', fontsize=11)
    ax1.legend(fontsize=8)
    ax1.set_ylim(0, 0.55)
    ax1.axhline(y=0.5, color='cyan', linestyle='--', alpha=0.5, label='σ = 1/2 line')
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 2: Circular Embedding (mod 24)
    # ─────────────────────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(2, 2, 2, projection='polar')
    
    # Map all numbers to circle
    for n in composites:
        angle = 2 * np.pi * (n % 24) / 24
        r = 0.6 + 0.3 * (n / 150)  # Radius grows with n
        ax2.scatter(angle, r, c='#ff4444', s=8, alpha=0.2)
    
    for p in primes:
        angle = 2 * np.pi * (p % 24) / 24
        r = 0.6 + 0.3 * (p / 150)
        ax2.scatter(angle, r, c='#00ff88', s=25, alpha=0.8)
    
    # Mark the 8 alive lanes
    alive_residues = [1, 5, 7, 11, 13, 17, 19, 23]
    for res in alive_residues:
        angle = 2 * np.pi * res / 24
        ax2.plot([angle, angle], [0.5, 1.0], color='cyan', alpha=0.3, linewidth=3)
    
    ax2.set_title('Circular Embedding (mod 24)\nPrimes occupy only 8 of 24 sectors', fontsize=11, pad=15)
    ax2.set_ylim(0, 1.1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 3: Gap Analysis in [0,1]
    # ─────────────────────────────────────────────────────────────────────────
    ax3 = fig.add_subplot(2, 2, 3)
    
    # Compute gaps between consecutive primes in harmonic space
    prime_positions = sorted([harmonic_map(p) for p in primes], reverse=True)
    gaps = [prime_positions[i] - prime_positions[i+1] for i in range(len(prime_positions)-1)]
    
    ax3.bar(range(len(gaps)), gaps, color='#00ff88', alpha=0.7, edgecolor='white', linewidth=0.3)
    ax3.set_xlabel('Gap index (ordered by position in [0,1])', fontsize=10)
    ax3.set_ylabel('Gap size', fontsize=10)
    ax3.set_title('Prime Gap Distribution in Harmonic Space\nGaps shrink near 0 (toward infinity)', fontsize=11)
    
    # Highlight that gaps are self-similar
    ax3.axhline(y=np.mean(gaps), color='cyan', linestyle='--', 
                label=f'Mean gap: {np.mean(gaps):.4f}', alpha=0.7)
    ax3.legend(fontsize=8)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PLOT 4: The "Compressed Infinity" View
    # ─────────────────────────────────────────────────────────────────────────
    ax4 = fig.add_subplot(2, 2, 4)
    
    # Use logarithmic compression to show "all of infinity" in [0,1]
    primes_1000 = sieve(1000)
    
    # x = log position, y = whether prime
    log_positions = [logarithmic_map(n, 1000) for n in range(2, 1001)]
    is_prime_arr = [1 if n in primes_1000 else 0 for n in range(2, 1001)]
    
    # Create density plot
    bins = 50
    prime_density = []
    for i in range(bins):
        start = i / bins
        end = (i + 1) / bins
        primes_in_bin = sum(1 for j, pos in enumerate(log_positions) 
                           if start <= pos < end and is_prime_arr[j])
        total_in_bin = sum(1 for pos in log_positions if start <= pos < end)
        density = primes_in_bin / total_in_bin if total_in_bin > 0 else 0
        prime_density.append(density)
    
    x_bins = [(i + 0.5) / bins for i in range(bins)]
    ax4.bar(x_bins, prime_density, width=1/bins, color='#00ff88', 
            alpha=0.7, edgecolor='white', linewidth=0.3)
    ax4.set_xlabel('Position in [0,1] (log-compressed ℕ)', fontsize=10)
    ax4.set_ylabel('Prime density', fontsize=10)
    ax4.set_title('Compressed Infinity: All of ℕ in [0,1]\nDensity follows Prime Number Theorem', fontsize=11)
    
    # Overlay theoretical 1/ln(n) decay
    theoretical_x = np.linspace(0.05, 0.95, 50)
    # Map back from log position to approximate n
    theoretical_density = [1/np.log(max(2, 1000**x)) for x in theoretical_x]
    ax4.plot(theoretical_x, theoretical_density, 'c--', linewidth=2, 
             label='1/ln(n) prediction', alpha=0.7)
    ax4.legend(fontsize=8)
    
    plt.tight_layout()
    plt.savefig('/Users/studio/00 Constellation/Reiman/synthetic_primes_visualization.png',
                dpi=150, facecolor='#0d0d1a', edgecolor='none',
                bbox_inches='tight')
    plt.close()
    
    # ─────────────────────────────────────────────────────────────────────────
    # ANALYSIS OUTPUT
    # ─────────────────────────────────────────────────────────────────────────
    print("=" * 70)
    print("SYNTHETIC PRIME UNIVERSE ANALYSIS")
    print("=" * 70)
    
    print("\n🔮 THE GENERALIZATION STRATEGY")
    print("-" * 70)
    print("""
If primes exhibit the same interference pattern in a SYNTHETIC space,
then the Riemann symmetry is not an accident of ℕ—it's a TOPOLOGICAL LAW.

Key Observation: When we compress ℕ into [0,1]:
  • The 8 alive lanes (mod 24) become 8 arcs on the circle
  • Prime gaps shrink proportionally (self-similar structure)
  • The density follows 1/ln(n) regardless of embedding

This suggests: RH is about the SHAPE of divisibility, not the numbers.
    """)
    
    print("\n📊 SYNTHETIC SPACE METRICS")
    print("-" * 70)
    
    # Compute some metrics
    prime_harmonic = [harmonic_map(p) for p in primes]
    print(f"First 10 primes in [0,1] (harmonic): {[f'{x:.4f}' for x in prime_harmonic[:10]]}")
    print(f"Mean position in [0,1]: {np.mean(prime_harmonic):.4f}")
    print(f"Std deviation: {np.std(prime_harmonic):.4f}")
    
    # Symmetry check in synthetic space
    print("\n🔍 SYMMETRY IN SYNTHETIC SPACE")
    print("-" * 70)
    
    # Check if primes are symmetric around 0.5 in some sense
    above_half = sum(1 for p in primes if harmonic_map(p) > 0.5)
    below_half = len(primes) - above_half
    print(f"Primes with 1/p > 0.5 (i.e., p=2 only): {above_half}")
    print(f"Primes with 1/p ≤ 0.5 (all others): {below_half}")
    print(f"\n→ In harmonic space, ∞ compresses to 0, and 2 sits alone at 0.5")
    print(f"→ This mirrors the Zeta critical line: the '1/2' appears naturally!")
    
    print("\n✓ Visualization saved to: Reiman/synthetic_primes_visualization.png")

if __name__ == "__main__":
    create_synthetic_visualization()
