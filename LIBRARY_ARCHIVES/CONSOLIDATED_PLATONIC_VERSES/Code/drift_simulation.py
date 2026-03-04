import numpy as np
import matplotlib.pyplot as plt

def run_drift_simulation(iterations=1000, noise_floor=0.01237):
    """
    Models the iterative 'aliasing' of the 10-24-26 right-angle triangle.
    Each iteration simulates one generation of 'Culture' or 'Implementation',
    injecting noise into the coordinates.
    """
    # Pure Invariant (Register 1)
    # A = (0,0), B = (10,0), C = (0,24)
    # Hypotenuse AC = sqrt(10^2 + 24^2) = 26
    
    base_coords = np.array([[0, 0], [10, 0], [0, 24]], dtype=float)
    current_coords = base_coords.copy()
    
    drifts = []
    angle_deviations = []
    
    for i in range(iterations):
        # Inject bounded noise factor (Register 2 Noise Floor)
        noise = np.random.uniform(-noise_floor, noise_floor, size=base_coords.shape)
        current_coords += noise
        
        # Calculate the 'Shear' of the right angle (Angle at B)
        # Vector BA = A - B, Vector BC = C - B
        ba = current_coords[0] - current_coords[1]
        bc = current_coords[2] - current_coords[1]
        
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
        
        angle_deviations.append(abs(90.0 - angle))
        
        # Calculate the cumulative 'Silt' (Distance from Invariant)
        silt = np.linalg.norm(current_coords - base_coords)
        drifts.append(silt)

    # Plotting the results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    ax1.plot(drifts, color='brown', label='Cumulative Silt (Drift)')
    ax1.set_title('Integration of Implementation Noise (The Silt)')
    ax1.set_ylabel('Absolute Distance from Invariant')
    ax1.legend()
    
    ax2.plot(angle_deviations, color='blue', label='Angular Shear (Quantization Error)')
    ax2.set_title('Aliasing of the Right Angle (10-24-26)')
    ax2.set_ylabel('Degrees from 90°')
    ax2.set_xlabel('Generations (Culture)')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('drift_simulation_results.png')
    
    final_shear = np.mean(angle_deviations)
    print(f"Simulation Complete over {iterations} generations.")
    print(f"Noise Floor (Hades Gap): {noise_floor * 100:.3f}%")
    print(f"Average Angular Shear: {final_shear:.4f} degrees")
    print(f"Residue (Silt) integrated. The 'Ground' has been established.")

if __name__ == "__main__":
    run_drift_simulation()
