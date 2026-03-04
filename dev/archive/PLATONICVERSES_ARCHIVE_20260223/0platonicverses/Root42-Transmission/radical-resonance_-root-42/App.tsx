import React, { useState, useEffect, useCallback } from 'react';
import { Scene } from './components/Scene';
import { Controls } from './components/Controls';
import { ViewMode, SimulationParams } from './types';
import { audioEngine } from './utils/audioEngine';
import { LADDER_STEPS } from './constants';

const App: React.FC = () => {
  const [mode, setMode] = useState<ViewMode>(ViewMode.FIELD);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  
  // Default to Step 1: The Interference Solid (93 Vertices)
  const initialStep = LADDER_STEPS[1];
  
  const [params, setParams] = useState<SimulationParams>({
    interferenceA: Math.sqrt(42),
    interferenceB: Math.sqrt(initialStep.radicand),
    distortion: 0.25,
    rotationSpeed: 0.2,
    activeStep: 1,
    fracture: false
  });

  const toggleAudio = useCallback(() => {
    if (isPlayingAudio) {
      audioEngine.stop();
      setIsPlayingAudio(false);
    } else {
      // Triadic Chord Generation based on the Ladder
      // Using x100 scale as per Python Sonification script (audible range)
      // Freqs: Root42, Root51, Root60 (The standard triad of the ladder)
      // If manual, we deduce 3rd freq by maintaining the gap logic or just use fixed triad for the "Hum" experience
      
      const freqA = params.interferenceA * 100; 
      const freqB = params.interferenceB * 100;
      
      // Calculate 3rd harmonic roughly based on the ladder progression for consistency
      // Step 0(42) -> Step 1(51) -> Step 2(60). Gap is 9.
      // So Harmonic C is approx sqrt(radicand + 9) * 100
      const radB = params.interferenceB * params.interferenceB;
      const freqC = Math.sqrt(radB + 9) * 100;

      audioEngine.playTriad(freqA, freqB, freqC, 0.15);
      setIsPlayingAudio(true);
    }
  }, [isPlayingAudio, params.interferenceA, params.interferenceB]);

  // Update audio in real-time if playing
  useEffect(() => {
    if (isPlayingAudio) {
        const freqA = params.interferenceA * 100;
        const freqB = params.interferenceB * 100;
        const radB = params.interferenceB * params.interferenceB;
        const freqC = Math.sqrt(radB + 9) * 100;
        
        audioEngine.playTriad(freqA, freqB, freqC, 0.15);
    }
  }, [params.interferenceA, params.interferenceB]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="relative w-screen h-screen bg-[#050508] overflow-hidden">
      <Scene mode={mode} params={params} />
      <Controls 
        mode={mode} 
        setMode={setMode} 
        params={params} 
        setParams={setParams}
        isPlayingAudio={isPlayingAudio}
        toggleAudio={toggleAudio}
      />
    </div>
  );
};

export default App;