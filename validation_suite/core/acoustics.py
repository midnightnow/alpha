import math

class AcousticModel:
    def __init__(self, constants):
        self.psi = constants["PSI"]
        self.root42 = constants["ROOT_42"]
        self.root51 = constants["ROOT_51"]

    def calculate_resonance(self, volume):
        # Helmholtz-like frequency based on Psi as the neck/gap
        # f = (v/2pi) * sqrt(A/(L*V))
        # Symbolic approximation for the Sovereign Lattice:
        v_sound = 343.0 # m/s
        # Scale volume to human torso / pyramid chamber
        return (v_sound / (2 * math.pi)) * math.sqrt(self.psi / volume)

    def get_letter_frequency(self, node_index):
        # Frequency mapping derived from the 171 spiral
        # Simplified: Base frequency shifted by node index
        base = 432.0 # Universal tuning
        return base + (node_index * self.root42)
