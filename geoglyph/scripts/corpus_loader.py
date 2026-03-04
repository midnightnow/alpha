#!/usr/bin/env python3
"""
Geofont Geometric Embedding (GGE) - Corpus Preprocessing Module
Protocol v1.0 | 2026-02-28
Implements: Protocol Sections 3 (Corpus) + 6 (Pre-Processing Requirements)
"""

import nltk
import hashlib
import re
from collections import Counter
from typing import List, Tuple, Dict
import sys
import os

# Download required NLTK data (silent)
def _ensure_nltk_data():
    resources = ['brown', 'wordnet', 'averaged_perceptron_tagger', 'stopwords', 'universal_tagset']
    for resource in resources:
        try:
            if resource == 'brown':
                nltk.data.find('corpora/brown')
            elif resource == 'wordnet':
                nltk.data.find('corpora/wordnet')
            elif 'tagger' in resource:
                nltk.data.find(f'taggers/{resource}')
            else:
                nltk.data.find(f'corpora/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

_ensure_nltk_data()

from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


# ─────────────────────────────────────────────────────────────
# 1. FILTERING CASCADE (Protocol Section 6)
# ─────────────────────────────────────────────────────────────

def filter_alpha_only(token: str) -> bool:
    """Protocol Section 6: A-Z only, uppercase, no diacritics/digits"""
    return bool(re.match(r'^[A-Z]{2,}$', token.upper()))

def filter_proper_nouns(token: str, pos: str) -> bool:
    """Protocol Section 6: Remove proper nouns (POS tags starting with NNP or NP)"""
    return not (pos.startswith('NNP') or pos.startswith('NP'))

def filter_length_bin(token: str, min_len: int = 2, max_len: int = 12) -> bool:
    """Protocol Section 6: Length bounds for analysis"""
    return min_len <= len(token) <= max_len


# ─────────────────────────────────────────────────────────────
# 2. LEMMATIZATION (Protocol Section 6)
# ─────────────────────────────────────────────────────────────

def lemmatize_token(token: str, pos: str) -> str:
    """
    Reduce inflected forms to base lemma.
    Maps NLTK POS tags to WordNet POS for accurate lemmatization.
    """
    lemmatizer = WordNetLemmatizer()
    
    # Map NLTK POS to WordNet POS
    pos_map = {
        'NN': 'n', 'NNS': 'n', 'NNP': 'n', 'NNPS': 'n',
        'VB': 'v', 'VBD': 'v', 'VBG': 'v', 'VBN': 'v', 'VBP': 'v', 'VBZ': 'v',
        'JJ': 'a', 'JJR': 'a', 'JJS': 'a',
        'RB': 'r', 'RBR': 'r', 'RBS': 'r'
    }
    wn_pos = pos_map.get(pos, 'n')  # Default to noun
    
    return lemmatizer.lemmatize(token.lower(), wn_pos).upper()


# ─────────────────────────────────────────────────────────────
# 3. CORPUS LOADER (Protocol Section 3)
# ─────────────────────────────────────────────────────────────

def load_brown_corpus(
    target_n: int = 5000,
    length_bins: Dict[str, Tuple[int, int]] = None,
    frequency_weighted: bool = True
) -> Tuple[List[str], Dict]:
    """
    Load and preprocess Brown Corpus per Protocol Section 3 + 6.
    """
    
    if length_bins is None:
        # Protocol Section 6 default bins
        length_bins = {
            'short': (2, 5),
            'medium': (6, 8),
            'long': (9, 12)
        }
    
    diagnostics = {
        'raw_tokens': 0,
        'after_alpha_filter': 0,
        'after_pos_filter': 0,
        'after_lemmatization': 0,
        'after_length_filter': 0,
        'final_unique': 0,
        'length_distribution': {},
        'pos_distribution': Counter(),
        'sha256_hash': ''
    }
    
    print("[Corpus Loader] Loading Brown Corpus...", file=sys.stderr)
    
    # Step 1: Load raw tokens (using tagged words for better POS filtering)
    tagged_tokens = brown.tagged_words()
    diagnostics['raw_tokens'] = len(tagged_tokens)
    print(f"  Raw tokens: {diagnostics['raw_tokens']:,}", file=sys.stderr)
    
    # Step 2: Apply filtering cascade
    filtered_tokens = []
    
    for token, pos in tagged_tokens:
        diagnostics['pos_distribution'][pos] += 1
        
        # Filter 1: A-Z only, length >= 2
        if not filter_alpha_only(token):
            continue
        diagnostics['after_alpha_filter'] += 1
        
        # Filter 2: Remove proper nouns
        if not filter_proper_nouns(token, pos):
            continue
        diagnostics['after_pos_filter'] += 1
        
        # Filter 3: Lemmatize
        lemma = lemmatize_token(token, pos)
        diagnostics['after_lemmatization'] += 1
        
        # Filter 4: Length bin check
        if not filter_length_bin(lemma, min_len=2, max_len=12):
            continue
        diagnostics['after_length_filter'] += 1
        
        filtered_tokens.append(lemma)
    
    print(f"  After alpha filter: {diagnostics['after_alpha_filter']:,}", file=sys.stderr)
    print(f"  After POS filter: {diagnostics['after_pos_filter']:,}", file=sys.stderr)
    print(f"  After lemmatization: {diagnostics['after_lemmatization']:,}", file=sys.stderr)
    print(f"  After length filter: {diagnostics['after_length_filter']:,}", file=sys.stderr)
    
    # Step 4: Frequency-weighted sampling (Protocol Section 3)
    print("[Corpus Loader] Computing frequency distribution...", file=sys.stderr)
    fdist = Counter(filtered_tokens)
    
    if frequency_weighted:
        # Sample top N by frequency
        sampled = [word for word, count in fdist.most_common(target_n)]
    else:
        # Uniform sample across frequency spectrum
        unique_words = list(fdist.keys())
        import random
        random.seed(42)
        sampled = random.sample(unique_words, min(target_n, len(unique_words)))
    
    diagnostics['final_unique'] = len(sampled)
    print(f"  Final corpus size: {diagnostics['final_unique']:,} unique lemmas", file=sys.stderr)
    
    # Step 5: Length distribution analysis (Protocol Section 6)
    for bin_name, (min_len, max_len) in length_bins.items():
        bin_count = sum(1 for w in sampled if min_len <= len(w) <= max_len)
        diagnostics['length_distribution'][bin_name] = {
            'count': bin_count,
            'percentage': (bin_count / len(sampled)) * 100 if sampled else 0,
            'range': f"{min_len}-{max_len}"
        }
    
    print("[Corpus Loader] Length distribution:", file=sys.stderr)
    for bin_name, stats in diagnostics['length_distribution'].items():
        print(f"  {bin_name} ({stats['range']}): {stats['count']} ({stats['percentage']:.1f}%)", file=sys.stderr)
    
    # Step 6: Generate SHA-256 hash for reproducibility (Protocol Section 7)
    corpus_string = ''.join(sorted(sampled))
    diagnostics['sha256_hash'] = hashlib.sha256(corpus_string.encode('utf-8')).hexdigest()
    print(f"  Corpus SHA-256: {diagnostics['sha256_hash'][:16]}...", file=sys.stderr)
    
    return sampled, diagnostics


# ─────────────────────────────────────────────────────────────
# 4. CONTROL: FREQUENCY-MATCHED RANDOM STRINGS (Protocol Section 4B)
# ─────────────────────────────────────────────────────────────

def generate_frequency_matched_random(
    reference_corpus: List[str],
    n_strings: int = 5000,
    seed: int = 42
) -> List[str]:
    """
    Generate random strings with length distribution matched to reference corpus.
    Letters sampled from empirical English unigram frequencies.
    """
    import random
    random.seed(seed)
    
    english_letter_freq = "ETAONIRSHDLFCMUGYPWBVKXJQZ"
    
    length_counts = Counter(len(w) for w in reference_corpus)
    total = sum(length_counts.values())
    length_probs = {length: count / total for length, count in length_counts.items()}
    
    random_strings = []
    for _ in range(n_strings):
        length = random.choices(
            list(length_probs.keys()),
            weights=list(length_probs.values())
        )[0]
        word = ''.join(random.choices(english_letter_freq, k=length))
        random_strings.append(word)
    
    return random_strings


if __name__ == "__main__":
    import json
    corpus, diagnostics = load_brown_corpus(target_n=5000, frequency_weighted=True)
    
    with open('geofont_corpus_5k.txt', 'w') as f:
        for word in corpus:
            f.write(word + '\n')
    print(f"\n[Saved] geofont_corpus_5k.txt ({len(corpus)} words)", file=sys.stderr)
