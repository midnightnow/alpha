#!/usr/bin/env python3
"""
Geofont Geometric Embedding (GGE) - Permutation Test Scaffold
Protocol v1.0 | 2026-02-28
Implements: Step 1 (Symmetry Baseline) + Step 2 (Permutation Test)
"""

import numpy as np
import pandas as pd
from itertools import product
import time
import sys

# ─────────────────────────────────────────────────────────────
# 1. CORE ENCODING (Protocol Section 1: Encoding Function f)
# ─────────────────────────────────────────────────────────────

def geofont_encode_word(word: str, mapping: dict) -> dict:
    """
    Deterministic transform f(S, φ) → θ_final, H_mag, H_par
    """
    word = word.upper()
    weights = [mapping[char] for char in word if char in mapping]
    n = len(weights)
    if n == 0:
        return None
    
    current_angle = 0.0
    for w in weights:
        step_dir = 1 if w % 2 == 0 else -1  # Even=CW, Odd=CCW
        angle_step = (w / 13.0) * 180.0
        current_angle = (current_angle + step_dir * angle_step) % 360.0
    
    total_weight = sum(weights)
    if total_weight > 0:
        p_weights = np.array([w / total_weight for w in weights])
        p_weights = p_weights[p_weights > 0]
        h_mag = -np.sum(p_weights * np.log2(p_weights)) / np.log2(n) if n > 1 else 0.0
    else:
        h_mag = 0.0
    
    cw_count = sum(1 for w in weights if w % 2 == 0)
    p_cw = cw_count / n
    p_ccw = 1 - p_cw
    h_par = 0.0
    if 0 < p_cw < 1:
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
# 3. STEP 1: BASELINE SYMMETRY TEST (Protocol Section 4, Step 1)
# ─────────────────────────────────────────────────────────────

def run_symmetry_baseline():
    print("[Step 1] Running Symmetry Baseline Test...", file=sys.stderr)
    mapping = {chr(65+i): i+1 for i in range(26)}
    
    thetas_1 = []
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        res = geofont_encode_word(char, mapping)
        if res: thetas_1.append(res['theta'])
    V_26 = circular_variance(np.array(thetas_1))
    
    thetas_2 = []
    for a, b in product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=2):
        res = geofont_encode_word(a+b, mapping)
        if res: thetas_2.append(res['theta'])
    V_676 = circular_variance(np.array(thetas_2))
    
    bias_note = "MECHANICAL BIAS DETECTED" if V_676 < 0.05 else "No strong mechanical bias"
    print(f"  V_26 (letters): {V_26:.4f}", file=sys.stderr)
    print(f"  V_676 (bigrams): {V_676:.4f}", file=sys.stderr)
    print(f"  Diagnostic: {bias_note}", file=sys.stderr)
    
    return V_26, V_676, bias_note


# ─────────────────────────────────────────────────────────────
# 4. STEP 2: PERMUTATION TEST (Protocol Section 4, Step 2)
# ─────────────────────────────────────────────────────────────

def run_permutation_test(corpus: list, n_permutations: int = 10000, seed: int = 42):
    print(f"[Step 2] Running Permutation Test (P={n_permutations})...", file=sys.stderr)
    np.random.seed(seed)
    
    canonical_mapping = {chr(65+i): i+1 for i in range(26)}
    canonical_data = [geofont_encode_word(w, canonical_mapping) for w in corpus]
    canonical_data = [d for d in canonical_data if d]
    
    canonical_thetas = np.array([d['theta'] for d in canonical_data])
    R_canonical = 1.0 - circular_variance(canonical_thetas)
    theta_star = circular_mean(canonical_thetas)
    
    print(f"  Canonical mapping: R = {R_canonical:.4f}, θ* = {theta_star:.2f}°", file=sys.stderr)
    
    permutation_R = np.zeros(n_permutations)
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    for p in range(n_permutations):
        perm_values = np.random.permutation(np.arange(1, 27))
        perm_mapping = {letters[i]: perm_values[i] for i in range(26)}
        
        # Optimized inner loop
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
    effect_size = R_canonical - np.mean(permutation_R)
    percentile = np.mean(permutation_R <= R_canonical) * 100
    
    if p_value < 0.01:
        decision = "PROCEED: Statistically significant (p < 0.01)"
    elif p_value > 0.10:
        decision = "PIVOT: Null result (p > 0.10)"
    else:
        decision = "INCONCLUSIVE (0.01 ≤ p ≤ 0.10)"
    
    return {
        'p_value': p_value,
        'effect_size': effect_size,
        'percentile': percentile,
        'R_canonical': R_canonical,
        'theta_star': theta_star,
        'decision': decision,
        'R_perm_mean': np.mean(permutation_R),
        'R_perm_std': np.std(permutation_R)
    }

if __name__ == "__main__":
    # Internal test only
    run_symmetry_baseline()
