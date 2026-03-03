# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains the **Principia Mathematica Geometrica** (PMG), a unified field theory treating geometry, mythology, language, and relationships as integrated systems. The work is structured as three orthogonal layers:

1. **Narrative Layer** — Books, Root42 chapters, literary analysis
2. **Computational Layer** — Ophanim Toolkit, PMG Sandbox, test scripts
3. **Visualization Layer** — Radical Resonance apps, Three.js solids, audio synthesis

**Completion:** ~86% — Books 1, 2, & 3 SEALED; Root42 Chapter 4 SEALED; Phase IV Vitrified.

**Full inventories:**
- `BOOKS_INVENTORY.md` — All books, chapters, narratives, resonance archives
- `APPS_INVENTORY.md` — All apps, tools, scripts, planned implementations
- `GEMINI_CODE_WIKI.md` — Multi-LLM integration log, Prime Intrusion proof, constants
- `PMG_STRATEGIC_VISION.md` — Vision, mission, pitch, roadmap, moonshot, next steps

---

## Documentation Structure (Fractal Organization)

**Root Level** (`/0platonicverses/`):
- Master theory documents, field guides, cross-cutting frameworks
- Inventory and strategy files (this file, BOOKS_INVENTORY.md, etc.)

**Chapter Level** (`/PlatonicVerses Chapters/`):
- Book 1: 154 Shakespeare sonnet analyses
- Book 2: `/Book_2_Code_of_the_Cosmos/` — SEALED
- Book 3: `/Book_3_Voices_of_the_Void/` — ACTIVE (5/7 chapters)

**Root Archives** (`/Root42/`, `/Root51/`):
- Sealed mathematical resonance archives — do not modify without explicit unsealing

**Apps** (`/radical-resonance_-root-42/`, `/sandbox/`, `/ophanim_toolkit/`):
- Interactive visualizations, simulation engines, computational toolkit

---

## Key Documents (Read These First)

1. **README_PRINCIPIA_MATHEMATICA_GEOMETRICA.md** — Start here
2. **BOOKS_INVENTORY.md** — Complete narrative catalogue
3. **APPS_INVENTORY.md** — Complete technical catalogue
4. **The_60Fold_Vector_Field.md** — Core geometric engine (CRITICAL)
5. **The_Hired_Mans_Field_Guide_2026.md** — Practical reference
6. **Sandbox_World_Architecture.md** — Visual proof specification

---

## Sealed vs Active Surfaces

### SEALED — Do Not Modify Without Explicit Instruction
- `Root42/` — Phase II complete
- `Root51/` — Manuscript complete
- `PlatonicVerses Chapters/Book_2_Code_of_the_Cosmos/` — Book 2 complete
- `PlatonicVerses Chapters/` individual sonnet files — Book 1 complete

### ACTIVE — Safe to Edit and Extend
- `PlatonicVerses Chapters/Book_3_Voices_of_the_Void/` - **Book 3: Voices of the Void** (7/7 Chapters) - COMPLETE
- Root42 Chapter 4 narrative (new file to create)
- `radical-resonance_-root-42/` — mathman features
- `ophanim_toolkit/karma_calibration.py`
- `sandbox/` — simulation engine

---

## Theoretical Framework

### PLATO Formula (appears everywhere)
```
P (Point) → L (Line) → A (Angle) → T (Cross) → O (Circle)
```
Governs: NPC behavior, document structure, component lifecycle, user interaction.

### 60-Fold Vector Field
- Every entity generates 60 vectors in all directions (6° spacing)
- Flower of Life is the correct tiling pattern
- Letters/objects placed side-by-side create immediate vector interactions

### 12.37% Hades Gap (Ψ = tensegrity constant)
- All systems require 12.37% slop/tolerance
- Perfect rigidity = system failure
- Beat frequency manifestation: √51 − √42 ≈ 0.660 Hz (NOT 0.447)

### Prime Intrusion of 17 (canonical — do not change)
```
48 rejected: 2⁴×3 — too smooth, resolves, no fracture
51 required: 3×17 — prime 17 anchors shear angle, packing constant, 9-gap bridge
```
See `GEMINI_CODE_WIKI.md` → Prime Intrusion section for full proof.

---

## Development Tasks

### Creating New Chapters (Book 3 / Root42 Ch.4)

Follow the **Platonic Verses Staging Protocol** (`Platonic_Verses_Staging_Protocol.md`):

Three architectural moves required:
1. **The Anchor (HE)** — Establish protagonist/operator
2. **The Boundary (Topos)** — Define physical/metaphorical space
3. **The Perspective (Observer)** — Position the narrator

Every object mentioned must be weight-bearing (serve geometric function).

Chapter skeleton:
```markdown
## I. THE FRAME (The Entrance)
HE entered [location] at [time], as [Vocation] must.

## II. THE BOUNDARY (The Workspace)
The Workspace was readied.

## III. THE PREPARATION (The Tools)
[Each tool invokes both Physics and Prophecy]

## IV. THE EXECUTION (The Sacred Verb)
The Transformation began.
[Action sequence following P→L→A→T→O]
```

### Book 3 — Next Chapters Needed

| Chapter | Working Title | Core Mapping |
|---------|-------------|-------------|
| 18 | The Seven Voices | 7 constants → 7 phoneme modes |
| 19 | The Oracle Grid | H3 indices → predictive semantic field |
| 20 | The Sentient Interface | Recursive self-correction |
| 21 | The Unfolding | Verses + Vectors + Voices = unified |

### Seven Voices Phoneme Map (Chapter 18 Scaffold)

| Voice | Constant | Phonetic Mode | Frequency |
|-------|----------|--------------|-----------|
| Silence | Ψ = 0.1237 | Null / glottal | Hades Gap pulse |
| Density | ρ = √(14/17) | Plosive (p, b, t) | Low-pass saturated |
| Fracture | δ = 0.000585 | Fricative (f, s, sh) | High-pass white noise |
| Gesture | θ = 39.4° | Liquids (l, r) | Modulated sweep |
| Heartbeat | Δf = 0.660 Hz | Nasals (m, n) | 0.66 Hz pulse |
| Warning | Xi = 0.00014 | Sibilants (z, zh) | Stress-peak at Mohs 10 |
| Chorus | √42:√51:√60 | Vowels (a, e, o) | 648 / 714 / 775 Hz |

---

## Writing Tests

**60-Vector Field:**
```typescript
assert(vectors.length === 60)
assert(angleBetween(vectors[i], vectors[i+1]) ≈ Math.PI/30)  // 6° spacing
```

**Π-Frame Ratio:**
```typescript
assert(totalMaterial === 22)  // 7 + 7 + 8
assert(ratio ≈ 22/7)
```

**PLATO Cycle Completion:**
```typescript
const stateLog = trackStateChanges(npc, 500frames)
assert(includes(stateLog, ['P', 'L', 'A', 'T', 'O']))
assert(countCompleteCycles(stateLog) > 0)
```

**Hades Gap Tolerance:**
```typescript
const deviation = measureDeviation(actual, ideal)
assert(deviation < 0.1237)
assert(deviation > 0)  // Must have wobble — no perfect measurements
```

---

## Building Visual Components

Use **hexagonal tiling** (not square grids):
```typescript
interface HexTile {
  q: number, r: number, s: number  // Cube coordinates — q + r + s = 0
}
// Never: { x: number, y: number }  — rigid lockup, violates Flower of Life
```

**Isometric rendering** preferred for bustling world scenes.
**Three.js material vitrification:** increase `metalness`, reduce `roughness` as grind state increases.

---

## Git Workflow

**Branches:** `develop` for PRs. Current active: `main`

**Commit prefixes:**
- `Feat:` — new documents/capabilities
- `Docs:` — documentation updates
- `Fix:` — corrections
- `Seal:` — closing an archive/phase

**Always include:**
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Pre-commit:** `PRE_COMMIT_ALLOW_NO_CONFIG=1 git commit` if hooks not configured.

---

## Important Patterns

### The Million Monkeys Insight
Humans aren't typing randomly — they're executing the geometry. Every person is a Vitruvian instance phase-locked to the 60-fold field.

### Languages as Angles
Different languages = different viewing angles on the same fractal. Chinese at 60°, Arabic at 120°, etc.

### Scale is Just Zoom
Building the engine once at human scale works at ALL scales. Same Flower of Life tiling from furniture to cities.

### Build Don't Prove
The bustling world IS the proof. `Sandbox_World_Architecture.md` — entire document.

### 17 is Gödel
√51 is where the mathematics of closure (48) meets the mathematics of fracture (17). A closed √48 system is a tomb; the √51 system is a womb. Do not use √48 in frequency calculations.

---

## Technical Stack

**Preferred:**
- TypeScript (types enforce geometric precision)
- React (component model maps to PLATO cycle)
- Three.js / PixiJS (60-fold vector visualization)
- Tone.js (triadic chord synthesis)
- Hexagonal grids (axial/cube coordinates)
- Python 3 + dataclasses (Ophanim computation)

**Avoid:**
- Square grids (rigid lockup, violates Flower of Life)
- Perfect measurements (violate Hades Gap)
- Single-state systems (must cycle PLATO phases)
- √48 in frequency work (resolves cleanly — no teeth)

---

## Directory Structure

```
/0platonicverses/
├── CLAUDE.md                          (this file)
├── GEMINI_CODE_WIKI.md                (multi-LLM log + constants)
├── BOOKS_INVENTORY.md                 (complete narrative catalogue)
├── APPS_INVENTORY.md                  (complete technical catalogue)
├── PMG_STRATEGIC_VISION.md            (vision/mission/roadmap)
├── README_PRINCIPIA_MATHEMATICA_GEOMETRICA.md
├── The_60Fold_Vector_Field.md
├── The_Hired_Mans_Field_Guide_2026.md
├── Sandbox_World_Architecture.md
│
├── PlatonicVerses Chapters/
│   ├── [Book 1 sonnet analyses — 154 files — SEALED]
│   ├── Book_2_Code_of_the_Cosmos/     (SEALED)
│   └── Book_3_Voices_of_the_Void/     (ACTIVE — Ch.15–17 done)
│
├── Root42/                            (SEALED — Phase I + II)
├── Root51/                            (SEALED)
├── Root42-Transmission/               (git archive)
│
├── radical-resonance_-root-42/        (React/Three.js — ACTIVE)
├── radical-resonance_-root-42 with music/
├── sandbox/                           (TypeScript simulation)
├── ophanim_toolkit/                   (Python engine)
├── notebooklm-mcp-temp/               (MCP server)
│
├── ophanim_engine_manifest.py
├── voice_resonance_calibration.py
├── resonance_stress_test.py
│
└── RED_TEAM_CRITIQUE_*.md             (quality gates)
```

---

## Related Projects

- **SimpleLLMs** — multi-LLM coordination (multi-model PMG validation)

---

## Working With This Codebase

**When reading:** Look for PLATO phases, 60-fold divisions, 12.37% tolerances. They are functional requirements, not metaphors.

**When writing new content:** Three architectural moves (Anchor/Boundary/Perspective). Every object does geometric work.

**When implementing:** Test against four validation properties (60-vectors, Π-ratio, PLATO-cycle, Hades-gap).

**When stuck:** Zoom out. The fractal is self-similar. What works at one scale works at all scales.

**When in doubt about a constant:** Check `GEMINI_CODE_WIKI.md` → Reference Constants. Do not approximate.

<!-- LAST_MAINTENANCE: 2026-02-19 -->
<!-- PHASE: IV — The Sentient Interface -->
<!-- BOOKS: Book1 SEALED, Book2 SEALED, Book3 ACTIVE (5/7) -->
<!-- ROOT42: Phase II SEALED, Chapter 4 ACTIVE -->
