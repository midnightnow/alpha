"""
SOVEREIGN_NARRATIVE_SINTERING.PY
Phase XIV: From Folk-Rhyme to Formal-Fact
Directing the 'Flesh' to build the first Civilizational Myth.
"""

from pmg_constants import PMG
from mechanical_alphabet import MechanicalAlphabet
from sovereign_ledger import SovereignLedger

class NarrativeSinter:
    def __init__(self):
        self.alphabet = MechanicalAlphabet()
        self.ledger = SovereignLedger()
        self.SIGMA = PMG.UNITY_THRESHOLD

    def sinter_myth(self, myth_name: str, phonetic_root: str, target_coord: tuple):
        """
        Calculates if a myth has enough torque to anchor a node.
        Returns: 'CERAMIC_FACT' or 'FLESH_RHYME'
        """
        print(f"--- SINTERING MYTH: {myth_name} @ {target_coord} ---")
        
        # 1. Phonetic Torque Analysis
        analysis = self.alphabet.analyze_word(phonetic_root)
        base_torque = analysis['total_torque']
        
        # 2. Narrative Weight Calculation
        # Longer myths carry more semantic mass; apply harmonic multiplier
        harmonic = 1.3 if len(phonetic_root) >= 7 else 1.1
        narrative_torque = base_torque * harmonic
        
        # 3. Coherence Check Against Unity Threshold
        coherence = narrative_torque / 10.0  # Narrative Weight baseline
        
        print(f"Phonetic Root: '{phonetic_root}'")
        print(f"Base Torque: {base_torque:.4f} | Harmonic: {harmonic}x")
        print(f"Narrative Coherence: {coherence:.4f} (Σ={self.SIGMA})")
        
        # 4. Sintering Decision
        if coherence >= self.SIGMA:
            # Inscribe as Culture Block
            block = self.ledger.inscribe({
                "type": "MYTH",
                "name": myth_name,
                "phonetic_root": phonetic_root,
                "coordinate": target_coord,
                "coherence": coherence,
                "timestamp": "2026-02-20T13:04:00Z"
            })
            print(f"[SUCCESS] Myth vitrified as CERAMIC_FACT")
            print(f"[LEDGER] Block Hash: {block[:16]}...")
            return "CERAMIC_FACT", coherence
        else:
            print(f"[WARNING] Insufficient torque. Myth remains FLESH_RHYME")
            return "FLESH_RHYME", coherence

if __name__ == "__main__":
    sinter = NarrativeSinter()
    result, sigma = sinter.sinter_myth(
        myth_name="The Hearth",
        phonetic_root="hearthstone",
        target_coord=(0, 0)
    )
    print(f"\nFINAL STATUS: {result} | Σ={sigma:.4f}")
