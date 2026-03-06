
import React from 'react';
import { WaveParams, LayerVisibility, ViewState } from '../types';
import { ANATOMICAL_LEVELS, SQRT_42, SQRT_51 } from '../constants';
import { downloadResearchPackage, downloadComparativeDataset } from '../utils/exportSystem';
import { RESEARCH_PRESETS } from '../utils/researchPresets';
import { Settings, Eye, Activity, Layers, Maximize, RotateCw, Box, Download, FileText, Database, FileJson, Camera, Bookmark, HelpCircle, Microscope, ArrowUpCircle } from 'lucide-react';

interface ControlsProps {
  params: WaveParams;
  setParams: React.Dispatch<React.SetStateAction<WaveParams>>;
  layers: LayerVisibility;
  setLayers: React.Dispatch<React.SetStateAction<LayerVisibility>>;
  view: ViewState;
  setView: React.Dispatch<React.SetStateAction<ViewState>>;
  onSnapshot: () => void;
  onOpenExplainer: () => void;
}

const Slider = ({ label, value, min, max, step, onChange, unit = "" }: any) => {
  const displayValue = step >= 1 && value % 1 === 0 ? value.toFixed(0) : value.toFixed(2);
  return (
    <div className="mb-3">
      <div className="flex justify-between text-xs text-gray-400 mb-1">
        <span>{label}</span>
        <span className="font-mono text-cyan-500">{displayValue}{unit}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-1 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-cyan-600 hover:accent-cyan-500"
      />
    </div>
  );
};

const Toggle = ({ label, active, onClick }: any) => (
  <button
    onClick={onClick}
    className={`px-3 py-1 text-xs rounded border transition-colors mr-2 mb-2 ${
      active 
        ? 'bg-cyan-900/40 border-cyan-500/50 text-cyan-100' 
        : 'bg-gray-900/40 border-gray-700 text-gray-500 hover:border-gray-500'
    }`}
  >
    {label}
  </button>
);

const Controls: React.FC<ControlsProps> = ({ params, setParams, layers, setLayers, view, setView, onSnapshot, onOpenExplainer }) => {
  const updateParam = (key: keyof WaveParams, val: number | boolean) => {
    setParams(p => ({ ...p, [key]: val }));
  };

  const toggleLayer = (key: keyof LayerVisibility) => {
    setLayers(l => ({ ...l, [key]: !l[key] }));
  };
  
  const updateView = (key: keyof ViewState, val: any) => {
    setView(v => ({ ...v, [key]: val }));
  };

  const loadPreset = (presetId: string) => {
      const preset = RESEARCH_PRESETS.find(p => p.id === presetId);
      if (preset) {
        setParams(prev => ({ ...prev, ...preset.parameters }));
        if (preset.view) {
          setView(prev => ({ ...prev, ...preset.view }));
        }
      }
  };

  const activateStudyMode = () => {
      setLayers({
        foundation: true,
        vitruvian: true,
        annotations: true,
        hexagonalLattice: false,
        earthMoon: false,
        triangleGeometry: false,
        heptagonalGrid: false,
        primeModuloGrid: false,
        platonic: false,
        sephiroticGraph: false,
        harmonicSpine: false,
        starTetrahedron: false,
        haricLevel: false,
        coreStarLevel: false,
      });
  };

  const setElevation = (mode: 'material' | 'etheric') => {
      if (mode === 'material') {
          updateParam('geometryScale', SQRT_42);
          updateParam('scanHeight', 4.2); // Snap to resonance
      } else {
          updateParam('geometryScale', SQRT_51);
          updateParam('scanHeight', 4.8); // Snap to resonance
      }
  };

  const currentElevation = Math.abs(params.geometryScale - SQRT_51) < 0.1 ? 'etheric' : 
                           Math.abs(params.geometryScale - SQRT_42) < 0.1 ? 'material' : 'custom';

  return (
    <div className="absolute top-4 left-4 bottom-4 w-80 bg-black/80 backdrop-blur-md border-r border-gray-800 p-4 overflow-y-auto rounded-xl shadow-2xl z-10 border border-gray-800/50 scrollbar-thin scrollbar-thumb-gray-700">
      
      <div className="flex items-center justify-between mb-6 border-b border-gray-800 pb-4">
        <div className="flex items-center gap-2">
            <Activity className="text-cyan-500" size={20} />
            <h1 className="font-bold text-lg tracking-wider text-gray-200">MATHMAN<span className="text-xs ml-1 font-normal text-gray-500">LAB</span></h1>
        </div>
        <div className="flex gap-2">
            <button onClick={onOpenExplainer} className="p-2 bg-gray-900 hover:bg-cyan-900/30 text-gray-400 hover:text-cyan-400 rounded-full transition-colors" title="Lab Manual"><HelpCircle size={18} /></button>
            <button onClick={onSnapshot} className="p-2 bg-gray-900 hover:bg-cyan-900/30 text-gray-400 hover:text-cyan-400 rounded-full transition-colors" title="Take Snapshot"><Camera size={18} /></button>
        </div>
      </div>

      <div className="mb-6">
        <h2 className="text-xs font-bold text-gray-500 uppercase mb-3 flex items-center gap-2"><Bookmark size={12} /> Research Protocols</h2>
        <div className="grid grid-cols-1 gap-2">
            {RESEARCH_PRESETS.map(preset => (
                <button
                    key={preset.id}
                    onClick={() => loadPreset(preset.id)}
                    className="px-3 py-2 text-[10px] bg-gray-900 border border-gray-700 hover:border-cyan-600 rounded text-gray-300 transition-all text-left flex justify-between items-center group"
                >
                    <span className="font-bold text-gray-200 group-hover:text-white">{preset.name}</span>
                    <span className="text-[9px] text-gray-500 italic">
                      {preset.id.includes('42') ? 'Substantiation' : preset.id.includes('51') ? 'Experimental' : ''}
                    </span>
                </button>
            ))}
        </div>
      </div>

      <div className="mb-6 border-t border-gray-800 pt-4">
         <h2 className="text-xs font-bold text-gray-500 uppercase mb-3 flex items-center gap-2"><ArrowUpCircle size={12} /> Dimensional Elevation</h2>
        <div className="flex gap-2">
            <button
                onClick={() => setElevation('material')}
                className={`flex-1 py-2 rounded text-[10px] border transition-all ${currentElevation === 'material' ? 'bg-cyan-900/40 border-cyan-500 text-cyan-200' : 'bg-gray-900 border-gray-700 text-gray-500'}`}
            >
                <div className="font-bold">√42 Material</div>
                <div className="text-[9px] opacity-70">Scale: {SQRT_42.toFixed(3)}</div>
            </button>
            <button
                onClick={() => setElevation('etheric')}
                className={`flex-1 py-2 rounded text-[10px] border transition-all ${currentElevation === 'etheric' ? 'bg-indigo-900/30 border-indigo-500 text-indigo-200' : 'bg-gray-900 border-gray-700 text-gray-500'}`}
            >
                <div className="font-bold">√51 Etheric</div>
                <div className="text-[9px] opacity-70">Scale: {SQRT_51.toFixed(3)}</div>
            </button>
        </div>
      </div>

      <div className="mb-6">
         <button onClick={activateStudyMode} className="w-full py-2 bg-indigo-900/30 border border-indigo-500/50 rounded hover:bg-indigo-900/50 hover:border-indigo-400 transition-all flex items-center justify-center gap-2 text-indigo-300 text-xs font-bold">
             <Microscope size={14} /> ENTER STUDY MODE
         </button>
      </div>

      <div className="mb-6">
        <h2 className="text-xs font-bold text-gray-500 uppercase mb-3 flex items-center gap-2"><Maximize size={12} /> Geometry</h2>
        <Slider label="Origin A-B Sep" value={params.originSeparation} min={0} max={70} step={0.1} unit="mm" onChange={(v: number) => updateParam('originSeparation', v)} />
        <Slider label="Origin C Offset" value={params.originCOffset} min={-30} max={50} step={0.1} unit="mm" onChange={(v: number) => updateParam('originCOffset', v)} />
        <Slider label="Geo Scale (X)" value={params.geometryScale} min={1} max={8} step={0.01} onChange={(v: number) => updateParam('geometryScale', v)} />
        <Slider label="Nesting Depth" value={params.nestingDepth} min={1} max={8} step={1} onChange={(v: number) => updateParam('nestingDepth', v)} />
      </div>

      <div className="mb-6">
        <h2 className="text-xs font-bold text-gray-500 uppercase mb-3">Scan Plane (Chakra)</h2>
        <div className="flex flex-wrap gap-1 mb-2">
            {ANATOMICAL_LEVELS.map(c => (
                <button
                    key={c.id}
                    onClick={() => updateParam('scanHeight', c.y)}
                    className={`text-[10px] px-2 py-1 border rounded flex-grow text-center transition-all ${Math.abs(params.scanHeight - c.y) < 0.1 ? 'bg-amber-900/40 border-amber-600 text-amber-200' : 'border-gray-800 text-gray-500 hover:bg-gray-800 hover:text-gray-300'}`}
                >
                    {c.name}
                </button>
            ))}
        </div>
        <Slider label="Manual Scan Y" value={params.scanHeight} min={-2} max={12} step={0.1} unit="mm" onChange={(v: number) => updateParam('scanHeight', v)} />
      </div>

      <div className="mb-6">
        <h2 className="text-xs font-bold text-gray-500 uppercase mb-3 flex items-center gap-2"><Settings size={12} /> Physics</h2>
        <Slider label="Wavelength (λ)" value={params.wavelength} min={0.1} max={5.0} step={0.1} unit="mm" onChange={(v: number) => updateParam('wavelength', v)} />
        <Slider label="Intensity Threshold" value={params.intensityThreshold} min={0} max={0.95} step={0.01} onChange={(v: number) => updateParam('intensityThreshold', v)} />
        <Slider label="Brightness" value={params.waveBrightness} min={0} max={1} step={0.01} onChange={(v: number) => updateParam('waveBrightness', v)} />
        <Slider label="Nodal Budget" value={params.nodalBudget} min={100} max={5000} step={100} onChange={(v: number) => updateParam('nodalBudget', v)} />
      </div>

      <div className="mb-6">
        <h2 className="text-xs font-bold text-gray-500 uppercase mb-3 flex items-center gap-2"><Eye size={12} /> View Controls</h2>
        <div className="flex justify-between mb-2 text-[10px] text-gray-500">
            <span>Rot: {view.rotation.toFixed(0)}°</span>
            <span>Pitch: {view.pitch.toFixed(0)}°</span>
        </div>
        <Slider label="Zoom" value={view.zoom} min={0.1} max={5} step={0.1} onChange={(v: number) => updateView('zoom', v)} />
        <Slider label="Node Size" value={params.nodeSize} min={0.1} max={3.0} step={0.1} onChange={(v: number) => updateParam('nodeSize', v)} />
        <div className="flex flex-wrap mt-2">
           <Toggle label="Mirror" active={view.mirror} onClick={() => updateView('mirror', !view.mirror)} />
           <Toggle label="Pulse" active={view.primePulse} onClick={() => updateView('primePulse', !view.primePulse)} />
           <Toggle label="Mandala (4x)" active={view.quaternion} onClick={() => updateView('quaternion', !view.quaternion)} />
           <Toggle label="Snap 22.5°" active={view.resonanceLock} onClick={() => updateView('resonanceLock', !view.resonanceLock)} />
           <button onClick={() => setView(v => ({ ...v, rotation: 0, pitch: 0, panX: 0, panY: 0 }))} className="px-3 py-1 text-xs rounded border border-gray-700 text-gray-500 hover:border-gray-500 hover:text-gray-300 transition-colors mr-2 mb-2">Reset Cam</button>
        </div>
      </div>

      <div className="mb-6">
        <h2 className="text-xs font-bold text-gray-500 uppercase mb-3 flex items-center gap-2"><Layers size={12} /> Dimensional Layers</h2>
        <div className="flex flex-wrap gap-1">
            <Toggle label="Haric (Intention)" active={layers.haricLevel} onClick={() => toggleLayer('haricLevel')} />
            <Toggle label="Core Star (Essence)" active={layers.coreStarLevel} onClick={() => toggleLayer('coreStarLevel')} />
            <Toggle label="Vitruvian (Body)" active={layers.foundation} onClick={() => toggleLayer('foundation')} />
            <div className="w-full h-px bg-gray-800 my-1"></div>
            <Toggle label="Hex Lattice" active={layers.hexagonalLattice} onClick={() => toggleLayer('hexagonalLattice')} />
            <Toggle label="Earth/Moon" active={layers.earthMoon} onClick={() => toggleLayer('earthMoon')} />
            <Toggle label="Platonic" active={layers.platonic} onClick={() => toggleLayer('platonic')} />
            <Toggle label="Mod 24 Grid" active={layers.primeModuloGrid} onClick={() => toggleLayer('primeModuloGrid')} />
            <Toggle label="Harmonic Spine" active={layers.harmonicSpine} onClick={() => toggleLayer('harmonicSpine')} />
            <Toggle label="Labels" active={layers.annotations} onClick={() => toggleLayer('annotations')} />
        </div>
      </div>

      <div className="mb-4 pt-4 border-t border-gray-800">
        <h2 className="text-xs font-bold text-gray-500 uppercase mb-3 flex items-center gap-2"><Download size={12} /> Research Export</h2>
        <div className="grid grid-cols-2 gap-2">
            <button onClick={() => downloadResearchPackage(params, 'csv')} className="flex flex-col items-center justify-center p-2 rounded bg-gray-900 border border-gray-700 hover:border-cyan-500 hover:text-cyan-400 transition-all group">
                <FileText size={16} className="text-gray-400 mb-1 group-hover:text-cyan-500" /><span className="text-[10px] text-gray-300">CSV</span>
            </button>
            <button onClick={() => downloadResearchPackage(params, 'json-ld')} className="flex flex-col items-center justify-center p-2 rounded bg-gray-900 border border-gray-700 hover:border-cyan-500 hover:text-cyan-400 transition-all group">
                <Database size={16} className="text-gray-400 mb-1 group-hover:text-cyan-500" /><span className="text-[10px] text-gray-300">JSON-LD</span>
            </button>
             <button onClick={() => downloadResearchPackage(params, 'json')} className="flex flex-col items-center justify-center p-2 rounded bg-gray-900 border border-gray-700 hover:border-cyan-500 hover:text-cyan-400 transition-all group">
                <FileJson size={16} className="text-gray-400 mb-1 group-hover:text-cyan-500" /><span className="text-[10px] text-gray-300">Package</span>
            </button>
            <button onClick={() => downloadComparativeDataset()} className="flex flex-col items-center justify-center p-2 rounded bg-indigo-900/30 border border-indigo-700 hover:border-indigo-400 hover:text-indigo-300 transition-all group">
                <ArrowUpCircle size={16} className="text-indigo-400 mb-1 group-hover:text-indigo-200" /><span className="text-[10px] text-indigo-300 text-center leading-tight">Decryption Study</span>
            </button>
        </div>
      </div>

    </div>
  );
};

export default Controls;
