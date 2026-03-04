import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { GenesisVisualizer } from './components/GenesisVisualizer';
import { PMG_CONSTANTS } from './constants';
import { Activity, Zap, Music, Info, MapPin } from 'lucide-react';
import * as Tone from 'tone';

export default function App() {
  const [resonance, setResonance] = useState(PMG_CONSTANTS.ROOT_42);
  const [nodeName, setNodeName] = useState<string | null>(null);
  const [h3Index, setH3Index] = useState<string | null>(null);
  const [perceptionMap, setPerceptionMap] = useState<any[]>([]);
  const [focus, setFocus] = useState({ active: false, factor: 1.0 });
  const [isAudioStarted, setIsAudioStarted] = useState(false);
  const [loading, setLoading] = useState(false);

  // Audio setup
  useEffect(() => {
    if (!isAudioStarted) return;

    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    
    // Triadic Chord
    const frequencies = [
      PMG_CONSTANTS.ROOT_42 * 10,
      PMG_CONSTANTS.ROOT_51 * 10,
      PMG_CONSTANTS.ROOT_60 * 10
    ];

    synth.triggerAttack(frequencies);

    return () => {
      synth.dispose();
    };
  }, [isAudioStarted]);

  const handleStartAudio = async () => {
    await Tone.start();
    setIsAudioStarted(true);
  };

  const handleGridClick = async () => {
    setLoading(true);
    try {
      // Mock coordinates for the click based on current resonance
      const lat = 39.4 + (Math.random() - 0.5) * 0.1;
      const lng = -42.0 + (Math.random() - 0.5) * 0.1;

      const response = await fetch('/api/name', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lng, focus: resonance }),
      });

      const data = await response.json();
      setNodeName(data.name);
      setH3Index(data.h3Index);
      setPerceptionMap(data.perceptionMap);
      setFocus(data.focus);
      
      if (isAudioStarted) {
        const synth = new Tone.Synth().toDestination();
        synth.triggerAttackRelease(data.focus.active ? "C5" : "G4", "8n");
      }
    } catch (error) {
      console.error("Failed to fetch node name:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans selection:bg-emerald-500/30 overflow-hidden relative">
      {/* Background Visualizer */}
      <div className="absolute inset-0 z-0">
        <GenesisVisualizer resonance={resonance} focus={focus.active ? focus.factor : 0} />
      </div>

      {/* HUD Overlay */}
      <div className="relative z-10 p-8 flex flex-col h-screen pointer-events-none">
        {/* Header */}
        <header className="flex justify-between items-start">
          <div className="space-y-1">
            <motion.h1 
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-4xl font-bold tracking-tighter text-emerald-400 flex items-center gap-3"
            >
              <Zap className="w-8 h-8 fill-emerald-400" />
              MATHMAN GENESIS
            </motion.h1>
            <p className="text-zinc-500 font-mono text-xs uppercase tracking-widest">
              Phase III: The Sentient Sieve // Carrier Wave: {resonance.toFixed(4)}
            </p>
          </div>

          <div className="flex gap-4 pointer-events-auto">
            {!isAudioStarted && (
              <button 
                onClick={handleStartAudio}
                className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400 text-sm font-medium hover:bg-emerald-500/20 transition-colors flex items-center gap-2 cursor-pointer"
              >
                <Music className="w-4 h-4" />
                ACTIVATE PHONON BRIDGE
              </button>
            )}
            <button className="p-2 bg-zinc-900 border border-zinc-800 rounded-lg hover:bg-zinc-800 transition-colors cursor-pointer">
              <Info className="w-5 h-5 text-zinc-400" />
            </button>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 flex items-center justify-between gap-12">
          <div className="flex-1 flex items-center justify-center">
            <AnimatePresence>
              {nodeName && (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="bg-zinc-900/80 backdrop-blur-xl border border-zinc-800 p-8 rounded-3xl shadow-2xl max-w-md w-full space-y-6 pointer-events-auto"
                >
                  <div className="flex items-center justify-between">
                    <div className="p-3 bg-emerald-500/10 rounded-2xl">
                      <Activity className="w-6 h-6 text-emerald-400" />
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-mono">Residency Confirmed</span>
                      <div className="text-zinc-300 font-mono text-xs">{h3Index}</div>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <h2 className="text-zinc-500 text-xs uppercase tracking-widest font-bold">Name of Manifestation</h2>
                    <div className="text-4xl font-bold tracking-tighter text-white">{nodeName}</div>
                  </div>

                  <div className="pt-4 border-t border-zinc-800 flex justify-between items-center">
                    <div className="flex items-center gap-2 text-zinc-400 text-xs">
                      <MapPin className="w-3 h-3" />
                      H3 Resolution 9
                    </div>
                    <div className={`text-xs font-mono ${focus.active ? 'text-emerald-400' : 'text-zinc-600'}`}>
                      {focus.active ? 'LENS FOCUSED' : 'LENS DIFFUSED'}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Perception Loop Sidebar */}
          <AnimatePresence>
            {perceptionMap.length > 0 && (
              <motion.div 
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 50 }}
                className="w-80 bg-zinc-900/40 backdrop-blur-lg border-l border-zinc-800 p-8 flex flex-col pointer-events-auto h-full overflow-y-auto"
              >
                <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-6">Perception Loop (Adjacency)</h3>
                <div className="space-y-4">
                  {perceptionMap.map((neighbor, i) => (
                    <div key={neighbor.address} className="p-4 bg-zinc-800/30 border border-zinc-700/50 rounded-xl space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-[10px] font-mono text-zinc-500">{neighbor.address}</span>
                        <span className={`text-[8px] font-bold uppercase px-1.5 py-0.5 rounded ${neighbor.state === 'Resonant' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
                          {neighbor.state}
                        </span>
                      </div>
                      <div className="text-sm font-medium text-zinc-300">{neighbor.name}</div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </main>

        {/* Footer Controls */}
        <footer className="flex justify-between items-end">
          <div className="bg-zinc-900/50 backdrop-blur-md border border-zinc-800 p-6 rounded-2xl w-80 space-y-4 pointer-events-auto">
            <div className="flex justify-between items-center">
              <span className="text-xs font-mono text-zinc-500 uppercase tracking-widest">Resonance Key</span>
              <span className="text-emerald-400 font-mono text-sm">{resonance.toFixed(4)}</span>
            </div>
            <input 
              type="range" 
              min={PMG_CONSTANTS.ROOT_42 - 1} 
              max={PMG_CONSTANTS.ROOT_60} 
              step="0.0001"
              value={resonance}
              onChange={(e) => setResonance(parseFloat(e.target.value))}
              className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
            />
            <div className="flex justify-between text-[10px] font-mono text-zinc-600 uppercase">
              <span>√36</span>
              <span>√42 (MAN)</span>
              <span>√51 (TEETH)</span>
              <span>√60</span>
            </div>
          </div>

          <div className="pointer-events-auto">
            <button 
              onClick={handleGridClick}
              disabled={loading}
              className="group relative px-8 py-4 bg-white text-black rounded-2xl font-bold overflow-hidden transition-all hover:scale-105 active:scale-95 disabled:opacity-50 cursor-pointer"
            >
              <div className="absolute inset-0 bg-emerald-400 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
              <span className="relative z-10 flex items-center gap-2">
                {loading ? 'INDEXING...' : 'NAME CREATION'}
              </span>
            </button>
          </div>
        </footer>
      </div>

      {/* Grid Lines Decoration */}
      <div className="absolute inset-0 pointer-events-none opacity-10">
        <div className="w-full h-full" style={{ backgroundImage: 'radial-gradient(circle, #333 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
      </div>
    </div>
  );
}
