import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

const PHI = (1 + Math.sqrt(5)) / 2;
const EULER = Math.E;
const PI = Math.PI;

interface EscapeShaderProps {
    time: number;
    perturbation?: number;
}

export const EscapeShader: React.FC<EscapeShaderProps> = ({
    time,
    perturbation = 0.5
}) => {
    // The 12/13 Hardcard Intersection
    const STAFF_TWELVE = 12;
    const CLAW_THIRTEEN = 13;
    const VITRIFICATION_RATIO = STAFF_TWELVE / CLAW_THIRTEEN;

    // Generate trajectories for φ, e, and π
    const trajectories = useMemo(() => {
        const points = 100;

        const generatePath = (constant: number, offsetAngle: number, scale: number) => {
            let pathD = `M 0 0`;
            for (let i = 1; i < points; i++) {
                // Growth influenced by the mathematical constant
                const t = (i / points) * Math.PI * 4;
                const radius = Math.pow(constant, t * 0.2) * scale * 10;

                // Add perturbation based on the unwobbling pivot
                const wobble = Math.sin(time * 2 + i * 0.1) * perturbation * 15;

                const angle = t + offsetAngle + (wobble * 0.01);
                const x = Math.cos(angle) * (radius + wobble);
                const y = Math.sin(angle) * (radius + wobble);

                pathD += ` L ${x} ${y}`;
            }
            return pathD;
        };

        return {
            phi: generatePath(PHI, 0, 1.2),           // Golden ratio spiral
            e: generatePath(EULER, Math.PI * 0.66, 0.8), // Exponential growth path
            pi: generatePath(PI, Math.PI * 1.33, 0.9)  // Transcendental circular limit
        };
    }, [time, perturbation]);

    return (
        <div className="w-full h-full relative flex items-center justify-center bg-[#050508] rounded-3xl overflow-hidden border border-zinc-800">
            <svg viewBox="-200 -200 400 400" className="w-full h-full max-w-[600px]">
                {/* The Unwobbling Pivot Background */}
                <circle
                    cx="0" cy="0" r={180 * VITRIFICATION_RATIO}
                    fill="none"
                    stroke="rgba(255, 255, 255, 0.03)"
                    strokeWidth="1"
                    strokeDasharray="4 4"
                />
                <circle
                    cx="0" cy="0" r={180}
                    fill="none"
                    stroke="rgba(16, 185, 129, 0.05)"
                    strokeWidth="0.5"
                />

                {/* The 12-Fold Staff (Base Matrix) */}
                {Array.from({ length: STAFF_TWELVE }).map((_, i) => {
                    const angle = (i / STAFF_TWELVE) * Math.PI * 2 + time * 0.1;
                    return (
                        <line
                            key={`staff-${i}`}
                            x1="0" y1="0"
                            x2={Math.cos(angle) * 180 * VITRIFICATION_RATIO}
                            y2={Math.sin(angle) * 180 * VITRIFICATION_RATIO}
                            stroke="rgba(255, 255, 255, 0.08)"
                            strokeWidth="1"
                        />
                    );
                })}

                {/* The Escape Trajectories */}

                {/* 1. Phi (The Fruit / Pentagonal Life) */}
                <motion.g animate={{ rotate: time * 10 }} transition={{ ease: "linear" }}>
                    <path
                        d={trajectories.phi}
                        fill="none"
                        stroke="#f59e0b" // Amber
                        strokeWidth="2"
                        strokeLinecap="round"
                        opacity={0.8}
                    />
                    <text x="0" y="-190" fill="#f59e0b" fontSize="8" className="font-mono tracking-widest text-center" textAnchor="middle">
                        φ ESCAPE (ORGANIC)
                    </text>
                </motion.g>

                {/* 2. Euler (Growth Constant / The Cube) */}
                <motion.g animate={{ rotate: -time * 8 }} transition={{ ease: "linear" }}>
                    <path
                        d={trajectories.e}
                        fill="none"
                        stroke="#10b981" // Emerald
                        strokeWidth="2"
                        strokeLinecap="round"
                        opacity={0.8}
                    />
                    <text x="-160" y="100" fill="#10b981" fontSize="8" className="font-mono tracking-widest text-center" textAnchor="middle" transform="rotate(-60, -160, 100)">
                        e ESCAPE (KINETIC)
                    </text>
                </motion.g>

                {/* 3. Pi (The Circular Limit / Equator) */}
                <motion.g animate={{ rotate: time * 5 }} transition={{ ease: "linear" }}>
                    <path
                        d={trajectories.pi}
                        fill="none"
                        stroke="#3b82f6" // Blue
                        strokeWidth="2"
                        strokeLinecap="round"
                        opacity={0.8}
                    />
                    <text x="160" y="100" fill="#3b82f6" fontSize="8" className="font-mono tracking-widest text-center" textAnchor="middle" transform="rotate(60, 160, 100)">
                        π ESCAPE (LIMIT)
                    </text>
                </motion.g>

                {/* The 12/13 Hardcard / Camera Obscura Point */}
                <motion.circle
                    cx="0" cy="0" r={4 + perturbation * 5}
                    fill="#f43f5e" // Rose (The Pivot)
                    className="animate-pulse"
                />
                <circle cx="0" cy="0" r="1.5" fill="#fff" />

                {/* Perturbation Rings */}
                {perturbation > 0.2 && (
                    <motion.circle
                        cx="0" cy="0"
                        r={perturbation * 40}
                        fill="none"
                        stroke="#f43f5e"
                        strokeWidth="0.5"
                        strokeDasharray="2 4"
                        animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.8, 0.3] }}
                        transition={{ duration: 1 / perturbation, repeat: Infinity }}
                    />
                )}
            </svg>

            {/* Dimensional Output HUD */}
            <div className="absolute bottom-4 right-4 text-right">
                <span className="text-[8px] text-zinc-500 uppercase block">Total Internal Reflection</span>
                <span className="text-sm font-mono text-rose-400">12/13 [HARDCARD]</span>
            </div>
            <div className="absolute top-4 left-4">
                <span className="text-[8px] text-zinc-500 uppercase block tracking-widest">Unwobbling Pivot</span>
                <span className="text-sm font-mono text-emerald-400">
                    Δ {perturbation.toFixed(3)}
                </span>
            </div>
        </div>
    );
};
