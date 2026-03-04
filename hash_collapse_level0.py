import os
import hashlib
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# CONFIGURATION
DOMAINS = [
    '/Users/studio/ALPHA',
    '/Volumes/Samsung T9 2'
]

EXTENSIONS = {'.md', '.epub', '.docx', '.txt', '.pdf', '.tex'}
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.DS_Store'}

# PRIORITY FOR KEEPER SELECTION (Higher index = Higher Priority)
PATH_PRIORITY = [
    'LIBRARY_CANON',
    'LIBRARY_ARCHIVES',
    'dev',
    'Projects',
    'archive',
    'PLATONICVERSES_ARCHIVE'
]

DRY_RUN = True  # Set to False to execute moves

def compute_sha256(filepath):
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (IOError, OSError):
        return None

def get_priority_score(filepath):
    """Assign priority score based on path containment."""
    path_str = str(filepath)
    for i, key in enumerate(reversed(PATH_PRIORITY)):
        if key in path_str:
            return i
    return 0

def scan_domains():
    """Walk domains and collect file hashes."""
    hash_map = defaultdict(list)
    total_files = 0
    
    print(f"Scanning {len(DOMAINS)} domains...")
    
    for domain in DOMAINS:
        if not os.path.exists(domain):
            print(f"Warning: Domain not found: {domain}")
            continue
            
        for root, dirs, files in os.walk(domain):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in EXTENSIONS:
                    full_path = os.path.join(root, file)
                    file_hash = compute_sha256(full_path)
                    
                    if file_hash:
                        hash_map[file_hash].append(full_path)
                        total_files += 1
                        
    return hash_map, total_files

def analyze_collisions(hash_map):
    """Identify equivalence classes with cardinality > 1."""
    collisions = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    unique_count = len(hash_map) - len(collisions)
    return collisions, unique_count

def select_keeper(paths):
    """Select the canonical path based on priority."""
    # Sort by priority score (descending), then by path length (shorter preferred)
    sorted_paths = sorted(paths, key=lambda p: (get_priority_score(p), -len(p)), reverse=True)
    return sorted_paths[0]

def generate_audit(collisions, output_file='/Users/studio/ALPHA/HASH_COLLAPSE_AUDIT.md'):
    """Generate the formal audit report."""
    total_redundant = 0
    space_recoverable = 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# HASH-EQUIVALENCE COLLAPSE AUDIT\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write("## I. Equivalence Classes (Collisions)\n\n")
        
        for h, paths in collisions.items():
            keeper = select_keeper(paths)
            redundancies = [p for p in paths if p != keeper]
            total_redundant += len(redundancies)
            
            # Estimate size from first file
            try:
                file_size = os.path.getsize(paths[0])
                space_recoverable += file_size * len(redundancies)
            except OSError:
                file_size = 0
            
            f.write(f"### Hash: `{h[:16]}...`\n")
            f.write(f"- **Cardinality:** {len(paths)}\n")
            f.write(f"- **Keeper:** `{keeper}`\n")
            f.write(f"- **Redundancies:** {len(redundancies)}\n")
            f.write(f"- **Potential Space Recovery:** {file_size * len(redundancies) / 1024:.2f} KB\n\n")
            
            if not DRY_RUN:
                # Execute Move Logic here if required
                pass
            
    return total_redundant, space_recoverable

def main():
    print("--- LEVEL 0: HASH-EQUIVALENCE COLLAPSE ---")
    hash_map, total_files = scan_domains()
    collisions, unique_count = analyze_collisions(hash_map)
    
    print(f"Total Files Scanned: {total_files}")
    print(f"Unique Information States: {unique_count}")
    print(f"Collision Clusters: {len(collisions)}")
    
    redundant_count, space_bytes = generate_audit(collisions)
    
    print(f"Redundant Files Identified: {redundant_count}")
    print(f"Estimated Space Recoverable: {space_bytes / (1024*1024):.2f} MB")
    print(f"Audit Log Generated: HASH_COLLAPSE_AUDIT.md")
    
    if DRY_RUN:
        print("\n[MODE: DRY_RUN] No files were moved. Review audit log.")
    else:
        print("\n[MODE: LIVE] Redundancies processed.")

if __name__ == "__main__":
    main()
