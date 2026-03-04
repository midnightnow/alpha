#!/usr/bin/env python3
import os
import sys
import hashlib
import shutil
import json
import argparse
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCAN_ROOTS: list = [
    "/Users/studio/ALPHA",
    "/Volumes/Samsung T9 2",
]

# Archive root. MUST NOT be inside any SCAN_ROOT — ensures idempotence.
ARCHIVE_ROOT: str = "/Users/studio/REDUNDANCY_SILT" # Cannot be inside SCAN_ROOTS

EXTENSIONS: frozenset = frozenset({
    ".md", ".epub", ".docx", ".txt", ".pdf", ".tex"
})

# Priority classes for keeper selection (lower = kept preferentially).
# First matching substring wins.
PRIORITY_RULES: list = [
    ("LIBRARY_CANON",          0),
    ("LIBRARY_ARCHIVES",       1),
    ("/dev/",                  2),
    ("/Projects/",             3),
    ("/archive/",              4),
    ("PLATONICVERSES_ARCHIVE", 5),
]
DEFAULT_PRIORITY: int = 9

# Additional paths to skip during scan.
ALWAYS_EXCLUDE: list = [
    ".git", "__pycache__", "node_modules", ".DS_Store", "DUPLICATE_OF_CANON"
]

# ---------------------------------------------------------------------------
# SHA-256
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Ranking function  rho(d)  — total order
# ---------------------------------------------------------------------------

def priority_class(path: str) -> int:
    for fragment, cls in PRIORITY_RULES:
        if fragment in path:
            return cls
    return DEFAULT_PRIORITY

def rho(path: str) -> tuple:
    return (priority_class(path), len(path), path)

# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------

def _is_excluded(path: str) -> bool:
    if ARCHIVE_ROOT in path:
        return True
    return any(ex in path for ex in ALWAYS_EXCLUDE)

def scan(roots: list) -> dict:
    classes = defaultdict(list)
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [
                d for d in dirs
                if not _is_excluded(os.path.join(dirpath, d))
            ]
            for fname in files:
                if Path(fname).suffix.lower() not in EXTENSIONS:
                    continue
                fpath = os.path.join(dirpath, fname)
                if _is_excluded(fpath):
                    continue
                digest = sha256(fpath)
                if digest:
                    classes[digest].append(fpath)
    return dict(classes)

# ---------------------------------------------------------------------------
# Two-phase commit move  (safe across device boundaries)
# ---------------------------------------------------------------------------

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
        return (False, f"hash mismatch after copy (src={src_digest} dest={tmp_digest})")

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

def _remove_silent(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass

# ---------------------------------------------------------------------------
# Destination path — preserves directory structure, avoids filename collisions
# ---------------------------------------------------------------------------

def _dest_path(src: str, digest: str) -> str:
    rel  = src.lstrip("/") # Make relative
    dest = os.path.join(ARCHIVE_ROOT, rel)
    if os.path.exists(dest):
        stem, ext = os.path.splitext(dest)
        dest = f"{stem}__{digest[:8]}{ext}"
    return dest

# ---------------------------------------------------------------------------
# Invariants
# ---------------------------------------------------------------------------

def invariants(classes: dict) -> dict:
    sizes = [len(v) for v in classes.values()]
    total      = sum(sizes)
    unique     = len(classes)
    redundancy = total - unique
    return {
        "total_files":       total,
        "unique_states":     unique,
        "redundancy_mass":   redundancy,
        "duplicate_classes": sum(1 for s in sizes if s > 1),
        "largest_cluster":   max(sizes) if sizes else 0,
        "reduction_ratio":   round(redundancy / total, 4) if total else 0.0,
    }

# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------

def plan(classes: dict) -> list:
    actions = []
    for digest, paths in classes.items():
        if len(paths) < 2:
            continue
        keeper = min(paths, key=rho)
        for path in paths:
            if path == keeper:
                continue
            actions.append({
                "hash":   digest,
                "keeper": keeper,
                "source": path,
                "dest":   _dest_path(path, digest),
            })
    return actions

# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------

def execute_plan(actions: list) -> tuple:
    ok = err = 0
    errors = []
    for a in actions:
        success, msg = _safe_move(a["source"], a["dest"])
        if success:
            ok += 1
        else:
            err += 1
            errors.append(f"{a['source']} — {msg}")
    return (ok, err, errors)

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(inv: dict, actions: list) -> None:
    sep = "=" * 64
    print(sep)
    print("  HASH COLLAPSE  —  INVARIANT REPORT")
    print(sep)
    print(f"  Total files scanned   |D|    : {inv['total_files']}")
    print(f"  Unique states         |D/~|  : {inv['unique_states']}")
    print(f"  Redundancy mass              : {inv['redundancy_mass']}")
    print(f"  Duplicate classes            : {inv['duplicate_classes']}")
    print(f"  Largest cluster              : {inv['largest_cluster']}")
    print(f"  Reduction ratio              : {inv['reduction_ratio']:.1%}")
    print(sep)

def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    classes = scan(SCAN_ROOTS)
    inv     = invariants(classes)
    actions = plan(classes)

    print_report(inv, actions)

    if args.execute:
        if not actions: return
        ok, err, errs = execute_plan(actions)
        print(f"  Moved: {ok}  Failed: {err}")
    else:
        print("  DRY-RUN complete. No files moved.")

if __name__ == "__main__":
    main()
