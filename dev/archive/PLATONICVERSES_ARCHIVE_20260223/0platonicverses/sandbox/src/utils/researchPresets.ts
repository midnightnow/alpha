/**
 * PMG SANDBOX - RESEARCH PRESETS
 * Presets for various geometric states and experiments.
 */

import { PMG_CONSTANTS } from '../types';

export const RESEARCH_PRESETS = {
    STANDARD_HUMAN: {
        id: 'standard-human',
        name: 'Standard Human (√42)',
        description: 'Biological baseline using the Heart Resonance constant.',
        params: {
            scanHeight: 1.0,
            geometryScale: PMG_CONSTANTS.HEART_RESONANCE,
            intensityThreshold: 0.2,
            wavelength: 1.0,
            originSeparation: 6.0,
            originCOffset: 7.0,
            rationalCoefficient: 0.618,
            organicCoefficient: 1.0,
            quaternionMode: false,
            resonanceLock: true
        },
        citation: 'Book I: The Platonic Verses'
    },

    CROWN_LOCK_PROTOCOL: {
        id: 'area-51-crown',
        name: 'Area 51: The Outer Orbit (√51)',
        description: 'Targeting the "Halo" anomaly at Y=7.0. Applies the Orthogonal Shift (+3.0z) to align with the √51 grid.',
        params: {
            // The Elevation Target
            scanHeight: 7.0,          // Sahasrara (The Crown)

            // The Dimensional Shift (The Hypotenuse)
            geometryScale: PMG_CONSTANTS.OUTER_ORBIT,    // √51 ≈ 7.1414

            // The Damping Field (High Tension)
            intensityThreshold: 0.35, // Requires stronger signal to lock

            // The "Alien" Geometry
            wavelength: 1.0,
            originSeparation: 12.0,   // Base Dodecagonal resonance
            originCOffset: 15.0,      // Elevated Solar Point (The stretched triangle)

            // Coefficients
            rationalCoefficient: 0.73, // 1/α (Fine Structure)
            organicCoefficient: 0.571, // 4/7 (Heptagonal)

            // Narrative Mode
            quaternionMode: true,      // Visualizes the multidimensionality
            resonanceLock: true
        },
        citation: 'Book II: Area 51 - The Orthogonal Shift'
    }
};
