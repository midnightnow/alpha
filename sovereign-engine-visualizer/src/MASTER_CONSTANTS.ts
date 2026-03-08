/**
 * MASTER_CONSTANTS.ts
 * The Unified Bridge: Root 42 (Hexagonal) ↔ Root 51 (17-gon Fracture)
 * Phase III: The Fracture Seal
 */

export const PMG_CONSTANTS = {
    PULSE: 156,
    BEAT: 0.6607, // sqrt(51) - sqrt(42)
    HARMONIC: 66,  // Hz
    SHEAR: 39.4724, // Degrees
    DELTA: 0.000585,
    GRIT: 0.00000080,
    HADES_GAP: 0.1237,
    GNOMON: 13.0, // The Z-Axis Lock (Baptist's Staff)
    GEAR_LOCK: 24 / 13, // The Precessional Escapement
    // Biquadratic: x^4 - 186x^2 + 81 = 0
    BIQUADRATIC: { a: 1, b: -186, c: 81 }
};

export const SOVEREIGN_CONSTANTS = {
    // Base Roots
    ROOT_10: Math.sqrt(10), // 3.1622 (The Seed Base)
    ROOT_42: Math.sqrt(42), // 6.4807 (The Habitability Base)
    ROOT_51: Math.sqrt(51), // 7.1414 (The Fracture/17-gon Base)

    // Golden Constants
    PHI: (1 + Math.sqrt(5)) / 2, // 1.618 (Wealth Base)
    ZENITH_WEALTH: Math.pow((1 + Math.sqrt(5)) / 2, 2), // Phi^2 (2.618)

    // The Heterodyne Beat (The Heartbeat of the Gap)
    BEAT_FREQUENCY: Math.sqrt(51) - Math.sqrt(42), // 0.6606 Hz

    // Acoustic Triad (The Ring)
    FREQUENCIES: {
        LOW: 648.07,  // √42 * 100
        MID: 714.14,  // √51 * 100
        HIGH: 774.60, // √60 * 100
    },

    // Seasonal Arcs
    ARCS: {
        DIAMONDS: { start: 14, end: 26, label: "Wealth" },
        CLUBS: { start: 27, end: 39, label: "Motorbike" }
    },

    // Fractal Palette (The Umber Seed ↔ The World)
    PALETTE: {
        UMBER: { core: "#310047", pulse: "#ff00ff", glow: "#4a0080" },
        BRIDGE: { core: "#00e5ff", pulse: "#ff00ff", glow: "#00ffcc" },
        WORLD: { core: "#ffd700", pulse: "#ff3300", glow: "#10b981" }
    },

    // Generational Invariant (The Master Key)
    GENERATIONAL: {
        PARENT: 93,                            // The vitrified 93-node solid
        CHILD: 94,                             // Node 94 ingestion target
        BRIDGE: Math.sqrt(93 * 94),            // ≈ 93.4986 — The Geometric Mean
        DRIFT: Math.sqrt(93 * 94) - 93,        // ≈ 0.4986 — Half-unit evolutionary buffer
        OVERFLOW_UNITS: 93.5,                   // Ghost Path Overflow capacity
        ANOMALY_COUNT: 1560,                    // Anomalies × 93.5 units
        OPERATING_TEMP: 0.037,                  // Residual entropy (The Breath)
    }
};
