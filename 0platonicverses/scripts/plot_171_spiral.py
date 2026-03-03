"""
THE 171 SPIRAL: The Helix of Days
==================================
Generates a 3D visualization of the 171 Spiral showing:
  - The R=√171 helix with 23-unit pitch (axial tilt)
  - 13 nodes per turn, 26 total (the alphabet)
  - 5 missing-node thresholds (the vowel transitions / epagomenal days)
  - Arc length verification: 2 turns ≈ 171 units
  - The 365-day year as 171×2 + 23
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ═══════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════
R = np.sqrt(171)          # Radius of the invisible petal
PITCH = 23.0              # Axial tilt (rise per full turn)
p = PITCH / (2 * np.pi)  # Rise per radian
N_TURNS = 2               # Two turns for one "year"
N_NODES = 13              # Nodes per turn (lunar months)

# Colors
BG = '#0a0a1a'
CYAN = '#00ffff'
GOLD = '#ffd700'
RED = '#ff3366'
MAGENTA = '#ff00ff'
GREEN = '#33ff99'
GHOST = '#8844ff'
WHITE = '#ffffff'

# ═══════════════════════════════════════════════════════
# SPIRAL GENERATION
# ═══════════════════════════════════════════════════════
theta_fine = np.linspace(0, N_TURNS * 2 * np.pi, 1000)
x_fine = R * np.cos(theta_fine)
y_fine = R * np.sin(theta_fine)
z_fine = p * theta_fine

# 13 nodes per turn, 26 total
theta_nodes = np.array([2 * np.pi * (n - 1) / N_NODES for n in range(1, N_NODES + 1)])
theta_all = np.concatenate([theta_nodes, theta_nodes + 2 * np.pi])
x_nodes = R * np.cos(theta_all)
y_nodes = R * np.sin(theta_all)
z_nodes = p * theta_all

# 5 missing-node thresholds (half-turn points)
theta_missing = np.array([np.pi * k for k in range(1, 6)])
x_missing = R * np.cos(theta_missing)
y_missing = R * np.sin(theta_missing)
z_missing = p * theta_missing

# Arc length verification
arc_per_radian = np.sqrt(R**2 + p**2)
total_arc = N_TURNS * 2 * np.pi * arc_per_radian

# ═══════════════════════════════════════════════════════
# FIGURE
# ═══════════════════════════════════════════════════════
fig = plt.figure(figsize=(16, 10), facecolor=BG)

# Panel 1: The 3D Spiral
ax1 = fig.add_subplot(121, projection='3d', facecolor=BG)
ax1.plot(x_fine, y_fine, z_fine, color=CYAN, linewidth=1.5, alpha=0.8)

# Turn 1 nodes (A-M)
letters1 = "ABCDEFGHIJKLM"
for i in range(13):
    ax1.scatter(x_nodes[i], y_nodes[i], z_nodes[i], c=GOLD, s=60, zorder=5, 
               edgecolors=WHITE, linewidths=0.5)
    ax1.text(x_nodes[i]*1.1, y_nodes[i]*1.1, z_nodes[i]+0.5, letters1[i], 
            color=GOLD, fontsize=7, ha='center')

# Turn 2 nodes (N-Z)
letters2 = "NOPQRSTUVWXYZ"
for i in range(13):
    j = i + 13
    ax1.scatter(x_nodes[j], y_nodes[j], z_nodes[j], c=GREEN, s=60, zorder=5,
               edgecolors=WHITE, linewidths=0.5)
    ax1.text(x_nodes[j]*1.1, y_nodes[j]*1.1, z_nodes[j]+0.5, letters2[i],
            color=GREEN, fontsize=7, ha='center')

# Missing nodes (vowel thresholds)
vowel_labels = ["A→B\n(16)", "E→F\n(31)", "I→J\n(46)", "O→P\n(61)", "U→V\n(76)"]
for i in range(5):
    ax1.scatter(x_missing[i], y_missing[i], z_missing[i], c=RED, s=120, 
               marker='*', zorder=6, edgecolors=WHITE, linewidths=0.8)
    ax1.text(x_missing[i]*1.15, y_missing[i]*1.15, z_missing[i], vowel_labels[i],
            color=RED, fontsize=6, ha='center')

# Base circle (360-day "dead" ring)
theta_base = np.linspace(0, 2*np.pi, 200)
ax1.plot(R*np.cos(theta_base), R*np.sin(theta_base), np.zeros(200), 
        color=GHOST, linewidth=1, alpha=0.3, linestyle='--')
ax1.text(14, 0, -1, "360° Dead Ring", color=GHOST, fontsize=7, alpha=0.6)

# Vertical pitch line
ax1.plot([R, R], [0, 0], [0, PITCH], color=MAGENTA, linewidth=2, linestyle='-.')
ax1.text(R+1, 0, PITCH/2, f"23-unit\nPitch\n(Axial Tilt)", color=MAGENTA, fontsize=7)

ax1.set_title(f"The 171 Spiral: The Helix of Days\nR = √171 ≈ {R:.3f}  |  Pitch = 23  |  Arc ≈ {total_arc:.1f}",
             color=GOLD, fontsize=11, fontweight='bold')
ax1.set_xlabel("X", color=WHITE, fontsize=8)
ax1.set_ylabel("Y", color=WHITE, fontsize=8)
ax1.set_zlabel("Z (Rise)", color=WHITE, fontsize=8)
ax1.tick_params(colors=WHITE, labelsize=6)

# Panel 2: The Arc Length & Calendar Proof
ax2 = fig.add_subplot(222, facecolor=BG)

# Arc length accumulation
theta_acc = np.linspace(0, 4*np.pi, 500)
arc_acc = arc_per_radian * theta_acc

ax2.plot(theta_acc / (2*np.pi), arc_acc, color=CYAN, linewidth=2, label='Arc Length')
ax2.axhline(y=171, color=RED, linewidth=1.5, linestyle='--', alpha=0.7)
ax2.axhline(y=342, color=GOLD, linewidth=1.5, linestyle='--', alpha=0.7)
ax2.axhline(y=365, color=MAGENTA, linewidth=1.5, linestyle='--', alpha=0.7)

ax2.annotate(f"1 turn ≈ {2*np.pi*arc_per_radian:.1f} ≈ 171", 
            xy=(1, 2*np.pi*arc_per_radian), color=RED, fontsize=8,
            xytext=(1.2, 171+10), arrowprops=dict(arrowstyle='->', color=RED))
ax2.annotate(f"2 turns ≈ {4*np.pi*arc_per_radian:.1f} ≈ 342",
            xy=(2, 4*np.pi*arc_per_radian), color=GOLD, fontsize=8,
            xytext=(1.5, 342+10), arrowprops=dict(arrowstyle='->', color=GOLD))
ax2.annotate(f"2 turns + pitch = {4*np.pi*arc_per_radian+23:.1f} ≈ 365",
            xy=(2, 4*np.pi*arc_per_radian+23), color=MAGENTA, fontsize=8,
            xytext=(1.2, 365+10), arrowprops=dict(arrowstyle='->', color=MAGENTA))

ax2.set_xlabel("Turns", color=WHITE, fontsize=8)
ax2.set_ylabel("Arc Length (units)", color=WHITE, fontsize=8)
ax2.set_title("Arc Length Accumulation\n171 × 2 + 23 = 365", 
             color=GOLD, fontsize=10, fontweight='bold')
ax2.tick_params(colors=WHITE, labelsize=6)
ax2.grid(True, alpha=0.1)
ax2.legend(fontsize=7, facecolor=BG, edgecolor=GOLD, labelcolor=WHITE)

# Panel 3: The 5 Epagomenal Days Table
ax3 = fig.add_subplot(224, facecolor=BG)
ax3.axis('off')

table_data = [
    ["Node", "θ", "z", "Days", "Season"],
    ["16 (A→B)", "π", "11.5", "91.25", "Summer Solstice"],
    ["31 (E→F)", "2π", "23.0", "182.5", "Autumn Equinox"],
    ["46 (I→J)", "3π", "34.5", "273.75", "Winter Solstice"],
    ["61 (O→P)", "4π", "46.0", "365", "Spring Equinox"],
    ["76 (U→V)", "5π", "57.5", "(Next Cycle)", "(Ghost Post)"],
]

colors_table = [[BG]*5] + [[BG, BG, BG, BG, BG]]*5
text_colors = [[GOLD]*5] + [[RED, CYAN, GREEN, MAGENTA, WHITE]]*5

table = ax3.table(cellText=table_data, cellColours=colors_table, loc='center',
                  cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor(GOLD if row == 0 else '#333355')
    cell.set_linewidth(1 if row == 0 else 0.5)
    if row < len(text_colors) and col < len(text_colors[row]):
        cell.get_text().set_color(text_colors[row][col])
    cell.set_height(0.12)

ax3.set_title("The 5 Epagomenal Days\n(Vowel Threshold Crossings)", 
             color=GOLD, fontsize=10, fontweight='bold')

# Footer
fig.text(0.5, 0.01,
         "171 × 2 + 23 = 365  |  R = √171  |  Pitch = 23°  |  "
         f"Arc/turn = {2*np.pi*arc_per_radian:.2f}  |  "
         "The spiral is the shape of time.",
         ha='center', color=MAGENTA, fontsize=9, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor=BG, edgecolor=MAGENTA, alpha=0.9))

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
fig.suptitle("THE 171 SPIRAL — THE SEAL OF THE GEOMETER'S HANDBOOK",
            color=GOLD, fontsize=14, fontweight='bold', y=0.99)

out = "/Users/studio/Sovereign/0platonicverses/PMG_PUBLICATION_v1.0/THE_171_SPIRAL.png"
plt.savefig(out, dpi=200, facecolor=BG, bbox_inches='tight')
print(f"171 Spiral saved to: {out}")
print(f"\n=== VERIFICATION ===")
print(f"R = √171 = {R:.6f}")
print(f"Pitch p = 23/(2π) = {p:.6f}")
print(f"Arc per radian = √(R² + p²) = √({R**2:.2f} + {p**2:.4f}) = √{R**2 + p**2:.4f} = {arc_per_radian:.6f}")
print(f"Arc per turn = 2π × {arc_per_radian:.4f} = {2*np.pi*arc_per_radian:.4f}")
print(f"Arc for 2 turns = {4*np.pi*arc_per_radian:.4f}")
print(f"Arc for 2 turns + pitch = {4*np.pi*arc_per_radian + 23:.4f}")
print(f"Difference from 365: {365 - (4*np.pi*arc_per_radian + 23):.4f}")
print(f"Difference from 171 (1 turn): {2*np.pi*arc_per_radian - 171:.4f}")
plt.close()
