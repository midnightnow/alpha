#!/usr/bin/env python3
"""
Comprehensive Root42 and Root51 Content Audit
"""

import os
import hashlib
from pathlib import Path
import subprocess

ORIGINAL_DIRS = [
    "/Users/midnight/dev/0platonicverses",
    "/Users/midnight/dev/PLATONICVERSES", 
    "/Users/midnight/dev/Platonic Verses",
    "/Users/midnight/dev/radical-resonance_-root-42"
]

CONSOLIDATED_DIR = "/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES"

def find_root42_root51_content():
    """Find all Root42 and Root51 related content"""
    
    root_content = {
        'Root42': {},
        'Root51': {},
        'radical-resonance_-root-42': {},
        'radical-resonance_-root-51': {},
        'Root42-Transmission': {},
        'root_42_mathman-genesis': {}
    }
    
    for directory in ORIGINAL_DIRS:
        if not os.path.exists(directory):
            continue
            
        print(f"\n🔍 Scanning {directory} for Root42/Root51 content...")
        
        for root, dirs, files in os.walk(directory):
            # Check if this path contains root42/root51 content
            rel_path = os.path.relpath(root, directory)
            
            # Look for specific patterns
            for pattern in ['Root42', 'Root51', 'root-42', 'root-51', 'root_42', 'root42', 'root51']:
                if pattern.lower() in rel_path.lower():
                    
                    # Determine category
                    category = None
                    if 'root42' in rel_path.lower() and 'transmission' in rel_path.lower():
                        category = 'Root42-Transmission'
                    elif 'root_42_mathman' in rel_path.lower():
                        category = 'root_42_mathman-genesis'
                    elif 'radical-resonance' in rel_path.lower() and 'root-42' in rel_path.lower():
                        category = 'radical-resonance_-root-42'
                    elif 'radical-resonance' in rel_path.lower() and 'root-51' in rel_path.lower():
                        category = 'radical-resonance_-root-51'
                    elif 'root42' in rel_path.lower():
                        category = 'Root42'
                    elif 'root51' in rel_path.lower():
                        category = 'Root51'
                    
                    if category and category not in root_content:
                        root_content[category] = {}
                    
                    if category:
                        # Record all files in this directory
                        for file in files:
                            if not file.startswith('.') and file != 'Thumbs.db':
                                full_path = os.path.join(root, file)
                                file_rel_path = os.path.relpath(full_path, directory)
                                
                                size = os.path.getsize(full_path)
                                ext = os.path.splitext(file)[1].lower()
                                
                                root_content[category][file_rel_path] = {
                                    'full_path': full_path,
                                    'size': size,
                                    'extension': ext,
                                    'directory': os.path.basename(directory),
                                    'hash': get_file_hash(full_path)
                                }
                    break
    
    return root_content

def get_file_hash(filepath):
    """Get MD5 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def check_consolidated_coverage(root_content):
    """Check what Root42/Root51 content exists in consolidated directory"""
    
    print(f"\n📊 ROOT42/ROOT51 CONTENT ANALYSIS:")
    
    total_files = 0
    preserved_files = 0
    missing_files = []
    
    for category, files in root_content.items():
        if not files:
            continue
            
        print(f"\n{category}:")
        category_preserved = 0
        category_total = len(files)
        total_files += category_total
        
        for rel_path, info in files.items():
            # Check if file exists in consolidated
            consolidated_path = os.path.join(CONSOLIDATED_DIR, rel_path)
            alt_consolidated_path = os.path.join(CONSOLIDATED_DIR, "0platonicverses", rel_path)
            
            exists = False
            hash_match = False
            
            for check_path in [consolidated_path, alt_consolidated_path]:
                if os.path.exists(check_path):
                    exists = True
                    consolidated_hash = get_file_hash(check_path)
                    if consolidated_hash == info['hash']:
                        hash_match = True
                        break
            
            if exists and hash_match:
                category_preserved += 1
                preserved_files += 1
            else:
                missing_files.append({
                    'category': category,
                    'file': rel_path,
                    'size': info['size'],
                    'full_path': info['full_path'],
                    'reason': 'missing' if not exists else 'different_content'
                })
        
        print(f"   ✅ Preserved: {category_preserved}/{category_total}")
        if category_preserved < category_total:
            print(f"   ⚠️  Missing: {category_total - category_preserved}")
    
    print(f"\n📈 OVERALL ROOT42/ROOT51 STATUS:")
    print(f"   Total files: {total_files}")
    print(f"   Preserved: {preserved_files}")
    print(f"   Missing: {len(missing_files)}")
    
    if missing_files:
        print(f"\n❌ MISSING ROOT42/ROOT51 FILES:")
        for item in missing_files:
            print(f"   {item['reason'].upper()}: {item['category']} - {item['file']} ({item['size']} bytes)")
            print(f"      Source: {item['full_path']}")
    
    return missing_files

def check_git_status_in_root_dirs():
    """Check git status in Root42/Root51 directories"""
    print(f"\n🔄 GIT STATUS IN ROOT42/ROOT51 DIRECTORIES:")
    
    git_issues = []
    
    for directory in ORIGINAL_DIRS:
        if not os.path.exists(directory):
            continue
            
        for root, dirs, files in os.walk(directory):
            if '.git' in dirs:
                rel_path = os.path.relpath(root, directory)
                if any(pattern in rel_path.lower() for pattern in ['root42', 'root51', 'root-42', 'root-51']):
                    print(f"   📂 {root}")
                    try:
                        # Check for uncommitted changes
                        result = subprocess.run(['git', '-C', root, 'status', '--porcelain'], 
                                              capture_output=True, text=True, timeout=10)
                        if result.stdout.strip():
                            print(f"      ⚠️  UNCOMMITTED CHANGES:")
                            for line in result.stdout.strip().split('\n')[:5]:  # Show first 5 changes
                                print(f"         {line}")
                            git_issues.append(root)
                        else:
                            print(f"      ✅ Clean")
                    except:
                        print(f"      ❓ Could not check git status")
    
    return git_issues

def main():
    print("🔍 COMPREHENSIVE ROOT42/ROOT51 AUDIT")
    print("=" * 60)
    
    # Find all Root42/Root51 content
    root_content = find_root42_root51_content()
    
    # Check coverage in consolidated directory
    missing_files = check_consolidated_coverage(root_content)
    
    # Check git status
    git_issues = check_git_status_in_root_dirs()
    
    print(f"\n" + "="*60)
    print(f"ROOT42/ROOT51 SAFETY ASSESSMENT:")
    
    if missing_files:
        print(f"❌ NOT SAFE - {len(missing_files)} ROOT42/ROOT51 FILES MISSING")
        return False
    elif git_issues:
        print(f"⚠️  CAUTION - {len(git_issues)} ROOT42/ROOT51 REPOS HAVE UNCOMMITTED CHANGES")
        print(f"    (These changes need to be preserved)")
        return False
    else:
        print(f"✅ SAFE - ALL ROOT42/ROOT51 CONTENT PRESERVED")
        return True

if __name__ == "__main__":
    main()