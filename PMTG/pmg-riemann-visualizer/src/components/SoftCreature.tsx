import React, { useMemo } from 'react';
import { motion } from 'motion/react';

interface SoftCreatureProps {
    mobility: number;
    time: number;
    sync: number;
}

export const SoftCreature: React.FC<SoftCreatureProps & { color?: string }> = ({ mobility, time, sync, color = "#e0f2fe" }) => {
    const tentacles = useMemo(() => {
        const count = Math.floor(8 + mobility * 12);
        return Array.from({ length: count }, (_, i) => {
            const angle = (i / count) * Math.PI * 2;
            return { id: i, angle };
        });
    }, [mobility]);

    return (
        <g className="soft-creature">
            {/* Nautilus Body (The Soft Part) */}
            <motion.path
                d="M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z"
                fill={color}
                fillOpacity="0.1"
                stroke={color}
                strokeWidth="0.5"
                animate={{
                    d: [
                        "M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z",
                        "M -22 2 Q -32 -38 0 -52 Q 32 -38 22 2 Z",
                        "M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z"
                    ]
                }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            />
            {/* Stippled Texture Overlay for Body */}
            <path
                d="M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z"
                fill="url(#stippled-pattern)"
                opacity="1"
            />
            {/* Eyes (The Intelligence) */}
            <circle cx="-8" cy="-15" r="1.5" fill="#3e2723" opacity={0.6} />
            <circle cx="8" cy="-15" r="1.5" fill="#3e2723" opacity={0.6} />

            {/* Diamond Dust / Ketheric Trails  */}
            {Array.from({ length: 12 }).map((_, i) => {
                const angle = (i / 12) * Math.PI * 2 + time * 1.5;
                const rad = 15 + Math.sin(time * 0.8 + i) * 12;
                return (
                    <motion.polygon
                        key={`diamond-${i}`}
                        points={`0,-2 2,0 0,2 -2,0`} // Diamond shape
                        fill="#ffffff"
                        animate={{
                            x: Math.cos(angle) * rad,
                            y: Math.sin(angle) * rad - 20,
                            opacity: [0, 0.8, 0],
                            scale: [0.2, 1.5, 0.2],
                            rotate: [0, 180, 360]
                        }}
                        transition={{
                            duration: 2 + Math.random() * 2,
                            repeat: Infinity,
                            delay: i * 0.15,
                            ease: "easeInOut"
                        }}
                        style={{ filter: "drop-shadow(0 0 4px rgba(255,255,255,0.8))" }}
                    />
                );
            })}

            {/* Tentacles (Soft Mobility) */}
            {tentacles.map((t, i) => {
                const length = 40 + mobility * 60;
                const wave = Math.sin(time * 2 + i) * 10;
                const tx = Math.cos(t.angle) * 10;
                const ty = Math.sin(t.angle) * 5 + 10;
                return (
                    <g key={t.id}>
                        <motion.path
                            d={`M ${tx} ${ty} Q ${tx + wave} ${ty + length / 2} ${tx} ${ty + length}`}
                            fill="none"
                            stroke={color}
                            strokeOpacity="0.2"
                            strokeWidth="1.5"
                            strokeLinecap="round"
                            animate={{
                                d: [
                                    `M ${tx} ${ty} Q ${tx + wave} ${ty + length / 2} ${tx} ${ty + length}`,
                                    `M ${tx} ${ty} Q ${tx - wave} ${ty + length / 2} ${tx} ${ty + length}`,
                                    `M ${tx} ${ty} Q ${tx + wave} ${ty + length / 2} ${tx} ${ty + length}`
                                ]
                            }}
                            transition={{
                                duration: 3 + Math.random(),
                                repeat: Infinity,
                                ease: "easeInOut",
                                delay: i * 0.2
                            }}
                        />
                        {/* Diamond dust tips (Ketheric Trails) - Sharp crystal points */}
                        <motion.polygon
                            points={`${tx},${ty + length - 2} ${tx + 2},${ty + length} ${tx},${ty + length + 2} ${tx - 2},${ty + length}`}
                            fill="#ffffff"
                            animate={{
                                opacity: [0.2, 1, 0.2],
                                scale: [0.8, 1.2, 0.8]
                            }}
                            transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
                            style={{ filter: "drop-shadow(0 0 2px rgba(255,255,255,0.8))" }}
                        />
                    </g>
                );
            })}

            {/* Resonance Glow (Biological Sync) - Hyperdiamond Glow */}
            <circle r={15 + sync * 25} fill="url(#res-glow)" />
            <defs>
                <radialGradient id="res-glow">
                    <stop offset="0%" stopColor="rgba(224,242,254,0.15)" />
                    <stop offset="100%" stopColor="transparent" />
                </radialGradient>
            </defs>
        </g>
    );
};
