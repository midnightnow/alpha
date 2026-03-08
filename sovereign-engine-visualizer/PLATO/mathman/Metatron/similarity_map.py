#!/usr/bin/env python3
"""
similarity_map.py  —  Canon Similarity Audit
=============================================

Purpose
-------
  Audit the 59-file Minimal Antichain Basis for near-duplicate pairs
  and topical clusters. READ-ONLY — no files are moved or deleted.

  This is a measurement pass, not a projection pass.
  Output is used to inform Level 3 (sequencing, cross-reference).

Algorithm
---------
  Two-stage pipeline:

  Stage 1 — MinHash LSH sieve (fast)
    Decomposes each document into k-gram shingles.
    Generates 128-hash MinHash signature per document.
    Identifies candidate pairs where Jaccard similarity > threshold.
    O(N * M) where N=128 hashes, M=59 documents.

  Stage 2 — TF-IDF cosine (for all pairs, fast at m=59)
    Builds TF-IDF matrix over full corpus vocabulary.
    Computes full 59x59 cosine similarity matrix.
    O(m^2 * V) where V = vocabulary size, trivial at m=59.

  LCS / edit distance is NOT used.
  Rationale: at 20KB per file, O(L^2) per pair = ~400M ops per pair,
  ~685B ops total. Jaccard + cosine gives sufficient signal at O(N*M).

Output
------
  SIMILARITY_MATRIX.csv     — 59x59 pairwise cosine similarity
  SIMILARITY_REPORT.json    — ranked pairs + cluster candidates
  SIMILARITY_REPORT.md      — human-readable summary
  similarity_heatmap.png    — visual distance matrix (if matplotlib available)

Usage
-----
  python similarity_map.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON
  python similarity_map.py --input-dir ... --threshold 0.3
  python similarity_map.py --input-dir ... --no-plot
"""

import os
import re
import sys
import json
import csv
import math
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EXTENSIONS: frozenset = frozenset({
    ".md", ".epub", ".docx", ".txt", ".pdf", ".tex"
})

# MinHash parameters
MINHASH_N:   int = 128    # number of hash functions
SHINGLE_K:   int = 5      # character n-gram size

# Default similarity threshold for flagging pairs
DEFAULT_THRESHOLD: float = 0.30

# Large prime for hash function family
_P = (1 << 31) - 1   # Mersenne prime 2^31 - 1
_M = (1 << 32)


# ---------------------------------------------------------------------------
# Text normalisation
# ---------------------------------------------------------------------------

def normalise(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def load_normalised(path: str):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()
    except (IOError, OSError):
        return None
    return normalise(raw)


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def collect_files(directory: str) -> list:
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for fname in sorted(filenames):
            if Path(fname).suffix.lower() in EXTENSIONS:
                files.append(os.path.join(dirpath, fname))
    return sorted(files)


# ---------------------------------------------------------------------------
# MinHash
# ---------------------------------------------------------------------------

def _shingles(text: str, k: int) -> set:
    return {text[i:i+k] for i in range(len(text) - k + 1)}


def _hash_family(n: int):
    """
    Generate n independent hash functions of the form:
        h(x) = (a*x + b) mod p mod m
    using fixed seeds for reproducibility.
    """
    rng_state = 42
    params = []
    for _ in range(n):
        rng_state = (rng_state * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        a = (rng_state >> 33) | 1          # odd, non-zero
        rng_state = (rng_state * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        b = rng_state >> 33
        params.append((a, b))
    return params


_HASH_PARAMS = _hash_family(MINHASH_N)


def minhash_signature(text: str) -> list:
    """Compute MinHash signature of length MINHASH_N for text."""
    shingles = _shingles(text, SHINGLE_K)
    if not shingles:
        return [0] * MINHASH_N

    # Hash each shingle to an integer
    hashed = []
    for s in shingles:
        h = int(hashlib.md5(s.encode()).hexdigest(), 16) % _P
        hashed.append(h)

    sig = []
    for a, b in _HASH_PARAMS:
        min_val = min((a * x + b) % _P for x in hashed)
        sig.append(min_val)
    return sig


def jaccard_from_minhash(sig_a: list, sig_b: list) -> float:
    """Estimate Jaccard similarity from MinHash signatures."""
    matches = sum(1 for x, y in zip(sig_a, sig_b) if x == y)
    return matches / MINHASH_N


# ---------------------------------------------------------------------------
# TF-IDF cosine similarity
# ---------------------------------------------------------------------------

def tokenise(text: str) -> list:
    """Split on whitespace, filter short tokens."""
    return [t for t in text.split() if len(t) > 2]


def build_tfidf_matrix(documents: list) -> list:
    """
    documents: list of (path, norm_text)
    Returns: list of {term: tfidf_weight} dicts, one per document.
    """
    m = len(documents)

    # Term frequency per document
    tf_dicts = []
    for _, text in documents:
        tokens = tokenise(text)
        if not tokens:
            tf_dicts.append({})
            continue
        counts = defaultdict(int)
        for t in tokens:
            counts[t] += 1
        total = len(tokens)
        tf_dicts.append({t: c / total for t, c in counts.items()})

    # Document frequency
    df = defaultdict(int)
    for tf in tf_dicts:
        for term in tf:
            df[term] += 1

    # IDF
    idf = {term: math.log((m + 1) / (count + 1)) + 1
           for term, count in df.items()}

    # TF-IDF
    tfidf = []
    for tf in tf_dicts:
        vec = {term: tf[term] * idf[term] for term in tf}
        tfidf.append(vec)

    return tfidf


def cosine(vec_a: dict, vec_b: dict) -> float:
    if not vec_a or not vec_b:
        return 0.0
    dot = sum(vec_a.get(t, 0.0) * vec_b.get(t, 0.0) for t in vec_a)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_similarity_matrix(tfidf: list) -> list:
    """Returns m x m cosine similarity matrix."""
    m = len(tfidf)
    matrix = [[0.0] * m for _ in range(m)]
    for i in range(m):
        matrix[i][i] = 1.0
        for j in range(i + 1, m):
            s = cosine(tfidf[i], tfidf[j])
            matrix[i][j] = s
            matrix[j][i] = s
    return matrix


# ---------------------------------------------------------------------------
# Cluster detection (connected components at threshold)
# ---------------------------------------------------------------------------

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


def find_clusters(matrix: list, threshold: float) -> list:
    """
    Returns list of clusters (each a list of doc indices).
    Two documents are in the same cluster if cosine similarity >= threshold
    (single-linkage via Union-Find).
    """
    n = len(matrix)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] >= threshold:
                uf.union(i, j)

    groups = defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)

    return [sorted(members) for members in groups.values()]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def write_csv(documents: list, matrix: list, path: str) -> None:
    labels = [os.path.basename(p) for p, _ in documents]
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([''] + labels)
        for i, row in enumerate(matrix):
            writer.writerow([labels[i]] + [f"{v:.4f}" for v in row])
    print(f"  CSV matrix: {path}")


def write_json_report(documents: list, matrix: list,
                      clusters: list, threshold: float, path: str) -> None:
    m = len(documents)
    labels = [os.path.basename(p) for p, _ in documents]

    # Ranked pairs above threshold
    pairs = []
    for i in range(m):
        for j in range(i + 1, m):
            s = matrix[i][j]
            if s >= threshold:
                pairs.append({
                    "doc_a":      documents[i][0],
                    "doc_b":      documents[j][0],
                    "similarity": round(s, 4),
                })
    pairs.sort(key=lambda x: -x["similarity"])

    cluster_records = []
    for members in clusters:
        if len(members) == 1:
            continue
        cluster_records.append({
            "size":    len(members),
            "members": [documents[i][0] for i in members],
            "pairwise_similarities": [
                {
                    "a": documents[i][0],
                    "b": documents[j][0],
                    "similarity": round(matrix[i][j], 4),
                }
                for ii, i in enumerate(members)
                for j in members[ii+1:]
            ],
        })

    report = {
        "timestamp":        datetime.now().isoformat(),
        "total_documents":  m,
        "threshold":        threshold,
        "pairs_above_threshold": len(pairs),
        "clusters_above_threshold": len(cluster_records),
        "singleton_count":  sum(1 for c in clusters if len(c) == 1),
        "ranked_pairs":     pairs,
        "clusters":         cluster_records,
    }

    with open(path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  JSON report: {path}")


def write_md_report(documents: list, matrix: list,
                    clusters: list, threshold: float, path: str) -> None:
    m = len(documents)
    lines = [
        "# Canon Similarity Audit — Level 2",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"*Metric: TF-IDF cosine similarity*",
        f"*Threshold: {threshold}*",
        "",
        "## Summary",
        f"- Documents audited: {m}",
    ]

    pairs_above = [(i, j, matrix[i][j])
                   for i in range(m)
                   for j in range(i+1, m)
                   if matrix[i][j] >= threshold]
    pairs_above.sort(key=lambda x: -x[2])

    non_singleton = [c for c in clusters if len(c) > 1]

    lines += [
        f"- Pairs above threshold ({threshold}): {len(pairs_above)}",
        f"- Clusters (size > 1): {len(non_singleton)}",
        f"- Singletons (no near-duplicate): {m - sum(len(c) for c in non_singleton)}",
        "",
    ]

    if not pairs_above:
        lines += [
            "## Result",
            f"**No pairs found above similarity threshold {threshold}.**",
            "The Minimal Antichain Basis is confirmed semantically distinct at this threshold.",
            "",
        ]
    else:
        lines += ["## Pairs Above Threshold", ""]
        for i, j, s in pairs_above:
            pi = os.path.basename(documents[i][0])
            pj = os.path.basename(documents[j][0])
            lines.append(f"- `{pi}` ↔ `{pj}`  — similarity: **{s:.4f}**")
        lines.append("")

        if non_singleton:
            lines += ["## Clusters", ""]
            for k, members in enumerate(non_singleton, 1):
                lines.append(f"### Cluster {k} ({len(members)} documents)")
                for idx in members:
                    lines.append(f"- `{os.path.basename(documents[idx][0])}`")
                lines.append("")

    lines += [
        "## Interpretation",
        "",
        "Similarity >= 0.70 : strong topical overlap — inspect for hidden duplicates.",
        "Similarity 0.30–0.69: related content — useful for sequencing in Level 3.",
        "Similarity < 0.30  : distinct documents.",
        "",
        "This report is READ-ONLY. No files have been moved.",
        "To archive near-duplicates, run `near_duplicate_cluster.py` with `--execute`.",
    ]

    with open(path, 'w') as f:
        f.write("\n".join(lines))
    print(f"  Markdown report: {path}")


def print_summary(documents: list, matrix: list,
                  clusters: list, threshold: float) -> None:
    m = len(documents)
    pairs_above = [(i, j, matrix[i][j])
                   for i in range(m)
                   for j in range(i+1, m)
                   if matrix[i][j] >= threshold]
    pairs_above.sort(key=lambda x: -x[2])

    sep = "=" * 64
    print(sep)
    print("  CANON SIMILARITY AUDIT  —  LEVEL 2")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Threshold: {threshold}  |  Metric: TF-IDF cosine")
    print(sep)
    print(f"  Documents:              {m}")
    print(f"  Pairs above threshold:  {len(pairs_above)}")
    print(f"  Clusters (size > 1):    {sum(1 for c in clusters if len(c) > 1)}")
    print(sep)

    if pairs_above:
        print("\n  TOP SIMILAR PAIRS\n")
        for i, j, s in pairs_above[:20]:
            pi = os.path.basename(documents[i][0])
            pj = os.path.basename(documents[j][0])
            bar = "█" * int(s * 20)
            print(f"  {s:.3f} {bar:<20}  {pi}")
            print(f"                           ↔ {pj}")
        if len(pairs_above) > 20:
            print(f"  ... and {len(pairs_above) - 20} more pairs. See JSON report.")
        print()
    else:
        print(f"\n  No pairs above threshold {threshold}.")
        print("  Canon is confirmed semantically distinct at this threshold.\n")


# ---------------------------------------------------------------------------
# Optional: heatmap plot
# ---------------------------------------------------------------------------

def plot_heatmap(documents: list, matrix: list, path: str) -> None:
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
    except ImportError:
        print("  matplotlib not available — skipping heatmap.")
        return

    m = len(documents)
    labels = [os.path.basename(p)[:30] for p, _ in documents]

    fig, ax = plt.subplots(figsize=(max(12, m // 3), max(10, m // 3)))
    im = ax.imshow(matrix, cmap='YlOrRd', vmin=0, vmax=1, aspect='auto')
    plt.colorbar(im, ax=ax, label='Cosine Similarity')

    ax.set_xticks(range(m))
    ax.set_yticks(range(m))
    ax.set_xticklabels(labels, rotation=90, fontsize=6)
    ax.set_yticklabels(labels, fontsize=6)
    ax.set_title("Canon Similarity Matrix — TF-IDF Cosine", fontsize=10)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Heatmap: {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Canon Similarity Audit — read-only measurement pass",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input-dir", required=True, metavar="DIR",
        help="Directory to scan (e.g. /Users/studio/ALPHA/LIBRARY_CANON)"
    )
    parser.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help=f"Similarity threshold for flagging pairs (default: {DEFAULT_THRESHOLD})"
    )
    parser.add_argument(
        "--no-plot", action="store_true",
        help="Skip heatmap generation"
    )
    args = parser.parse_args()

    # Collect
    print(f"\n  Scanning: {args.input_dir}")
    paths = collect_files(args.input_dir)
    print(f"  {len(paths)} files found.\n")

    # Load and normalise
    print("  Loading and normalising...")
    documents = []
    for p in paths:
        norm = load_normalised(p)
        if norm:
            documents.append((p, norm))
        else:
            print(f"  SKIP (unreadable): {p}")

    m = len(documents)
    print(f"  {m} documents loaded.\n")

    if m < 2:
        print("  Need at least 2 documents. Exiting.")
        sys.exit(1)

    # MinHash sieve (informational — flags candidates for manual review)
    print("  Computing MinHash signatures...")
    signatures = [minhash_signature(norm) for _, norm in documents]

    minhash_candidates = []
    for i in range(m):
        for j in range(i + 1, m):
            j_est = jaccard_from_minhash(signatures[i], signatures[j])
            if j_est >= 0.15:
                minhash_candidates.append((i, j, j_est))

    print(f"  MinHash sieve: {len(minhash_candidates)} candidate pairs "
          f"(Jaccard >= 0.15) out of {m*(m-1)//2} total.\n")

    # TF-IDF cosine matrix
    print("  Building TF-IDF matrix...")
    tfidf = build_tfidf_matrix(documents)

    print("  Computing cosine similarity matrix...")
    matrix = build_similarity_matrix(tfidf)

    # Cluster detection
    clusters = find_clusters(matrix, args.threshold)

    # Output
    print_summary(documents, matrix, clusters, args.threshold)

    write_csv(documents, matrix, "SIMILARITY_MATRIX.csv")
    write_json_report(documents, matrix, clusters, args.threshold,
                      "SIMILARITY_REPORT.json")
    write_md_report(documents, matrix, clusters, args.threshold,
                    "SIMILARITY_REPORT.md")

    if not args.no_plot:
        plot_heatmap(documents, matrix, "similarity_heatmap.png")

    print("\n  READ-ONLY audit complete. No files modified.")
    print("  Review SIMILARITY_REPORT.md before any archival decisions.\n")


if __name__ == "__main__":
    main()
