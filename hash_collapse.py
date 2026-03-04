#!/usr/bin/env python3
"""
hash_collapse.py  —  Level 0: Equivalence Partitioning  D -> D/~
=================================================================

Formal model
------------
  d_i ~ d_j  <=>  SHA-256(d_i) = SHA-256(d_j)
  K = argmin_{d in [d]} rho(d)
  rho(d) = (priority_class, path_length, path_string)   [total order]

Guarantees
----------
  Deterministic  : rho is a total order; min is unique
  Idempotent     : P(P(D)) = P(D)
                   — archive root excluded from scan
                   — source deleted only after hash-verified copy
  Safe           : two-phase commit prevents partial moves
                   copy -> verify SHA-256 -> delete
                   (never shutil.move cross-device without verification)

Usage
-----
  python hash_collapse.py --dry-run            # report only, no changes
  python hash_collapse.py --dry-run --json     # + machine-readable output
  python hash_collapse.py --execute            # apply moves
  python hash_collapse.py --execute --json     # apply + record

  Override roots:
  python hash_collapse.py --dry-run --roots /path/a /path/b
"""

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
]

# Archive root. MUST NOT be inside any SCAN_ROOT — ensures idempotence.
ARCHIVE_ROOT: str = "/Users/studio/ALPHA/LIBRARY_ARCHIVES/EXACT_DUPLICATES"

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
    ".git", "__pycache__", "node_modules", ".DS_Store", "EXACT_DUPLICATES"
]


# ---------------------------------------------------------------------------
# SHA-256
# ---------------------------------------------------------------------------

def sha256(path: str):
    """Return hex digest of file, or None on read error."""
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
    """
    rho(d) = (priority_class, path_length, path_string)

    Total order: path_string is the unique final tie-breaker.
    Result is identical regardless of filesystem traversal order.
    """
    return (priority_class(path), len(path), path)


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------

def _is_excluded(path: str) -> bool:
    if ARCHIVE_ROOT in path:
        return True
    return any(ex in path for ex in ALWAYS_EXCLUDE)


def scan(roots: list) -> dict:
    """
    Walk roots, hash every qualifying file.
    Returns {digest: [path, ...]} — equivalence classes.
    Unreadable files are silently skipped.
    """
    classes = defaultdict(list)
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirs, files in os.walk(root):
            # Prune excluded subdirs in-place to prevent descent.
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
    """
    Phase 1: copy src -> dest.tmp
    Phase 2: verify SHA-256(dest.tmp) == SHA-256(src)
    Phase 3: rename dest.tmp -> dest  (atomic on same fs)
    Phase 4: delete src

    Returns (success: bool, error_message: str).
    Leaves src intact on any failure before phase 4.
    """
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".tmp"

    # Phase 1 — copy
    try:
        shutil.copy2(src, tmp)
    except (IOError, OSError, shutil.Error) as e:
        _remove_silent(tmp)
        return (False, f"copy failed: {e}")

    # Phase 2 — verify
    src_digest = sha256(src)
    tmp_digest = sha256(tmp)
    if src_digest != tmp_digest:
        _remove_silent(tmp)
        return (False, f"hash mismatch after copy (src={src_digest} dest={tmp_digest})")

    # Phase 3 — rename tmp -> dest
    try:
        os.replace(tmp, dest)
    except OSError as e:
        _remove_silent(tmp)
        return (False, f"rename failed: {e}")

    # Phase 4 — delete source
    try:
        os.remove(src)
    except OSError as e:
        # Destination is written and verified. Source delete failure is
        # recoverable: next dry-run will show it as a remaining redundancy.
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
    """
    Mirror src under ARCHIVE_ROOT, preserving directory structure.
    If the computed dest already exists, append short digest to stem.
    """
    rel  = src.lstrip("/")
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
# Plan  (pure; no filesystem writes)
# ---------------------------------------------------------------------------

def plan(classes: dict) -> list:
    """
    For each equivalence class |C| > 1: select keeper via argmin rho,
    generate move record for every non-keeper.
    No filesystem changes.
    """
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

def execute(actions: list) -> tuple:
    """Apply planned moves. Returns (ok_count, error_count, error_list)."""
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
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)
    print(f"  Total files scanned   |D|    : {inv['total_files']}")
    print(f"  Unique states         |D/~|  : {inv['unique_states']}")
    print(f"  Redundancy mass              : {inv['redundancy_mass']}")
    print(f"  Duplicate classes            : {inv['duplicate_classes']}")
    print(f"  Largest cluster              : {inv['largest_cluster']}")
    print(f"  Reduction ratio              : {inv['reduction_ratio']:.1%}")
    print(sep)

    if not actions:
        print("\n  Basis is already minimal. No moves required.\n")
        return

    print(f"\n  PLANNED MOVES  ({len(actions)} files)\n")
    last_hash = None
    for a in sorted(actions, key=lambda x: x["hash"]):
        if a["hash"] != last_hash:
            last_hash = a["hash"]
            print(f"  [{a['hash'][:16]}...]")
            print(f"    KEEP : {a['keeper']}")
        print(f"    MOVE : {a['source']}")
        print(f"      ->   {a['dest']}")
    print()


def write_json(inv: dict, actions: list, path: str) -> None:
    data = {
        "timestamp":    datetime.now().isoformat(),
        "archive_root": ARCHIVE_ROOT,
        "invariants":   inv,
        "actions":      actions,
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  JSON report written: {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Level 0 Hash Collapse — D -> D/~",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--dry-run", action="store_true",
        help="Compute and report only. No files moved."
    )
    mode.add_argument(
        "--execute", action="store_true",
        help="Apply moves via two-phase commit."
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Write HASH_COLLAPSE_REPORT.json"
    )
    parser.add_argument(
        "--roots", nargs="*", default=None,
        help="Override scan roots (space-separated paths)."
    )
    args = parser.parse_args()

    roots = args.roots or SCAN_ROOTS

    print(f"\n  Scanning {len(roots)} root(s)...")
    classes = scan(roots)
    total   = sum(len(v) for v in classes.values())
    print(f"  {total} files found.\n")

    inv     = invariants(classes)
    actions = plan(classes)

    print_report(inv, actions)

    if args.json:
        write_json(inv, actions, "HASH_COLLAPSE_REPORT.json")

    if args.execute:
        if not actions:
            print("  Nothing to move.")
            return
        print(f"  Executing {len(actions)} two-phase commits...")
        ok, err, errs = execute(actions)
        print(f"  Moved: {ok}  Failed: {err}")
        if errs:
            print("\n  ERRORS:")
            for e in errs:
                print(f"    {e}")
        print(f"\n  Archive: {ARCHIVE_ROOT}")
    else:
        print("  DRY-RUN complete. No files moved.")
        print("  Re-run with --execute to apply.\n")


if __name__ == "__main__":
    main()
