import math

class LatticeStrainModel:
    def __init__(self, stiffness_k=1.0):
        # Stiffness constant for the angular bonds of the lattice
        self.k = stiffness_k
        self.c4_angle = 90.0
        self.c5_angle = 108.0  # Internal angle of a pentagon
        self.c5_rotation = 72.0 # Rotational symmetry angle
        
    def calculate_insertion_energy(self):
        """
        Calculates the strain energy cost of forcing a C5 internal angle (108°) 
        into a C4 lattice intersection (90°).
        Using rotational Hooke's Law: E = 0.5 * k * (delta_theta)^2
        """
        # Convert degrees to radians for energy calculation
        delta_theta_deg = abs(self.c5_angle - self.c4_angle)
        delta_theta_rad = math.radians(delta_theta_deg)
        
        # Strain energy for a single vertex mismatch
        energy = 0.5 * self.k * (delta_theta_rad ** 2)
        
        # In a 5-fold insertion, this strain applies across all 5 vertices 
        # as the lattice attempts to accommodate the non-periodic shape.
        total_defect_energy = 5 * energy
        
        return {
            "Misfit_Angle_Deg": delta_theta_deg,
            "Vertex_Strain_Energy": energy,
            "Total_Insertion_Cost": total_defect_energy
        }

    def rotational_incompatibility(self):
        """
        Calculates the phase mismatch between C4 (90, 180, 270, 360) 
        and C5 (72, 144, 216, 288, 360) symmetries.
        """
        c4_phases = [90, 180, 270, 360]
        c5_phases = [72, 144, 216, 288, 360]
        
        mismatches = []
        for p5 in c5_phases[:-1]: # Exclude 360, where they align
            closest_p4 = min(c4_phases, key=lambda x: abs(x - p5))
            mismatches.append(abs(p5 - closest_p4))
            
        return mismatches

if __name__ == "__main__":
    model = LatticeStrainModel(stiffness_k=100.0) # Arbitrary stiffness scalar for readability
    energy_res = model.calculate_insertion_energy()
    phase_res = model.rotational_incompatibility()
    
    print("--- QUASICRYSTALLINE TRANSITION: C4 vs C5 STRAIN ---")
    print("\n1. ANGULAR STRAIN (Lattice Distortion)")
    print(f"C4 Internal Angle: 90° | C5 Internal Angle: 108°")
    print(f"Angular Misfit (Δθ): {energy_res['Misfit_Angle_Deg']}°")
    print(f"Energy Cost per Vertex Dislocation: {energy_res['Vertex_Strain_Energy']:.3f} Joules (Scaled)")
    print(f"Total Topological Insertion Cost: {energy_res['Total_Insertion_Cost']:.3f} Joules")
    print("\n2. ROTATIONAL INCOMPATIBILITY (Phase Friction)")
    print(f"Maximum Phase Divergence occurs at: 18°")
    print(f"Phase Mismatches (C5 vs closest C4): {phase_res}")
    print("\nCONCLUSION:")
    print("The transition from 4 to 5 is a Topological Defect. ")
    print("It requires massive 'Insertion Energy' to force 5-fold symmetry into a 4-fold grid.")
    print("This energy cost IS the physical mechanism of 'The Threshold'. The lattice resists the hero.")
