
import React, { useState } from 'react';
import { X, BookOpen, Layers, Activity, GitCommit, Heart, Microscope, GraduationCap, Sigma, Lock, ArrowUpCircle } from 'lucide-react';
import { SQRT_42, SQRT_51 } from '../constants';

interface ExplainerModalProps {
  onClose: () => void;
}

const ExplainerModal: React.FC<ExplainerModalProps> = ({ onClose }) => {
  const [level, setLevel] = useState<1 | 2 | 3 | 4>(1);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-gray-900 border border-gray-700 w-full max-w-2xl h-[85vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-800 bg-gray-950">
          <div className="flex items-center gap-3">
            <BookOpen className="text-cyan-500" size={24} />
            <div>
              <h2 className="text-xl font-bold text-gray-100 tracking-wide">Lab Manual: The Resonant Sphere</h2>
              <p className="text-xs text-gray-500 uppercase tracking-widest">Progressive Disclosure Guide</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-gray-800 rounded-full transition-colors text-gray-400 hover:text-white">
            <X size={20} />
          </button>
        </div>

        {/* Level Selector Tabs */}
        <div className="flex border-b border-gray-800 bg-gray-900/50 overflow-x-auto scrollbar-none">
          <button
            onClick={() => setLevel(1)}
            className={`flex-1 py-4 px-2 text-[10px] sm:text-xs font-bold uppercase tracking-wider transition-all flex items-center justify-center gap-2 whitespace-nowrap ${
              level === 1 ? 'border-b-2 border-cyan-500 text-cyan-400 bg-cyan-900/10' : 'text-gray-500 hover:text-gray-300'
            }`}
          >
            <GitCommit size={14} /> Theory
          </button>
          <button
            onClick={() => setLevel(2)}
            className={`flex-1 py-4 px-2 text-[10px] sm:text-xs font-bold uppercase tracking-wider transition-all flex items-center justify-center gap-2 whitespace-nowrap ${
              level === 2 ? 'border-b-2 border-amber-500 text-amber-400 bg-amber-900/10' : 'text-gray-500 hover:text-gray-300'
            }`}
          >
            <Layers size={14} /> Geometry
          </button>
          <button
            onClick={() => setLevel(3)}
            className={`flex-1 py-4 px-2 text-[10px] sm:text-xs font-bold uppercase tracking-wider transition-all flex items-center justify-center gap-2 whitespace-nowrap ${
              level === 3 ? 'border-b-2 border-green-500 text-green-400 bg-green-900/10' : 'text-gray-500 hover:text-gray-300'
            }`}
          >
            <Sigma size={14} /> Math
          </button>
          <button
            onClick={() => setLevel(4)}
            className={`flex-1 py-4 px-2 text-[10px] sm:text-xs font-bold uppercase tracking-wider transition-all flex items-center justify-center gap-2 whitespace-nowrap ${
              level === 4 ? 'border-b-2 border-indigo-500 text-indigo-400 bg-indigo-900/10' : 'text-gray-500 hover:text-gray-300'
            }`}
          >
            <Lock size={14} /> Decryption
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8 text-gray-300 leading-relaxed scrollbar-thin scrollbar-thumb-gray-700">
          
          {level === 1 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-2 text-cyan-400 mb-2">
                <Heart size={20} />
                <h3 className="text-2xl font-light text-white">The Body as a Standing Wave</h3>
              </div>
              <p>
                Matter is simply localized vibration. In this laboratory, we model the human form not as a solid object, but as an <strong>interference pattern</strong> created by three primary oscillators:
              </p>
              <ul className="list-disc pl-5 space-y-2 text-gray-400">
                <li><strong>The Tan Tien</strong> (Will / Physical Center)</li>
                <li><strong>The Heart</strong> (Connection / Feeling Center)</li>
                <li><strong>The Core Star</strong> (Essence / Divine Center)</li>
              </ul>
              <div className="p-4 bg-gray-800 rounded border-l-2 border-cyan-500">
                <p className="text-sm italic">
                  "Where these waves overlap constructively, they 'substantiate' into the stable nodal points we recognize as the Biofield or Chakras."
                </p>
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Primary Reference: Brennan, B. A. (1993). <em>Light Emerging</em>.
              </p>
            </div>
          )}

          {level === 2 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-2 text-amber-400 mb-2">
                <Microscope size={20} />
                <h3 className="text-2xl font-light text-white">Hexagonal Packing & Proportions</h3>
              </div>
              <p>
                When we scan the body at the <strong>Heart Station (Y: 4.32)</strong>, the interference pattern achieves peak stability.
              </p>
              <p>
                This results in a <strong>6-fold symmetry</strong> (Hexagon). This isn't a mystical accident; it is mathematically the most efficient way to pack wave energy (or circles) on a 2D plane, mirroring the honeycomb structures found in nature.
              </p>
              
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div className="p-3 bg-gray-800 rounded border border-gray-700">
                    <h4 className="text-xs font-bold uppercase text-amber-500 mb-1">Vertical Axis</h4>
                    <p className="text-xs">Aligned with the Hara Line (Laser line of Intent).</p>
                </div>
                <div className="p-3 bg-gray-800 rounded border border-gray-700">
                    <h4 className="text-xs font-bold uppercase text-amber-500 mb-1">Horizontal Plane</h4>
                    <p className="text-xs">Aligned with T-5 Vertebra (Heart Center).</p>
                </div>
              </div>

              <p className="text-sm text-gray-500 mt-4">
                Reference: Conway & Sloane (1999). <em>Sphere Packings, Lattices and Groups</em>.
              </p>
            </div>
          )}

          {level === 3 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-2 text-green-400 mb-2">
                <GraduationCap size={20} />
                <h3 className="text-2xl font-light text-white">The Physics of the Void</h3>
              </div>
              <p>
                The core engine calculates the total intensity $I$ at any point $(x,y,z)$ using the linear superposition of spherical waves.
              </p>
              
              <div className="font-mono text-sm bg-black p-4 rounded border border-gray-700 text-green-400 overflow-x-auto">
                I(x, y, z, t) = (1/3) * Σ cos(k * d_i + φ_i) * sin(ωt)
              </div>
              
              <div className="space-y-2 mt-4 text-sm text-gray-400">
                <p>Where:</p>
                <ul className="list-disc pl-5">
                    <li>$k = 2\pi / \lambda$ (Wave Number)</li>
                    <li>$d_i$ = Distance from Origin $i$ to point $(x,y,z)$</li>
                    <li>$\phi_i$ = Phase offset (Phi/Psi)</li>
                </ul>
              </div>

              <p>
                We apply <strong>Fine Structure Damping</strong> ($\alpha \approx 1/137$) to simulate the decay of the field as it moves into the objective world.
              </p>

              <p className="text-sm text-gray-500 mt-4">
                Reference: Hecht, E. (2016). <em>Optics</em>. Eq. 9.11.
              </p>
            </div>
          )}

          {level === 4 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-2 text-indigo-400 mb-2">
                <ArrowUpCircle size={20} />
                <h3 className="text-2xl font-light text-white">The Vitruvian Decryption</h3>
              </div>
              <p>
                Analysis of the geometric relationships in the Vitruvian Man reveals two distinct "operating systems" for the human form.
              </p>

              <div className="space-y-4">
                  <div className="p-4 bg-gray-800 rounded border border-gray-700">
                    <h4 className="text-amber-500 font-bold mb-1">√42 ({SQRT_42.toFixed(3)}) - The Material Plane</h4>
                    <p className="text-sm text-gray-400">
                        The "Square of Materiality". This constant anchors the physical body to the 2D plane (Flatland). The geometric center is the <strong>Navel</strong>. 
                        This represents the "Hired Man" or the biological vessel.
                    </p>
                  </div>
                  
                  <div className="flex justify-center text-gray-600">
                      <ArrowUpCircle size={24} className="animate-bounce" />
                  </div>

                  <div className="p-4 bg-gray-800 rounded border border-gray-700">
                    <h4 className="text-cyan-400 font-bold mb-1">√51 ({SQRT_51.toFixed(3)}) - The Resonant Sphere</h4>
                    <p className="text-sm text-gray-400">
                        The "Symmetry Point" ($\approx \pi + 4$). This acts as a bridge between circular transcendence ($\pi$) and earthly manifestation ($4$).
                        The geometric center shifts to the <strong>Heart/Core Star</strong>. This represents the "Higher Man" or the resonant occupant.
                    </p>
                  </div>
              </div>

              <div className="p-4 bg-indigo-900/20 border border-indigo-500/30 rounded mt-4">
                  <h4 className="text-xs font-bold uppercase text-indigo-300 mb-1">Research Implication</h4>
                  <p className="text-sm text-gray-300">
                      Scaling the simulation to √51 allows for "Resonance Lock," where the nodal skeleton of reality snaps into 6-fold hexagonal stability.
                  </p>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default ExplainerModal;
