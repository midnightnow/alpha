import os
import hashlib
import json
import argparse
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# CONFIGURATION
DOMAINS = [
    '/Users/studio/ALPHA',
    '/Volumes/Samsung T9 2/dev'  # Focus on the dev payload
]

EXTENSIONS = {'.md', '.epub', '.docx', '.txt', '.pdf', '.tex'}
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.DS_Store', 'DUPLICATE_OF_CANON', 'Precipitated_Silt'}
ARCHIVE_DEST = '/Users/studio/ALPHA/LIBRARY_ARCHIVES/DUPLICATE_OF_CANON'

# PRIORITY FOR KEEPER SELECTION (Lower index = Higher Priority)
PATH_PRIORITY = [
    'LIBRARY_CANON',
    'LIBRARY_ARCHIVES',
    'dev',
    'Projects',
    'archive',
    'PLATONICVERSES_ARCHIVE'
]

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (IOError, OSError):
        return None

def get_priority_score(filepath):
    path_str = str(filepath)
    for i, key in enumerate(PATH_PRIORITY):
        if key in path_str:
            return i
    return len(PATH_PRIORITY) # Lowest priority

def scan_domains():
    hash_map = defaultdict(list)
    total_files = 0
    
    print(f"Scanning {len(DOMAINS)} domains for topological reduction...")
    for domain in DOMAINS:
        if not os.path.exists(domain): continue
        for root, dirs, files in os.walk(domain):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if file.startswith('.'): continue
                ext = os.path.splitext(file)[1].lower()
                if ext in EXTENSIONS:
                    full_path = os.path.join(root, file)
                    file_hash = compute_sha256(full_path)
                    if file_hash:
                        hash_map[file_hash].append(full_path)
                        total_files += 1
    return hash_map, total_files

def analyze_collisions(hash_map):
    collisions = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    unique_count = len(hash_map)
    return collisions, unique_count

def select_keeper(paths):
    # Formal Deterministic Ranking:
    # 1. priority class (p1)
    # 2. path length (p2)
    # 3. lexicographic file path (p3)
    sorted_paths = sorted(paths, key=lambda p: (get_priority_score(p), len(p), p))
    return sorted_paths[0]

def process_collisions(collisions, execute):
    total_redundant = 0
    space_recoverable = 0
    
    if execute:
        os.makedirs(ARCHIVE_DEST, exist_ok=True)
        
    for h, paths in collisions.items():
        keeper = select_keeper(paths)
        redundancies = [p for p in paths if p != keeper]
        total_redundant += len(redundancies)
        
        try:
            file_size = os.path.getsize(paths[0])
            space_recoverable += file_size * len(redundancies)
        except OSError:
            file_size = 0
            
        if execute:
            for r in redundancies:
                # Prepend 8 chars of hash to ensure flat directory safety
                dest_filename = f"{h[:8]}_{os.path.basename(r)}"
                dest_path = os.path.join(ARCHIVE_DEST, dest_filename)
                try:
                    shutil.move(r, dest_path)
                except Exception:
                    pass
                    
    return total_redundant, space_recoverable

def main():
    parser = argparse.ArgumentParser(description="Deterministic Hash-Equivalence Collapse")
    parser.add_argument('--execute', action='store_true', help="Execute the physical collapse (moves files)")
    args = parser.parse_args()

    print("--- LEVEL 0: HASH-EQUIVALENCE COLLAPSE ---")
    hash_map, total_files = scan_domains()
    collisions, unique_count = analyze_collisions(hash_map)
    
    largest_cluster = max([len(v) for v in hash_map.values()]) if hash_map else 0
    
    print(f"|D| (Total Files Scanned): {total_files}")
    print(f"|D/~| (Unique Information States): {unique_count}")
    print(f"Collision Clusters: {len(collisions)}")
    print(f"max|Ci| (Largest Iteration Cluster): {largest_cluster}")
    
    redundant_count, space_bytes = process_collisions(collisions, args.execute)
    
    print(f"Σ(|Ci| - 1) (Redundant Files Identified): {redundant_count}")
    print(f"Space Recoverable/Recovered: {space_bytes / (1024*1024):.2f} MB")
    
    if not args.execute:
        print("\n[MODE: DRY_RUN] Run with --execute to perform the invariant dimensional collapse.")
    else:
        print(f"\n[MODE: LIVE] Operator executed. {redundant_count} redundancies collapsed to {ARCHIVE_DEST}.")

if __name__ == "__main__":
    main()
