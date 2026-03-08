import numpy as np
import matplotlib.pyplot as plt

class BreathDebtSimulator:
    """
    Models the "Breath Debt" and "Envelope Integrity" of the Sovereign Lattice.
    Based on the PMG framework (Kar/Action vs Ma/Mass).
    """
    
    HADES_GAP = 0.1237  # 12.37% failure threshold
    OPTIMAL_COHERENCE = 0.50  # 50% is a coherent solid
    
    def __init__(self, label="Simulation"):
        self.label = label
        self.co2_accum = 0.0  # Normalized Carbon/Debt/Wait
        self.integrity = self.OPTIMAL_COHERENCE
        self.history = []
        self.steps = 0
        
    def step(self, pulse):
        """
        Processes a single step/breath.
        pulse: 1 for "Go" (Inhale/Alkalinizing), 0 for "Stop" (Hold/Exhaling structure/Acidifying)
        """
        self.steps += 1
        
        # Go (1): Intake of fresh count, releases Weight (Weight Release / Hyperventilation risk)
        if pulse == 1:
            # Releasing debt through action
            drift = -0.02  # Alkalinizing effect
        else:
            # Stop (0): Structural stabilization, accumulating Wait/Weight (Acidification risk)
            drift = 0.02   # Acidifying effect
            
        self.co2_accum += drift
        
        # Envelope Integrity Calculation
        # Integrity is a measure of geometric coherence.
        # Deviation from 0.0 (equilibrium) affects the integrity.
        # We model the pH drift as the absolute value of accumulation.
        ph_drift = abs(self.co2_accum)
        
        if ph_drift > self.HADES_GAP:
            # Hades Gap breached: Shear failure begins
            # Integrity drops exponentially or linearly beyond the gap
            penalty = (ph_drift - self.HADES_GAP) * 5.0
            self.integrity -= penalty
        else:
            # Homeostasis: Small debts absorbed by the 12.37% buffer
            # Slight recovery toward optimal coherence
            recovery = 0.01 * (1.1237 - ph_drift)
            if self.integrity < self.OPTIMAL_COHERENCE:
                self.integrity += recovery
            elif self.integrity > self.OPTIMAL_COHERENCE:
                 self.integrity -= recovery # Pull back from vitrification
                 
        # Clamp integrity
        self.integrity = max(0.0, min(1.0, self.integrity))
        
        self.history.append({
            "step": self.steps,
            "co2": self.co2_accum,
            "ph_drift": ph_drift,
            "integrity": self.integrity,
            "state": "SLURRY" if self.co2_accum > self.HADES_GAP else ("VITRIFIED" if self.co2_accum < -self.HADES_GAP else "COHERENT")
        })

def run_comparison():
    # 1. 3x3 Rhythm (Scrubbing Protocol)
    # Balanced 3 Go, 3 Stop
    sim_3x3 = BreathDebtSimulator("3x3 Rhythm")
    for _ in range(20): # 120 steps total
        for _ in range(3): sim_3x3.step(1)
        for _ in range(3): sim_3x3.step(0)
        
    # 2. 4x4 Rhythm (Structural Stagnation?)
    # Also balanced, but longer "holds"
    sim_4x4 = BreathDebtSimulator("4x4 Rhythm")
    for _ in range(15):
        for _ in range(4): sim_4x4.step(1)
        for _ in range(4): sim_4x4.step(0)
        
    # 3. "Held Breath" (Debt Accumulation)
    # 1 Inhale, 5 Holds/Stop
    sim_debt = BreathDebtSimulator("Stall / Debt Accumulation")
    for _ in range(120):
        if _ % 6 == 0:
            sim_debt.step(1) # Occasional inhale
        else:
            sim_debt.step(0) # Sustained hold
            
    # Print results
    for sim in [sim_3x3, sim_4x4, sim_debt]:
        last = sim.history[-1]
        print(f"--- {sim.label} ---")
        print(f"Steps: {sim.steps}, Final CO2: {last['co2']:.4f}, Final Integrity: {last['integrity']:.4%}")
        print(f"State: {last['state']}")
        print()

if __name__ == "__main__":
    run_comparison()
