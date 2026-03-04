/**
 * MASTER_CONSTANTS.ts
 * The Unified Bridge: Root 42 (Hexagonal) ↔ Root 51 (17-gon Fracture)
 */

export const SOVEREIGN_CONSTANTS = {
    // Base Roots
    ROOT_42: Math.sqrt(42), // 6.4807 (The Habitability Base)
    ROOT_51: Math.sqrt(51), // 7.1414 (The Fracture/17-gon Base)

    // The Heterodyne Beat (The Heartbeat of the Gap)
    BEAT_FREQUENCY: Math.sqrt(51) - Math.sqrt(42), // 0.6606 Hz

    // The Hades Gap (Structural Tensegrity)
    PSI: 0.1237, // 12.37% (e / 22 resonance)

    // The Prime Intrusion (17-gon geometry)
    PACKING_RHO: Math.sqrt(14 / 17), // 0.9075
    SHEAR_ANGLE_THETA: Math.atan(14 / 17) * (180 / Math.PI), // 39.47°
    OVERPACK_DELTA: Math.sqrt(14 / 17) - (Math.PI / (2 * Math.sqrt(3))), // 0.000585

    // Acoustic Triad (The Ring)
    FREQUENCIES: {
        LOW: 648.07,  // √42 * 100
        MID: 714.14,  // √51 * 100
        HIGH: 774.60, // √60 * 100
    }
};

export const THERMODYNAMIC_LAWS = {
    MOD_GOVERNOR: 24,
    FLIP_RATE: Math.sqrt(42) % 24, // 6.4807...
    LIGHT_SPEED_C: 299792458, // Arc-length time calculation
    MOBIUS_TORSION_RAD: 3 * Math.PI, // 540 degrees of torsion
    PENTAGON_ANGLE: 108,             // 3 * (2 * 3)^2 - The geometric lock for the icosidodecahedron
    GREAT_YEAR: 25920,               // 108 * 240
    PRECESSIONAL_CYCLE: 24000,       // 24,000 year Great Year
};
