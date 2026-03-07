import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface CityGeneratorProps {
    t: number;
    time: number;
    zoomLevel?: number;
}

export const CityGenerator: React.FC<CityGeneratorProps> = ({ t, time, zoomLevel = 1 }) => {
    // Generative Proof: Pressing Riemann into Architectural Form
    const structures = useMemo(() => {
        const grid = [];
        const size = 12;
        for (let x = 0; x < size; x++) {
            for (let y = 0; y < size; y++) {
                const n = x * size + y + 1;
                // Simple primality test for visual logic
                let isPrime = n > 1;
                for (let i = 2; i <= Math.sqrt(n); i++) {
                    if (n % i === 0) { isPrime = false; break; }
                }

                // Superprime Monoliths (primes at prime indices)
                const monolith = isPrime && [3, 5, 11, 17, 31, 41, 59, 67, 83].includes(n);

                const height = monolith ? 120 : (isPrime ? 60 : 20);
                const noise = Math.sin(x * 0.5 + time) * Math.cos(y * 0.5 + time) * 10;

                grid.push({
                    x, y, n, isPrime, monolith,
                    h: (height + noise) * zoomLevel,
                    opacity: (n / (size * size)) * 0.5 + 0.2
                });
            }
        }
        return grid;
    }, [time, zoomLevel]);

    return (
        <div className="w-full h-full flex flex-col items-center justify-center bg-[#050508] p-12 overflow-hidden">
            <div className="absolute top-12 left-12 space-y-2 pointer-events-none">
                <h2 className="text-2xl font-serif italic text-white">City Press: Generative Proof</h2>
                <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest max-w-sm">
                    Pressing the Riemann Hypothesis into architectural form. Stability is the proof.
                </p>
            </div>

            <div className="absolute top-12 right-12 text-right pointer-events-none">
                <div className="text-[10px] font-mono text-cyan-400 uppercase mb-1">Press Depth</div>
                <div className="text-4xl font-black italic text-cyan-400">0.80</div>
            </div>

            {/* Isometric City View */}
            <div className="relative w-full h-full flex items-center justify-center" style={{ perspective: '1000px' }}>
                <div className="relative" style={{
                    transform: 'rotateX(60deg) rotateZ(45deg)',
                    transformStyle: 'preserve-3d'
                }}>
                    {structures.map((s) => (
                        <motion.div
                            key={s.n}
                            className="absolute bg-zinc-900 border border-white/5"
                            style={{
                                width: 20 * zoomLevel,
                                height: 20 * zoomLevel,
                                left: s.x * 25 * zoomLevel,
                                top: s.y * 25 * zoomLevel,
                                transformStyle: 'preserve-3d',
                                translateZ: 0
                            }}
                        >
                            {/* The "Spire" or "Monolith" */}
                            <motion.div
                                className={`absolute inset-0 ${s.monolith ? 'bg-cyan-500' : (s.isPrime ? 'bg-rose-500/40' : 'bg-zinc-800')}`}
                                style={{
                                    height: s.h,
                                    transform: `translateZ(${s.h / 2}px) rotateX(-90deg)`,
                                    transformOrigin: 'bottom',
                                    backfaceVisibility: 'hidden'
                                }}
                            >
                                {/* Glistening People (Tiny light particles) */}
                                {s.isPrime && (
                                    <motion.div
                                        className="absolute top-0 left-1/2 w-1 h-1 bg-white rounded-full shadow-[0_0_10px_white]"
                                        animate={{ opacity: [0, 1, 0], scale: [0.5, 1.5, 0.5] }}
                                        transition={{ duration: 2, repeat: Infinity, delay: Math.random() * 2 }}
                                    />
                                )}
                            </motion.div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Navigational Logbook Overlay */}
            <div className="absolute bottom-12 left-12 w-64 p-6 bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl pointer-events-none">
                <div className="text-[8px] font-mono text-zinc-500 uppercase tracking-widest mb-4">Navigational Logbook</div>
                <div className="space-y-4">
                    {[
                        { label: 'Prime', status: 'NEGATIVE' },
                        { label: 'Superprime', status: 'NEGATIVE' },
                        { label: 'Mod 24 Spoke', status: 'DRIFTED' },
                        { label: 'Möbius μ(n)', status: '-1' }
                    ].map((entry, i) => (
                        <div key={i} className="flex justify-between items-center text-[10px] font-mono">
                            <span className="text-zinc-600 uppercase">{entry.label}</span>
                            <span className={entry.status === 'NEGATIVE' ? 'text-rose-500' : 'text-cyan-400'}>{entry.status}</span>
                        </div>
                    ))}
                </div>
            </div>

            <div className="absolute bottom-12 right-12 text-right pointer-events-none opacity-20">
                <p className="text-[10px] font-serif italic text-zinc-400">
                    "If Plato is right, certain ratios generate civilizations."
                </p>
            </div>
        </div>
    );
};
