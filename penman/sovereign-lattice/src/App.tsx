import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Compass, 
  PenTool, 
  Grid3X3, 
  Activity, 
  Info,
  ChevronRight,
  Maximize2,
  Minimize2,
  Database,
  BookOpen,
  FileText,
  Triangle,
  Scroll
} from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { AXIOMS, type Axiom } from './types';
import AxiomPen from './components/AxiomPen';
import AxiomSpiral from './components/AxiomSpiral';
import AxiomVoronoi from './components/AxiomVoronoi';
import AxiomDivine from './components/AxiomDivine';
import AxiomHypotenuse from './components/AxiomHypotenuse';
import AxiomEnergy from './components/AxiomEnergy';
import AxiomCurvature from './components/AxiomCurvature';
import AxiomSonnetEngine from './components/AxiomSonnetEngine';
import AxiomSpiral24 from './components/AxiomSpiral24';
import ParableView from './components/ParableView';
import FormalPaper from './components/FormalPaper';
import Methodology from './components/Methodology';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

type Mode = 'visualizer' | 'parable' | 'paper' | 'methodology';

export default function App() {
  const [activeAxiom, setActiveAxiom] = useState<Axiom>(AXIOMS[0]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [mode, setMode] = useState<Mode>('visualizer');

  const renderVisualizer = () => {
    switch (activeAxiom.id) {
      case 'pen-physics':
        return <AxiomPen axiom={activeAxiom} />;
      case 'curvature-constraint':
      case 'curvature-derivation':
        return <AxiomCurvature axiom={activeAxiom} />;
      case 'log-spiral':
        return <AxiomSpiral axiom={activeAxiom} />;
      case 'voronoi-361':
        return <AxiomVoronoi axiom={activeAxiom} />;
      case 'divine-size':
        return <AxiomDivine axiom={activeAxiom} />;
      case 'hypotenuse-meaning':
        return <AxiomHypotenuse axiom={activeAxiom} />;
      case 'energy-derivation':
        return <AxiomEnergy axiom={activeAxiom} />;
      case 'sonnet-engine':
        return <AxiomSonnetEngine axiom={activeAxiom} />;
      case 'spiral-24':
        return <AxiomSpiral24 axiom={activeAxiom} />;
      default:
        return <div className="flex items-center justify-center h-full text-zinc-500">Select an Axiom</div>;
    }
  };

  const renderContent = () => {
    switch (mode) {
      case 'parable':
        return <ParableView />;
      case 'paper':
        return <FormalPaper />;
      case 'methodology':
        return <Methodology />;
      default:
        return renderVisualizer();
    }
  };

  return (
    <div className="flex h-screen bg-[#E4E3E0] text-[#141414] font-sans selection:bg-[#141414] selection:text-[#E4E3E0]">
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isSidebarOpen ? 320 : 64 }}
        className="relative border-r border-[#141414] flex flex-col bg-[#E4E3E0] z-20"
      >
        <div className="p-4 border-bottom border-[#141414] flex items-center justify-between">
          {isSidebarOpen && (
            <motion.h1 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="font-serif italic text-xl font-bold tracking-tight"
            >
              Sovereign Lattice
            </motion.h1>
          )}
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 hover:bg-[#141414] hover:text-[#E4E3E0] transition-colors rounded"
          >
            {isSidebarOpen ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
          </button>
        </div>

        {/* Mode Switcher */}
        <div className="px-2 py-4 flex flex-col gap-1 border-b border-[#141414]/10">
          <button
            onClick={() => setMode('visualizer')}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded transition-colors text-sm font-medium",
              mode === 'visualizer' ? "bg-[#141414] text-[#E4E3E0]" : "hover:bg-[#141414]/5"
            )}
          >
            <Activity size={16} />
            {isSidebarOpen && <span>Visualizer</span>}
          </button>
          <button
            onClick={() => setMode('parable')}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded transition-colors text-sm font-medium",
              mode === 'parable' ? "bg-[#141414] text-[#E4E3E0]" : "hover:bg-[#141414]/5"
            )}
          >
            <Scroll size={16} />
            {isSidebarOpen && <span>The Parable</span>}
          </button>
          <button
            onClick={() => setMode('paper')}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded transition-colors text-sm font-medium",
              mode === 'paper' ? "bg-[#141414] text-[#E4E3E0]" : "hover:bg-[#141414]/5"
            )}
          >
            <FileText size={16} />
            {isSidebarOpen && <span>Formal Paper</span>}
          </button>
          <button
            onClick={() => setMode('methodology')}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded transition-colors text-sm font-medium",
              mode === 'methodology' ? "bg-[#141414] text-[#E4E3E0]" : "hover:bg-[#141414]/5"
            )}
          >
            <Compass size={16} />
            {isSidebarOpen && <span>The Method</span>}
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-4">
          {isSidebarOpen && (
            <p className="px-4 text-[10px] font-mono opacity-50 uppercase tracking-widest mb-2">Axiomatic Foundations</p>
          )}
          {AXIOMS.map((axiom) => (
            <button
              key={axiom.id}
              onClick={() => {
                setActiveAxiom(axiom);
                setMode('visualizer');
              }}
              className={cn(
                "w-full text-left px-4 py-3 flex items-center gap-3 transition-all group relative",
                activeAxiom.id === axiom.id && mode === 'visualizer' ? "bg-[#141414] text-[#E4E3E0]" : "hover:bg-[#141414]/5"
              )}
            >
              <div className="flex-shrink-0">
                {axiom.id.includes('pen') && <PenTool size={18} />}
                {axiom.id.includes('curvature') && <Activity size={18} />}
                {axiom.id.includes('spiral') && <Compass size={18} />}
                {axiom.id.includes('voronoi') && <Grid3X3 size={18} />}
                {axiom.id.includes('divine') && <Database size={18} />}
                {axiom.id.includes('hypotenuse') && <Triangle size={18} />}
              </div>
              {isSidebarOpen && (
                <div className="flex-1 overflow-hidden">
                  <p className="text-xs font-mono opacity-50 uppercase tracking-widest mb-0.5">
                    {axiom.formula}
                  </p>
                  <p className="font-medium truncate">{axiom.title}</p>
                </div>
              )}
              {activeAxiom.id === axiom.id && mode === 'visualizer' && isSidebarOpen && (
                <ChevronRight size={16} className="opacity-50" />
              )}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-[#141414]">
          <div className="flex items-center gap-2 text-[10px] font-mono opacity-50 uppercase tracking-widest">
            <Info size={12} />
            <span>System Status: Stable</span>
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {/* Header */}
        <header className="h-16 border-b border-[#141414] flex items-center justify-between px-8 bg-[#E4E3E0]/80 backdrop-blur-sm z-10">
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono opacity-50 uppercase tracking-widest">
              {mode === 'visualizer' ? 'Axiom:' : mode === 'parable' ? 'Manuscript:' : 'Document:'}
            </span>
            <h2 className="font-serif italic text-lg">
              {mode === 'visualizer' ? activeAxiom.title : mode === 'parable' ? 'The Parable of Ember & Umber' : mode === 'paper' ? 'The Sovereign Lattice (Formal Paper)' : 'The Scribe of the Mother of Pearl'}
            </h2>
          </div>
          <div className="flex items-center gap-6">
            <div className="text-right">
              <p className="text-[10px] font-mono opacity-50 uppercase tracking-widest">Stability Constant</p>
              <p className="font-mono text-sm font-bold">4w / π²</p>
            </div>
            <div className="h-8 w-px bg-[#141414]/20" />
            <div className="text-right">
              <p className="text-[10px] font-mono opacity-50 uppercase tracking-widest">Frequency</p>
              <p className="font-mono text-sm font-bold">3.88 Hz</p>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 relative bg-[#E4E3E0] overflow-hidden">
          {mode === 'visualizer' && (
            <div className="absolute inset-0 pointer-events-none opacity-[0.03]" 
                 style={{ backgroundImage: 'radial-gradient(#141414 1px, transparent 0)', backgroundSize: '24px 24px' }} />
          )}
          
          <AnimatePresence mode="wait">
            <motion.div
              key={mode === 'visualizer' ? activeAxiom.id : mode}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className="w-full h-full"
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Footer / Description (Only in visualizer mode) */}
        {mode === 'visualizer' && (
          <footer className="border-t border-[#141414] bg-[#E4E3E0] p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-[10px] font-mono opacity-50 uppercase tracking-widest mb-2">Geometric Derivation</h3>
              <p className="text-sm leading-relaxed max-w-xl">
                {activeAxiom.description}
              </p>
            </div>
            <div>
              <h3 className="text-[10px] font-mono opacity-50 uppercase tracking-widest mb-2">Mythological Scaffolding</h3>
              <p className="text-sm italic font-serif leading-relaxed max-w-xl opacity-80">
                "{activeAxiom.mythos}"
              </p>
            </div>
          </footer>
        )}
      </main>
    </div>
  );
}
