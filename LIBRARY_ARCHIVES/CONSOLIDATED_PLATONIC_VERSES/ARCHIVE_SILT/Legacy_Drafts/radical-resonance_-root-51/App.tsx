import React, { useState, useEffect, useCallback } from 'react';
import { Scene } from './components/Scene';
import { Controls } from './components/Controls';
import { ViewMode, SimulationParams } from './types';
import { audioEngine } from './utils/audioEngine';
import { InterfaceHUD } from './components/InterfaceHUD';
import { LADDER_STEPS } from './constants';
import { ROOT_51, ROOT_60 } from '@platonic/core';

import { STLExporter } from 'three-stdlib';
import * as THREE from 'three';

const App: React.FC = () => {
  const [mode, setMode] = useState<ViewMode>(ViewMode.FIELD);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const meshRef = React.useRef<THREE.Mesh>(null);

  // Default to Step 1: The Root 51 Interference
  const initialStep = LADDER_STEPS[1];

  const [params, setParams] = useState<SimulationParams>({
    interferenceA: ROOT_51,
    interferenceB: ROOT_60,
    distortion: 0.25,
    rotationSpeed: 0.2,
    activeStep: 1,
    fracture: false,
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

  // "Anchor the Scars" - Persistence Logic
  const queryParams = new URLSearchParams(window.location.search);
  const currentH3 = queryParams.get('h3') || '8928308280fffff'; // Default to a known cell if none provided

  useEffect(() => {
    let lastAnchorTime = 0;
    const interval = setInterval(() => {
      if (!isPlayingAudio) return;

      const resonance = audioEngine.getResonance();
      const now = Date.now();

      // If resonance exceeds threshold (> 0.8) and 2s has passed
      if (resonance > 0.8 && now - lastAnchorTime > 2000) {
        lastAnchorTime = now;

        console.log(`[PMG] Stress Limit Exceeded at ${currentH3}. Anchoring Scars...`);

        // We use the Mathman server as the unified gateway
        fetch('http://localhost:3000/api/fracture', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ h3Index: currentH3, resonance: 1.0 - resonance }) // Inverting to represent "damage"
        }).catch(err => console.error("Memory Lattice Connection Failed", err));
      }
    }, 100);

    return () => clearInterval(interval);
  }, [isPlayingAudio, currentH3]);

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
      <Scene mode={mode} params={params} ref={meshRef} />
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