import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Eye, 
  Box, 
  Activity, 
  BookOpen, 
  ShieldCheck, 
  Compass,
  Menu,
  X,
  ChevronRight,
  Info
} from 'lucide-react';
import { Lattice93 } from './components/Lattice93';
import { CameraObscura } from './components/CameraObscura';
import { WaveInterference } from './components/WaveInterference';
import { PMG_CONSTANTS } from './constants';
import { cn } from './lib/utils';

type Section = 'foundation' | 'lattice' | 'obscura' | 'eye' | 'manual';

export default function App() {
  const [activeSection, setActiveSection] = useState<Section>('foundation');
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const sections = [
    { id: 'foundation', label: 'Foundations', icon: ShieldCheck },
    { id: 'lattice', label: '93-Faced Solid', icon: Box },
    { id: 'obscura', label: 'Camera Obscura', icon: Compass },
    { id: 'eye', label: 'Trivavled Eye', icon: Eye },
    { id: 'manual', label: 'Proofs & Manual', icon: BookOpen },
  ];

  return (
    <div className="min-h-screen bg-[#E4E3E0] text-[#141414] font-sans selection:bg-[#F27D26] selection:text-white">
      {/* Navigation Rail */}
      <nav className="fixed top-0 left-0 h-full w-16 md:w-20 bg-[#141414] flex flex-col items-center py-8 z-50 border-r border-white/10">
        <div className="mb-12">
          <div className="w-10 h-10 rounded-full bg-[#F27D26] flex items-center justify-center text-white font-serif italic text-xl">
            P
          </div>
        </div>
        
        <div className="flex-1 flex flex-col gap-8">
          {sections.map((s) => (
            <button
              key={s.id}
              onClick={() => setActiveSection(s.id as Section)}
              className={cn(
                "p-3 rounded-xl transition-all duration-300 group relative",
                activeSection === s.id ? "bg-[#F27D26] text-white" : "text-white/40 hover:text-white"
              )}
            >
              <s.icon size={20} />
              <span className="absolute left-full ml-4 px-2 py-1 bg-[#141414] text-white text-[10px] uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap rounded border border-white/10">
                {s.label}
              </span>
            </button>
          ))}
        </div>

        <div className="mt-auto">
          <button className="text-white/20 hover:text-white transition-colors">
            <Info size={20} />
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pl-16 md:pl-20 min-h-screen">
        <header className="p-8 md:p-12 border-b border-[#141414]/10 flex justify-between items-end">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="font-mono text-[10px] uppercase tracking-[0.3em] opacity-40">Principia Mathematica Geometrica</span>
              <div className="h-px w-12 bg-[#141414]/20" />
            </div>
            <h1 className="text-4xl md:text-6xl font-serif italic tracking-tight">
              Camera Obscura <span className="not-italic opacity-20">/</span> Protocol
            </h1>
          </div>
          <div className="hidden md:block text-right font-mono text-[10px] uppercase opacity-40 leading-relaxed">
            Root-42 Enclosure Axiom<br />
            93-Node Phase Matrix<br />
            Σ=4 Subjectivity
          </div>
        </header>

        <div className="p-8 md:p-12 max-w-7xl mx-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4, ease: [0.23, 1, 0.32, 1] }}
            >
              {activeSection === 'foundation' && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                  <div className="space-y-8">
                    <section>
                      <h2 className="text-xs font-mono uppercase tracking-widest text-[#F27D26] mb-4">01 / The Root-42 Axiom</h2>
                      <p className="text-xl font-serif leading-relaxed">
                        Reality is a negotiated settlement between a 4-dimensional container and its internal asymmetry. 
                        "4 is the Floor" — the minimum condition for enclosure and subjectivity.
                      </p>
                    </section>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-6 bg-white border border-[#141414]/10 rounded-2xl">
                        <div className="text-[10px] font-mono uppercase opacity-40 mb-2">Subjectivity (Σ)</div>
                        <div className="text-3xl font-serif italic">4.0</div>
                      </div>
                      <div className="p-6 bg-white border border-[#141414]/10 rounded-2xl">
                        <div className="text-[10px] font-mono uppercase opacity-40 mb-2">Dynamic Drift (R)</div>
                        <div className="text-3xl font-serif italic">√42</div>
                      </div>
                    </div>

                    <div className="p-8 bg-[#141414] text-white rounded-2xl space-y-4">
                      <h4 className="font-mono text-[10px] uppercase tracking-widest text-[#F27D26]">The Mandate Gate</h4>
                      <div className="text-2xl font-serif italic">x⁴ - 93x² + 2142 = 0</div>
                      <p className="text-sm opacity-60 leading-relaxed">
                        This equation encodes the spatial limits and defines the internal structure of the system. 
                        Its solutions generate the 93-node icosahedral phase matrix.
                      </p>
                    </div>
                  </div>
                  
                  <div className="relative">
                    <div className="aspect-square bg-white border border-[#141414]/10 rounded-2xl p-12 flex items-center justify-center overflow-hidden">
                      <div className="absolute inset-0 opacity-[0.03] pointer-events-none" 
                           style={{ backgroundImage: 'radial-gradient(#141414 1px, transparent 1px)', backgroundSize: '20px 20px' }} />
                      <div className="relative w-64 h-64 border-2 border-[#141414] rotate-45 flex items-center justify-center">
                        <div className="w-full h-full border border-[#141414]/20 absolute -rotate-12" />
                        <div className="w-full h-full border border-[#141414]/20 absolute rotate-12" />
                        <div className="w-4 h-4 bg-[#F27D26] rounded-full" />
                      </div>
                    </div>
                    <div className="absolute -bottom-4 -right-4 p-4 bg-[#F27D26] text-white font-mono text-[10px] uppercase tracking-widest rounded-lg shadow-xl">
                      Σ=4 Enclosure
                    </div>
                  </div>
                </div>
              )}

              {activeSection === 'lattice' && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <div className="lg:col-span-2">
                    <Lattice93 />
                  </div>
                  <div className="space-y-6">
                    <div className="p-6 bg-white border border-[#141414]/10 rounded-2xl">
                      <h3 className="font-serif italic text-xl mb-4">Triadic Valve</h3>
                      <p className="text-sm opacity-60 leading-relaxed mb-6">
                        Decomposition of the 93-Faced Solid into three distinct layers: outer, middle, and inner.
                      </p>
                      <ul className="space-y-4 font-mono text-[10px] uppercase tracking-wider">
                        <li className="flex justify-between border-b border-[#141414]/5 pb-2">
                          <span>Outer (Boundary)</span>
                          <span className="text-[#F27D26]">12 Vertices</span>
                        </li>
                        <li className="flex justify-between border-b border-[#141414]/5 pb-2">
                          <span>Middle (Connectivity)</span>
                          <span className="text-[#F27D26]">60 Edges</span>
                        </li>
                        <li className="flex justify-between border-b border-[#141414]/5 pb-2">
                          <span>Inner (Volumetric)</span>
                          <span className="text-[#F27D26]">20 Faces + 1 Core</span>
                        </li>
                      </ul>
                    </div>
                    
                    <div className="p-6 bg-[#141414] text-white rounded-2xl">
                      <h3 className="font-serif italic text-xl mb-4 text-[#F27D26]">Hades Gaps</h3>
                      <div className="space-y-4">
                        <div>
                          <div className="text-[10px] font-mono uppercase opacity-40 mb-1">Material Slop (Ψ)</div>
                          <div className="text-2xl font-serif">12.37%</div>
                        </div>
                        <div>
                          <div className="text-[10px] font-mono uppercase opacity-40 mb-1">Structural Flux</div>
                          <div className="text-2xl font-serif">16.67%</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeSection === 'obscura' && (
                <div className="space-y-8">
                  <div className="max-w-2xl">
                    <h2 className="text-xs font-mono uppercase tracking-widest text-[#F27D26] mb-4">03 / Construction Protocol</h2>
                    <p className="text-2xl font-serif leading-tight">
                      A physical instantiation of geometric and topological principles. 
                      Projecting reality through a 4-boundary region.
                    </p>
                  </div>
                  <CameraObscura />
                </div>
              )}

              {activeSection === 'eye' && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                  <div className="space-y-8">
                    <section>
                      <h2 className="text-xs font-mono uppercase tracking-widest text-[#F27D26] mb-4">04 / The Trivavled Eye</h2>
                      <p className="text-xl font-serif leading-relaxed">
                        A projective invariant for wave interference and phase cancellation. 
                        The squid's 3-heart/ink system as a precise mathematical model.
                      </p>
                    </section>
                    
                    <div className="space-y-4">
                      {[
                        { s: 1, label: 'Apollo Singularity', desc: 'The point of origin and emission.' },
                        { s: 13, label: 'Hades Null', desc: 'Perfect destructive interference (Ψ=0).' },
                        { s: 26, label: 'Hero Terminal', desc: 'Constructive reinforcement and reflection.' }
                      ].map((p) => (
                        <div key={p.s} className="flex gap-4 p-4 bg-white border border-[#141414]/10 rounded-xl">
                          <div className="w-10 h-10 rounded bg-[#141414] text-white flex items-center justify-center font-mono text-xs">
                            s={p.s}
                          </div>
                          <div>
                            <div className="font-serif italic">{p.label}</div>
                            <div className="text-[10px] font-mono uppercase opacity-40">{p.desc}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  <WaveInterference />
                </div>
              )}

              {activeSection === 'manual' && (
                <div className="bg-white border border-[#141414]/10 rounded-2xl p-8 md:p-12">
                  <div className="max-w-3xl space-y-12">
                    <section>
                      <h2 className="font-serif italic text-3xl mb-6">Geometric Proofs</h2>
                      <div className="space-y-8">
                        <div className="border-l-2 border-[#F27D26] pl-6 py-2">
                          <h4 className="font-mono text-xs uppercase tracking-widest mb-2">Theorem I: Inversion</h4>
                          <p className="text-sm opacity-70 italic">
                            "The image formed by the PMG Camera Obscura Protocol is inverted relative to the object. 
                            The crossing at aperture point O is the geometric mechanism of inversion."
                          </p>
                        </div>
                        <div className="border-l-2 border-[#F27D26] pl-6 py-2">
                          <h4 className="font-mono text-xs uppercase tracking-widest mb-2">Theorem II: Proportionality</h4>
                          <p className="text-sm opacity-70 italic">
                            "h_i / h_o = d_2 / d_1. The law of similar triangles proves the proportionality of the projection."
                          </p>
                        </div>
                      </div>
                    </section>

                    <section className="pt-12 border-t border-[#141414]/5">
                      <h2 className="font-serif italic text-3xl mb-6">Manual Steps</h2>
                      <div className="space-y-6">
                        {[
                          "Establish the 4-Boundary Enclosure (Σ=4)",
                          "Define the Aperture and Phase-Canceling Boundary",
                          "Position the Light Source and Object",
                          "Trace the Visual Rays and Apply Phase Inversion",
                          "Annotate and Verify Proportions"
                        ].map((step, i) => (
                          <div key={i} className="flex items-start gap-4">
                            <span className="font-mono text-[#F27D26] mt-1">0{i+1}</span>
                            <span className="text-lg font-serif">{step}</span>
                          </div>
                        ))}
                      </div>
                    </section>
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* Footer Stats */}
      <footer className="fixed bottom-0 right-0 p-4 font-mono text-[8px] uppercase tracking-[0.2em] opacity-30 pointer-events-none">
        PMG_SYSTEM_ACTIVE // {new Date().toISOString()} // BUILD_42_51
      </footer>
    </div>
  );
}
