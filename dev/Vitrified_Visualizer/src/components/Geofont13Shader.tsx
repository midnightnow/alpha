import React, { useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { audioEngine } from '../audioEngine';

/**
 * GEOFONTS 13: The 13th Silent God Code
 * Arranged for the 13-point circumscribed grid.
 */
const GEOFONTS_ALPHA = {
    ascending: [
        { letter: 'A', name: 'Alpha', type: 'vowel', housing: 'sqrt(51)' },
        { letter: 'B', name: 'Beta', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'C', name: 'Gamma', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'D', name: 'Delta', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'E', name: 'Epsilon', type: 'vowel', housing: 'sqrt(51)' },
        { letter: 'F', name: 'Zeta', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'G', name: 'Eta', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'H', name: 'Theta', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'I', name: 'Iota', type: 'vowel', housing: 'sqrt(51)' },
        { letter: 'J', name: 'Kappa', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'K', name: 'Lambda', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'L', name: 'Mu', type: 'consonant', housing: 'sqrt(51)' },
        { letter: 'M', name: 'Nu', type: 'consonant', housing: 'sqrt(51)' }
    ],
    descending: [
        { letter: 'N', name: 'Xi', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'O', name: 'Omicron', type: 'pivot', housing: 'VOID' }, // O is the Pivot
        { letter: 'P', name: 'Pi', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'Q', name: 'Rho', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'R', name: 'Sigma', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'S', name: 'Tau', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'T', name: 'Upsilon', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'U', name: 'Phi', type: 'vowel', housing: 'sqrt(42)' },
        { letter: 'V', name: 'Chi', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'W', name: 'Psi', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'X', name: 'Omega', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'Y', name: 'Stigma', type: 'consonant', housing: 'sqrt(42)' },
        { letter: 'Z', name: 'Sampi', type: 'consonant', housing: 'sqrt(42)' }
    ]
};

/**
 * NOTES 12: Chromatic / Pentatonic Scale
 */
const NOTES_12 = [
    { note: 'C', pentatonic: true },
    { note: 'C#', pentatonic: false },
    { note: 'D', pentatonic: true },
    { note: 'D#', pentatonic: false },
    { note: 'E', pentatonic: true },
    { note: 'F', pentatonic: false },
    { note: 'F#', pentatonic: false },
    { note: 'G', pentatonic: true },
    { note: 'G#', pentatonic: false },
    { note: 'A', pentatonic: true },
    { note: 'A#', pentatonic: false },
    { note: 'B', pentatonic: false }
];

interface Geofont13ShaderProps {
    time: number;
}

export const Geofont13Shader: React.FC<Geofont13ShaderProps> = ({ time }) => {
    // Rotation calculations: 13-point logic
    const rotAlpha = time * 10;
    const rotNotes = time * 10 * (13 / 12);

    // Current indices under the Root 42 Dial
    const currentIdxAlpha = Math.floor(((rotAlpha + 360) % 360) / (360 / 13)) % 13;
    const currentIdxNotes = Math.floor(((rotNotes + 360) % 360) / (360 / 12)) % 12;

    const activeAscending = GEOFONTS_ALPHA.ascending[(13 - currentIdxAlpha) % 13];
    const activeDescending = GEOFONTS_ALPHA.descending[(13 - currentIdxAlpha) % 13];
    const activeNote = NOTES_12[(12 - currentIdxNotes) % 12];

    // VERBAL INTERFACE STATE
    const [activeIndex, setActiveIndex] = React.useState(-1);
    const [isSequencing, setIsSequencing] = React.useState(false);

    const playAlphaSequence = async () => {
        if (isSequencing) return;
        setIsSequencing(true);
        const sequence = "ALPHA";
        for (let i = 0; i < sequence.length; i++) {
            setActiveIndex(i);
            audioEngine.playLetter(sequence[i]);
            await new Promise(resolve => setTimeout(resolve, 600));
        }
        setActiveIndex(-1);
        setIsSequencing(false);
    };

    // SONIFICATION: Trigger letter tones on transition
    useEffect(() => {
        if (activeAscending) {
            audioEngine.playLetter(activeAscending.letter);
        }
        if (activeDescending && activeDescending.type !== 'pivot') {
            audioEngine.playLetter(activeDescending.letter);
        }
    }, [activeAscending.letter, activeDescending.letter]);

    return (
        <div className="w-full h-full relative flex items-center justify-center bg-black overflow-hidden border border-zinc-900 font-mono">

            {/* Perspective Viewport */}
            <div className="relative w-full h-full flex items-center justify-center" style={{ perspective: '1000px' }}>

                {/* 3D Flat-Platter Rotation */}
                <motion.div
                    className="relative flex items-center justify-center"
                    animate={{ rotateX: 65 }}
                    transition={{ ease: "linear" }}
                    style={{ transformStyle: 'preserve-3d' }}
                >
                    <svg viewBox="-300 -300 600 600" className="w-[800px] h-[800px] overflow-visible">

                        {/* Reference Grid (Root 42 Lines) */}
                        <g opacity="0.1">
                            {Array.from({ length: 12 }).map((_, i) => (
                                <line
                                    key={`grid-${i}`}
                                    x1="0" y1="0"
                                    x2={Math.cos((i / 6) * Math.PI) * 300}
                                    y2={Math.sin((i / 6) * Math.PI) * 300}
                                    stroke="white" strokeWidth="0.5"
                                />
                            ))}
                            <circle cx="0" cy="0" r="100" fill="none" stroke="white" strokeWidth="0.5" />
                            <circle cx="0" cy="0" r="200" fill="none" stroke="white" strokeWidth="0.5" />
                        </g>

                        {/* OUTER DISC (ASCENDING / DESCENDING PAIRS) */}
                        <motion.g animate={{ rotate: rotAlpha }} transition={{ ease: "linear" }}>
                            <circle cx="0" cy="0" r="250" fill="none" stroke="rgba(255, 60, 100, 0.1)" strokeWidth="40" />
                            {GEOFONTS_ALPHA.ascending.map((item, i) => {
                                const angle = (i / 13) * Math.PI * 2 - Math.PI / 2;
                                const r = 250;
                                const x = Math.cos(angle) * r;
                                const y = Math.sin(angle) * r;
                                const descItem = GEOFONTS_ALPHA.descending[i];

                                return (
                                    <g key={`pair13-${i}`} transform={`translate(${x}, ${y})`}>
                                        {/* Ascending Character (Top) */}
                                        <text
                                            textAnchor="middle"
                                            alignmentBaseline="middle"
                                            fill={item.type === 'vowel' ? '#ff3c64' : '#ffffff'}
                                            fontSize="22"
                                            fontWeight="bold"
                                            style={{ transform: `rotate(${-rotAlpha}deg) translateY(-8px)` }}
                                        >
                                            {item.letter}
                                        </text>
                                        {/* Descending Character (Bottom) */}
                                        <text
                                            textAnchor="middle"
                                            alignmentBaseline="middle"
                                            fill={descItem.type === 'pivot' ? '#ffcc00' : '#3c82ff'}
                                            fontSize="16"
                                            fontWeight="light"
                                            opacity="0.8"
                                            style={{ transform: `rotate(${-rotAlpha}deg) translateY(12px)` }}
                                        >
                                            {descItem.letter}
                                        </text>
                                    </g>
                                );
                            })}
                        </motion.g>

                        {/* INNER DISC (12 NOTES) */}
                        <motion.g animate={{ rotate: rotNotes }} transition={{ ease: "linear" }}>
                            <circle cx="0" cy="0" r="160" fill="none" stroke="rgba(60, 130, 255, 0.1)" strokeWidth="30" />
                            {NOTES_12.map((item, i) => {
                                const angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
                                const r = 160;
                                const x = Math.cos(angle) * r;
                                const y = Math.sin(angle) * r;
                                return (
                                    <g key={`note12-${i}`} transform={`translate(${x}, ${y})`}>
                                        <text
                                            textAnchor="middle"
                                            alignmentBaseline="middle"
                                            fill={item.pentatonic ? '#3c82ff' : 'rgba(255,255,255,0.4)'}
                                            fontSize="14"
                                            fontWeight="bold"
                                            style={{ transform: `rotate(${-rotNotes}deg)` }}
                                        >
                                            {item.note}
                                        </text>
                                    </g>
                                );
                            })}
                        </motion.g>

                        {/* CENTER - THE O PIVOT (ABSOLUTE VOID) */}
                        <g transform="translate(0, 0)">
                            <circle r="40" fill="rgba(0,0,0,0.9)" stroke="#ffcc00" strokeWidth="1" strokeDasharray="4 4" />
                            <text textAnchor="middle" alignmentBaseline="middle" fill="#ffcc00" fontSize="36" fontWeight="bold">O</text>
                            <text y="20" textAnchor="middle" fill="#ffcc00" fontSize="8" tracking="0.2em">PIVOT</text>
                        </g>

                        {/* THE ROOT 42 DIAL (The Needle) */}
                        <g transform="translate(0, -280)">
                            <path d="M -10 0 L 0 50 L 10 0 Z" fill="#ff3c64" />
                            <text x="0" y="-10" textAnchor="middle" fill="#ff3c64" fontSize="12" fontWeight="bold">ROOT 42 READING LINE</text>
                        </g>

                    </svg>
                </motion.div>
            </div>

            {/* LIVE READING PANEL */}
            <div className="absolute top-10 left-10 p-6 bg-zinc-900/90 border border-zinc-800 rounded-xl backdrop-blur-xl shadow-2xl space-y-4">
                <div className="flex flex-col gap-1 border-b border-zinc-800 pb-2">
                    <span className="text-[10px] text-zinc-500 tracking-widest uppercase">Refractive Pair (26)</span>
                    <div className="flex items-end gap-2 text-3xl font-bold text-white">
                        <span className="text-rose-500">{activeAscending.letter}</span>
                        <span className="text-zinc-600">/</span>
                        <span className="text-blue-500">{activeDescending.letter}</span>
                        <span className="text-[10px] font-mono text-zinc-500 mb-1">LOCK: {(rotAlpha % 360).toFixed(4)}</span>
                    </div>
                </div>

                <div className="flex flex-col gap-1 border-b border-zinc-800 pb-2">
                    <span className="text-[10px] text-zinc-500 tracking-widest uppercase">Resonance Note (12)</span>
                    <div className="flex items-end gap-2 text-3xl font-bold text-white">
                        <span className="text-amber-400">{activeNote.note}</span>
                        <span className="text-[10px] tracking-wide text-zinc-500 mb-1 uppercase">
                            {activeNote.pentatonic ? 'Pentatonic' : 'Chromatic'}
                        </span>
                    </div>
                </div>

                <div className="flex flex-col gap-1">
                    <span className="text-[10px] text-zinc-500 tracking-widest uppercase">Möbius Gear Ratio</span>
                    <span className="text-emerald-400 font-mono text-xl">1.0833 (13:12)</span>
                </div>
            </div>

            {/* VERBAL DIAGNOSTIC INTERFACE */}
            <motion.div
                initial={{ x: 50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="absolute top-10 right-80 p-6 bg-rose-950/20 border border-rose-500/30 rounded-xl backdrop-blur-xl shadow-2xl space-y-4"
            >
                <div className="flex justify-between items-center border-b border-rose-500/20 pb-2">
                    <span className="text-[10px] text-rose-500 tracking-widest uppercase font-bold">Verbal Diagnostic Interface</span>
                    <div className={`w-2 h-2 rounded-full ${isSequencing ? 'bg-rose-500 animate-pulse' : 'bg-zinc-800'}`} />
                </div>

                <div className="flex gap-4 py-2">
                    {"ALPHA".split("").map((char, i) => (
                        <motion.div
                            key={`diagnostic-${i}`}
                            animate={{
                                scale: activeIndex === i ? 1.4 : 1,
                                color: activeIndex === i ? "#ff3c64" : "rgba(255,255,255,0.3)",
                                textShadow: activeIndex === i ? "0 0 20px rgba(255,60,100,0.8)" : "none"
                            }}
                            className="text-4xl font-black font-mono"
                        >
                            {char}
                        </motion.div>
                    ))}
                </div>

                <div className="space-y-2">
                    <button
                        onClick={playAlphaSequence}
                        disabled={isSequencing}
                        className="w-full py-3 bg-rose-600/20 hover:bg-rose-600/40 border border-rose-500/50 rounded text-[10px] uppercase font-bold tracking-[0.3em] text-rose-500 transition-all active:scale-95 disabled:opacity-20 disabled:cursor-not-allowed"
                    >
                        {isSequencing ? "RESONATING..." : "IGNITE ALPHA SEQUENCE"}
                    </button>
                    {activeIndex !== -1 && (
                        <div className="text-center font-mono text-[8px] text-zinc-500 uppercase tracking-tighter">
                            Transmitting Frequency: <span className="text-rose-400">Node {activeIndex === 0 || activeIndex === 4 ? "01" : activeIndex === 1 ? "12" : activeIndex === 2 ? "16" : "08"}</span>
                        </div>
                    )}
                </div>
            </motion.div>

            <div className="absolute bottom-10 right-10 flex flex-col items-end gap-2">
                <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-lg">
                    <span className="text-[8px] text-zinc-500 uppercase block tracking-widest mb-1">Scale Synchronizer</span>
                    <div className="flex gap-4">
                        <div className="text-center">
                            <span className="text-[8px] text-zinc-600 block">PHI</span>
                            <span className="text-sm font-bold text-zinc-300">1.618</span>
                        </div>
                        <div className="text-center">
                            <span className="text-[8px] text-zinc-600 block">PI</span>
                            <span className="text-sm font-bold text-zinc-300">3.142</span>
                        </div>
                        <div className="text-center">
                            <span className="text-[8px] text-zinc-600 block">ROOT 42</span>
                            <span className="text-sm font-bold text-rose-500">6.481</span>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
};
