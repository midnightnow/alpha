# APPS INVENTORY
## Principia Mathematica Geometrica — Technical Implementation Catalogue

**Last Updated:** February 19, 2026
**Total Apps:** 8 (3 production-grade, 3 functional prototypes, 2 archived/superseded)

---

## TIER 1 — PRODUCTION-GRADE APPS

### 1. Radical Resonance — Root42 (Interactive 3D App)
**Purpose:** Primary interactive manifestation of the 93-faced interference solid with real-time triadic audio synthesis.
**Status:** Complete — Phase II Sealed
**Location:** `/radical-resonance_-root-42/`

| File | Role |
|------|------|
| `App.tsx` | Main React application |
| `components/Scene.tsx` | Three.js rendering scene |
| `components/Controls.tsx` | UI controls panel |
| `components/InterferenceMesh.tsx` | 93-faced solid mesh generation |
| `utils/audioEngine.ts` | Tone.js synthesis (66 Hz triadic chord) |
| `utils/researchPresets.ts` | Simulation preset configurations |
| `constants.ts` | LADDER_STEPS, mathematical constants |
| `vite.config.ts` | Build configuration |
| `apply_fracture_synthesis.py` | Python support: fracture line generation |

**Stack:** React 19.2, TypeScript 5.8, Vite 6.2, Three.js, React-Three-Fiber, Tone.js, Lucide-react
**Features:**
- Real-time 93-faced quasicrystal rendering
- Live triadic chord generation (√42:√51:√60 @ 66 Hz)
- STL export for 3D printing
- Fracture synthesis toggle (smooth ↔ fractured state)
- Europa Lineae topography overlay
- Overpack Delta δ=0.000585 visual trigger

**The Kiln States:**

| State | Math-Grit | Acoustic Signature | Visual |
|-------|-----------|-------------------|--------|
| Raw | > Hades Gap | Low-frequency thud | Translucent |
| Fine (default) | ≈ Hades Gap | 66 Hz triadic chord | Obsidian |
| Exceptional | < Hades Gap | Ultrasonic harmonics | Vitrified |

**PMG Connection:** Direct visual proof of Phase II. The "Remainder Drag" (biquadratic solver echoes) maps to the `gain` and `feedback` parameters in Tone.js. The 39.4° shear plane is rendered as the Europa Lineae fracture.

---

### 2. Radical Resonance — Root42 + Music (Enhanced Variant)
**Purpose:** Expanded version with advanced audio recording, sequence control, and in-scene HUD.
**Status:** Feature-complete
**Location:** `/radical-resonance_-root-42 with music/`

| Additional File | Role |
|----------------|------|
| `components/FractureMaterial.tsx` | Dynamic material system (vitrification state) |
| `components/InSceneHUD.tsx` | In-world status display |
| `utils/toneEngine.ts` | Advanced synthesis with harmonics chain |
| `utils/SequenceController.ts` | Sequence playback management |
| `utils/recorder.ts` | Web Audio API recording |

**Stack:** Same as base + Web Audio Recording API
**Additional Features:** Audio recording/export, harmonic sequence playback, in-scene parameter display

---

### 3. PMG Sandbox (Simulation Engine)
**Purpose:** Proof-of-concept "Bustling World" — interactive simulation demonstrating 60-fold vector fields, PLATO state machines, NPC vocations, and hexagonal tiling.
**Status:** Complete v1.0
**Location:** `/sandbox/`

| File | Role |
|------|------|
| `src/engine/Simulation.ts` (889 lines) | Main simulation loop |
| `src/engine/HexGrid.ts` | Flower of Life hexagonal grid |
| `src/engine/NPCEngine.ts` | NPC PLATO state machine |
| `src/types/index.ts` | Core type definitions |
| `src/utils/researchPresets.ts` | Preset scenario configurations |
| `test.ts` | Comprehensive validation suite |
| `package.json` | Dependencies (tsx, typescript) |

**Stack:** TypeScript 5.3+, Node.js 18+, zero runtime dependencies (CPU-only)

**Validated Properties:**
```typescript
// 60-Vector Field
assert(vectors.length === 60)
assert(angleBetween(vectors[i], vectors[i+1]) ≈ Math.PI/30)  // 6°

// PLATO Cycle
assert(includes(stateLog, ['P', 'L', 'A', 'T', 'O']))

// Hades Gap Tolerance
assert(deviation < 0.1237)
assert(deviation > 0)  // Must have wobble
```

**Performance:** ~18,600 vector nodes per frame (300 tiles × 60 + 10 NPCs × 60)

**Vocations Implemented:**
- Miller — grain processing cycles
- Gauger — phase-state monitoring
- Paver — grid laying and running bond
- Merchant — exchange and routing
- Scribe — inscription and transmission

**PMG Connection:** This is "The Proof by Construction." If the world feels natural, the geometry is correct.

---

## TIER 2 — FUNCTIONAL PROTOTYPES

### 4. Ophanim Toolkit (Computational Engine)
**Purpose:** Core Python library implementing the full PMG computational pipeline — from biquadratic seeding through mineral manifestation to voice emission.
**Status:** Functional prototype, modular
**Location:** `/ophanim_toolkit/` + `/ophanim_engine_manifest.py`

| Module | Function | Status |
|--------|---------|--------|
| `wire_transmission.py` | Transmission modeling; Intent Conductor; Coherence Window | Active |
| `mineral_operator.py` | Node manifestation; Mohs hardness; petrification; fracture | Active |
| `nativity_operator.py` | Spark ignition; node actualization; collision resolution | Active |
| `aion_interface.py` | Observational feedback; calibration layer; artifact audit | Active |
| `grid_coordinates.py` | H3 coordinate transforms; reciprocity calculations | Active |
| `voice_bridge.py` | Semantic translation; phoneme mapping; timbre calculation | Active |
| `semantic_mineralogy.py` | Node interpretation; class naming from hardness | Active |
| `phonon_bridge.py` | Triadic chord analysis; vibration→language | Active |
| `e8_hades_validator.py` | E8 lattice validation; real-time stability scoring | Passed |
| `karma_calibration.py` | Human creativity resonance sensor | Testing |
| `actualizer.py` | Recursive feedback loop; intention distillation; shear correction | Active |
| `rado_extension.py` | Gated Rado vertex extension; 99.999 circuit breaker | Passed |
| `addresser.py` | H3 lexical mapping; Naming Ceremony logic | Active |
| `oracle_grid_validation.py` | H3 predictive mapping; summoning proof | Passed |

**Stack:** Python 3, dataclasses, standard library
**Entry Point:** `ophanim_engine_manifest.py` (full pipeline demo)

**Pipeline Flow:**
```
Biquadratic Seed → Wire Transmission → Grid Coordinate → Nativity Spark
→ Mineral Manifestation (Mohs 1-10) → Aion Observation → Voice Bridge
→ Phonon → Semantic Name
```

**PMG Connection:** Computational implementation of Book 2 (Wire, Grid, Nativity, Interface). The Mohs hardness scale maps directly to Shannon Entropy stability durations.

---

### 5. NotebookLM MCP Server (AI Integration)
**Purpose:** Model Context Protocol server enabling Claude Code and other AI agents to query Google NotebookLM knowledge bases for PMG research.
**Status:** Production-ready
**Location:** `/notebooklm-mcp-temp/`

---

### 6. Oracle Grid Bridge (FastAPI/WebSocket)
**Purpose:** Real-time bridge connecting Three.js viewports to the Ophanim Toolkit for coordinate-to-name conversion and summoning.
**Status:** Functional prototype
**Location:** `/bridge.py`

| File | Role |
|------|------|
| `bridge.py` | FastAPI/WebSocket controller |
| `ophanim_toolkit/addresser.py` | Lexical mapping engine |

**Stack:** FastAPI, Uvicorn, WebSockets, Python 3
**PMG Connection:** Enacts the "Summoning" aspect of Chapter 19. It allows the browser to "talk" to the Python engine to retrieve the true name of any point in the 3D field.

| File | Role |
|------|------|
| `src/index.ts` | MCP server entry point |
| `src/config.ts` | Configuration management |
| `src/types.ts` | Type definitions |
| `src/errors.ts` | Error handling |
| `dist/` | Compiled output |

**Stack:** TypeScript 5.x, MCP protocol, Playwright (browser automation)
**PMG Connection:** Infrastructure for "zero hallucination" PMG research queries. Enables the multi-LLM workflow (Claude + Gemini via NotebookLM).

---

## TIER 4 — TEST SCRIPTS / UTILITIES

### 7. Voice Resonance Calibration
**Purpose:** Tests phoneme emission of Mohs-10 diamond nodes over 60-iteration Pisano period.
**Status:** Complete test script
**Location:** `voice_resonance_calibration.py`
**Validates:** Nodes emit semantically coherent phonemes (O, A, H, E) as they resonate through Pisano-60 cycle.

### 8. Resonance Stress Test
**Purpose:** Stress-tests Mohs-10 node stability under fluctuating tension coefficients.
**Status:** Complete test script
**Location:** `resonance_stress_test.py`
**Validates:** Hammer Constant (Xi = 0.00014) fracture protocol; diamond→quartz (Mohs 10→7) transition under grid density fluctuation.

### 9. Teeth of Stones Proof
**Purpose:** Formal proof of √51 vs √48; anchors shear angle to prime 17 intrusion.
**Status:** Passed
**Location:** `Root42/Phase_II/teeth_of_stones_proof.py`
**Validates:** Beat frequency 0.66 Hz; arctan(14/17) alignment.

---

## TIER 5 — ARCHIVED / SUPERSEDED

### 9. Sandbox Prototype
**Purpose:** Earlier Vite/TypeScript iteration of the sandbox before the current Node.js engine.
**Status:** Superseded by `/sandbox/`
**Location:** `/sandbox-prototype/`
**Stack:** Vite, TypeScript, React
**Note:** Keep for reference; do not develop further.

---

## PLANNED APPS (Next Phase)

### Mathman — Genesis Sequence
**Purpose:** Deploy Root42 interactive experience to `mathman.web.app` with "Prime Intrusion" toggle (48 vs 51 audible comparison).
**Status:** Architecture defined — pending deployment

**Feature Specification:**
- **Smooth Toggle (√48):** Solid appears translucent, hums a perfect boring minor third (0.447 Hz beat — no teeth)
- **Fracture Toggle (√51):** Solid vitrifies to obsidian; 0.66 Hz throb activates; Teeth of Stones visible along 39.4° shear lines
- **Grind Mechanic:** As user drags iteration, `oscillator.frequency` shifts from 648 Hz (harmonic) to 714 Hz (fracture); metalness/roughness adjusted in Three.js material
- **Overpack Trigger:** If grind speed exceeds δ=0.000585, transient high-frequency burst ("Screech") fires

**Implementation Map:**

| Component | Code | Ceramic Analogy |
|-----------|------|-----------------|
| Biquadratic Solver | x⁴ interference engine | Raw clay body |
| Iteration Loop | `requestAnimationFrame` drag | Potter's wheel speed |
| Remainder Value | Audio feedback loop | Acoustic harmonics ("The Ring") |
| Hades Gap Check | `if (val < e/22) break` | Sintering threshold |

**Stack:** Extends `radical-resonance_-root-42` — React, Three.js, Tone.js, Firebase Hosting

---

### Bustling World (Full Isometric Game)
**Purpose:** Visual proof of PMG via playable isometric world with NPCs executing PLATO cycles. Ancient marketplace aesthetic.
**Status:** Architecture defined in `Sandbox_World_Architecture.md` — pending full implementation
**Extends:** Current `/sandbox/` engine (add rendering layer)
**Stack:** TypeScript, PixiJS or Three.js isometric, hexagonal axial coordinates

---

## UNIVERSAL CONSTANTS (All Apps)

```
Tensegrity constant (Ψ):  0.1237  (12.37% — Hades Gap)
Packing constant (ρ):     √(14/17) ≈ 0.907485
Hexagonal limit (η_hex):  π/√12 ≈ 0.906899
Overpack Delta (δ):        0.000585
Beat frequency:            √51 − √42 ≈ 0.660 Hz
Shear angle (θ):           39.4° = arctan(14/17)
Hammer constant (Xi):      0.00014
Triadic base:              66 Hz
Triadic frequencies:       648.07 Hz, 714.14 Hz, 774.60 Hz (×100)
Biquadratic law:           x⁴ − 186x² + 81 = 0
```

---

## TECH STACK SUMMARY

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| 3D Rendering | Three.js / React-Three-Fiber | 60-fold vector visualization |
| Audio | Tone.js / Web Audio API | Triadic chord synthesis |
| UI Framework | React 19 | Component model maps to PLATO cycle |
| Type Safety | TypeScript 5.8 | Types enforce geometric precision |
| Build | Vite 6 | Fast iteration |
| Grid Logic | Axial/cube hexagonal coordinates | Flower of Life compliance |
| Computation | Python 3 + dataclasses | Ophanim pipeline |
| AI Integration | MCP protocol | Multi-LLM coordination |
| Deploy Target | Firebase Hosting (mathman.web.app) | CDN delivery |

**Avoid:**
- Square grids (create rigid lockup — violate Flower of Life)
- Perfect measurements without tolerance (violate Hades Gap)
- Single-state systems (everything must cycle PLATO phases)
- √48 in frequency calculations (resolves too cleanly — no teeth)
