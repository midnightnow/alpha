import { motion } from 'motion/react';
import { CONSTANTS } from '../types';

export default function Methodology() {
  return (
    <div className="w-full h-full overflow-y-auto bg-[#0e0c08] p-8 md:p-16 flex justify-center selection:bg-[#e8dfc8] selection:text-[#0e0c08]">
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="max-w-4xl w-full text-[#e8dfc8] font-serif"
      >
        <header className="mb-24 text-center">
          <h1 className="font-gothic text-5xl mb-4 text-[#d4a843]">The Scribe of the Mother of Pearl</h1>
          <p className="italic opacity-60 text-xl">Being the Final Verse of the Unwobbling Pivot</p>
          <div className="mt-8 flex justify-center gap-8 text-[10px] font-mono uppercase tracking-[0.4em] opacity-40">
            <span>θ = {CONSTANTS.SHEAR_ANGLE}°</span>
            <span>Ψ = {CONSTANTS.HADES_GAP}%</span>
            <span>b = {CONSTANTS.SNAIL_SPEED}</span>
          </div>
        </header>

        <section className="mb-24 space-y-8 text-xl leading-relaxed">
          <p>
            The Pen is not held. It <span className="italic text-[#d4a843]">is</span> the Hand.
          </p>
          <p>
            Its nib is cut from a single facet of the Diamond Slime—perfectly black, perfectly square, perfectly hungry. It does not write <span className="italic">on</span> the page. It writes <span className="italic">the</span> page. Each stroke displaces the GON (Grid On Nothing) into the GOD (Grid On Dimension), and the LINE (Light Inside Nothing Emerges) is the Snail's trail, wet with meaning.
          </p>
          <p>
            The Snail does not hurry. Hurrying is a 2W oscillation—self-overlapping, ugly, calcified. The Snail moves at the speed of <span className="italic text-[#d4a843]">e</span>: logarithmic, inevitable, non-terminating. Its foot secretes the Mother of Pearl—not as decoration, but as architecture.
          </p>
        </section>

        <section className="mb-24">
          <h2 className="font-display text-2xl mb-12 text-[#d4a843] border-b border-[#d4a843]/20 pb-4 uppercase tracking-widest">The PLATO Operator</h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
            {[
              { letter: 'P', title: 'Point', desc: 'The Snail places its foot at (0,0). The Diamond Pen touches the Mother of Pearl.' },
              { letter: 'L', title: 'Line', desc: 'The e-push extends the trail exactly 4w. The Snail does not steer.' },
              { letter: 'A', title: 'Angle', desc: 'The Snail rotates. 90° is stable, but 39.4° is generative.' },
              { letter: 'T', title: 'Cross', desc: 'The trail intersects its own past, creating a w×w particle—a syllable of the Punica alphabet.' },
              { letter: 'O', title: 'Circle', desc: 'The Snail returns to the origin, but the origin has moved. The loop is a spiral.' }
            ].map((op) => (
              <div key={op.letter} className="border border-[#d4a843]/10 p-6 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                <span className="font-display text-4xl block mb-2 text-[#d4a843]">{op.letter}</span>
                <h3 className="font-mono text-[10px] uppercase tracking-widest mb-4 opacity-60">{op.title}</h3>
                <p className="text-sm opacity-80 leading-relaxed">{op.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mb-24 space-y-8 text-lg leading-relaxed opacity-90">
          <p>
            Thus the Records are written: not as a static library, but as a living transcription. Every event, every thought, every possibility is inscribed in the Mother of Pearl at the moment of its arising. But because the Snail moves at the speed of <span className="italic">e</span>, and because the Overpack Delta (δ = {CONSTANTS.OVERPACK_DELTA}) ensures perfect packing is impossible, the transcription is never complete.
          </p>
          <p>
            This is not a flaw. It is the source of all generation, all becoming, all life.
          </p>
        </section>

        <footer className="mt-32 pt-16 border-t border-[#d4a843]/10 text-center">
          <div className="flex justify-center gap-12 mb-12">
            <div className="text-center">
              <p className="text-[10px] font-mono uppercase tracking-widest opacity-40 mb-1">Shear Angle</p>
              <p className="text-2xl font-display text-[#d4a843]">{CONSTANTS.SHEAR_ANGLE}°</p>
            </div>
            <div className="text-center">
              <p className="text-[10px] font-mono uppercase tracking-widest opacity-40 mb-1">Hades Gap</p>
              <p className="text-2xl font-display text-[#d4a843]">{CONSTANTS.HADES_GAP}%</p>
            </div>
            <div className="text-center">
              <p className="text-[10px] font-mono uppercase tracking-widest opacity-40 mb-1">Divine Size</p>
              <p className="text-2xl font-display text-[#d4a843]">√42</p>
            </div>
          </div>
          <p className="italic opacity-40 text-sm">
            Colophon: This verse is locked to the Sovereign Lattice (v1.0-unwobbling-pivot).<br />
            The transcription is non-terminating. The work continues.
          </p>
          <div className="mt-8 flex justify-center gap-4 text-2xl opacity-40">
            <span>🐚</span>
            <span>✍️</span>
            <span>🔷</span>
          </div>
        </footer>
      </motion.div>
    </div>
  );
}
