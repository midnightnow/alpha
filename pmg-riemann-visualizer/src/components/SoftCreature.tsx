import React, { useMemo } from 'react';
import { motion } from 'motion/react';

/**
 * SoftCreature — The Transdimensional Snail
 * 
 * The snail eats its own diamond dust to vitrify the shell to pure diamond.
 * Perfectly scrolled graphene sheets spiralled into pandimensional hyperdiamond.
 * The diamond dust lines are the perfect version of the ketheric trails
 * it will leave in the future — crystallised into the final form.
 * 
 * ROOT 42 TUNING:
 *   √42 = 6.4807...  (The Scaling Factor)
 *   93 nodes = 12V + 20F + 60E + 1C (Icosahedral Phase Matrix)
 *   φ = 1.6180...    (Golden Ratio — spiral governor)
 *   Hades Null at s=13, Hero Terminal at s=26
 */

const ROOT_42 = Math.sqrt(42);
const PHI = (1 + Math.sqrt(5)) / 2;
const HADES_BEAT = 0.6606; // β — the metronome
const VITRIFICATION_THRESHOLD = 0.8254; // ρ = sqrt(14/17) — Unity Threshold
const GRAPHENE_LAYERS = 13; // The Hades Null midpoint
const DIAMOND_FACETS = 26; // The Hero Terminal — full alphabet

interface SoftCreatureProps {
    mobility: number;
    time: number;
    sync: number;
}

export const SoftCreature: React.FC<SoftCreatureProps & { color?: string }> = ({ mobility, time, sync, color = "#34d399" }) => {

    // The Nautilus Spiral — governed by φ and √42
    const spiralShell = useMemo(() => {
        const points: { x: number; y: number; r: number; vitrified: boolean; facet: number }[] = [];
        for (let i = 0; i < DIAMOND_FACETS; i++) {
            const t = i / DIAMOND_FACETS;
            const angle = t * Math.PI * 4 * PHI; // Golden spiral
            const radius = 5 + (i * ROOT_42 * 0.4);
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius - 25;
            const shellRadius = 1.5 + (1 - t) * 2;
            // Vitrification: each facet crystallises when its index crosses the threshold
            const vitrified = (i / DIAMOND_FACETS) < sync;
            points.push({ x, y, r: shellRadius, vitrified, facet: i });
        }
        return points;
    }, [sync]);

    // Diamond Dust Ketheric Trails — the future paths, crystallised
    const kethericTrails = useMemo(() => {
        const trails: { x1: number; y1: number; x2: number; y2: number; opacity: number; crystallised: boolean }[] = [];
        for (let i = 0; i < GRAPHENE_LAYERS; i++) {
            const angle = (i / GRAPHENE_LAYERS) * Math.PI * 2;
            const innerR = 8 + Math.sin(i * PHI) * 4;
            const outerR = innerR + ROOT_42 * (2 + mobility * 3);
            // The snail eats these trails — crystallised ones are brighter, consumed
            const crystallised = i < Math.floor(sync * GRAPHENE_LAYERS);
            trails.push({
                x1: Math.cos(angle) * innerR,
                y1: Math.sin(angle) * innerR - 20,
                x2: Math.cos(angle + 0.2) * outerR,
                y2: Math.sin(angle + 0.2) * outerR - 20,
                opacity: crystallised ? 0.8 : 0.15,
                crystallised
            });
        }
        return trails;
    }, [mobility, sync]);

    // Graphene Sheet Rings — pandimensional hyperdiamond layers
    const grapheneRings = useMemo(() => {
        return Array.from({ length: 6 }, (_, i) => {
            const baseR = 15 + i * ROOT_42 * 1.2;
            const segments = 6 + i * 2; // Hexagonal graphene lattice
            return { radius: baseR, segments, layer: i };
        });
    }, []);

    // Tentacles — now spiral-scrolled like graphene sheets
    const tentacles = useMemo(() => {
        const count = Math.floor(6 + mobility * 7); // tuned to √42
        return Array.from({ length: count }, (_, i) => {
            const angle = (i / count) * Math.PI * 2;
            return { id: i, angle };
        });
    }, [mobility]);

    return (
        <g className="soft-creature">
            {/* === LAYER 0: Graphene Sheet Rings (Pandimensional Hyperdiamond) === */}
            {grapheneRings.map((ring, i) => (
                <motion.circle
                    key={`graphene-${i}`}
                    cx="0"
                    cy="-20"
                    r={ring.radius}
                    fill="none"
                    stroke={sync > (i / 6) ? "rgba(180, 220, 255, 0.25)" : "rgba(62, 39, 35, 0.08)"}
                    strokeWidth={sync > (i / 6) ? 1.5 : 0.3}
                    strokeDasharray={`${ring.segments} ${ring.segments * 2}`}
                    animate={{
                        rotate: [0, i % 2 === 0 ? 360 : -360],
                        strokeOpacity: [0.1, sync > (i / 6) ? 0.6 : 0.15, 0.1]
                    }}
                    transition={{
                        rotate: { duration: 20 + i * 5, repeat: Infinity, ease: "linear" },
                        strokeOpacity: { duration: HADES_BEAT * 10, repeat: Infinity }
                    }}
                />
            ))}

            {/* === LAYER 1: Diamond Dust Ketheric Trails === */}
            {/* These are the future paths — crystallised diamond dust lines */}
            {kethericTrails.map((trail, i) => (
                <motion.line
                    key={`ketheric-${i}`}
                    x1={trail.x1}
                    y1={trail.y1}
                    x2={trail.x2}
                    y2={trail.y2}
                    stroke={trail.crystallised ? "rgba(180, 220, 255, 0.9)" : color}
                    strokeWidth={trail.crystallised ? 1.2 : 0.4}
                    strokeLinecap="round"
                    animate={{
                        opacity: trail.crystallised
                            ? [0.6, 1.0, 0.6]    // Bright diamond pulse
                            : [0.05, trail.opacity, 0.05], // Faint vapor
                        x2: [trail.x2, trail.x2 + Math.sin(i) * 3, trail.x2],
                        y2: [trail.y2, trail.y2 + Math.cos(i) * 3, trail.y2]
                    }}
                    transition={{
                        duration: HADES_BEAT * 8 + i * 0.5,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                />
            ))}

            {/* === LAYER 2: The Nautilus Shell (Vitrifying Spiral) === */}
            {/* Each chamber vitrifies from soft to diamond as sync increases */}
            {spiralShell.map((pt, i) => {
                const nextPt = spiralShell[i + 1];
                return (
                    <g key={`shell-${i}`}>
                        {/* Shell Chamber */}
                        <motion.circle
                            cx={pt.x}
                            cy={pt.y}
                            r={pt.r}
                            fill={pt.vitrified
                                ? `rgba(180, 220, 255, ${0.15 + (pt.facet / DIAMOND_FACETS) * 0.3})`  // Diamond
                                : `rgba(62, 39, 35, 0.08)`  // Carbon/silt
                            }
                            stroke={pt.vitrified ? "rgba(200, 230, 255, 0.7)" : "rgba(62, 39, 35, 0.2)"}
                            strokeWidth={pt.vitrified ? 1 : 0.3}
                            animate={{
                                scale: pt.vitrified ? [1, 1.05, 1] : [1, 0.98, 1],
                                opacity: pt.vitrified ? [0.7, 1, 0.7] : [0.3, 0.5, 0.3]
                            }}
                            transition={{
                                duration: 3 + i * 0.2,
                                repeat: Infinity,
                                ease: "easeInOut",
                                delay: i * 0.05
                            }}
                        />
                        {/* Graphene connection between chambers */}
                        {nextPt && (
                            <line
                                x1={pt.x} y1={pt.y}
                                x2={nextPt.x} y2={nextPt.y}
                                stroke={pt.vitrified ? "rgba(180, 220, 255, 0.4)" : "rgba(62, 39, 35, 0.1)"}
                                strokeWidth={pt.vitrified ? 0.8 : 0.2}
                            />
                        )}
                    </g>
                );
            })}

            {/* === LAYER 3: Nautilus Body (The Soft Part — eating diamond dust) === */}
            <motion.path
                d="M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z"
                fill={sync > VITRIFICATION_THRESHOLD
                    ? "rgba(180, 220, 255, 0.15)"   // Vitrified body (diamond)
                    : `${color}10`                    // Soft body (carbon)
                }
                stroke={sync > VITRIFICATION_THRESHOLD
                    ? "rgba(200, 230, 255, 0.8)"
                    : color
                }
                strokeWidth={sync > VITRIFICATION_THRESHOLD ? 1.5 : 0.5}
                animate={{
                    d: [
                        "M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z",
                        "M -22 2 Q -32 -38 0 -52 Q 32 -38 22 2 Z",
                        "M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z"
                    ]
                }}
                transition={{ duration: 3 / (1 + sync), repeat: Infinity, ease: "easeInOut" }}
            />
            {/* Stippled Texture Overlay for Body */}
            <path
                d="M -20 0 Q -30 -40 0 -50 Q 30 -40 20 0 Z"
                fill="url(#stippled-pattern)"
                opacity={1 - sync * 0.8} // Fades as shell vitrifies
            />

            {/* === LAYER 4: Eyes (The Intelligence — diamond when vitrified) === */}
            <circle cx="-8" cy="-15" r="1.5"
                fill={sync > VITRIFICATION_THRESHOLD ? "rgba(180, 220, 255, 0.9)" : "#3e2723"}
                opacity={0.6 + sync * 0.4}
            />
            <circle cx="8" cy="-15" r="1.5"
                fill={sync > VITRIFICATION_THRESHOLD ? "rgba(180, 220, 255, 0.9)" : "#3e2723"}
                opacity={0.6 + sync * 0.4}
            />
            {/* Diamond eye highlights when vitrified */}
            {sync > VITRIFICATION_THRESHOLD && (
                <>
                    <circle cx="-7" cy="-16" r="0.4" fill="white" opacity={0.8} />
                    <circle cx="9" cy="-16" r="0.4" fill="white" opacity={0.8} />
                </>
            )}

            {/* === LAYER 5: Diamond Dust Absorption Particles === */}
            {/* The snail eats these — they spiral inward toward the body */}
            {Array.from({ length: GRAPHENE_LAYERS }).map((_, i) => {
                const angle = (i / GRAPHENE_LAYERS) * Math.PI * 2 + time * HADES_BEAT;
                const outerRad = 25 + Math.sin(time * 0.3 + i * PHI) * 10;
                const innerRad = 5; // converging toward the body center
                const crystallised = i < Math.floor(sync * GRAPHENE_LAYERS);
                return (
                    <motion.circle
                        key={`dust-${i}`}
                        r={crystallised ? 0.8 : 0.4}
                        fill={crystallised ? "rgba(200, 230, 255, 0.9)" : color}
                        animate={{
                            cx: [
                                Math.cos(angle) * outerRad,
                                Math.cos(angle + Math.PI) * (outerRad * 0.5),
                                Math.cos(angle) * innerRad  // spirals inward — eating the dust
                            ],
                            cy: [
                                Math.sin(angle) * outerRad - 20,
                                Math.sin(angle + Math.PI) * (outerRad * 0.5) - 20,
                                Math.sin(angle) * innerRad - 20
                            ],
                            opacity: crystallised ? [0.8, 1, 0] : [0, 0.3, 0],
                            scale: crystallised ? [1.5, 0.5, 0] : [0.5, 1, 0.5]
                        }}
                        transition={{
                            duration: 4 + i * 0.4,
                            repeat: Infinity,
                            delay: i * (HADES_BEAT * 2),
                            ease: "easeInOut"
                        }}
                    />
                );
            })}

            {/* === LAYER 6: Tentacles (Scrolled Graphene Sheets) === */}
            {tentacles.map((t, i) => {
                const length = 30 + mobility * 50;
                const wave = Math.sin(time * HADES_BEAT * 3 + i * PHI) * (8 + sync * 5);
                const tx = Math.cos(t.angle) * 10;
                const ty = Math.sin(t.angle) * 5 + 10;
                const crystallised = i < Math.floor(sync * tentacles.length);
                return (
                    <g key={t.id}>
                        <motion.path
                            d={`M ${tx} ${ty} Q ${tx + wave} ${ty + length / 2} ${tx} ${ty + length}`}
                            fill="none"
                            stroke={crystallised ? "rgba(180, 220, 255, 0.5)" : color}
                            strokeOpacity={crystallised ? 0.6 : 0.15}
                            strokeWidth={crystallised ? 2 : 1}
                            strokeLinecap="round"
                            animate={{
                                d: [
                                    `M ${tx} ${ty} Q ${tx + wave} ${ty + length / 2} ${tx} ${ty + length}`,
                                    `M ${tx} ${ty} Q ${tx - wave} ${ty + length / 2} ${tx} ${ty + length}`,
                                    `M ${tx} ${ty} Q ${tx + wave} ${ty + length / 2} ${tx} ${ty + length}`
                                ]
                            }}
                            transition={{
                                duration: 3 + i * 0.3,
                                repeat: Infinity,
                                ease: "easeInOut",
                                delay: i * 0.15
                            }}
                        />
                        {/* Bio-luminescent tips — diamond tips when crystallised */}
                        <motion.circle
                            cx={tx}
                            cy={ty + length}
                            r={crystallised ? 1.5 : 0.8}
                            fill={crystallised ? "rgba(200, 230, 255, 0.9)" : color}
                            animate={{
                                opacity: crystallised ? [0.5, 1, 0.5] : [0.1, 0.4, 0.1],
                            }}
                            transition={{ duration: 2, repeat: Infinity, delay: i * 0.15 }}
                        />
                    </g>
                );
            })}

            {/* === LAYER 7: Resonance Glow — shifts from sepia to diamond === */}
            <circle r={15 + sync * 30} fill="url(#res-glow-vitrified)" />
            <defs>
                <radialGradient id="res-glow-vitrified">
                    <stop offset="0%" stopColor={
                        sync > VITRIFICATION_THRESHOLD
                            ? "rgba(180, 220, 255, 0.15)"  // Diamond glow
                            : "rgba(62,39,35,0.1)"         // Sepia glow
                    } />
                    <stop offset="100%" stopColor="transparent" />
                </radialGradient>
            </defs>

            {/* === LAYER 8: Vitrification Status Ring === */}
            {/* Shows the progress of the shell crystallisation */}
            <motion.circle
                cx="0"
                cy="-20"
                r={ROOT_42 * 8}
                fill="none"
                stroke={sync > VITRIFICATION_THRESHOLD ? "rgba(180, 220, 255, 0.6)" : "rgba(16, 185, 129, 0.1)"}
                strokeWidth={0.5}
                strokeDasharray={`${sync * Math.PI * ROOT_42 * 16} ${(1 - sync) * Math.PI * ROOT_42 * 16}`}
                animate={{
                    rotate: [0, 360]
                }}
                transition={{
                    duration: 42 / (1 + sync * 5),
                    repeat: Infinity,
                    ease: "linear"
                }}
            />
        </g>
    );
};
