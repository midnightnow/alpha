#!/usr/bin/env python3
"""
Comprehensive Final Audit - Ensure ZERO important content is lost before deletion
"""

import os
import hashlib
import json
from pathlib import Path
from collections import defaultdict
import subprocess

# Original directories to be deleted
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

def get_git_info(directory):
    """Check for git repositories and uncommitted changes"""
    git_repos = []
    try:
        result = subprocess.run(['find', directory, '-type', 'd', '-name', '.git'], 
                              capture_output=True, text=True, timeout=30)
        git_dirs = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        for git_dir in git_dirs:
            repo_dir = os.path.dirname(git_dir)
            try:
                # Check for uncommitted changes
                status_result = subprocess.run(['git', '-C', repo_dir, 'status', '--porcelain'], 
                                             capture_output=True, text=True, timeout=10)
                uncommitted = bool(status_result.stdout.strip())
                
                # Get recent commits
                log_result = subprocess.run(['git', '-C', repo_dir, 'log', '--oneline', '-5'], 
                                          capture_output=True, text=True, timeout=10)
                recent_commits = log_result.stdout.strip().split('\n')[:3]
                
                git_repos.append({
                    'path': repo_dir,
                    'uncommitted_changes': uncommitted,
                    'recent_commits': recent_commits
                })
            except:
                git_repos.append({
                    'path': repo_dir,
                    'uncommitted_changes': 'unknown',
                    'recent_commits': []
                })
    except:
        pass
    
    return git_repos

def scan_all_files(directory):
    """Scan ALL files, not just content files"""
    all_files = {}
    
    if not os.path.exists(directory):
        return all_files
        
    for root, dirs, files in os.walk(directory):
        # Don't skip anything in this comprehensive scan
        for file in files:
            # Skip only OS files
            if file in ['.DS_Store', 'Thumbs.db']:
                continue
                
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, directory)
            
            try:
                size = os.path.getsize(full_path)
                file_hash = get_file_hash(full_path)
                
                all_files[rel_path] = {
                    'hash': file_hash,
                    'size': size,
                    'full_path': full_path,
                    'extension': os.path.splitext(file)[1].lower()
                }
            except:
                continue
    
    return all_files

def find_critical_files():
    """Find files that are typically critical: configs, secrets, keys, etc."""
    critical_patterns = [
        '.env', '.secret', '.key', '.pem', '.p12', '.jks',
        'config.json', 'settings.json', 'credentials.json',
        '.gitignore', '.gitconfig', 'package.json', 'package-lock.json',
        'requirements.txt', 'Pipfile', 'poetry.lock', 'yarn.lock',
        'tsconfig.json', 'webpack.config.js', 'vite.config.js',
        'Dockerfile', 'docker-compose.yml', '.dockerignore',
        'Makefile', 'makefile', 'build.sh', 'deploy.sh',
        'README', 'LICENSE', 'CHANGELOG', 'TODO',
        '.claude.json', 'claude.json', 'anthropic.json'
    ]
    
    critical_files = []
    
    for directory in ORIGINAL_DIRS:
        if not os.path.exists(directory):
            continue
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                filename_lower = file.lower()
                
                # Check exact matches and patterns
                for pattern in critical_patterns:
                    if (filename_lower == pattern.lower() or 
                        filename_lower.startswith(pattern.lower()) or
                        filename_lower.endswith(pattern.lower())):
                        
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, directory)
                        critical_files.append({
                            'file': file,
                            'path': rel_path,
                            'full_path': full_path,
                            'directory': os.path.basename(directory),
                            'size': os.path.getsize(full_path)
                        })
                        break
    
    return critical_files

def comprehensive_file_audit():
    """Complete audit of ALL files across directories"""
    print("🔍 COMPREHENSIVE FINAL AUDIT")
    print("=" * 60)
    
    # 1. Check for git repositories and uncommitted changes
    print("\n🔄 GIT REPOSITORY AUDIT:")
    all_git_repos = []
    for directory in ORIGINAL_DIRS:
        if os.path.exists(directory):
            repos = get_git_info(directory)
            all_git_repos.extend(repos)
    
    if all_git_repos:
        for repo in all_git_repos:
            print(f"   📂 {repo['path']}")
            if repo['uncommitted_changes']:
                print(f"      ⚠️  UNCOMMITTED CHANGES DETECTED")
            if repo['recent_commits']:
                print(f"      Recent: {repo['recent_commits'][0]}")
    else:
        print("   ✅ No git repositories found")
    
    # 2. Find critical configuration files
    print(f"\n🔧 CRITICAL FILES AUDIT:")
    critical_files = find_critical_files()
    
    critical_in_consolidated = []
    critical_missing = []
    
    for cf in critical_files:
        consolidated_path = os.path.join(CONSOLIDATED_DIR, cf['path'])
        if os.path.exists(consolidated_path):
            # Check if it's the same content
            orig_hash = get_file_hash(cf['full_path'])
            cons_hash = get_file_hash(consolidated_path)
            if orig_hash == cons_hash:
                critical_in_consolidated.append(cf)
            else:
                critical_missing.append({**cf, 'reason': 'different_content'})
        else:
            critical_missing.append({**cf, 'reason': 'file_missing'})
    
    print(f"   Found {len(critical_files)} critical files")
    print(f"   ✅ Preserved in consolidated: {len(critical_in_consolidated)}")
    
    if critical_missing:
        print(f"   ⚠️  MISSING/DIFFERENT: {len(critical_missing)}")
        for cf in critical_missing:
            print(f"      {cf['reason'].upper()}: {cf['directory']}:{cf['path']} ({cf['size']} bytes)")
    
    # 3. Complete file inventory comparison
    print(f"\n📊 COMPLETE FILE INVENTORY:")
    
    total_original_files = 0
    all_original_hashes = set()
    
    for directory in ORIGINAL_DIRS:
        if os.path.exists(directory):
            files = scan_all_files(directory)
            total_original_files += len(files)
            for info in files.values():
                if info['hash']:
                    all_original_hashes.add(info['hash'])
    
    consolidated_files = scan_all_files(CONSOLIDATED_DIR)
    consolidated_hashes = set(info['hash'] for info in consolidated_files.values() if info['hash'])
    
    print(f"   Original files (all types): {total_original_files}")
    print(f"   Consolidated files: {len(consolidated_files)}")
    print(f"   Unique original hashes: {len(all_original_hashes)}")
    print(f"   Consolidated hashes: {len(consolidated_hashes)}")
    
    missing_hashes = all_original_hashes - consolidated_hashes
    print(f"   ⚠️  Missing unique content hashes: {len(missing_hashes)}")
    
    # 4. Find large files that might be important
    print(f"\n📦 LARGE FILES AUDIT (>1MB):")
    large_files = []
    
    for directory in ORIGINAL_DIRS:
        if os.path.exists(directory):
            files = scan_all_files(directory)
            for rel_path, info in files.items():
                if info['size'] > 1024 * 1024:  # > 1MB
                    large_files.append({
                        'directory': os.path.basename(directory),
                        'path': rel_path,
                        'size_mb': round(info['size'] / (1024*1024), 2),
                        'hash': info['hash'],
                        'full_path': info['full_path']
                    })
    
    # Check which large files are preserved
    large_preserved = 0
    large_missing = []
    
    for lf in large_files:
        consolidated_path = os.path.join(CONSOLIDATED_DIR, lf['path'])
        if os.path.exists(consolidated_path):
            cons_hash = get_file_hash(consolidated_path)
            if cons_hash == lf['hash']:
                large_preserved += 1
            else:
                large_missing.append({**lf, 'reason': 'different_hash'})
        else:
            large_missing.append({**lf, 'reason': 'missing_file'})
    
    print(f"   Found {len(large_files)} files >1MB")
    print(f"   ✅ Preserved: {large_preserved}")
    
    if large_missing:
        print(f"   ⚠️  MISSING LARGE FILES: {len(large_missing)}")
        for lf in large_missing:
            print(f"      {lf['reason'].upper()}: {lf['directory']}:{lf['path']} ({lf['size_mb']}MB)")
    
    # 5. Extension analysis
    print(f"\n📁 FILE TYPE ANALYSIS:")
    ext_counts = defaultdict(int)
    for directory in ORIGINAL_DIRS:
        if os.path.exists(directory):
            files = scan_all_files(directory)
            for info in files.values():
                ext = info['extension'] or 'no_ext'
                ext_counts[ext] += 1
    
    # Show top file types
    top_extensions = sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for ext, count in top_extensions:
        print(f"   {ext}: {count} files")
    
    return {
        'git_repos': all_git_repos,
        'critical_missing': critical_missing,
        'missing_hashes': len(missing_hashes),
        'large_missing': large_missing,
        'safe_to_delete': len(critical_missing) == 0 and len(large_missing) == 0 and len(missing_hashes) == 0
    }

def main():
    audit_results = comprehensive_file_audit()
    
    print(f"\n" + "="*60)
    print(f"FINAL SAFETY ASSESSMENT:")
    
    if audit_results['safe_to_delete']:
        print(f"✅ SAFE TO DELETE ORIGINAL DIRECTORIES")
        print(f"   All critical files preserved")
        print(f"   All large files preserved") 
        print(f"   All unique content preserved")
    else:
        print(f"⚠️  NOT SAFE TO DELETE - ISSUES FOUND:")
        if audit_results['critical_missing']:
            print(f"   - {len(audit_results['critical_missing'])} critical files missing/different")
        if audit_results['large_missing']:
            print(f"   - {len(audit_results['large_missing'])} large files missing")
        if audit_results['missing_hashes']:
            print(f"   - {audit_results['missing_hashes']} unique content hashes missing")
    
    return audit_results

if __name__ == "__main__":
    main()