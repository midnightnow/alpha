#!/usr/bin/env python3
"""
sequence_builder.py  —  Level 3: Topological Assembler
=======================================================

Purpose
-------
  Generate a publication manifest from the 59-file Minimal Antichain Basis.
  Output: MASTER_MANIFEST.md + MASTER_MANIFEST.json

  Ordering is determined by a three-stage hybrid pipeline:

  Stage 1 — Deterministic (no LLM)
    Extract sequence markers from:
      - Frontmatter fields: sequence, order, chapter, part, book
      - Filename numeric prefixes: Chapter_01_, 03_, Part_2_, etc.
      - Header H1 containing ordinal patterns

  Stage 2 — LLM-assisted gap fill (optional, requires API key)
    For files with no deterministic marker, call Claude API with
    file title + first 500 chars to infer position in sequence.
    Requires: ANTHROPIC_API_KEY environment variable.

  Stage 3 — Manual seed override
    If SEED_ORDER.json exists in working directory, positions in
    that file take absolute precedence over Stages 1 and 2.

Output columns (publication manifest)
--------------------------------------
  position      : integer sequence position (1-indexed)
  filename      : basename
  path          : absolute path
  title         : extracted H1 or filename stem
  word_count    : approximate word count
  char_count    : character count
  size_bytes    : file size on disk
  book          : extracted book/part grouping
  chapter       : extracted chapter number
  order_source  : how position was determined (frontmatter/filename/llm/seed/unresolved)
  summary       : first non-empty paragraph (truncated to 200 chars)

Usage
-----
  # Deterministic only (no API call)
  python sequence_builder.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON

  # With LLM gap-fill (requires ANTHROPIC_API_KEY)
  python sequence_builder.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON --llm

  # With manual seed overrides
  python sequence_builder.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON --seed SEED_ORDER.json

  # Full pipeline
  python sequence_builder.py --input-dir /Users/studio/ALPHA/LIBRARY_CANON --llm --seed SEED_ORDER.json

SEED_ORDER.json format
----------------------
  {
    "Foreword_The_Leak.md": 1,
    "Epilogue_The_Man_Who_Ate_at_Noon.md": 59
  }
  Keys are basenames. Values are 1-indexed positions.
"""

import os
import re
import sys
import json
import math
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EXTENSIONS: frozenset = frozenset({
    ".md", ".txt", ".epub", ".docx", ".tex"
})

# Frontmatter fields checked for sequence markers (in priority order)
SEQUENCE_FIELDS = ["sequence", "order", "chapter", "part", "book_order", "position"]

# Filename patterns that imply sequence
# Matches: Chapter_01, 03_Title, Part_2, Book_1, etc.
FILENAME_PATTERNS = [
    r'^(?:chapter|ch|part|book|section|vol|volume|ep|episode)[_\-\s]*(\d+)',
    r'^(\d{1,3})[_\-\s]',
    r'[_\-\s](\d{1,3})[_\-\s]',
]

# LLM model
LLM_MODEL = "claude-sonnet-4-20250514"
LLM_MAX_TOKENS = 150


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def collect_files(directory: str) -> list:
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for fname in sorted(filenames):
            if Path(fname).suffix.lower() in EXTENSIONS:
                files.append(os.path.join(dirpath, fname))
    return sorted(files)


# ---------------------------------------------------------------------------
# Text loading
# ---------------------------------------------------------------------------

def load_text(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except (IOError, OSError):
        return ""


# ---------------------------------------------------------------------------
# Frontmatter extraction
# ---------------------------------------------------------------------------

def extract_frontmatter(text: str) -> dict:
    """
    Parse YAML-style frontmatter between --- delimiters.
    Returns dict of key: value pairs. Values are kept as strings.
    """
    fm = {}
    if not text.startswith('---'):
        return fm
    end = text.find('\n---', 3)
    if end == -1:
        return fm
    block = text[3:end].strip()
    for line in block.splitlines():
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip().lower()] = val.strip().strip('"\'')
    return fm


def frontmatter_sequence(fm: dict) -> tuple:
    """
    Returns (position, field_name) if a sequence marker is found, else (None, None).
    """
    for field in SEQUENCE_FIELDS:
        val = fm.get(field)
        if val is not None:
            # Extract first integer from value
            m = re.search(r'(\d+)', str(val))
            if m:
                return (int(m.group(1)), field)
    return (None, None)


# ---------------------------------------------------------------------------
# Filename pattern extraction
# ---------------------------------------------------------------------------

def filename_sequence(path: str) -> tuple:
    """
    Returns (position, 'filename') if numeric prefix/pattern found, else (None, None).
    """
    stem = Path(path).stem.lower()
    for pattern in FILENAME_PATTERNS:
        m = re.match(pattern, stem, re.IGNORECASE)
        if m:
            return (int(m.group(1)), 'filename')
    return (None, None)


# ---------------------------------------------------------------------------
# Title and metadata extraction
# ---------------------------------------------------------------------------

def extract_title(text: str, path: str) -> str:
    """Extract H1 heading or fall back to filename stem."""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return Path(path).stem.replace('_', ' ').replace('-', ' ')


def extract_book_chapter(text: str, path: str, fm: dict) -> tuple:
    """
    Returns (book_label, chapter_number) strings.
    Checks frontmatter first, then filename, then H2 patterns.
    """
    book = fm.get('book', fm.get('part', ''))
    chapter = fm.get('chapter', '')

    if not book:
        stem = Path(path).stem
        # Look for Book_N or Part_N in path components
        for part in Path(path).parts:
            bm = re.match(r'(?:book|part|vol)_?(\d+)', part, re.IGNORECASE)
            if bm:
                book = f"Book {bm.group(1)}"
                break

    if not chapter:
        m = re.match(r'(?:chapter|ch)[_\-\s]*(\d+)', Path(path).stem, re.IGNORECASE)
        if m:
            chapter = m.group(1)

    return (book, chapter)


def extract_summary(text: str) -> str:
    """Return first non-empty, non-header paragraph, truncated to 200 chars."""
    # Skip frontmatter
    body = text
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            body = text[end+4:]

    for para in body.split('\n\n'):
        para = para.strip()
        if para and not para.startswith('#') and len(para) > 20:
            clean = re.sub(r'\s+', ' ', para)
            return clean[:200] + ('...' if len(clean) > 200 else '')
    return ''


def word_count(text: str) -> int:
    return len(text.split())


# ---------------------------------------------------------------------------
# Stage 1: Deterministic ordering
# ---------------------------------------------------------------------------

def stage1_deterministic(documents: list) -> dict:
    """
    Returns {path: (position, source)} for all files where a marker is found.
    """
    positions = {}
    for path, text in documents:
        fm = extract_frontmatter(text)

        pos, source = frontmatter_sequence(fm)
        if pos is not None:
            positions[path] = (pos, f'frontmatter:{source}')
            continue

        pos, source = filename_sequence(path)
        if pos is not None:
            positions[path] = (pos, source)

    return positions


# ---------------------------------------------------------------------------
# Stage 2: LLM gap-fill
# ---------------------------------------------------------------------------

def _call_llm(title: str, summary: str, known_titles: list, api_key: str) -> int | None:
    """
    Ask Claude for a suggested sequence position.
    Returns integer or None on failure.
    """
    known_str = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(known_titles[:20]))
    prompt = (
        f"You are ordering documents for publication. "
        f"The following titles are already placed in sequence:\n{known_str}\n\n"
        f"Where should this document fit in the sequence (give only an integer)?\n"
        f"Title: {title}\n"
        f"Opening: {summary[:300]}"
    )

    payload = json.dumps({
        "model": LLM_MODEL,
        "max_tokens": LLM_MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            text = data["content"][0]["text"].strip()
            m = re.search(r'\d+', text)
            return int(m.group()) if m else None
    except Exception as e:
        print(f"    LLM call failed: {e}", file=sys.stderr)
        return None


def stage2_llm(documents: list, positions: dict, api_key: str) -> dict:
    """
    For documents without a deterministic position, call LLM.
    Updates positions dict in place, returns it.
    """
    unresolved = [d for d in documents if d[0] not in positions]
    if not unresolved:
        return positions

    print(f"  LLM gap-fill: {len(unresolved)} unresolved documents...")

    # Build list of known titles in current order for context
    resolved_sorted = sorted(
        [(p, pos, src) for p, (pos, src) in positions.items()],
        key=lambda x: x[1]
    )
    known_titles = [extract_title(text, path)
                    for path, text in documents
                    if path in positions]

    for path, text in unresolved:
        title = extract_title(text, path)
        summary = extract_summary(text)
        print(f"    Querying LLM for: {Path(path).name}")
        pos = _call_llm(title, summary, known_titles, api_key)
        if pos is not None:
            positions[path] = (pos, 'llm')
            known_titles.insert(min(pos - 1, len(known_titles)), title)
        else:
            positions[path] = (10000, 'unresolved')

    return positions


# ---------------------------------------------------------------------------
# Stage 3: Manual seed override
# ---------------------------------------------------------------------------

def stage3_seed(documents: list, positions: dict, seed_path: str) -> dict:
    """
    Load SEED_ORDER.json and override positions for named files.
    Seed positions take absolute precedence.
    """
    try:
        with open(seed_path) as f:
            seed = json.load(f)
    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f"  WARNING: Could not load seed file {seed_path}: {e}")
        return positions

    path_by_basename = {Path(p).name: p for p, _ in documents}

    overrides = 0
    for basename, pos in seed.items():
        full_path = path_by_basename.get(basename)
        if full_path:
            positions[full_path] = (int(pos), 'seed')
            overrides += 1
        else:
            print(f"  WARNING: Seed file references unknown basename: {basename}")

    print(f"  Seed overrides applied: {overrides}")
    return positions


# ---------------------------------------------------------------------------
# Position normalisation
# ---------------------------------------------------------------------------

def normalise_positions(documents: list, positions: dict) -> list:
    """
    Convert raw positions to clean 1-indexed integers.
    Handles: duplicate positions (interleaved by path), gaps, unresolved.

    Returns list of (path, final_position, source) sorted by position.
    """
    # Separate resolved from unresolved
    resolved = [(p, pos, src) for p, (pos, src) in positions.items()
                if src != 'unresolved']
    unresolved_paths = [p for p, (pos, src) in positions.items()
                        if src == 'unresolved']
    # Files completely missing from positions dict
    all_paths = {p for p, _ in documents}
    missing_paths = list(all_paths - set(positions.keys()))
    unresolved_paths += missing_paths

    # Sort resolved by (position, path) for determinism on ties
    resolved.sort(key=lambda x: (x[1], x[0]))

    # Assign final 1-indexed positions
    result = []
    for i, (path, _, src) in enumerate(resolved, start=1):
        result.append((path, i, src))

    # Append unresolved at end, sorted by path for determinism
    offset = len(result) + 1
    for i, path in enumerate(sorted(unresolved_paths), start=offset):
        result.append((path, i, 'unresolved'))

    return result


# ---------------------------------------------------------------------------
# Build manifest records
# ---------------------------------------------------------------------------

def build_manifest(documents: list, ordered: list) -> list:
    """
    Returns list of manifest record dicts, one per document.
    """
    text_by_path = {p: t for p, t in documents}
    records = []

    for path, position, order_source in ordered:
        text = text_by_path.get(path, '')
        fm = extract_frontmatter(text)
        title = extract_title(text, path)
        book, chapter = extract_book_chapter(text, path, fm)
        summary = extract_summary(text)
        wc = word_count(text)
        cc = len(text)
        try:
            sb = os.path.getsize(path)
        except OSError:
            sb = 0

        records.append({
            "position":     position,
            "filename":     Path(path).name,
            "path":         path,
            "title":        title,
            "book":         book,
            "chapter":      chapter,
            "word_count":   wc,
            "char_count":   cc,
            "size_bytes":   sb,
            "order_source": order_source,
            "summary":      summary,
        })

    records.sort(key=lambda r: r["position"])
    return records


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_json(records: list, path: str) -> None:
    total_words = sum(r["word_count"] for r in records)
    output = {
        "timestamp":        datetime.now().isoformat(),
        "total_documents":  len(records),
        "total_words":      total_words,
        "total_chars":      sum(r["char_count"] for r in records),
        "total_bytes":      sum(r["size_bytes"] for r in records),
        "unresolved_count": sum(1 for r in records if r["order_source"] == "unresolved"),
        "documents":        records,
    }
    with open(path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"  JSON manifest: {path}")


def write_markdown(records: list, path: str) -> None:
    total_words = sum(r["word_count"] for r in records)
    unresolved = [r for r in records if r["order_source"] == "unresolved"]

    lines = [
        "# MASTER MANIFEST",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## Corpus Statistics",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Documents | {len(records)} |",
        f"| Total words | {total_words:,} |",
        f"| Total bytes | {sum(r['size_bytes'] for r in records):,} |",
        f"| Unresolved positions | {len(unresolved)} |",
        "",
        "---",
        "",
        "## Sequence",
        "",
        "| # | Title | Book | Ch | Words | Source | Summary |",
        "|---|-------|------|----|-------|--------|---------|",
    ]

    for r in records:
        flag = " ⚠" if r["order_source"] == "unresolved" else ""
        src_short = r["order_source"].split(":")[0]  # strip field name
        lines.append(
            f"| {r['position']} "
            f"| {r['title']}{flag} "
            f"| {r['book']} "
            f"| {r['chapter']} "
            f"| {r['word_count']:,} "
            f"| {src_short} "
            f"| {r['summary'][:80]}... |"
        )

    if unresolved:
        lines += [
            "",
            "---",
            "",
            "## ⚠ Unresolved Positions",
            "",
            "These documents have no deterministic sequence marker and no LLM position.",
            "Add them to `SEED_ORDER.json` to assign explicit positions.",
            "",
        ]
        for r in unresolved:
            lines.append(f"- `{r['filename']}`")

    lines += [
        "",
        "---",
        "",
        "## Order Sources",
        "",
        "| Source | Meaning |",
        "|--------|---------|",
        "| `frontmatter:*` | Position from YAML frontmatter field |",
        "| `filename` | Position from numeric prefix in filename |",
        "| `llm` | Position inferred by LLM from title + opening |",
        "| `seed` | Position from SEED_ORDER.json (manual override) |",
        "| `unresolved` | No position determined — appended at end |",
    ]

    with open(path, 'w') as f:
        f.write("\n".join(lines))
    print(f"  Markdown manifest: {path}")


def write_seed_template(records: list, path: str) -> None:
    """Write a SEED_ORDER.json template pre-populated with current positions."""
    seed = {r["filename"]: r["position"] for r in records}
    with open(path, 'w') as f:
        json.dump(seed, f, indent=2)
    print(f"  Seed template: {path}  (edit and re-run with --seed to override)")


def print_summary(records: list) -> None:
    total_words = sum(r["word_count"] for r in records)
    sources = defaultdict(int)
    for r in records:
        sources[r["order_source"].split(":")[0]] += 1

    sep = "=" * 64
    print(sep)
    print("  MASTER MANIFEST  —  LEVEL 3")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)
    print(f"  Documents       : {len(records)}")
    print(f"  Total words     : {total_words:,}")
    print(f"  Order sources   :")
    for src, count in sorted(sources.items()):
        print(f"    {src:<20}: {count}")
    print(sep)
    print()

    # Show first 10 and last 5
    print("  SEQUENCE PREVIEW\n")
    for r in records[:10]:
        flag = " [UNRESOLVED]" if r["order_source"] == "unresolved" else ""
        print(f"  {r['position']:>3}.  {r['title'][:50]:<50}  {r['word_count']:>6} words{flag}")
    if len(records) > 15:
        print(f"       ... {len(records) - 15} more ...")
    for r in records[-5:]:
        flag = " [UNRESOLVED]" if r["order_source"] == "unresolved" else ""
        print(f"  {r['position']:>3}.  {r['title'][:50]:<50}  {r['word_count']:>6} words{flag}")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Level 3: Publication Manifest Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input-dir", required=True, metavar="DIR",
        help="Canonical document directory."
    )
    parser.add_argument(
        "--llm", action="store_true",
        help="Use LLM to fill positions for unordered documents. "
             "Requires ANTHROPIC_API_KEY env var."
    )
    parser.add_argument(
        "--seed", metavar="JSON",
        help="Path to SEED_ORDER.json for manual position overrides."
    )
    parser.add_argument(
        "--write-seed-template", action="store_true",
        help="Write SEED_ORDER_TEMPLATE.json with current positions for editing."
    )
    args = parser.parse_args()

    # Validate LLM flag
    api_key = None
    if args.llm:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("ERROR: --llm requires ANTHROPIC_API_KEY environment variable.",
                  file=sys.stderr)
            sys.exit(1)

    # Collect and load
    print(f"\n  Scanning: {args.input_dir}")
    paths = collect_files(args.input_dir)
    print(f"  {len(paths)} files found.\n")

    documents = []
    for p in paths:
        text = load_text(p)
        if text:
            documents.append((p, text))
        else:
            print(f"  SKIP (unreadable): {p}")

    print(f"  {len(documents)} documents loaded.\n")

    # Stage 1: Deterministic
    print("  Stage 1: Deterministic extraction...")
    positions = stage1_deterministic(documents)
    resolved_count = sum(1 for src in positions.values() if src[1] != 'unresolved')
    print(f"  Resolved: {resolved_count}/{len(documents)}")

    # Stage 2: LLM gap-fill
    if args.llm and api_key:
        print("\n  Stage 2: LLM gap-fill...")
        positions = stage2_llm(documents, positions, api_key)

    # Stage 3: Seed override
    if args.seed:
        print(f"\n  Stage 3: Seed override from {args.seed}...")
        positions = stage3_seed(documents, positions, args.seed)

    # Normalise to clean 1-indexed positions
    ordered = normalise_positions(documents, positions)

    # Build manifest records
    records = build_manifest(documents, ordered)

    # Output
    print_summary(records)
    write_json(records, "MASTER_MANIFEST.json")
    write_markdown(records, "MASTER_MANIFEST.md")

    if args.write_seed_template:
        write_seed_template(records, "SEED_ORDER_TEMPLATE.json")

    unresolved = sum(1 for r in records if r["order_source"] == "unresolved")
    if unresolved:
        print(f"\n  ⚠  {unresolved} documents have no sequence position.")
        print("  Run with --write-seed-template to generate a template,")
        print("  edit it, then re-run with --seed SEED_ORDER_TEMPLATE.json\n")
    else:
        print("  All documents have resolved positions.\n")


if __name__ == "__main__":
    main()
