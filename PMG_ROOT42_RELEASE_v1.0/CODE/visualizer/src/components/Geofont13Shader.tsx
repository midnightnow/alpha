import React, { useMemo } from 'react';
import { motion } from 'motion/react';

const OLYMPIANS = [
    { letter: 'B', name: 'Athena', type: 'consonant' },
    { letter: 'A', name: 'Zeus', type: 'vowel', highlight: '#3b82f6' }, // Sky/Pi
    { letter: 'C', name: 'Aphrodite', type: 'consonant' },
    { letter: 'D', name: 'Hermes', type: 'consonant' },
    { letter: 'E', name: 'Demeter', type: 'vowel', highlight: '#10b981' }, // Earth/e
    { letter: 'F', name: 'Hephaestus', type: 'consonant' },
    { letter: 'I', name: 'Apollo', type: 'vowel', highlight: '#f59e0b' }, // Light/Phi
    { letter: 'G', name: 'Artemis', type: 'consonant' },
    { letter: 'H', name: 'Ares', type: 'consonant' },
    { letter: 'O', name: 'Poseidon', type: 'vowel', highlight: '#60a5fa' }, // Sea/O
    { letter: 'J', name: 'Hera', type: 'consonant' },
    { letter: 'U', name: 'Hestia', type: 'vowel', highlight: '#f43f5e' }  // Hearth/U
];

interface Geofont13ShaderProps {
    time: number;
    pulseFrequency?: number;
}

export const Geofont13Shader: React.FC<Geofont13ShaderProps> = ({
    time,
    pulseFrequency = 0.66
}) => {
    // Generate the inversion rays (CAMERA -> O -> BSCURA)
    const rays = useMemo(() => {
        return Array.from({ length: 6 }).map((_, i) => {
            const angle = (i / 6) * Math.PI * 2 + time * 0.2;
            return { id: i, angle };
        });
    }, [time]);

    // The Hades Gap pulse
    const pulse = (Math.sin(time * Math.PI * 2 * pulseFrequency) + 1) / 2;

    return (
        <div className="w-full h-full relative flex items-center justify-center bg-[#000000] rounded-3xl overflow-hidden border border-zinc-900">
            {/* 3D Perspective Container */}
            <div className="w-full h-full" style={{ perspective: '800px' }}>
                <motion.div
                    className="w-full h-full flex items-center justify-center"
                    animate={{ rotateX: 60, rotateZ: time * 5 }}
                    transition={{ ease: "linear" }}
                    style={{ transformStyle: 'preserve-3d' }}
                >
                    <svg viewBox="-200 -200 400 400" className="w-[800px] h-[800px] overflow-visible">
                        {/* The Ideal Sphere (Wireframe) */}
                        <circle cx="0" cy="0" r="160" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="0.5" />
                        <ellipse cx="0" cy="0" rx="160" ry="40" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="0.5" />
                        <ellipse cx="0" cy="0" rx="40" ry="160" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="0.5" />

                        {/* The 12/13 Hardcard (Luminous Plane) */}
                        <motion.circle
                            cx="0" cy="0"
                            r={160 * (12 / 13)}
                            fill={`rgba(16, 185, 129, ${0.05 + pulse * 0.05})`}
                            stroke="rgba(16, 185, 129, 0.4)"
                            strokeWidth="1"
                            strokeDasharray="4 4"
                            style={{ transform: `translateZ(-20px)` }}
                        />

                        {/* Central Axis (The Pivot) */}
                        <line x1="0" y1="0" x2="0" y2="0" stroke="white" strokeWidth="2" style={{ transform: 'translateZ(-100px) scaleZ(200)' }} />

                        {/* The 12 Olympian Letters on Circumference */}
                        {OLYMPIANS.map((god, i) => {
                            const angle = (i / 12) * Math.PI * 2;
                            const r = 160 * (12 / 13);
                            const x = Math.cos(angle) * r;
                            const y = Math.sin(angle) * r;
                            const isVowel = god.type === 'vowel';

                            return (
                                <g key={`god-${i}`} transform={`translate(${x}, ${y})`}>
                                    <circle
                                        cx="0" cy="0"
                                        r={isVowel ? 3 : 1}
                                        fill={isVowel ? god.highlight : 'rgba(255,255,255,0.3)'}
                                    />
                                    {/* Keep text upright against the parent rotation */}
                                    <motion.text
                                        x="0" y="-10"
                                        fill={isVowel ? god.highlight : 'rgba(255,255,255,0.3)'}
                                        fontSize={isVowel ? "12" : "8"}
                                        fontWeight={isVowel ? "bold" : "normal"}
                                        textAnchor="middle"
                                        animate={{ rotateX: -60, rotateZ: -time * 5 }}
                                    >
                                        {god.letter}
                                    </motion.text>
                                </g>
                            );
                        })}

                        {/* CAMERA -> O -> BSCURA Inversion Rays */}
                        <g>
                            {rays.map((ray, i) => {
                                const r = 160 * (12 / 13);
                                const xOut = Math.cos(ray.angle) * r;
                                const yOut = Math.sin(ray.angle) * r;

                                return (
                                    <motion.g key={`ray-${i}`}>
                                        {/* Incoming Light (CAMERA) */}
                                        <line
                                            x1={-xOut} y1={-yOut}
                                            x2="0" y2="0"
                                            stroke="rgba(255, 255, 255, 0.4)"
                                            strokeWidth="1.5"
                                            strokeDasharray="2 4"
                                            style={{ transform: `translateZ(50px)` }}
                                        />
                                        {/* Outgoing Light Flipped (BSCURA) */}
                                        <line
                                            x1="0" y1="0"
                                            x2={xOut} y2={yOut}
                                            stroke={`rgba(16, 185, 129, ${0.4 + pulse * 0.4})`}
                                            strokeWidth="1.5"
                                            style={{ transform: `translateZ(-50px)` }}
                                        />
                                    </motion.g>
                                );
                            })}
                        </g>

                        {/* The Silent Ω (Center Point) */}
                        <g transform="translate(0, 0)">
                            {/* Pulse Rings */}
                            <motion.circle
                                cx="0" cy="0" r={10 + pulse * 20}
                                fill="none"
                                stroke="rgba(244, 63, 94, 0.5)"
                                strokeWidth="0.5"
                            />
                            <motion.circle
                                cx="0" cy="0" r="4"
                                fill="rgba(244, 63, 94, 0.9)"
                            />

                            <motion.text
                                x="0" y="4"
                                fill="#ffffff"
                                fontSize="10"
                                fontWeight="bold"
                                textAnchor="middle"
                                animate={{ rotateX: -60, rotateZ: -time * 5 }}
                                style={{ transform: 'translateZ(10px)' }}
                            >
                                Ω
                            </motion.text>
                        </g>
                    </svg>
                </motion.div>
            </div>

            {/* HUD Status Elements */}
            <div className="absolute top-4 left-4 bg-black/60 p-2 border border-white/5 rounded backdrop-blur max-w-[200px]">
                <h3 className="text-[10px] text-zinc-500 tracking-widest uppercase mb-1">OGC-13 Parity Flip</h3>
                <div className="flex flex-col gap-1 text-xs font-mono text-zinc-400">
                    <div className="flex justify-between"><span>CAMERA</span> <span className="text-white">+Light</span></div>
                    <div className="flex justify-between border-y border-white/10 py-1"><span>Ω (O)</span> <span className="text-rose-400">0.00 Hz</span></div>
                    <div className="flex justify-between"><span>BSCURA</span> <span className="text-emerald-400">-Dark</span></div>
                </div>
            </div>

            <div className="absolute bottom-4 right-4 text-right">
                <span className="text-[8px] text-zinc-500 uppercase tracking-widest block">Silent Center Pulse</span>
                <span className="text-sm font-mono text-rose-400">{(pulseFrequency).toFixed(2)} Hz</span>
            </div>
        </div>
    );
};
