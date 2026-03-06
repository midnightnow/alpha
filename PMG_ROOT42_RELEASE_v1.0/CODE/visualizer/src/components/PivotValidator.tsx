import React, { useEffect, useState } from 'react';

/**
 * PIVOT VALIDATOR DASHBOARD
 * This bridges the Python Simulation Engine into the React Visualizer.
 * It monitors the 93 points of the Platonic Man in real-time.
 */

interface SimulationMetrics {
    pivot: number;            // 6.4807 (sqrt 42)
    shellBoundary: number;    // 7.1414 (sqrt 51)
    fillTime: number;         // 8975
    currentEntropy: number;
    maxRadialDrift: number;
    isPhaseLocked: boolean;
}

export const PivotValidator = () => {
    const [metrics, setMetrics] = useState<SimulationMetrics | null>(null);

    useEffect(() => {
        // Connect to the Python 777-Million Iteration Pipeline
        const ws = new WebSocket('ws://127.0.0.1:8975/ws');

        ws.onmessage = (event) => {
            try {
                const liveMetrics = JSON.parse(event.data);
                setMetrics(liveMetrics);
            } catch (e) {
                console.error("M/W Turbine Parsing Error:", e);
            }
        };

        ws.onclose = () => {
            console.warn("Connection to Sovereign Engine lost. 8975-second fill interrupted.");
        };

        return () => {
            ws.close();
        };
    }, []);

    if (!metrics) {
        return (
            <div className="absolute top-4 right-4 bg-black/80 border border-red-500 text-red-500 p-4 font-mono text-sm z-50">
                <div>[SYSTEM] INITIALIZING PIVOT PARAMETERS...</div>
                <div className="animate-pulse">AWAITING 8975 FILL LOCK...</div>
            </div>
        );
    }

    return (
        <div className="absolute top-4 right-4 bg-black/90 backdrop-blur-xl border border-rose-500/50 text-rose-100 p-5 font-mono text-[10px] shadow-[0_0_30px_rgba(244,63,94,0.15)] z-50 w-72 rounded-lg">
            <h3 className="text-rose-500 font-bold border-b border-rose-500/20 mb-4 pb-2 tracking-[0.2em] uppercase flex justify-between items-center">
                <span>◆ Sovereign Dashboard</span>
                <span className="text-[8px] bg-rose-500/10 px-1.5 py-0.5 rounded text-rose-400 border border-rose-500/20">V1.0</span>
            </h3>

            <div className="space-y-3">
                <div className="flex justify-between items-center">
                    <span className="text-zinc-500 uppercase tracking-widest">Pivot (√42)</span>
                    <span className="text-rose-200">{metrics.pivot.toFixed(6)}</span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="text-zinc-500 uppercase tracking-widest">Skybox (√51)</span>
                    <span className="text-rose-200">{metrics.shellBoundary.toFixed(6)}</span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="text-zinc-500 uppercase tracking-widest">Radial Drift</span>
                    <span className={metrics.maxRadialDrift > 0.00039 ? 'text-rose-500/70' : 'text-green-400/70'}>
                        {metrics.maxRadialDrift.toFixed(8)}
                    </span>
                </div>

                <div className="pt-4 mt-2 border-t border-rose-500/10 space-y-2">
                    <div className="flex justify-between items-end mb-1">
                        <span className="text-zinc-500 uppercase text-[9px] tracking-widest">Active Fill (8975s)</span>
                        <span className="text-rose-400 text-[9px]">
                            {metrics.isPhaseLocked ? '87.63% TAUT' : 'GAP INTRUSION'}
                        </span>
                    </div>
                    {/* Progress Bar for the 8975-second cycle */}
                    <div className="w-full h-1 bg-zinc-900 rounded-full overflow-hidden border border-rose-500/10">
                        <motion.div
                            className={`h-full ${metrics.isPhaseLocked ? 'bg-rose-500' : 'bg-rose-900'}`}
                            initial={false}
                            animate={{ width: `${(metrics.pivot / metrics.shellBoundary) * 100}%` }}
                            style={{ width: `${(metrics.pivot / metrics.shellBoundary) * 100}%` }}
                        />
                    </div>
                    <div className="flex justify-between text-[8px] text-zinc-600 uppercase tracking-tighter">
                        <span>0.00 Void</span>
                        <span>{metrics.isPhaseLocked ? 'Active' : 'Hades Gap'}</span>
                        <span>10242 Reset</span>
                    </div>
                </div>
            </div>

            <div className="mt-6 pt-2 text-center">
                {metrics.isPhaseLocked ? (
                    <div className="flex items-center justify-center gap-2">
                        <span className="w-1.5 h-1.5 bg-rose-500 rounded-full animate-ping" />
                        <span className="text-rose-500 font-bold tracking-[0.3em] text-[9px] uppercase">Lattice Sealed</span>
                    </div>
                ) : (
                    <div className="flex items-center justify-center gap-2">
                        <span className="w-1.5 h-1.5 bg-red-900 rounded-full" />
                        <span className="text-red-900 font-bold tracking-[0.3em] text-[9px] uppercase animate-pulse">Gap Detected</span>
                    </div>
                )}
            </div>
        </div>
    );
};
