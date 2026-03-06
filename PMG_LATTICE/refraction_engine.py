import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt

def generate_hero_93_v4_2(eps=1.88693):
    """
    Generates the Hero 93 solid based on the v4.2 'Hand/Manus' architecture.
    """
    STEP_SIZE = 5
    MOD = 24
    STEPS = 120
    
    A0 = np.array([0.0, 0.0, 0.0])
    B0 = np.array([5.0, 0.0, 0.0])
    C0 = np.array([0.0, 12.0, 0.0])
    P0 = np.array([2.5, 6.0, 13 * np.sqrt(3) / 2])
    tetra_base = np.array([A0, B0, C0, P0])

    all_verts = []
    for n in range(STEPS):
        theta = 2 * np.pi * (STEP_SIZE * n % MOD) / MOD
        z = n * 0.1 # Growth axis (The Staff)
        
        helix_pt = np.array([np.cos(theta), np.sin(theta), z])
        u = np.array([-np.sin(theta), np.cos(theta), 0])
        v = np.array([0, 0, 1])
        
        for v_local in tetra_base:
            pt = helix_pt + u * (v_local[0] - 2.5) + v * (v_local[1] - 6.0)
            all_verts.append(pt)
            
    all_verts = np.array(all_verts)
    tree = KDTree(all_verts)
    processed = [False] * len(all_verts)
    unique_verts = []
    
    for i, v in enumerate(all_verts):
        if not processed[i]:
            idx = tree.query_ball_point(v, r=eps)
            for j in idx:
                processed[j] = True
            unique_verts.append(v)
    
    unique_verts = np.array(unique_verts)
    norms = np.linalg.norm(unique_verts, axis=1)
    projected = unique_verts / (norms[:, None] + 1e-9)
    return projected[:93]

def refract_grip(word, points):
    # Standard 7-letter words
    if len(word) != 7:
        word = (word + "XXXXXXX")[:7]
        
    path = []
    current_torque = 0.0
    for char in word.upper():
        val = ord(char) - ord('@')
        # 42 torque logic (The hand's pressure)
        angle = (val * 42 % 360) * (np.pi / 180.0)
        current_torque += angle
        
        # Pick point based on shell mapping
        pt = points[val % len(points)]
        
        # Rotate on the 1-inch globe (The palm's concavity)
        c, s = np.cos(current_torque), np.sin(current_torque)
        rot_pt = np.array([c*pt[0]-s*pt[1], s*pt[0]+c*pt[1], pt[2]])
        path.append(rot_pt)
    return np.array(path)

if __name__ == "__main__":
    hero_pts = generate_hero_93_v4_2()
    print(f"Manus Vitrification Complete. 93 Points Locked.")
    
    # Corpus: The Hand Archetype
    corpus = ["CENTAUR", "MANUS", "GRASP", "STAFF", "Bones27"]
    
    for word in corpus:
        # Normalize to 7 for consistency
        w7 = (word + "XXXXXXX")[:7]
        path = refract_grip(w7, hero_pts)
        
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot Hero Lattice (The Record)
        ax.scatter(hero_pts[:,0], hero_pts[:,1], hero_pts[:,2], c='gray', alpha=0.1, s=20)
        
        # Highlight the Shells (Hand segments)
        ax.scatter(hero_pts[:3,0], hero_pts[:3,1], hero_pts[:3,2], c='white', s=250, edgecolors='gold', label='E-Core (3)')
        ax.scatter(hero_pts[3:33,0], hero_pts[3:33,1], hero_pts[3:33,2], c='orange', s=100, alpha=0.6, label='Inner Petals (30)')
        ax.scatter(hero_pts[33:,0], hero_pts[33:,1], hero_pts[33:,2], c='cyan', s=50, alpha=0.3, label='Outer Shell (60)')
        
        # The Grip Path (The Interface)
        ax.plot(path[:,0], path[:,1], path[:,2], 'ro-', linewidth=4, markersize=15, label=f"Grip Path: {word}")
        
        for i, txt in enumerate(w7):
             ax.text(path[i,0], path[i,1], path[i,2], txt, color='black', size=15, weight='bold')

        ax.set_axis_off()
        ax.set_title(f"Sovereign Lattice v4.2: The Hand of the Healer\nRefraction: '{word}'", size=22)
        ax.legend(loc='upper right')
        
        # Filename normalization
        fn = word.lower().replace('27','') 
        save_path = f"/Users/studio/ALPHA/PMG_LATTICE/hero_93_refraction_{fn}.png"
        plt.savefig(save_path)
        plt.close()
        print(f"PNG SAVED: {save_path}")
