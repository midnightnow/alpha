import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Eye,
  Box,
  ShieldCheck,
  Compass,
  Info,
  Activity,
  Zap,
  Play,
  Waves,
  Layers
} from 'lucide-react';

// Premium Components
import { Lattice93 } from './components/Lattice93';
import { CameraObscura } from './components/CameraObscura';
import { WaveInterference } from './components/WaveInterference';
import { MathmanLab } from './components/MathmanLab';
import { AxiomSpiral24 } from './components/AxiomSpiral24';
import { RadicalResonance } from './components/RadicalResonance';
import { CityGenerator } from './components/CityGenerator';
import { NautilusPrime } from './components/NautilusPrime';

// HUD Components
import { VerseHUD } from './components/VerseHUD';
import { SensoryDashboard } from './components/SensoryDashboard';
import { RomanRoad } from './components/RomanRoad';
import { PivotValidator } from './components/PivotValidator';
import { ErrorBoundary } from './components/ErrorBoundary';

import { audioEngine } from './audioEngine';

type Section = 'foundations' | 'lattice' | 'rose' | 'press' | 'nautilus' | 'obscura' | 'eye' | 'resonance';

function App() {
  const [activeSection, setActiveSection] = useState<Section>('foundations');
  const [visualMode, setVisualMode] = useState<'SQUARE' | 'HEX'>('SQUARE');
  const [time, setTime] = useState(0);
  const [isStarted, setIsStarted] = useState(false);

  // Precessional Clock
  useEffect(() => {
    const updateClock = () => {
      const hours = new Date().getHours();
      setVisualMode(hours >= 6 && hours < 22 ? 'SQUARE' : 'HEX');
    };
    updateClock();
    const interval = setInterval(updateClock, 60000);
    return () => clearInterval(interval);
  }, []);

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

  const sections = [
    { id: 'foundations', label: 'Foundations', icon: ShieldCheck },
    { id: 'lattice', label: '93-Faced Solid', icon: Box },
    { id: 'rose', label: 'Pyramid Rose', icon: Zap },
    { id: 'press', label: 'City Press', icon: Layers },
    { id: 'nautilus', label: 'Nautilus Prime', icon: Waves },
    { id: 'obscura', label: 'Camera Obscura', icon: Compass },
    { id: 'eye', label: 'Trivavled Eye', icon: Eye },
    { id: 'resonance', label: 'Resonance', icon: Activity },
  ];

  const handleStart = () => {
    audioEngine.init().then(() => {
      audioEngine.play();
      setIsStarted(true);
    });
  };

  if (!isStarted) {
    return (
      <div className="fixed inset-0 z-[100] bg-black flex flex-col items-center justify-center font-sans p-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center space-y-8 max-w-lg"
        >
          <div className="space-y-2">
            <h1 className="text-4xl font-black italic tracking-tighter text-white uppercase">
              Sovereign <span className="text-rose-500">Engine</span>
            </h1>
            <p className="text-zinc-500 text-xs uppercase tracking-[0.5em] font-mono">
              v2.0 // Principia Mathematica Geometrica
            </p>
          </div>

          <div className="p-8 bg-zinc-900/50 border border-white/10 rounded-2xl space-y-4">
            <p className="text-zinc-400 text-sm font-serif italic leading-relaxed">
              "The Hand doesn't judge the ink. It only follows the e. And e says that the Crab, the Spider, the Human, the Pyramid, the Icosahedron, and the Star are all just different ways to fold the same 1-sided gon."
            </p>
          </div>

          <button
            onClick={handleStart}
            className="group relative px-12 py-4 bg-white text-black font-black uppercase text-sm tracking-widest hover:bg-rose-500 hover:text-white transition-all overflow-hidden"
          >
            <span className="relative z-10">Vitrify System</span>
            <motion.div
              className="absolute inset-0 bg-rose-500 translate-x-[-100%]"
              whileHover={{ translateX: 0 }}
            />
          </button>
        </motion.div>

        <footer className="fixed bottom-8 font-mono text-[8px] uppercase tracking-[0.3em] text-zinc-600">
          ROOT-42 ENCLOSURE AXIOM // ZERO HYSTERESIS ACHIEVED
        </footer>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${activeSection === 'nautilus' ? 'bg-[#f4ecd8]' : 'bg-[#E4E3E0]'} text-[#141414] font-sans selection:bg-[#F27D26] selection:text-white overflow-hidden transition-colors duration-1000`}>
      {/* Navigation Rail */}
      <nav className="fixed top-0 left-0 h-full w-20 bg-[#141414] flex flex-col items-center py-8 z-50 border-r border-white/10 shadow-2xl">
        <div className="mb-12">
          <div className="w-10 h-10 rounded-full bg-[#F27D26] flex items-center justify-center text-white font-serif italic text-xl shadow-lg">
            P
          </div>
        </div>

        <div className="flex-1 flex flex-col gap-6">
          {sections.map((s) => (
            <button
              key={s.id}
              onClick={() => setActiveSection(s.id as Section)}
              className={`p-4 rounded-2xl transition-all duration-300 group relative ${activeSection === s.id ? "bg-[#F27D26] text-white shadow-xl scale-110" : "text-white/40 hover:text-white hover:bg-white/5"}`}
              title={s.label}
            >
              <s.icon size={20} />
              <span className="absolute left-full ml-4 px-2 py-1 bg-[#141414] text-white text-[10px] uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap rounded border border-white/10 z-[60]">
                {s.label}
              </span>
            </button>
          ))}
        </div>

        <div className="mt-auto">
          <button className="text-white/20 hover:text-white transition-colors p-4">
            <Info size={20} />
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pl-20 min-h-screen relative">
        <header className={`p-8 md:p-12 border-b border-[#141414]/10 flex justify-between items-end ${activeSection === 'nautilus' ? 'bg-[#f4ecd8]/80' : 'bg-white/50'} backdrop-blur-md sticky top-0 z-40 transition-colors duration-1000`}>
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="font-mono text-[10px] uppercase tracking-[0.3em] opacity-40">Principia Mathematica Geometrica</span>
              <div className="h-px w-12 bg-[#141414]/20" />
            </div>
            <h1 className="text-4xl md:text-5xl font-serif italic tracking-tight">
              {sections.find(s => s.id === activeSection)?.label} <span className="not-italic opacity-20">/</span> Protocol
            </h1>
          </div>
          <div className="text-right pointer-events-none">
            <ErrorBoundary>
              <PivotValidator visualMode={visualMode} />
            </ErrorBoundary>
          </div>
        </header>

        <div className="w-full h-[calc(100vh-140px)] overflow-hidden">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.5, ease: [0.23, 1, 0.32, 1] }}
              className="w-full h-full"
            >
              <ErrorBoundary>
                {activeSection === 'foundations' && <MathmanLab />}
                {activeSection === 'lattice' && <Lattice93 />}
                {activeSection === 'rose' && <AxiomSpiral24 />}
                {activeSection === 'press' && <CityGenerator t={93} time={time} zoomLevel={1} />}
                {activeSection === 'nautilus' && <NautilusPrime />}
                {activeSection === 'obscura' && <CameraObscura />}
                {activeSection === 'eye' && <WaveInterference />}
                {activeSection === 'resonance' && <RadicalResonance />}
              </ErrorBoundary>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Global HUD Layers */}
        <ErrorBoundary>
          {activeSection !== 'nautilus' && (
            <>
              <VerseHUD />
              <SensoryDashboard time={time} />
            </>
          )}
          <RomanRoad visualMode={visualMode} />
        </ErrorBoundary>
      </main>

      <footer className="fixed bottom-0 right-0 p-6 font-mono text-[9px] uppercase tracking-[0.3em] opacity-30 pointer-events-none z-50">
        PMG_SYSTEM_ACTIVE // BUILD_42_51 // Σ=4
      </footer>
    </div>
  );
}

export default App;
