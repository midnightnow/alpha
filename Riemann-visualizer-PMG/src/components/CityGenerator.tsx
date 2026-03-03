import React, { useMemo } from 'react';
import { motion } from 'motion/react';
import { Building2, Box, Castle, TowerControl as Tower } from 'lucide-react';

interface CityGeneratorProps {
    t: number;
    time: number;
}

interface Building {
    id: number;
    x: number;
    y: number;
    height: number;
    type: 'box' | 'tower' | 'castle';
    stability: number;
}

export const CityGenerator: React.FC<CityGeneratorProps> = ({ t, time }) => {
    const buildings = useMemo(() => {
        // Generate buildings based on Riemann resonance at the current t
        return Array.from({ length: 12 }, (_, i) => {
            const angle = (i / 12) * Math.PI * 2 + time * 0.05;
            const resonance = (Math.sin(i * t) + 1) / 2;
            const stability = 1 - Math.abs(resonance - 0.5) * 2; // Perfect stability at 0.5

            const types: Building['type'][] = ['box', 'tower', 'castle'];
            const type = types[i % 3];

            return {
                id: i,
                x: 200 + Math.cos(angle) * 120,
                y: 200 + Math.sin(angle) * 120,
                height: 20 + resonance * 80,
                type,
                stability
            };
        });
    }, [t, time]);

    return (
        <div className="w-full h-full relative flex items-center justify-center bg-black/20 rounded-3xl border border-white/5 overflow-hidden">
            <div className="absolute top-4 left-4 flex items-center gap-2">
                <Building2 className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold uppercase tracking-widest text-emerald-400">Stable Construction Paddock</h3>
            </div>

            <svg viewBox="0 0 400 400" className="w-full h-full max-w-[500px]">
                {/* Foundation Grid */}
                <circle cx="200" cy="200" r="130" fill="none" stroke="rgba(16,185,129,0.05)" strokeWidth="1" strokeDasharray="5 5" />

                {buildings.map((building) => {
                    const isStable = building.stability > 0.8;
                    const color = isStable ? '#10b981' : '#3f3f46';

                    return (
                        <motion.g
                            key={building.id}
                            initial={{ opacity: 0, scale: 0 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="cursor-pointer"
                        >
                            {/* Building Shadow/Base */}
                            <ellipse
                                cx={building.x}
                                cy={building.y + 10}
                                rx="15" ry="5"
                                fill="rgba(0,0,0,0.3)"
                            />

                            {/* Construction Form */}
                            {building.type === 'box' && (
                                <rect
                                    x={building.x - 10}
                                    y={building.y - building.height}
                                    width="20"
                                    height={building.height}
                                    fill={color}
                                    fillOpacity={0.2}
                                    stroke={color}
                                    strokeWidth="1.5"
                                />
                            )}
                            {building.type === 'tower' && (
                                <path
                                    d={`M ${building.x - 8} ${building.y} L ${building.x + 8} ${building.y} L ${building.x + 4} ${building.y - building.height} L ${building.x - 4} ${building.y - building.height} Z`}
                                    fill={color}
                                    fillOpacity={0.2}
                                    stroke={color}
                                    strokeWidth="1.5"
                                />
                            )}
                            {building.type === 'castle' && (
                                <g>
                                    <rect x={building.x - 12} y={building.y - building.height} width="24" height={building.height} fill={color} fillOpacity={0.1} stroke={color} strokeWidth="1.5" />
                                    <rect x={building.x - 12} y={building.y - building.height - 5} width="6" height="5" fill={color} />
                                    <rect x={building.x + 6} y={building.y - building.height - 5} width="6" height="5" fill={color} />
                                </g>
                            )}

                            {/* Stability Indicator */}
                            <circle
                                cx={building.x}
                                cy={building.y - building.height - 10}
                                r="2"
                                fill={isStable ? '#10b981' : '#f43f5e'}
                                className={isStable ? 'animate-pulse' : ''}
                            />
                        </motion.g>
                    );
                })}
            </svg>

            <div className="absolute bottom-4 right-4 text-right">
                <span className="text-[8px] text-zinc-500 uppercase block">Integration Factor</span>
                <span className="text-sm font-mono text-emerald-400">{(t / 93).toFixed(4)}</span>
            </div>
        </div>
    );
};
