import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface VerseMapping {
    [key: number]: {
        title: string;
        law: string;
    };
}

const VERSE_MAP: VerseMapping = {
    0: { title: "The Singularity", law: "The universe is a single I and O in constant alternation." },
    3: { title: "The Man", law: "Primal post (buried foot). Vertical support." },
    4: { title: "The Home", law: "Rail / Square. Horizontal rule. Best Laid Plan." },
    5: { title: "The Queen", law: "Hypotenuse / Diagonal. The bridge — makes 3+4 whole." },
    12: { title: "The City State", law: "12 rails require 13 posts. The +1 is the vibration of life." },
    13: { title: "The City State", law: "12 rails require 13 posts. The +1 is the vibration of life." },
    24: { title: "The Axial Chamber", law: "Hours in a day — the full rotation of the plan." },
    26: { title: "The Alphabet", law: "Language as the doubled hypotenuse (13x2)." },
    37: { title: "The Soul Seat", law: "37°C Axis. Radiance becoming visible light." },
    42: { title: "The Aperture", law: "The 42° Glow. The aperture where Light enters Gravity." },
    51: { title: "The Skybox", law: "Root 51. The boundary of the information paddock." },
    60: { title: "The Hex Reset", law: "The pillars lie down and dance. Return to 60° symmetry." },
    78: { title: "Reflective Inversion", law: "Lateral Symmetry Plane. p ↔ b. The Flip." },
    93: { title: "The Final Seal", law: "The Taut Record. The Full Stop. Vitrified." }
};

export const VerseHUD = () => {
    const [activeNode, setActiveNode] = useState<number | null>(null);
    const [isDiscovery, setIsDiscovery] = useState(false);
    const [residue, setResidue] = useState(0);

    useEffect(() => {
        const handleNodeEvent = (e: any) => {
            if (e.detail?.nodeIndex !== undefined) {
                const idx = e.detail.nodeIndex;
                if (VERSE_MAP[idx]) {
                    setActiveNode(idx);

                    // Node 42: Discovery Flicker + Residue Check
                    if (idx === 42) {
                        setIsDiscovery(true);
                        // Simulate a residue for the visual trigger (12.37% threshold)
                        const simulatedResidue = 0.1237 + (Math.random() * 0.05);
                        setResidue(simulatedResidue);
                        setTimeout(() => setIsDiscovery(false), 500);
                    } else {
                        setResidue(0);
                    }
                } else {
                    setActiveNode(null);
                    setResidue(0);
                }
            }
        };

        window.addEventListener('lattice:letter' as any, handleNodeEvent);
        return () => window.removeEventListener('lattice:letter' as any, handleNodeEvent);
    }, []);

    const isFifthPost = activeNode === 12 || activeNode === 13;

    return (
        <div className="fixed top-32 left-10 z-[60] pointer-events-none w-80">
            <AnimatePresence mode="wait">
                {activeNode !== null && (
                    <motion.div
                        key={activeNode}
                        initial={{ opacity: 0, x: -20, scale: 0.95 }}
                        animate={{
                            opacity: isDiscovery ? [1, 0.4, 1] : 1,
                            x: 0,
                            scale: 1,
                            filter: isDiscovery ? ["blur(0px)", "blur(2px)", "blur(0px)"] : "blur(0px)"
                        }}
                        exit={{ opacity: 0, x: -10, scale: 0.9 }}
                        transition={{ duration: isDiscovery ? 0.2 : 0.4 }}
                        className={`bg-zinc-950/90 backdrop-blur-3xl border-l-[3px] p-8 shadow-[0_0_80px_rgba(244,63,94,0.15)] rounded-r-2xl ring-1 ring-white/10 ${isFifthPost ? 'border-emerald-500 shadow-[0_0_40px_rgba(16,185,129,0.2)]' : 'border-rose-500'}`}
                    >
                        <div className="flex items-center gap-3 mb-4">
                            <span className={`font-mono text-[10px] font-bold px-3 py-1 rounded-full border ${isFifthPost ? 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20' : 'text-rose-500 bg-rose-500/10 border-rose-500/20'}`}>
                                NODE #{activeNode}
                            </span>
                            <div className={`h-px flex-1 bg-gradient-to-r ${isFifthPost ? 'from-emerald-500/30' : 'from-rose-500/30'} to-transparent`} />
                        </div>

                        <h2 className="text-white text-xl font-black tracking-tight mb-3 uppercase italic leading-none">
                            {VERSE_MAP[activeNode].title}
                            {isFifthPost && <span className="ml-2 text-emerald-500 text-[10px] lowercase font-mono animate-pulse">(The +1 Post)</span>}
                        </h2>

                        <p className="text-rose-100/80 text-sm leading-relaxed font-serif italic mb-6">
                            "{VERSE_MAP[activeNode].law}"
                        </p>

                        <div className="flex items-center gap-2">
                            <motion.div
                                animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
                                transition={{ duration: 2, repeat: Infinity }}
                                className={`w-2 h-2 rounded-full ${isFifthPost ? 'bg-emerald-500' : 'bg-rose-500'}`}
                            />
                            <span className="text-[10px] text-zinc-500 uppercase tracking-[0.4em] font-bold">
                                {isFifthPost ? 'Sure System Confirmed' : 'Juridical Engine Active'}
                            </span>
                        </div>

                        {activeNode === 42 && residue >= 0.1237 && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="mt-4 pt-4 border-t border-rose-500/10 text-[9px] text-rose-500/80 font-mono tracking-widest uppercase"
                            >
                                <div className="flex justify-between mb-1">
                                    <span>Hades Residue:</span>
                                    <span className="text-rose-400">{(residue * 100).toFixed(4)}%</span>
                                </div>
                                <div className="flex justify-between mb-1">
                                    <span>Vitrification:</span>
                                    <span className="text-rose-400">Standing Wave @ 51°</span>
                                </div>
                                <div className="text-rose-500/40 animate-pulse mt-2">
                                    WARNING: 12.37% Information Leak Detected
                                </div>
                                <div className="text-rose-500/20 text-[7px] mt-1 italic">
                                    Butcher Reborn mode: Lambskin Filter Active
                                </div>
                            </motion.div>
                        )}

                        {isFifthPost && (
                            <div className="mt-4 pt-4 border-t border-emerald-500/10 text-[9px] text-emerald-500/60 font-mono tracking-widest uppercase">
                                The 13th Post Vibration Active
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
