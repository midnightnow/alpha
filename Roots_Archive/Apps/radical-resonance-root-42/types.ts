FIELD = 'FIELD',
  SOLID = 'SOLID',
  CRYSTAL = 'CRYSTAL',
  ECHO = 'ECHO'
}

export interface AudioState {
  isPlaying: boolean;
  volume: number;
  frequencyA: number;
  frequencyB: number;
}

export interface SimulationParams {
  interferenceA: number;
  interferenceB: number;
  distortion: number;
  rotationSpeed: number;
  activeStep: number | null; // null implies manual override
  fracture: boolean;
  harmonicMode: 'smooth' | 'fracture';
  showGrid?: boolean;
}