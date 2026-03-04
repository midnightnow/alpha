"""
RENDER_FRONTISPIECE.PY
The Sovereign Sphere: Visual proof of the 10-24-26 Triad.
Rendered with Hades Slack jitter and Steward force vectors.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless rendering
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pmg_constants import PMG

def render(save_path=None):
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # === THE SPHERE: Sovereign Origin ===
    u, v = np.mgrid[0:2*np.pi:80j, 0:np.pi:80j]
    x = np.cos(u)*np.sin(v) + np.random.normal(0, PMG.HADES_SLACK, u.shape)
    y = np.sin(u)*np.sin(v) + np.random.normal(0, PMG.HADES_SLACK, u.shape)
    z = np.cos(v) + np.random.normal(0, PMG.HADES_SLACK, u.shape)
    
    ax.plot_surface(x, y, z, color='gold', alpha=0.25, edgecolor='white', 
                    linewidth=0.15, antialiased=True)
    
    # === STEWARD VECTORS ===
    origin = [0, 0, 0]
    
    # Mason (10/Number): Cyan strut along X — The Ground
    ax.quiver(*origin, 1.4, 0, 0, color='cyan', arrow_length_ratio=0.1, 
              linewidth=2.5, label='Mason (10: Number)')
    
    # Weaver (24/Measure): Magenta arc along Y — The Weight
    ax.quiver(*origin, 0, 1.4, 0, color='magenta', arrow_length_ratio=0.1, 
              linewidth=2.5, label='Weaver (24: Measure)')
    
    # Architect (26/Language): Gold lift along Z — The Torque
    ax.quiver(*origin, 0, 0, 1.4, color='gold', arrow_length_ratio=0.1, 
              linewidth=2.5, label='Architect (26: Language)')
    
    # === HADES GAP RING ===
    theta = np.linspace(0, 2*np.pi, 100)
    gap_r = PMG.HADES_GAP * 8  # Scaled for visibility
    ax.plot(gap_r * np.cos(theta), gap_r * np.sin(theta), 
            np.zeros_like(theta), color='red', linewidth=1.5, 
            alpha=0.6, linestyle='--', label=f'Hades Gap (Ψ={PMG.HADES_GAP})')
    
    # === STYLING ===
    ax.set_title(
        f"PRINCIPIA MATHEMATICA GEOMETRICA v1.0\n"
        f"THE SPHERE — Σ={PMG.UNITY_THRESHOLD} | β={PMG.BEAT_FREQUENCY} Hz",
        color='white', fontsize=14, fontweight='bold', pad=20
    )
    
    ax.set_xlabel('10 (Number)', color='cyan', fontsize=10)
    ax.set_ylabel('24 (Measure)', color='magenta', fontsize=10)
    ax.set_zlabel('26 (Language)', color='gold', fontsize=10)
    
    ax.tick_params(colors='gray', labelsize=7)
    ax.legend(loc='upper left', fontsize=9, facecolor='black', edgecolor='gray',
              labelcolor='white')
    
    # Clean grid
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True, alpha=0.15)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor='black', bbox_inches='tight')
        print(f"[INSCRIBED] Frontispiece saved to {save_path}")
    else:
        plt.show()

if __name__ == "__main__":
    render(save_path="frontispiece.png")