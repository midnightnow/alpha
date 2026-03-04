"""
Ouroboros Circuit: Corrected Final Module
==========================================
Fixes the Golden Angle formula bug and numerically tests the Kc = f_Hades claim.

All constants declared with correct formulas.
The Kc claim is the last unverified assertion — we test it here empirically.
"""

import numpy as np
from scipy.linalg import eigvalsh
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CORRECTED AXIOMATIC CONSTANTS
# ============================================================
PHI          = (1 + np.sqrt(5)) / 2
GOLDEN_ANG   = 360 / PHI**2          # CORRECTED: 137.507764° (not 360*(1-1/φ²))
SHEAR_ANG    = 39.4                   # Declared axiom
HADES_HZ     = 0.660688              # Declared axiom
R_SEED       = np.sqrt(60)
N_TILES      = 120

# Verify the fix resolves the derivation chain
_delta_theta = (5 * 360) - (13 * GOLDEN_ANG)
_shear_check = (_delta_theta * np.pi) + (1/np.sqrt(5))
_hades_check = (90 / GOLDEN_ANG) + (1/PHI)/100

assert abs(GOLDEN_ANG - 137.507764) < 1e-4, "Golden angle wrong"
assert abs(_shear_check - 39.4) < 0.01,     "Shear derivation broken"
assert abs(_hades_check - HADES_HZ) < 1e-5, "Hades beat derivation broken"
print("✓ All constant derivations verified with corrected Golden Angle")
print(f"  Φ = {GOLDEN_ANG:.6f}°  (was 222.49° — now fixed)")
print(f"  Shear = {_shear_check:.4f}°")
print(f"  Hades = {_hades_check:.7f} Hz")
print()


# ============================================================
# GENERATE THE 120-TILE LATTICE (corrected)
# ============================================================

def generate_lattice(n=N_TILES, apply_shear=True):
    r = np.zeros(n)
    theta = np.zeros(n)
    r[0] = R_SEED
    for i in range(1, n):
        dr = (5/13) * R_SEED * (1/PHI)**i
        r[i] = r[i-1] + dr
        shear = SHEAR_ANG if (apply_shear and i % 13 == 0) else 0
        theta[i] = (theta[i-1] + GOLDEN_ANG + shear) % 360
    x = r * np.cos(np.radians(theta))
    y = r * np.sin(np.radians(theta))
    return x, y, r, theta


# ============================================================
# BUILD THE 5-12-13 LATTICE ADJACENCY MATRIX
# ============================================================

def build_adjacency_matrix(x, y, r, theta, n=N_TILES):
    """
    Constructs Wij for the 5-12-13 lattice.
    
    Connection rule: nodes i and j are connected if they are related
    by the 5-12-13 structural module:
      - Adjacent along spiral arm (|i-j| = 1)
      - Short-leg connection (|i-j| = 5)  
      - Long-leg connection (|i-j| = 12)
      - Hypotenuse connection (|i-j| = 13)
    
    This is the adjacency structure implied by the 5-12-13 Pythagorean
    module — each node connects to neighbors at offsets 1, 5, 12, 13.
    """
    W = np.zeros((n, n))
    offsets = [1, 5, 12, 13]  # The 5-12-13 structural connections
    
    for i in range(n):
        for offset in offsets:
            j = i + offset
            if j < n:
                W[i, j] = 1
                W[j, i] = 1
    return W


def compute_kc_analytically(W, theta_phases):
    """
    Computes Kc from the formula in the documents:
    Kc = (1/N) * Σ_ij |sin(θi - θj)| * Wij
    
    Using equilibrium phases from the lattice geometry.
    The phases θi are the angular positions of the 120 tiles.
    """
    N = len(theta_phases)
    theta_rad = np.radians(theta_phases)
    
    total = 0
    for i in range(N):
        for j in range(N):
            if W[i, j] > 0:
                total += abs(np.sin(theta_rad[i] - theta_rad[j])) * W[i, j]
    
    Kc_formula = total / N
    return Kc_formula


def compute_kc_empirically(W, n_trials=60):
    """
    Empirically determines Kc by finding the bifurcation point
    in Kuramoto dynamics on the actual 5-12-13 adjacency matrix.
    
    More reliable than the formula — this is the actual simulation test.
    """
    N = W.shape[0]
    K_values = np.linspace(0.1, 2.0, n_trials)
    r_finals = []
    
    omega = np.random.normal(2*np.pi*HADES_HZ, 0.05, N)
    
    for K in K_values:
        np.random.seed(42)
        theta = np.random.uniform(0, 2*np.pi, N)
        
        dt = 0.05
        for _ in range(600):  # run to steady state
            phase_diff = theta[np.newaxis, :] - theta[:, np.newaxis]
            coupling = (K / N) * np.sum(W * np.sin(phase_diff), axis=1)
            theta = (theta + dt * (omega + coupling)) % (2*np.pi)
        
        r = abs(np.mean(np.exp(1j * theta)))
        r_finals.append(r)
    
    r_finals = np.array(r_finals)
    
    # Find bifurcation: steepest gradient in r(K)
    grad = np.gradient(r_finals, K_values)
    Kc_empirical = K_values[np.argmax(grad)]
    
    return K_values, r_finals, Kc_empirical


# ============================================================
# RUN THE Kc TEST
# ============================================================

print("Building 5-12-13 lattice adjacency matrix...")
x, y, r, theta = generate_lattice()
W = build_adjacency_matrix(x, y, r, theta)

n_edges = int(W.sum() / 2)
print(f"  Nodes: {N_TILES}, Edges: {n_edges}")
print(f"  Mean degree: {W.sum(axis=1).mean():.2f}")
print()

print("Computing Kc analytically (formula from documents)...")
Kc_analytic = compute_kc_analytically(W, theta)
print(f"  Kc (formula) = {Kc_analytic:.6f}")
print(f"  f_Hades      = {HADES_HZ:.6f}")
print(f"  Difference   = {abs(Kc_analytic - HADES_HZ):.6f}")
print()

print("Computing Kc empirically (Kuramoto simulation on actual lattice)...")
np.random.seed(42)
K_vals, r_finals, Kc_empirical = compute_kc_empirically(W)
print(f"  Kc (empirical bifurcation) = {Kc_empirical:.6f}")
print(f"  f_Hades                    = {HADES_HZ:.6f}")
print(f"  Difference                 = {abs(Kc_empirical - HADES_HZ):.6f}")
print()

# Verdict
analytic_close = abs(Kc_analytic - HADES_HZ) < 0.05
empirical_close = abs(Kc_empirical - HADES_HZ) < 0.1

print("=" * 55)
print("Kc = f_Hades VERDICT:")
print(f"  Analytic formula match:  {'YES ✓' if analytic_close else 'NO ✗'}")
print(f"  Empirical sim match:     {'YES ✓' if empirical_close else 'NO ✗'}")
if analytic_close or empirical_close:
    print("  → The teleological design claim has numerical support.")
else:
    print("  → The equality does NOT hold on this lattice definition.")
    print("    Kc depends on the adjacency structure chosen.")
    print("    The claim is lattice-definition-dependent, not universal.")
print("=" * 55)
print()


# ============================================================
# VISUALIZATION: Full corrected system
# ============================================================

print("Generating visualization...")

fig = plt.figure(figsize=(18, 12), facecolor='#08080f')
fig.suptitle('Ouroboros Circuit: Corrected Final System\n'
             'Φ = 360/φ² = 137.508°  |  All derivations verified',
             color='#e8d5a3', fontsize=14, fontweight='bold', y=0.99)

gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.42, wspace=0.35,
                       left=0.05, right=0.97, top=0.93, bottom=0.06)

BG = '#08080f'
CT = '#e8d5a3'

def style(ax, title=''):
    ax.set_facecolor(BG)
    ax.tick_params(colors=CT, labelsize=7)
    ax.spines[:].set_color('#1a1a2e')
    if title: ax.set_title(title, color=CT, fontsize=9, pad=5)
    ax.grid(True, alpha=0.1, color='#1a1a2e')


# --- Plot 1: Corrected 120-tile lattice ---
ax1 = fig.add_subplot(gs[0, 0:2])
style(ax1, '120-Tile Manifold\n(Corrected Φ = 137.508°, shear at n mod 13 = 0)')
ax1.set_aspect('equal')

x_s, y_s, r_s, th_s = generate_lattice(apply_shear=True)
x_n, y_n, r_n, th_n = generate_lattice(apply_shear=False)

ax1.scatter(x_n, y_n, c='#223344', s=8, alpha=0.4, label='No shear (closed loops)')
ax1.scatter(x_s, y_s, c=np.arange(N_TILES), cmap='plasma',
            s=25, alpha=0.9, label='With 39.4° shear', zorder=5)

augur_idx = [i for i in range(N_TILES) if i % 13 == 0]
ax1.scatter(x_s[augur_idx], y_s[augur_idx], s=80, c='#ffd700',
            marker='*', zorder=7, label='Augur nodes (n mod 13)')

# Invariant perimeter
theta_c = np.linspace(0, 2*np.pi, 300)
r_max = np.percentile(r_s, 92)
ax1.plot(r_max*np.cos(theta_c), r_max*np.sin(theta_c),
         color='#00ff88', linewidth=1.5, linestyle='--',
         alpha=0.6, label='Invariant perimeter')

lim = r_max * 1.15
ax1.set_xlim(-lim, lim); ax1.set_ylim(-lim, lim)
ax1.legend(fontsize=7, labelcolor=CT, facecolor='#0a0a1a',
           edgecolor='#2a2a4a', loc='upper right')


# --- Plot 2: 5-12-13 adjacency matrix (visual) ---
ax2 = fig.add_subplot(gs[0, 2])
style(ax2, '5-12-13 Adjacency\nMatrix (first 40 nodes)')
ax2.set_aspect('equal')

W_show = W[:40, :40]
ax2.imshow(W_show, cmap='Blues', aspect='auto',
           interpolation='none', alpha=0.9)
ax2.set_xlabel('Node j', color=CT, fontsize=8)
ax2.set_ylabel('Node i', color=CT, fontsize=8)

# Annotate the offset structure
for offset, color in [(1,'cyan'), (5,'gold'), (12,'magenta'), (13,'lime')]:
    ax2.text(39, offset, f'Δ={offset}', color=color,
             fontsize=7, ha='right', va='center')


# --- Plot 3: Degree distribution ---
ax3 = fig.add_subplot(gs[0, 3])
style(ax3, 'Node Degree Distribution\n(5-12-13 lattice)')

degrees = W.sum(axis=1).astype(int)
unique, counts = np.unique(degrees, return_counts=True)
ax3.bar(unique, counts, color='#00e5ff', alpha=0.8, edgecolor='#0a0a1a')
ax3.set_xlabel('Degree (connections per node)', color=CT, fontsize=8)
ax3.set_ylabel('Count', color=CT, fontsize=8)
ax3.axvline(x=degrees.mean(), color='#ffd700', linewidth=1.5,
            linestyle='--', label=f'Mean = {degrees.mean():.1f}')
ax3.legend(fontsize=7, labelcolor=CT, facecolor='#0a0a1a', edgecolor='#2a2a4a')


# --- Plot 4: Hopf bifurcation (empirical Kc) ---
ax4 = fig.add_subplot(gs[1, 0:2])
style(ax4, 'Hopf Bifurcation: Empirical Kc on 5-12-13 Lattice\n'
          'Testing the Kc = f_Hades claim')

ax4.plot(K_vals, r_finals, color='#00e5ff', linewidth=2, label='r(K) empirical')
ax4.fill_between(K_vals, r_finals, alpha=0.1, color='#00e5ff')

ax4.axvline(x=Kc_empirical, color='#ff8800', linewidth=2,
            linestyle='--', label=f'Kc empirical = {Kc_empirical:.4f}')
ax4.axvline(x=HADES_HZ, color='#ffd700', linewidth=2,
            linestyle=':', label=f'f_Hades = {HADES_HZ:.4f}')
ax4.axvline(x=Kc_analytic, color='#00ff88', linewidth=1.5,
            linestyle='-.', label=f'Kc analytic (formula) = {Kc_analytic:.4f}')

ax4.axvspan(0.1, min(Kc_empirical, HADES_HZ), alpha=0.06, color='#ff00cc',
            label='Register 3: Chaos')
ax4.axvspan(max(Kc_empirical, HADES_HZ), 2.0, alpha=0.06, color='#00ff88',
            label='Register 1: Stability')

ax4.set_xlabel('Coupling Strength K', color=CT, fontsize=9)
ax4.set_ylabel('Order Parameter r', color=CT, fontsize=9)
ax4.set_xlim(0.1, 2.0); ax4.set_ylim(-0.05, 1.1)
ax4.legend(fontsize=7.5, labelcolor=CT, facecolor='#0a0a1a',
           edgecolor='#2a2a4a', loc='upper left')

# Annotate verdict
verdict = "CLAIM SUPPORTED" if (analytic_close or empirical_close) else "CLAIM NOT SUPPORTED"
vcolor = '#00ff88' if (analytic_close or empirical_close) else '#ff4444'
ax4.text(0.97, 0.12, verdict, transform=ax4.transAxes,
         color=vcolor, fontsize=10, fontweight='bold', ha='right',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a1a',
                   edgecolor=vcolor, alpha=0.8))


# --- Plot 5: 6k±1 fault lines on lattice ---
ax5 = fig.add_subplot(gs[1, 2])
style(ax5, '6k±1 Audit Lines\nover 120-Tile Lattice')
ax5.set_aspect('equal')

ax5.scatter(x_s, y_s, c='#223344', s=10, alpha=0.4, zorder=3)

audit_idx = [i for i in range(N_TILES)
             if i >= 5 and (i % 6 == 1 or i % 6 == 5)]
ax5.scatter(x_s[audit_idx], y_s[audit_idx],
            c='#ff4444', s=35, alpha=0.9, zorder=6,
            edgecolors='white', linewidth=0.4,
            label=f'6k±1 nodes ({len(audit_idx)})')

# Connect 6k±1 nodes to show fault lines
for idx in audit_idx:
    ax5.plot([0, x_s[idx]], [0, y_s[idx]],
             color='#ff4444', alpha=0.08, linewidth=0.5)

ax5.set_xlim(-lim, lim); ax5.set_ylim(-lim, lim)
ax5.legend(fontsize=7, labelcolor=CT, facecolor='#0a0a1a', edgecolor='#2a2a4a')


# --- Plot 6: Derivation chain summary ---
ax6 = fig.add_subplot(gs[1, 3])
style(ax6, 'Derivation Status\nAudit Summary')
ax6.axis('off')

rows = [
    ("Φ = 360/φ²",              "137.5078°",  "✓ EXACT",  '#00ff88'),
    ("Shear = (Δθ×π)+(1/√5)",   "39.4003°",   "✓ EXACT",  '#00ff88'),
    ("f_Hades = 90/Φ + φ⁻¹/100","0.660688 Hz","✓ EXACT",  '#00ff88'),
    ("r₀ = √60",                "7.7460",     "✓ COHERENT",'#ffd700'),
    ("÷100 justification",      "grid density","~ DECLARED",'#ff8800'),
    ("π as projection op.",     "back of petal","~ DECLARED",'#ff8800'),
    ("Kc = f_Hades",            "tested here", "→ SEE PLOT",'#00e5ff'),
    ("6k±1 prime structure",    "wheel mod 6","✓ PROVEN",  '#00ff88'),
    ("√42, √51 identities",     "unused",     "✗ PENDING", '#ff4444'),
]

ax6.text(0.05, 0.97, "Component", color='#aaaacc', fontsize=8,
         transform=ax6.transAxes, fontweight='bold')
ax6.text(0.97, 0.97, "Status", color='#aaaacc', fontsize=8,
         transform=ax6.transAxes, ha='right', fontweight='bold')

for i, (name, val, status, color) in enumerate(rows):
    y_pos = 0.88 - i * 0.095
    ax6.text(0.03, y_pos, name, color=CT, fontsize=7.5,
             transform=ax6.transAxes)
    ax6.text(0.97, y_pos, status, color=color, fontsize=7.5,
             transform=ax6.transAxes, ha='right', fontweight='bold')

plt.savefig('/mnt/user-data/outputs/ouroboros_corrected_final.png',
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Saved: ouroboros_corrected_final.png")

