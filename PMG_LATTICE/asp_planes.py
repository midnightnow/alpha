import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. CORE GEOMETRY (Hero 93 v4.0 Logic) ---
def generate_hero_93():
    phi = (1 + np.sqrt(5)) / 2
    STEP_SIZE = 5
    MOD = 24
    STEPS = 120
    TOL = 0.45
    
    apex_height = 13 * np.sqrt(3) / 2
    
    all_verts = []
    for n in range(STEPS):
        theta = 2 * np.pi * (STEP_SIZE * n % MOD) / MOD
        z = n * 0.08
        helix_pt = np.array([np.cos(theta), np.sin(theta), z])
        
        base_offsets = [
            np.array([-0.5, -0.5, 0]),
            np.array([ 0.5, -0.5, 0]),
            np.array([ 0.5,  0.5, 0]),
            np.array([-0.5,  0.5, 0])
        ]
        apex_offset = np.array([0, 0, apex_height / 13])
        
        for offset in base_offsets + [apex_offset]:
            all_verts.append(helix_pt + offset)

    all_verts = np.array(all_verts)
    # Simple deduplication for visualization script
    unique_verts = []
    for v in all_verts:
        if not any(np.linalg.norm(v - uv) < TOL for uv in unique_verts):
            unique_verts.append(v)
    
    unique_verts = np.array(unique_verts)
    norms = np.linalg.norm(unique_verts, axis=1)
    projected = unique_verts / (norms[:, None] + 1e-9)
    return projected[:93]

# --- 2. GOLDEN RECTANGLES (Icosahedral Seeds) ---
phi = (1 + np.sqrt(5)) / 2

def get_rect(plane='xy'):
    # A golden rectangle is 1 x phi
    h = phi / 2
    w = 0.5
    if plane == 'xy': # Sagittal slice context
        return np.array([[w, h, 0], [w, -h, 0], [-w, -h, 0], [-w, h, 0], [w, h, 0]])
    elif plane == 'yz': # Coronal slice context
        return np.array([[0, w, h], [0, w, -h], [0, -w, -h], [0, -w, h], [0, w, h]])
    elif plane == 'zx': # Transverse slice context
        return np.array([[h, 0, w], [-h, 0, w], [-h, 0, -w], [h, 0, -w], [h, 0, w]])

# --- 3. PLOTTING ---
pts = generate_hero_93()
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# The Asp (93 Points)
t = np.linspace(0, 1, 93)
ax.scatter(pts[:,0], pts[:,1], pts[:,2], c=t, cmap='plasma', s=40, label='Asp (93 Nodes)')
ax.plot(pts[:,0], pts[:,1], pts[:,2], color='white', alpha=0.3, linewidth=1)

# The Three Golden Rectangles (Light Lines)
rect_xy = get_rect('xy')
rect_yz = get_rect('yz')
rect_zx = get_rect('zx')

ax.plot(rect_xy[:,0], rect_xy[:,1], rect_xy[:,2], color='cyan', linewidth=3, label='XY (Transverse Lintel)')
ax.plot(rect_yz[:,0], rect_yz[:,1], rect_yz[:,2], color='magenta', linewidth=3, label='YZ (Sagittal Lens)')
ax.plot(rect_zx[:,0], rect_zx[:,1], rect_zx[:,2], color='yellow', linewidth=3, label='ZX (Coronal Manus)')

# Anatomical Planes (Semi-transparent)
lim = 1.2
xx, yy = np.meshgrid([-lim, lim], [-lim, lim])
ax.plot_surface(xx, yy, np.zeros_like(xx), alpha=0.1, color='blue') # Transverse
ax.plot_surface(np.zeros_like(xx), xx, yy, alpha=0.1, color='red') # Sagittal
ax.plot_surface(xx, np.zeros_like(xx), yy, alpha=0.1, color='green') # Coronal

# Annotations (Lentil/Lintel Logic)
# Heart Centre = 4
heart = pts[4]
ax.scatter(heart[0], heart[1], heart[2], color='red', s=200, marker='*', label='Heart (4)')
ax.text(heart[0], heart[1], heart[2], "  CENTRE (4)", color='red', weight='bold')

# Manus (27 Bones / Shave)
manus_pts = pts[33:60] # Approximate 27-bone section
ax.scatter(manus_pts[:,0], manus_pts[:,1], manus_pts[:,2], color='gold', s=100, label='Manus (27 Bones)')

# Labels & View
ax.set_axis_off()
ax.set_title("The Asp Manifold: Lintel, Lens, and Lentil\n(93 Points in 3 Golden Sections)", color='white', size=20)
ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.legend(facecolor='black', labelcolor='white')

# Set camera angle
ax.view_init(elev=20, azim=45)

plt.savefig("/Users/studio/ALPHA/PMG_LATTICE/asp_3_planes_final.png", dpi=300, bbox_inches='tight')
print("Vitrification Complete: asp_3_planes_final.png saved.")
