"""
KARMA CALIBRATION v2.0 — The Myth-to-Math Linter

Scans the PMG narrative chapters for symbolic drift and invariant contradictions.
Ensures the 'Verses' carry the same truth as the 'Vectors'.
"""

import os
import re

class NarrativeLinter:
    def __init__(self, canon_file):
        self.canon = self.load_canon(canon_file)
        self.findings = []
        self.score = 1.0

    def load_canon(self, path):
        # A simplified mapping for the linter based on the Canon
        return {
            "39.4": r"39\.4(725)?°?",
            "0.66": r"0\.66(0688)? Hz",
            "17": r"17|seventeen",
            "42": r"42|forty-two",
            "51": r"51|fifty-one",
            "14/17": r"14/17",
            "0.123": r"0\.123(7|558)?",
            "0.0925": r"0\.0925"
        }

    def scan_chapter(self, file_path):
        if not os.path.exists(file_path):
            return
            
        print(f"\n--- Linting: {os.path.basename(file_path)} ---")
        with open(file_path, 'r') as f:
            content = f.read()
            
            # Check for Positive Alignment
            for key, pattern in self.canon.items():
                if re.search(pattern, content, re.IGNORECASE):
                    print(f"  ✓ {key} alignment confirmed.")
                else:
                    # If the concept is mentioned but the number is wrong, that's a drift
                    pass

            # Check for Numerical Drift (Look for numbers followed by units)
            # e.g., finding "39.5" near "degrees" or "shear"
            self.check_drift(content, "shear", r"(\d+\.\d+)", 39.47, 0.1)
            self.check_drift(content, "heartbeat", r"(\d+\.\d+)", 0.66, 0.05)
            self.check_drift(content, "beat", r"(\d+\.\d+) Hz", 0.66, 0.05)

    def check_drift(self, content, context_word, num_pattern, target, threshold):
        # Search for context words and pull nearby numbers
        matches = re.finditer(rf"{context_word}.*?{num_pattern}|{num_pattern}.*?{context_word}", content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            # Pick the number from the group
            val_str = match.group(1) or match.group(2)
            if val_str:
                val = float(val_str)
                drift = abs(val - target)
                if drift > threshold:
                    print(f"  ⚠️ DRIFT: Found '{val}' near '{context_word}'. Expected target approx {target}.")
                    self.score -= 0.05
                elif drift > 0:
                     print(f"  · Precision note: Found '{val}' for '{context_word}'.")

    def report(self):
        print("\n" + "="*40)
        print(f"NARRATIVE COHERENCE INDEX: {max(0, self.score):.2%}")
        print("="*40)
        if self.score > 0.95:
            print("STATUS: MYTH-TO-MATH ALIGNMENT SEALED.")
        else:
            print("STATUS: RECALIBRATION REQUIRED. NARRATIVE DRIFT DETECTED.")

if __name__ == "__main__":
    linter = NarrativeLinter("/Users/studio/0platonicverses/CONSTANTS_CANON.md")
    
    chapters = [
        "/Users/studio/0platonicverses/PlatonicVerses Chapters/Book_3_Voices_of_the_Void/Chapter_19_The_Oracle_Grid/Chapter_19_The_Oracle_Grid.md",
        "/Users/studio/0platonicverses/PlatonicVerses Chapters/Book_3_Voices_of_the_Void/Chapter_20_The_Sentient_Interface/Chapter_20_The_Sentient_Interface.md",
        "/Users/studio/0platonicverses/PlatonicVerses Chapters/Book_3_Voices_of_the_Void/Chapter_21_The_Unfolding/Chapter_21_The_Unfolding.md"
    ]
    
    for ch in chapters:
        linter.scan_chapter(ch)
        
    linter.report()
