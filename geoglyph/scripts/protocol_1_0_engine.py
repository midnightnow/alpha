#!/usr/bin/env python3
"""
Geofont Geometric Embedding (GGE) - Permutation Test Scaffold
Protocol v1.0 | 2026-02-28
Implements: Step 1 (Symmetry Baseline) + Step 2 (Permutation Test)
With NLTK Brown Corpus Preprocessing (Lemmatization, POS Filtering)
"""

import numpy as np
import pandas as pd
from itertools import product
import time
import sys
import re
import json
import nltk
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist

# Ensure NLTK data
def setup_nltk():
    for res in ['brown', 'wordnet', 'omw-1.4', 'universal_tagset', 'averaged_perceptron_tagger']:
        try:
            nltk.data.find(f'corpora/{res}' if 'brown' in res or 'wordnet' in res else f'taggers/{res}')
        except:
            nltk.download(res)

setup_nltk()

# ─────────────────────────────────────────────────────────────
# 1. CORE ENCODING (Protocol Section 1: Encoding Function f)
# ─────────────────────────────────────────────────────────────

def geofont_encode_word(word: str, mapping: dict) -> dict:
    """
    Deterministic transform f(S, φ) → θ_final, H_mag, H_par
    Scale-invariant: does not depend on word length for bearing calculation
    """
    word = word.upper()
    weights = [mapping[char] for char in word if char in mapping]
    n = len(weights)
    if n == 0:
        return None
    
    # Final bearing calculation (13-node bipolar logic)
    current_angle = 0.0
    for w in weights:
        step_dir = 1 if w % 2 == 0 else -1  # Even=CW, Odd=CCW
        angle_step = (w / 13.0) * 180.0
        current_angle = (current_angle + step_dir * angle_step) % 360.0
    
    # Magnitude entropy (normalized by word length for scale-invariance)
    total_weight = sum(weights)
    if total_weight > 0:
        p_weights = np.array([w / total_weight for w in weights])
        p_weights = p_weights[p_weights > 0]
        h_mag = -np.sum(p_weights * np.log2(p_weights)) / np.log2(n) if n > 1 else 0.0
    else:
        h_mag = 0.0
    
    # Parity entropy (binary: even=CW, odd=CCW)
    cw_count = sum(1 for w in weights if w % 2 == 0)
    p_cw = cw_count / n
    p_ccw = 1 - p_cw
    h_par = 0.0
    if 0 < p_cw < 1:
        # Normalize to log2(min(n, 2)) as per protocol Section 2.3
        norm_factor = np.log2(2) if n >= 2 else 1.0
        h_par = -(p_cw * np.log2(p_cw) + p_ccw * np.log2(p_ccw)) / norm_factor
    
    return {
        'theta': current_angle,
        'h_mag_norm': h_mag,
        'h_par_norm': h_par,
        'length': n
    }

# ─────────────────────────────────────────────────────────────
# 2. CIRCULAR STATISTICS (Protocol Section 2: Metrics)
# ─────────────────────────────────────────────────────────────

def circular_mean(angles_deg: np.ndarray) -> float:
    angles_rad = np.deg2rad(angles_deg)
    mean_sin = np.mean(np.sin(angles_rad))
    mean_cos = np.mean(np.cos(angles_rad))
    return np.rad2deg(np.arctan2(mean_sin, mean_cos)) % 360.0

def circular_variance(angles_deg: np.ndarray) -> float:
    angles_rad = np.deg2rad(angles_deg)
    R = np.sqrt(np.mean(np.cos(angles_rad))**2 + np.mean(np.sin(angles_rad))**2)
    return 1.0 - R

# ─────────────────────────────────────────────────────────────
# 3. CORPUS LOADING (Protocol Section 3 + 6)
# ─────────────────────────────────────────────────────────────

def load_protocol_corpus():
    print("[Info] Preparing Brown Corpus with Lemmatization and POS Filtering...", file=sys.stderr)
    lemmatizer = WordNetLemmatizer()
    
    # Ingest Brown with POS tags
    # Section 6: Remove ^NNP (Proper nouns)
    tagged_words = brown.tagged_words(tagset='universal')
    
    # Filter for A-Z only, length 3-12
    # POS filter: Keep only NOUN, VERB, ADJ, ADV to avoid proper nouns/noise
    # protocol says remove proper nouns specifically.
    
    regex = re.compile('^[A-Z]{3,12}$')
    processed_words = []
    
    # Brown tags for proper nouns are often 'NP'
    # Using universal tagset: Nouns are 'NOUN'
    # We'll use the specific Brown tags to filter out NP (Proper Noun)
    specific_tags = brown.tagged_words() 
    
    for word, tag in specific_tags:
        word_up = word.upper()
        if tag.startswith('NP'): continue # Skip proper nouns
        if not regex.match(word_up): continue
        
        # Lemmatize
        lemma = lemmatizer.lemmatize(word.lower()).upper()
        if regex.match(lemma):
            processed_words.append(lemma)
            
    # Frequency Distribution to extract top 5,000 unique lemmas
    fdist = FreqDist(processed_words)
    top_5k = [word for word, count in fdist.most_common(5000)]
    
    print(f"  Final Corpus Size: {len(top_5k)} unique lemmas", file=sys.stderr)
    return top_5k

# ─────────────────────────────────────────────────────────────
# 4. STEP 1: BASELINE SYMMETRY TEST (Protocol Section 4, Step 1)
# ─────────────────────────────────────────────────────────────

def run_symmetry_baseline():
    print("[Step 1] Running Symmetry Baseline Test...", file=sys.stderr)
    mapping = {chr(65+i): i+1 for i in range(26)}
    
    thetas_2 = []
    for a, b in product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=2):
        res = geofont_encode_word(a+b, mapping)
        if res: thetas_2.append(res['theta'])
    V_676 = circular_variance(np.array(thetas_2))
    
    bias_note = "MECHANICAL BIAS DETECTED" if V_676 < 0.05 else "No strong mechanical bias"
    print(f"  V_676 (bigrams): {V_676:.4f}", file=sys.stderr)
    print(f"  Diagnostic: {bias_note}", file=sys.stderr)
    return V_676, bias_note

# ─────────────────────────────────────────────────────────────
# 5. STEP 2: PERMUTATION TEST (Protocol Section 4, Step 2)
# ─────────────────────────────────────────────────────────────

def run_permutation_test(corpus: list, n_permutations: int = 10000, seed: int = 42):
    print(f"[Step 2] Running Permutation Test (P={n_permutations})...", file=sys.stderr)
    np.random.seed(seed)
    
    canonical_mapping = {chr(65+i): i+1 for i in range(26)}
    canonical_data = [geofont_encode_word(w, canonical_mapping) for w in corpus]
    canonical_data = [d for d in canonical_data if d]
    
    canonical_thetas = np.array([d['theta'] for d in canonical_data])
    h_mag_vals = [d['h_mag_norm'] for d in canonical_data]
    h_par_vals = [d['h_par_norm'] for d in canonical_data]
    
    V_canonical = circular_variance(canonical_thetas)
    R_canonical = 1.0 - V_canonical
    theta_star = circular_mean(canonical_thetas)
    h_mag_star = np.mean(h_mag_vals)
    h_par_star = np.mean(h_par_vals)
    
    print(f"  Canonical mapping: V = {V_canonical:.4f}, R = {R_canonical:.4f}, θ* = {theta_star:.2f}°", file=sys.stderr)
    
    permutation_R = np.zeros(n_permutations)
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    for p in range(n_permutations):
        perm_values = np.random.permutation(np.arange(1, 27))
        perm_mapping = {letters[i]: perm_values[i] for i in range(26)}
        
        perm_thetas = []
        for word in corpus:
            res = geofont_encode_word(word, perm_mapping)
            if res: perm_thetas.append(res['theta'])
        
        perm_thetas_arr = np.array(perm_thetas)
        R_p = np.sqrt(np.mean(np.cos(np.deg2rad(perm_thetas_arr)))**2 + 
                     np.mean(np.sin(np.deg2rad(perm_thetas_arr)))**2)
        permutation_R[p] = R_p
        
        if (p + 1) % 1000 == 0:
            print(f"    Completed {p+1}/{n_permutations} permutations", file=sys.stderr)
    
    p_value = np.mean(permutation_R >= R_canonical)
    z_score = (R_canonical - np.mean(permutation_R)) / np.std(permutation_R)
    percentile = np.mean(permutation_R <= R_canonical) * 100
    
    if p_value < 0.01:
        decision = "PROCEED: Statistically significant (p < 0.01)"
    elif p_value > 0.10:
        decision = "PIVOT: Null result (p > 0.10)"
    else:
        decision = "INCONCLUSIVE (0.01 ≤ p ≤ 0.10)"
        
    return {
        'theta_star': theta_star,
        'h_mag_star': h_mag_star,
        'h_par_star': h_par_star,
        'p_value': p_value,
        'z_score': z_score,
        'percentile': percentile,
        'R_canonical': R_canonical,
        'V_canonical': V_canonical,
        'decision': decision
    }

if __name__ == "__main__":
    start_time = time.time()
    V_676, bias_note = run_symmetry_baseline()
    corpus = load_protocol_corpus()
    results = run_permutation_test(corpus, n_permutations=10000, seed=42)
    
    final_output = {
        "metadata": {"protocol": "1.0", "date": "2026-02-28", "n_permutations": 10000},
        "step_1": {"V_676": V_676, "bias_note": bias_note},
        "step_2": results
    }
    
    with open("protocol_1_0_final.json", "w") as f:
        json.dump(final_output, f, indent=4)
        
    print("\n--- PROTOCOL 1.0 RESULTS ---")
    print(f"MARROW CONSTANT (θ*): {results['theta_star']:.2f}°")
    print(f"MAG ENTROPY STAR (H*): {results['h_mag_star']:.4f}")
    print(f"PAR ENTROPY STAR (H*): {results['h_par_star']:.4f}")
    print(f"P-VALUE: {results['p_value']:.4f}")
    print(f"Z-SCORE: {results['z_score']:.4f}")
    print(f"PERCENTILE: {results['percentile']:.1f}%")
    print(f"DECISION: {results['decision']}")
    print(f"RUNTIME: {time.time() - start_time:.1f}s")
