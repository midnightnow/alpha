/**
 * THE SEVEN CONSTANTS OF RADICAL RESONANCE
 * These are the immutable values that define the Phase II Artifact.
 * As defined in Seven_Constants.md
 */

// 1. Habitability Constant (ΔΦ)
export const HABITABILITY_CONSTANT = 2 * Math.PI * (Math.sqrt(42) / 6 - 1); // ≈ 0.0801 rad/beat

// 2. Packing Constant (ρ) - Governs density limit
export const PACKING_CONSTANT = Math.sqrt(14 / 17); // ≈ 0.907485

// 3. Overpack Delta (δ) - The force that fractures the solid
export const HEXAGONAL_LIMIT = Math.PI / Math.sqrt(12); // η_hex ≈ 0.906899
export const OVERPACK_DELTA = PACKING_CONSTANT - HEXAGONAL_LIMIT; // ≈ 0.000585

// 4. Log Mirror (Λ)
export const LOG_MIRROR = Math.log10(PACKING_CONSTANT); // ≈ -0.04216

// 5. Shear Angle (θ) - The angle of fracture
export const SHEAR_ANGLE_RAD = Math.atan(14 / 17); // In radians
export const SHEAR_ANGLE_DEG = SHEAR_ANGLE_RAD * (180 / Math.PI); // ≈ 39.425°

// 6. Beat Frequency (β) - The "Hum"
export const ROOT_42 = Math.sqrt(42);
export const ROOT_51 = Math.sqrt(51);
export const ROOT_60 = Math.sqrt(60);
export const BEAT_FREQUENCY = ROOT_51 - ROOT_42; // ≈ 0.6607 Hz

// 7. Minimal Polynomial (Biquadratic Field)
// P(x) = x^4 - 186x^2 + 81
export const BIQUADRATIC_COEFF_A = 1;
export const BIQUADRATIC_COEFF_B = -186;
export const BIQUADRATIC_COEFF_C = 81;


/**
 * ADDITIONAL SYSTEM CONSTANTS
 * From Sandbox and App implementations
 */

// Hades Gap (Ψ) - The "slop" or jitter tolerance (12.37%)
export const HADES_GAP = 0.1237;

// Hammer Constant (Xi) - Cumulative drift threshold
export const HAMMER_CONSTANT = 0.00014;

// Triadic Base Frequency (Hz)
export const TRIADIC_BASE_FREQ = 66;

/**
 * RESONANCE LADDER
 * Steps of the geometric progression
 */
export const LADDER_STEPS = [
    { step: 0, radicand: 42, vertices: 42, name: "The Resonant Sphere", label: "BASE", desc: "Pure Potential" },
    { step: 1, radicand: 51, vertices: 93, name: "The Interference Solid", label: "INTERFERENCE", desc: "Triadic Tension" },
    { step: 2, radicand: 60, vertices: 153, name: "The Resolution Solid", label: "RESOLUTION", desc: "Harmonic Stabilizer" },
    { step: 3, radicand: 69, vertices: 222, name: "The Chaotic Solid", label: "CHAOS", desc: "Entropy Bloom" },
] as const;

/**
 * PHONETIC MAPPING
 * For Mathman Genesis Naming Ceremony
 */
export const VOICES = {
    Silence: "0",
    Density: "p",
    Fracture: "s",
    Gesture: "l",
    Heartbeat: "m",
    Warning: "z",
    Chorus: "a"
} as const;
