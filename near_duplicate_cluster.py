#!/usr/bin/env python3
"""
near_duplicate_cluster.py  —  Level 2: Near-Duplicate Clustering B -> B_reduced
=============================================================================

Formal model
------------
  Metric Space:   B = { b_1, ..., b_m } (Minimal Antichain Basis)
  Distance:       delta(b_i, b_j) = 1 - similarity(b_i, b_j)
  Similarity:     SequenceMatcher ratio (approximation of normalized LCS)
  
  Clustering:     b_i ~_eps b_j <=> delta(b_i, b_j) <= epsilon
                  Connected components (single-linkage) via Union-Find.
  
  Representative: rep(K) = argmin_{b in K} rho(b)
  Total order:    rho(b) = (priority_class(b), -len(b), path_string(b))

Execution
---------
  Safe, idempotent, two-phase cross-device commit archival of non-reps.

Usage
-----
  python near_duplicate_cluster.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON --epsilon 0.10 --dry-run
  python near_duplicate_cluster.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON --epsilon 0.10 --execute
"""

import os
import sys
import re
import math
import json
import difflib
import argparse
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EXTENSIONS = frozenset({".md", ".epub", ".docx", ".txt", ".pdf", ".tex"})

ARCHIVE_DEST = "/Users/studio/ALPHA/LIBRARY_ARCHIVES/NEAR_DUPLICATES"

# Default priorities for representative selection
PRIORITY_RULES = [
    ("LIBRARY_CANON",          0),
    ("LIBRARY_ARCHIVES",       1),
    ("/dev/",                  2),
    ("/Projects/",             3),
    ("/archive/",              4),
    ("PLATONICVERSES_ARCHIVE", 5),
]
DEFAULT_PRIORITY = 9

# ---------------------------------------------------------------------------
# Core Computations
# ---------------------------------------------------------------------------

def priority_class(path: str) -> int:
    for fragment, cls in PRIORITY_RULES:
        if fragment in path:
            return cls
    return DEFAULT_PRIORITY

def rho(path: str, size: int) -> tuple:
    # Notice: -size (favor larger)
    return (priority_class(path), -size, path)

def sha256(path: str):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except (IOError, OSError):
        return None

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

def compute_similarity(norm_i: str, norm_j: str) -> float:
    # difflib's ratio is 2.0*M / T (M = matches, T = total elements)
    # Serves as a fast pseudo-LCS Normalized Edit Similarity
    return difflib.SequenceMatcher(None, norm_i, norm_j).ratio()

# ---------------------------------------------------------------------------
# Union-Find
# ---------------------------------------------------------------------------

class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
    
    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
        
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Deterministic merge to smaller index
            if root_i < root_j:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j

def get_clusters(uf, elements):
    clusters = defaultdict(list)
    for e in elements:
        clusters[uf.find(e)].append(e)
    return list(clusters.values())

# ---------------------------------------------------------------------------
# Idempotent Move Operations
# ---------------------------------------------------------------------------

def _remove_silent(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass

def _safe_move(src: str, dest: str) -> tuple:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".tmp"

    try:
        shutil.copy2(src, tmp)
    except (IOError, OSError, shutil.Error) as e:
        _remove_silent(tmp)
        return (False, f"copy failed: {e}")

    src_digest = sha256(src)
    tmp_digest = sha256(tmp)
    if src_digest != tmp_digest:
        _remove_silent(tmp)
        return (False, f"hash mismatch after copy")

    try:
        os.replace(tmp, dest)
    except OSError as e:
        _remove_silent(tmp)
        return (False, f"rename failed: {e}")

    try:
        os.remove(src)
    except OSError as e:
        return (False, f"dest written+verified but source delete failed: {e}")

    return (True, "")

# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def report_invariants(docs, clusters, representatives, distances, epsilon, dry_run):
    archive_candidates = sum([len(c)-1 for c in clusters if len(c) > 1])
    largest_cluster_size = max([len(c) for c in clusters]) if clusters else 0
    
    intra_dists = []
    for (i, j), d in distances.items():
        if d <= epsilon:
            intra_dists.append(d)
    avg_intra = (sum(intra_dists) / len(intra_dists)) if intra_dists else 0.0
    
    rep_size = len(representatives)
    clus_found = len([c for c in clusters if len(c) > 1])
    
    print("================================================================")
    print("  EAR-DUPLICATE POSET  —  LEVEL 2 REPORT")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("================================================================")
    print(f"  Threshold (epsilon)      : {epsilon}")
    print(f"  Total documents checked  : {len(docs)}")
    print(f"  Clusters found           : {clus_found}")
    print(f"  Representatives (kept)   : {rep_size}")
    print(f"  Candidates for archive   : {archive_candidates}")
    print(f"  Largest cluster size     : {largest_cluster_size}")
    print(f"  Avg intra-cluster dist   : {avg_intra:.4f}")
    print("================================================================\n")
    
    md_lines = [
        "# Level 2: Near-Duplicate Clustering Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Invariants",
        f"- Threshold $\\epsilon$: {epsilon}",
        f"- Documents processed: {len(docs)}",
        f"- Clusters identified: {clus_found}",
        f"- Representatives (kept): {rep_size}",
        f"- Candidates for archive: {archive_candidates}",
        f"- Largest cluster size: {largest_cluster_size}",
        f"- Avg intra-cluster distance: {avg_intra:.4f}",
        ""
    ]
    
    cluster_idx = 1
    actions = []
    
    for c in clusters:
        if len(c) == 1:
            actions.append({"path": docs[c[0]][0], "action": "KEEP", "distance": 0.0, "cluster": f"Singleton_{docs[c[0]][0]}"})
            continue
            
        rep_idx = representatives[tuple(c)]
        rep_path = docs[rep_idx][0]
        md_lines.append(f"## Cluster {cluster_idx} (Representative: `{os.path.basename(rep_path)}`)")
        md_lines.append("| Document | Distance to Rep | Action |")
        md_lines.append("|----------|-----------------|--------|")
        
        for idx in sorted(c, key=lambda x: distances.get((min(x, rep_idx), max(x, rep_idx)), 0.0)):
            path = docs[idx][0]
            dist = distances.get((min(idx, rep_idx), max(idx, rep_idx)), 0.0) if idx != rep_idx else 0.0
            
            action = "KEEP" if idx == rep_idx else "ARCHIVE"
            md_lines.append(f"| `{os.path.basename(path)}` | {dist:.3f} | {action} |")
            
            actions.append({
                "path": path,
                "action": action,
                "distance": dist,
                "cluster": f"Cluster_{cluster_idx}",
                "rep": rep_path if action == "ARCHIVE" else None
            })
            
        md_lines.append("")
        cluster_idx += 1
        
    with open("NEAR_DUPLICATE_REPORT.md", "w") as f:
        f.write("\n".join(md_lines))
        
    json_rep = {
        "timestamp": datetime.now().isoformat(),
        "epsilon": epsilon,
        "total_documents": len(docs),
        "clusters_found": clus_found,
        "representatives": rep_size,
        "archive_candidates": archive_candidates,
        "largest_cluster_size": largest_cluster_size,
        "avg_intra_cluster_distance": avg_intra,
        "actions": actions
    }
    with open("NEAR_DUPLICATE_REPORT.json", "w") as f:
        json.dump(json_rep, f, indent=2)
        
    print("  Reports written: NEAR_DUPLICATE_REPORT.md | NEAR_DUPLICATE_REPORT.json\n")
    return actions

# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Level 2: Near-Duplicate Clustering")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--epsilon", type=float, default=0.10)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    
    if not args.dry_run and not args.execute:
        print("Specify --dry-run or --execute")
        sys.exit(1)
        
    paths = collect_files(args.input_dir)
    print(f"Collected {len(paths)} target documents...")
    
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
    
    distances = {}
    uf = UnionFind(range(len(docs)))
    
    # Single-pass dense comparison
    for i in range(len(docs)):
        for j in range(i+1, len(docs)):
            sim = compute_similarity(docs[i][1], docs[j][1])
            d = 1.0 - sim
            distances[(i, j)] = d
            if d <= args.epsilon:
                uf.union(i, j)
                
    clusters = get_clusters(uf, range(len(docs)))
    
    representatives = {}
    for c in clusters:
        # argmin_b rho(b)
        rep = min(c, key=lambda idx: rho(docs[idx][0], docs[idx][2]))
        representatives[tuple(c)] = rep
        
    actions = report_invariants(docs, clusters, representatives, distances, args.epsilon, args.dry_run)
    
    if args.execute:
        os.makedirs(ARCHIVE_DEST, exist_ok=True)
        moved = 0
        for act in actions:
            if act["action"] == "ARCHIVE":
                src = act["path"]
                rep_hash = sha256(act["rep"])[:8] if act["rep"] else "00000000"
                stem, ext = os.path.splitext(os.path.basename(src))
                dest_name = f"{stem}__{act['cluster']}_{rep_hash}{ext}"
                dest = os.path.join(ARCHIVE_DEST, dest_name)
                
                print(f"  Archiving Variant -> {dest_name}")
                success, msg = _safe_move(src, dest)
                if success:
                    moved += 1
                else:
                    print(f"  Fail ({src}): {msg}")
        print(f"\n  Successfully executed {moved} physical archival transfers.")
    else:
        print("  DRY-RUN Complete. Review NEAR_DUPLICATE_REPORT.md and rerun with --execute")

if __name__ == "__main__":
    main()
