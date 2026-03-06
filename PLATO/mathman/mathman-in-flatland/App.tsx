
import React, { useState, useRef } from 'react';
import Visualizer, { VisualizerHandle } from './components/Visualizer';
import Controls from './components/Controls';
import ExplainerModal from './components/ExplainerModal';
import { WaveParams, LayerVisibility, ViewState } from './types';
import { DEFAULT_WAVE_PARAMS, DEFAULT_LAYERS, DEFAULT_VIEW } from './constants';

const App: React.FC = () => {
  const [params, setParams] = useState<WaveParams>(DEFAULT_WAVE_PARAMS);
  const [layers, setLayers] = useState<LayerVisibility>(DEFAULT_LAYERS);
  const [view, setView] = useState<ViewState>(DEFAULT_VIEW);
  const [stats, setStats] = useState<string>("");
  const [showExplainer, setShowExplainer] = useState<boolean>(false);
  
  const visualizerRef = useRef<VisualizerHandle>(null);

  const handleSnapshot = () => {
      visualizerRef.current?.takeSnapshot();
  };

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden text-gray-200">
      {/* Background Visualizer */}
      <Visualizer 
        ref={visualizerRef}
        params={params} 
        layers={layers} 
        view={view} 
        setStats={setStats}
        setView={setView}
      />

      {/* Main UI Overlay */}
      <Controls 
        params={params} 
        setParams={setParams} 
        layers={layers} 
        setLayers={setLayers}
        view={view}
        setView={setView}
        onSnapshot={handleSnapshot}
        onOpenExplainer={() => setShowExplainer(true)}
      />

      {/* Theory Guide Modal */}
      {showExplainer && (
        <ExplainerModal onClose={() => setShowExplainer(false)} />
      )}

      {/* Top Bar Stats */}
      <div className="absolute top-0 right-0 p-4 z-20 pointer-events-none">
        <div className="bg-black/40 backdrop-blur border border-gray-800 rounded px-3 py-1">
            <span className="text-xs font-mono text-cyan-500">{stats}</span>
        </div>
      </div>
      
      {/* Bottom Right Attribution */}
      <div className="absolute bottom-4 right-4 z-10 text-[10px] text-gray-600 font-mono text-right pointer-events-none opacity-60">
        <p>√42 RESONANT SPHERE LAB</p>
        <p>HIGH-PRECISION WAVE MECHANICS ENGINE</p>
        <p>SEE CITATIONS.MD FOR REFERENCES</p>
      </div>
    </div>
  );
};

export default App;
