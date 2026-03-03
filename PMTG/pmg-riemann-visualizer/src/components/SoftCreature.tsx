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
            {/* Nautilus Body -> Vitrified Hyperdiamond (Crystallised Form) */}
            <motion.path
                d="M 0 -50 L 30 -15 L 0 20 L -30 -15 Z M 0 -30 L 15 -10 L 0 5 L -15 -10 Z M 0 -40 L 5 -20 L 0 -10 L -5 -20 Z"
                fill={color}
                fillOpacity="0.15"
                stroke={color}
                strokeWidth="1.0"
                strokeLinejoin="miter"
                strokeMiterlimit="5"
                animate={{
                    d: [
                        "M 0 -50 L 30 -15 L 0 20 L -30 -15 Z M 0 -30 L 15 -10 L 0 5 L -15 -10 Z M 0 -40 L 5 -20 L 0 -10 L -5 -20 Z",
                        "M 0 -52 L 32 -13 L 0 22 L -32 -13 Z M 0 -32 L 17 -8 L 0 7 L -17 -8 Z M 0 -42 L 7 -18 L 0 -8 L -7 -18 Z",
                        "M 0 -50 L 30 -15 L 0 20 L -30 -15 Z M 0 -30 L 15 -10 L 0 5 L -15 -10 Z M 0 -40 L 5 -20 L 0 -10 L -5 -20 Z"
                    ]
                }}
                transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                style={{ filter: "drop-shadow(0 0 8px rgba(224,242,254,0.4))" }}
            />
            {/* Pan-dimensional graphene sheets spiralling inward */}
            <path
                d="M 0 -50 L 30 -15 L 0 20 L -30 -15 Z"
                fill="url(#stippled-pattern)"
                opacity="0.8"
            />
            {/* Inner crystalline scaffolding */}
            <path
                d="M -30 -15 L 30 -15 M 0 -50 L 0 20 M -15 -10 L 15 -10 M 0 -30 L 0 5"
                stroke="rgba(224,242,254,0.5)"
                strokeWidth="0.5"
                fill="none"
                strokeDasharray="2 2"
            />
            {/* Eyes (The Intelligence) - Geometric */}
            <polygon points="-8,-17 -6,-15 -8,-13 -10,-15" fill="#bae6fd" opacity={0.9} />
            <polygon points="8,-17 10,-15 8,-13 6,-15" fill="#bae6fd" opacity={0.9} />

            {/* Diamond Dust / Ketheric Trails - Eaten by the shell (Spiralling INWARD) */}
            {Array.from({ length: 42 }).map((_, i) => { // Scaled to 42 for Root 42 tuning
                const startAngle = (i / 42) * Math.PI * 2 + time;
                const startRad = 45 + Math.sin(i * 1.618) * 15; // Phased by golden ratio

                // End coordinates are at the geometric center/mouth of the hyperdiamond
                const endX = 0;
                const endY = -15;

                return (
                    <motion.polygon
                        key={`diamond-${i}`}
                        // Sharp geometric ketheric trails
                        points={`0,-1 1,0 0,1 -1,0`}
                        fill="#ffffff"
                        animate={{
                            x: [Math.cos(startAngle) * startRad, endX],
                            y: [Math.sin(startAngle) * startRad - 15, endY],
                            opacity: [0, 1, 0],
                            scale: [0.5, 1.5, 0.1],
                            rotate: [0, 90]
                        }}
                        transition={{
                            duration: 1.5 + Math.random(),
                            repeat: Infinity,
                            delay: i * 0.05,
                            ease: "easeIn" // Accelerates as it gets "eaten"
                        }}
                        style={{ filter: "drop-shadow(0 0 3px rgba(224,242,254,0.9))" }}
                    />
                );
            })}

            {/* Crystalline Tendrils (Vitrified Mobility) */}
            {tentacles.map((t, i) => {
                const length = 50 + mobility * 40; // Sharper, longer rigid lengths
                const tx = Math.cos(t.angle) * 12;
                const ty = Math.sin(t.angle) * 6 + 10;

                // Calculate zig-zag pattern instead of bezier curves
                const z1x = tx + Math.cos(t.angle + Math.PI / 4) * 8;
                const z1y = ty + length * 0.33;
                const z2x = tx + Math.cos(t.angle - Math.PI / 4) * 8;
                const z2y = ty + length * 0.66;
                const endx = tx;
                const endy = ty + length;

                return (
                    <g key={t.id}>
                        <motion.path
                            d={`M ${tx} ${ty} L ${z1x} ${z1y} L ${z2x} ${z2y} L ${endx} ${endy}`}
                            fill="none"
                            stroke={color}
                            strokeOpacity="0.4"
                            strokeWidth="1.0"
                            strokeLinejoin="miter"
                            animate={{
                                d: [
                                    `M ${tx} ${ty} L ${z1x} ${z1y} L ${z2x} ${z2y} L ${endx} ${endy}`,
                                    `M ${tx} ${ty} L ${z1x * 1.2} ${z1y} L ${z2x * 1.2} ${z2y} L ${endx} ${endy * 1.05}`,
                                    `M ${tx} ${ty} L ${z1x} ${z1y} L ${z2x} ${z2y} L ${endx} ${endy}`
                                ]
                            }}
                            transition={{
                                duration: 2 + Math.random(),
                                repeat: Infinity,
                                ease: "linear",
                                delay: i * 0.1
                            }}
                        />
                        {/* Diamond dust tips (Ketheric Trails) - Sharp crystal points */}
                        <motion.polygon
                            points={`${endx},${endy - 3} ${endx + 3},${endy} ${endx},${endy + 3} ${endx - 3},${endy}`}
                            fill="#ffffff"
                            animate={{
                                opacity: [0.4, 1, 0.4],
                                scale: [0.5, 1.0, 0.5]
                            }}
                            transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
                            style={{ filter: "drop-shadow(0 0 3px rgba(224,242,254,0.9))" }}
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
