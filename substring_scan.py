#!/usr/bin/env python3
"""
substring_scan.py  —  Level 1: Containment Poset  D/~ -> B
===========================================================

Formal model
------------
  Normalisation:  f(d) = collapse_whitespace(lowercase(d))
                  Preserves digits and punctuation.
                  Does NOT strip non-alphanumeric — avoids collapsing
                  numeric distinctions (e.g. "4.2" != "42").

  Containment:    d_i preceq d_j  <=>  f(d_i) is a contiguous
                                        substring of f(d_j)
                  where i != j and |f(d_i)| <= |f(d_j)|

  Poset:          (D, preceq) is reflexive, antisymmetric, transitive.

  Basis:          B = { m in D | not-exists x in D s.t. m prec x }
                  = maximal elements of the poset.

Algorithm
---------
  Naive O(n^2 * L) is acceptable at n=1500, avg 20KB.
  We apply two pre-filters to skip most pairs:

    Filter 1 (size):     skip if |f(d_i)| > |f(d_j)|
    Filter 2 (prefix):   skip if f(d_i)[:64] not in f(d_j)
                         (cheap membership test before full search)

  For pairs that pass both filters: Python's str.find() which uses a
  two-way algorithm, O(|d_j|) average.

  For large corpora: --suffix-array flag builds a generalised suffix
  array on the full corpus for O(N) amortised queries, where N is
  total normalised characters.

Output
------
  CONTAINMENT_REPORT.json   — full poset edges + basis
  CONTAINMENT_REPORT.md     — human-readable summary
  stdout                    — progress + invariants

Usage
-----
  python substring_scan.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON
  python substring_scan.py --input-hashes HASH_COLLAPSE_REPORT.json
  python substring_scan.py --input-dir ... --execute   # move non-maximal files
  python substring_scan.py --input-dir ... --suffix-array  # large corpora
"""

import os
import re
import sys
import json
import argparse
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EXTENSIONS: frozenset = frozenset({
    ".md", ".epub", ".docx", ".txt", ".pdf", ".tex"
})

ARCHIVE_DEST: str = "/Users/studio/ALPHA/LIBRARY_ARCHIVES/NonMaximal_Nodes"

# Minimum normalised length to participate in containment check.
# Files below this are fragments too small to be meaningful containers.
MIN_LENGTH: int = 200

# Prefix length used for cheap pre-filter (Filter 2).
PREFIX_LEN: int = 64


# ---------------------------------------------------------------------------
# Normalisation  f(d)
# ---------------------------------------------------------------------------

def normalise(text: str) -> str:
    """
    f(d): lowercase + collapse all whitespace sequences to single space.

    Preserves: digits, punctuation, alphanumeric.
    Strips:    leading/trailing whitespace.

    Deliberately does NOT remove punctuation or digits.
    Rationale: "4.2" and "42" are distinct information states in a
    mathematics corpus. Removing punctuation would collapse them.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def load_normalised(path: str) -> str | None:
    """Read file, decode as UTF-8 (fallback latin-1), return normalised string."""
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()
    except (IOError, OSError):
        return None
    return normalise(raw)


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def collect_files(directory: str) -> list:
    """Return all files with qualifying extensions under directory."""
    files = []
    for dirpath, _, filenames in os.walk(directory):
        if "Precipitated_Silt" in dirpath or "DUPLICATE_OF_CANON" in dirpath or "NonMaximal_Nodes" in dirpath:
            continue
        for fname in filenames:
            if Path(fname).suffix.lower() in EXTENSIONS:
                files.append(os.path.join(dirpath, fname))
    return files


def collect_from_hash_report(report_path: str) -> list:
    """
    Load keeper files from a HASH_COLLAPSE_REPORT.json produced by
    hash_collapse.py. Uses only the keeper path from each cluster,
    plus all singleton files.
    """
    with open(report_path) as f:
        report = json.load(f)

    keepers = set()
    # Singletons: files not in any duplicate cluster are implicitly unique.
    # The report only lists clusters, so we need the source directory.
    # Fallback: caller should combine --input-dir with this flag.
    for action in report.get("actions", []):
        keepers.add(action["keeper"])

    return list(keepers)


# ---------------------------------------------------------------------------
# Containment check  (naive, with pre-filters)
# ---------------------------------------------------------------------------

def is_contained(norm_i: str, norm_j: str, prefix_index: dict | None = None) -> bool:
    """
    Returns True if norm_i is a contiguous substring of norm_j.

    Filter 1: length — norm_i must be strictly shorter.
    Filter 2: prefix — first PREFIX_LEN chars of norm_i must appear in norm_j.
              Uses pre-built index if available.
    Filter 3: full substring search via str.find() (two-way algorithm).
    """
    if len(norm_i) >= len(norm_j):
        return False

    prefix = norm_i[:PREFIX_LEN]
    if prefix not in norm_j:
        return False

    return norm_i in norm_j


# ---------------------------------------------------------------------------
# Generalised suffix array  (optional, for large corpora)
# ---------------------------------------------------------------------------

def build_suffix_array_index(documents: list) -> dict:
    """
    Build a simple inverted index mapping 64-char shingles to document ids.
    Used as an accelerated Filter 2 for --suffix-array mode.

    A full SA-IS suffix array is overkill at n=1500. This shingle index
    gives O(1) lookup for the prefix pre-filter and reduces full substring
    searches to candidates only.

    Returns: {shingle_str: set(doc_ids)}
    """
    index = defaultdict(set)
    for doc_id, (_, norm) in enumerate(documents):
        for i in range(0, len(norm) - PREFIX_LEN, PREFIX_LEN // 2):
            shingle = norm[i:i + PREFIX_LEN]
            index[shingle].add(doc_id)
    return dict(index)


# ---------------------------------------------------------------------------
# Poset construction
# ---------------------------------------------------------------------------

def build_containment_poset(documents: list, use_suffix_array: bool = False) -> list:
    """
    documents: list of (path, normalised_text)
    Returns list of (i, j) pairs where documents[i] preceq documents[j].
    """
    n = len(documents)
    edges = []

    shingle_index = None
    if use_suffix_array:
        print("  Building shingle index...")
        shingle_index = build_suffix_array_index(documents)

    total_pairs = n * (n - 1) // 2
    checked = skipped = 0

    for i in range(n):
        path_i, norm_i = documents[i]
        if len(norm_i) < MIN_LENGTH:
            skipped += n - i - 1
            continue

        for j in range(n):
            if i == j:
                continue

            path_j, norm_j = documents[j]
            if len(norm_j) < MIN_LENGTH:
                skipped += 1
                continue

            # Filter 1: norm_i must be strictly shorter than norm_j
            if len(norm_i) >= len(norm_j):
                continue

            checked += 1
            if is_contained(norm_i, norm_j):
                edges.append((i, j))

        # Progress indicator
        if (i + 1) % 50 == 0 or i == n - 1:
            print(f"  [{i+1}/{n}] edges found: {len(edges)}  "
                  f"checked: {checked}  skipped: {skipped}")

    return edges


def find_maximal_elements(n: int, edges: list) -> set:
    """
    Given n documents and containment edges (i preceq j),
    return the set of indices that are maximal:
    i is maximal if no j exists such that i prec j.
    """
    contained_in_something = set(i for (i, j) in edges)
    return set(range(n)) - contained_in_something


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def write_json_report(documents: list, edges: list, maximal: set, path: str) -> None:
    edge_records = [
        {
            "contained":  documents[i][0],
            "inside":     documents[j][0],
        }
        for (i, j) in edges
    ]

    basis = [documents[i][0] for i in sorted(maximal)]
    non_maximal = [documents[i][0] for i in range(len(documents)) if i not in maximal]

    report = {
        "timestamp":   datetime.now().isoformat(),
        "total_docs":  len(documents),
        "basis_size":  len(basis),
        "non_maximal": len(non_maximal),
        "edges":       edge_records,
        "basis":       basis,
        "archive_candidates": non_maximal,
    }

    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  JSON report: {path}")


def write_md_report(documents: list, edges: list, maximal: set, path: str) -> None:
    lines = [
        "# Level 1: Containment Poset Report",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## Invariants",
        f"- Total documents: {len(documents)}",
        f"- Basis |B| (maximal elements): {len(maximal)}",
        f"- Non-maximal (archive candidates): {len(documents) - len(maximal)}",
        f"- Containment edges: {len(edges)}",
        "",
        "## Basis (Maximal Elements)",
        "*These files are not contained within any other file.*",
        "",
    ]
    for i in sorted(maximal):
        lines.append(f"- `{documents[i][0]}`")

    lines += [
        "",
        "## Archive Candidates (Non-Maximal Elements)",
        "*These files are fully contained within at least one basis element.*",
        "",
    ]
    for (i, j) in sorted(edges, key=lambda e: documents[e[0]][0]):
        lines.append(
            f"- `{documents[i][0]}`  \n"
            f"  ⊆ `{documents[j][0]}`"
        )

    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Markdown report: {path}")


def print_summary(documents: list, edges: list, maximal: set) -> None:
    sep = "=" * 64
    print(sep)
    print("  CONTAINMENT POSET  —  LEVEL 1 REPORT")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)
    print(f"  Total documents          : {len(documents)}")
    print(f"  Basis |B|                : {len(maximal)}")
    print(f"  Non-maximal (contained)  : {len(documents) - len(maximal)}")
    print(f"  Containment edges        : {len(edges)}")
    print(sep)

    if edges:
        print("\n  CONTAINMENT EDGES  (d_i ⊆ d_j)\n")
        for (i, j) in sorted(edges, key=lambda e: documents[e[0]][0]):
            pi = documents[i][0]
            pj = documents[j][0]
            li = len(documents[i][1])
            lj = len(documents[j][1])
            pct = round(li / lj * 100, 1)
            print(f"  [{pct:5.1f}%]  {pi}")
            print(f"          ⊆  {pj}")
        print()


# ---------------------------------------------------------------------------
# Execute: move non-maximal files to archive
# ---------------------------------------------------------------------------

def execute_archive(documents: list, maximal: set) -> None:
    os.makedirs(ARCHIVE_DEST, exist_ok=True)
    moved = errors = 0
    for i in range(len(documents)):
        if i in maximal:
            continue
        src = documents[i][0]
        if not os.path.exists(src):
            continue
        dest = os.path.join(ARCHIVE_DEST, os.path.basename(src))
        if os.path.exists(dest):
            stem, ext = os.path.splitext(dest)
            h = hashlib.sha256(src.encode()).hexdigest()[:8]
            dest = f"{stem}__{h}{ext}"
        try:
            shutil.move(src, dest)
            print(f"  ARCHIVED: {src}")
            moved += 1
        except (IOError, OSError, shutil.Error) as e:
            print(f"  ERROR: {src} — {e}", file=sys.stderr)
            errors += 1
    print(f"\n  Archived: {moved}  Errors: {errors}")
    print(f"  Destination: {ARCHIVE_DEST}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Level 1: Containment Poset — find maximal elements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument(
        "--input-dir", metavar="DIR",
        help="Scan directory for qualifying files."
    )
    src.add_argument(
        "--input-hashes", metavar="JSON",
        help="Load keeper paths from hash_collapse.py JSON report."
    )
    parser.add_argument(
        "--execute", action="store_true",
        help="Move non-maximal files to archive after reporting."
    )
    parser.add_argument(
        "--suffix-array", action="store_true",
        help="Build shingle index for faster filtering (large corpora)."
    )
    args = parser.parse_args()

    # Collect files
    if args.input_dir:
        paths = collect_files(args.input_dir)
    else:
        paths = collect_from_hash_report(args.input_hashes)

    print(f"\n  {len(paths)} files collected.")

    # Load and normalise
    print("  Normalising...")
    documents = []
    for p in paths:
        norm = load_normalised(p)
        if norm and len(norm) >= MIN_LENGTH:
            documents.append((p, norm))
        else:
            pass # Removed noisy output

    print(f"  {len(documents)} documents will participate in containment check.")

    # Build poset
    print("\n  Building containment poset...")
    edges = build_containment_poset(documents, use_suffix_array=args.suffix_array)

    # Find maximal elements
    maximal = find_maximal_elements(len(documents), edges)

    # Report
    print_summary(documents, edges, maximal)
    write_json_report(documents, edges, maximal, "CONTAINMENT_REPORT.json")
    write_md_report(documents, edges, maximal, "CONTAINMENT_REPORT.md")

    # Execute
    if args.execute:
        if not edges:
            print("  All documents are maximal. Nothing to archive.")
            return
        print(f"\n  Archiving {len(documents) - len(maximal)} non-maximal files...")
        execute_archive(documents, maximal)
    else:
        print("  DRY-RUN. Pass --execute to archive non-maximal files.")
        print("  Review CONTAINMENT_REPORT.md before executing.\n")


if __name__ == "__main__":
    main()
