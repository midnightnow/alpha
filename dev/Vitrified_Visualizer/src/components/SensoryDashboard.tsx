import React, { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Target, Scroll, Circle, Zap, Eye, ChevronRight } from 'lucide-react';

interface OperatorProps {
    name: string;
    icon: any;
    status: string;
    value: number;
    color: string;
    description: string;
}

const OperatorStrip: React.FC<OperatorProps> = ({ name, icon: Icon, status, value, color, description }) => (
    <div className="flex flex-col gap-1 p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors group">
        <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
                <Icon size={14} style={{ color }} />
                <span className="text-[10px] font-black text-white uppercase tracking-widest">{name}</span>
            </div>
            <span className="text-[8px] font-mono text-zinc-500 uppercase">{status}</span>
        </div>
        <div className="text-[9px] text-zinc-400 font-mono italic mb-1 opacity-70 group-hover:opacity-100 transition-opacity">"{description}"</div>
        <div className="w-full h-1 bg-zinc-900 rounded-full overflow-hidden">
            <motion.div
                className="h-full"
                style={{ backgroundColor: color }}
                animate={{ width: `${value * 100}%` }}
                transition={{ type: 'spring', stiffness: 50 }}
            />
        </div>
    </div>
);

export const SensoryDashboard: React.FC<{ time: number }> = ({ time }) => {
    const [baaLevel, setBaaLevel] = useState(0); // 0: Toki Pona, 1: Literal, 2: Full Render

    const baaLabels = [
        { tp: "suli oko mute", lit: "A large being with many eyes", level: "SAFE" },
        { tp: "alasa sona sewi", lit: "Seeking higher knowledge", level: "MANAGED" },
        { tp: "sewi wawa monsuta", lit: "Holy power and terror", level: "HAZARDOUS" }
    ];

    const operators = useMemo(() => [
        {
            name: "Artemis",
            icon: Target,
            status: "TRACKING",
            value: 0.85 + Math.sin(time * 0.5) * 0.1,
            color: "#f43f5e",
            description: "Invariant Ratio Provisions"
        },
        {
            name: "Athena",
            icon: Shield,
            status: "WEAVING",
            value: 0.7 + Math.cos(time * 0.3) * 0.2,
            color: "#0ea5e9",
            description: "Civilized Structure Translation"
        },
        {
            name: "Plato",
            icon: Scroll,
            status: "PULSING",
            value: 0.9 + Math.sin(time * 0.8) * 0.05,
            color: "#fbbf24",
            description: "Similar Triangle Extraction"
        },
        {
            name: "Hades",
            icon: Circle,
            status: "SINKING",
            value: 0.4 + Math.cos(time * 0.1) * 0.3,
            color: "#3f3f46",
            description: "Void Debt Custodian"
        }
    ], [time]);

    return (
        <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="fixed bottom-10 left-10 p-5 bg-black/90 backdrop-blur-2xl border border-white/10 rounded-3xl w-72 space-y-4 z-50 shadow-[0_0_50px_rgba(0,0,0,0.5)]"
        >
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse shadow-[0_0_10px_#06b6d4]" />
                    <h3 className="text-[10px] font-black text-white uppercase tracking-[0.2em]">Operator Console</h3>
                </div>
                <Zap size={12} className="text-zinc-500" />
            </div>

            <div className="space-y-2">
                {operators.map(op => <OperatorStrip key={op.name} {...op} />)}
            </div>

            {/* BAA-TP Codec / Revelation Slider */}
            <div className="pt-4 border-t border-white/5">
                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2 text-[9px] font-bold text-zinc-400 uppercase tracking-widest">
                        <Eye size={12} className="text-purple-500" /> BAA-TP CODEC
                    </div>
                    <span className={`text-[8px] font-black px-1.5 py-0.5 rounded ${baaLevel === 2 ? 'bg-red-500 text-white' : 'bg-zinc-800 text-zinc-400'}`}>
                        LVL {baaLevel + 1}
                    </span>
                </div>

                <div className="bg-black/50 p-3 rounded-xl border border-white/5 min-h-[60px] flex flex-col justify-center">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={baaLevel}
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -5 }}
                            className="space-y-1"
                        >
                            <div className="text-[11px] font-mono font-bold text-purple-400 tracking-tight leading-tight">
                                {baaLabels[baaLevel].tp}
                            </div>
                            <div className="text-[9px] text-zinc-500 font-serif italic">
                                {baaLevel > 0 ? baaLabels[baaLevel].lit : "..."}
                            </div>
                        </motion.div>
                    </AnimatePresence>
                </div>

                <div className="mt-3 flex gap-1">
                    {[0, 1, 2].map(l => (
                        <button
                            key={l}
                            onClick={() => setBaaLevel(l)}
                            className={`flex-1 h-1 rounded-full transition-all ${baaLevel === l ? 'bg-purple-500' : 'bg-zinc-800'}`}
                        />
                    ))}
                </div>
            </div>

            <div className="pt-2 text-center">
                <p className="text-[8px] text-zinc-600 font-black uppercase tracking-tighter">
                    Principia Mathematica Geometrica v1.0
                </p>
            </div>
        </motion.div>
    );
};
