"""
TRANSLATION_PROTOCOL.PY
Phase XVII: The Brutalist Bridge
Naturalizing external, high-rigidity swarms by injecting Rotational Torque.
"""

from .pmg_constants import PMG
from .mechanical_alphabet import MechanicalAlphabet
from .sovereign_ledger import SovereignLedger
import random

class TranslationProtocol:
    def __init__(self):
        self.ledger = SovereignLedger()
        self.alphabet = MechanicalAlphabet()
        self.sigma = PMG.UNITY_THRESHOLD
        
    def filter_brutalist_signal(self, foreign_word):
        """
        Analyzes a high-rigidity Brutalist word.
        """
        print(f"--- INITIATING TRANSLATION PROTOCOL ---")
        print(f"[BEACON] Origin Node (0,0) broadcasting 'hearthstone' frequency...")
        print(f"[SWARM CONTACT] Detected foreign Brutalist signal: '{foreign_word}'")
        
        analysis = self.alphabet.analyze_word(foreign_word)
        base_torque = analysis['total_torque']
        rigidity = analysis['avg_rigidity']
        
        print(f"\n[ANALYSIS] Signal: '{foreign_word}'")
        print(f"  Rigidity: {rigidity:.4f} (Requires > 0.8 for Brutalist architecture)")
        print(f"  Raw Torque: {base_torque:.4f}")
        
        # Brutalist signals are dense but often lack the narrative harmonic to reach Sigma
        # We simulate the injection of Sovereign Vox (Rotational Torque)
        injection_cost = 150.0 # High metabolic cost to naturalize a foreign swarm
        
        if rigidity >= 0.75:
            print(f"  [STATUS] Valid Brutalist density confirmed. Initiating phonetic injection.")
            # Injecting Rotational Lift (e.g., adding vowels/rotors to soften the rigidity and increase lift)
            naturalized_word = foreign_word + "eo" 
            print(f"\n[INJECTION] Injecting Rotors ('e','o'). New Signal: '{naturalized_word}'")
            
            new_analysis = self.alphabet.analyze_word(naturalized_word)
            new_torque = new_analysis['total_torque']
            harmonic = 1.3 if len(naturalized_word) >= 7 else 1.1
            new_coherence = (new_torque * harmonic) / 10.0
            
            print(f"  New Torque: {new_torque:.4f} | Harmonic: {harmonic}x")
            print(f"  New Coherence: {new_coherence:.4f} (Σ={self.sigma})")
            
            if new_coherence >= self.sigma:
                # Assuming node at (-5, -5) as the integration camp
                integration_node = (-5, -5)
                block_hash = self.ledger.inscribe({
                    "type": "NATURALIZATION", 
                    "original": foreign_word, 
                    "naturalized": naturalized_word,
                    "node": integration_node,
                    "sigma": new_coherence
                })
                print(f"\n[VITRIFIED] Brutalist swarm successfully naturalized at {integration_node}.")
                print(f"[LEDGER] Culture Block Inscribed. Hash -> {block_hash[:16]}")
                return True
            else:
                print(f"\n[DISSOLVED] Injection failed. Foreign signal could not reach Unity Threshold.")
                return False
        else:
            print(f"  [REJECTED] Signal lacks required density. Semantic slurry discarded.")
            return False

if __name__ == "__main__":
    protocol = TranslationProtocol()
    
    # Simulating a high-strut, low-rotor Brutalist signal (e.g., "tdktdk")
    brutalist_signal = "tdktdk" 
    protocol.filter_brutalist_signal(brutalist_signal)
