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
        <div className="absolute top-4 right-4 bg-black/80 border border-green-500 text-green-400 p-4 font-mono text-sm shadow-[0_0_15px_rgba(0,255,0,0.3)] z-50">
            <h3 className="text-white font-bold border-b border-green-500/50 mb-2 pb-1">
                ◆ PIVOT DASHBOARD
            </h3>

            <div className="grid grid-cols-2 gap-x-6 gap-y-1">
                <span className="text-gray-400">PIVOT (√42)</span>
                <span className="text-right">{metrics.pivot.toFixed(5)}</span>

                <span className="text-gray-400">SKYBOX (√51)</span>
                <span className="text-right">{metrics.shellBoundary.toFixed(5)}</span>

                <span className="text-gray-400">ENTROPY</span>
                <span className="text-right">{metrics.currentEntropy.toFixed(5)} bits</span>

                <span className="text-gray-400">RADIAL DRIFT</span>
                <span className={`text-right ${metrics.maxRadialDrift > 0.00039 ? 'text-red-500' : 'text-green-400'}`}>
                    {metrics.maxRadialDrift.toFixed(6)}
                </span>
            </div>

            <div className="mt-3 pt-2 border-t border-green-500/50 text-center font-bold">
                {metrics.isPhaseLocked ? (
                    <span className="text-green-400 tracking-widest">PHASE LOCKED: TRUE</span>
                ) : (
                    <span className="text-red-500 tracking-widest animate-pulse">PHASE LOST: PRUNING</span>
                )}
            </div>
        </div>
    );
};
