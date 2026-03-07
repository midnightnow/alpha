import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface SoftCreatureProps {
    mobility: number;
    time: number;
    sync: number;
}

export const SoftCreature: React.FC<SoftCreatureProps & { color?: string }> = ({ mobility, time, sync, color = "#3e2723" }) => {
    // Concentric "Shell" ripples - matches the 'slinky' style in sketches
    const segments = useMemo(() => {
        return Array.from({ length: 15 }, (_, i) => ({ id: i }));
    }, []);

    return (
        <g className="soft-creature">
            <defs>
                <pattern id="stippled-pattern" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
                    <circle cx="1" cy="1" r="0.5" fill={color} opacity="0.3" />
                </pattern>
            </defs>

            {/* Concentric Ripples (The snail's face/body segments) */}
            {segments.map((seg, i) => {
                const scale = 1 - (i * 0.04);
                const drift = Math.sin(time * 2 + i * 0.3) * (2 + mobility * 5);

                return (
                    <motion.circle
                        key={seg.id}
                        cx={drift + (i * 3)}
                        cy={Math.cos(time * 3 + i * 0.5) * 2}
                        r={35 * scale}
                        fill="none"
                        stroke={color}
                        strokeWidth="0.4"
                        strokeOpacity={0.5 - (i * 0.03)}
                        animate={{
                            r: [35 * scale, (35 * scale) + 1.5, 35 * scale],
                            cx: [drift + (i * 3), drift + (i * 3) + 1, drift + (i * 3)]
                        }}
                        transition={{
                            duration: 2.5,
                            repeat: Infinity,
                            delay: i * 0.05,
                            ease: "easeInOut"
                        }}
                    />
                );
            })}

            {/* The "Glistening" Center (intelligence/eye) */}
            <motion.circle
                cx="0"
                cy="0"
                r="1.8"
                fill="#F27D26"
                animate={{
                    opacity: [0.3, 1, 0.3],
                    scale: [1, 1.2, 1]
                }}
                transition={{ duration: 1.5, repeat: Infinity }}
            />

            {/* Subtle trailing feelers / tentacles */}
            {segments.slice(0, 6).map((_, i) => (
                <motion.path
                    key={`tentacle-${i}`}
                    d={`M 0 0 Q ${15 + i * 4} 15 ${30 + i * 8} 0`}
                    fill="none"
                    stroke={color}
                    strokeWidth="0.15"
                    strokeOpacity="0.2"
                    animate={{
                        d: [
                            `M 0 0 Q ${15 + i * 4} 15 ${30 + i * 8} 0`,
                            `M 0 0 Q ${15 + i * 4} -15 ${30 + i * 8} 0`,
                            `M 0 0 Q ${15 + i * 4} 15 ${30 + i * 8} 0`
                        ]
                    }}
                    transition={{ duration: 4, repeat: Infinity, delay: i * 0.15 }}
                />
            ))}
        </g>
    );
};
