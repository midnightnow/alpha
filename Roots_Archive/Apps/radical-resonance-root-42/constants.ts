/**
 * DEPRECATED: Use @platonic/core for the Unified Geometric Laws.
 * This file is kept for backward compatibility until migration is complete.
 */
export const ROOT_42 = Math.sqrt(42);
export const ROOT_51 = Math.sqrt(51);
export const PHI = (1 + Math.sqrt(5)) / 2;

// Frequencies for the "Hum"
export const FREQ_HEX = 60.0;
export const FREQ_HEP = 70.0; // 6:7 ratio approx

// Phase IV: Unified Geometric Laws
export const UNITY_THRESHOLD = 0.8254; // ρ = sqrt(14/17)
export const HADES_GAP = 0.1237; // Ψ
export const SHEAR_ANGLE = 39.47; // θ
export const BEAT_FREQUENCY = 0.6606; // β

export const COLORS = {
  primary: '#00ffff',
  secondary: '#ff0055',
  bg: '#050508',
  grid: 'rgba(255, 255, 255, 0.1)',
  originA: '#FF6F61',
  originB: '#6B5B95',
  echo: '#00f3ff'
};

export const LADDER_STEPS = [
  { step: 0, radicand: 42, vertices: 42, name: "The Resonant Sphere", label: "BASE", desc: "Pure Potential" },
  { step: 1, radicand: 51, vertices: 93, name: "The Interference Solid", label: "INTERFERENCE", desc: "Triadic Tension" },
  { step: 2, radicand: 60, vertices: 153, name: "The Resolution Solid", label: "RESOLUTION", desc: "Harmonic Stabilizer" },
  { step: 3, radicand: 69, vertices: 222, name: "The Chaotic Solid", label: "CHAOS", desc: "Entropy Bloom" },
];