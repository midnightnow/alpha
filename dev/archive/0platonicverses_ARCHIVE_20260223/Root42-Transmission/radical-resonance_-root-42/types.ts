export enum ViewMode {
  FIELD = 'FIELD',
  SOLID = 'SOLID',
  CRYSTAL = 'CRYSTAL'
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
}