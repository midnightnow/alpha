// ============================================================================
// SOVEREIGN ENGINE: THERMODYNAMIC REALITY (v1.0.0)
// ============================================================================
// This module bridges the static geometry with the differential of Grace.
// ============================================================================

export const LUNAR_MERCY_HZ = 12.368;

/**
 * 12.37 is the Metric of Mercy - the refractive lubricant ensuring the 
 * icosidodecahedron maintains its internal volume during the torsion twist.
 */
export const HADES_GAP = 1 - (12 / 13.6937); // ~0.12368... (dx)

/**
 * Grace (G) is the accumulated integral of Mercy over the precessional 
 * 25,920-year Great Year, regulating the 540-degree torsion.
 */
export const GREAT_YEAR_CYCLES = 25920;

export const PRECESSIONAL_VELOCITY = (2 * Math.PI) / GREAT_YEAR_CYCLES;

export const MAX_MOBIUS_TORSION_DEG = 540;
export const MAX_MOBIUS_TORSION_RAD = MAX_MOBIUS_TORSION_DEG * (Math.PI / 180);

/**
 * Computes the instantaneous Grace Integral value and the corresponding torsion
 * modifier given the current timeframe in the cycle.
 * @param t Active simulation time component
 * @returns Built state for visual/UI bindings
 */
export function computeGraceIntegral(t: number) {
    // 1. Accumulate dx
    const accumulatedGrace = t * HADES_GAP;

    // 2. Map position in the Mod 24 / Great Year spiral.
    const cyclePosition = (t * LUNAR_MERCY_HZ) % GREAT_YEAR_CYCLES;

    // 3. Compute rotation offset using precessional velocity
    const shimmerVelocity = (cyclePosition * PRECESSIONAL_VELOCITY);

    return {
        accumulatedGrace,
        cyclePosition,
        shimmerVelocity,
        completionRatio: cyclePosition / GREAT_YEAR_CYCLES
    };
}
