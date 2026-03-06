import math

def compute_metabolic_efficiency(input_energy):
    """
    Calculates metabolic efficiency target based on the 12.37% Hades Gap.
    Theoretical Maximum Efficiency = 100% - Ψ
    """
    psi = 0.12367
    max_efficiency = 1.0 - psi
    actual_metabolic_work = input_energy * max_efficiency
    heat_loss = input_energy * psi
    return actual_metabolic_work, heat_loss

if __name__ == "__main__":
    energy = 1000 # units
    work, heat = compute_metabolic_efficiency(energy)
    print(f"Metabolic Work: {work}")
    print(f"Mandatory Heat Loss (Psi): {heat}")
    assert abs(heat/energy - 0.12367) < 0.0001
