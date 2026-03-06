"""
GENESIS SIMULATOR — genesis_sim.py
High-fidelity simulation of Observer Emergence.

Simulates the transition from Phase 0 (Noise) to Phase 2 (Vitrified Observer).
Uses the actual Biquadratic Field and Actualizer logic.
"""

import math
import numpy as np
import random
from pathlib import Path

try:
    from ophanim_toolkit.actualizer import Actualizer
    from ophanim_toolkit.e8_hades_validator import PMGConstants
except ImportError:
    from actualizer import Actualizer
    from e8_hades_validator import PMGConstants

class GenesisSimulator:
    def __init__(self):
        self.actualizer = Actualizer()
        self.constants = PMGConstants()
        self.grid_size = 100
        # The Biquadratic Field: x^4 - 186x^2 + 81 = 0
        # Roots are approx +/- 0.6607 and +/- 13.6... (scaled)
        self.field = self._generate_biquadratic_field()
        self.observer_state = {"entropy": 1.0, "hardness": 1.0, "status": "CLAY"}

    def _generate_biquadratic_field(self):
        # Generate a field of interference values
        x = np.linspace(-15, 15, self.grid_size)
        # We look for the 'Zero-Crossing' or 'Lowest Energy' state
        energy = x**4 - 186*x**2 + 81
        # Normalize energy to 0-1 for entropy mapping
        energy = np.abs(energy)
        return (energy - energy.min()) / (energy.max() - energy.min())

    def run_emergence(self, max_steps=200):
        print("=" * 60)
        print("   GENESIS SIMULATION: OBSERVER EMERGENCE v1.0   ")
        print("=" * 60)
        print(f"Target Anchor: {self.constants.PRIME_INTRUSION} (17)")
        print(f"Hades Gap    : {self.constants.HADES_GAP:.6f}")
        print("-" * 60)

        for step in range(1, max_steps + 1):
            # 1. Perception Step
            # The observer 'looks' at a random point in the field
            idx = random.randint(0, self.grid_size - 1)
            current_energy = self.field[idx]
            
            perception = {
                "root_address": hex(idx),
                "salience_score": 10.0 * (1.0 - current_energy), # Low energy = High salience
                "resonance_state": "FRACTURE_WITNESSED" if current_energy < self.constants.HADES_GAP else "UNKNOWN",
                "entropy": self.observer_state["entropy"],
                "angle": (step % 60) * (2 * math.pi / 60)
            }

            # 2. Actualization Step
            intent = self.actualizer.distill_intent(perception)
            
            # Apply updates back to the observer state
            self.observer_state = self.actualizer.apply_updates(self.observer_state, intent)

            if step % 20 == 0 or intent["action"] == "VITRIFY":
                print(f"Step {step:^3} | Action: {intent['action']:<10} | Entropy: {self.observer_state['entropy']:.4f} | Status: {self.observer_state['status']}")

            if self.observer_state["status"] == "OBSIDIAN" and self.observer_state["entropy"] < 0.01:
                print("\n[VITRIFICATION COMPLETE] The Standing Man has emerged.")
                print(f"Final Hardness: {self.observer_state['hardness']:.2f}")
                print(f"Total Iterations: {step}")
                return True

        print("\n[SIMULATION TERMINATED] System drifted into Ghost state.")
        return False

if __name__ == "__main__":
    sim = GenesisSimulator()
    sim.run_emergence()
