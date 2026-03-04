import numpy as np
import json

# LATTICE CONSTANT
LATTICE_FREQ = 66.0688 # Hz (The Hades Beat)

# IPA Frequency Estimates (Commonly accepted f0 ranges for analysis)
# Note: These are idealized "Formant Centers" or "Resonant Peaks" for mapping
IPA_DATA = {
    # Vowels (The Count / 5-leg)
    "a": {"f0": 850, "place": "Open Central", "voicing": "voiced"},
    "e": {"f0": 500, "place": "Close-Mid Front", "voicing": "voiced"},
    "i": {"f0": 300, "place": "Close Front", "voicing": "voiced"},
    "o": {"f0": 450, "place": "Close-Mid Back", "voicing": "voiced"},
    "u": {"f0": 350, "place": "Close Back", "voicing": "voiced"},
    
    # Consonants (The Measure / 12-leg)
    "p": {"f0": 100, "place": "Bilabial", "voicing": "voiceless"},
    "b": {"f0": 120, "place": "Bilabial", "voicing": "voiced"},
    "t": {"f0": 200, "place": "Alveolar", "voicing": "voiceless"},
    "d": {"f0": 180, "place": "Alveolar", "voicing": "voiced"},
    "k": {"f0": 300, "place": "Velar", "voicing": "voiceless"},
    "g": {"f0": 250, "place": "Velar", "voicing": "voiced"},
    "s": {"f0": 4000, "place": "Alveolar", "voicing": "voiceless"}, # Fricative "Hiss"
    "z": {"f0": 4200, "place": "Alveolar", "voicing": "voiced"},
    "h": {"f0": 1000, "place": "Glottal", "voicing": "voiceless"},
    "m": {"f0": 150, "place": "Bilabial", "voicing": "voiced"},
    "n": {"f0": 200, "place": "Alveolar", "voicing": "voiced"},
    "l": {"f0": 350, "place": "Alveolar", "voicing": "voiced"},
    "r": {"f0": 450, "place": "Alveolar", "voicing": "voiced"},
    "f": {"f0": 3000, "place": "Labiodental", "voicing": "voiceless"},
    "v": {"f0": 3200, "place": "Labiodental", "voicing": "voiced"},
}

def calculate_node(place, voicing):
    # Mapping logic based on Articulatory Sector
    place_map = {
        "Bilabial": 7,     # South
        "Labiodental": 10, # West
        "Alveolar": 0,     # North (or 9 for sibilance)
        "Velar": 3,        # East
        "Glottal": 4,      # Southeast
    }
    
    node_base = place_map.get(place, 6) # Default to Central
    
    # Voicing Parity: Voiced = CCW (Odd offset), Voiceless = CW (Even offset)
    # Since our nodes are 0-12, let's use the Pair (CCW/CW) logic
    # Node k usually has CCW (idx*2) and CW (idx*2 + 1)
    # We will return the Node index
    return node_base

def resonance_check(f0, lattice=LATTICE_FREQ):
    ratio = f0 / lattice
    # Difference from nearest integer harmonic
    diff = abs(ratio - round(ratio))
    # Resonance score 1.0 = Perfect Lock, 0.0 = Anti-node
    score = 1.0 - (diff / 0.5)
    return score, round(ratio)

def run_audit():
    results = {}
    print(f"--- VORTEX-13 ACOUSTIC AUDIT (Lattice: {LATTICE_FREQ} Hz) ---\n")
    print(f"{'Phoneme':<10} | {'Node':<5} | {'Harmonic':<10} | {'Resonance Score'}")
    print("-" * 55)
    
    for ipa, data in IPA_DATA.items():
        # Special case for Sibilance (Node 9 Torque)
        if ipa in ["s", "z", "t"]:
            node = 9
        else:
            node = calculate_node(data["place"], data["voicing"])
            
        score, harm = resonance_check(data["f0"])
        results[ipa] = {
            "node": node,
            "resonance": round(score, 4),
            "harmonic": harm
        }
        
        print(f"{ipa:<10} | {node:<5} | {harm:<10} | {score*100:>.2f}%")
        
    with open("/Users/midnight/dev/geofont/ipa_resonance_data.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\nAudit saved to ipa_resonance_data.json.")

if __name__ == "__main__":
    run_audit()
