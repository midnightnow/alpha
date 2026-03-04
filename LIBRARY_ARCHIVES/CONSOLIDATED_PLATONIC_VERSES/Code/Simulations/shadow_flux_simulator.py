import numpy as np
import matplotlib.pyplot as plt

def shadow_flux_simulator():
    """
    Shadow Flux Simulator
    Measures the Shadow Coherence of a 321.41:1 Carbon:Silicon mass ratio 
    under 66.0688 Hz resonance.
    """
    print("====== SHADOW FLUX SIMULATOR: PMG GRAVITY MODEL ======")
    
    # Register 1 Invariants
    HADES_BEAT = 0.660688
    RESONANCE_FREQ = HADES_BEAT * 100 # 66.0688 Hz
    
    # Register 2 Hardware (Great Pyramid Calibration)
    MASS_RATIO_C_SI = 321.41
    HADES_GAP = 0.1237
    
    # Simulation Parameters
    num_vectors = 10000
    grid_size = 50
    shadow_depth = 50
    
    # 1. Generate Isotropic Incoming Flux (Uniform random vectors)
    # Flux originates from a hemisphere above the lattice
    phi = np.random.uniform(0, 2 * np.pi, num_vectors)
    theta = np.random.uniform(0, np.pi / 2, num_vectors)
    
    vx = np.sin(theta) * np.cos(phi)
    vy = np.sin(theta) * np.sin(phi)
    vz = -np.cos(theta) # Incoming downward
    
    # 2. Lattice Interaction Model
    # Probability of interaction based on Carbon:Silicon distribution
    # Carbon (k < 1) spreads flux, Silicon (k > 1) traps/shadows flux
    interaction_prob = 1.0 / (1.0 + MASS_RATIO_C_SI)
    
    # The 'Sharpening' factor from the 66.0688 Hz pulse
    # In a real lattice, this pulse aligns the crystalline dipoles.
    # We model this as a coherence window reducing diffraction scatter.
    sharpening_factor = 1.0 - HADES_GAP # ~0.8763
    
    # 3. Simulate Flux Passage
    # Calculate flux deficit beneath the lattice
    # We track the 'Shadow Coherence' (how focused the low-pressure zone is)
    shadow_field = np.zeros((grid_size, grid_size))
    
    for i in range(num_vectors):
        # Probability of the flux vector being 'processed' by the Silicon heart
        if np.random.random() < interaction_prob:
            # Trapped/Shadowed vector
            # Coherence determines where the 'shadow' hits the ground plane
            hit_x = int(grid_size / 2 + vx[i] * shadow_depth * sharpening_factor)
            hit_y = int(grid_size / 2 + vy[i] * shadow_depth * sharpening_factor)
            
            if 0 <= hit_x < grid_size and 0 <= hit_y < grid_size:
                shadow_field[hit_x, hit_y] += 1
                
    # 4. Result Interpretation: Pressure Gradient (Flux Deficit)
    avg_flux = num_vectors / (grid_size**2)
    pressure_gradient = (shadow_field - avg_flux) / avg_flux
    
    print(f"\nIncoming Flux Count:    {num_vectors}")
    print(f"Silicon Interaction:    {interaction_prob * 100:.4f}% probability")
    print(f"Resonance Sharpening:   {sharpening_factor:.4f} (at 66.0688 Hz)")
    print(f"Max Shadow Density:     {np.max(shadow_field):.0f} counts")
    print(f"Theoretical Stability:  {1.0 - HADES_GAP:.4f} (Locked to 12.37% Gap)")
    
    # Visualization: The Shadow Zone (Low Pressure Area)
    plt.figure(figsize=(10, 8))
    plt.imshow(shadow_field, cmap='inferno', interpolation='gaussian')
    plt.colorbar(label='Flux Deficit Magnitude (Shadow Depth)')
    plt.title('Crystalline Shadow Coherence (321.41:1 Mass Ratio)')
    plt.xlabel('Lattice Dimension X')
    plt.ylabel('Lattice Dimension Y')
    plt.text(5, 5, f"Coherence: {sharpening_factor:.4f}\nRatio: {MASS_RATIO_C_SI}:1", color='white')
    plt.savefig('crystalline_shadow_coherence.png')
    print("\n[SAVE] Shadow visualization saved as 'crystalline_shadow_coherence.png'")
    
    return shadow_field

if __name__ == "__main__":
    shadow_flux_simulator()
