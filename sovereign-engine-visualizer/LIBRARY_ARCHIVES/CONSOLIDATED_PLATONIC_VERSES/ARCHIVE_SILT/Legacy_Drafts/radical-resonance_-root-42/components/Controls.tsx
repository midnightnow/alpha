import React from 'react';
import { ViewMode, SimulationParams } from '../types';
import { LADDER_STEPS } from '../constants';
import { Play, Pause, Download, Github, RefreshCw, Cpu, Layers, Box, ChevronsUp, Zap } from 'lucide-react';

interface Props {
  mode: ViewMode;
  setMode: (m: ViewMode) => void;
  params: SimulationParams;
  setParams: (p: SimulationParams) => void;
  isPlayingAudio: boolean;
  toggleAudio: () => void;
  onExport: () => void;
}

export const Controls: React.FC<Props> = ({
  mode, setMode, params, setParams, isPlayingAudio, toggleAudio
}) => {

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
    let newB = Math.sqrt(step.radicand);

    // If Smooth Mode is active and we select Step 1 (Interference), enforce √48 (Harmonic) instead of √51 (Fracture)
    if (params.harmonicMode === 'smooth' && step.step === 1) {
      newB = Math.sqrt(48);
    }

    setParams({
      ...params,
      interferenceA: Math.sqrt(42),
      interferenceB: newB,
      activeStep: stepIndex,
      distortion: 0.2 + (stepIndex * 0.05) // Increase distortion slightly with complexity
    });
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
            onClick={props.onExport}
            className="p-2 bg-gray-900/80 border border-gray-700 text-gray-300 hover:text-purple-400 hover:border-purple-400 transition rounded"
            title="Materialize (Export .STL)"
          >
            <Box size={18} />
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
                onClick={() => handleStepSelect(step.step)}
                className={`py-2 px-1 text-[10px] font-mono border rounded transition-all duration-300 flex flex-col items-center justify-center
                            ${params.activeStep === step.step
                    ? 'bg-cyan-900/40 border-cyan-400 text-cyan-300 shadow-[0_0_10px_rgba(34,211,238,0.2)]'
                    : 'bg-gray-900/50 border-gray-800 text-gray-500 hover:border-gray-600 hover:text-gray-300'
                  }`}
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
              value={params.distortion}
              onChange={(e) => setParams({ ...params, distortion: parseFloat(e.target.value) })}
              className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-pink-500"
            />
          </div>
        </div>

        {/* Mode Toggles */}
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setMode(ViewMode.FIELD)}
            className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.FIELD ? 'bg-indigo-900/30 border-indigo-500 text-indigo-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'}`}
          >
            <Cpu size={12} /> FIELD
          </button>
          <button
            onClick={() => setMode(ViewMode.SOLID)}
            className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.SOLID ? 'bg-purple-900/30 border-purple-500 text-purple-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'}`}
          >
            <Box size={12} /> SOLID
          </button>
          <button
            onClick={() => setMode(ViewMode.CRYSTAL)}
            className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.CRYSTAL ? 'bg-teal-900/30 border-teal-500 text-teal-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'}`}
          >
            <Layers size={12} /> MESH
          </button>
          <button
            onClick={() => setMode(ViewMode.ECHO)}
            className={`flex-1 py-2 px-2 text-[10px] font-mono border rounded flex items-center justify-center gap-1 transition ${mode === ViewMode.ECHO ? 'bg-cyan-900/30 border-cyan-500 text-cyan-400' : 'border-gray-700 text-gray-400 hover:border-gray-500'}`}
          >
            <RefreshCw size={12} /> ECHO
          </button>
        </div>

        {/* Fracture Toggle */}
        <button
          onClick={() => setParams({ ...params, fracture: !params.fracture })}
          className={`w-full py-2 mb-2 text-xs font-mono border rounded flex items-center justify-center gap-2 transition ${params.fracture ? 'bg-orange-900/40 border-orange-500 text-orange-400 animate-pulse' : 'border-gray-700 text-gray-400'}`}
        >
          <Zap size={14} /> {params.fracture ? 'FRACTURE SYNTHESIS ACTIVE' : 'ENABLE FRACTURE SYNTHESIS'}
        </button>

        {/* Prime Intrusion Toggle */}
        <button
          onClick={() => {
            const newMode = params.harmonicMode === 'fracture' ? 'smooth' : 'fracture';
            setParams({
              ...params,
              harmonicMode: newMode,
              interferenceB: newMode === 'fracture' ? Math.sqrt(51) : Math.sqrt(48),
              fracture: newMode === 'fracture' // Auto-enable/disable cracks based on mode preference? Or keep independent?
              // Let's keep cracks visible for fracture mode as per prompt "Teeth of Stones become visible"
            });
          }}
          className={`w-full py-2 mb-4 text-xs font-mono border rounded flex items-center justify-center gap-2 transition ${params.harmonicMode === 'fracture' ? 'bg-red-900/40 border-red-500 text-red-400' : 'bg-blue-900/30 border-blue-500 text-blue-300'}`}
        >
          <Layers size={14} /> {params.harmonicMode === 'fracture' ? 'PRIME INTRUSION (√51)' : 'HARMONIC SMOOTH (√48)'}
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

    </div>
  );
};