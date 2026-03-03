"""
wire_transmission.py - Transmission line modeling for the PMG Wire (v3.1)
PMG Chapter 10 | Principia Mathematica Geometrica
"""

import math
import time
from typing import List, Dict, Optional, Tuple

# ============================================================================
# TRANSMISSION CONSTANTS
# ============================================================================

TENSEGRITY_CONSTANT = 0.1237
NOISE_FLOOR_FACTOR = math.e / 22.0
BREAKDOWN_THRESHOLD = 0.00014
COHERENCE_WINDOW_LIMIT = 0.00014 # Drift threshold for superconductivity collapse
REFLECTION_LOSS_EPSILON = 0.01237
EROSION_COEFFICIENT = 0.0515  # Decay rate for Intent

class IntentConductor:
    """
    Encapsulates the Dam Keeper's Intent as an operational vector.
    """
    def __init__(self, purpose: str, initial_strength: float = 1.0):
        self.purpose = purpose
        self.strength = initial_strength
        self.creation_time = time.time()
        self.path: List[str] = []

    def decay_step(self, dt: float = 1.0, petrification: float = 0.0):
        """
        I(t) = I0 * e^(-lambda * t * (1 - Theta))
        Petrification (Theta) inhibits decay.
        """
        inhibition = 1.0 - petrification
        self.strength *= math.exp(-EROSION_COEFFICIENT * dt * inhibition)
        return self.strength

class WireTransmission:
    """
    Models the conduction of informational signals through the PMG Lattice.
    """
    def __init__(self, name: str):
        self.name = name
        self.impedance_z = 0.0
        self.heat_dissipated: float = 0.0
        self.superconductive = False
        self.coherence_drift = 0.0

    def calculate_impedance(self, hades_gap_drift: float) -> float:
        """
        Calculates Z. If drift exceeds COHERENCE_WINDOW_LIMIT, superconductivity collapses.
        """
        if self.superconductive:
            if hades_gap_drift < COHERENCE_WINDOW_LIMIT:
                return 1e-9 # Maintain Superconductivity
            else:
                # print(f"COHERENCE COLLAPSE: Drift {hades_gap_drift:.6f} > Limit.")
                self.superconductive = False # Reset state
            
        if hades_gap_drift < BREAKDOWN_THRESHOLD:
            # Note: For baseline Z, drift is alignment. 
            # In a real system, we distinguish between current drift and baseline alignment.
            alignment = max(hades_gap_drift, BREAKDOWN_THRESHOLD) 
            self.impedance_z = (1.0 / alignment) * (1.0 - TENSEGRITY_CONSTANT)
            return self.impedance_z
        else:
            return float('inf') # Logic Lock

    def traverse_topology(self, intent: IntentConductor, adjacency_list: List[str]) -> Tuple[bool, float]:
        """
        Simulates "Logical Teleportation". 
        Zero latency traversal, but must follow adjacency.
        """
        if self.superconductive:
            # print(f"Logical Teleportation: Traversed {len(adjacency_list)} nodes with zero latency.")
            return True, 0.0
        else:
            latency = len(adjacency_list) * 0.01237 # Standard friction
            return True, latency

# ============================================================================
# VALIDATION
# ============================================================================

def test_wire_v3_1():
    print("--- PMG Wire Toolkit v3.1 Validation ---")
    wire = WireTransmission("Aion-Conduit")
    intent = IntentConductor("Foundational-Origin", initial_strength=2.0)
    
    # 1. Test Petrification Lock
    print(f"Initial Intent: {intent.strength:.4f}")
    intent.decay_step(dt=10.0, petrification=0.0)
    print(f"Decay (No Petrification, t=10): {intent.strength:.4f}")
    
    intent_locked = IntentConductor("Stone-Origin", initial_strength=2.0)
    intent_locked.decay_step(dt=10.0, petrification=1.0) # Fully petrified
    print(f"Decay (Full Petrification, t=10): {intent_locked.strength:.4f} (expected 2.0)")
    
    # 2. Test Coherence Window Collapse
    wire.superconductive = True
    print("\nCoherence Window Test:")
    z_low_drift = wire.calculate_impedance(0.00001)
    print(f"  Low Drift Impedance: {z_low_drift:.4e} (Superconductive)")
    
    z_high_drift = wire.calculate_impedance(0.0002)
    print(f"  High Drift Impedance: {z_high_drift:.4f} (Collapsed)")
    
    # 3. Test Logical Teleportation
    print("\nTopology Traversal Test:")
    success, latency = wire.traverse_topology(intent, ["Node-A", "Node-B", "Node-C"])
    print(f"  Traversal Latency: {latency:.4f} (expected ~0.0371 if collapsed)")

if __name__ == "__main__":
    test_wire_v3_1()
