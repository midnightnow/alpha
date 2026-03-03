import numpy as np
import matplotlib.pyplot as plt

def plot_the_flower_of_petals():
    """
    Plots the "Flower of the 13th Petal" where each petal is a 5:12:13 triangle
    scaled such that its circumradius squared (R^2) is an integer m.
    """
    # Base triangle ratios
    ratio_a = 5
    ratio_b = 12
    ratio_c = 13
    
    # R^2 values to plot
    # m=169 is the 10-24-26 visible petal
    # m=171 is the invisible petal
    # m=42 is near the 5-12-13 seed
    m_values = [42, 169, 171, 338, 676]
    labels = ["Near Seed (m=42)", "Visible (m=169)", "Invisible (m=171)", "Doubled (m=338)", "Visible 2 (m=676)"]
    colors = ['gray', 'blue', 'red', 'green', 'purple']
    
    plt.figure(figsize=(10, 10))
    
    # Plot a representation of each triangle as a petal on the flower
    for i, m in enumerate(m_values):
        k = 2 * np.sqrt(m) / ratio_c
        a = ratio_a * k
        b = ratio_b * k
        c = ratio_c * k
        
        # Coordinates for plotting (petal-like orientation)
        angle = (360 / len(m_values)) * i
        theta = np.radians(angle)
        
        # Rotation matrix
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        
        # Triangle vertices in local space
        tri_pts = np.array([[0, 0], [a, 0], [0, b], [0, 0]])
        
        # Rotate and plot
        rot_pts = tri_pts @ rot.T
        
        plt.plot(rot_pts[:, 0], rot_pts[:, 1], color=colors[i], label=f"{labels[i]} (k={k:.3f})")
        plt.fill(rot_pts[:, 0], rot_pts[:, 1], color=colors[i], alpha=0.1)
        
    # Circumcircle of the m=171 petal
    R_171 = np.sqrt(171)
    circle = plt.Circle((0, 0), R_171, color='red', fill=False, linestyle='--', label="R^2 = 171 Threshold")
    plt.gca().add_artist(circle)

    plt.axhline(0, color='black', alpha=0.3)
    plt.axvline(0, color='black', alpha=0.3)
    plt.setp(plt.gca(), aspect='equal')
    plt.title("The Flower of the 13th Petal (5:12:13 scaled by R^2=m)")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    plt.savefig("/Users/studio/Sovereign/0platonicverses/PMG_PUBLICATION_v1.0/THE_FLOWER_OF_PETALS.png")
    print("Visual diagnostic saved to PMG_PUBLICATION_v1.0/THE_FLOWER_OF_PETALS.png")

if __name__ == "__main__":
    plot_the_flower_of_petals()
