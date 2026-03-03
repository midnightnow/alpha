# @platonic/core

**The Unified Geometric Laws of the Principia Mathematica Geometrica (PMG)**

This library serves as the single source of truth for all constants, formulas, and "Laws" governing the Platonic Verses ecosystem.

## The Seven Constants

As defined in `Seven_Constants.md`:

1.  **Habitability Constant (ΔΦ)**: `0.0801 rad/beat`
2.  **Packing Constant (ρ)**: `√14/17` (≈ 0.907485)
3.  **Overpack Delta (δ)**: `0.000585`
4.  **Log Mirror (Λ)**: `-0.04216`
5.  **Shear Angle (θ)**: `39.425°`
6.  **Beat Frequency (β)**: `0.6607 Hz`
7.  **Minimal Polynomial**: `x^4 - 186x^2 + 81 = 0`

## System Constants

*   **Hades Gap (Ψ)**: `0.1237` (12.37% jitter tolerance)
*   **Hammer Constant (Xi)**: `0.00014` (Fracture threshold)

## Usage

```typescript
import { PACKING_CONSTANT, HADES_GAP } from '@platonic/core';

const simulate = (val: number) => {
  if (val > PACKING_CONSTANT + HADES_GAP) {
    throw new Error("Logic Lockup Detected");
  }
}
```
