
export interface WaveParams {
  originSeparation: number; // mm
  originCOffset: number; // mm
  scanHeight: number; // Y (or Z depth slice)
  wavelength: number; // mm
  phasePhi: number; // degrees
  phasePsi: number; // degrees
  intensityThreshold: number; // 0.0 - 0.95
  waveBrightness: number; // 0.0 - 1.0
  nodalBudget: number; // count
  nestingDepth: number; // 1 - 12
  spatialCoherence: number; // 0.1 - 2.0
  temporalFrequency: number; // 0.1 - 1.5
  geometryScale: number; // 1.0 - 5.0
  projectionMode: boolean; // 3D Layer Separation
  layerSeparation: number; // Distance between layers in Projection Mode
  nodeSize: number; // Size of nodes
}

export interface LayerVisibility {
  foundation: boolean;
  hexagonalLattice: boolean;
  earthMoon: boolean;
  triangleGeometry: boolean;
  heptagonalGrid: boolean;
  primeModuloGrid: boolean;
  platonic: boolean;
  sephiroticGraph: boolean;
  harmonicSpine: boolean;
  vitruvian: boolean;
  annotations: boolean;
  starTetrahedron: boolean;
  haricLevel: boolean;    // New: Intention / Life Task
  coreStarLevel: boolean; // New: Divine Essence
}

export interface ViewState {
  zoom: number;
  panX: number;
  panY: number;
  rotation: number; // Yaw in degrees
  pitch: number;    // Pitch in degrees
  mirror: boolean;
  primePulse: boolean;
  quaternion: boolean;
  resonanceLock: boolean;
}

export type ExportFormat = 'json' | 'csv' | 'json-ld';

export interface NodalPoint {
  id: string;
  x: number;
  y: number;
  intensity: number;
  classification: 'constructive' | 'destructive';
  anatomicalRegion: string;
}

export interface ResearchExportPackage {
  metadata: {
    timestamp: string;
    engineVersion: string;
    parameterHash: string;
    citationSet: string[];
  };
  parameters: WaveParams;
  nodalData: NodalPoint[];
  jsonLd?: any;
  compliance: {
    dataProvenance: string;
    piiStatus: 'none' | 'anonymized';
  };
}
