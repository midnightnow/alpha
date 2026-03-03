#!/usr/bin/env python3
"""
Platonic Verses Consolidation Analysis
Identifies duplicates and best versions across scattered folders
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
import subprocess

# The 4 main Platonic Verses directories
DIRECTORIES = [
    "/Users/midnight/dev/0platonicverses",
    "/Users/midnight/dev/PLATONICVERSES", 
    "/Users/midnight/dev/Platonic Verses",
    "/Users/midnight/dev/radical-resonance_-root-42"
]

def get_file_hash(filepath):
    """Get MD5 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def get_file_info(filepath):
    """Get file size and modification time"""
    try:
        stat = os.stat(filepath)
        return {
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'path': filepath
        }
    except:
        return None

def find_markdown_files():
    """Find all .md files in Platonic directories"""
    files_by_name = defaultdict(list)
    
    for directory in DIRECTORIES:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.md'):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, directory)
                        
                        info = get_file_info(full_path)
                        if info:
                            info['directory'] = directory
                            info['relative_path'] = rel_path
                            info['hash'] = get_file_hash(full_path)
                            files_by_name[file].append(info)
    
    return files_by_name

def analyze_duplicates(files_by_name):
    """Identify duplicates and recommend best versions"""
    duplicates = {}
    unique_files = {}
    
    for filename, file_list in files_by_name.items():
        if len(file_list) > 1:
            # Group by hash to find identical content
            by_hash = defaultdict(list)
            for file_info in file_list:
                if file_info['hash']:
                    by_hash[file_info['hash']].append(file_info)
            
            # If all have same hash, they're identical
            if len(by_hash) == 1:
                # Pick most recent modification
                best_file = max(file_list, key=lambda x: x['mtime'])
                duplicates[filename] = {
                    'type': 'identical',
                    'best': best_file,
                    'duplicates': [f for f in file_list if f != best_file]
                }
            else:
                # Different content - pick largest/newest
                best_file = max(file_list, key=lambda x: (x['size'], x['mtime']))
                duplicates[filename] = {
                    'type': 'different_content', 
                    'best': best_file,
                    'alternatives': [f for f in file_list if f != best_file]
                }
        else:
            unique_files[filename] = file_list[0]
    
    return duplicates, unique_files

def main():
    print("🔍 Scanning all Platonic Verses directories...")
    files_by_name = find_markdown_files()
    
    print(f"📊 Found {sum(len(files) for files in files_by_name.values())} total .md files")
    print(f"📋 {len(files_by_name)} unique filenames")
    
    duplicates, unique_files = analyze_duplicates(files_by_name)
    
    print(f"\n🔄 DUPLICATES ANALYSIS:")
    print(f"   Identical content: {len([d for d in duplicates.values() if d['type'] == 'identical'])}")
    print(f"   Different content: {len([d for d in duplicates.values() if d['type'] == 'different_content'])}")
    print(f"   Unique files: {len(unique_files)}")
    
    # Show details for files with different content
    print(f"\n📝 FILES WITH DIFFERENT VERSIONS:")
    for filename, info in duplicates.items():
        if info['type'] == 'different_content':
            print(f"\n{filename}:")
            print(f"  ✅ BEST: {info['best']['relative_path']} ({info['best']['size']} bytes)")
            for alt in info['alternatives']:
                print(f"  📄 ALT:  {alt['relative_path']} ({alt['size']} bytes)")
    
    # Show some key Book 1 expansions
    book1_files = [f for f in files_by_name.keys() if 'Chapter_' in f and ('_1' in f or '_2' in f or '_3' in f)]
    print(f"\n📖 BOOK 1 EXPANDED CHAPTERS: {len(book1_files)} files")
    
    return duplicates, unique_files

if __name__ == "__main__":
    main()