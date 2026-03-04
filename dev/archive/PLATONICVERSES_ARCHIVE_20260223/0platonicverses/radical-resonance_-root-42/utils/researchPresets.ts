/**
 * RADICAL RESONANCE - RESEARCH PRESETS
 * Presets for the Radical Quasicrystal Visualizer.
 */

export const RESEARCH_PRESETS = {
    STANDARD_HUMAN: {
        id: 'standard-human',
        name: 'Standard Human (√42)',
        description: 'Biological baseline using the Heart Resonance constant.',
        params: {
            interferenceA: Math.sqrt(42),
            interferenceB: Math.sqrt(42),
            distortion: 0.2,
            rotationSpeed: 0.2,
            activeStep: 0,
            fracture: false
        },
        citation: 'Book I: The Platonic Verses'
    },

    CROWN_LOCK_PROTOCOL: {
        id: 'area-51-crown',
        name: 'Area 51: The Outer Orbit (√51)',
        description: 'Targeting the "Halo" anomaly at Y=7.0. Applies the Orthogonal Shift to align with the √51 grid.',
        params: {
            interferenceA: Math.sqrt(42),     // The Vessel
            interferenceB: Math.sqrt(51),     // The Signal (√51 ≈ 7.14)
            distortion: 0.35,                // Higher tension
            rotationSpeed: 0.15,             // Deliberate rotation
            activeStep: 1,                   // Ladder Step 1
            fracture: true                    // Fracture Synthesis Active
        },
        citation: 'Book II: Area 51 - The Orthogonal Shift'
    }
};
