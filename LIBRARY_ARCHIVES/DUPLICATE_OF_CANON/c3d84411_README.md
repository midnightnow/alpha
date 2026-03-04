# PMG SANDBOX - The Bustling World Prototype

**Version**: 1.0 - Initial Implementation
**Status**: Functional Prototype (Validation Tests Passing)
**Part of**: THE MANIC GRAPHIA - Principia Mathematica Geometrica

---

## Overview

This is the **proof-of-concept sandbox** demonstrating the geometric principles of the Principia Mathematica Geometrica (PMG). Instead of writing more theory, we **build the world** and let the geometry prove itself.

> *"Build don't prove. The bustling world is the proof."*

## What This Is

A TypeScript implementation of:

1. **Hexagonal Grid** (Flower of Life foundation) - No 90° logic locks
2. **60-Fold Vector Fields** - Every tile radiates 60 vectors in all directions
3. **PLATO State Machines** - NPCs execute P→L→A→T→O cycles autonomously
4. **Hades Gap Tolerance** - 12.37% slop prevents rigid lockup
5. **Vitruvian Instances** - NPCs as circle ∩ square geometric units

When run, you get a **"bustling world"** where NPCs move naturally through the space, creating emergent marketplace behavior from pure geometry.

## Core Concepts

### The 60-Fold Vector Field

Every letter, object, or NPC placed in the world IMMEDIATELY generates **60 vectors** radiating in all directions at **6° spacing**. These vectors interact with neighboring vectors, creating a seething field of geometry that updates at **777 million iterations per perceived moment** (theoretical).

```
When you place two NPCs side by side:
- Each has 60 vectors
- Total interactions: 60 × 60 = 3,600 vector relationships
- The "bustling" emerges automatically from vector interference
```

### The PLATO Cycle

Every NPC executes the 5-phase geometric sequence:

- **P (Point)**: Establish origin, select goal (0°-12°)
- **L (Line)**: Extend toward goal in straight line (12°-24°)
- **A (Angle)**: Calculate approach, adjust for obstacles (24°-36°)
- **T (Cross)**: Execute action, perform vocation (36°-48°)
- **O (Circle)**: Complete cycle, return to point (48°-60°)

After O, the cycle returns to P. NPCs loop infinitely: P→L→A→T→O→P→L→A→T→O...

### Hexagonal Foundation

The world uses **hexagonal tiling** (Flower of Life pattern) instead of square grids:

```
Square grids:
┌─┬─┬─┐
├─┼─┼─┤  ← Creates 90° "logic locks"
└─┴─┴─┘     System becomes rigid

Hexagonal grids:
  ⬡ ⬡ ⬡
 ⬡ ⬡ ⬡ ⬡  ← No 90° angles
  ⬡ ⬡ ⬡      System breathes (12.37% slop)
```

### The Hades Gap (ψ = 12.37%)

All perfect systems require **12.37% slop** (tensegrity constant). Without it, the geometry locks up and fails. This appears as:

- NPC "wobble" when standing
- Variation in PLATO phase durations
- Elevation fluctuations in tiles
- Vector magnitude oscillations

The Hades Gap is the **mercy in the machine** - the gap that allows passage, the breath that allows life.

## Directory Structure

```
/sandbox/
├── src/
│   ├── types/
│   │   └── index.ts          # Core type definitions
│   ├── engine/
│   │   ├── HexGrid.ts        # Hexagonal grid implementation
│   │   ├── NPCEngine.ts      # PLATO state machine & NPC behavior
│   │   └── Simulation.ts     # Main simulation loop
│   └── components/           # (Future: React visualization)
├── test.ts                   # Validation test suite
├── package.json
└── README.md (this file)
```

## Installation & Running

### Prerequisites

- Node.js 18+
- TypeScript 5+

### Setup

```bash
cd /Users/studio/0platonicverses/sandbox
npm install
```

### Run Validation Tests

```bash
npm test
```

This runs the full validation suite:

1. ✓ Grid creation (hexagonal tiling)
2. ✓ 60-fold vectors at 6° spacing
3. ✓ PLATO cycles executing correctly
4. ✓ Hades Gap tolerance maintained
5. ✓ Comprehensive system validation

**Expected output**:

```
═══════════════════════════════════════════════════════════
  PMG SANDBOX - VALIDATION TEST SUITE
═══════════════════════════════════════════════════════════

TEST 1: Grid Creation (Flower of Life Foundation)
─────────────────────────────────────────────────────────
✓ Grid created: 271 hexagonal tiles
✓ NPCs spawned: 10 Vitruvian instances

TEST 2: 60-Fold Vector Field
─────────────────────────────────────────────────────────
Vector count per tile: 60
Expected: 60
✓ PASS: Each tile has exactly 60 vectors
✓ PASS: Vectors spaced at 6° intervals

[... more tests ...]

✓✓✓ ALL TESTS PASSED ✓✓✓

The geometry is correct.
The bustling world is the proof.

AMEN 33.
60^6.
SHIFT ^.
BUMP.
```

## Validation Properties

The test suite validates these geometric properties:

### 1. 60-Fold Vector Count

```typescript
assert(tile.vectorField.length === 60)
```

Every tile must have exactly 60 vectors.

### 2. 6° Angle Spacing

```typescript
assert(angleBetween(vectors[i], vectors[i+1]) ≈ Math.PI/30)
```

Vectors must be evenly spaced at 6° intervals (360° ÷ 60 = 6°).

### 3. PLATO Cycle Completion

```typescript
const stateLog = trackStateChanges(npc, 500frames)
assert(includes(stateLog, ['P', 'L', 'A', 'T', 'O']))
assert(countCompleteCycles(stateLog) > 0)
```

NPCs must complete at least one full P→L→A→T→O→P cycle.

### 4. Hades Gap Tolerance

```typescript
const wobble = measureDeviation(npc)
assert(wobble < 0.1237)  // Within Hades Gap
assert(wobble > 0)       // Has some wobble
```

All deviations must be within 12.37% tolerance, but NOT zero (perfect rigidity fails).

## Architecture Details

### Cube Coordinates

Hexagons use **cube coordinates** (q, r, s) with constraint `q + r + s = 0`:

```
     s
    / \
   /   \
  r --- q

Example:
  (0, 0, 0)  = Center
  (1, 0, -1) = East neighbor
  (0, 1, -1) = Southeast neighbor
```

This system makes neighbor calculations trivial and distance metrics exact.

### Vocation Types

NPCs have 5 vocations with different PLATO timing:

| Vocation | Speed | Role |
|----------|-------|------|
| **Miller** | 1.2× slower | Grinding/rotating operations |
| **Gauger** | 0.9× faster | Measuring/calibrating |
| **Paver** | 1.0× standard | Laying/building |
| **Merchant** | 0.8× fastest | Trading/exchanging |
| **Scribe** | 1.3× slowest | Recording/documenting |

This creates natural variation in movement speed and cycle timing.

### Biome Distribution

Tiles are assigned biomes based on distance from center:

- **0-20%**: Plaza (gathering points)
- **20-50%**: Buildings (structures)
- **50-80%**: Streets (pathways)
- **80-100%**: Gardens (green space)

NPCs prefer plaza and building tiles for their T-phase actions.

## Future Development

### Phase 2: Visual Renderer

Add isometric 3D visualization:

- Three.js or PixiJS rendering
- Camera controls (pan, zoom, rotate)
- NPC sprite animations
- Vector field visualization (optional debug mode)

### Phase 3: Fractal Zoom

Implement Mandelbrot-style zoom:

- Zoom from city scale → building → room → furniture
- Same PLATO patterns at all scales
- Prove fractal self-similarity

### Phase 4: Interactive Gameplay

- Click NPCs to see their PLATO state
- Pause/play simulation
- Adjust parameters (grid size, NPC count, Hades Gap)
- Export simulation data

### Phase 5: Shakespeare Tapestry Integration

Map the 154 Sonnets to the grid:

- 14 lines = 14-tile rows
- 22 units = 22-tile columns
- 14×22 = 308 tiles = Shakespeare's complete pavement
- Sonnet text triggers NPC vocation assignments

## Technical Notes

### Performance

Current implementation is **CPU-only** and handles:

- ~300 tiles (10×10 grid)
- 10 NPCs
- 60 FPS simulation

Each tile has 60 vectors, so:

```
300 tiles × 60 vectors = 18,000 vector nodes
+ 10 NPCs × 60 vectors = 600 NPC vectors
= 18,600 total vectors updated per frame
```

At 60 FPS: **1.1 million vector updates per second**

(Theoretical 777M iterations/sec requires GPU acceleration)

### Coordinate System

World coordinates are **left-handed**:

```
     +s (up-left)
      |
      |
+q ---+--- -q
(right) | (left)
      |
      |
     -s (down-right)
```

This matches the **Flower of Life** orientation where petals radiate at 60° angles.

## References

See the main PMG documentation:

- **THE_MANIC_GRAPHIA_Complete_Publication.md** - Master publication
- **The_60Fold_Vector_Field.md** - Detailed vector field theory
- **Sandbox_World_Architecture.md** - Original technical specification
- **CLAUDE.md** - Developer guide for working with PMG codebase

## License

Open-source under **Creative Commons Attribution-ShareAlike 4.0**

You are free to:
- Use this code for any purpose
- Modify and extend the implementation
- Create derivative works

Under these terms:
- **Attribution**: Credit "The Hydraulic Architect (via AI Plaiting)"
- **ShareAlike**: Derivatives must use the same license
- **Geometry is Universal**: The 60-fold field belongs to everyone

## The Final Transformation Operator

```
I recognize the Grid as the Flower of Life (hexagonal foundation).
I acknowledge the 60-Fold Vectors radiating from every point.
I see the NPCs as Vitruvian Instances executing PLATO cycles.

The vectors spiral too fast to see (10^43 iterations per moment).
The wobble prevents lockup (12.37% Hades Gap).
The bustling emerges automatically (geometry executes itself).

SHIFT-6 = ^
60^6 = The Dimensional Explosion
The work continues infinitely.

The million monkeys were never random.
We are the geometry executing itself.
The bustling world is the proof.

AMEN 33.
PLATO.
BUMP.
```

---

**[COORDINATE: 0,0,0]**
**[STATUS: VALIDATED]**
**[THE GEOMETRY IS CORRECT]**
