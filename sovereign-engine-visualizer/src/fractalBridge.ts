/**
 * fractalBridge.ts
 * 
 * Mathematical kernel for the generational cascade.
 * 
 * Core identity:
 *   g_n = √(n(n+1))  ≈  n + 1/2 - 1/(8n) + O(n⁻³)
 * 
 * This geometric mean is the multiplicative midpoint between
 * consecutive integers. It drives the three-phase lifecycle:
 *   Parent (n) → Bridge (g_n) → Child (n+1)
 */

/** Geometric mean of n and n+1 — the transition threshold */
export function geometricBridge(n: number): number {
    return Math.sqrt(n * (n + 1));
}

/** 
 * Bridge offset: how far g_n sits below the arithmetic mean (n + 0.5).
 * δ_n ≈ 1/(8n) for large n.
 * This is the "entropy residual" — it decreases as scale increases,
 * encoding natural stabilization of transitions.
 */
export function bridgeDrift(n: number): number {
    return (n + 0.5) - geometricBridge(n);
}

/**
 * Pell identity verification.
 * 
 * The sequence satisfies the exact identity:
 *   (2n+1)² - 4·n(n+1) = 1
 * 
 * This is a Pell-type equation, which explains why the geometric
 * mean sits so close to the half-integer: the sequence traces
 * points on the hyperbola x² - y² = 1/4.
 * 
 * Returns 1 for all valid integers (mathematical invariant).
 */
export function pellIdentity(n: number): number {
    return (2 * n + 1) ** 2 - 4 * n * (n + 1);
    // Always returns 1
}

/**
 * Gap between the next perfect square and g_n².
 * 
 *   (n+1)² - g_n² = (n+1)² - n(n+1) = n+1
 * 
 * The bridge's square is always exactly (n+1) below
 * the next perfect square. This regularity is what makes
 * the animation feel organic.
 */
export function squareGap(n: number): number {
    return (n + 1) ** 2 - n * (n + 1);
    // Always returns n+1
}

/**
 * Three-phase state machine for zoom-space navigation.
 * 
 * Given a continuous zoom coordinate z and a parent node index n:
 *   - 'parent':  z < g_n        (stable structure)
 *   - 'bridge':  g_n ≤ z < n+1  (transition / emergence)
 *   - 'child':   z ≥ n+1        (next generation stable)
 * 
 * In practice, the bridge phase is split into:
 *   - approach:   n → ~n+0.3     (oscillation begins)
 *   - pulse:      ~n+0.3 → g_n   (distortion / glow peak)
 *   - emergence:  g_n → n+1      (new node appears)
 */
export type NodePhase = 'parent' | 'bridge' | 'child';

export function nodeState(z: number, n: number): NodePhase {
    const bridge = geometricBridge(n);
    if (z < bridge) return 'parent';
    if (z < n + 1) return 'bridge';
    return 'child';
}

/**
 * Compute the transition frame within an animation cycle.
 * For a cycle of `totalFrames` frames spanning one integer step (n → n+1),
 * the bridge threshold falls at:
 *   frame = totalFrames × (g_n - n)
 * 
 * Example: n=93, totalFrames=120 → transition at frame ~59.8
 */
export function transitionFrame(n: number, totalFrames: number = 120): number {
    const g = geometricBridge(n);
    return totalFrames * (g - n);
}

/**
 * Generate the first `count` steps of the generational cascade
 * starting from parent node `startN`.
 * 
 * Returns array of { parent, child, bridge, drift } objects.
 */
export interface CascadeStep {
    k: number;        // generation index
    parent: number;   // n_k
    child: number;    // n_k + 1
    bridge: number;   // √(n_k × (n_k+1))
    drift: number;    // (n_k + 0.5) - bridge  ≈ 1/(8n_k)
}

export function generateCascade(startN: number, count: number): CascadeStep[] {
    const steps: CascadeStep[] = [];
    for (let k = 0; k < count; k++) {
        const n = startN + k;
        steps.push({
            k,
            parent: n,
            child: n + 1,
            bridge: geometricBridge(n),
            drift: bridgeDrift(n),
        });
    }
    return steps;
}

/**
 * Map a linear zoom value (0.0 → 1.0) to the cascade coordinate space.
 * 
 * zoom=0.0 → seed center (n=startN)
 * zoom=0.5 → bridge threshold (g_startN)
 * zoom=1.0 → child/fruit (n=startN+1)
 * 
 * The mapping is slightly nonlinear because g_n < n+0.5
 * (geometric mean < arithmetic mean). This gives the transition
 * an organic, multiplicative feel rather than a mechanical linear one.
 */
export function zoomToCascade(zoom: number, startN: number = 93): {
    z: number;
    phase: NodePhase;
    progress: number; // 0-1 within current phase
} {
    // Map 0-1 to the n → n+1 range
    const z = startN + zoom;
    const bridge = geometricBridge(startN);
    const phase = nodeState(z, startN);

    let progress: number;
    switch (phase) {
        case 'parent':
            // 0 at n, 1 at bridge
            progress = (z - startN) / (bridge - startN);
            break;
        case 'bridge':
            // 0 at bridge, 1 at n+1
            progress = (z - bridge) / (startN + 1 - bridge);
            break;
        case 'child':
            progress = 1;
            break;
    }

    return { z, phase, progress: Math.max(0, Math.min(1, progress)) };
}
