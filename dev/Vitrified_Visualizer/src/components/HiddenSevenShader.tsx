import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface HiddenSevenShaderProps {
    time: number;
    tension?: number; // Representing Hades Gap slop / tension
}

export const HiddenSevenShader: React.FC<HiddenSevenShaderProps> = ({
    time,
    tension = 0.5
}) => {
    // 12-Fold Outer Frame (The Straight Integer World)
    const twelveVectors = useMemo(() => {
        return Array.from({ length: 12 }).map((_, i) => {
            const angle = (i / 12) * Math.PI * 2;
            return { id: i, angle };
        });
    }, []);

    // 7-Fold Inner Engine (The Curved Root 42 World)
    const sevenArcs = useMemo(() => {
        return Array.from({ length: 7 }).map((_, i) => {
            const angle = (i / 7) * Math.PI * 2 + time * 0.3;
            return { id: i, angle };
        });
    }, [time]);

    // Bifold Radius constraints
    const STRING_RADIUS = 120; // Represents the 6-foot string
    const BOW_RADIUS = STRING_RADIUS + (48.07 * tension); // Extra curve length representing the 0.4807 tension (Root 42)

    return (
        <div className="w-full h-full relative flex items-center justify-center bg-[#000000] rounded-3xl overflow-hidden border border-zinc-900">
            {/* Dark Room (BSCURA) perspective */}
            <svg viewBox="-200 -200 400 400" className="w-[800px] h-[800px]">

                {/* O Aperture (The 15th Letter / Void / 13th Pivot) */}
                <motion.circle
                    cx="0" cy="0" r={8 + tension * 4}
                    fill="none"
                    stroke="rgba(244, 63, 94, 0.8)"
                    strokeWidth="2"
                    animate={{ scale: [1, 1.2, 1], rotate: time * 10 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                />
                <circle cx="0" cy="0" r="2" fill="#fff" />

                {/* The 12-Vector Outer Frame (Straight Lines) */}
                <g>
                    {twelveVectors.map((vec, i) => {
                        const x = Math.cos(vec.angle) * STRING_RADIUS;
                        const y = Math.sin(vec.angle) * STRING_RADIUS;

                        return (
                            <motion.line
                                key={`vec-12-${i}`}
                                x1="0" y1="0"
                                x2={x} y2={y}
                                stroke="#ef4444" // The "Red Flag" of straightness
                                strokeWidth="1"
                                opacity={0.6}
                                strokeLinecap="square"
                            />
                        );
                    })}
                </g>

                {/* The 7-Fold Inner Engine (Curved Bow-Arcs) */}
                <g>
                    {sevenArcs.map((arc, i) => {
                        const startAngle = arc.angle;
                        const midAngle = startAngle + (Math.PI / 7);
                        const endAngle = startAngle + (Math.PI * 2 / 7);

                        // Points for the quadratic bezier curve shaping the bow
                        const x1 = Math.cos(startAngle) * STRING_RADIUS;
                        const y1 = Math.sin(startAngle) * STRING_RADIUS;

                        const xCtrl = Math.cos(midAngle) * BOW_RADIUS;
                        const yCtrl = Math.sin(midAngle) * BOW_RADIUS;

                        const x2 = Math.cos(endAngle) * STRING_RADIUS;
                        const y2 = Math.sin(endAngle) * STRING_RADIUS;

                        const pathD = `M ${x1} ${y1} Q ${xCtrl} ${yCtrl} ${x2} ${y2}`;

                        return (
                            <motion.path
                                key={`arc-7-${i}`}
                                d={pathD}
                                fill="none"
                                stroke="#a855f7" // Purple Root 42 resonance
                                strokeWidth="2"
                                opacity={0.7 + tension * 0.3}
                                strokeLinecap="round"
                                animate={{ strokeDasharray: ["0, 100", "100, 0"] }}
                                transition={{ duration: 3, repeat: Infinity, repeatType: "reverse", ease: "easeInOut" }}
                            />
                        );
                    })}
                </g>

                {/* Vitrification Lattice Boundary */}
                <circle cx="0" cy="0" r={STRING_RADIUS} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="1" strokeDasharray="2 4" />
                <motion.circle
                    cx="0" cy="0" r={BOW_RADIUS}
                    fill="none"
                    stroke="rgba(168, 85, 247, 0.2)"
                    strokeWidth="0.5"
                    animate={{ rotate: time * -5 }}
                    strokeDasharray="4 8"
                />

                {/* "O" Central Convergence UI markers */}
                <text x="0" y="-12" fill="rgba(244, 63, 94, 0.8)" fontSize="8" fontWeight="bold" textAnchor="middle" tracking="widest">
                    O
                </text>
            </svg>

            {/* HUD Status Elements */}
            <div className="absolute top-4 left-4 bg-black/60 p-2 border border-red-500/20 rounded backdrop-blur max-w-[250px]">
                <h3 className="text-[10px] text-zinc-500 tracking-widest uppercase mb-1">Gordian Interference</h3>
                <div className="flex flex-col gap-1 text-xs font-mono text-zinc-400">
                    <div className="flex justify-between">
                        <span>Outer Paddock [12]</span>
                        <span className="text-red-400">STRAIGHT</span>
                    </div>
                    <div className="flex justify-between border-y border-white/10 py-1">
                        <span>O Aperture [15]</span>
                        <span className="text-rose-400">120/17.14 Hz</span>
                    </div>
                    <div className="flex justify-between">
                        <span>Inner Engine [7]</span>
                        <span className="text-purple-400">CURVED (√42)</span>
                    </div>
                </div>
            </div>

            <div className="absolute bottom-4 right-4 text-right">
                <span className="text-[8px] text-zinc-500 uppercase tracking-widest block">Root 42 Bow Tension (0.48)</span>
                <span className="text-sm font-mono text-purple-400">Δ {tension.toFixed(4)}</span>
            </div>
        </div>
    );
};
