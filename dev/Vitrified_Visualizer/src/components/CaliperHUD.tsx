import React, { useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useVitrifiedStore } from '../store/vitrifiedStore';
import { generateRatioLookup, RatioEntry } from '../utils/RatioLookupTable';

export const CaliperHUD = () => {
    const {
        nodes,
        selectedNodeIds,
        caliperMode,
        setCaliperMode,
        shavedMode,
        setShavedMode,
        setActiveMatches
    } = useVitrifiedStore();

    const [ratioTable, setRatioTable] = useState<RatioEntry[]>([]);

    useEffect(() => {
        if (nodes.length > 0 && ratioTable.length === 0) {
            setRatioTable(generateRatioLookup(nodes));
        }
    }, [nodes, ratioTable.length]);

    const selectedNodes = useMemo(() => {
        return selectedNodeIds.map(id => nodes.find(n => n.NodeID === id)).filter(Boolean);
    }, [selectedNodeIds, nodes]);

    const ratioData = useMemo(() => {
        if (selectedNodes.length !== 2) return null;
        const n1 = selectedNodes[0]!;
        const n2 = selectedNodes[1]!;

        const d1 = Math.sqrt(n1.x ** 2 + n1.y ** 2 + n1.z ** 2);
        const d2 = Math.sqrt(n2.x ** 2 + n2.y ** 2 + n2.z ** 2);

        const ratio = Math.max(d1, d2) / Math.min(d1, d2);
        const phi = 1.6180339887;
        const phiDiff = Math.abs(ratio - phi);

        // Shear Angle arctan(14/17) = 39.4
        const v1 = new THREE.Vector3(n1.x, n1.y, n1.z);
        const v2 = new THREE.Vector3(n2.x, n2.y, n2.z);
        const angle = v1.angleTo(v2) * (180 / Math.PI);
        const shearAngle = 39.4;
        const shearDiff = Math.abs(angle - shearAngle);

        return { ratio, phiDiff, angle, shearDiff };
    }, [selectedNodes]);

    const findMatches = () => {
        if (!ratioData) return;
        const delta = 0.000585;
        const matches = ratioTable.filter(entry => {
            const radialMatch = Math.abs(entry.radialRatio - ratioData.ratio) < delta;
            const angularMatch = Math.abs(entry.angularDist - ratioData.angle) < 0.1;
            return radialMatch || angularMatch;
        }).map(e => e.pair);

        setActiveMatches(matches.slice(0, 50)); // Cap for performance
    };

    if (!caliperMode) return (
        <button
            onClick={() => setCaliperMode(true)}
            className="p-3 bg-zinc-900/80 border border-zinc-800 rounded-lg text-[10px] text-zinc-400 uppercase tracking-widest hover:bg-zinc-800 pointer-events-auto"
        >
            Activate Caliper Mode
        </button>
    );

    return (
        <div className="p-6 bg-black/90 backdrop-blur-3xl border border-rose-900/30 rounded-2xl w-full pointer-events-auto shadow-[0_0_50px_rgba(255,0,50,0.1)]">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-[10px] font-bold text-rose-500 uppercase tracking-[0.3em]">Golden Mean Caliper</h3>
                <button onClick={() => setCaliperMode(false)} className="text-[10px] text-zinc-600 hover:text-white">EXIT</button>
            </div>

            {!ratioData ? (
                <p className="text-[9px] text-zinc-500 uppercase italic">Select two nodes to measure the "Whirred" ratio</p>
            ) : (
                <div className="space-y-6">
                    <div className="flex justify-between items-end border-b border-zinc-800 pb-2">
                        <span className="text-[9px] text-zinc-500 uppercase">Proportional Ratio</span>
                        <span className="text-xl font-mono text-white tracking-tighter">{ratioData.ratio.toFixed(6)}</span>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className={`p-3 rounded-lg border ${ratioData.phiDiff < 0.001 ? 'bg-gold-500/10 border-gold-500/50' : 'bg-zinc-900 border-zinc-800'}`}>
                            <span className="block text-[8px] text-zinc-500 uppercase mb-1">Phi (ϕ) Variance</span>
                            <span className="text-[12px] font-mono text-zinc-200">±{ratioData.phiDiff.toFixed(6)}</span>
                        </div>
                        <div className={`p-3 rounded-lg border ${ratioData.shearDiff < 0.5 ? 'bg-rose-500/10 border-rose-500/50' : 'bg-zinc-900 border-zinc-800'}`}>
                            <span className="block text-[8px] text-zinc-500 uppercase mb-1">Shear Alignment</span>
                            <span className="text-[12px] font-mono text-zinc-200">{ratioData.angle.toFixed(1)}°</span>
                        </div>
                    </div>

                    {ratioData.shearDiff < 0.5 && (
                        <div className="p-3 bg-rose-500/20 border border-rose-500/50 rounded-lg animate-pulse">
                            <p className="text-[10px] text-rose-400 font-bold uppercase tracking-widest text-center">Fracture Point Detected</p>
                            <p className="text-[8px] text-rose-300/70 text-center mt-1 uppercase">Geometry breaking into motion</p>
                        </div>
                    )}

                    <div className="flex gap-2">
                        <button
                            onClick={findMatches}
                            disabled={!ratioData}
                            className="flex-1 py-3 bg-rose-500/20 border border-rose-500/50 rounded-xl text-[10px] text-rose-400 font-bold uppercase tracking-widest hover:bg-rose-500/30 disabled:opacity-20 transition-all"
                        >
                            Vitrify Matches (δ)
                        </button>
                        <button
                            onClick={() => setActiveMatches([])}
                            className="px-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl text-[10px] text-zinc-500 uppercase hover:text-white"
                        >
                            Clear
                        </button>
                    </div>

                    <div className="flex items-center justify-between p-4 bg-zinc-900/50 border border-zinc-800/50 rounded-xl">
                        <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-bold">Dimensionless Mode</span>
                        <button
                            onClick={() => setShavedMode(!shavedMode)}
                            className={`w-12 h-6 rounded-full transition-colors relative ${shavedMode ? 'bg-rose-500' : 'bg-zinc-800'}`}
                        >
                            <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${shavedMode ? 'left-7' : 'left-1'}`} />
                        </button>
                    </div>

                    <div className="mt-4 pt-4 border-t border-zinc-800 text-center">
                        <span className="text-[8px] text-zinc-600 uppercase italic">"The ratio is the invariant; the number is its shadow."</span>
                    </div>
                </div>
            )}
        </div>
    );
};
