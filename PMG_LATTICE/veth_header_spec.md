# 🏛️ .VETH FILE FORMAT SPECIFICATION: THE STRUCTURAL CROSS

**Status:** Canonical Spec | **System:** The Sovereign Lattice | **Version:** 1.0 (Vitrified)

The `.veth` (Vitrified Essential Tensed Harmonic) file format is the standard for serializing geometric data within the PMG Lattice. The file header is built upon the **24/37/43/73 Structural Cross**, ensuring that any data point is anchored in the absolute metrics of the **Hero 93**.

## 1. The Header Cross (The Core Pillars)

The first 64 bytes of a `.veth` file are dedicated to the **Identity Cross**. 

| Register | Offset | Axis | Geometric Identity | Role |
| :--- | :--- | :--- | :--- | :--- |
| `0x00` | 0-15 | **Time (24)** | The Axial Chamber | **The Measure.** Timestamps, frame modulus (mod 24), and vertebrae alignment. |
| `0x10` | 16-31 | **Light (37)** | The Prime Source | **The Truth.** 37°C body temp resonance, human signature, and the Ample Candle frequency. |
| `0x20` | 32-47 | **Offset (43)** | The H-Void Guard | **The Stitch.** Tension constant ($H = 43-42$), the 1-unit pinhole gap, and guard bits. |
| `0x30` | 48-63 | **Mirror (73)** | The Palindrome | **The Seal.** Reflection of Light (37), 2701 Trinity check, and 0-hysteresis verification. |

## 2. The H-Constant & Vacuum Tension
Every `.veth` record must maintain a structural vacuum of **-1/12**.
*   **H-Constant:** The displacement between the **Savage 42** and the **Offset Guard 43**. 
*   **Verification:** If $43 - 42 \neq 1$, the record is considered "Russet" (corrupt) and will be shaven by the auto-repair tautener.

## 3. The 156-Tick Payload
Following the header, the payload consists of 156 discrete data nodes (The Alphabet). 
*   Each node must be **Integers-Only** for the "Stitch Holes" (coordinates).
*   Fractional values are only permitted for **Physical Signatures** (EM/GR/QM) which represent the "inter-stitch" interference pattern.

## 4. Stability Condition
A `.veth` file is only "Taut" if:
$$ \sum_{n=1}^{156} \text{Tension}(n) \times (-1/12) = \text{Anchor}(24/37) $$
This ensures the file itself acts as a **Camera Obscura**, projecting only the essential geometry and filtering out over-sampled noise.

The Header is Secured. The Record is Locked.
