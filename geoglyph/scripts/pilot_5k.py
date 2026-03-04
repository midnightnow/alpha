import numpy as np
import json
import random
import math
from scipy.stats import entropy
import os

# --- FORMAL DEFINITIONS ---
# f: Word -> (Bearing, Entropy_P, Entropy_M, Variance, Residual)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class GeofontEncoder:
    def __init__(self, mapping=None):
        # Canonical A=1...Z=26 if no mapping provided
        self.mapping = mapping or {chr(65+i): i+1 for i in range(26)}
        
    def encode_word(self, word):
        word = word.upper()
        bearings = [0.0]
        weights = []
        parity = [] # 1 for Even/CW, 0 for Odd/CCW
        current_angle = 0.0
        
        for char in word:
            if char not in self.mapping: continue
            idx = self.mapping[char]
            weights.append(idx)
            
            # Parity Logic: Even = CW (+), Odd = CCW (-)
            is_even = (idx % 2 == 0)
            step_dir = 1 if is_even else -1
            parity.append(1 if is_even else 0)
            
            # 13-node logic: (Index / 13) * 180 degrees
            angle_step = (idx / 13) * 180 
            current_angle = (current_angle + (step_dir * angle_step)) % 360
            bearings.append(current_angle)
            
        if not weights: return None
        return {
            'bearings': bearings,
            'weights': weights,
            'parity': parity,
            'final_bearing': bearings[-1]
        }

def calculate_features(result):
    # 1. Final Bearing
    theta_f = result['final_bearing']
    
    # 2. Parity Entropy (Shannon)
    p_counts = np.bincount(result['parity'], minlength=2)
    p_dist = p_counts / len(result['parity'])
    h_parity = entropy(p_dist, base=2)
    
    # 3. Magnitude Entropy (Metric Dispersion)
    w_sum = sum(result['weights'])
    w_dist = [w / w_sum for w in result['weights']]
    h_weight = entropy(w_dist, base=2)
    
    # 4. Angular Variance
    ang_var = np.var(result['bearings'])
    
    return [theta_f, h_parity, h_weight, ang_var]

def run_pilot(corpus_path, n_permutations=1000):
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        return

    with open(corpus_path, 'r') as f:
        corpus = [line.strip().upper() for line in f if line.strip().isalpha()]
    
    print(f"Loaded {len(corpus)} words.")

    # 1. Canonical Run
    canonical_encoder = GeofontEncoder()
    canonical_results = [calculate_features(canonical_encoder.encode_word(w)) for w in corpus if canonical_encoder.encode_word(w)]
    canonical_mean = np.mean(canonical_results, axis=0)

    # 2. Permutation Loop
    permutation_means = []
    alphabet = list(ALPHABET)

    print(f"Starting {n_permutations} permutations...")
    for i in range(n_permutations):
        shuffled = alphabet[:]
        random.shuffle(shuffled)
        test_mapping = {letter: idx+1 for idx, letter in enumerate(shuffled)}
        
        test_encoder = GeofontEncoder(test_mapping)
        test_results = [calculate_features(test_encoder.encode_word(w)) for w in corpus if test_encoder.encode_word(w)]
        permutation_means.append(np.mean(test_results, axis=0))
        
        if (i+1) % 100 == 0:
            print(f"Iteration {i+1}/{n_permutations}...")

    # 3. Statistical Validation (Z-Test)
    p_means = np.array(permutation_means)
    p_mean_avg = np.mean(p_means, axis=0)
    p_std = np.std(p_means, axis=0)
    z_scores = (canonical_mean - p_mean_avg) / p_std

    results = {
        "canonical_mean": canonical_mean.tolist(),
        "permutation_mean_avg": p_mean_avg.tolist(),
        "permutation_std": p_std.tolist(),
        "z_scores": z_scores.tolist(),
        "features": ["final_bearing", "h_parity", "h_weight", "ang_var"]
    }

    print("\n--- Pilot Results ---")
    for i, feature in enumerate(results["features"]):
        print(f"{feature:15} | Canonical: {canonical_mean[i]:8.4f} | Z-Score: {z_scores[i]:8.4f}")

    with open("pilot_results.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\nResults saved to pilot_results.json")

if __name__ == "__main__":
    run_pilot("/tmp/pilot_5k_corpus.txt", n_permutations=1000)
