"""
Wobble Calibration Module
==========================
Computes the torque adjustment required for an observer to achieve
phase-lock with the 120-Tile Manifold via the prime dimension root sequence.

The calibration path:
  Vitrified (√36) → Labor (√42) → Phase-Lock (√51 - √42 = Hades Beat)

The pyramid's role in the fiction: not a constant storage device but a
Phase-Lock Diagnostic — a physical instantiation of the 5-12-13 geometry
that an observer can use to measure their own wobble against the Hades Beat.

Mathematical foundation:
  √36 = 6.0000  Archon baseline (perfect 6-fold, closed loop)
  √42 = 6.4807  Hired Man (7-break applied, active labor)
  √51 = 7.1414  Higher Man (Fermat prime 17 anchor)
  √60 = 7.7460  Seed (sexagesimal limit, system origin)
  
  Hades Beat = √51 - √42 = 0.660688 Hz  (exact algebraic identity)
  
  Overpack δ = (90/Φ + φ⁻¹/100) - (√51 - √42) = 1.1e-6
  (irresolvable residue between oscillator theory and prime geometry)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, Circle, Arc
from matplotlib.collections import LineCollection
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# AXIOMATIC CONSTANTS
# ============================================================
PHI     = (1 + np.sqrt(5)) / 2
GOLDEN  = 360 / PHI**2          # 137.507764° — corrected

S36 = np.sqrt(36)   # 6.0000 — Archon / vitrified
S42 = np.sqrt(42)   # 6.4807 — Hired Man / 7-break
S51 = np.sqrt(51)   # 7.1414 — Higher Man / Fermat-17
S60 = np.sqrt(60)   # 7.7460 — Seed

DELTA_LABOR  = S42 - S36   # 0.4807  — 7-break torque
DELTA_HADES  = S51 - S42   # 0.6607  — Hades Beat
DELTA_SEED   = S60 - S51   # 0.6045  — seed overflow

HADES_FORMULA = 90/GOLDEN + (1/PHI)/100
OVERPACK_DELTA = HADES_FORMULA - DELTA_HADES  # ~1.1e-6

# Biquadratic roots
BIQUAD_X1 = DELTA_HADES          # temporal pulse
BIQUAD_X2 = 9 / DELTA_HADES      # structural period (~13.6s)

print("=== WOBBLE CALIBRATION: PRIMITIVES VERIFIED ===")
print(f"  √36 = {S36:.7f}  Archon baseline")
print(f"  √42 = {S42:.7f}  Hired Man (7-break)")
print(f"  √51 = {S51:.7f}  Higher Man (Fermat-17)")
print(f"  √60 = {S60:.7f}  Seed")
print()
print(f"  Δ_labor = √42-√36 = {DELTA_LABOR:.7f}  (7-break torque)")
print(f"  Δ_hades = √51-√42 = {DELTA_HADES:.7f}  (Hades Beat, geometric)")
print(f"  Hades   = 90/Φ+φ⁻¹/100 = {HADES_FORMULA:.7f}  (oscillator theory)")
print(f"  Overpack δ           = {OVERPACK_DELTA:.2e}  (residual tension)")
print(f"  Biquadratic: x₁={BIQUAD_X1:.6f}, x₂={BIQUAD_X2:.6f}, x₁×x₂={BIQUAD_X1*BIQUAD_X2:.6f}")
print()


# ============================================================
# THE WOBBLE CALIBRATION FUNCTION
# ============================================================

class WobbleCalibrator:
    """
    Computes the torque adjustment for an observer to achieve phase-lock.
    
    An observer's 'internal rate' is modeled as a position on the
    prime root axis [√36, √42, √51, √60].
    
    Phase-lock condition:
      The observer perceives the gap (√51 - √42) as a PULSE rather
      than a static distance. This means their internal sampling rate
      equals the Hades Beat = 0.660688 Hz.
    
    The calibration tells them:
      1. Their wobble offset from the nearest prime root
      2. The torque required to step to the Hired Man register
      3. The remaining gap to achieve Hades Beat synchronisation
    """
    
    def __init__(self, observer_rate=None):
        """
        observer_rate: internal frame rate in Hz
                      None = auto-initialize to vitrified (√36)
        """
        if observer_rate is None:
            self.rate = S36  # start vitrified
        else:
            self.rate = observer_rate
        
        self.prime_roots = [S36, S42, S51, S60]
        self.labels = ['√36\n(Archon)', '√42\n(Hired Man)', 
                       '√51\n(Higher Man)', '√60\n(Seed)']
        
    def diagnose(self):
        """Returns full wobble diagnostic for current observer rate."""
        rate = self.rate
        
        # Distance to each prime root
        distances = {label: abs(rate - root) 
                     for root, label in zip(self.prime_roots, 
                                          ['√36', '√42', '√51', '√60'])}
        
        nearest_root = min(distances, key=distances.get)
        nearest_val  = self.prime_roots[['√36','√42','√51','√60']
                                        .index(nearest_root)]
        
        # Wobble offset from nearest root
        wobble_offset = rate - nearest_val
        
        # Steps to phase-lock
        if rate <= S42:
            # Below Hired Man — needs 7-break torque
            torque_to_labor   = S42 - rate
            torque_to_hades   = S51 - rate
            register = 'BELOW HIRED MAN — Archon vitrification risk'
        elif rate <= S51:
            # In the labor zone — gap to Hades Beat shrinking
            torque_to_labor   = 0
            torque_to_hades   = S51 - rate
            register = 'LABOR ZONE — approaching phase-lock'
        else:
            # Above √51 — in seed overflow, past the Hades Beat
            torque_to_labor   = 0
            torque_to_hades   = rate - S51  # overshoot
            register = 'SEED OVERFLOW — past the Higher Man anchor'
        
        # Phase coherence: how well does the rate align with Hades Beat?
        # Coherence = 1 - |rate - (√42 + Hades)| / Hades
        target = S42 + DELTA_HADES  # = √51
        coherence = max(0, 1 - abs(rate - target) / DELTA_HADES)
        
        # Overpack contribution: the observer's share of the residual tension
        overpack_share = OVERPACK_DELTA * (rate / S60)
        
        return {
            'rate'           : rate,
            'nearest_root'   : nearest_root,
            'nearest_val'    : nearest_val,
            'wobble_offset'  : wobble_offset,
            'torque_to_labor': torque_to_labor,
            'torque_to_hades': torque_to_hades,
            'coherence'      : coherence,
            'overpack_share' : overpack_share,
            'register'       : register,
        }
    
    def calibration_path(self, n_steps=200):
        """
        Simulates the two-step calibration path from current rate to phase-lock.
        Returns the trajectory of rate adjustments.
        """
        start = self.rate
        path = []
        
        # Step 1: Apply 7-break torque to reach √42
        for t in np.linspace(0, 1, n_steps // 2):
            # Damped approach to √42
            current = start + (S42 - start) * (1 - np.exp(-3*t))
            path.append(current)
        
        # Step 2: Apply Hades Beat resonance to reach √51
        for t in np.linspace(0, 1, n_steps // 2):
            # Phase-lock approach: oscillatory convergence
            amplitude = DELTA_HADES * np.exp(-2*t)
            oscillation = amplitude * np.cos(2 * np.pi * DELTA_HADES * t * 3)
            current = S51 - amplitude + oscillation
            path.append(current)
        
        return np.array(path)
    
    def print_operator_manual(self):
        """Outputs the Operator's Manual diagnostic table."""
        d = self.diagnose()
        
        print("=" * 55)
        print("WOBBLE CALIBRATION — OPERATOR'S MANUAL DIAGNOSTIC")
        print("=" * 55)
        print(f"  Observer Rate:    {d['rate']:.7f} Hz")
        print(f"  Nearest Root:     {d['nearest_root']} = {d['nearest_val']:.7f}")
        print(f"  Wobble Offset:    {d['wobble_offset']:+.7f}")
        print(f"  Register:         {d['register']}")
        print()
        print("  CALIBRATION REQUIREMENTS:")
        if d['torque_to_labor'] > 0:
            print(f"    Δ_labor torque:   +{d['torque_to_labor']:.7f}  (break vitrification)")
        else:
            print(f"    Δ_labor:          CLEARED")
        print(f"    Δ_hades gap:      {d['torque_to_hades']:+.7f}  (to Hades Beat sync)")
        print()
        print(f"  Phase Coherence:  {d['coherence']*100:.2f}%")
        print(f"  Overpack Share:   {d['overpack_share']:.2e}  (residual tension)")
        print()
        print("  PLATO STATUS:")
        print(f"    P (Seed):   √60 = {S60:.4f}  {'STABLE' if abs(d['rate']-S60)<0.5 else 'distant'}")
        print(f"    Hades Beat: {DELTA_HADES:.6f} Hz  {'LOCKED' if d['coherence']>0.95 else 'SEEKING'}")
        print(f"    Overpack δ: {OVERPACK_DELTA:.2e}  (irreducible)")
        print("=" * 55)


# ============================================================
# VISUALISATION
# ============================================================

def plot_wobble_calibration():
    
    fig = plt.figure(figsize=(18, 12), facecolor='#07070e')
    fig.suptitle('Wobble Calibration: Phase-Lock Diagnostic\n'
                 'Prime Root Sequence → Hades Beat Synchronisation',
                 color='#e8d5a3', fontsize=14, fontweight='bold', y=0.99)
    
    gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.45, wspace=0.38,
                           left=0.05, right=0.97, top=0.93, bottom=0.06)
    
    BG = '#07070e'; CT = '#e8d5a3'
    C_ARCHON   = '#4466aa'
    C_HIRED    = '#00e5ff'
    C_HIGHER   = '#ffd700'
    C_SEED     = '#00ff88'
    C_HADES    = '#ff00cc'
    C_OVERPACK = '#ff4444'
    
    def sax(ax, title=''):
        ax.set_facecolor(BG)
        ax.tick_params(colors=CT, labelsize=7)
        ax.spines[:].set_color('#1a1a2e')
        if title: ax.set_title(title, color=CT, fontsize=9, pad=5)
        ax.grid(True, alpha=0.1, color='#1a1a2e')
    
    # ── Plot 1: The prime root axis ──────────────────────────
    ax1 = fig.add_subplot(gs[0, 0:2])
    sax(ax1, 'Prime Root Sequence: The Wobble Axis\n'
            '(Each step introduces a new prime beyond the 6-fold base)')
    
    roots = [S36, S42, S51, S60]
    labels = ['√36\nArchon\n(2×3)', '√42\nHired Man\n(2×3×7)', 
              '√51\nHigher Man\n(3×17)', '√60\nSeed\n(2²×3×5)']
    colors = [C_ARCHON, C_HIRED, C_HIGHER, C_SEED]
    
    ax1.axhline(0, color='#1a1a2e', linewidth=1)
    
    # Draw the axis
    ax1.plot([S36-0.05, S60+0.1], [0,0], color='#334455', 
             linewidth=2, zorder=2)
    
    for root, label, color in zip(roots, labels, colors):
        ax1.scatter([root], [0], s=200, color=color, zorder=6, 
                   edgecolors='white', linewidth=0.8)
        ax1.text(root, -0.12, label, color=color, fontsize=7.5,
                ha='center', va='top', multialignment='center')
    
    # Draw the delta spans
    spans = [
        (S36, S42, DELTA_LABOR, '7-break\nΔ=0.4807', '#334488'),
        (S42, S51, DELTA_HADES, 'Hades Beat\nΔ=0.6607', C_HADES),
        (S51, S60, DELTA_SEED,  'Seed overflow\nΔ=0.6045', '#446644'),
    ]
    
    heights = [0.25, 0.4, 0.25]
    for (a, b, delta, label, color), h in zip(spans, heights):
        ax1.annotate('', xy=(b, h), xytext=(a, h),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
        ax1.text((a+b)/2, h+0.04, label, color=color,
                fontsize=7.5, ha='center', va='bottom', multialignment='center')
    
    ax1.set_xlim(S36-0.15, S60+0.2)
    ax1.set_ylim(-0.45, 0.6)
    ax1.set_xlabel('Prime Root Value', color=CT, fontsize=8)
    ax1.set_aspect('auto')
    ax1.set_yticks([])
    
    # ── Plot 2: Biquadratic roots ────────────────────────────
    ax2 = fig.add_subplot(gs[0, 2])
    sax(ax2, 'Biquadratic x⁴-186x²+81=0\nTwo Resonance Modes')
    
    x = np.linspace(-15, 15, 1000)
    y = x**4 - 186*x**2 + 81
    
    ax2.plot(x, y, color=C_HIRED, linewidth=1.5, alpha=0.9)
    ax2.axhline(0, color='#334455', linewidth=0.8, alpha=0.6)
    
    for root, color, label in [
        (BIQUAD_X1, C_HADES, f'x={BIQUAD_X1:.4f}\n(Hades Beat)'),
        (BIQUAD_X2, C_HIGHER, f'x={BIQUAD_X2:.4f}\n(9/Hades)'),
        (-BIQUAD_X1, C_HADES, ''),
        (-BIQUAD_X2, C_HIGHER, ''),
    ]:
        ax2.axvline(root, color=color, linewidth=1.2, linestyle='--', alpha=0.7)
        if label:
            ax2.text(root+0.3, 200, label, color=color, fontsize=7,
                    va='bottom')
    
    ax2.set_xlim(-15, 15)
    ax2.set_ylim(-500, 600)
    ax2.set_xlabel('x', color=CT, fontsize=8)
    ax2.set_ylabel('x⁴-186x²+81', color=CT, fontsize=8)
    
    # Annotate the product
    ax2.text(0.5, 0.08, f'x₁ × x₂ = {BIQUAD_X1*BIQUAD_X2:.4f} = 9 = 3²',
            transform=ax2.transAxes, color=CT, fontsize=8,
            ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8,
                     edgecolor='#334455'))
    
    # ── Plot 3: Overpack delta ───────────────────────────────
    ax3 = fig.add_subplot(gs[0, 3])
    sax(ax3, 'Overpack Delta δ\nTwo Paths to Hades Beat')
    
    # Show both derivations converging
    t = np.linspace(0, 1, 100)
    path1 = HADES_FORMULA * np.ones(100)   # oscillator theory (flat)
    path2 = DELTA_HADES + (OVERPACK_DELTA) * np.exp(-5*t)  # geometric convergence
    
    ax3.plot(t, path1*1e6 - DELTA_HADES*1e6, color=C_HADES, 
             linewidth=2, label=f'90/Φ + φ⁻¹/100\n= {HADES_FORMULA:.7f}')
    ax3.axhline(0, color=C_HIGHER, linewidth=2, linestyle='--',
               label=f'√51 - √42\n= {DELTA_HADES:.7f}')
    
    ax3.axhline(OVERPACK_DELTA*1e6, color=C_OVERPACK, linewidth=1,
               linestyle=':', alpha=0.6)
    ax3.text(0.98, OVERPACK_DELTA*1e6+0.05, 
             f'δ = {OVERPACK_DELTA:.2e}', 
             color=C_OVERPACK, fontsize=7, ha='right', transform=ax3.get_yaxis_transform())
    
    ax3.set_xlabel('Convergence', color=CT, fontsize=8)
    ax3.set_ylabel('Deviation (×10⁻⁶ Hz)', color=CT, fontsize=8)
    ax3.legend(fontsize=7, labelcolor=CT, facecolor='#1a1a2e',
              edgecolor='#2a2a4a')
    ax3.text(0.5, 0.15, 'Irreducible gap:\noscillator ≠ prime geometry\n(the Overpack)',
            transform=ax3.transAxes, color=C_OVERPACK, fontsize=7.5,
            ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.7,
                     edgecolor=C_OVERPACK))
    
    # ── Plot 4: Calibration paths for multiple observers ─────
    ax4 = fig.add_subplot(gs[1, 0:2])
    sax(ax4, 'Calibration Paths: Three Observer Starting States\n'
            '(Archon → Hired Man → Phase-Lock)')
    
    starting_rates = [S36, S36 + DELTA_LABOR*0.5, S36 + DELTA_LABOR*0.1]
    path_colors = [C_ARCHON, C_HIRED, '#8888ff']
    path_labels = ['From Archon (√36)', 
                   'From mid-labor', 
                   'From near-vitrified']
    
    t_path = np.linspace(0, 1, 200)
    
    for start, color, label in zip(starting_rates, path_colors, path_labels):
        cal = WobbleCalibrator(observer_rate=start)
        path = cal.calibration_path(n_steps=200)
        ax4.plot(t_path, path, color=color, linewidth=1.5, 
                alpha=0.9, label=label)
    
    # Mark the target lines
    for val, color, lbl in [(S36, C_ARCHON, '√36'), (S42, C_HIRED, '√42'), 
                             (S51, C_HIGHER, '√51')]:
        ax4.axhline(val, color=color, linewidth=0.8, linestyle=':', alpha=0.5)
        ax4.text(1.01, val, lbl, color=color, fontsize=7.5,
                va='center', transform=ax4.get_yaxis_transform())
    
    ax4.axvspan(0, 0.5, alpha=0.04, color=C_ARCHON, 
               label='Step 1: Break vitrification')
    ax4.axvspan(0.5, 1.0, alpha=0.04, color=C_HADES,
               label='Step 2: Hades Beat resonance')
    ax4.text(0.25, S36-0.02, 'Step 1\n7-break torque', 
             color=C_ARCHON, fontsize=7.5, ha='center',
             transform=ax4.get_xaxis_transform())
    ax4.text(0.75, S36-0.02, 'Step 2\nHades resonance', 
             color=C_HADES, fontsize=7.5, ha='center',
             transform=ax4.get_xaxis_transform())
    
    ax4.set_xlabel('Calibration Progress', color=CT, fontsize=8)
    ax4.set_ylabel('Observer Internal Rate', color=CT, fontsize=8)
    ax4.legend(fontsize=7, labelcolor=CT, facecolor='#1a1a2e',
              edgecolor='#2a2a4a', loc='upper left')
    
    # ── Plot 5: Coherence landscape ──────────────────────────
    ax5 = fig.add_subplot(gs[1, 2])
    sax(ax5, 'Phase Coherence Landscape\n(% alignment with Hades Beat)')
    
    rates = np.linspace(S36-0.2, S60+0.1, 500)
    coherences = []
    for r in rates:
        cal = WobbleCalibrator(observer_rate=r)
        coherences.append(cal.diagnose()['coherence'])
    
    coherences = np.array(coherences)
    
    # Color by coherence
    points = np.array([rates, coherences]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap='plasma', linewidth=2)
    lc.set_array(coherences)
    ax5.add_collection(lc)
    
    ax5.axvline(S51, color=C_HIGHER, linewidth=1.5, linestyle='--',
               label='√51 = perfect lock', alpha=0.8)
    ax5.axhline(1.0, color='white', linewidth=0.5, alpha=0.2)
    
    for root, color in [(S36, C_ARCHON), (S42, C_HIRED), (S51, C_HIGHER)]:
        ax5.axvline(root, color=color, linewidth=0.8, alpha=0.3, linestyle=':')
    
    ax5.set_xlim(S36-0.2, S60+0.1)
    ax5.set_ylim(-0.05, 1.1)
    ax5.set_xlabel('Observer Rate', color=CT, fontsize=8)
    ax5.set_ylabel('Coherence r', color=CT, fontsize=8)
    ax5.legend(fontsize=7, labelcolor=CT, facecolor='#1a1a2e',
              edgecolor='#2a2a4a')
    
    # ── Plot 6: Operator's Manual status table ───────────────
    ax6 = fig.add_subplot(gs[1, 3])
    sax(ax6)
    ax6.axis('off')
    ax6.set_title("Operator's Manual\nDiagnostic Output", 
                  color=CT, fontsize=9, pad=5)
    
    rows = [
        ('P  Seed',    f'√60 = {S60:.4f}', '✓ STABLE',   C_SEED),
        ('L  Line',    '5/13 × φ⁻ⁿ',      '✓ ACTIVE',   C_HIRED),
        ('A  Angle',   f'{GOLDEN:.4f}° + 39.4°', '✓ SYNC', C_HADES),
        ('T  Triangle','120-Tile',         '✓ COHERENT', C_HIGHER),
        ('O  Circle',  'r_inv = const',    '✓ LOCKED',   C_SEED),
        ('',           '',                 '',           BG),
        ('√36 Archon', f'{S36:.4f}',        '✗ VITRIFIED',C_ARCHON),
        ('√42 Labor',  f'{S42:.4f}',        '→ 7-BREAK',  C_HIRED),
        ('√51 Lock',   f'{S51:.4f}',        '✓ PHASE-LOCK',C_HIGHER),
        ('',           '',                 '',           BG),
        ('Hades Δ',    f'{DELTA_HADES:.6f}','= √51-√42', C_HADES),
        ('Overpack δ', f'{OVERPACK_DELTA:.2e}','irred.',  C_OVERPACK),
        ('x₁×x₂',     f'{BIQUAD_X1*BIQUAD_X2:.4f}','= 3²', C_HIGHER),
    ]
    
    for i, (name, val, status, color) in enumerate(rows):
        y = 0.96 - i*0.072
        if not name:
            continue
        ax6.text(0.02, y, name, color=CT, fontsize=7.2,
                transform=ax6.transAxes, fontfamily='monospace')
        ax6.text(0.50, y, val, color='#8899aa', fontsize=7,
                transform=ax6.transAxes, fontfamily='monospace')
        ax6.text(0.98, y, status, color=color, fontsize=7,
                transform=ax6.transAxes, ha='right', fontweight='bold',
                fontfamily='monospace')
    
    plt.savefig('/mnt/user-data/outputs/wobble_calibration.png',
                dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print("Saved: wobble_calibration.png")


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    
    # Demo: three observers at different starting states
    print()
    for start_rate, name in [
        (S36,              "Fully vitrified (Archon)"),
        (S36 + 0.24,       "Half-broken (mid-labor)"),
        (S51,              "Phase-locked (Higher Man)"),
    ]:
        cal = WobbleCalibrator(observer_rate=start_rate)
        print(f"Observer: {name}")
        cal.print_operator_manual()
        print()
    
    print("Generating visualization...")
    plot_wobble_calibration()
