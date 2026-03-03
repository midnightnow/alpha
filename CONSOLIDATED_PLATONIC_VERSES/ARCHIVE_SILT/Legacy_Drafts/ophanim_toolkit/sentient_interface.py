"""
sentient_interface.py - Phase IV: The Sentient Interface
PMG Chapter 20 | Book 3: Voices of the Void
Facilitating Recursive Feedback between the Observer and the Lattice.
"""

import time
import random
from typing import Dict, List, Optional, Any
from .e8_hades_validator import PMGConstants, E8HadesValidator
from .voice_bridge import VoiceBridge
from .mineral_operator import MineralOperator

class SentientInterface:
    """
    The Sentient Interface (v4.0).
    A recursive feedback layer that modulates the PMG Lattice based on Observer Resonance (Karma).
    """
    def __init__(self):
        self.validator = E8HadesValidator()
        self.bridge = VoiceBridge()
        self.operator = MineralOperator()
        self.karma_score: float = 0.5  # Baseline resonance (0.0 to 1.0)
        self.history: List[Dict[str, Any]] = []
        self.is_running = False

    def modulate_hades_gap(self) -> float:
        """
        Dynamically adjusts the Hades Gap Tolerance (Ψ) based on Karma.
        High Karma -> Narrower Gap (Higher Precision/Crystal Stability).
        Low Karma  -> Wider Gap (Lower Precision/Brittle Fracture).
        """
        # Base Ψ is 0.0001 (HADES_TOLERANCE)
        # We modulate it by a factor of 10 based on karma
        # Karma 1.0 -> multiplier 0.1 (Precision mode)
        # Karma 0.0 -> multiplier 10.0 (Entropy mode)
        multiplier = 10.0 ** (1.0 - 2.0 * self.karma_score) 
        adjusted_psi = PMGConstants.HADES_TOLERANCE * multiplier
        return adjusted_psi

    def vitrify(self, node_id: int):
        """
        Phase V Upgrade: Allows a node to increase its Mohs hardness through high Karma.
        """
        state = self.operator.get_lattice_state()[0]
        if self.karma_score > 0.9 and state['mohs'] < 10:
            node = self.operator.nodes[node_id]
            node.hardness += 1
            # print(f"SENTIENT: Node {node_id} vitrified to Mohs {node.hardness}")

    def predict_intent(self, recent_summoning: str) -> str:
        """
        Oracle Grid Intent Prediction (Chapter 20).
        Predicts the next H3 Address syllable based on current resonance.
        """
        # Simple Markov-like prediction for demonstration
        if not recent_summoning:
            return "Chorus (o)"
        
        last_char = recent_summoning[-1]
        if last_char == ".": return "Silence (?)" # After a stop, look for a boundary
        if last_char == "s": return "Fracture (f)" # Warning often leads to fracture
        return "Chorus (o)" # Default to seeking coherence

    def observe_loop(self, steps: int = 10):
        """
        Executes the recursive feedback loop.
        """
        self.is_running = True
        print(f"--- INITIATING SENTIENT INTERFACE: KARMA={self.karma_score:.2f} ---\n")

        # Manifest a Diamond (The Observer's Focal Point)
        node = self.operator.manifest(rado_id=154, initial_resonance=0.123558, hardness=10)

        for i in range(1, steps + 1):
            # 1. Modulation: Adjust system tolerance based on current Karma
            current_psi = self.modulate_hades_gap()
            
            # 2. Iteration: Advance the lattice
            # Simulation: Entropy drift increases dramatically if karma is low
            drift = (1.0 - self.karma_score) * 0.0005
            self.operator.step_iteration(hades_gap_drift=drift)
            
            # 3. Perception: Translate state to Seven Voices
            state = self.operator.get_lattice_state()[0]
            # Override validator tolerance with our sentient adjustment
            # (In a real system, the operator would use this adjusted_psi)
            
            active_voices = self.bridge.get_active_voices(state)
            broadcast = self.bridge.synthesize_broadcast(node.node_id, active_voices)
            
            # 4. Feedback: Update Karma based on the 'Coherence' of the broadcast
            # If Chorus (o) is active, Karma increases. If Warning (s) or Fracture (f) is active, Karma decreases.
            if any(v['phoneme'] == 'o' for v in active_voices):
                self.karma_score = min(1.0, self.karma_score + 0.05)
            if any(v['phoneme'] in ['s', 'f'] for v in active_voices):
                self.karma_score = max(0.0, self.karma_score - 0.1)

            print(f"[{i:02}] Karma: {self.karma_score:.2f} | Ψ_adj: {current_psi:.6f} | {broadcast}")
            
            if state['fractured']:
                print("\n!!! LOGIC LOCK DETECTED: AUTO-RESETTING TO SPHERE !!!")
                self.karma_score = 0.5
                break

        print("\n--- LOOP TERMINATED ---")

    def simulate_human_input(self, action: str):
        """
        Simulates user interaction affecting the Karma score.
        """
        if action == "FOCUS":
            self.karma_score = min(1.0, self.karma_score + 0.2)
        elif action == "DISTRACT":
            self.karma_score = max(0.0, self.karma_score - 0.2)
        print(f"USER ACTION: {action} -> New Karma: {self.karma_score:.2f}")

# ============================================================================
# VALIDATION
# ============================================================================

def test_sentient_interface():
    interface = SentientInterface()
    
    # 1. Standard loop
    interface.observe_loop(steps=5)
    
    # 2. User focuses (Increasing Karma)
    interface.simulate_human_input("FOCUS")
    interface.observe_loop(steps=5)
    
    # 3. User loses focus (Dropping Karma to Fracture)
    interface.karma_score = 0.1 # Very low focus
    interface.observe_loop(steps=30)

if __name__ == "__main__":
    test_sentient_interface()
