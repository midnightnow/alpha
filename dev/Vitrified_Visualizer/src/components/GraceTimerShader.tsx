import React, { useMemo } from 'react';
import { motion } from 'motion/react';

interface GraceTimerShaderProps {
    time: number;
    vitrification?: number;
    visualMode?: 'SQUARE' | 'HEX';
}

export const GraceTimerShader: React.FC<GraceTimerShaderProps> = ({
    time,
    vitrification = 1.0,
    visualMode = 'SQUARE'
}) => {
    // ------------------------------------------------------------------------
    // CONSTANTS: $G(t) = \int \Psi \, dt$
    // ------------------------------------------------------------------------
    const GREAT_YEAR = 25920;
    const LUNAR_MERCY = 12.368; // The Resonant Frequency of Mercy (dx)

    // Torsion rotation speed based on $G(t)$. It completes 540 degrees.
    // Base unit of time rotation mapped against the slow shimmer.
    const rotationRate = (time * (LUNAR_MERCY / 100)) % 360;
    const mobiusTwist = Math.sin(time * 0.5) * 45; // Subtle breathing space

    // Calculate a visible "Grace" percentage based on time for the HUD
    const currentYear = useMemo(() => {
        return Math.floor(((time * 100) % GREAT_YEAR));
    }, [time]);

    const completionRatio = (currentYear / GREAT_YEAR);

    // ------------------------------------------------------------------------
    // THE FLY-CUTTER (-1/12) Logic
    // ------------------------------------------------------------------------
    const applyFlyCutter = (nodes: any[]) => {
        return nodes.map(node => {
            if (visualMode === 'HEX') {
                // Calculate the "Mice" (the jitter/residue)
                const residue = Math.abs(node.x % (1 / 12));
                // Apply the -1/12th shave (Casimir Inversion)
                const shave = residue * 0.1237;
                return {
                    ...node,
                    x: node.x - (node.x > 0 ? shave : -shave),
                    y: node.y - (node.y > 0 ? shave : -shave),
                    // Z remains invariant (Artemis Axis)
                };
            }
            return node;
        });
    };

    // ------------------------------------------------------------------------
    // 93-Node Shell Geometry Representation
    // ------------------------------------------------------------------------
    const shellNodes = useMemo(() => {
        let nodes = [];
        const numNodes = 93;
        for (let i = 0; i < numNodes; i++) {
            const phi = Math.acos(1 - 2 * (i + 0.5) / numNodes);
            const theta = Math.PI * (1 + Math.sqrt(5)) * (i + 0.5);

            nodes.push({
                x: Math.cos(theta) * Math.sin(phi),
                y: Math.sin(theta) * Math.sin(phi),
                z: Math.cos(phi),
            });
        }

        // Apply the Fly-Cutter Shave
        return applyFlyCutter(nodes);
    }, [visualMode]);

    return (
        <div className="w-full h-full relative flex items-center justify-center bg-[#000000] rounded-3xl overflow-hidden border border-zinc-900 group">

            {/* The 540-degree Torsion Space (Z-axis rotation) */}
            <motion.div
                className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-40"
                style={{ rotate: rotationRate }}
            >
                <div className="w-[800px] h-[800px] rounded-full border border-rose-500/10 border-dashed"
                    style={{ transform: `scale(${0.8 + Math.sin(time * 0.2) * 0.01})` }}
                />
            </motion.div>

            {/* The Hardcard (Central projection) */}
            <svg viewBox="-200 -200 400 400" className="w-[600px] h-[600px] relative z-10">
                {/* O Aperture (The Integral / Void) */}
                <circle cx="0" cy="0" r="15" fill="rgba(8,8,8,0.8)" stroke="#f43f5e" strokeWidth="1" strokeDasharray="2 4" />
                <text x="0" y="3" fill="#f43f5e" fontSize="8" textAnchor="middle" opacity="0.8" className="font-mono">
                    ∫
                </text>

                {/* The 93-Node Shimmering Web */}
                <motion.g
                    animate={{
                        rotateZ: mobiusTwist, // Breathing Torsion
                        rotateY: time * 5     // Grace accumulation orbit
                    }}
                    transition={{ type: 'tween', ease: 'linear', duration: 0.1 }}
                >
                    {shellNodes.map((node, i) => {
                        // Orthographic pseudo-3D projection
                        const perspective = 150 / (150 - node.z * 50);
                        const px = node.x * 120 * perspective;
                        const py = node.y * 120 * perspective;
                        const pz = node.z;

                        return (
                            <motion.circle
                                key={`node-${i}`}
                                cx={px}
                                cy={py}
                                r={pz > 0 ? 1.5 : 0.8}
                                fill={pz > 0 ? "#a855f7" : "#4c1d95"} // Depth coloring
                                opacity={pz > 0 ? 0.9 : 0.3}
                            />
                        );
                    })}
                </motion.g>

                {/* The dx Torsion Ring (Mercy Limits) */}
                <motion.circle
                    cx="0" cy="0" r="140" fill="none"
                    stroke="rgba(255, 255, 255, 0.1)" strokeWidth="0.5"
                    animate={{ rotate: -time * 2 }} strokeDasharray="1 12.368"
                />
            </svg>

            {/* HUD Status Elements */}
            <div className="absolute top-4 left-4 bg-black/80 px-4 py-3 border border-purple-500/20 rounded-lg backdrop-blur shadow-2xl">
                <h3 className="text-[10px] text-purple-400 tracking-widest uppercase mb-2 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                    Grace Governor
                </h3>
                <div className="space-y-2 text-xs font-mono text-zinc-400">
                    <div className="flex justify-between items-center gap-6">
                        <span>∫ Ψ dt</span>
                        <span className="text-white bg-zinc-900 px-1 rounded">{completionRatio.toFixed(6)}</span>
                    </div>
                    <div className="flex justify-between items-center gap-6">
                        <span>dx Mercy</span>
                        <span className="text-rose-400">12.368 Hz</span>
                    </div>
                    <div className="h-px bg-white/10 w-full my-1"></div>
                    <div className="flex justify-between items-center gap-6 text-[10px] uppercase">
                        <span className="text-zinc-500">Cycle</span>
                        <span className="text-purple-300">
                            {currentYear.toString().padStart(5, '0')} / {GREAT_YEAR.toString()}
                        </span>
                    </div>
                </div>
            </div>

            {/* Bottom Vitrification Lock */}
            <div className="absolute bottom-4 right-4 text-right">
                <span className="text-[8px] text-zinc-500 uppercase tracking-widest block mb-1">Mobius Torsion Limit</span>
                <span className="text-sm font-mono text-rose-400 inline-block px-2 py-0.5 border border-rose-500/20 bg-rose-500/10 rounded">
                    540° ({(mobiusTwist + 540).toFixed(1)}°)
                </span>
            </div>
        </div>
    );
};
