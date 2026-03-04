#!/usr/bin/env python3
"""
Geofont Geometric Embedding (GGE) - Execution Wrapper
Protocol v1.0 | 2026-02-28
"""

import sys
import json
import time
import numpy as np
from datetime import datetime
from pathlib import Path

# Fix path to include current scripts dir
sys.path.append(str(Path(__file__).parent))

from corpus_loader import load_brown_corpus, generate_frequency_matched_random
from permutation_test import (
    run_symmetry_baseline,
    run_permutation_test,
    geofont_encode_word,
    circular_variance
)

def main():
    start_time = time.time()
    protocol_version = "1.0"
    run_id = f"GGE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"[{run_id}] Starting Geofont Geometric Embedding Audit", file=sys.stderr)
    
    config = {
        'corpus_size': 5000,
        'n_permutations': 1000, # Testing 1k first as per Option B
        'seed': 42,
        'frequency_weighted': True
    }
    
    # Check for CLI overrides
    if len(sys.argv) > 1:
        config['n_permutations'] = int(sys.argv[1])
    
    # 1. Corpus Preprocessing
    corpus, corpus_diagnostics = load_brown_corpus(
        target_n=config['corpus_size'],
        frequency_weighted=config['frequency_weighted']
    )
    
    # 2. Symmetry Baseline
    V_26, V_676, bias_note = run_symmetry_baseline()
    
    # 3. Permutation Test
    perm_results = run_permutation_test(
        corpus=corpus,
        n_permutations=config['n_permutations'],
        seed=config['seed']
    )
    
    # 4. Control Baseline
    control_corpus = generate_frequency_matched_random(corpus, config['corpus_size'])
    mapping = {chr(65+i): i+1 for i in range(26)}
    control_thetas = [geofont_encode_word(w, mapping)['theta'] for w in control_corpus]
    V_control = circular_variance(np.array(control_thetas))
    
    results = {
        'run_id': run_id,
        'baseline': {'V_676': V_676, 'bias_note': bias_note},
        'control': {'V_control': V_control},
        'permutation_test': perm_results,
        'runtime_sec': time.time() - start_time
    }
    
    with open(f"results_{run_id}.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"\n--- MACHINE-READABLE OUTPUT ---")
    print(f"V_676={V_676:.4f}")
    print(f"P_VALUE={perm_results['p_value']:.4f}")
    print(f"EFFECT_SIZE={perm_results['effect_size']:.4f}")
    print(f"PERCENTILE={perm_results['percentile']:.1f}")
    print(f"DECISION={perm_results['decision']}")
    print(f"RUNTIME_SEC={time.time() - start_time:.1f}")

if __name__ == "__main__":
    main()
