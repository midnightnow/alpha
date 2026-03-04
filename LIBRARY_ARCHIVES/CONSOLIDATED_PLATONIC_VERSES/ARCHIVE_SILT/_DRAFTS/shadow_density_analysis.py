import numpy as np
import matplotlib.pyplot as plt

def calculate_shadow_density():
    """
    Calculates the 'Shadow Density' (Diffraction Deficit) for:
    1. Titan (10-node equilateral triangle/fractal)
    2. Human (13-node stellate projection)
    """
    
    # Constants
    Pu = 1.0  # Normalized Isometric Flux
    k = 0.1237 # Hades Gap (Inherent Leakage)
    
    # 1. Titan (10 nodes)
    # Perfectly ordered, low diffraction noise
    titan_nodes = 10
    titan_coherence = 0.999 # High coherence due to symmetry
    titan_shadow_density = Pu * (1 - titan_coherence) # Minimal shadow
    
    # 2. Human (13 nodes)
    # Stellate projection, higher 'Wait' (informational complexity)
    human_nodes = 13
    # Wait = Weight. The 13 nodes introduce the 12.37% gap more aggressively
    human_coherence = 1.0 - k # Shadow density directly scales with the Hades Gap
    human_shadow_density = Pu * (1 - human_coherence)
    
    # Ratio Calculation
    shadow_ratio = human_shadow_density / titan_shadow_density if titan_shadow_density > 0 else float('inf')
    
    print("--- Shadow Density Analysis ---")
    print(f"Titan (10 Nodes) Shadow Density: {titan_shadow_density:.6f}")
    print(f"Human (13 Nodes) Shadow Density: {human_shadow_density:.6f}")
    print(f"Shadow Density Ratio (Human/Titan): {shadow_ratio:.2f}x")
    print("\nInterpretation:")
    print("The Human 13-node projection generates 123x more 'Gravity' (Shadow) than the Titan 10-node ideal.")
    print("This explains why 'Life' (13) is heavier than 'Ideal Geometry' (10).")

    # Visualizing the Shadow Profile
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Titan Shadow (Perfectly balanced circle/triangle)
    titan_profile = 0.1 * np.ones_like(theta)
    
    # Human Shadow (Stellate/Star-shaped)
    # Using a 5-pointed star (Register 2/3) influenced by prime 13 tension
    human_profile = 0.1237 * (1 + 0.5 * np.sin(5 * theta))
    
    plt.figure(figsize=(10, 6))
    plt.plot(theta, titan_profile, label='Titan (10-node) Stable Slurry', color='cyan', linestyle='--')
    plt.fill_between(theta, 0, human_profile, label='Human (13-node) Stellate Shadow', color='red', alpha=0.3)
    plt.title("Shadow Density Profile: Titan vs. Human")
    plt.xlabel("Phase (24-Modulus substrate)")
    plt.ylabel("Shadow Depth (Flux Deficit)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    # plt.show() # Can't show, but calculating
    plt.savefig("/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES/shadow_density_comparison.png")
    print("\nVisual profile saved to: shadow_density_comparison.png")

if __name__ == "__main__":
    calculate_shadow_density()
