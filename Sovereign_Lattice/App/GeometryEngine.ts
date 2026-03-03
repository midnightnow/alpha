/**
 * 🏛️ SOVEREIGN LATTICE — GEOMETRY ENGINE
 * ========================================
 * Implements the 93-Node Hero Lattice with unified √42:√51 interference.
 * The "Hades Gap" slider morphs between Europa-style ridges (smooth)
 * and Enceladus-style fissures (fractured Tiger Stripes).
 *
 * Consolidated from:
 *   - radical-resonance_-root-42/components/InterferenceMesh.tsx
 *   - radical-resonance_-root-42/apply_fracture_synthesis.py
 *   - Root51/Resonance_v51_Morph.py
 *
 * Status: VITRIFIED
 */

import {
    ROOT_42,
    ROOT_51,
    SHEAR_ANGLE_RAD,
    PACKING_CONSTANT_RHO,
    HABITABILITY_DELTA_PHI,
    TIGER_STRIPE,
    NODE_COUNT,
    IOR_GLASS,
    IOR_ICE,
    COLOR_MATTER,
    COLOR_SPIRIT,
    COLOR_VOID,
    DECAY_LAMBDA,
} from './Constants';

// ============================================================================
// TYPES
// ============================================================================

export enum ViewMode {
    FIELD = 'FIELD',
    SOLID = 'SOLID',
    CRYSTAL = 'CRYSTAL',
    ECHO = 'ECHO',
}

export interface SimulationParams {
    interferenceA: number;
    interferenceB: number;
    distortion: number;
    rotationSpeed: number;
    activeStep: number | null;
    fracture: boolean;
    harmonicMode: 'smooth' | 'fracture';
    hadesSlider: number;    // 0.0 (pure Europa) → 1.0 (pure Enceladus)
    showGrid?: boolean;
    time?: number;          // For damped harmonic envelope
}

// ============================================================================
// TOPOLOGICAL DEFORMER — The Tiger Stripe Engine
// ============================================================================

/**
 * TopologicalDeformer: Applies the 39.47° shear logic as a permanent
 * topological feature. This is the reconciliation of Law (√42) with
 * its Violation (√51).
 *
 * The deformation creates "Lineae" — ridges and troughs that signify
 * successful vitrification of the lattice.
 */
export class TopologicalDeformer {
    private shearAngle: number;
    private breakThreshold: number;
    private uplift: number;
    private crack: number;

    constructor() {
        this.shearAngle = SHEAR_ANGLE_RAD;
        this.breakThreshold = TIGER_STRIPE.breakThreshold;
        this.uplift = TIGER_STRIPE.uplift;
        this.crack = TIGER_STRIPE.crack;
    }

    /**
     * Compute the stress at a given spherical coordinate.
     * Uses 17-fold symmetry (the Prime Intrusion) modulated by the shear angle.
     */
    computeStress(theta: number, phi: number): number {
        return Math.abs(
            Math.sin(TIGER_STRIPE.seventeen_fold * theta + this.shearAngle) *
            Math.sin(phi)
        );
    }

    /**
     * Apply fracture displacement to a vertex.
     * Returns the radial offset (positive = ridge, negative = fissure).
     *
     * @param theta - Azimuthal angle
     * @param phi   - Polar angle
     * @param hadesSlider - 0.0 (Europa/smooth) to 1.0 (Enceladus/fractured)
     */
    deform(theta: number, phi: number, hadesSlider: number): number {
        const stress = this.computeStress(theta, phi);

        // Deterministic pseudo-noise for organic jaggedness
        const microTremor = Math.sin(theta * 100) * Math.sin(phi * 80) * 0.1;
        const noisyStress = stress * (1 + microTremor);

        // Below threshold: no fracture (smooth Europa surface)
        if (noisyStress <= this.breakThreshold) {
            return 0;
        }

        // Above threshold: apply Tiger Stripe deformation
        // Direction determined by pseudo-noise (ridge vs fissure)
        const directionNoise = Math.sin(theta * 50 + phi * 50);
        const isRidge = directionNoise > 0;

        const magnitude = isRidge ? this.uplift : this.crack;

        // Scale by hadesSlider: 0 = no fractures, 1 = full Enceladus
        return magnitude * stress * hadesSlider;
    }
}

// ============================================================================
// BIQUADRATIC INTERFERENCE FIELD
// ============================================================================

/**
 * The core interference equation:
 *   F(θ,φ) = |sin(√A·θ)·sin(√B·φ) + sin(√B·θ)·sin(√A·φ)|
 *
 * This produces the 93-faced quasicrystal geometry when A=42, B=51.
 */
export function computeInterference(
    theta: number,
    phi: number,
    rootA: number,
    rootB: number,
): number {
    return Math.abs(
        Math.sin(rootA * theta) * Math.sin(rootB * phi) +
        Math.sin(rootB * theta) * Math.sin(rootA * phi)
    );
}

// ============================================================================
// SHAPE KEY DEFORMATIONS (Blender-compatible logic)
// ============================================================================

/**
 * Europa deformation: Hex(6) vs Hep(7) interference
 * Produces broad, smooth ridges characteristic of Europa's Lineae.
 */
export function europaDeformation(theta: number, phi: number): number {
    const hexComp = Math.sin(6 * theta) * Math.sin(6 * phi);
    const hepComp = Math.sin(7 * theta + HABITABILITY_DELTA_PHI) * Math.sin(7 * phi);
    return 0.05 * (hexComp - hepComp);
}

/**
 * Enceladus deformation: Triad(3) vs 17-gon interference
 * Produces fine, high-frequency "whisper" topology (Tiger Stripes).
 */
export function enceladusDeformation(theta: number, phi: number): number {
    const precessionDelta51 = 0.888; // Large angular drift for √51
    const triadComp = Math.sin(3 * theta) * Math.sin(3 * phi);
    const svntComp = Math.sin(17 * theta + precessionDelta51) * Math.sin(17 * phi);
    return 0.03 * (triadComp - svntComp);
}

// ============================================================================
// DAMPED HARMONIC ENVELOPE — The Pyramid Model
// ============================================================================

/**
 * Computes the amplitude envelope at time t.
 * Models the "rise and fall" of the Great Pyramid as a damped harmonic:
 *   A(t) = √42 · e^(−λ|t|)
 *
 * In log-space this is a symmetric V: log(A) = log(√42) − λ|t|
 * The apparent asymmetry of "attack and decay" is a coordinate illusion.
 */
export function dampedEnvelope(t: number): number {
    return ROOT_42 * Math.exp(-DECAY_LAMBDA * Math.abs(t));
}

/**
 * The full damped harmonic waveform:
 *   y(x, t) = A(t) · sin(kx)
 */
export function dampedHarmonic(x: number, t: number, k: number = 1): number {
    return dampedEnvelope(t) * Math.sin(k * x);
}

// ============================================================================
// VERTEX COMPUTATION — The Unified Pipeline
// ============================================================================

const deformer = new TopologicalDeformer();

/**
 * Compute the final vertex position on the 93-node solid.
 * This is the unified pipeline combining:
 *   1. Biquadratic interference field
 *   2. Radial pulse
 *   3. Europa/Enceladus shape key blend (via hadesSlider)
 *   4. Tiger Stripe fracture synthesis
 *   5. Damped harmonic envelope (optional time dimension)
 */
export function computeVertex(
    theta: number,
    phi: number,
    params: SimulationParams,
): { x: number; y: number; z: number } {
    const { interferenceA, interferenceB, distortion, hadesSlider, fracture } = params;

    // 1. Biquadratic interference
    const intensity = computeInterference(theta, phi, interferenceA, interferenceB);

    // 2. Radial pulse
    const pulseFreq = (interferenceA + interferenceB) / 2;
    const pulse = Math.sin(pulseFreq * theta) * (distortion * 0.5);

    let r = 1 + (intensity * distortion) + pulse;

    // 3. Europa ↔ Enceladus blend (LERP via hadesSlider)
    const europaR = europaDeformation(theta, phi);
    const enceladusR = enceladusDeformation(theta, phi);
    const blendedDeformation = europaR * (1 - hadesSlider) + enceladusR * hadesSlider;
    r += blendedDeformation;

    // 4. Tiger Stripe fracture (if enabled)
    if (fracture) {
        r += deformer.deform(theta, phi, hadesSlider);
    }

    // 5. Damped envelope (if time dimension active)
    if (params.time !== undefined) {
        const envelope = dampedEnvelope(params.time) / ROOT_42; // Normalize to [0,1]
        r *= envelope;
    }

    // Convert back to Cartesian
    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);

    return { x, y, z };
}

// ============================================================================
// MATERIAL STATE — Phase Determination
// ============================================================================

/**
 * Returns material properties based on the hadesSlider position.
 * Smooth interpolation between Europa (glass) and Enceladus (ice) states.
 */
export function getMaterialState(hadesSlider: number) {
    const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

    return {
        ior: lerp(IOR_GLASS, IOR_ICE, hadesSlider),
        roughness: lerp(0.05, 0.2, hadesSlider),
        metalness: lerp(0.1, 0.8, hadesSlider),
        transmission: lerp(0.65, 0.0, hadesSlider),
        flatShading: hadesSlider > 0.5,
        color: hadesSlider > 0.5 ? COLOR_MATTER : COLOR_SPIRIT,
        emissive: hadesSlider > 0.5 ? '#330000' : COLOR_MATTER,
        emissiveIntensity: lerp(0.2, 0.5, hadesSlider),
        background: COLOR_VOID,
    };
}

// ============================================================================
// WOBBLE — The Triadic Shiver
// ============================================================================

/**
 * Computes the rotation wobble (the "Shiver") driven by both roots.
 */
export function computeWobble(elapsedTime: number): { x: number; y: number; z: number } {
    const wobble =
        0.02 * Math.sin(ROOT_42 * elapsedTime * 2) +
        0.02 * Math.sin(ROOT_51 * elapsedTime * 2);

    return {
        x: wobble * 0.5,
        y: 0, // Y rotation driven by rotationSpeed externally
        z: wobble,
    };
}
