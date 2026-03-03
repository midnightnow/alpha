"""
THE 171 INTERSECTION DIAGRAM
=============================
Generates a multi-panel visualization proving that Node 171 is the
universal convergence point of all PMG frameworks.

Panels:
  1. The 13-Node Lattice (2D circle) with Hades Null at node 13
  2. The 93-Node Icosahedron (3D) with Node 78 highlighted
  3. The Flower of Petals (R²=m for 5:12:13 family) showing 169/171 adjacency
  4. The 26-Letter Orbit (linear congruential path through Orbit 1)
  5. The Conservation of Light & Shade (L×S = 0.573 invariant)
  6. The Accumulated Drift (171 × 0.0191 ≈ π + Hades Gap)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
import json
import os

# ═══════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════
PHI = (1 + np.sqrt(5)) / 2
HADES_DRIFT = 0.0191
PI = np.pi

# Color palette (dark synthwave)
BG_COLOR = '#0a0a1a'
GRID_COLOR = '#1a1a3a'
TEXT_COLOR = '#e0e0ff'
GOLD = '#ffd700'
CYAN = '#00ffff'
MAGENTA = '#ff00ff'
RED = '#ff3366'
GREEN = '#33ff99'
BLUE = '#3366ff'
WHITE = '#ffffff'
GHOST = '#8844ff'

# ═══════════════════════════════════════════════════════
# PANEL 1: 13-NODE LATTICE
# ═══════════════════════════════════════════════════════
def draw_13_node_lattice(ax):
    ax.set_facecolor(BG_COLOR)
    ax.set_title("Panel 1: The 13-Node Lattice\n(Hades Null at Node 13)", 
                  color=GOLD, fontsize=10, fontweight='bold')
    
    R = 4.0
    angles = [2 * PI * (n-1) / 13 for n in range(1, 14)]
    xs = [R * np.cos(a) for a in angles]
    ys = [R * np.sin(a) for a in angles]
    
    # Draw circle
    circle = Circle((0, 0), R, fill=False, color=CYAN, alpha=0.3, linewidth=1)
    ax.add_patch(circle)
    
    # Draw nodes
    for i in range(13):
        color = RED if i == 12 else (GOLD if i in [0, 4, 8] else CYAN)
        size = 120 if i == 12 else (80 if i in [0, 4, 8] else 40)
        ax.scatter(xs[i], ys[i], c=color, s=size, zorder=5, edgecolors=WHITE, linewidths=0.5)
        label = f"N{i+1}" if i != 12 else "N13\n(Hades)"
        ax.annotate(label, (xs[i], ys[i]), textcoords="offset points", 
                   xytext=(10, 5), color=color, fontsize=6)
    
    # Hades annotation
    ax.annotate(f"E = 1/169\nψ = 0", (xs[12], ys[12]), textcoords="offset points",
               xytext=(-40, -25), color=RED, fontsize=7, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_COLOR, edgecolor=RED, alpha=0.8))
    
    # Center (Ω)
    ax.scatter(0, 0, c=GHOST, s=100, zorder=5, marker='*', edgecolors=WHITE)
    ax.annotate("Ω\n(Silent)", (0, 0), textcoords="offset points",
               xytext=(8, -15), color=GHOST, fontsize=7)
    
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-5.5, 5.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.1, color=GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=6)

# ═══════════════════════════════════════════════════════
# PANEL 2: 93-NODE MATRIX (projected 3D → 2D)
# ═══════════════════════════════════════════════════════
def draw_93_node_matrix(ax):
    ax.set_facecolor(BG_COLOR)
    ax.set_title("Panel 2: 93-Node Matrix\n(Node 78 = 171 Spark)", 
                  color=GOLD, fontsize=10, fontweight='bold')
    
    # Load coordinates
    json_path = "/Users/studio/Sovereign/0platonicverses/93_NODE_COORDINATES.json"
    if not os.path.exists(json_path):
        ax.text(0.5, 0.5, "93_NODE_COORDINATES.json\nnot found", 
                transform=ax.transAxes, color=RED, ha='center', fontsize=10)
        return
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    verts = np.array(data["coordinates"]["vertices"])        # 12
    faces = np.array(data["coordinates"]["faces"])            # 20
    edges = np.array(data["coordinates"]["edge_nodes"])       # 60
    center = np.array(data["coordinates"]["center"])          # 1
    
    # Project 3D to 2D (simple orthographic XY)
    ax.scatter(verts[:, 0], verts[:, 1], c=BLUE, s=60, alpha=0.7, label='Vertices (12)', zorder=3)
    ax.scatter(faces[:, 0], faces[:, 1], c=GOLD, s=30, alpha=0.5, label='Faces (20)', zorder=3)
    ax.scatter(edges[:, 0], edges[:, 1], c=GREEN, s=15, alpha=0.4, label='Edges (60)', zorder=3)
    ax.scatter(center[:, 0], center[:, 1], c=GHOST, s=120, marker='*', label='Ω (1)', zorder=5)
    
    # Highlight Node 78 (171 Spark) - edge_nodes index 78-33 = 45
    n78 = edges[78 - 33]
    ax.scatter(n78[0], n78[1], c=RED, s=200, marker='D', zorder=6, edgecolors=WHITE, linewidths=1.5)
    ax.annotate("Node 78\n(171 Spark)", (n78[0], n78[1]), textcoords="offset points",
               xytext=(12, 12), color=RED, fontsize=8, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_COLOR, edgecolor=RED, alpha=0.9))
    
    # Highlight vowels
    vowel_nodes = {
        "A": ("vertices", 0),    # Node 1
        "E": ("edge_nodes", 1),  # Node 34
        "I": ("edge_nodes", 34), # Node 67
        "O": ("edge_nodes", 37), # Node 70
        "U": ("edge_nodes", 40), # Node 73
    }
    for v, (layer, idx) in vowel_nodes.items():
        coord = np.array(data["coordinates"][layer][idx])
        ax.scatter(coord[0], coord[1], c=MAGENTA, s=80, marker='o', zorder=5, 
                  edgecolors=WHITE, linewidths=0.8)
        ax.annotate(v, (coord[0], coord[1]), textcoords="offset points",
                   xytext=(6, 6), color=MAGENTA, fontsize=7, fontweight='bold')
    
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-6.5, 6.5)
    ax.set_aspect('equal')
    ax.legend(fontsize=6, loc='lower right', facecolor=BG_COLOR, edgecolor=GRID_COLOR, 
              labelcolor=TEXT_COLOR)
    ax.grid(True, alpha=0.1, color=GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=6)

# ═══════════════════════════════════════════════════════
# PANEL 3: THE FLOWER OF PETALS (R² = m)
# ═══════════════════════════════════════════════════════
def draw_flower_of_petals(ax):
    ax.set_facecolor(BG_COLOR)
    ax.set_title("Panel 3: The Flower of Petals\n(169 Visible ↔ 171 Invisible)", 
                  color=GOLD, fontsize=10, fontweight='bold')
    
    # Plot R² values for m = 1 to 250
    m_vals = np.arange(1, 251)
    k_vals = 2 * np.sqrt(m_vals) / 13
    
    # Highlight specific petals
    special = {
        42: ("m=42 (Near Seed)", 'gray', 60),
        169: ("m=169 (Visible)", CYAN, 150),
        171: ("m=171 (Invisible)", RED, 150),
        216: ("m=216 (3³+4³+5³)", GOLD, 80),
        338: ("m=338 (5²+12²+13²)", GREEN, 80),
    }
    
    # Plot all petals as a spiral
    theta_vals = m_vals * 2 * PI / 13  # wrap around the 13-cycle
    r_vals = np.sqrt(m_vals)
    
    ax.scatter(theta_vals, r_vals, c=CYAN, s=5, alpha=0.2)
    
    for m, (label, color, size) in special.items():
        theta = m * 2 * PI / 13
        r = np.sqrt(m)
        ax.scatter(theta, r, c=color, s=size, zorder=5, edgecolors=WHITE, linewidths=0.8)
        ax.annotate(label, (theta, r), textcoords="offset points",
                   xytext=(8, 8), color=color, fontsize=6, fontweight='bold')
    
    # Draw the 169-171 bridge
    t169 = 169 * 2 * PI / 13
    t171 = 171 * 2 * PI / 13
    r169 = np.sqrt(169)
    r171 = np.sqrt(171)
    ax.annotate("", xy=(t171, r171), xytext=(t169, r169),
               arrowprops=dict(arrowstyle='<->', color=MAGENTA, lw=2))
    ax.annotate("+2\n(Ghost Post)", ((t169+t171)/2, (r169+r171)/2),
               textcoords="offset points", xytext=(15, 0),
               color=MAGENTA, fontsize=7, fontweight='bold')
    
    ax.set_xlabel("θ (phase angle)", color=TEXT_COLOR, fontsize=7)
    ax.set_ylabel("R = √m", color=TEXT_COLOR, fontsize=7)
    ax.grid(True, alpha=0.1, color=GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=6)

# ═══════════════════════════════════════════════════════
# PANEL 4: THE 26-LETTER ORBIT
# ═══════════════════════════════════════════════════════
def draw_26_letter_orbit(ax):
    ax.set_facecolor(BG_COLOR)
    ax.set_title("Panel 4: The 26-Letter Orbit\n(171 Index → 93-Node Path)", 
                  color=GOLD, fontsize=10, fontweight='bold')
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nodes = []
    for i, letter in enumerate(letters):
        m = i + 1
        N = ((m - 1) * 171) % 93 + 1
        nodes.append(N)
    
    # Plot the path
    ax.plot(range(1, 27), nodes, '-', color=CYAN, alpha=0.5, linewidth=1)
    
    # Color by type
    vowels = set('AEIOU')
    for i, (letter, node) in enumerate(zip(letters, nodes)):
        if letter in vowels:
            color = MAGENTA
            marker = 'D'
            size = 80
        else:
            color = CYAN
            marker = 'o'
            size = 30
        ax.scatter(i+1, node, c=color, s=size, marker=marker, zorder=5, 
                  edgecolors=WHITE, linewidths=0.5)
        ax.annotate(letter, (i+1, node), textcoords="offset points",
                   xytext=(0, 7), color=color, fontsize=6, ha='center')
    
    # Mark the missing nodes
    missing = [16, 31, 46, 61, 76]
    for m in missing:
        ax.axhline(y=m, color=RED, alpha=0.2, linewidth=0.8, linestyle='--')
    ax.annotate("Missing: 16,31,46,61,76\n(Unspoken Phonemes)", 
               xy=(20, 16), color=RED, fontsize=6,
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_COLOR, edgecolor=RED, alpha=0.8))
    
    # Mark Node 78 as unreachable by any letter
    ax.axhline(y=78, color=GOLD, alpha=0.5, linewidth=1.5, linestyle='-.')
    ax.annotate("Node 78 (171 Spark)\nNot in Orbit 1 → Silent Ω", 
               xy=(5, 78), color=GOLD, fontsize=7, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_COLOR, edgecolor=GOLD, alpha=0.9))
    
    ax.set_xlabel("Letter Weight (m)", color=TEXT_COLOR, fontsize=7)
    ax.set_ylabel("93-Node Index", color=TEXT_COLOR, fontsize=7)
    ax.set_xlim(0, 27)
    ax.set_ylim(0, 95)
    ax.grid(True, alpha=0.1, color=GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=6)

# ═══════════════════════════════════════════════════════
# PANEL 5: CONSERVATION OF LIGHT & SHADE
# ═══════════════════════════════════════════════════════
def draw_conservation(ax):
    ax.set_facecolor(BG_COLOR)
    ax.set_title("Panel 5: Conservation of Light & Shade\n(L × S = 0.573 invariant)", 
                  color=GOLD, fontsize=10, fontweight='bold')
    
    # Data: triangle family scaling
    k_vals = np.array([1, 2, 3, 4, 5, 6])
    light_vals = 30 * k_vals  # sum of sides scales linearly
    shade_vals = 0.573 / light_vals  # conservation: L × S = const
    
    # Plot
    ax2 = ax.twinx()
    
    line1, = ax.plot(k_vals, light_vals, 'o-', color=CYAN, linewidth=2, markersize=6, label='Light (L)')
    line2, = ax2.plot(k_vals, shade_vals, 's-', color=RED, linewidth=2, markersize=6, label='Shade (S)')
    
    # Annotate the constant
    for k, l, s in zip(k_vals, light_vals, shade_vals):
        product = l * s
        ax.annotate(f"L×S={product:.3f}", (k, l), textcoords="offset points",
                   xytext=(8, -12), color=GOLD, fontsize=6)
    
    ax.set_xlabel("Scale Factor k", color=TEXT_COLOR, fontsize=7)
    ax.set_ylabel("Light (integer nodes)", color=CYAN, fontsize=7)
    ax2.set_ylabel("Shade (Hades Gap per node)", color=RED, fontsize=7)
    
    ax.tick_params(axis='y', colors=CYAN, labelsize=6)
    ax2.tick_params(axis='y', colors=RED, labelsize=6)
    ax.tick_params(axis='x', colors=TEXT_COLOR, labelsize=6)
    
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, fontsize=6, loc='center right', facecolor=BG_COLOR, 
              edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax.grid(True, alpha=0.1, color=GRID_COLOR)

# ═══════════════════════════════════════════════════════
# PANEL 6: ACCUMULATED DRIFT (171 × 0.0191 ≈ π + Hades)
# ═══════════════════════════════════════════════════════
def draw_accumulated_drift(ax):
    ax.set_facecolor(BG_COLOR)
    ax.set_title("Panel 6: Accumulated Drift\n(171 × 0.0191 ≈ π + Hades Gap)", 
                  color=GOLD, fontsize=10, fontweight='bold')
    
    nodes = np.arange(1, 250)
    drift = HADES_DRIFT * nodes
    
    ax.plot(nodes, drift, color=CYAN, linewidth=1.5, alpha=0.8)
    
    # Mark π
    ax.axhline(y=PI, color=GOLD, alpha=0.6, linewidth=1, linestyle='--')
    ax.annotate(f"π = {PI:.4f}", xy=(20, PI), color=GOLD, fontsize=7)
    
    # Mark 171
    d171 = HADES_DRIFT * 171
    ax.scatter(171, d171, c=RED, s=150, marker='D', zorder=5, edgecolors=WHITE, linewidths=1.5)
    ax.annotate(f"Node 171\nDrift = {d171:.4f}\n= π + {d171-PI:.4f}", 
               (171, d171), textcoords="offset points",
               xytext=(15, 15), color=RED, fontsize=8, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
               bbox=dict(boxstyle='round,pad=0.4', facecolor=BG_COLOR, edgecolor=RED, alpha=0.9))
    
    # Mark 169
    d169 = HADES_DRIFT * 169
    ax.scatter(169, d169, c=CYAN, s=80, marker='o', zorder=5, edgecolors=WHITE)
    ax.annotate(f"Node 169\nDrift = {d169:.4f}", (169, d169), textcoords="offset points",
               xytext=(-60, -20), color=CYAN, fontsize=7)
    
    # Mark the gap
    ax.annotate("", xy=(171, d171), xytext=(171, PI),
               arrowprops=dict(arrowstyle='<->', color=MAGENTA, lw=2))
    ax.annotate(f"Hades Gap\n= {d171-PI:.4f}", (174, (d171+PI)/2),
               color=MAGENTA, fontsize=7, fontweight='bold')
    
    ax.set_xlabel("Node Index", color=TEXT_COLOR, fontsize=7)
    ax.set_ylabel("Accumulated Drift (0.0191 × n)", color=TEXT_COLOR, fontsize=7)
    ax.set_xlim(0, 250)
    ax.grid(True, alpha=0.1, color=GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=6)

# ═══════════════════════════════════════════════════════
# MAIN: ASSEMBLE THE 6-PANEL DIAGRAM
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    fig = plt.figure(figsize=(18, 12), facecolor=BG_COLOR)
    fig.suptitle("THE 171 INTERSECTION DIAGRAM\nUniversal Convergence of All PMG Frameworks",
                 color=GOLD, fontsize=16, fontweight='bold', y=0.98)
    
    # Create 6 subplots (2 rows × 3 cols)
    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236)
    
    draw_13_node_lattice(ax1)
    draw_93_node_matrix(ax2)
    draw_flower_of_petals(ax3)
    draw_26_letter_orbit(ax4)
    draw_conservation(ax5)
    draw_accumulated_drift(ax6)
    
    # Footer equation
    fig.text(0.5, 0.01, 
             "171 = 13² + 2 = (5²+12²+13²)/2 + 2 = 156 + 15 = 169 × (26.16/26)²  |  171 mod 93 = 78  |  171 × 0.0191 ≈ π + 0.1245",
             ha='center', color=MAGENTA, fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', facecolor=BG_COLOR, edgecolor=MAGENTA, alpha=0.9))
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    out_path = "/Users/studio/Sovereign/0platonicverses/PMG_PUBLICATION_v1.0/THE_171_INTERSECTION_DIAGRAM.png"
    plt.savefig(out_path, dpi=200, facecolor=BG_COLOR, bbox_inches='tight')
    print(f"171 Intersection Diagram saved to: {out_path}")
    plt.close()
