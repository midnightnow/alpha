# The Rotational Key: Compressing Reality into 3x4 Logic

This document extends the `MUNDI_GEOMETRY_ARCHITECTURE.md` concept by defining the data structure for the "Rotational Key."

## 1. The Core Shift: Voxel to Vector
Standard engines store lists of coordinates. The Mundi Engine stores **Recursive Seeds**.
We replace `List<Block> blocks` with `RotationalKey key`.

## 2. The Key Structure: `[Base:Zodiac:Ratio:Depth]`
A massive structure is defined by a single radial string, e.g., `[60:12:3.4.5:R6]`.

### Components:
*   **Base (60):** The System (Sexagesimal). High composite number (1,2,3,4,5,6,10,12,15,20,30,60). Prevents floating point errors.
*   **Zodiac (12):** The Partition. 3 (Space/Columns) x 4 (Density/Worlds). Represents the angular "sectors" of the build.
*   **Ratio (3.4.5):** The "Flavor" or Geometry. 
    *   `3.4.5` = The "Perfect" Pythagorean Harmonic (Organic/Balanced).
    *   `1.1.2` = Binary/Cubic (Artificial/Boxy).
    *   `1.618` = Golden Spiral (Exponential/Fibonacci).
*   **Depth (Rn):** The Recursion Level. How many times the triangle subdivides.

## 3. The Operation: Phase Shifting
"Mining" or "Crafting" is re-defined as **Re-tuning**.
*   **Action:** Apply a "4-Logic" (Density) shift to a "3-Logic" (Growth) area.
*   **Result:** The local harmonic frequency shifts from "Tree" to "Wood."
*   **Compute Cost:** Extremely Low. The math doesn't change, only the *rotational phase*.

## 4. The Encode Test: A 4-Pillared Temple
### The Goal
Encode a simple temple (4 pillars, 1 roof) into a single numeric string.

### The Standard Way (Voxel)
*   Pillar 1: (0,0,0) to (0,10,0) -> 10 blocks
*   Pillar 2: (10,0,0) to (10,10,0) -> 10 blocks
*   ...
*   Roof: (0,10,0) to (10,10,10) -> 100 blocks
*   **Total Data:** ~140 coordinate sets.

### The Mundi Way (Rotational Key)
*   **Origin:** Center Point.
*   **Symmetry:** 4-fold (Square). Frequency = 90 degrees ($360/4$).
*   **Ratio:** 3:4 (Height is 1.33x Width).
*   **Component 1 (Pillars):** `[4x:Vertical:R1]` (4x symmetry, Vertical extrusion, Recursion 1).
*   **Component 2 (Roof):** `[1x:Horizontal:R2]` (Connects the 4 points).

**The Key:** `[60:4:3.4.5:R2]`
*   *Interpretation:* "In Base-60, divide space into 4 sectors (Zodiac 4). Apply the 3-4-5 harmonic. Iterate twice."
*   The system "unfolds" the temple from this single line.

---
*Generated: 2026-01-12 | Context: AI Vet Book Volume 3 / Mundi Vision*
