#!/usr/bin/env python3
"""
Content Preservation Audit - Ensure ALL unique content is preserved
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict

# Original directories
ORIGINAL_DIRS = [
    "/Users/midnight/dev/0platonicverses",
    "/Users/midnight/dev/PLATONICVERSES", 
    "/Users/midnight/dev/Platonic Verses",
    "/Users/midnight/dev/radical-resonance_-root-42"
]

CONSOLIDATED_DIR = "/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES"

def get_file_hash(filepath):
    """Get MD5 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def scan_content_files(directory):
    """Find all content files (.md, .py, .json, .ts, .tsx, .js, .txt, .epub)"""
    content_files = {}
    
    if not os.path.exists(directory):
        return content_files
        
    for root, dirs, files in os.walk(directory):
        # Skip node_modules and .git
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
        
        for file in files:
            if file.endswith(('.md', '.py', '.json', '.ts', '.tsx', '.js', '.txt', '.epub', '.html', '.css')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, directory)
                
                file_hash = get_file_hash(full_path)
                if file_hash:
                    size = os.path.getsize(full_path)
                    content_files[rel_path] = {
                        'hash': file_hash,
                        'size': size,
                        'full_path': full_path
                    }
    
    return content_files

def find_missing_content():
    """Find any unique content that might be missing from consolidated"""
    print("🔍 Scanning all directories for content files...")
    
    # Scan all original directories
    all_original_files = {}
    for directory in ORIGINAL_DIRS:
        print(f"   Scanning {os.path.basename(directory)}...")
        files = scan_content_files(directory)
        for rel_path, info in files.items():
            key = f"{os.path.basename(directory)}:{rel_path}"
            all_original_files[key] = info
    
    # Scan consolidated directory
    print(f"   Scanning consolidated directory...")
    consolidated_files = scan_content_files(CONSOLIDATED_DIR)
    
    print(f"\n📊 AUDIT RESULTS:")
    print(f"   Original content files: {len(all_original_files)}")
    print(f"   Consolidated files: {len(consolidated_files)}")
    
    # Group by hash to find truly unique content
    original_by_hash = defaultdict(list)
    for key, info in all_original_files.items():
        original_by_hash[info['hash']].append((key, info))
    
    consolidated_hashes = set(info['hash'] for info in consolidated_files.values())
    
    # Find missing unique content
    missing_unique = []
    for file_hash, file_list in original_by_hash.items():
        if file_hash not in consolidated_hashes:
            # This hash is completely missing from consolidated
            # Pick the largest version
            best_file = max(file_list, key=lambda x: x[1]['size'])
            missing_unique.append(best_file)
    
    if missing_unique:
        print(f"\n⚠️  MISSING UNIQUE CONTENT: {len(missing_unique)} files")
        for key, info in missing_unique:
            print(f"   MISSING: {key} ({info['size']} bytes)")
            print(f"            {info['full_path']}")
        return missing_unique
    else:
        print(f"\n✅ ALL UNIQUE CONTENT PRESERVED")
        return []

def find_potentially_better_versions():
    """Find files where original might have better versions"""
    print(f"\n🔍 Checking for potentially better versions...")
    
    consolidated_files = scan_content_files(CONSOLIDATED_DIR)
    
    # Check each consolidated file against originals
    better_versions = []
    
    for cons_rel_path, cons_info in consolidated_files.items():
        # Look for same relative path in originals
        for orig_dir in ORIGINAL_DIRS:
            orig_path = os.path.join(orig_dir, cons_rel_path)
            if os.path.exists(orig_path):
                orig_hash = get_file_hash(orig_path)
                orig_size = os.path.getsize(orig_path)
                
                if orig_hash != cons_info['hash']:
                    # Different content - check if original is better
                    if orig_size > cons_info['size']:
                        better_versions.append({
                            'file': cons_rel_path,
                            'consolidated_size': cons_info['size'],
                            'original_size': orig_size,
                            'original_path': orig_path,
                            'original_dir': os.path.basename(orig_dir)
                        })
    
    if better_versions:
        print(f"\n📈 POTENTIALLY BETTER VERSIONS: {len(better_versions)}")
        for item in better_versions:
            print(f"   UPGRADE: {item['file']}")
            print(f"            Consolidated: {item['consolidated_size']} bytes")
            print(f"            {item['original_dir']}: {item['original_size']} bytes")
    else:
        print(f"\n✅ ALL BEST VERSIONS ALREADY USED")
    
    return better_versions

def main():
    print("🔍 CONTENT PRESERVATION AUDIT")
    print("=" * 50)
    
    missing = find_missing_content()
    better = find_potentially_better_versions()
    
    if missing or better:
        print(f"\n🚨 ACTION REQUIRED:")
        print(f"   Missing files: {len(missing)}")
        print(f"   Better versions available: {len(better)}")
        return missing, better
    else:
        print(f"\n✅ CONSOLIDATION IS COMPLETE AND OPTIMAL")
        return [], []

if __name__ == "__main__":
    main()