export enum ViewMode {
    FIELD = 'FIELD',
    SOLID = 'SOLID',
    CRYSTAL = 'CRYSTAL',
    ECHO = 'ECHO'
}

export interface SimulationParams {
    interferenceA: number;
    interferenceB: number;
    distortion: number;
    rotationSpeed: number;
    activeStep: number | null;
    fracture: boolean;
    harmonicMode: 'smooth' | 'fracture';
    showGrid?: boolean;
}

export const LADDER_STEPS = [
    { step: 0, radicand: 42, vertices: 42, name: "The Resonant Sphere", label: "BASE", desc: "Pure Potential" },
    { step: 1, radicand: 51, vertices: 93, name: "The Interference Solid", label: "INTERFERENCE", desc: "Triadic Tension" },
    { step: 2, radicand: 60, vertices: 153, name: "The Resolution Solid", label: "RESOLUTION", desc: "Harmonic Stabilizer" },
    { step: 3, radicand: 69, vertices: 222, name: "The Chaotic Solid", label: "CHAOS", desc: "Entropy Bloom" },
];
