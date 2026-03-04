import React, { useState, useEffect, useCallback } from 'react';
import { Scene } from './components/Scene';
import { Controls } from './components/Controls';
import { ViewMode, SimulationParams } from './types';
import { audioEngine } from './utils/audioEngine';
import { InterfaceHUD } from './components/InterfaceHUD';
import { LADDER_STEPS } from './constants';

import { STLExporter } from 'three-stdlib';
import * as THREE from 'three';

import { MathmanV1Patch } from './components/MathmanV1Patch';

const App: React.FC = () => {
  const [mode, setMode] = useState<ViewMode>(ViewMode.FIELD);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const meshRef = React.useRef<THREE.Mesh>(null);

  // Default to Step 1: The Interference Solid (93 Vertices)
  const initialStep = LADDER_STEPS[1];

  const [params, setParams] = useState<SimulationParams>({
    interferenceA: Math.sqrt(42),
    interferenceB: Math.sqrt(51), // Hardened to Root 51
    distortion: 0.25,
    rotationSpeed: 0.2,
    activeStep: 1,
    fracture: true, // Default to fractured/vitrified state
    harmonicMode: 'fracture'
  });

  const handleExport = useCallback(() => {
    if (!meshRef.current) return;

    // Ensure we are exporting logic from a scene where rotation isn't crazy
    const originalRotation = meshRef.current.rotation.clone();
    meshRef.current.rotation.set(0, 0, 0);

    const exporter = new STLExporter();
    const result = exporter.parse(meshRef.current);

    const blob = new Blob([result], { type: 'application/octet-stream' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `root42_phase2_fracture_${params.fracture ? 'active' : 'dormant'}.stl`;
    link.click();

    // Restore rotation
    meshRef.current.rotation.copy(originalRotation);
  }, [params.fracture]);

  const toggleAudio = useCallback(() => {
    if (isPlayingAudio) {
      audioEngine.stop();
      setIsPlayingAudio(false);
    } else {
      const freqA = params.interferenceA * 100;
      const freqB = params.interferenceB * 100;
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
      {mode === ViewMode.ECHO || mode === ViewMode.FIELD ? (
        <MathmanV1Patch params={params} />
      ) : (
        <Scene mode={mode} params={params} ref={meshRef} />
      )}

      <Controls
        mode={mode}
        setMode={setMode}
        params={params}
        setParams={setParams}
        isPlayingAudio={isPlayingAudio}
        toggleAudio={toggleAudio}
        onExport={handleExport}
      />

      {/* Sentient Interface HUD (Phase IV) */}
      <InterfaceHUD
        manualSalience={isPlayingAudio ? 8.5 : 0.5}
        manualHardness={params.fracture ? 9.0 : 4.0}
      />
    </div>
  );
};

export default App;