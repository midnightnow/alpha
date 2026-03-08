
import { WaveParams, ViewState } from '../types';
import { DEFAULT_WAVE_PARAMS, SQRT_42, SQRT_51 } from '../constants';

export interface ResearchPreset {
  id: string;
  name: string;
  description: string;
  parameters: Partial<WaveParams>;
  view?: Partial<ViewState>;
  citation?: string;
}

export const RESEARCH_PRESETS: ResearchPreset[] = [
  {
    id: 'standard',
    name: 'Standard Model',
    description: 'Baseline configuration using standard biological constants.',
    parameters: DEFAULT_WAVE_PARAMS
  },
  {
    id: 'vitruvian-decryption',
    name: 'Vitruvian Decryption (√42)',
    description: 'The "Substantiation" state. Geometry scale locked to √42 (~6.48), focusing on the Navel center where wave density collapses into form.',
    parameters: {
      ...DEFAULT_WAVE_PARAMS,
      geometryScale: SQRT_42,
      scanHeight: 4.2, // Critical resonance point for √42
      wavelength: 1.0,
      intensityThreshold: 0.25,
    },
    view: {
      resonanceLock: true,
      mirror: true
    },
    citation: 'Grant (2018) Unlocking the Cipher; Da Vinci (1490).'
  },
  {
    id: 'etheric-bridge',
    name: 'Etheric Bridge (√51)',
    description: 'Experimental: The "Higher Man" state (~π + 4). Shifts focus to the Heart/Core Star level. Note: Requires precise tuning.',
    parameters: {
      ...DEFAULT_WAVE_PARAMS,
      geometryScale: SQRT_51,
      scanHeight: 4.8, 
      wavelength: 1.05, // Adjusted wavelength for larger scale
      intensityThreshold: 0.25,
    },
    view: {
      resonanceLock: true,
      mirror: true
    },
    citation: 'Brennan (1993); Theoretical Extension'
  },
  {
    id: 'heart-station',
    name: 'Heart Station (Anahata)',
    description: 'Optimized for peak hexagonal symmetry at the cardiac center (Y=4.32).',
    parameters: {
      ...DEFAULT_WAVE_PARAMS,
      scanHeight: 4.32,
      wavelength: 1.0,
      originSeparation: 12.0,
      originCOffset: 12.0,
      intensityThreshold: 0.30, 
      spatialCoherence: 0.73,
      geometryScale: 2.4, // Classic Scale
    },
    view: {
      resonanceLock: true,
      quaternion: false
    },
    citation: 'Brennan (1993) Light Emerging; Hecht (2002) Optics.'
  },
  {
    id: 'golden-ratio',
    name: 'Golden Ratio',
    description: 'Parameters tuned to Phi (1.618) harmonics.',
    parameters: { 
      ...DEFAULT_WAVE_PARAMS, 
      wavelength: 1.618, 
      originSeparation: 16.18, 
      phasePhi: 137.5, 
      phasePsi: 137.5, 
      geometryScale: 3.2 
    }
  }
];
