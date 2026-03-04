import React, { useEffect, useState } from 'react';
import { useOracleGrid, OraclePacket } from '../utils/useOracleGrid';

// Extended Packet Interface (matching bridge.py updates)
interface PhaseIVPacket extends OraclePacket {
    salience?: number;
    intent?: string;
    actualization_intensity?: number;
    shear_correction?: number;
}

interface HUDProps {
    // Optional overrides for simulation mode
    manualSalience?: number;
    manualHardness?: number;
}

export const InterfaceHUD: React.FC<HUDProps> = ({ manualSalience, manualHardness }) => {
    const { packet } = useOracleGrid();
    const p = packet as PhaseIVPacket | null;

    const [localSalience, setSalience] = useState(0);
    const [localHardness, setHardness] = useState(5);
    const [localIntent, setIntent] = useState("SCANNING...");

    useEffect(() => {
        if (p) {
            if (p.salience !== undefined) setSalience(p.salience);
            if (p.intent !== undefined) setIntent(p.intent);

            // Simulate hardness accumulation based on intent
            if (p.intent === 'VITRIFY') {
                setHardness(h => Math.min(10, h + (p.actualization_intensity || 0.1)));
            }
        } else {
            // Fallback to manual props or default drift
            if (manualSalience !== undefined) setSalience(manualSalience);
            if (manualHardness !== undefined) setHardness(manualHardness);
        }
    }, [p, manualSalience, manualHardness]);

    // Entropy is inverse of hardness
    const entropy = Math.max(0, 1.0 - (localHardness / 10));

    return (
        <div className="absolute top-4 right-4 bg-black/80 p-4 rounded-lg font-mono text-xs text-white border border-purple-500/30 backdrop-blur-sm w-64 pointer-events-none select-none z-50">
            <div className="mb-4 border-b border-white/10 pb-2 flex justify-between items-end">
                <div>
                    <h3 className="text-purple-400 font-bold">SENTIENT INTERFACE</h3>
                    <span className="text-[10px] text-gray-400">PHASE IV: RECURSIVE</span>
                </div>
                <div className={`w-2 h-2 rounded-full ${p ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
            </div>

            {/* Salience Meter (Attention) */}
            <div className="mb-3">
                <div className="flex justify-between mb-1">
                    <span className="text-gray-400">SALIENCE (Ψ)</span>
                    <span className="text-cyan-400 font-bold">{localSalience.toFixed(2)}</span>
                </div>
                <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-cyan-500 transition-all duration-300"
                        style={{ width: `${Math.min(100, localSalience * 10)}%` }}
                    />
                </div>
            </div>

            {/* Hardness Scale (Vitrification) */}
            <div className="mb-3">
                <div className="flex justify-between mb-1">
                    <span className="text-gray-400">HARDNESS (Mohs)</span>
                    <span className={`font-bold ${localHardness >= 7 ? 'text-green-400' : 'text-yellow-400'}`}>
                        {localHardness.toFixed(1)}
                    </span>
                </div>
                <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
                    <div
                        className={`h-full transition-all duration-500 ${localHardness >= 7 ? 'bg-green-500' : 'bg-yellow-500'}`}
                        style={{ width: `${(localHardness / 10) * 100}%` }}
                    />
                </div>
            </div>

            {/* Intent & Entropy Grid */}
            <div className="grid grid-cols-2 gap-2 text-[10px] mb-3">
                <div className="bg-white/5 p-2 rounded border border-white/5">
                    <div className="text-gray-500 mb-1">ENTROPY</div>
                    <div className="text-red-400 font-bold">{(entropy * 100).toFixed(1)}%</div>
                </div>
                <div className="bg-white/5 p-2 rounded border border-white/5">
                    <div className="text-gray-500 mb-1">INTENT</div>
                    <div className="text-purple-300 font-bold tracking-tight">{localIntent}</div>
                </div>
            </div>

            {/* Current Address from Oracle */}
            <div className="pt-2 border-t border-white/10 text-center relative">
                <div className="text-[10px] text-gray-500 mb-1 tracking-widest">FOCUS COORDINATE</div>
                {p ? (
                    <>
                        <div className="text-cyan-300 font-bold tracking-widest text-sm mb-1">{p.address}</div>
                        <div className="text-[10px] text-purple-400">{p.name}</div>
                        {p.is_hades_gap && (
                            <div className="absolute top-2 right-0 text-[8px] bg-red-900/50 text-red-200 px-1 rounded">NULL</div>
                        )}
                    </>
                ) : (
                    <div className="text-gray-600 italic py-2">Waiting for gaze...</div>
                )}
            </div>
        </div>
    );
};
