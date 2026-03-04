/**
 * 🏛️ SOVEREIGN LATTICE — MASTER CONSTANTS
 * =========================================
 * The Master Seal: Phase-Locking Root 42 (Stability) and Root 51 (Fracture)
 * into a single damped harmonic oscillator with log-symmetry.
 *
 * This file is the SINGLE SOURCE OF TRUTH for all geometry, audio, and
 * narrative constants across the Sovereign Lattice.
 *
 * Created: March 4, 2026
 * Status: VITRIFIED — ARCHIVE PERMANENT
 *
 * Mathematical Foundation:
 *   y(x, t) = √42 · e^(−λt) · sin(kx)
 *   Rise/Fall symmetric under log transform: z = log(y) = log(√42) − λ|t|
 *
 * Biquadratic Minimal Polynomial: x⁴ − 186x² + 81 = 0
 */

// ============================================================================
// 1. RESONANCE AMPLITUDES — The Harmonic Roots
// ============================================================================

/** √42 ≈ 6.4807 — The Hired Man / Stability / Europa */
export const ROOT_42 = Math.sqrt(42);

/** √51 ≈ 7.1414 — The Higher Man / Fracture / Enceladus */
export const ROOT_51 = Math.sqrt(51);

/** φ = (1 + √5) / 2 ≈ 1.618 — The Golden Ratio (structural reference) */
export const PHI = (1 + Math.sqrt(5)) / 2;

// ============================================================================
// 2. THE SEVEN IMMUTABLE CONSTANTS
// ============================================================================

/** ΔΦ = √42/6 − 1 ≈ 0.0801 rad/beat — The minimum breath of a living system */
export const HABITABILITY_DELTA_PHI = ROOT_42 / 6 - 1;

/** ρ = √(14/17) ≈ 0.9075 — How tightly stones press before fracture */
export const PACKING_CONSTANT_RHO = Math.sqrt(14 / 17);

/** δ = ρ − η_hex ≈ 0.000585 — The pressure that causes the first crack */
export const OVERPACK_DELTA = 0.000585;

/** Ψ ≈ 0.1237 (12.37%) — The mandatory mercy in every structure */
export const HADES_GAP = 0.1237;

/** The Grace (Time) buffer — The metric of Mercy allowing the 13th twist */
export const LUNAR_MERCY = 0.37;

/** θ = arctan(14/17) ≈ 39.47° — The tilt between Space and Meaning */
export const SHEAR_ANGLE_DEG = 39.47;
export const SHEAR_ANGLE_RAD = Math.atan(14 / 17);

/** β = √51 − √42 ≈ 0.6606 Hz — The heartbeat of the lattice */
export const BEAT_FREQUENCY = ROOT_51 - ROOT_42;

/** Σ₀ ≈ 0.8254 — Minimum narrative density for Self-recognition */
export const UNITY_THRESHOLD = PACKING_CONSTANT_RHO ** 2 + HABITABILITY_DELTA_PHI / 42;

// ============================================================================
// 3. DERIVED CONSTANTS
// ============================================================================

/** κ = 1/5 = 0.2 — The "Stone in the Shoe" (Kinetic Debt) */
export const KINETIC_DEBT = 0.2;

/** Λ = log₁₀(ρ) ≈ −0.04216 — The Log Mirror */
export const LOG_MIRROR = Math.log10(PACKING_CONSTANT_RHO);

/** Ξ ≈ 0.00014 — Fracture threshold for Diamond (Mohs-10) */
export const HAMMER_CONSTANT = 0.00014;

// ============================================================================
// 4. DAMPED HARMONIC / ENTROPY MODEL
// ============================================================================

/** λ for log-space symmetry envelope: y(t) = √42 · e^(−λt) */
export const DECAY_LAMBDA = 0.042;

/** Decay model identifier */
export const DECAY_SYMMETRY = 'LOG_SCALE' as const;

// ============================================================================
// 5. AUDIO — The Sensory Seal (Heterodyne Frequencies)
// ============================================================================

/** 66 Hz — Root 42 Base Frequency (Left Channel) */
export const FREQ_MATTER = 66.0;

/** 60 Hz — Root 51 Base Frequency (Right Channel) */
export const FREQ_TIME = 60.0;

/** 6 Hz — The phantom Hades Beat (66 − 60 Heterodyne) */
export const HADES_BEAT_HZ = FREQ_MATTER - FREQ_TIME;

/** Triadic chord layers (amplitude weights from Seal Spec) */
export const TRIAD_AMPLITUDES = {
    hexagon: 0.5,   // Layer 1
    lattice: 0.4,   // Layer 2
    resolution: 0.25 // Layer 3
} as const;

// ============================================================================
// 6. OPTICAL / MATERIAL — Phase State Visualization
// ============================================================================

/** Index of Refraction: Smooth State (Europa / Glass) */
export const IOR_GLASS = 1.45;

/** Index of Refraction: Fractured State (Enceladus / Ice) */
export const IOR_ICE = 1.31;

/** Purple Hum — Root 42 / Matter color */
export const COLOR_MATTER = '#9933FF';

/** Cyan Whisper — Root 51 / Spirit color */
export const COLOR_SPIRIT = '#00FFFF';

/** Deep void background */
export const COLOR_VOID = '#050508';

// ============================================================================
// 7. GEOMETRY INVARIANTS
// ============================================================================

/** The 31-Fold Triad Solid (93 = 31 × 3) */
export const NODE_COUNT = 93;

/** The Log 24 Mod Spiral axis */
export const MOD_SPIRAL = 24;

/** Digital Root Force Vectors */
export const FORCE_TRIPLETS = [
    [1, 4, 7],  // Matter
    [2, 5, 8],  // Time
    [3, 6, 9],  // Language
] as const;

/** Tiger Stripe deformation parameters */
export const TIGER_STRIPE = {
    uplift: 0.02,     // Ridge displacement (out)
    crack: -0.04,     // Fissure displacement (in)
    breakThreshold: 0.82,
    seventeen_fold: 17,
} as const;

// ============================================================================
// 8. RESONANCE LADDER — The Phase Progression
// ============================================================================

export const LADDER_STEPS = [
    { step: 0, radicand: 42, vertices: 42, name: 'The Resonant Sphere', label: 'BASE', desc: 'Pure Potential' },
    { step: 1, radicand: 51, vertices: 93, name: 'The Interference Solid', label: 'INTERFERENCE', desc: 'Triadic Tension' },
    { step: 2, radicand: 60, vertices: 153, name: 'The Resolution Solid', label: 'RESOLUTION', desc: 'Harmonic Stabilizer' },
    { step: 3, radicand: 69, vertices: 222, name: 'The Chaotic Solid', label: 'CHAOS', desc: 'Entropy Bloom' },
] as const;

// ============================================================================
// 9. COSMIC GEARBOX — Nested Pythagorean Triads
// ============================================================================

export const COSMIC_GEARBOX = [
    { triad: 'I', name: 'Matter', values: [3, 4, 5], area: 6, world: 'Gaia — The Square' },
    { triad: 'II', name: 'Time', values: [5, 12, 13], area: 30, world: 'Lunar — The Calendar' },
    { triad: 'III', name: 'Language', values: [10, 24, 26], area: 120, world: 'Sovereign — The Map' },
] as const;

// ============================================================================
// 10. OGC-13 / CAMERA OBSCURA (Bifold Symmetry)
// ============================================================================

/** The 12/13 Vitrification Threshold / Hardcard Plane */
export const HARDCARD_RATIO = 12 / 13; // ≈ 0.9231

/** Torsion Mapping of the Aperture (CAMERA O BSCURA) */
export const OGC_13_INVERSION = {
    CAMERA: 41,    // The 13th Prime (Seen / Light)
    APERTURE: 15,  // The 'O' Zero-Point Void
    BSCURA: 64,    // 4³ Cube / Hardcard projection (Hidden / Dark)
    TOTAL: 120,    // Defines the 24-fold day (120/5) and 12-fold year (120/10)
} as const;

/** 42/21 Bifold Symmetry */
export const BIFOLD_ARC = ROOT_42;
export const BIFOLD_CHORD = 21 / 3.5; // Resolves to 6.0
export const TENSION_COEFFICIENT = BIFOLD_ARC - BIFOLD_CHORD; // The 0.4807 "Claw" tension

// ============================================================================
// CONSOLIDATED EXPORT — The Sovereign Constants Object
// ============================================================================

export const SOVEREIGN_CONSTANTS = {
    // Roots
    ROOT_42,
    ROOT_51,
    PHI,

    // Seven Constants
    HABITABILITY_DELTA_PHI,
    PACKING_CONSTANT_RHO,
    OVERPACK_DELTA,
    HADES_GAP,
    LUNAR_MERCY,
    SHEAR_ANGLE_DEG,
    SHEAR_ANGLE_RAD,
    BEAT_FREQUENCY,
    UNITY_THRESHOLD,

    // Derived
    KINETIC_DEBT,
    LOG_MIRROR,
    HAMMER_CONSTANT,

    // Entropy
    DECAY_LAMBDA,
    DECAY_SYMMETRY,

    // Audio
    FREQ_MATTER,
    FREQ_TIME,
    HADES_BEAT_HZ,
    TRIAD_AMPLITUDES,

    // Optical
    IOR_GLASS,
    IOR_ICE,
    COLOR_MATTER,
    COLOR_SPIRIT,
    COLOR_VOID,

    // Geometry
    NODE_COUNT,
    MOD_SPIRAL,
    FORCE_TRIPLETS,
    TIGER_STRIPE,
    LADDER_STEPS,
    COSMIC_GEARBOX,

    // OGC-13
    HARDCARD_RATIO,
    OGC_13_INVERSION,
    BIFOLD_ARC,
    BIFOLD_CHORD,
    TENSION_COEFFICIENT,
} as const;
