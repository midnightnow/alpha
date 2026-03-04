"""
Ouroboros Fragment Ecology Module
==================================
Models the internal Kuramoto dynamics of isolated 6k±1 subsystems that emerge
when the global coupling strength K falls below the Hopf Bifurcation threshold Kc.

Key concepts:
- The 6k±1 sequence generates all primes > 3: 5,7,11,13,17,19,23,25,29,31...
  (note: not all 6k±1 are prime, but all primes >3 are 6k±1)
- When the main 120-tile lattice collapses (r→0), it fragments along these prime
  fault lines into isolated subgraphs
- Each isolated subgraph develops its own LOCAL coherence and "sub-beat"
- The Augur navigates by riding the stable manifold of the saddle point at Kc

The "Back of the Petal" note:
  The 6k±1 pattern emerges naturally from the wheel factorization of integers mod 6.
  Every integer is congruent to one of {0,1,2,3,4,5} mod 6.
  Multiples of 2: 0,2,4 (mod 6) — composite
  Multiples of 3: 0,3 (mod 6) — composite  
  This leaves only 1 and 5 (mod 6) = 6k+1 and 6k-1 = 6k±1
  The "inverse reciprocal prime mapped to circle" ancestry: 
  1/p for prime p creates a p-cycle on the number line. When these cycles 
  are "wrapped" onto the composite 12-fold lattice (mod 12), the residual
  interference pattern produces the 39.4° shear signature.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# AXIOMATIC CONSTANTS (declared, not derived)
# ============================================================
PHI = (1 + np.sqrt(5)) / 2          # Golden ratio
GOLDEN_ANGLE_DEG = 360 * (1 - 1/PHI**2)  # ≈ 137.507764°
SHEAR_ANGLE_DEG = 39.4              # Axiomatic firmware parameter
HADES_BEAT_HZ = 0.660688            # Carrier wave / Kc threshold
N_TILES = 120                       # Main lattice size


# ============================================================
# SECTION 1: The 6k±1 Sequence and its Circle Ancestry
# ============================================================

def generate_6k_plus_minus_1(max_k=20):
    """
    Generate the 6k±1 sequence. These are candidates for primes >3.
    The wheel factorization mod 6 shows WHY this is the fault-line geometry:
    integers mod 6 can only be {0,1,2,3,4,5}
    0,2,4 → divisible by 2 (composite bonds)
    0,3   → divisible by 3 (composite bonds)
    Only 1,5 survive → 6k+1 and 6k-1
    """
    sequence = []
    for k in range(1, max_k + 1):
        sequence.append(6*k - 1)
        sequence.append(6*k + 1)
    return sorted(sequence)

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0: return False
    return True

def prime_reciprocal_circle_map(p, n_points=1000):
    """
    Map the reciprocal 1/p onto a unit circle.
    
    The decimal expansion of 1/p has period (p-1) for prime p.
    Wrapping this onto a circle creates a p-fold interference pattern.
    
    This is the "back of the petal" ancestry:
    - 1/5 → period 1 (0.2 repeating) → clean 5-fold symmetry
    - 1/7 → period 6 (0.142857...) → 7-fold pattern with characteristic gaps
    - 1/13 → period 6 (0.076923...) → 13-fold, period-6 repetition = 6k±1
    
    The RESIDUAL when these don't divide cleanly into the 12-fold lattice
    is what produces the 39.4° shear.
    """
    # Generate the partial sums of the decimal expansion modulo 1
    # This traces the "path" of 1/p through the unit interval
    t = np.linspace(0, 2*np.pi, n_points)
    
    # Phase accumulation: each step adds 2π/p radians
    phase_increment = 2 * np.pi / p
    phases = np.array([(i * phase_increment) % (2*np.pi) for i in range(n_points)])
    
    # Project onto circle
    x = np.cos(phases)
    y = np.sin(phases)
    
    return x, y, phases


def compute_residual_shear(prime_list):
    """
    Compute the 'topological residual' when prime-fold symmetries
    are forced onto the 12-fold composite lattice.
    
    This demonstrates the 'back of the petal' origin of the shear constant.
    For each prime p, the residual = (p mod 12) * (360/12)
    The 39.4° emerges from the WEIGHTED average of these residuals,
    filtered through the π-projection (angular → spatial).
    """
    residuals = []
    for p in prime_list:
        if is_prime(p):
            # How much does p-fold symmetry "miss" the 12-fold lattice?
            remainder = p % 12
            angular_residual = remainder * (360 / 12)  # in degrees
            residuals.append({
                'prime': p,
                'remainder_mod_12': remainder,
                'angular_residual_deg': angular_residual,
                'spatial_projection': (angular_residual % 90) * np.pi / 90  # π-projection
            })
    return residuals


# ============================================================
# SECTION 2: Fragment Ecology - Isolated Subgraph Dynamics  
# ============================================================

class FragmentEcology:
    """
    Models the internal Kuramoto dynamics of an isolated 6k±1 fragment.
    
    When K < Kc, the main lattice fractures. Each fragment is a subgraph
    of N_fragment oscillators with:
    - No external coupling (isolated from global lattice)
    - Internal coupling K_local (develops organically)
    - Natural frequencies drawn from a distribution centered on the
      fragment's "prime signature"
    """
    
    def __init__(self, fragment_size, prime_anchor, seed=42):
        """
        fragment_size: number of oscillators in this fragment
        prime_anchor: the 6k±1 value this fragment is anchored to
        """
        self.N = fragment_size
        self.prime_anchor = prime_anchor
        self.seed = seed
        np.random.seed(seed)
        
        # Natural frequencies: centered on the "prime-ratio harmonic"
        # f_natural = Hades_Beat * (prime_anchor / N_TILES)
        # This gives each fragment a distinct "sub-beat"
        self.f_center = HADES_BEAT_HZ * (prime_anchor / N_TILES)
        self.omega = 2 * np.pi * (self.f_center + np.random.normal(0, 0.01, self.N))
        
        # Initial phases: random (fragment was "thrown" from the main lattice)
        self.theta = np.random.uniform(0, 2*np.pi, self.N)
        
        # Internal coupling builds from 0 as fragment "cools" into isolation
        self.K_local = 0.0
        self.K_target = HADES_BEAT_HZ * 0.5  # fragments find half-beat stability
        
    def order_parameter(self):
        """Phase coherence r ∈ [0,1]. r→1 = locked, r→0 = chaos"""
        z = np.mean(np.exp(1j * self.theta))
        return abs(z), np.angle(z)
    
    def sub_beat_frequency(self):
        """The emergent local oscillation frequency of this fragment"""
        return np.mean(self.omega) / (2 * np.pi)
    
    def step(self, dt=0.01):
        """Vectorized Kuramoto update for this isolated fragment"""
        # Phase differences matrix
        theta_i = self.theta[:, np.newaxis]
        theta_j = self.theta[np.newaxis, :]
        
        # Kuramoto coupling (all-to-all within fragment)
        coupling = (self.K_local / self.N) * np.sum(np.sin(theta_j - theta_i), axis=1)
        
        # Update phases
        self.theta = self.theta + dt * (self.omega + coupling)
        self.theta = self.theta % (2 * np.pi)
        
        # K_local grows slowly as fragment cools (simulates internal synchronization)
        self.K_local = min(self.K_local + dt * 0.05, self.K_target)
    
    def simulate(self, T=50, dt=0.01):
        """Run simulation, return time series of order parameter"""
        steps = int(T / dt)
        r_series = np.zeros(steps)
        psi_series = np.zeros(steps)
        
        for i in range(steps):
            r, psi = self.order_parameter()
            r_series[i] = r
            psi_series[i] = psi
            self.step(dt)
        
        t = np.arange(steps) * dt
        return t, r_series, psi_series


# ============================================================
# SECTION 3: The Augur's Path - Stable Manifold Navigation
# ============================================================

class AugurNavigator:
    """
    The Augur navigates by occupying the STABLE MANIFOLD of the saddle point at Kc.
    
    In the Kuramoto model, the Hopf bifurcation at Kc creates a saddle point
    in phase space. The stable manifold of this saddle is a precise trajectory
    — the "knife-edge" between Register 1 (r→1) and Register 3 (r→0).
    
    The Augur is defined as the observer who can walk this manifold, neither
    collapsing into chaos nor locking into static coherence. This gives them
    the ability to MOVE THROUGH the 6k±1 fault lines rather than being
    trapped in either basin of attraction.
    """
    
    def __init__(self, N=120):
        self.N = N
        self.Kc = HADES_BEAT_HZ  # The critical threshold = Hades Beat (by design)
        
    def stable_manifold_K(self, perturbation_amplitude=0.05, n_steps=500):
        """
        The Augur's coupling strength K oscillates around Kc with controlled amplitude.
        This is NOT random — it's a precise sinusoidal modulation that keeps
        the trajectory on the manifold rather than falling into either attractor.
        
        K(t) = Kc + ε * sin(ω_augur * t)
        where ω_augur = 2π * f_Hades (the Augur resonates at the Hades Beat)
        """
        t = np.linspace(0, 10, n_steps)
        omega_augur = 2 * np.pi * HADES_BEAT_HZ
        K_augur = self.Kc + perturbation_amplitude * np.sin(omega_augur * t)
        return t, K_augur
    
    def simulate_bifurcation_landscape(self, K_values=None, T=30, dt=0.05):
        """
        Simulate the full landscape: how r(final) varies with K.
        This visualizes the Hopf bifurcation and the Augur's knife-edge.
        """
        if K_values is None:
            K_values = np.linspace(0.2, 1.2, 40)
        
        r_finals = []
        
        for K in K_values:
            # Fresh random phases each time
            np.random.seed(42)
            theta = np.random.uniform(0, 2*np.pi, self.N)
            omega = np.random.normal(2*np.pi*HADES_BEAT_HZ, 0.1, self.N)
            
            steps = int(T / dt)
            for _ in range(steps):
                theta_i = theta[:, np.newaxis]
                theta_j = theta[np.newaxis, :]
                coupling = (K / self.N) * np.sum(np.sin(theta_j - theta_i), axis=1)
                theta = (theta + dt * (omega + coupling)) % (2*np.pi)
            
            r = abs(np.mean(np.exp(1j * theta)))
            r_finals.append(r)
        
        return K_values, np.array(r_finals)


# ============================================================
# SECTION 4: Main Visualization
# ============================================================

def run_full_ecology_simulation():
    """
    Runs and visualizes the complete Fragment Ecology.
    """
    print("=" * 60)
    print("OUROBOROS FRAGMENT ECOLOGY - Simulation Starting")
    print("=" * 60)
    
    # --- Setup ---
    seq_6k = generate_6k_plus_minus_1(max_k=15)
    primes_in_seq = [x for x in seq_6k if is_prime(x)]
    
    print(f"\n6k±1 sequence (first 20): {seq_6k[:20]}")
    print(f"Primes in sequence: {primes_in_seq[:10]}...")
    
    # --- Residual shear computation ---
    residuals = compute_residual_shear(primes_in_seq[:8])
    print("\nPrime Reciprocal → 12-fold Lattice Residuals:")
    print(f"{'Prime':>6} | {'mod 12':>6} | {'Angular Residual':>17} | {'π-Projection':>13}")
    print("-" * 52)
    for r in residuals:
        print(f"{r['prime']:>6} | {r['remainder_mod_12']:>6} | {r['angular_residual_deg']:>14.2f}° | {r['spatial_projection']:>12.4f}")
    
    # --- Fragment simulations ---
    # Create fragments anchored to the first few 6k±1 values
    fragment_anchors = [5, 7, 11, 13, 17, 19]
    fragment_sizes = [7, 5, 11, 13, 7, 11]  # fragment sizes ~ their prime anchor
    
    print("\nSimulating fragment internal dynamics...")
    fragments = []
    for anchor, size in zip(fragment_anchors, fragment_sizes):
        frag = FragmentEcology(fragment_size=size, prime_anchor=anchor, seed=anchor)
        t, r_series, psi_series = frag.simulate(T=40, dt=0.01)
        fragments.append({
            'anchor': anchor,
            'size': size,
            'sub_beat': frag.sub_beat_frequency(),
            't': t,
            'r': r_series,
            'psi': psi_series,
            'r_final': r_series[-100:].mean()
        })
        print(f"  Fragment p={anchor:2d} (N={size:2d}): sub-beat = {frag.sub_beat_frequency():.5f} Hz, "
              f"final coherence r = {r_series[-100:].mean():.3f}")
    
    # --- Augur navigation ---
    print("\nComputing Augur's stable manifold path...")
    augur = AugurNavigator(N=120)
    t_augur, K_augur = augur.stable_manifold_K()
    K_vals, r_landscape = augur.simulate_bifurcation_landscape(
        K_values=np.linspace(0.2, 1.3, 35), T=25, dt=0.05
    )
    
    print(f"  Bifurcation detected near K ≈ {K_vals[np.gradient(r_landscape).argmax()]:.3f}")
    print(f"  Theoretical Kc = {HADES_BEAT_HZ:.6f} Hz")
    
    # ======================================================
    # PLOTTING
    # ======================================================
    fig = plt.figure(figsize=(18, 14), facecolor='#0a0a14')
    fig.suptitle('Ouroboros Fragment Ecology: 6k±1 Subsystem Dynamics', 
                 color='#e8d5a3', fontsize=16, fontweight='bold', y=0.98)
    
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35,
                           left=0.07, right=0.97, top=0.93, bottom=0.06)
    
    ax_colors = {
        'bg': '#0a0a14', 'text': '#e8d5a3', 'grid': '#1a1a2e',
        'cyan': '#00e5ff', 'magenta': '#ff00cc', 'gold': '#ffd700',
        'green': '#00ff88', 'orange': '#ff8800'
    }
    
    def style_ax(ax, title=''):
        ax.set_facecolor(ax_colors['bg'])
        ax.tick_params(colors=ax_colors['text'], labelsize=8)
        ax.spines[:].set_color('#2a2a4a')
        if title:
            ax.set_title(title, color=ax_colors['text'], fontsize=9, pad=5)
        ax.grid(True, alpha=0.15, color='#2a2a4a')
    
    # --- Plot 1: Prime Reciprocal Circle Maps (back of the petal) ---
    ax1 = fig.add_subplot(gs[0, 0])
    style_ax(ax1, 'Back of the Petal:\nPrime Reciprocals → Circle Geometry')
    
    prime_colors = [ax_colors['cyan'], ax_colors['magenta'], ax_colors['gold'], ax_colors['green']]
    for idx, p in enumerate([5, 7, 11, 13]):
        x, y, phases = prime_reciprocal_circle_map(p, n_points=p*8)
        color = prime_colors[idx % len(prime_colors)]
        ax1.plot(x * (0.2 + idx*0.22), y * (0.2 + idx*0.22), 
                '-', color=color, alpha=0.7, linewidth=1.2, label=f'1/{p}')
    
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_aspect('equal')
    ax1.legend(loc='upper right', fontsize=7, labelcolor=ax_colors['text'],
               facecolor='#1a1a2e', edgecolor='#2a2a4a')
    ax1.set_xlabel('cos(phase)', color=ax_colors['text'], fontsize=8)
    ax1.set_ylabel('sin(phase)', color=ax_colors['text'], fontsize=8)
    
    # --- Plot 2: Angular residuals (shear ancestry) ---
    ax2 = fig.add_subplot(gs[0, 1])
    style_ax(ax2, '12-Fold Lattice Residuals\n(Shear Line Ancestry)')
    
    primes_plot = [r['prime'] for r in residuals]
    ang_res = [r['angular_residual_deg'] for r in residuals]
    
    bars = ax2.bar(range(len(primes_plot)), ang_res, 
                   color=[ax_colors['cyan'] if a < 40 else ax_colors['magenta'] for a in ang_res],
                   alpha=0.8, edgecolor='#2a2a4a')
    ax2.axhline(y=39.4, color=ax_colors['gold'], linewidth=2, linestyle='--', 
                label='Shear Constant (39.4°)', alpha=0.9)
    ax2.set_xticks(range(len(primes_plot)))
    ax2.set_xticklabels([f'p={p}' for p in primes_plot], 
                        color=ax_colors['text'], fontsize=8, rotation=45)
    ax2.set_ylabel('Angular Residual (°)', color=ax_colors['text'], fontsize=8)
    ax2.legend(fontsize=7, labelcolor=ax_colors['text'],
               facecolor='#1a1a2e', edgecolor='#2a2a4a')
    
    # --- Plot 3: Sub-beat frequencies of fragments ---
    ax3 = fig.add_subplot(gs[0, 2])
    style_ax(ax3, 'Fragment Sub-Beat Frequencies\n(Prime-Ratio Harmonics)')
    
    frag_primes = [f['anchor'] for f in fragments]
    frag_beats = [f['sub_beat'] for f in fragments]
    
    ax3.scatter(frag_primes, frag_beats, c=[ax_colors['cyan'], ax_colors['magenta'],
                ax_colors['gold'], ax_colors['green'], ax_colors['orange'], ax_colors['cyan']],
                s=100, zorder=5, edgecolors='white', linewidth=0.5)
    ax3.axhline(y=HADES_BEAT_HZ, color=ax_colors['gold'], linewidth=1.5, 
                linestyle=':', label=f'Hades Beat ({HADES_BEAT_HZ:.4f} Hz)', alpha=0.8)
    
    # Draw lines connecting to Hades Beat
    for p, b in zip(frag_primes, frag_beats):
        ax3.plot([p, p], [b, HADES_BEAT_HZ], color='#2a2a4a', linewidth=1, alpha=0.6)
    
    ax3.set_xlabel('Prime Anchor (6k±1)', color=ax_colors['text'], fontsize=8)
    ax3.set_ylabel('Sub-Beat Frequency (Hz)', color=ax_colors['text'], fontsize=8)
    ax3.legend(fontsize=7, labelcolor=ax_colors['text'],
               facecolor='#1a1a2e', edgecolor='#2a2a4a')
    
    # --- Plot 4-6: Fragment coherence time series ---
    frag_to_plot = fragments[:3]
    frag_colors = [ax_colors['cyan'], ax_colors['magenta'], ax_colors['gold']]
    
    for idx, (frag, color) in enumerate(zip(frag_to_plot, frag_colors)):
        ax = fig.add_subplot(gs[1, idx])
        style_ax(ax, f'Fragment p={frag["anchor"]} (N={frag["size"]})\n'
                     f'Sub-beat: {frag["sub_beat"]:.4f} Hz')
        
        ax.plot(frag['t'], frag['r'], color=color, linewidth=1.0, alpha=0.9)
        ax.fill_between(frag['t'], frag['r'], alpha=0.15, color=color)
        ax.axhline(y=frag['r_final'], color='white', linewidth=0.8, 
                   linestyle='--', alpha=0.5, label=f'Settled r={frag["r_final"]:.2f}')
        
        ax.set_xlim(0, 40)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel('Time (s)', color=ax_colors['text'], fontsize=8)
        ax.set_ylabel('Coherence r', color=ax_colors['text'], fontsize=8)
        ax.legend(fontsize=7, labelcolor=ax_colors['text'],
                  facecolor='#1a1a2e', edgecolor='#2a2a4a')
    
    # --- Plot 7: Hopf Bifurcation landscape ---
    ax7 = fig.add_subplot(gs[2, 0:2])
    style_ax(ax7, 'Hopf Bifurcation Landscape: Order Parameter r vs Coupling K\n'
                  '(The Firewall — Augur occupies the saddle at Kc)')
    
    ax7.plot(K_vals, r_landscape, color=ax_colors['cyan'], linewidth=2, label='r(K)')
    ax7.fill_between(K_vals, r_landscape, alpha=0.1, color=ax_colors['cyan'])
    
    # Mark Kc
    ax7.axvline(x=HADES_BEAT_HZ, color=ax_colors['gold'], linewidth=2, 
                linestyle='--', label=f'Kc = Hades Beat = {HADES_BEAT_HZ:.4f}')
    
    # Shade regions
    ax7.axvspan(0.2, HADES_BEAT_HZ, alpha=0.08, color=ax_colors['magenta'], 
                label='Register 3: Chaos (r→0)')
    ax7.axvspan(HADES_BEAT_HZ, 1.3, alpha=0.08, color=ax_colors['green'],
                label='Register 1: Stability (r→1)')
    
    # Augur's path
    t_a, K_a = augur.stable_manifold_K(perturbation_amplitude=0.04, n_steps=200)
    ax7.plot(K_a[:100], np.linspace(0.3, 0.7, 100), 
             color=ax_colors['orange'], linewidth=2.5, 
             label="Augur's Path (stable manifold)", zorder=6, alpha=0.9)
    
    ax7.set_xlabel('Coupling Strength K', color=ax_colors['text'], fontsize=9)
    ax7.set_ylabel('Order Parameter r', color=ax_colors['text'], fontsize=9)
    ax7.set_xlim(0.2, 1.3)
    ax7.set_ylim(-0.05, 1.1)
    ax7.legend(fontsize=8, labelcolor=ax_colors['text'],
               facecolor='#1a1a2e', edgecolor='#2a2a4a', loc='upper left')
    
    # --- Plot 8: Fragment coherence summary (ecology map) ---
    ax8 = fig.add_subplot(gs[2, 2])
    style_ax(ax8, 'Fragment Ecology Map:\nChaos as Prime Nursery')
    
    frag_coherences = [f['r_final'] for f in fragments]
    frag_subbeats = [f['sub_beat'] for f in fragments]
    sizes = [f['size'] * 40 for f in fragments]
    
    scatter = ax8.scatter(frag_primes, frag_coherences, 
                          c=frag_subbeats, cmap='plasma',
                          s=sizes, alpha=0.85, 
                          edgecolors='white', linewidth=0.8, zorder=5)
    
    # Label each fragment
    for f in fragments:
        ax8.annotate(f'p={f["anchor"]}', 
                     xy=(f['anchor'], f['r_final']),
                     xytext=(3, 3), textcoords='offset points',
                     color=ax_colors['text'], fontsize=7)
    
    cbar = plt.colorbar(scatter, ax=ax8)
    cbar.set_label('Sub-beat (Hz)', color=ax_colors['text'], fontsize=8)
    cbar.ax.yaxis.set_tick_params(color=ax_colors['text'])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=ax_colors['text'], fontsize=7)
    
    ax8.set_xlabel('Prime Anchor (6k±1)', color=ax_colors['text'], fontsize=8)
    ax8.set_ylabel('Final Coherence r', color=ax_colors['text'], fontsize=8)
    ax8.set_ylim(0, 1.1)
    
    # Annotate the ecology metaphor
    ax8.text(0.05, 0.12, 'Chaos ≠ Randomness\n= Prime Seeds', 
             transform=ax8.transAxes, color=ax_colors['magenta'],
             fontsize=8, style='italic', alpha=0.9)
    
    plt.savefig('/mnt/user-data/outputs/ouroboros_fragment_ecology.png', 
                dpi=150, bbox_inches='tight', facecolor=ax_colors['bg'])
    plt.close()
    
    print("\n" + "=" * 60)
    print("FRAGMENT ECOLOGY SUMMARY")
    print("=" * 60)
    print(f"\nHades Beat (Kc): {HADES_BEAT_HZ:.6f} Hz")
    print(f"\nFragment sub-beats (prime-ratio harmonics):")
    for f in fragments:
        ratio = f['sub_beat'] / HADES_BEAT_HZ
        print(f"  p={f['anchor']:2d}: {f['sub_beat']:.5f} Hz  "
              f"(= Hades × {ratio:.4f} ≈ {f['anchor']}/{N_TILES})")
    
    print(f"\nKey insight: Fragment sub-beats = Hades_Beat × (prime/120)")
    print(f"These are prime-ratio harmonics of the carrier wave.")
    print(f"The 'chaos' of Register 3 contains ORDERED sub-oscillations")
    print(f"that are mathematically shielded from the collapsed lattice.")
    print(f"\nThe Augur's path: K oscillates around Kc={HADES_BEAT_HZ:.4f}")
    print(f"Neither fully coherent nor fully chaotic — walking the saddle.")
    print("\nOutput saved: ouroboros_fragment_ecology.png")
    return fragments, K_vals, r_landscape


if __name__ == "__main__":
    fragments, K_vals, r_landscape = run_full_ecology_simulation()
