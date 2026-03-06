
import { WaveParams, LayerVisibility, ViewState } from './types';

export const SQRT_42 = 6.4807406984; // Material Plane / Navel (Substantiation)
export const SQRT_51 = 7.1414284285; // Resonant Sphere / Heart (Elevation)

export const DEFAULT_WAVE_PARAMS: WaveParams = {
  originSeparation: 12.0,
  originCOffset: 12.0,
  scanHeight: 4.2, // Aligned to SQRT_42 resonance (Navel/Substantiation)
  wavelength: 1.0,
  phasePhi: 0,
  phasePsi: 0,
  intensityThreshold: 0.15, // Reduced from 0.25 to ensure visibility
  waveBrightness: 0.50,
  nodalBudget: 2000,
  nestingDepth: 3,
  spatialCoherence: 0.73,
  temporalFrequency: 0.571,
  geometryScale: SQRT_42, // CORE FIX: Default to √42
  projectionMode: false,
  layerSeparation: 2.0,
  nodeSize: 1.0,
};

export const DEFAULT_LAYERS: LayerVisibility = {
  foundation: true,
  hexagonalLattice: false,
  earthMoon: false,
  triangleGeometry: false,
  heptagonalGrid: false,
  primeModuloGrid: false,
  platonic: false,
  sephiroticGraph: false,
  harmonicSpine: false,
  vitruvian: true,
  annotations: true,
  starTetrahedron: false,
  haricLevel: false,
  coreStarLevel: false,
};

export const DEFAULT_VIEW: ViewState = {
  zoom: 0.9,
  panX: 0,
  panY: 50,
  rotation: 0,
  pitch: 0,
  mirror: false,
  primePulse: false,
  quaternion: false,
  resonanceLock: false,
};

// Derived from "Light Emerging" text (approximate Y units where 0=Feet, 7=Crown)
export const ANATOMICAL_LEVELS = [
  { id: 1, name: "Root (Coccyx)", y: 0.0, freq: "C" },
  { id: 2, name: "Sacral (Pubic)", y: 1.2, freq: "D" },
  { id: 3, name: "Solar Plexus (T12)", y: 4.2, freq: "E" }, // 4.2 Matches √42 resonance
  { id: 4, name: "Heart (T5)", y: 4.8, freq: "F" },
  { id: 5, name: "Throat (C3)", y: 5.8, freq: "G" },
  { id: 6, name: "Brow (Center Head)", y: 6.5, freq: "A" },
  { id: 7, name: "Crown (Top Head)", y: 7.0, freq: "B" },
];

export const HARIC_POINTS = {
    idPoint: 11.3,
    soulSeat: 5.0,
    tanTien: 3.54,
    coreStar: 3.95,
    earthCore: -200
};

export const SEPHIROTIC_NODES = [
  { name: 'Kether', id: 'K', x: 0, y: 7.0 },
  { name: 'Chokmah', id: 'C', x: 1.2, y: 6.0 },
  { name: 'Binah', id: 'B', x: -1.2, y: 6.0 },
  { name: 'Chesed', id: 'Ch', x: 3.5, y: 5.2 },
  { name: 'Geburah', id: 'G', x: -3.5, y: 5.2 },
  { name: 'Tiphareth', id: 'T', x: 0, y: 4.32 },
  { name: 'Netzach', id: 'N', x: 3.0, y: 1.5 },
  { name: 'Hod', id: 'H', x: -3.0, y: 1.5 },
  { name: 'Yesod', id: 'Y', x: 0, y: 3.2 },
  { name: 'Malkuth', id: 'M', x: 0, y: 0 },
];
