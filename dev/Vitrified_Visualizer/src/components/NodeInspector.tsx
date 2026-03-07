import React from 'react';
import { useVitrifiedStore } from '../store/vitrifiedStore';
import { formatSexagesimalFrac, toFixedTrim, toPitchPer12 } from '../utils/math_bridge';
import slopeLibrary from '../data/slope_library.json';

export const NodeInspector: React.FC = () => {
    const { nodes, selectedNodeId } = useVitrifiedStore();
    const node = nodes.find(n => n.NodeID === selectedNodeId);

    if (!node) {
        return (
            <div className="p-6 bg-black/60 backdrop-blur-xl border border-zinc-800 rounded-2xl w-full pointer-events-none">
                <p className="text-[9px] text-zinc-500 uppercase tracking-widest">Select a node to begin audit</p>
            </div>
        );
    }

    // Calculate slope to Apex (Node 93 at 0,0,6.48)
    const dx = 0 - node.x;
    const dy = 0 - node.y;
    const dz = 6.48 - node.z;
    const dr = Math.sqrt(dx * dx + dy * dy);
    const slope = dr > 0 ? dz / dr : 0;
    const angle = Math.atan(slope) * (180 / Math.PI);

    // Find closest slope in library
    const match = slopeLibrary.find(s => Math.abs(s.ratio - slope) < 0.05);
    const slop = match ? Math.abs(match.ratio - slope) : 0;

    return (
        <div className="p-6 bg-black/80 backdrop-blur-2xl border border-rose-500/30 rounded-2xl w-full pointer-events-auto shadow-[0_0_50px_rgba(255,60,100,0.1)]">
            <div className="flex justify-between items-start border-b border-zinc-800 pb-4 mb-4">
                <div>
                    <h3 className="text-[10px] font-bold text-rose-500 uppercase tracking-[0.3em]">Node Audit</h3>
                    <div className="text-2xl font-bold text-white tracking-tighter mt-1">
                        #{node.NodeID} <span className="text-zinc-600 text-xs font-mono ml-2">[{node.SymbolicName}]</span>
                    </div>
                </div>
                <div className="text-right">
                    <div className="text-[10px] text-zinc-500 uppercase tracking-widest">Sector</div>
                    <div className="text-lg font-mono text-zinc-300">{node.sector} / 8</div>
                </div>
            </div>

            <div className="space-y-6">
                {/* Exact Ratio Section */}
                <section>
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-[9px] text-zinc-500 uppercase font-bold tracking-widest">Exact Ratio (Rise/Run)</span>
                        <span className="px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-500 text-[8px] font-bold border border-rose-500/20">SEXAGESIMAL</span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 bg-zinc-900/40 p-3 rounded-lg border border-zinc-800/50">
                        <div>
                            <div className="text-[14px] font-mono text-white">{formatSexagesimalFrac(slope, 3)}</div>
                            <div className="text-[8px] text-zinc-500 mt-1 uppercase">Base-60 Notation</div>
                        </div>
                        <div className="text-right">
                            <div className="text-[14px] font-mono text-zinc-300">{toFixedTrim(angle, 2)}°</div>
                            <div className="text-[8px] text-zinc-500 mt-1 uppercase">Modern Angle</div>
                        </div>
                    </div>
                </section>

                {/* Slope Family Match */}
                <section className="relative">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-[9px] text-zinc-500 uppercase font-bold tracking-widest">Plimpton Match</span>
                        {match && slop < 0.01 && (
                            <span className="text-emerald-500 text-[8px] font-bold uppercase tracking-tighter animate-pulse">Exact Match Verified</span>
                        )}
                    </div>

                    {match ? (
                        <div className="bg-emerald-500/5 border border-emerald-500/20 p-4 rounded-lg">
                            <div className="flex justify-between items-center mb-1">
                                <span className="text-xs font-bold text-emerald-400">{match.label}</span>
                                <span className="text-[10px] font-mono text-emerald-500/70">Row #{match.row_id}</span>
                            </div>
                            <p className="text-[10px] text-zinc-400 leading-relaxed mb-3">{match.use}</p>
                            <div className="flex justify-between text-[8px] text-zinc-500 uppercase tracking-widest border-t border-emerald-500/10 pt-2">
                                <span>Slope Slop: {toFixedTrim(slop, 4)}</span>
                                <span>Pitch: {toPitchPer12(slope)}</span>
                            </div>
                        </div>
                    ) : (
                        <div className="bg-zinc-900/40 border border-zinc-800 p-4 rounded-lg text-center">
                            <span className="text-[9px] text-zinc-600 uppercase">No Canonical Match Found</span>
                            <p className="text-[8px] text-zinc-700 mt-1">Coordinate tension remains unresolved.</p>
                        </div>
                    )}
                </section>

                <section className="pt-2">
                    <p className="text-[8px] text-zinc-600 leading-relaxed italic uppercase tracking-tighter">
                        "The ball does not fly TO the world; the ball migrates toward the world's coordinates until the pulse resets."
                    </p>
                </section>
            </div>
        </div>
    );
};
