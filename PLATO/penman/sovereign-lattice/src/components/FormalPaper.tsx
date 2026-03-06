import { motion } from 'motion/react';
import { AXIOMS } from '../types';

export default function FormalPaper() {
  return (
    <div className="w-full h-full overflow-y-auto bg-white p-12 flex justify-center">
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="max-w-3xl w-full font-sans text-zinc-900"
      >
        <header className="mb-12 border-b-2 border-zinc-900 pb-8">
          <h1 className="text-4xl font-bold tracking-tight mb-2 uppercase">The Sovereign Lattice</h1>
          <p className="text-xl font-medium italic text-zinc-600 mb-4">A Unified Geometric Cosmology of Calligraphic Motion</p>
          <div className="flex justify-between text-sm font-mono uppercase tracking-widest text-zinc-500">
            <span>Version 1.0.361</span>
            <span>Date: March 2026</span>
          </div>
        </header>

        <section className="mb-12">
          <h2 className="text-sm font-mono uppercase tracking-[0.3em] text-zinc-400 mb-6 border-b border-zinc-100 pb-2">Abstract</h2>
          <p className="leading-relaxed text-lg italic">
            This paper formalizes the "Sovereign Lattice" framework, bridging the physics of penmanship with Platonic geometry and biological anatomy. We derive the 4w stability threshold, the √42 divine constant, and the Voronoi-361 transition. Finally, we provide a calligraphic derivation of $E=mc^2$ as the transformation of the Count (5) into the Meaning (13) via the Golden Ratio.
          </p>
        </section>

        <div className="grid grid-cols-1 gap-12">
          {AXIOMS.map((axiom) => (
            <section key={axiom.id} className="border-l-4 border-zinc-100 pl-8">
              <div className="flex items-baseline gap-4 mb-2">
                <h3 className="text-2xl font-bold">{axiom.title}</h3>
                <span className="font-mono text-zinc-400 text-sm">{axiom.formula}</span>
              </div>
              <p className="mb-4 text-zinc-700 leading-relaxed">
                {axiom.description}
              </p>
              {axiom.id === 'energy-derivation' && (
                <div className="mb-4 p-4 bg-zinc-50 border border-zinc-100 rounded text-sm font-mono">
                  <p className="mb-2">Derivation Logic:</p>
                  <p>1. Let m = 5 (The Count / The Seed)</p>
                  <p>2. Let c² = φ² ≈ 2.618 (The Golden Expansion)</p>
                  <p>3. E = 5 * 2.618 = 13.09 ≈ 13 (The Meaning / The Hypotenuse)</p>
                  <p>Result: The 5-12-13 bridge is the relativistic energy-momentum union.</p>
                </div>
              )}
              {axiom.id === 'curvature-derivation' && (
                <div className="mb-4 p-4 bg-zinc-50 border border-zinc-100 rounded text-sm font-mono">
                  <p className="mb-2">Rigorous Derivation:</p>
                  <p>1. Wave: y(x) = w · sin(2πx/L)</p>
                  <p>2. Curvature κ = |y''| / (1 + (y')²)^(3/2)</p>
                  <p>3. At peak: y' = 0, y'' = -w · (4π²/L²)</p>
                  <p>4. R_peak = 1/κ = L² / (4π²w)</p>
                  <p>5. Stability: R_peak ≥ w (Pen width constraint)</p>
                  <p>6. L² / (4π²w) ≥ w  ⇒ L ≥ 2πw ≈ 6.283w</p>
                  <p>Conclusion: Below 6.28w, the pen is physically wider than the turn.</p>
                </div>
              )}
              {axiom.id === 'sonnet-engine' && (
                <div className="mb-4 p-4 bg-zinc-50 border border-zinc-100 rounded text-sm font-mono">
                  <p className="mb-2">Biological Calibration:</p>
                  <p>1. Seed Count = 1609 (The Poppy)</p>
                  <p>2. Golden Ratio = 1.618 (The Bloom)</p>
                  <p>3. Will (Δ) = 1.618 - 1.609 = 0.009</p>
                  <p>4. Aperture = 20° (The Radial Release)</p>
                  <p>Result: The 0.009 Will drives the 24-log spiral germination.</p>
                </div>
              )}
              {axiom.id === 'spiral-24' && (
                <div className="mb-4 p-4 bg-zinc-50 border border-zinc-100 rounded text-sm font-mono">
                  <p className="mb-2">Folding Mechanism Derivation:</p>
                  <p>1. Spiral: r(θ) = a · e^(bθ)</p>
                  <p>2. Anchor: θ₀ = 20°, r₀ ≈ 122.8</p>
                  <p>3. 24-Step Scaling: r₂₄ = r₀ · (1.618/1.609)</p>
                  <p>4. Growth Constant b ≈ 0.0006657</p>
                  <p>5. Initial Radius a ≈ 122.77</p>
                  <p>Result: The spiral orchestrates the √42 resonance across 24 chronons.</p>
                </div>
              )}
              <div className="bg-zinc-50 p-4 rounded text-sm italic font-serif text-zinc-500">
                "{axiom.mythos}"
              </div>
            </section>
          ))}
        </div>

        <footer className="mt-24 pt-12 border-t border-zinc-200 text-center text-zinc-400 text-xs font-mono uppercase tracking-widest">
          <p>© 2026 The Sovereign Scriptorium. All rights reserved.</p>
          <p className="mt-2">Akashic Record ID: 1360-361-42</p>
        </footer>
      </motion.div>
    </div>
  );
}
