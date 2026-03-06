import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import csv

def generate_hero_points(steps=120, tol=0.45):
    STEP_SIZE = 5
    MOD = 24
    apex_height = 13 * np.sqrt(3) / 2
    
    all_verts = []
    for n in range(steps):
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
            v = helix_pt + offset
            all_verts.append(v)

    all_verts = np.array(all_verts)
    tree = KDTree(all_verts)
    processed = [False] * len(all_verts)
    unique_verts = []
    
    for i, v in enumerate(all_verts):
        if not processed[i]:
            idx = tree.query_ball_point(v, r=tol)
            for j in idx:
                processed[j] = True
            unique_verts.append(v)
    
    unique_verts = np.array(unique_verts)
    norms = np.linalg.norm(unique_verts, axis=1)
    projected = unique_verts / (norms[:, None] + 1e-9)
    return projected

def sensitivity_test():
    results = {}
    for eps in [0.4, 0.45, 0.5, 0.55]:
        pts = generate_hero_points(steps=120, tol=eps)
        results[eps] = len(pts)
    return results

def step_count_test():
    # 120 (Cycle) vs 52 (Biological Year)
    res_120 = len(generate_hero_points(steps=120))
    res_52 = len(generate_hero_points(steps=52))
    return res_120, res_52

def refract_corpus(corpus, points):
    corpus_results = {}
    for word in corpus:
        word_padded = (word + "XXXXXXX")[:7]
        path = []
        current_torque = 0.0
        for char in word_padded.upper():
            val = ord(char) - ord('@')
            angle = (val * 42 % 360) * (np.pi / 180.0)
            current_torque += angle
            idx = (val * 13) % len(points)
            pt = points[idx]
            c, s = np.cos(current_torque), np.sin(current_torque)
            rot_pt = np.array([c*pt[0]-s*pt[1], s*pt[0]+c*pt[1], pt[2]])
            path.append(rot_pt)
        corpus_results[word] = np.array(path)
    return corpus_results

if __name__ == "__main__":
    # 1. Sensitivity
    s_results = sensitivity_test()
    print(f"P1 SENSITIVITY TEST: {s_results}")
    
    # 2. Step Comparison
    c120, c52 = step_count_test()
    print(f"P1 STEP COMPARISON: 120 steps -> {c120}, 52 steps -> {c52}")
    
    # 3. Points Generation & CSV Export
    hero_93 = generate_hero_points(steps=120)[:93]
    with open('/Users/studio/ALPHA/PMG_LATTICE/hero_93_coordinates.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['X', 'Y', 'Z'])
        writer.writerows(hero_93)
    print("CSV EXPORTED: hero_93_coordinates.csv")
    
    # 4. Corpus Refraction
    corpus = ["PYTHON", "APOLLO", "CHIRON", "CENTAUR", "VIPERA", "ASP", "ROSE"]
    refractions = refract_corpus(corpus, hero_93)
    print("CORPUS REFRACTED")

    # 5. Consolidated Visualisation (Rose)
    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Shell Colors: White (Core), Orange (Inner), Cyan (Outer)
    ax.scatter(hero_93[:3,0], hero_93[:3,1], hero_93[:3,2], c='white', s=250, edgecolors='gold', label='E-Core (3)')
    ax.scatter(hero_93[3:33,0], hero_93[3:33,1], hero_93[3:33,2], c='orange', s=100, alpha=0.6, label='Inner Petals (30)')
    ax.scatter(hero_93[33:,0], hero_93[33:,1], hero_93[33:,2], c='cyan', s=50, alpha=0.3, label='Outer Petals (60)')
    
    # Mapping the word ROSE as the primary 7-beat ride
    rose_path = refractions["ROSE"]
    ax.plot(rose_path[:,0], rose_path[:,1], rose_path[:,2], color='crimson', linewidth=4, marker='o', markersize=12, label='Rider: ROSE')
    for i, char in enumerate("ROSEX"): # Padded logic
        if i < len("ROSE"):
            ax.text(rose_path[i,0], rose_path[i,1], rose_path[i,2], char, size=18, weight='extra bold', color='darkred')

    ax.set_title("HERO 93 P1 DIAGNOSTIC: The Rose Refraction\nShell Mapping: 3-30-60", size=22, weight='bold')
    ax.set_axis_off()
    ax.legend(prop={'size': 12})
    
    plt.savefig("/Users/studio/ALPHA/PMG_LATTICE/hero_93_p1_diagnostic.png")
    print("DIAGNOSTIC VISUALIZATION SAVED: hero_93_p1_diagnostic.png")
