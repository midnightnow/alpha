---
ID: DUAL_CLOCK_SPEC
DESCRIPTION: Specification for Dual-Clock quantization and sampling escapement.
STATUS: VITRIFIED
---

The Sovereign Engine operates on two synchronized clocks:

1. Registry Clock (Spatial Grid): 288 Ticks
   - Provides the discrete lattice for node assignment.
   - 288 = 12 * 24 (The Architecture of Time).

2. Pulse Clock (Temporal Trigger): 156 Ticks
   - The heartbeat that advances the DFA states.
   - 156 = 12 * 13 (The 13-Cycle Loop).

3. The Nyquist-Shannon Escapement (24:13 Ratio):
   - The ratio 288/156 simplifies to 24:13 (~1.846).
   - This ensures that the discrete Registry is sampled at or above its fundamental limit.
   - Prevents aliasing and spectral leakage from the √42 core.
   - Acts as the 'Gearbox' for the 10-24-26 manifold.

4. The Supercycle (3744 Ticks):
   - LCM(288, 156) = 3744.
   - Full synchronization is achieved every 13 Registry rotations and 24 Pulse cycles.

This escapement ensures zero drift and zero hysteresis.
