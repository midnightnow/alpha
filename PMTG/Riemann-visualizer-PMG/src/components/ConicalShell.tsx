import React, { useMemo } from 'react';
import { motion } from 'motion/react';
import { Shell, Lock, Zap } from 'lucide-react';

interface ConicalShellProps {
    t: number;
    time: number;
}

const TOTAL_NODES = 93;
const ROOT_42 = Math.sqrt(42);

export const ConicalShell: React.FC<ConicalShellProps> = ({ t, time }) => {
    const nodes = useMemo(() => {
        return Array.from({ length: TOTAL_NODES }, (_, i) => {
            const n = i + 1;
            // Conical mapping
            const radius = n * 1.5;
            const height = n * 2.5;
            // Wrapping to mod 24 as suggested
            const angle = (n % 24) * (Math.PI * 2 / 24) + time * 0.1;

            // Root 42 Radiation Arms logic
            // We look for resonance with the root 42 axis
            const radiationResonance = Math.abs((n % ROOT_42) - (ROOT_42 / 2));
            const vitrified = (n % 42 === 0) || (Math.abs(n - 42) < 2);

            const x = 200 + Math.cos(angle) * radius;
            const y = 200 + Math.sin(angle) * radius - (height * 0.5); // Isometric-ish lift

            return {
                id: n,
                x,
                y,
                radius,
                height,
                vitrified,
                resonance: radiationResonance,
                prime: isPrime(n)
            };
        });
    }, [time]);

    return (
        <div className="w-full h-full relative flex items-center justify-center bg-[#080808] rounded-3xl border border-white/5 overflow-hidden">
            <div className="absolute top-4 left-4 flex items-center gap-2">
                <Shell className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold uppercase tracking-widest text-emerald-400">Vitrified Conical Shell</h3>
            </div>

            <svg viewBox="0 0 400 400" className="w-full h-full max-w-[500px]">
                {/* Conical Guide Lines */}
                <path
                    d="M 200 50 L 50 350 L 350 350 Z"
                    fill="none"
                    stroke="rgba(16,185,129,0.05)"
                    strokeWidth="1"
                />

                {/* Radiation Arms (Root 42) */}
                {Array.from({ length: 6 }).map((_, i) => {
                    const angle = (i * Math.PI * 2 / 6) + time * 0.05;
                    return (
                        <line
                            key={i}
                            x1="200" y1="200"
                            x2={200 + Math.cos(angle) * 200}
                            y2={200 + Math.sin(angle) * 200}
                            stroke="rgba(244,63,94,0.1)"
                            strokeWidth="0.5"
                            strokeDasharray="4 4"
                        />
                    );
                })}

                {nodes.map((node) => {
                    const isPrime = node.prime;
                    const color = node.vitrified ? '#fbbf24' : isPrime ? '#10b981' : '#27272a';
                    const size = node.vitrified ? 4 : isPrime ? 3 : 1.5;

                    return (
                        <motion.g key={node.id}>
                            {/* Node connection to center */}
                            <line
                                x1="200" y1="200"
                                x2={node.x} y2={node.y}
                                stroke={`rgba(16,185,129, ${0.1 * (1 - node.id / 93)})`}
                                strokeWidth="0.5"
                            />

                            <motion.circle
                                cx={node.x}
                                cy={node.y}
                                r={size}
                                fill={color}
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className={node.vitrified ? 'shadow-[0_0_10px_#fbbf24]' : ''}
                            />

                            {node.vitrified && (
                                <text
                                    x={node.x + 5}
                                    y={node.y}
                                    className="text-[8px] fill-amber-400 font-mono"
                                >
                                    VIT-42
                                </text>
                            )}
                        </motion.g>
                    );
                })}
            </svg>

            <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end backdrop-blur-sm bg-black/40 p-3 rounded-xl border border-white/5">
                <div>
                    <span className="text-[8px] text-zinc-500 uppercase block">Stabilisation Axis</span>
                    <span className="text-xs font-mono text-emerald-400">ROOT 42 SOLUTION</span>
                </div>
                <div className="text-right">
                    <span className="text-[8px] text-zinc-500 uppercase block">Hades Lock status</span>
                    <div className="flex items-center gap-1">
                        <Lock className="w-3 h-3 text-amber-400" />
                        <span className="text-xs font-mono text-amber-400">VITRIFIED</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Simple primality check
function isPrime(num: number) {
    if (num <= 1) return false;
    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) return false;
    }
    return true;
}
