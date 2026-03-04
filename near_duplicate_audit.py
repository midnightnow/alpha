#!/usr/bin/env python3
"""
LEVEL 2: NEAR-DUPLICATE CLUSTERING (AUDIT VERSION)
Identifies clusters in B where delta(di, dj) <= 0.10.
Non-destructive: Generates NEAR_DUPLICATE_REPORT.md.
"""

import os
import sys
import json
import difflib
import argparse
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import re

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
EXTENSIONS = {'.md', '.epub', '.docx', '.txt', '.pdf', '.tex'}

# ---------------------------------------------------------------------------
# Core Computations
# ---------------------------------------------------------------------------
def normalise(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_normalised(path: str) -> str | None:
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()
    except (IOError, OSError):
        return None
    return normalise(raw)

def collect_files(directory: str) -> list:
    files = []
    for dirpath, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "NEAR_DUPLICATES", "DUPLICATE_OF_CANON", "NonMaximal_Nodes", "Precipitated_Silt"}]
        for fname in filenames:
            if Path(fname).suffix.lower() in EXTENSIONS:
                files.append(os.path.join(dirpath, fname))
    return files

def calculate_similarity(text1, text2):
    """Normalized similarity based on SequenceMatcher (LCS heuristic)."""
    return difflib.SequenceMatcher(None, text1, text2).ratio()

# ---------------------------------------------------------------------------
# Logic for Level 2 (Strict epsilon-graph component finding for Reporting)
# ---------------------------------------------------------------------------
def build_epsilon_graph(documents, epsilon):
    """Finds all connected components where similarity >= (1 - epsilon)."""
    clusters = []
    processed = set()
    n = len(documents)
    
    threshold = 1.0 - epsilon
    
    for i in range(n):
        if i in processed: continue
        current_cluster = [i]
        processed.add(i)
        
        for j in range(i + 1, n):
            if j in processed: continue
            
            sim = calculate_similarity(documents[i][1], documents[j][1])
            if sim >= threshold:
                current_cluster.append(j)
                processed.add(j)
        
        if len(current_cluster) > 1:
            clusters.append(current_cluster)
            
    return clusters

# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Level 2: Near-Duplicate Clustering (Audit Version)")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--epsilon", type=float, default=0.10)
    args = parser.parse_args()
    
    paths = collect_files(args.input_dir)
    print(f"Collected {len(paths)} canonical documents...")
    
    docs = [] # [(path, norm, size)]
    for p in paths:
        norm = load_normalised(p)
        if norm and len(norm) > 10:
            try:
                size = os.path.getsize(p)
                docs.append((p, norm, size))
            except OSError:
                pass

    print(f"Normalised {len(docs)} documents. Computing pairwise metric space (O(N^2))...")
    
    clusters = build_epsilon_graph(docs, args.epsilon)
    
    # Analyze the clusters
    archive_candidates = sum([len(c)-1 for c in clusters])
    largest_cluster = max([len(c) for c in clusters]) if clusters else 0
    total_clusters = len(clusters)
    
    print("================================================================")
    print("  EAR-DUPLICATE POSET  —  LEVEL 2 AUDIT REPORT")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("================================================================")
    print(f"  Threshold (epsilon)      : {args.epsilon}")
    print(f"  Total documents checked  : {len(docs)}")
    print(f"  Clusters found           : {total_clusters}")
    print(f"  Candidates for review    : {archive_candidates}")
    print(f"  Largest cluster size     : {largest_cluster}")
    print("================================================================\n")
    
    md_lines = [
        "# Level 2: Near-Duplicate Clustering Audit Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Invariants",
        f"- Threshold $\\epsilon$: {args.epsilon}",
        f"- Documents processed: {len(docs)}",
        f"- Clusters identified: {total_clusters}",
        f"- Candidates for internal review: {archive_candidates}",
        f"- Largest cluster size: {largest_cluster}",
        ""
    ]
    
    cluster_idx = 1
    for c in clusters:
        # Sort internal cluster by size descending so max element is top
        c_sorted = sorted(c, key=lambda idx: -docs[idx][2])
        
        rep_path = docs[c_sorted[0]][0]
        md_lines.append(f"## Cluster {cluster_idx} (Potential Rep: `{os.path.basename(rep_path)}`)")
        md_lines.append(f"*(All files > {int((1.0 - args.epsilon)*100)}% identical)*\n")
        
        md_lines.append("| Document | Path |")
        md_lines.append("|----------|------|")
        
        for idx in c_sorted:
            path = docs[idx][0]
            md_lines.append(f"| `{os.path.basename(path)}` | `{path}` |")
            
        md_lines.append("")
        cluster_idx += 1
        
    with open("NEAR_DUPLICATE_REPORT.md", "w") as f:
        f.write("\n".join(md_lines))
        
    print("  Report written: NEAR_DUPLICATE_REPORT.md\n")

if __name__ == "__main__":
    main()
