import React, { useState, useEffect } from 'react';
import { Play, RotateCcw, Activity, CheckCircle2, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { findOptimalEpsilon, generateLatticePoints, calculateHullVolume } from '../math/geometry';

interface Props {
  onResult: (epsilon: number, volume: number) => void;
}

const OptimizerPanel: React.FC<Props> = ({ onResult }) => {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<{ epsilon: number; volume: number; iterations: number } | null>(null);
  const [currentEpsilon, setCurrentEpsilon] = useState(0);
  const [currentVolume, setCurrentVolume] = useState(0);

  const runOptimization = async () => {
    setIsOptimizing(true);
    setResult(null);
    setProgress(0);

    // Simulate optimization steps for UI feedback
    const target = 42.0;
    const low = 0.0;
    const high = 0.1;

    // Actual calculation
    const optResult = findOptimalEpsilon(target, low, high);

    // Animation steps
    for (let i = 0; i <= 20; i++) {
      setProgress(i * 5);
      const tempEps = low + (high - low) * (i / 20);
      setCurrentEpsilon(tempEps);
      setCurrentVolume(calculateHullVolume(generateLatticePoints(tempEps)));
      await new Promise(resolve => setTimeout(resolve, 50));
    }

    setResult(optResult);
    setCurrentEpsilon(optResult.epsilon);
    setCurrentVolume(optResult.volume);
    setIsOptimizing(false);
    onResult(optResult.epsilon, optResult.volume);
  };

  const reset = () => {
    setResult(null);
    setCurrentEpsilon(0);
    setCurrentVolume(calculateHullVolume(generateLatticePoints(0)));
    setProgress(0);
  };

  useEffect(() => {
    setCurrentVolume(calculateHullVolume(generateLatticePoints(0)));
  }, []);

  return (
    <div className="bg-[#151619] border border-white/10 rounded-xl p-6 shadow-2xl h-full flex flex-col">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-lg font-medium text-white tracking-tight flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-500" />
            Calibration Search
          </h2>
          <p className="text-xs text-white/40 font-mono uppercase tracking-widest mt-1">
            Synthetic Parameter Tuning
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={reset}
            className="p-2 rounded-lg border border-white/10 hover:bg-white/5 transition-colors text-white/60"
            title="Reset"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={runOptimization}
            disabled={isOptimizing}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${isOptimizing
                ? 'bg-white/5 text-white/20 cursor-not-allowed'
                : 'bg-emerald-500 hover:bg-emerald-400 text-black shadow-[0_0_20px_rgba(16,185,129,0.3)]'
              }`}
          >
            <Play className="w-4 h-4 fill-current" />
            {isOptimizing ? 'Optimizing...' : 'Run Script'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-8">
        <div className="bg-black/40 border border-white/5 rounded-lg p-4">
          <div className="text-[10px] font-mono text-white/40 uppercase tracking-widest mb-1">Equilibrium Tension</div>
          <div className="text-2xl font-mono text-white">42.000000</div>
        </div>
        <div className="bg-black/40 border border-white/5 rounded-lg p-4">
          <div className="text-[10px] font-mono text-white/40 uppercase tracking-widest mb-1">Current Volume</div>
          <div className="text-2xl font-mono text-emerald-400 tabular-nums">
            {currentVolume.toFixed(6)}
          </div>
        </div>
      </div>

      <div className="flex-1 space-y-6">
        <div>
          <div className="flex justify-between text-[10px] font-mono text-white/40 uppercase tracking-widest mb-2">
            <span>Phase Offset (ε)</span>
            <span className="text-white/80 tabular-nums">{currentEpsilon.toFixed(8)} rad</span>
          </div>
          <div className="h-1 bg-white/5 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-emerald-500"
              initial={{ width: '0%' }}
              animate={{ width: `${(currentEpsilon / 0.1) * 100}%` }}
              transition={{ type: 'spring', bounce: 0, duration: 0.2 }}
            />
          </div>
        </div>

        <AnimatePresence mode="wait">
          {result ? (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-4"
            >
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-emerald-400">Tension Stabilized</div>
                  <div className="text-xs text-emerald-400/60 mt-1 leading-relaxed">
                    Found ε = {result.epsilon.toFixed(8)} radians.
                    The shell is now perfectly balanced against the void at 42.0.
                  </div>
                </div>
              </div>
            </motion.div>
          ) : isOptimizing ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-white/5 border border-white/10 rounded-lg p-4"
            >
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
                <div className="text-xs text-white/60 font-mono uppercase tracking-widest">
                  Processing iterations... {progress}%
                </div>
              </div>
            </motion.div>
          ) : (
            <div className="bg-white/5 border border-white/10 rounded-lg p-4 border-dashed">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-white/20 shrink-0 mt-0.5" />
                <div className="text-xs text-white/40 leading-relaxed italic">
                  Waiting for optimization trigger. The Path B script will perform a root-finding search over ε to find the exact geometric closure.
                </div>
              </div>
            </div>
          )}
        </AnimatePresence>
      </div>

      <div className="mt-8 pt-6 border-t border-white/5">
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <div className="text-[10px] font-mono text-white/20 uppercase tracking-widest mb-2">Axiom Status</div>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5, 6].map(i => (
                <div
                  key={i}
                  className={`h-1 flex-1 rounded-full ${result && i <= 6 ? 'bg-emerald-500' : 'bg-white/10'
                    }`}
                />
              ))}
            </div>
          </div>
          <div className="text-[10px] font-mono text-white/40 uppercase tracking-widest">
            ρ = {result ? '1.000' : 'Tuning'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OptimizerPanel;
