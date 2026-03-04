import numpy as np
import pandas as pd
import json
import random
import math
import re
import nltk
from nltk.corpus import brown
from nltk.probability import FreqDist
from scipy.stats import entropy
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure NLTK data is available
try:
    brown.words()
except:
    nltk.download('brown')

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class GeofontEncoder:
    def __init__(self, mapping=None):
        self.mapping = mapping or {chr(65+i): i+1 for i in range(26)}
        
    def encode_word(self, word):
        word = word.upper()
        bearings = [0.0]
        weights = []
        parity = []
        current_angle = 0.0
        
        for char in word:
            if char not in self.mapping: continue
            idx = self.mapping[char]
            weights.append(idx)
            is_even = (idx % 2 == 0)
            step_dir = 1 if is_even else -1
            parity.append(1 if is_even else 0)
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
    if not result: return None
    theta_f = result['final_bearing']
    p_counts = np.bincount(result['parity'], minlength=2)
    p_dist = p_counts / len(result['parity'])
    h_parity = entropy(p_dist, base=2)
    w_sum = sum(result['weights'])
    w_dist = [w / w_sum for w in result['weights']]
    h_weight = entropy(w_dist, base=2)
    ang_var = np.var(result['bearings'])
    return [theta_f, h_parity, h_weight, ang_var]

def get_corpus_5k():
    print("Ingesting Brown Corpus...")
    raw_words = [w.upper() for w in brown.words()]
    regex = re.compile('^[A-Z]+$')
    clean_words = [w for w in raw_words if regex.match(w)]
    fdist = FreqDist(clean_words)
    top_5k = [word for word, count in fdist.most_common(5500) if len(word) > 1][:5000]
    print(f"Successfully sourced {len(top_5k)} words.")
    return top_5k

def run_tomography(n_permutations=1000):
    corpus = get_corpus_5k()
    
    # 1. Canonical Run
    encoder = GeofontEncoder()
    print("Executing Canonical Run...")
    raw_results = [encoder.encode_word(w) for w in corpus]
    features = [calculate_features(r) for r in raw_results if r]
    features_arr = np.array(features)
    
    # Average Stats
    canonical_mean = np.mean(features_arr, axis=0)
    
    # Calculate Theta Star (Circular Mean)
    bearings_rad = np.radians(features_arr[:, 0])
    sin_sum = np.sum(np.sin(bearings_rad))
    cos_sum = np.sum(np.cos(bearings_rad))
    theta_star = np.degrees(np.arctan2(sin_sum, cos_sum)) % 360
    
    # 2. Permutation Analysis
    print(f"Starting Permutation Analysis (N={n_permutations})...")
    permutation_means = []
    
    alphabet_list = list(ALPHABET)
    for i in range(n_permutations):
        shuffled = alphabet_list[:]
        random.shuffle(shuffled)
        mapping = {letter: idx+1 for idx, letter in enumerate(shuffled)}
        
        test_encoder = GeofontEncoder(mapping)
        test_feats = [calculate_features(test_encoder.encode_word(w)) for w in corpus if test_encoder.encode_word(w)]
        permutation_means.append(np.mean(test_feats, axis=0))
        
        if (i+1) % 100 == 0:
            print(f"Iteration {i+1}/{n_permutations}...")

    # 3. Statistical Validation
    p_means = np.array(permutation_means)
    p_mean_avg = np.mean(p_means, axis=0)
    p_std = np.std(p_means, axis=0)
    z_scores = (canonical_mean - p_mean_avg) / p_std
    
    # 4. Outlier Detection
    df = pd.DataFrame(features_arr, columns=['theta', 'h_parity', 'h_weight', 'ang_var'])
    df['word'] = corpus[:len(features_arr)]
    df['theta_dev'] = np.abs(df['theta'] - theta_star)
    
    # Resonance Index (Composite Z)
    # Lower is more "stable" (less entropy, less variance, less deviation)
    df['resonance_score'] = (df['h_parity'] + df['h_weight'] + df['theta_dev']/360 + df['ang_var']/10000)
    
    monoliths = df.sort_values(by='resonance_score').head(10)
    shrapnel = df.sort_values(by='resonance_score', ascending=False).head(10)
    
    # Results Object
    results = {
        "theta_star": theta_star,
        "h_mag_star": canonical_mean[2],
        "h_par_star": canonical_mean[1],
        "canonical_mean": canonical_mean.tolist(),
        "z_scores": z_scores.tolist(),
        "monoliths": monoliths[['word', 'resonance_score', 'theta']].to_dict(orient='records'),
        "shrapnel": shrapnel[['word', 'resonance_score', 'theta']].to_dict(orient='records')
    }
    
    with open("tomography_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\n--- THE MARROW AUDIT ---")
    print(f"Theta Star (Attractor): {theta_star:.2f}°")
    print(f"Mean Magnitude Entropy: {canonical_mean[2]:.4f} bits")
    print(f"Mean Parity Entropy:    {canonical_mean[1]:.4f} bits")
    print("-" * 23)
    
    print("\n--- Z-SCORE PROFILE ---")
    feat_names = ["Final Bearing", "Parity Entropy", "Mag Entropy", "Ang Variance"]
    for i, name in enumerate(feat_names):
        print(f"{name:15} | Z: {z_scores[i]:8.4f}")

    print("\n--- THE MONOLITHS (Most Stable) ---")
    print(monoliths[['word', 'resonance_score', 'theta']])
    
    print("\n--- THE SHRAPNEL (Most Chaotic) ---")
    print(shrapnel[['word', 'resonance_score', 'theta']])

if __name__ == "__main__":
    run_tomography(n_permutations=1000)
