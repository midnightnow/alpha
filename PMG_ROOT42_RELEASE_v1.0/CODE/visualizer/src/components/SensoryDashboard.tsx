import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface SensoryHubProps {
    label: string;
    intensity: number;
    nodes: number[];
    color: string;
}

const SensoryHub: React.FC<SensoryHubProps> = ({ label, intensity, nodes, color }) => (
    <div className="flex flex-col gap-1 p-3 bg-zinc-900/50 border border-zinc-800 rounded-lg">
        <div className="flex justify-between items-center">
            <span className="text-[10px] text-zinc-500 uppercase tracking-widest">{label}</span>
            <span className="text-[10px] font-mono" style={{ color }}>{Math.floor(intensity * 100)}%</span>
        </div>
        <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
            <motion.div
                className="h-full"
                style={{ backgroundColor: color }}
                animate={{ width: `${intensity * 100}%` }}
            />
        </div>
        <div className="flex gap-1 mt-1">
            {nodes.map(n => (
                <div key={n} className="text-[8px] text-zinc-600 font-mono">#{n}</div>
            ))}
        </div>
    </div>
);

export const SensoryDashboard: React.FC<{ time: number }> = ({ time }) => {
    // Simulate flux based on precessional clock
    const flux = useMemo(() => ({
        light: 0.5 + Math.sin(time * 0.5) * 0.42,
        hearing: 0.5 + Math.cos(time * 0.66) * 0.33,
        smell: 0.3 + Math.sin(time * 1.08) * 0.12
    }), [time]);

    return (
        <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="fixed bottom-32 left-10 p-4 bg-black/80 backdrop-blur-xl border border-zinc-800 rounded-2xl w-64 space-y-3 z-50 shadow-2xl"
        >
            <div className="flex items-center gap-2 border-b border-zinc-800 pb-2">
                <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
                <h3 className="text-[10px] font-bold text-zinc-300 uppercase tracking-[0.2em]">Sensory Flux Map</h3>
            </div>

            <SensoryHub
                label="Light / Sound (Front 15°)"
                intensity={flux.light}
                nodes={[9, 10, 11, 12]}
                color="#ff3c64"
            />

            <SensoryHub
                label="Hearing (Side 90°)"
                intensity={flux.hearing}
                nodes={[7, 8, 19, 20]}
                color="#3c82ff"
            />

            <SensoryHub
                label="Smell (Below -90°)"
                intensity={flux.smell}
                nodes={[4, 6, 8, 44]}
                color="#00ffa3"
            />

            <div className="pt-2 border-t border-zinc-800">
                <p className="text-[8px] text-zinc-600 uppercase tracking-tighter text-center">
                    Bridging Verbal-Geometric Interference
                </p>
            </div>
        </motion.div>
    );
};
