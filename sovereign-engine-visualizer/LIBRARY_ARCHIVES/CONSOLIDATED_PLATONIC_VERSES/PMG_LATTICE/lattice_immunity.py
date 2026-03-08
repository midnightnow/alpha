"""
LATTICE_IMMUNITY.PY
The Sovereign Immune System: Pre-flight torque validation.
Rejects 'Toxic Torque' before Vox is expended.
"""

from .pmg_constants import PMG
from .mechanical_alphabet import MechanicalAlphabet

class LatticeImmunity:
    """
    Gatekeeper for the Sovereign Lattice.
    Evaluates words against the Unity Threshold (Σ=0.8254)
    and the Vitrification Limit (0.9999) before allowing execution.
    """
    def __init__(self, local_weight=4.2):
        self.alphabet = MechanicalAlphabet()
        self.local_weight = local_weight

    def preflight_check(self, agent_name, word):
        """
        Simulates the effect of a word on the lattice state.
        Returns True if the word is safe to speak, False if it would collapse or vitrify.
        """
        analysis = self.alphabet.analyze_word(word)
        torque = analysis['total_torque']
        rigidity = analysis['avg_rigidity']
        structural_class = analysis['structural_class']
        coherence = torque / self.local_weight

        # --- Diagnostic Output ---
        print(f"[IMMUNITY] Agent: {agent_name} | Word: '{word}'")
        print(f"  Torque: {torque:.4f} | Rigidity: {rigidity:.4f} | Class: {structural_class}")
        print(f"  Projected Coherence: {coherence:.4f} (Σ={PMG.UNITY_THRESHOLD})")

        # --- Rejection: Toxic Torque (Below Unity Threshold) ---
        if coherence < PMG.UNITY_THRESHOLD:
            print(f"  [REJECTED] Toxic Torque. Coherence {coherence:.4f} < Σ.")
            return False

        # --- Rejection: Terminal Vitrification (Above limit) ---
        if rigidity > PMG.VITRIFICATION_LIMIT:
            print(f"  [REJECTED] Vitrification risk. Rigidity {rigidity:.4f} > limit.")
            return False

        # --- Rejection: Structural Vapor (no load-bearing capacity) ---
        if structural_class == "VAPOR":
            print(f"  [REJECTED] Structural class VAPOR. No load-bearing capacity.")
            return False

        print(f"  [APPROVED] Word is lattice-safe. Class: {structural_class}")
        return True

if __name__ == "__main__":
    immunity = LatticeImmunity()
    
    print("=== LATTICE IMMUNITY VALIDATION ===\n")
    test_words = ["sphere", "anchor", "step", "glide", "hearthstone", "tt"]
    for word in test_words:
        immunity.preflight_check("MASON", word)
        print()