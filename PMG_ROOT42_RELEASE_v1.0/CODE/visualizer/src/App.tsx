import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SoftCreature } from './components/SoftCreature';
import { PivotValidator } from './components/PivotValidator';
import { EscapeShader } from './components/EscapeShader';
import { Geofont13Shader } from './components/Geofont13Shader';
import { HiddenSevenShader } from './components/HiddenSevenShader';
import { GraceTimerShader } from './components/GraceTimerShader';
import { CityGenerator } from './components/CityGenerator';
import { SensoryDashboard } from './components/SensoryDashboard';
import { audioEngine } from './audioEngine';

function App() {
  const [viewMode, setViewMode] = useState<'resonance' | 'circular-limit' | 'city-press' | 'stabilisated-cone' | 'nautilus-prime' | 'escape-shader' | 'geofont-13' | 'hidden-seven' | 'grace-timer'>('resonance');
  const [time, setTime] = useState(0);

  // Global event bridge: Audio -> Geometry
  useEffect(() => {
    audioEngine.onLetterPlay = (letter, freq) => {
      window.dispatchEvent(new CustomEvent('lattice:letter', {
        detail: {
          nodeIndex: letter.charCodeAt(0) - 65, // A=0, B=1...
          letter,
          freq,
          timestamp: Date.now()
        }
      }));
    };
  }, []);

  // Global simulation clock
  useEffect(() => {
    let animationFrame: number;
    const start = Date.now();

    const update = () => {
      setTime((Date.now() - start) / 1000);
      animationFrame = requestAnimationFrame(update);
    };

    update();
    return () => cancelAnimationFrame(animationFrame);
  }, []);

  const navItems = [
    { id: 'resonance', label: 'Resonance' },
    { id: 'city-press', label: 'City Press' },
    { id: 'escape-shader', label: 'Escape' },
    { id: 'geofont-13', label: 'Geofont 13' },
    { id: 'hidden-seven', label: 'Hidden 7' },
    { id: 'grace-timer', label: 'Grace Timer' }
  ];

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden text-white font-sans">
      {/* Background Layer: 93-Point Shell or Shaders */}
      <div className="absolute inset-0 z-0">
        <AnimatePresence mode="wait">
          {viewMode === 'resonance' && (
            <motion.div
              key="resonance"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full h-full"
            >
              <SoftCreature />
            </motion.div>
          )}

          {viewMode === 'city-press' && (
            <motion.div
              key="city"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full h-full"
            >
              <CityGenerator />
            </motion.div>
          )}

          {viewMode === 'escape-shader' && (
            <motion.div
              key="escape"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full h-full"
            >
              <EscapeShader time={time} />
            </motion.div>
          )}

          {viewMode === 'geofont-13' && (
            <motion.div
              key="geofont"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full h-full"
            >
              <Geofont13Shader time={time} />
            </motion.div>
          )}

          {viewMode === 'hidden-seven' && (
            <motion.div
              key="hidden7"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full h-full"
            >
              <HiddenSevenShader time={time} tension={0.42} />
            </motion.div>
          )}

          {viewMode === 'grace-timer' && (
            <motion.div
              key="grace"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full h-full"
            >
              <GraceTimerShader time={time} vitrification={1.0} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Foreground UI Layer */}
      <div className="relative z-10 w-full h-full pointer-events-none p-6 flex flex-col justify-between">
        {/* Header */}
        <header className="flex justify-between items-start">
          <div className="pointer-events-auto">
            <h1 className="text-2xl font-bold tracking-tighter text-rose-500 uppercase">
              Sovereign Engine <span className="text-zinc-500 font-mono text-xs ml-2">v1.0.0</span>
            </h1>
            <p className="text-zinc-400 text-[10px] uppercase tracking-[0.2em] mt-1">
              93-Node Hyperdiamond Shell | √42 Invariant
            </p>
          </div>

          <div className="pointer-events-auto">
            <PivotValidator />
          </div>
        </header>

        <SensoryDashboard time={time} />

        {/* Navigation Footer */}
        <footer className="flex justify-center pb-8 sticky bottom-8">
          <nav className="flex gap-2 bg-zinc-900/80 backdrop-blur-md p-1.5 rounded-full border border-zinc-800 pointer-events-auto">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setViewMode(item.id as any)}
                className={`px-4 py-1.5 rounded-full text-[10px] uppercase font-bold tracking-widest transition-all ${viewMode === item.id
                  ? 'bg-rose-500 text-white shadow-lg'
                  : 'text-zinc-500 hover:text-white hover:bg-zinc-800'
                  }`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </footer>
      </div>

      {/* Global Aesthetics */}
      <div className="absolute inset-0 pointer-events-none border-[24px] border-black z-20" />
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_center,_transparent_0%,_black_95%)] opacity-30 z-20" />
    </div>
  );
}

export default App;
