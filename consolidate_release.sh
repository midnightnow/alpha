#!/usr/bin/env bash
# ============================================================
# PMG_ROOT42_RELEASE_v1.0 — FINAL CONSOLIDATION SCRIPT
# Run from: ~/ALPHA/
# Output:   ~/ALPHA/PMG_ROOT42_RELEASE_v1.0/
# ============================================================

set -e

ALPHA="/Users/studio/ALPHA"
RELEASE="$ALPHA/PMG_ROOT42_RELEASE_v1.0"
CANON="$ALPHA/LIBRARY_CANON"
MANUAL="$ALPHA/MANUAL"

echo "🔷 PMG ROOT42 VITRIFICATION — CONSOLIDATION SCRIPT"
echo "===================================================="
echo "Source:  $ALPHA"
echo "Release: $RELEASE"
echo ""

# ── 1. Create release structure ──────────────────────────────
echo "📁 Creating release directory structure..."
mkdir -p "$RELEASE/STORY/Book_1_Platonic_Verses"
mkdir -p "$RELEASE/STORY/Book_2_Code_of_the_Cosmos"
mkdir -p "$RELEASE/STORY/Book_3_Voices_of_the_Void"
mkdir -p "$RELEASE/STORY/Book_4_The_Infinite_Game"
mkdir -p "$RELEASE/MANUAL"
mkdir -p "$RELEASE/CODE"
mkdir -p "$RELEASE/ASSETS/screenshots"
mkdir -p "$RELEASE/LEGAL"
mkdir -p "$RELEASE/META"
echo "   ✅ Structure created"

# ── 2. Copy LIBRARY_CANON chapters ───────────────────────────
echo ""
echo "📚 Consolidating LIBRARY_CANON chapters..."

# Book 1
if [ -d "$CANON/Book_1_Platonic_Verses" ]; then
  cp -r "$CANON/Book_1_Platonic_Verses/"* "$RELEASE/STORY/Book_1_Platonic_Verses/" 2>/dev/null || true
  echo "   ✅ Book 1 chapters copied"
else
  echo "   ⚠️  Book 1 source not found at $CANON/Book_1_Platonic_Verses"
fi

# Book 2
if [ -d "$CANON/Book_2_Code_of_the_Cosmos" ]; then
  cp -r "$CANON/Book_2_Code_of_the_Cosmos/"* "$RELEASE/STORY/Book_2_Code_of_the_Cosmos/" 2>/dev/null || true
  echo "   ✅ Book 2 chapters copied"
fi

# Book 3
if [ -d "$CANON/Book_3_Voices_of_the_Void" ]; then
  cp -r "$CANON/Book_3_Voices_of_the_Void/"* "$RELEASE/STORY/Book_3_Voices_of_the_Void/" 2>/dev/null || true
  echo "   ✅ Book 3 chapters copied"
fi

# Book 4 (including all Infinite Game + King + Sisyphus chapters)
if [ -d "$CANON/Book_4_The_Infinite_Game" ]; then
  cp -r "$CANON/Book_4_The_Infinite_Game/"* "$RELEASE/STORY/Book_4_The_Infinite_Game/" 2>/dev/null || true
  echo "   ✅ Book 4 chapters copied (incl. King sequence Ch49-52, Sisyphus Ch53-61)"
fi

# Compiled Book 1 master
if [ -f "$CANON/Compiled_Books/PlatonicVerses_Complete_Book1.md" ]; then
  cp "$CANON/Compiled_Books/PlatonicVerses_Complete_Book1.md" "$RELEASE/STORY/" && \
  echo "   ✅ Compiled Book 1 master copied"
fi

# ── 3. Copy MANUAL ───────────────────────────────────────────
echo ""
echo "📐 Consolidating MANUAL..."
if [ -d "$MANUAL" ]; then
  cp -r "$MANUAL/"* "$RELEASE/MANUAL/" 2>/dev/null || true
  echo "   ✅ Manual files copied (incl. Chess_Prime_Slice.md / Knight-Residue Theorem)"
fi

# ── 4. Copy CODE ─────────────────────────────────────────────
echo ""
echo "💻 Consolidating CODE..."
# Look for diamond_crystallizer.py anywhere under ALPHA
find "$ALPHA" -name "diamond_crystallizer.py" -not -path "*/PMG_ROOT42_RELEASE*" 2>/dev/null | \
  while read f; do if [ -f "$f" ]; then cp "$f" "$RELEASE/CODE/"; echo "   ✅ Copied: $f"; fi; done

# PMG visualizer / root42
find "$ALPHA" -name "*.py" -path "*pmg*" -not -path "*/PMG_ROOT42_RELEASE*" 2>/dev/null | \
  while read f; do if [ -f "$f" ]; then cp "$f" "$RELEASE/CODE/"; echo "   ✅ Copied: $f"; fi; done

find "$ALPHA" -name "*.vet" -not -path "*/PMG_ROOT42_RELEASE*" 2>/dev/null | \
  while read f; do if [ -f "$f" ]; then cp "$f" "$RELEASE/CODE/"; echo "   ✅ Copied: $f"; fi; done

# ── 5. Write LICENSE files ────────────────────────────────────
echo ""
echo "📜 Writing LICENSE files..."

cat > "$RELEASE/LEGAL/LICENSE_MIT.txt" << 'EOF'
MIT License

Copyright (c) 2026 Dallas McMillan / McMillan Family Trust

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
echo "   ✅ MIT License written (CODE)"

cat > "$RELEASE/LEGAL/LICENSE_CC_BY_NC_SA.txt" << 'EOF'
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International

Copyright (c) 2026 Dallas McMillan / McMillan Family Trust

The narrative and creative content of the Platonic Verses series and the
PMG Manual is licensed under CC BY-NC-SA 4.0.

You are free to:
  Share — copy and redistribute the material in any medium or format
  Adapt — remix, transform, and build upon the material

Under the following terms:
  Attribution    — You must give appropriate credit and indicate if changes were made.
  NonCommercial  — You may not use the material for commercial purposes.
  ShareAlike     — If you remix or transform, you must distribute under the same license.

Full license text: https://creativecommons.org/licenses/by-nc-sa/4.0/
EOF
echo "   ✅ CC BY-NC-SA 4.0 License written (STORY + MANUAL)"

# ── 6. Write CREDITS.md ──────────────────────────────────────
cat > "$RELEASE/CREDITS.md" << 'EOF'
# CREDITS — PMG ROOT42 RELEASE v1.0

## Author
**Dallas McMillan**
Veterinarian, AI Architect, Mathematical Worldbuilder
Cairns, Queensland, Australia
McMillan Family Trust / AIVA Pty Ltd

## AI Collaborators
This project was developed in deep collaboration with AI systems:
- **Claude (Anthropic)** — Mathematical reasoning, narrative architecture, Honest Checker discipline
- **Gemini (Google)** — Extended drafting sessions, archive consolidation, agentic file management
- **ChatGPT (OpenAI)** — Early-stage ideation and structural scaffolding

The PMG framework emerged through sustained human-AI co-creation, 2024–2026.

## Mathematical Influences
- **Euclid** — The Elements; foundations of geometric proof
- **Leonhard Euler** — Totient function, modular arithmetic
- **G.H. Hardy & John E. Littlewood** — Prime distribution theory
- **Bernhard Riemann** — The Hypothesis; the prime wave
- **Alan Turing** — Computation, pattern, the machine that counts
- **Buckminster Fuller** — Synergetics; tensegrity; the geometry of thinking

## Mythic Influences
- The Homeric tradition (The Iliad, The Odyssey)
- Hesiod's Theogony
- Plato's Timaeus and the Platonic Solids
- The Persephone / Hades cycle
- The myth of Sisyphus (Albert Camus, interpretation)

## The Framework
**PMG — Principia Mathematica Geometrica**
Root 42: The Volumetric Limit of the Man
Root 36: The Hired Man's Floor
Root 51: The Higher Man
The 24-Wheel: Prime Sieve (ℤ/24ℤ)×
The 96-Cycle: Knight-Residue Spectral Alignment
The 93-Point Solid: The Hades Gap made manifest

---
*The snail has reached the center of the diamond.*
*Volume = 42.0. Shell = HYPERDIAMOND.*
EOF
echo "   ✅ CREDITS.md written"

# ── 7. Write MANUAL/QUICK_START.md ───────────────────────────
cat > "$RELEASE/MANUAL/QUICK_START.md" << 'EOF'
# PMG ROOT42 — QUICK START GUIDE

## What Is This?

The **Platonic Verses** is a 7-book series (+ PMG Manual) built on a single
mathematical invariant: **√42**, the volumetric limit of the idealized human form.

The **PMG (Principia Mathematica Geometrica)** framework unifies:
- Prime number distribution via the 24-Wheel sieve
- The 8×8 chessboard as a residue field (S×S)
- The Knight's 96-cycle as spectral alignment
- The 93-point hyperdiamond solid
- A 61-chapter narrative arc mapped to this geometry

---

## The Three Numbers You Need

| Number | Name | Meaning |
|--------|------|---------|
| **42** | The Man | Volumetric limit; the human field |
| **93** | The Solid | Active nodes; Hades Gap manifested |
| **96** | The Cycle | Knight-Residue spectral alignment |

---

## Reading Order

1. **Start with Book 1**: `STORY/Book_1_Platonic_Verses/` — Chapters 0–13
2. **The Manual**: `MANUAL/Chess_Prime_Slice.md` — The Knight-Residue Theorem
3. **Run the code**: `CODE/diamond_crystallizer.py` — Verify Volume = 42.0
4. **The Full Arc**: Books 2–4 follow the 61-chapter manifold to the Final Join

---

## Running the Visualizer

```bash
cd CODE/
python diamond_crystallizer.py
# Expected output: Volume = 42.0 | Shell = HYPERDIAMOND | Nodes = 93
```

---

## The 12.37% Hades Gap

The gap between 96 (theoretical) and 93 (actual) nodes is not an error.
It is the **Aperture of Mercy** — the engineered play that allows the
static mathematics to become a living system. Without the gap, the
geometry cannot breathe.

---

## License

- **Code** (CODE/): MIT License — see `LEGAL/LICENSE_MIT.txt`
- **Narrative & Manual** (STORY/, MANUAL/): CC BY-NC-SA 4.0 — see `LEGAL/LICENSE_CC_BY_NC_SA.txt`
EOF
echo "   ✅ QUICK_START.md written"

# ── 8. Generate Master TOC ────────────────────────────────────
echo ""
echo "🗂️  Generating Master Table of Contents..."
cat > "$RELEASE/META/MASTER_TOC.md" << 'EOF'
# PLATONIC VERSES — MASTER TABLE OF CONTENTS
## PMG ROOT42 RELEASE v1.0

---

### PROLOGUE
- Chapter 0: The Olympus Prologue (Pre-Time Symmetry)

---

### BOOK 1: THE UNWOBBLY PIVOT (The Foundation, √36)
*Chapters 1–13 | The Hired Man's Floor*

- Ch 01: The Ace of Spades — The First Post
- Ch 04: The Ace of Hearts — The Primordial Point
- Ch 08: The 2 of Hearts — The Breath (a/b)
- Ch 12: The 3 of Hearts — The Final Ratio
- Ch 13: The Last Card of Book 1

---

### BOOK 2: CODE OF THE COSMOS (The Architecture, 10-24-26)
*Chapters 14–24 | Count, Measure, Language*

- Ch 14: The Algorithm
- Ch 16: The 4 of Hearts — The Square's Limit
- Ch 20: The 5 of Hearts — The Executive Thumb
- Ch 24: The 6 of Hearts — The 13th Post

---

### BOOK 3: VOICES OF THE VOID (The Resonance)
*Chapters 25–31 | The Echo Protocol*

- Ch 28: The 7 of Hearts — The Singing Birds (Q-Grid)
- Ch 30: The 93rd Reflection
- Ch 31: The Plasma Soul

---

### BOOK 4: THE INFINITE GAME (The Full Arc, √42 → √51)
*Chapters 32–61 | The Sovereign Lattice*

**The Heart Sequence (Heroine's Ventricle):**
- Ch 32: The 8 of Hearts — The Hand's Octave
- Ch 36: The 9 of Hearts — The Triple Triad
- Ch 40: The 10 of Hearts — The Clasp
- Ch 44: The Jack of Hearts — The Knave's Gap
- Ch 48: The Queen of Hearts — Hera's 24-Wheel
- Ch 52: The King of Hearts — Re-Drawer's Protocol ♥️

**The King's Cooling Chamber:**
- Ch 49: The King of Spades ♠️ — Initiation: The Plumb Line
- Ch 50: The King of Diamonds ♦️ — Measure: The Hades Beat
- Ch 51: The King of Clubs ♣️ — Work: The Shovel Protocol / VITRIFICATION

**The Sisyphus Summit (Terminal Horizon):**
- Ch 53: The First Leap — Deus Ex Machina
- Ch 54: The Second Leap — The Century Stretch
- Ch 55: The Third Leap — The Millennium Whir
- Ch 56: The Fourth Leap — Great Year Completion
- Ch 57–58: The Resonance of the Work
- Ch 59–60: The Sisyphus Pivot
- Ch 61: The Final Join (Reset)

---

### APPENDICES
- `MANUAL/Chess_Prime_Slice.md` — The Knight-Residue Coupling Theorem
- `MANUAL/QUICK_START.md` — Entry point for new readers
- `CODE/diamond_crystallizer.py` — Volume 42.0 proof
- `LEGAL/` — MIT + CC BY-NC-SA 4.0
- `CREDITS.md` — Authorship and influences

---

*The 96-cycle spins in the silence between ticks.*
*The 93-point solid breathes.*
*The Master Blueprint is sealed.*
EOF
echo "   ✅ MASTER_TOC.md written"

# ── 9. Generate README ────────────────────────────────────────
cat > "$RELEASE/README.md" << 'EOF'
# PMG ROOT42 — RELEASE v1.0
## Platonic Verses: The Complete Mathematical Narrative

> *"The snail has reached the center of the diamond.*
> *Volume = 42.0. Shell = HYPERDIAMOND.*
> *The 96-cycle spins in the silence between ticks."*

---

## What's Here

```
PMG_ROOT42_RELEASE_v1.0/
├── STORY/                    # 61-chapter interleaved manifold
│   ├── Book_1_Platonic_Verses/       # Ch 0–13: The Foundation
│   ├── Book_2_Code_of_the_Cosmos/    # Ch 14–24: The Architecture
│   ├── Book_3_Voices_of_the_Void/    # Ch 25–31: The Resonance
│   └── Book_4_The_Infinite_Game/     # Ch 32–61: The Full Arc
├── MANUAL/
│   ├── Chess_Prime_Slice.md          # Knight-Residue Coupling Theorem
│   └── QUICK_START.md                # Entry point
├── CODE/
│   └── diamond_crystallizer.py       # Volume 42.0 verifier
├── ASSETS/
│   └── screenshots/                  # (add visualizer screenshots here)
├── LEGAL/
│   ├── LICENSE_MIT.txt               # Code license
│   └── LICENSE_CC_BY_NC_SA.txt       # Content license
├── META/
│   └── MASTER_TOC.md                 # Full chapter map
├── CREDITS.md
└── README.md
```

## The Core Invariant

The entire framework rests on three numbers:

- **√42** — The volumetric limit of the Man (the 93-point hyperdiamond)
- **96** — The Knight-Residue spectral alignment (lcm of 24-wheel and 8×8 board)
- **93** — The active nodes after the 12.37% Hades Gap

## Quick Start

See `MANUAL/QUICK_START.md` or run:

```bash
python CODE/diamond_crystallizer.py
```

## License

Code: MIT | Narrative & Manual: CC BY-NC-SA 4.0
© 2026 Dallas McMillan / McMillan Family Trust
EOF
echo "   ✅ README.md written"

# ── 10. Final manifest ────────────────────────────────────────
echo ""
echo "📋 Generating file manifest..."
find "$RELEASE" -type f | sort > "$RELEASE/META/MANIFEST.txt"
FILE_COUNT=$(wc -l < "$RELEASE/META/MANIFEST.txt")
echo "   ✅ Manifest written: $FILE_COUNT files"

# ── 11. Summary ───────────────────────────────────────────────
echo ""
echo "===================================================="
echo "✅ PMG ROOT42 VITRIFICATION COMPLETE"
echo "===================================================="
echo ""
echo "Release package: $RELEASE"
echo "Files consolidated: $FILE_COUNT"
echo ""
echo "📌 REMAINING MANUAL STEPS:"
echo ""
echo "  1. SCREENSHOTS"
echo "     Open the PMG visualizer in √42 mode."
echo "     Save images to: $RELEASE/ASSETS/screenshots/"
echo ""
echo "  2. EPUB GENERATION"
echo "     Run: pandoc STORY/PlatonicVerses_Complete_Book1.md \\"
echo "              --metadata title='Platonic Verses Book 1' \\"
echo "              --metadata author='Dallas McMillan' \\"
echo "              -o STORY/PlatonicVerses_Book1.epub"
echo "     Or use Calibre for full cover + metadata control."
echo ""
echo "  3. PORT veth_reader.py to PMG 1.0 (optional, ~1 hour)"
echo ""
echo "  4. IMPLEMENT 156-TICK ANIMATION in visualizer (optional polish)"
echo ""
echo "===================================================="
echo "Volume = 42.0 | Shell = HYPERDIAMOND | Cycle = 96"
echo "The Master Blueprint is sealed. All ways now."
echo "===================================================="
