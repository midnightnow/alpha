/**
 * THE SEVEN CONSTANTS OF RADICAL RESONANCE
 * These are the immutable values that define the Phase II Artifact.
 * As defined in Seven_Constants.md
 */
export declare const HABITABILITY_CONSTANT: number;
export declare const PACKING_CONSTANT: number;
export declare const HEXAGONAL_LIMIT: number;
export declare const OVERPACK_DELTA: number;
export declare const LOG_MIRROR: number;
export declare const SHEAR_ANGLE_RAD: number;
export declare const SHEAR_ANGLE_DEG: number;
export declare const ROOT_42: number;
export declare const ROOT_51: number;
export declare const ROOT_60: number;
export declare const BEAT_FREQUENCY: number;
export declare const BIQUADRATIC_COEFF_A = 1;
export declare const BIQUADRATIC_COEFF_B = -186;
export declare const BIQUADRATIC_COEFF_C = 81;
/**
 * ADDITIONAL SYSTEM CONSTANTS
 * From Sandbox and App implementations
 */
export declare const HADES_GAP = 0.1237;
export declare const HAMMER_CONSTANT = 0.00014;
export declare const TRIADIC_BASE_FREQ = 66;
/**
 * RESONANCE LADDER
 * Steps of the geometric progression
 */
export declare const LADDER_STEPS: readonly [{
    readonly step: 0;
    readonly radicand: 42;
    readonly vertices: 42;
    readonly name: "The Resonant Sphere";
    readonly label: "BASE";
    readonly desc: "Pure Potential";
}, {
    readonly step: 1;
    readonly radicand: 51;
    readonly vertices: 93;
    readonly name: "The Interference Solid";
    readonly label: "INTERFERENCE";
    readonly desc: "Triadic Tension";
}, {
    readonly step: 2;
    readonly radicand: 60;
    readonly vertices: 153;
    readonly name: "The Resolution Solid";
    readonly label: "RESOLUTION";
    readonly desc: "Harmonic Stabilizer";
}, {
    readonly step: 3;
    readonly radicand: 69;
    readonly vertices: 222;
    readonly name: "The Chaotic Solid";
    readonly label: "CHAOS";
    readonly desc: "Entropy Bloom";
}];
/**
 * PHONETIC MAPPING
 * For Mathman Genesis Naming Ceremony
 */
export declare const VOICES: {
    readonly Silence: "0";
    readonly Density: "p";
    readonly Fracture: "s";
    readonly Gesture: "l";
    readonly Heartbeat: "m";
    readonly Warning: "z";
    readonly Chorus: "a";
};
