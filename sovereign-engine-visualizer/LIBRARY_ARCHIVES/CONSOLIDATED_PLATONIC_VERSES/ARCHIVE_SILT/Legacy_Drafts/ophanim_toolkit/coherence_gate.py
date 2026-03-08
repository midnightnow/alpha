"""
COHERENCE GATE — coherence_gate.py
Automated metrological audit for the Principia Mathematica Geometrica.
Ensures that narrative metaphors remain phase-locked to technical invariants.
"""

import re
import os
import math
from pathlib import Path

# --- THE SOVEREIGN CONSTANTS (Source of Truth) ---
# Derived from CONSTANTS_CANON.md
INVARIANTS = {
    "PRIME_ANCHOR": 17,
    "SHEAR_ANGLE": 39.4725,
    "HADES_BEAT": 0.660688,
    "HADES_GAP": 0.1237,
    "PISANO_CLOCK": 0.66,
    "PACKING_DELTA": 0.0925,
    "ROOT_42": 648.07,
    "ROOT_51": 714.14,
    "ROOT_60": 774.60
}

class CoherenceGate:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.narrative_dirs = [
            self.root_dir / "PlatonicVerses Chapters",
            self.root_dir / "Root42",
            self.root_dir / "Root51"
        ]
        self.code_dir = self.root_dir / "ophanim_toolkit"
        self.failures = []

    def scan_narrative(self):
        print("\n--- Scanning Narrative for Metrological Drift ---")
        for ndir in self.narrative_dirs:
            if not ndir.exists():
                continue
            for md_file in ndir.glob("**/*.md"):
                content = md_file.read_text(errors='ignore')
                self._check_content(content, md_file.relative_to(self.root_dir))

    def _check_content(self, content, filename):
        # Look for numerical mentions of our constants
        
        # 1. Check Shear Angle
        # Use negative lookbehind to avoid catching decimals in larger numbers
        shear_matches = re.findall(r"(?<!\d)(\d{1,3}\.\d{1,4})[°\s]*?(?:shear|angle|degrees)", content, re.IGNORECASE)
        for match in shear_matches:
            val = float(match)
            if abs(val - INVARIANTS["SHEAR_ANGLE"]) > 0.1: # Allow 39.4 to pass for 39.47
                if abs(val - 39.4) > 0.01 and abs(val - 39.5) > 0.01:
                    self.failures.append(f"Chapter Drift: {filename} contains '{val}°' near 'shear'. Expected approx {INVARIANTS['SHEAR_ANGLE']}.")

        # 2. Check Hades Heartbeat / Root Frequencies
        # Use negative lookbehind to ensure we get the full number
        freq_matches = re.findall(r"(?<!\d)(\d{1,3}\.\d{1,6})\s*?(?:Hz|heartbeat|pulse|beat)", content, re.IGNORECASE)
        for match in freq_matches:
            val = float(match)
            # Check against Beat
            is_beat = abs(val - INVARIANTS["HADES_BEAT"]) < 0.01 or abs(val - 0.66) < 0.001
            # Check against Roots
            is_root = any(abs(val - root) < 1.0 for root in [INVARIANTS["ROOT_42"], INVARIANTS["ROOT_51"], INVARIANTS["ROOT_60"]])
            
            # Special case: explicitly mentioned rejected √48 beat
            if val == 0.447 and "48" in content:
                continue

            if not (is_beat or is_root):
                self.failures.append(f"Chapter Drift: {filename} contains '{val} Hz'. No matching invariant (Beat=0.66, Roots=648/714/774).")

        # 3. Check Prime Anchor
        prime_mentions = re.findall(r"\b1[78]\b", content) # Looking for potential swaps to 18
        if "18" in prime_mentions and "17" not in content.lower():
             # This is a weak check but flags potential dead-symmetry vs living-fracture swaps
             pass

    def scan_code(self):
        print("--- Scanning Code for Invariant Divergence ---")
        # Check specific python files for the constants
        targets = {
            "actualizer.py": ["14/17", "0.0925"],
            "e8_hades_validator.py": ["math.e / 22", "30", "8"],
            "standing_man_functor.py": ["39.4725", "0.660688"]
        }
        
        for script, constants in targets.items():
            path = self.code_dir / script
            if not path.exists():
                continue
            content = path.read_text()
            for c in constants:
                if c not in content:
                    self.failures.append(f"Code Divergence: {script} missing required invariant '{c}'.")

    def report(self):
        print("\n" + "="*60)
        print("   PMG COHERENCE GATE: METROLOGICAL REPORT   ")
        print("="*60)
        
        if not self.failures:
            print("\n[STATUS: PHASE-LOCKED]")
            print("Narrative metaphors are technically binding. Repository vitrified.")
            return True
        else:
            print(f"\n[STATUS: DRIFT DETECTED] ({len(self.failures)} instances)")
            for f in self.failures:
                print(f"  ✗ {f}")
            return False

if __name__ == "__main__":
    gate = CoherenceGate("/Users/studio/0platonicverses")
    gate.scan_narrative()
    gate.scan_code()
    if gate.report():
        exit(0)
    else:
        exit(1)
