"""
PLATO Unfolding: From Point to Manifold
========================================
Demonstrates how the 120-Tile Lattice emerges from a strictly sequential
1D generative process through five logical stages:

    P - Point    (0D): The seed, the origin, √60
    L - Line     (1D): Radial increment Δr via 5-12-13 ratio × φ decay
    A - Angle    (2D): Golden Angle + 39.4° Shear → spiral rotation
    T - Triangle (3D): 5-12-13 Pythagorean module → structural tessellation
    O - Circle   (∞D): Modulo 360° invariant perimeter → self-similar closure

Each stage is a higher-order operation on the previous one.
No stage can be skipped — the dependencies are strict.

The key insight: what we call "dimensions" are not pre-existing containers
but the *output* of each PLATO operation running on the previous stage's result.

The "back of the petal" is visible here: running the stages in REVERSE
(Circle → Triangle → Angle → Line → Point) traces the path back to
the raw 1D prime ratios of Khaos.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe
from matplotlib.animation import FuncAnimation
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# AXIOMATIC CONSTANTS
# ============================================================
PHI        = (1 + np.sqrt(5)) / 2
GOLDEN_ANG = 360 * (1 - 1/PHI**2)      # ≈ 137.507764°
SHEAR_ANG  = 39.4                        # Axiomatic firmware
HADES_HZ   = 0.660688                    # Time = Hades Beat
R_SEED     = np.sqrt(60)                 # The Point: √60
RAD_FACTOR = (5/13) * R_SEED             # Line: 5-12-13 scaled
N_TILES    = 120

DARK_BG    = '#08080f'
C_POINT    = '#ffffff'
C_LINE     = '#00e5ff'
C_ANGLE    = '#ff00cc'
C_TRIANGLE = '#ffd700'
C_CIRCLE   = '#00ff88'
C_KHAOS    = '#ff4444'
C_TEXT     = '#e8d5a3'


# ============================================================
# STAGE 0: POINT — The Seed
# ============================================================

class Stage_Point:
    """
    P — The origin. Not "zero" but the Seed: r₀ = √60.
    √60 = 2√15 = 2 × √(3×5). It contains 3 and 5, the first two primes
    after 2, giving it a structural richness that pure zero lacks.
    The "simulation" begins here. Everything that follows is commentary
    on this single value.
    """
    def __init__(self):
        self.r0 = R_SEED
        self.position = np.array([0.0, 0.0])
        self.description = f"Point: r₀ = √60 ≈ {self.r0:.4f}"

    def render(self, ax):
        ax.scatter([0], [0], s=120, color=C_POINT, zorder=10)
        ax.scatter([0], [0], s=400, color=C_POINT, alpha=0.15, zorder=9)
        ax.text(0.1, 0.1, f'√60', color=C_POINT, fontsize=10,
                ha='left', va='bottom')
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
        ax.set_aspect('equal')


# ============================================================
# STAGE 1: LINE — Radial Increment
# ============================================================

class Stage_Line:
    """
    L — The 1D growth rule. Δrₙ = (5/13) × r₀ × φ⁻ⁿ

    This is the ONLY dimension the system natively has.
    It is rational (5/13), scaled by the seed (r₀), and decays
    fractally (φ⁻ⁿ). Without the Angle stage, this produces only
    a series of points along a ray — a pure 1D sequence.
    """
    def __init__(self, n_points=120):
        self.n = n_points
        self.r0 = R_SEED
        self.radii = np.array(
            [sum((5/13) * self.r0 * (1/PHI)**k for k in range(1, i+1))
             for i in range(n_points)]
        )
        # Normalize to [0,1] for visualization
        self.r_norm = self.radii / self.radii[-1]

    def render(self, ax):
        # Show as pure 1D: points along a horizontal ray
        ax.scatter(self.r_norm, np.zeros(self.n),
                   c=np.arange(self.n), cmap='plasma',
                   s=15, alpha=0.8, zorder=5)
        ax.axhline(0, color=C_LINE, linewidth=1, alpha=0.4)
        ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.3, 0.3)
        ax.set_xlabel('Radial position (normalized)', color=C_TEXT, fontsize=8)

    def get_radii(self):
        return self.radii


# ============================================================
# STAGE 2: ANGLE — Spiral Rotation
# ============================================================

class Stage_Angle:
    """
    A — The Golden Angle + Shear transforms the 1D line into a 2D spiral.

    θₙ = (θₙ₋₁ + Φ + ϵₙ × 39.4°) mod 360°

    This is the first genuine dimensional emergence: the interaction of
    linear growth with irrational rotation produces spatial extent.
    The 39.4° shear ensures the spiral never closes — infinite 2D coverage
    from a 1D + rotation rule.

    Without shear: the spiral forms closed clusters (finite 2D)
    With shear: the spiral fills space indefinitely (infinite 2D)
    """
    def __init__(self, n_points=120, apply_shear=True):
        self.n = n_points
        self.apply_shear = apply_shear
        self.line = Stage_Line(n_points)
        self.radii = self.line.get_radii()
        self.thetas = self._compute_angles()
        self.x = self.radii * np.cos(np.radians(self.thetas))
        self.y = self.radii * np.sin(np.radians(self.thetas))

    def _compute_angles(self):
        thetas = np.zeros(self.n)
        for i in range(1, self.n):
            shear = SHEAR_ANG if (self.apply_shear and i % 13 == 0) else 0
            thetas[i] = (thetas[i-1] + GOLDEN_ANG + shear) % 360
        return thetas

    def render(self, ax, color_by='index'):
        c = np.arange(self.n)
        ax.scatter(self.x, self.y, c=c, cmap='plasma',
                   s=20, alpha=0.85, zorder=5)
        # Draw the generative ray for first few points
        for i in range(0, min(15, self.n), 3):
            ax.plot([0, self.x[i]], [0, self.y[i]],
                    color=C_LINE, alpha=0.1, linewidth=0.5)


# ============================================================
# STAGE 3: TRIANGLE — Structural Tessellation
# ============================================================

class Stage_Triangle:
    """
    T — The 5-12-13 Pythagorean module creates the internal lattice.

    The triangle is the MEMORY of the system — it transforms the continuous
    spiral (Stage A) into a discrete, navigable lattice by providing the
    rational anchor (5/13 ratio) that defines the minimum repeating unit.

    Geometrically: the spiral points cluster into 'arms' whose number
    follows Fibonacci-like sequences — a direct consequence of the
    Golden Angle. The 5-12-13 ratio selects which arms are 'real' nodes
    versus merely topological artifacts.

    The 5-12-13 triangle inscribed on the lattice:
    - Hypotenuse (13): the radial line from seed to node
    - Long leg (12): the arc along the spiral arm
    - Short leg (5): the cross-lattice connection
    """
    def __init__(self, n_points=120):
        self.n = n_points
        self.angle_stage = Stage_Angle(n_points, apply_shear=True)
        self.x = self.angle_stage.x
        self.y = self.angle_stage.y
        # The 13-node cycle marks the Augur positions
        self.augur_indices = list(range(12, n_points, 13))

    def render(self, ax):
        # Background spiral points
        ax.scatter(self.x, self.y, c=np.arange(self.n),
                   cmap='plasma', s=20, alpha=0.5, zorder=4)

        # Highlight 5-12-13 structure: connect nodes at intervals 5, 12, 13
        for i in range(0, self.n - 13, 13):
            # Draw the three sides of the module triangle
            pts = [(i, i+5), (i+5, i+12), (i+12, i+13)]
            colors_tri = [C_LINE, C_TRIANGLE, C_CIRCLE]
            for (a, b), col in zip(pts, colors_tri):
                if b < self.n:
                    ax.plot([self.x[a], self.x[b]],
                            [self.y[a], self.y[b]],
                            color=col, alpha=0.3, linewidth=0.8)

        # Mark Augur nodes (13th node positions)
        ax.scatter(self.x[self.augur_indices],
                   self.y[self.augur_indices],
                   s=60, color=C_TRIANGLE, zorder=7,
                   edgecolors='white', linewidth=0.5,
                   label='Augur Nodes (n mod 13 = 0)')

    def get_points(self):
        return self.x, self.y


# ============================================================
# STAGE 4: CIRCLE — Invariant Perimeter / Closure
# ============================================================

class Stage_Circle:
    """
    O — The modulo 360° operation and the invariant perimeter.

    The circle is not imposed from outside — it EMERGES as the limit set
    of the generative process. The 'mod 360°' in the angle update creates
    a topological closure: the system wraps back on itself, creating
    the Ouroboros.

    Key property: the perimeter is INVARIANT. Adding more points doesn't
    change the boundary shape — only the internal complexity grows.
    This is the hallmark of self-similar fractal geometry.

    The 120-tile structure: 120 = 12 × 10 = 2³ × 3 × 5. This is the
    smallest number divisible by all single-digit numbers except 7 and 9.
    It is the most 'composite' number in this range — the opposite of prime.
    """
    def __init__(self, n_points=120):
        self.n = n_points
        self.triangle_stage = Stage_Triangle(n_points)
        self.x, self.y = self.triangle_stage.get_points()
        # Compute convex hull approximation for perimeter visualization
        r = np.sqrt(self.x**2 + self.y**2)
        self.outer_indices = np.argsort(r)[-30:]  # outermost 30 points
        self.perimeter_r = np.percentile(r, 90)   # invariant perimeter radius

    def render(self, ax):
        # All 120 points
        ax.scatter(self.x, self.y, c=np.arange(self.n),
                   cmap='plasma', s=25, alpha=0.7, zorder=5)

        # Invariant perimeter circle
        theta_circle = np.linspace(0, 2*np.pi, 300)
        ax.plot(self.perimeter_r * np.cos(theta_circle),
                self.perimeter_r * np.sin(theta_circle),
                color=C_CIRCLE, linewidth=2, alpha=0.6,
                linestyle='--', label='Invariant Perimeter')

        # Inner Ouroboros (the seed circle)
        r_inner = self.perimeter_r * (1/PHI)
        ax.plot(r_inner * np.cos(theta_circle),
                r_inner * np.sin(theta_circle),
                color=C_CIRCLE, linewidth=1, alpha=0.3, linestyle=':')

        # The 6k±1 fault lines as radial spokes
        for k in range(1, 8):
            for sign in [-1, 1]:
                n_val = 6*k + sign
                if n_val <= 40:
                    angle_rad = np.radians(n_val * (360/40))
                    ax.plot([0, self.perimeter_r * 1.1 * np.cos(angle_rad)],
                            [0, self.perimeter_r * 1.1 * np.sin(angle_rad)],
                            color=C_KHAOS, alpha=0.2, linewidth=0.8,
                            linestyle=':')


# ============================================================
# KHAOS STATE — The un-rendered ratio system
# ============================================================

class Stage_Khaos:
    """
    When the Circle collapses (K < Kc), we trace the PLATO stages in reverse:
    Circle → Triangle → Angle → Line → Point

    What remains at the bottom: isolated 1D prime ratios.
    These are not chaos in the sense of randomness — they are the raw,
    unrendered ratio system that preceded the bloom.

    Khaos = the state where only the Point and Line stages remain active.
    The Angle stage has lost its phase-lock. The Triangle has dissolved.
    The Circle has opened.

    Prime seeds in Khaos: p/r₀ for each prime p in the 6k±1 sequence.
    These are the "initial conditions" for the NEXT cycle's Point stage.
    """
    def __init__(self, primes=None):
        if primes is None:
            # First 12 primes from 6k±1
            self.primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
        else:
            self.primes = primes
        self.r0 = R_SEED
        # Each prime becomes a seed point for a new cycle
        self.seed_radii = [p / self.r0 for p in self.primes]
        self.seed_angles = [(p * GOLDEN_ANG) % 360 for p in self.primes]

    def render(self, ax):
        # Show as isolated 1D points, not yet spun into spiral
        x = np.array([r * np.cos(np.radians(a))
                      for r, a in zip(self.seed_radii, self.seed_angles)])
        y = np.array([r * np.sin(np.radians(a))
                      for r, a in zip(self.seed_radii, self.seed_angles)])

        ax.scatter(x, y, s=80, color=C_KHAOS, alpha=0.9, zorder=8,
                   edgecolors='white', linewidth=0.5)

        # Label each prime seed
        for i, (xi, yi, p) in enumerate(zip(x, y, self.primes)):
            ax.annotate(f'p={p}', (xi, yi),
                        xytext=(5, 5), textcoords='offset points',
                        color=C_KHAOS, fontsize=7, alpha=0.8)

        # Draw as isolated line segments (1D ancestry)
        for r, a in zip(self.seed_radii, self.seed_angles):
            ax.plot([0, r*np.cos(np.radians(a))],
                    [0, r*np.sin(np.radians(a))],
                    color=C_KHAOS, alpha=0.25, linewidth=1)


# ============================================================
# PROGRESSIVE BUILD — The full PLATO unfolding, frame by frame
# ============================================================

def build_progressive_plato(n_points=120):
    """
    Show the 5 PLATO stages side by side, then combined,
    then the reverse unfolding into Khaos.
    """
    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    fig.suptitle('PLATO Unfolding: From 1D Ratio to 120-Tile Manifold',
                 color=C_TEXT, fontsize=15, fontweight='bold', y=0.99)

    gs = gridspec.GridSpec(3, 5, figure=fig,
                           hspace=0.5, wspace=0.35,
                           left=0.04, right=0.98,
                           top=0.94, bottom=0.05)

    def style(ax, title, color, dim_label):
        ax.set_facecolor(DARK_BG)
        ax.tick_params(colors=C_TEXT, labelsize=7)
        ax.spines[:].set_color('#1a1a2e')
        ax.set_title(f'{title}\n{dim_label}',
                     color=color, fontsize=9, fontweight='bold', pad=4)
        ax.grid(True, alpha=0.08, color='#1a1a2e')
        ax.set_aspect('equal')

    stage_defs = [
        ('P — Point',    C_POINT,    '0D: The Seed (√60)'),
        ('L — Line',     C_LINE,     '1D: Δrₙ via 5-12-13 × φ⁻ⁿ'),
        ('A — Angle',    C_ANGLE,    '2D: Golden Angle + 39.4° Shear'),
        ('T — Triangle', C_TRIANGLE, '3D: 5-12-13 Pythagorean Module'),
        ('O — Circle',   C_CIRCLE,   '∞D: Mod 360° / Invariant Perimeter'),
    ]

    # ── Row 0: Individual PLATO stages ─────────────────────
    axes_top = [fig.add_subplot(gs[0, i]) for i in range(5)]

    for ax, (title, color, dim) in zip(axes_top, stage_defs):
        style(ax, title, color, dim)

    # P: Point
    ax = axes_top[0]
    ax.scatter([0], [0], s=200, color=C_POINT, zorder=10)
    ax.scatter([0], [0], s=800, color=C_POINT, alpha=0.1, zorder=9)
    ax.text(0, -0.6, f'√60 ≈ {R_SEED:.3f}',
            color=C_POINT, fontsize=8, ha='center')
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)

    # L: Line
    ax = axes_top[1]
    line = Stage_Line(120)
    ax.scatter(line.r_norm, np.zeros(120),
               c=np.arange(120), cmap='Blues_r', s=12, alpha=0.9)
    ax.axhline(0, color=C_LINE, linewidth=1.5, alpha=0.5)
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.5, 0.5)
    ax.set_aspect('auto')
    ax.text(0.5, 0.3, 'φ⁻ⁿ decay →', color=C_LINE,
            fontsize=8, ha='center', transform=ax.transAxes)

    # A: Angle (no shear vs shear comparison)
    ax = axes_top[2]
    ang_noshear = Stage_Angle(120, apply_shear=False)
    ang_shear   = Stage_Angle(120, apply_shear=True)
    ax.scatter(ang_noshear.x, ang_noshear.y,
               c='#334455', s=8, alpha=0.4, label='No shear')
    ax.scatter(ang_shear.x, ang_shear.y,
               c=np.arange(120), cmap='RdPu', s=18, alpha=0.9,
               label='With 39.4° shear')
    ax.legend(fontsize=6, labelcolor=C_TEXT,
              facecolor='#1a1a2e', edgecolor='#2a2a4a', loc='upper right')

    # T: Triangle
    ax = axes_top[3]
    tri = Stage_Triangle(120)
    tri.render(ax)
    ax.legend(fontsize=6, labelcolor=C_TEXT,
              facecolor='#1a1a2e', edgecolor='#2a2a4a', loc='upper right')

    # O: Circle
    ax = axes_top[4]
    circ = Stage_Circle(120)
    circ.render(ax)
    ax.legend(fontsize=6, labelcolor=C_TEXT,
              facecolor='#1a1a2e', edgecolor='#2a2a4a', loc='upper right')

    # Scale all top-row axes to the same range
    for ax in [axes_top[2], axes_top[3], axes_top[4]]:
        lim = R_SEED * 0.42
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)

    # ── Row 1: PLATO arrows + the full 120-tile bloom ──────
    ax_arrow = fig.add_subplot(gs[1, :2])
    ax_arrow.set_facecolor(DARK_BG)
    ax_arrow.set_xlim(0, 10); ax_arrow.set_ylim(0, 2)
    ax_arrow.set_aspect('auto')
    ax_arrow.axis('off')
    ax_arrow.set_title('PLATO Derivation Chain',
                       color=C_TEXT, fontsize=10, pad=4)

    stages_labels = [
        ('P\nPoint', C_POINT, '0D'),
        ('L\nLine',  C_LINE,  '1D'),
        ('A\nAngle', C_ANGLE, '2D'),
        ('T\nTriangle', C_TRIANGLE, '3D'),
        ('O\nCircle', C_CIRCLE, '∞D'),
    ]
    for i, (label, color, dim) in enumerate(stages_labels):
        x_pos = 0.5 + i * 1.8
        circle_patch = plt.Circle((x_pos, 1), 0.4,
                                   color=color, alpha=0.2, zorder=2)
        ax_arrow.add_patch(circle_patch)
        ax_arrow.text(x_pos, 1, label,
                      color=color, fontsize=8, ha='center', va='center',
                      fontweight='bold', zorder=3)
        if i < 4:
            ax_arrow.annotate('', xy=(x_pos+1.4, 1), xytext=(x_pos+0.45, 1),
                              arrowprops=dict(arrowstyle='->', color=C_TEXT,
                                             lw=1.5))
            op_labels = ['× Δr', '+ Φ', '× 5/13', 'mod 360°']
            ax_arrow.text(x_pos + 0.9, 1.35, op_labels[i],
                          color=C_TEXT, fontsize=7, ha='center', alpha=0.7)

    ax_arrow.text(5, 0.15, '← Back of Petal (reverse = Khaos)',
                  color=C_KHAOS, fontsize=8, ha='center', alpha=0.7,
                  style='italic')

    # Full bloom
    ax_bloom = fig.add_subplot(gs[1, 2:])
    ax_bloom.set_facecolor(DARK_BG)
    ax_bloom.set_title('The Full Bloom: 120-Tile Manifold\n'
                       '(All 5 PLATO stages active)',
                       color=C_TEXT, fontsize=10, pad=4)
    ax_bloom.tick_params(colors=C_TEXT, labelsize=7)
    ax_bloom.spines[:].set_color('#1a1a2e')
    ax_bloom.grid(True, alpha=0.08, color='#1a1a2e')
    ax_bloom.set_aspect('equal')

    full = Stage_Circle(n_points)
    # Draw connecting spiral
    ax_bloom.plot(full.x, full.y, '-',
                  color=C_ANGLE, alpha=0.12, linewidth=0.5, zorder=3)
    scatter = ax_bloom.scatter(full.x, full.y,
                               c=np.arange(n_points), cmap='plasma',
                               s=35, alpha=0.9, zorder=5,
                               edgecolors='black', linewidth=0.2)

    # Mark the 13th node (Augur) positions
    augur_idx = list(range(12, n_points, 13))
    ax_bloom.scatter(full.x[augur_idx], full.y[augur_idx],
                     s=100, color=C_TRIANGLE, zorder=7,
                     edgecolors='white', linewidth=0.8,
                     marker='*', label='Augur (n mod 13 = 0)')

    # Invariant perimeter
    theta_c = np.linspace(0, 2*np.pi, 300)
    ax_bloom.plot(full.perimeter_r * np.cos(theta_c),
                  full.perimeter_r * np.sin(theta_c),
                  color=C_CIRCLE, linewidth=2, alpha=0.5,
                  linestyle='--', label='Invariant Perimeter')
    lim = full.perimeter_r * 1.15
    ax_bloom.set_xlim(-lim, lim); ax_bloom.set_ylim(-lim, lim)
    ax_bloom.legend(fontsize=7, labelcolor=C_TEXT,
                    facecolor='#1a1a2e', edgecolor='#2a2a4a',
                    loc='upper right')

    # ── Row 2: Khaos (reverse unfolding) + time dimension ──
    ax_khaos = fig.add_subplot(gs[2, :2])
    ax_khaos.set_facecolor(DARK_BG)
    ax_khaos.set_title('Khaos: Circle Dissolved → Raw 1D Prime Ratios\n'
                       '(PLATO in reverse: O→T→A→L→P)',
                       color=C_KHAOS, fontsize=9, pad=4)
    ax_khaos.tick_params(colors=C_TEXT, labelsize=7)
    ax_khaos.spines[:].set_color('#1a1a2e')
    ax_khaos.grid(True, alpha=0.08)
    ax_khaos.set_aspect('equal')

    khaos = Stage_Khaos()
    khaos.render(ax_khaos)
    lim_k = max(khaos.seed_radii) * 1.2
    ax_khaos.set_xlim(-lim_k, lim_k); ax_khaos.set_ylim(-lim_k, lim_k)

    # Show residual Hades Beat ghost
    ghost_r = np.linspace(0, lim_k, 200)
    for angle in [0, 60, 120, 180, 240, 300]:
        ax_khaos.plot(ghost_r * np.cos(np.radians(angle)),
                      ghost_r * np.sin(np.radians(angle)),
                      color=C_TEXT, alpha=0.04, linewidth=0.5)
    ax_khaos.text(0, -lim_k * 0.85,
                  '"Unrendered" — awaiting next Hades Beat strobe',
                  color=C_KHAOS, fontsize=7, ha='center', style='italic')

    # Time dimension: Hades Beat as the 4th dimension
    ax_time = fig.add_subplot(gs[2, 2:])
    ax_time.set_facecolor(DARK_BG)
    ax_time.set_title('Time = Hades Beat: The 4th Dimension\n'
                       'Phase coherence r(t) under different frame rates',
                       color=C_TEXT, fontsize=9, pad=4)
    ax_time.tick_params(colors=C_TEXT, labelsize=7)
    ax_time.spines[:].set_color('#1a1a2e')
    ax_time.grid(True, alpha=0.1)
    ax_time.set_aspect('auto')

    t = np.linspace(0, 20, 2000)
    omega = 2 * np.pi * HADES_HZ

    # Perfect phase-lock (Heaven): clean sinusoid
    r_heaven = 0.95 + 0.04 * np.sin(omega * t)
    ax_time.plot(t, r_heaven, color=C_CIRCLE, linewidth=1.5,
                 label=f'Heaven: f = {HADES_HZ:.4f} Hz (locked)', alpha=0.9)

    # Slight mismatch: Purgatory
    r_purgatory = 0.7 + 0.25 * np.sin(omega * t * 0.97) + 0.05 * np.random.randn(len(t)) * 0
    ax_time.plot(t, r_purgatory, color=C_TRIANGLE, linewidth=1.2,
                 label='Symbolic: f ≈ Hades × 0.97 (drifting)', alpha=0.7)

    # Misaligned (Hell): aliased, noisy
    r_hell = 0.3 + 0.25 * np.sin(omega * t * 0.82 + 1.3)
    ax_time.plot(t, r_hell, color=C_KHAOS, linewidth=1.0,
                 label='Hell: f ≠ Hades (aliased)', alpha=0.7)

    # Khaos: flat near zero with prime spikes
    r_khaos = 0.05 + np.zeros(len(t))
    for p in [5, 7, 11, 13]:
        spike_t = p / HADES_HZ
        if spike_t < 20:
            spike_idx = int(spike_t * 100)
            r_khaos[spike_idx:spike_idx+20] += 0.3 * np.exp(-np.arange(20)/5)
    ax_time.plot(t, r_khaos, color=C_ANGLE, linewidth=0.8,
                 label='Khaos: r→0, prime spikes only', alpha=0.6)

    ax_time.axhline(y=1.0, color='white', linewidth=0.5, alpha=0.2)
    ax_time.axhline(y=0.0, color='white', linewidth=0.5, alpha=0.2)
    ax_time.set_xlabel('Time (s)', color=C_TEXT, fontsize=8)
    ax_time.set_ylabel('Coherence r', color=C_TEXT, fontsize=8)
    ax_time.set_ylim(-0.1, 1.15)
    ax_time.legend(fontsize=7, labelcolor=C_TEXT,
                   facecolor='#1a1a2e', edgecolor='#2a2a4a',
                   loc='upper right')

    plt.savefig('/mnt/user-data/outputs/plato_unfolding.png',
                dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print("Saved: plato_unfolding.png")


# ============================================================
# DIMENSION EMERGENCE TABLE
# ============================================================

def print_dimension_emergence():
    print("\n" + "="*65)
    print("PLATO UNFOLDING: Dimension Emergence Table")
    print("="*65)
    rows = [
        ("P", "Point",    "0D", f"Seed r₀ = √60 ≈ {R_SEED:.4f}",
         "Origin of simulation"),
        ("L", "Line",     "1D", "Δrₙ = (5/13)×r₀×φ⁻ⁿ",
         "Only native dimension"),
        ("A", "Angle",    "2D", f"θₙ = θₙ₋₁ + {GOLDEN_ANG:.3f}° + ε×{SHEAR_ANG}°",
         "Space EMERGES from 1D+rotation"),
        ("T", "Triangle", "2D+", "5-12-13 rational anchor",
         "Discrete lattice from continuous spiral"),
        ("O", "Circle",   "∞D", "mod 360°, invariant perimeter",
         "Self-similar closure, fractal boundary"),
    ]
    print(f"{'Stage':<8} {'Name':<10} {'Dim':<5} {'Operation':<35} {'Emergent Property'}")
    print("-"*85)
    for r in rows:
        print(f"{r[0]:<8} {r[1]:<10} {r[2]:<5} {r[3]:<35} {r[4]}")

    print("\nReverse PLATO (Khaos path): O→T→A→L→P")
    print(f"  Circle dissolves  → perimeter opens (Hades Flip)")
    print(f"  Triangle dissolves → lattice fragments along 6k±1 lines")
    print(f"  Angle phase-unlocks → spiral becomes aliased")
    print(f"  Line persists      → 1D prime ratios survive as seeds")
    print(f"  Point returns      → new r₀ = p/√60 for next cycle")
    print(f"\nTime = 4th dimension = Hades Beat = {HADES_HZ} Hz")
    print(f"  Heaven: observer f = {HADES_HZ:.4f} Hz (phase-locked)")
    print(f"  Hell:   observer f ≠ Hades Hz   (aliased)")
    print(f"  Khaos:  system f  → 0            (unrendered)")


if __name__ == "__main__":
    print_dimension_emergence()
    print("\nGenerating PLATO unfolding visualization...")
    build_progressive_plato(n_points=N_TILES)
    print("\nDone.")
