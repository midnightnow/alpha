import numpy as np
import json

# LATTICE CONSTANT (Remains the same for baseline comparison)
LATTICE_FREQ = 66.0688 # Hz

# Greek Phoneme Estimates
# Note: Modern Greek pronunciation used as baseline for resonance check
GREEK_DATA = {
    "Alpha": {"ph": "/a/", "f0": 850, "node": 0, "type": "vowel"},
    "Beta": {"ph": "/v/", "f0": 3200, "node": 0, "type": "consonant"},
    "Gamma": {"ph": "/ɣ/", "f0": 2500, "node": 1, "type": "consonant"},
    "Delta": {"ph": "/ð/", "f0": 180, "node": 1, "type": "consonant"},
    "Epsilon": {"ph": "/e/", "f0": 500, "node": 2, "type": "vowel"},
    "Zeta": {"ph": "/z/", "f0": 4200, "node": 2, "type": "consonant"},
    "Eta": {"ph": "/i/", "f0": 300, "node": 3, "type": "vowel"},
    "Theta": {"ph": "/θ/", "f0": 3500, "node": 3, "type": "consonant"},
    "Iota": {"ph": "/i/", "f0": 300, "node": 4, "type": "vowel"},
    "Kappa": {"ph": "/k/", "f0": 300, "node": 4, "type": "consonant"},
    "Lambda": {"ph": "/l/", "f0": 350, "node": 5, "type": "consonant"},
    "Mu": {"ph": "/m/", "f0": 150, "node": 5, "type": "consonant"},
    "Nu": {"ph": "/n/", "f0": 200, "node": 6, "type": "consonant"},
    "Xi": {"ph": "/ks/", "f0": 4500, "node": 6, "type": "consonant"},
    "Omicron": {"ph": "/o/", "f0": 450, "node": 7, "type": "vowel"},
    "Pi": {"ph": "/p/", "f0": 100, "node": 7, "type": "consonant"},
    "Rho": {"ph": "/r/", "f0": 450, "node": 8, "type": "consonant"},
    "Sigma": {"ph": "/s/", "f0": 4000, "node": 8, "type": "consonant"},
    "Tau": {"ph": "/t/", "f0": 200, "node": 9, "type": "consonant"},
    "Upsilon": {"ph": "/i/", "f0": 300, "node": 9, "type": "vowel"},
    "Phi": {"ph": "/f/", "f0": 3000, "node": 10, "type": "consonant"},
    "Chi": {"ph": "/x/", "f0": 2800, "node": 10, "type": "consonant"},
    "Psi": {"ph": "/ps/", "f0": 4800, "node": 11, "type": "consonant"},
    "Omega": {"ph": "/o/", "f0": 450, "node": 11, "type": "vowel"},
}

def resonance_check(f0, lattice=LATTICE_FREQ):
    ratio = f0 / lattice
    diff = abs(ratio - round(ratio))
    score = 1.0 - (diff / 0.5)
    return score, round(ratio)

def run_greek_audit():
    results = {}
    print(f"--- GREEK 12-NODE ACOUSTIC AUDIT ---")
    print(f"{'Letter':<10} | {'Node':<5} | {'Harmonic':<10} | {'Resonance Score'}")
    print("-" * 55)
    
    for name, data in GREEK_DATA.items():
        score, harm = resonance_check(data["f0"])
        results[name] = {
            "phoneme": data["ph"],
            "node": data["node"],
            "resonance": round(score, 4),
            "harmonic": harm
        }
        print(f"{name:<10} | {data['node']:<5} | {harm:<10} | {score*100:>.2f}%")
        
    with open("/Users/midnight/dev/geofont/greek_resonance_data.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\nGreek Audit saved to greek_resonance_data.json.")

if __name__ == "__main__":
    run_greek_audit()
