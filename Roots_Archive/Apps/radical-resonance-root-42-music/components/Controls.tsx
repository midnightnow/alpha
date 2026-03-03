import React, { useState, useEffect } from 'react';
import { ViewMode, SimulationParams } from '../types';
import { LADDER_STEPS } from '../constants';
import { Play, Pause, Download, Github, Cpu, Layers, Box, ChevronsUp, Zap, Radio, Hammer } from 'lucide-react';
import { toneEngine } from '../utils/toneEngine';
import { youtubeExporter } from '../utils/recorder';
import * as THREE from 'three';
import { STLExporter } from 'three/examples/jsm/exporters/STLExporter';

import { SequenceController } from '../utils/SequenceController';

interface Props {
  mode: ViewMode;
  setMode: (m: ViewMode) => void;
  params: SimulationParams;
  setParams: React.Dispatch<React.SetStateAction<SimulationParams>>;
  isPlayingAudio: boolean;
  toggleAudio: () => void;
}

export const Controls: React.FC<Props> = ({
  mode, setMode, params, setParams, isPlayingAudio, toggleAudio
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPerforming, setIsPerforming] = useState(false);
  const [performanceTime, setPerformanceTime] = useState(0);

  // Initialize SequenceController lazily
  const [sequenceController] = useState(() =>
    new SequenceController(
      (updatedParams: Partial<SimulationParams>) => {
        setParams(prev => ({ ...prev, ...updatedParams }));
      },
      () => {
        setIsPerforming(false);
        setPerformanceTime(0);
      }
    )
  );

  // Update performance time readout
  useEffect(() => {
    let interval: any;
    if (isPerforming) {
      const start = performance.now();
      interval = setInterval(() => {
        setPerformanceTime((performance.now() - start) / 1000);
      }, 100);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPerforming]);

  const handleDownload = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(params, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "radical_resonance_config.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  const handleStepSelect = (stepIndex: number) => {
    const step = LADDER_STEPS[stepIndex];
    setParams({
      ...params,
      interferenceA: Math.sqrt(42),
      interferenceB: Math.sqrt(step.radicand),
      activeStep: stepIndex,
      distortion: 0.2 + (stepIndex * 0.05) // Increase distortion slightly with complexity
    });
    toneEngine.setStep(stepIndex);
  };

  const handleSandboxStart = async () => {
    await toneEngine.init();
    toneEngine.start();
    setMode(ViewMode.SANDBOX);
  };

  const handleRecord = async () => {
    if (isRecording) {
      await youtubeExporter.stop('Radical_Resonance_Manual_Capture');
      setIsRecording(false);
      return;
    }

    const canvas = document.querySelector('canvas');
    if (!canvas) return;

    youtubeExporter.start(canvas);
    setIsRecording(true);
  };

  const handleMasterCapture = async () => {
    if (isPerforming) {
      sequenceController.stop();
      setIsPerforming(false);
      return;
    }

    const canvas = document.querySelector('canvas');
    if (!canvas) return;

    setMode(ViewMode.SANDBOX);
    setIsPerforming(true);
    await sequenceController.start(canvas);
  };

  const handleMaterialize = () => {
    const scene = document.querySelector('canvas')?.parentElement; // Rough way to get context, but better to query Three.js scene object.
    // Actually, we can traverse from the root or use a global reference.
    // However, since we don't have direct access to the 'scene' object here easily without context,
    // we'll use a safer method: finding the specific mesh by UUID if we had it, or name.

    // Better approach: We can't easily access the Three.js scene from outside the Canvas context in R3F v8 without a hook.
    // But since this is a "hacky" creative coding enviro, let's assume we can find it via the window object if we exposed it, 
    // OR, we can just rely on the fact that we can't export directly from here without a ref.

    // WAIT. We DON'T have access to the scene here. 'Controls' is outside the Canvas.
    // We need to pass a signal to the internal components or use a global state store.

    // FASTEST PATH: Dispatch a custom event that the internal component listens to?
    // OR, just use the 'window' object if we attach the scene to it (debug mode).
    // Let's look at App.tsx to see if Scene is exposed.

    // Actually, let's use a simpler trick: We can't export from outside easily. 
    // User asked to "Add a button". 
    // I will add the logic to 'InterferenceMesh' to listen for a global event or prop?
    // No, 'Controls' is a sibling.

    // Let's use a Custom Event "trigger-stl-export".
    window.dispatchEvent(new CustomEvent('radical-resonance-materialize'));
  };

  const activeStepInfo = params.activeStep !== null ? LADDER_STEPS[params.activeStep] : null;

  return (
    <div className="absolute top-0 left-0 w-full h-full pointer-events-none flex flex-col justify-between p-6">

      {/* Header */}
      <div className="flex justify-between items-start pointer-events-auto">
        <div>
          <h1 className="text-2xl font-bold font-mono text-white tracking-tighter">
            RADICAL<span className="text-cyan-400">RESONANCE</span>
          </h1>
          <p className="text-xs text-gray-400 font-mono mt-1">
            SQRT(42) GENETIC LADDER
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleDownload}
            className="p-2 bg-gray-900/80 border border-gray-700 text-gray-300 hover:text-cyan-400 hover:border-cyan-400 transition rounded"
            title="Download Config"
          >
            <Download size={18} />
          </button>
          <button
            className="p-2 bg-gray-900/80 border border-gray-700 text-gray-300 hover:text-cyan-400 hover:border-cyan-400 transition rounded"
            title="View Source"
            onClick={() => alert("Source code embedded.")}
          >
            <Github size={18} />
          </button>
        </div>
      </div>

      {/* Main Control Panel (Bottom) */}
      <div className="pointer-events-auto bg-gray-950/90 backdrop-blur-md border border-gray-800 rounded-lg p-4 w-full max-w-md self-center md:self-start md:mb-0 mb-4 shadow-2xl">

        {/* Ladder Selector */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 mb-2">
            <ChevronsUp size={14} /> RADICAL LADDER
          </div>
          <div className="grid grid-cols-4 gap-1">
            {LADDER_STEPS.map((step) => (
              <button
                key={step.step}
                disabled={isPerforming}
                onClick={() => handleStepSelect(step.step)}
                className={`py-2 px-1 text-[10px] font-mono border rounded transition-all duration-300 flex flex-col items-center justify-center
                            ${params.activeStep === step.step
                    ? 'bg-cyan-900/40 border-cyan-400 text-cyan-300 shadow-[0_0_10px_rgba(34,211,238,0.2)]'
                    : 'bg-gray-900/50 border-gray-800 text-gray-500 hover:border-gray-600 hover:text-gray-300'
                  } ${isPerforming ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <span className="font-bold text-lg mb-1">{step.step}</span>
                <span>{step.label}</span>
              </button>
            ))}
          </div>
          {activeStepInfo && (
            <div className="mt-2 text-[10px] font-mono text-center text-gray-500 bg-black/20 py-1 rounded">
              {activeStepInfo.desc.toUpperCase()} // √42 : √{activeStepInfo.radicand}
            </div>
          )}
        </div>

        {/* Sliders */}
        <div className="space-y-4 mb-6 border-t border-gray-800 pt-4">
          <div>
            <div className="flex justify-between text-xs font-mono text-gray-400 mb-1">
              <span>HARMONIC A (√42)</span>
              <span>{params.interferenceA.toFixed(3)}</span>
            </div>
            <input
              type="range" min="1" max="12" step="0.01"
              disabled={isPerforming}
              value={params.interferenceA}
              onChange={(e) => setParams({ ...params, interferenceA: parseFloat(e.target.value), activeStep: null })}
              className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-cyan-500"
            />
          </div>
          <div>
            <div className="flex justify-between text-xs font-mono text-gray-400 mb-1">
              <span>HARMONIC B (√N)</span>
              <span>{params.interferenceB.toFixed(3)}</span>
            </div>
            <input
              type="range" min="1" max="12" step="0.01"
              disabled={isPerforming}
              value={params.interferenceB}
              onChange={(e) => setParams({ ...params, interferenceB: parseFloat(e.target.value), activeStep: null })}
              className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
            />
          </div>
          <div>
            <div className="flex justify-between text-xs font-mono text-gray-400 mb-1">
              <span>AMPLITUDE (DISTORTION)</span>
              <span>{params.distortion.toFixed(2)}</span>
            </div>
            <input
              type="range" min="0" max="1" step="0.01"
              disabled={isPerforming}
              value={params.distortion}
              onChange={(e) => {
                const val = parseFloat(e.target.value);
                setParams({ ...params, distortion: val });
                toneEngine.setDistortion(val); // Update audio engine
              }}
              className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-pink-500"
            />
          </div>
        </div>

        {/* Mode Toggles */}
        <div className="flex gap-2 mb-4">
          <button
            disabled={isPerforming}
            onClick={() => setMode(ViewMode.FIELD)}
            className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.FIELD ? 'bg-indigo-900/30 border-indigo-500 text-indigo-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'} ${isPerforming ? 'opacity-50' : ''}`}
          >
            <Cpu size={12} /> FIELD
          </button>
          <button
            disabled={isPerforming}
            onClick={() => setMode(ViewMode.SOLID)}
            className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.SOLID ? 'bg-purple-900/30 border-purple-500 text-purple-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'} ${isPerforming ? 'opacity-50' : ''}`}
          >
            <Box size={12} /> SOLID
          </button>
          <button
            disabled={isPerforming}
            onClick={() => setMode(ViewMode.CRYSTAL)}
            className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.CRYSTAL ? 'bg-teal-900/30 border-teal-500 text-teal-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'} ${isPerforming ? 'opacity-50' : ''}`}
          >
            <Layers size={12} /> MESH
          </button>
        </div>

        {/* Sandbox Tools */}
        <div className="mb-4 border-t border-gray-800 pt-4">
          <div className="flex items-center gap-2 text-xs font-mono text-pink-400 mb-2">
            <Zap size={14} /> GENERATIVE SANDBOX
          </div>
          <div className="flex gap-2 mb-2">
            <button
              disabled={isPerforming}
              onClick={handleSandboxStart}
              className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.SANDBOX ? 'bg-pink-900/30 border-pink-500 text-pink-400 animate-pulse' : 'border-gray-700 text-gray-400 hover:border-gray-500'} ${isPerforming ? 'opacity-50' : ''}`}
            >
              <Radio size={12} /> {mode === ViewMode.SANDBOX ? 'ACTIVE' : 'INITIATE'}
            </button>

            <button
              disabled={isPerforming}
              onClick={handleRecord}
              className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${isRecording ? 'bg-red-900/50 border-red-500 text-red-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'} ${isPerforming ? 'opacity-50' : ''}`}
            >
              <div className={`w-2 h-2 rounded-full mr-1 ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-gray-500'}`} />
              {isRecording ? 'STOP REC' : 'RECORD'}
            </button>
          </div>

          {/* MASTER CAPTURE (SCRIPTED) */}
          <div className="flex gap-2 mb-2">
            <button
              onClick={handleMasterCapture}
              className={`flex-1 py-2 text-[10px] font-mono border rounded transition-all flex items-center justify-center gap-2
                        ${isPerforming
                  ? 'bg-red-900/50 text-red-200 border-red-500 animate-pulse'
                  : 'bg-cyan-900/50 text-cyan-200 border-cyan-500 hover:bg-cyan-800/50 shadow-[0_0_15px_rgba(34,211,238,0.2)]'
                }`}
            >
              <Zap size={14} className={isPerforming ? 'animate-spin' : ''} />
              {isPerforming ? `RECORDING BREACH: ${performanceTime.toFixed(1)}s` : 'MASTER CAPTURE'}
            </button>

            <button
              onClick={handleMaterialize}
              title="Export STL for 3D Printing"
              className="flex-[0.5] py-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition bg-amber-900/30 border-amber-500 text-amber-400 hover:bg-amber-900/50"
            >
              <Hammer size={14} /> MATERIALIZE
            </button>
          </div>

          {/* Audio Controls */}
          {mode === ViewMode.SANDBOX && (
            <div className="mt-4 space-y-3 bg-black/20 p-2 rounded border border-gray-800">
              <div className="text-[10px] font-mono text-gray-500 mb-1">AUDIO MIXER</div>

              {/* Master Volume */}
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-gray-400 w-12">VOL</span>
                <input
                  type="range" min="0" max="1" step="0.01" defaultValue="1"
                  disabled={isPerforming}
                  onChange={(e) => toneEngine.setMasterVolume(parseFloat(e.target.value))}
                  className="flex-1 h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500"
                />
              </div>

              {/* Playback Speed */}
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-gray-400 w-12">SPD</span>
                <input
                  type="range" min="0.5" max="2" step="0.1" defaultValue="1"
                  onChange={(e) => toneEngine.setPlaybackSpeed(parseFloat(e.target.value))}
                  className="flex-1 h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
              </div>

              {/* Toggles */}
              <div className="grid grid-cols-4 gap-1">
                <button
                  onClick={() => {
                    const btn = document.getElementById('btn-mute');
                    const isMuted = btn?.classList.contains('bg-red-900/50');
                    toneEngine.setMuted(!isMuted);
                    btn?.classList.toggle('bg-red-900/50');
                    btn?.classList.toggle('text-red-400');
                    btn?.classList.toggle('border-red-500');
                  }}
                  id="btn-mute"
                  className="py-1 text-[9px] font-mono border border-gray-700 text-gray-400 rounded hover:border-gray-500"
                >
                  MUTE
                </button>
                <button
                  onClick={(e) => {
                    const btn = e.currentTarget;
                    const isActive = btn.classList.toggle('bg-blue-900/50');
                    btn.classList.toggle('text-blue-400');
                    btn.classList.toggle('border-blue-500');
                    toneEngine.setLayerState('kick', isActive);
                  }}
                  className="py-1 text-[9px] font-mono border border-blue-500 text-blue-400 bg-blue-900/50 rounded"
                >
                  KICK
                </button>
                <button
                  onClick={(e) => {
                    const btn = e.currentTarget;
                    const isActive = btn.classList.toggle('bg-purple-900/50');
                    btn.classList.toggle('text-purple-400');
                    btn.classList.toggle('border-purple-500');
                    toneEngine.setLayerState('lattice', isActive);
                  }}
                  className="py-1 text-[9px] font-mono border border-purple-500 text-purple-400 bg-purple-900/50 rounded"
                >
                  PAD
                </button>
                <button
                  onClick={(e) => {
                    const btn = e.currentTarget;
                    const isActive = btn.classList.toggle('bg-pink-900/50');
                    btn.classList.toggle('text-pink-400');
                    btn.classList.toggle('border-pink-500');
                    toneEngine.setLayerState('glitch', isActive);
                  }}
                  className="py-1 text-[9px] font-mono border border-pink-500 text-pink-400 bg-pink-900/50 rounded"
                >
                  GLITCH
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Fracture Toggle */}
        <button
          onClick={() => {
            const newFracture = !params.fracture;
            setParams({ ...params, fracture: newFracture });
            if (newFracture) toneEngine.triggerDrop(); // Trigger drop on fracture
          }}
          className={`w-full py-2 mb-4 text-xs font-mono border rounded flex items-center justify-center gap-2 transition ${params.fracture ? 'bg-orange-900/40 border-orange-500 text-orange-400 animate-pulse' : 'border-gray-700 text-gray-400'}`}
        >
          <Zap size={14} /> {params.fracture ? 'FRACTURE SYNTHESIS ACTIVE' : 'ENABLE FRACTURE SYNTHESIS'}
        </button>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            onClick={toggleAudio}
            className={`flex-1 py-3 px-4 rounded font-mono text-xs font-bold flex items-center justify-center gap-2 transition ${isPlayingAudio ? 'bg-red-500/10 text-red-400 border border-red-500/50' : 'bg-gray-800 hover:bg-gray-700 text-white'}`}
          >
            {isPlayingAudio ? <Pause size={14} /> : <Play size={14} />}
            {isPlayingAudio ? 'STOP TRIADIC HUM' : 'ACTIVATE AUDIO SEAL'}
          </button>
        </div>
      </div>

      {/* Footer Info */}
      <div className="absolute bottom-6 right-6 text-right pointer-events-none hidden md:block">
        <div className="text-xs font-mono text-gray-500 bg-black/40 backdrop-blur px-4 py-2 rounded border border-gray-800">
          <div className="text-cyan-500 font-bold mb-1">
            {activeStepInfo ? activeStepInfo.name.toUpperCase() : 'CUSTOM PARAMETRIC'}
          </div>
          <div className="flex justify-between gap-4">
            <span>VERTICES:</span>
            <span className="text-white">{activeStepInfo ? activeStepInfo.vertices : 'VARIABLE'}</span>
          </div>
          <div className="flex justify-between gap-4">
            <span>OVERPACK DELTA:</span>
            <span className={params.fracture ? "text-orange-400" : "text-gray-500"}>
              {params.fracture ? '0.000585 (ACTIVE)' : 'LATENT'}
            </span>
          </div>
          <div className="flex justify-between gap-4">
            <span>STATUS:</span>
            <span className={params.fracture ? "text-orange-400 font-bold" : "text-white"}>
              {params.fracture ? 'ARCHIVE SEALED' : (activeStepInfo ? 'LOCKED' : 'UNSTABLE')}
            </span>
          </div>
        </div>
      </div>

      {/* Metadata Overlay (Hacker HUD) - Visible in Sandbox Mode */}
      {mode === ViewMode.SANDBOX && (
        <div className="absolute top-6 right-6 pointer-events-none text-right font-mono text-[10px] text-green-500/80 leading-tight">
          <div>SYSTEM_ROOT: 42.0000</div>
          <div>ψ(r) = sin({params.interferenceA.toFixed(2)}·θ) × sin({params.interferenceB.toFixed(2)}·φ)</div>
          <div>SHEAR_ANGLE: 39.4° [LOCKED]</div>
          <div className="mt-2">
            OVERPACK_DELTA: <span className={params.fracture ? "text-orange-400 font-bold" : "text-green-500"}>{params.fracture ? '0.000585' : 'LATENT'}</span>
          </div>
          <div>
            STATUS: {params.fracture ? <span className="text-red-500 animate-pulse">CRITICAL_FRACTURE</span> : <span className="text-green-500">STABLE</span>}
          </div>
          <div className="mt-2 text-xs opacity-50">
                  // RADICAL RESONANCE ARCHIVE //
          </div>
        </div>
      )}

    </div>
  );
};