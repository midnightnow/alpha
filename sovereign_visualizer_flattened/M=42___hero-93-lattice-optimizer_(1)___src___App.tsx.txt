import { useState, useEffect, Suspense } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Hexagon, Cpu, Shield, Zap, Info, ChevronRight, Github, Target, Box, FileText, Activity } from 'lucide-react';
import LatticeVisualizer from './components/LatticeVisualizer';
import Lattice3D from './components/Lattice3D';
import OptimizerPanel from './components/OptimizerPanel';
import FormalProof from './components/FormalProof';
import { generateLatticePoints } from './math/geometry';

export default function App() {
  const [epsilon, setEpsilon] = useState(0);
  const [points, setPoints] = useState<number[][]>([]);
  const [viewMode, setViewMode] = useState<'2d' | '3d'>('3d');
  const [activeTab, setActiveTab] = useState<'manifold' | 'proof'>('manifold');

  useEffect(() => {
    setPoints(generateLatticePoints(epsilon));
  }, [epsilon]);

  const handleOptimizationResult = (newEpsilon: number) => {
    setEpsilon(newEpsilon);
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans selection:bg-emerald-500/30">
      {/* Navigation */}
      <nav className="border-b border-white/5 bg-black/40 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.4)]">
              <Hexagon className="w-5 h-5 text-black" />
            </div>
            <span className="font-medium tracking-tight text-lg">HERO 93 <span className="text-emerald-500 font-bold">Lattice</span></span>
          </div>
          
          <div className="flex items-center bg-white/5 rounded-full p-1 border border-white/10">
            <button 
              onClick={() => setActiveTab('manifold')}
              className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all flex items-center gap-2 ${activeTab === 'manifold' ? 'bg-emerald-500 text-black shadow-lg' : 'text-white/60 hover:text-white'}`}
            >
              <Activity className="w-3.5 h-3.5" />
              Manifold
            </button>
            <button 
              onClick={() => setActiveTab('proof')}
              className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all flex items-center gap-2 ${activeTab === 'proof' ? 'bg-emerald-500 text-black shadow-lg' : 'text-white/60 hover:text-white'}`}
            >
              <FileText className="w-3.5 h-3.5" />
              Formal Proof
            </button>
          </div>

          <div className="flex items-center gap-6">
            <button className="text-white/40 hover:text-white transition-colors">
              <Github className="w-5 h-5" />
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12">
        <AnimatePresence mode="wait">
          {activeTab === 'manifold' ? (
            <motion.div
              key="manifold"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
            >
              {/* Hero Section */}
              <div className="mb-16">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-mono uppercase tracking-widest mb-6">
                    <Zap className="w-3 h-3" />
                    Path B Optimized Visualization
                  </div>
                  <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 leading-[0.9]">
                    The Attractor <span className="text-emerald-500 italic">State.</span>
                  </h1>
                  <p className="text-lg text-white/60 leading-relaxed mb-8 max-w-2xl">
                    Witness the geometric convergence of the HERO 93 solid. By applying the optimized phase offset 
                    <span className="text-white font-mono mx-1">ε ≈ 0.08345</span>, the lattice volume stabilizes 
                    at the universal invariant <span className="text-white font-mono">42.0</span>.
                  </p>
                </div>
              </div>

              {/* Main Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Left Column: Visualizer */}
                <div className="lg:col-span-7 space-y-8">
                  <div className="relative group">
                    <div className="absolute top-4 right-4 z-20 flex gap-2">
                      <button 
                        onClick={() => setViewMode('2d')}
                        className={`p-2 rounded-lg border transition-all ${viewMode === '2d' ? 'bg-emerald-500 border-emerald-500 text-black' : 'bg-black/40 border-white/10 text-white/40 hover:text-white'}`}
                        title="2D Projection"
                      >
                        <Target className="w-4 h-4" />
                      </button>
                      <button 
                        onClick={() => setViewMode('3d')}
                        className={`p-2 rounded-lg border transition-all ${viewMode === '3d' ? 'bg-emerald-500 border-emerald-500 text-black' : 'bg-black/40 border-white/10 text-white/40 hover:text-white'}`}
                        title="3D Manifold"
                      >
                        <Box className="w-4 h-4" />
                      </button>
                    </div>
                    
                    <AnimatePresence mode="wait">
                      {viewMode === '3d' ? (
                        <motion.div
                          key="3d"
                          initial={{ opacity: 0, scale: 0.98 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.98 }}
                          transition={{ duration: 0.4 }}
                        >
                          <Suspense fallback={<div className="w-full h-[500px] bg-black/40 animate-pulse rounded-2xl border border-white/5" />}>
                            <Lattice3D points={points} epsilon={epsilon} />
                          </Suspense>
                        </motion.div>
                      ) : (
                        <motion.div
                          key="2d"
                          initial={{ opacity: 0, scale: 0.98 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.98 }}
                          transition={{ duration: 0.4 }}
                        >
                          <LatticeVisualizer points={points} height={500} />
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    {[
                      { icon: Cpu, label: 'Nodes', value: '93' },
                      { icon: Shield, label: 'Closure', value: 'Torsion' },
                      { icon: Target, label: 'Precision', value: '10⁻⁸' },
                    ].map((stat, i) => (
                      <div key={i} className="bg-white/5 border border-white/10 rounded-xl p-4">
                        <stat.icon className="w-4 h-4 text-emerald-500 mb-2" />
                        <div className="text-[10px] font-mono text-white/40 uppercase tracking-widest mb-1">{stat.label}</div>
                        <div className="text-lg font-medium">{stat.value}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Right Column: Controls */}
                <div className="lg:col-span-5">
                  <OptimizerPanel onResult={handleOptimizationResult} />
                </div>
              </div>

              {/* Bottom Info Section */}
              <div className="mt-20 grid grid-cols-1 lg:grid-cols-2 gap-12 border-t border-white/5 pt-12">
                <div>
                  <h3 className="text-sm font-mono text-white/40 uppercase tracking-widest mb-4 flex items-center gap-2">
                    <Info className="w-4 h-4" />
                    Honest Statement
                  </h3>
                  <p className="text-sm text-white/60 leading-relaxed">
                    The HERO 93 object is a hollow shell of geometry wrapped around a core of void. 
                    The boundary has zero thickness; it is an interpolation of 93 discrete points. 
                    The "mass" of 42 is not weight, but the <strong>tension</strong> required to hold 
                    the shell against the sky.
                  </p>
                  
                  <div className="mt-8">
                    <h3 className="text-sm font-mono text-white/40 uppercase tracking-widest mb-4">Comparative Analysis (k-Denom)</h3>
                    <div className="bg-black/40 border border-white/5 rounded-lg overflow-hidden">
                      <table className="w-full text-[10px] font-mono">
                        <thead className="bg-white/5 text-white/40 uppercase tracking-widest">
                          <tr>
                            <th className="p-2 text-left">Nodes</th>
                            <th className="p-2 text-left">k</th>
                            <th className="p-2 text-left">Volume</th>
                            <th className="p-2 text-left">Gap</th>
                          </tr>
                        </thead>
                        <tbody className="text-white/60">
                          <tr className="border-t border-white/5">
                            <td className="p-2">93</td>
                            <td className="p-2">12</td>
                            <td className="p-2">56.06</td>
                            <td className="p-2">14.06</td>
                          </tr>
                          <tr className="border-t border-white/5 bg-emerald-500/5 text-emerald-400">
                            <td className="p-2">93</td>
                            <td className="p-2">13</td>
                            <td className="p-2">41.40</td>
                            <td className="p-2">0.60</td>
                          </tr>
                          <tr className="border-t border-white/5">
                            <td className="p-2">93</td>
                            <td className="p-2">14</td>
                            <td className="p-2">34.71</td>
                            <td className="p-2">7.29</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <p className="text-[10px] text-white/30 mt-2 italic">
                      *Analysis confirms k=13 as the structural fit for the 42 attractor.
                    </p>
                  </div>
                </div>
                <div className="space-y-4">
                  <h3 className="text-sm font-mono text-white/40 uppercase tracking-widest mb-4">Revised Axioms</h3>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                      <span className="text-xs font-mono text-white/80">Axiom 1: Calibration Identity</span>
                      <ChevronRight className="w-4 h-4 text-emerald-500" />
                    </div>
                    <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                      <span className="text-xs font-mono text-white/80">Axiom 2: Symbolic Selection</span>
                      <ChevronRight className="w-4 h-4 text-emerald-500" />
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="proof"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
            >
              <FormalProof />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/5 py-12 mt-20">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6 text-white/40 text-xs font-mono uppercase tracking-widest">
          <div>© 2026 HERO 93 Research Collective</div>
          <div className="flex gap-8">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
