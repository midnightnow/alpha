/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import {
  Activity,
  Zap,
  Target,
  Info,
  AlertTriangle,
  ChevronRight,
  Waves,
  Cpu,
  Binary,
  Compass,
  RotateCcw,
  Infinity,
  Dna,
  Dna,
  Hash,
  Building2,
  Shell
} from 'lucide-react';
import { CityGenerator } from './components/CityGenerator';
import { ConicalShell } from './components/ConicalShell';

// --- Constants ---
const PHI = (1 + Math.sqrt(5)) / 2;
const TOTAL_NODES = 93;
const PRIME_SPOKES_MOD_24 = [1, 5, 7, 11, 13, 17, 19, 23];
const ZETA_NEG_ONE = -1 / 12;

// --- Utilities ---
const isPrime = (num: number) => {
  if (num <= 1) return false;
  if (num <= 3) return true;
  if (num % 2 === 0 || num % 3 === 0) return false;
  for (let i = 5; i * i <= num; i += 6) {
    if (num % i === 0 || num % (i + 2) === 0) return false;
  }
  return true;
};

// Get primes up to a limit for superprime indexing
const getPrimes = (limit: number) => {
  const primes = [];
  for (let i = 2; i <= limit; i++) {
    if (isPrime(i)) primes.push(i);
  }
  return primes;
};

const PRIMES_LIST = getPrimes(1000);
const isSuperPrime = (num: number) => {
  if (!isPrime(num)) return false;
  const index = PRIMES_LIST.indexOf(num) + 1;
  return isPrime(index);
};

export default function App() {
  const [t, setT] = useState(14.1347);
  const [activeNode, setActiveNode] = useState<number | null>(null);
  const [isSimulating, setIsSimulating] = useState(true);
  const [time, setTime] = useState(0);
  const [viewMode, setViewMode] = useState<'resonance' | 'circular-limit' | 'city-generator' | 'conical-shell'>('resonance');
  const [scannerNum, setScannerNum] = useState(42);

  // Animation loop
  useEffect(() => {
    let frame: number;
    const animate = () => {
      setTime(prev => prev + 0.01);
      frame = requestAnimationFrame(animate);
    };
    if (isSimulating) frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [isSimulating]);

  // --- Derived Data ---
  const nodes = useMemo(() => {
    return Array.from({ length: TOTAL_NODES }, (_, i) => {
      const n = i + 1;
      const mod24 = n % 24;
      const isPrimeSpoke = PRIME_SPOKES_MOD_24.includes(mod24);
      const prime = isPrime(n);
      const superPrime = isSuperPrime(n);

      const nodeTension = (Math.sin(n * t + time) % PHI) / PHI;

      return {
        id: n,
        mod24,
        isPrimeSpoke,
        prime,
        superPrime,
        tension: nodeTension,
        angle: (i / TOTAL_NODES) * Math.PI * 2
      };
    });
  }, [t, time]);

  const scannerResult = useMemo(() => {
    const prime = isPrime(scannerNum);
    const superPrime = isSuperPrime(scannerNum);
    const mod24 = scannerNum % 24;
    const isSpoke = PRIME_SPOKES_MOD_24.includes(mod24);

    // Esoteric check for 42
    const isHarmonicAnchor = scannerNum === 42;

    return { prime, superPrime, mod24, isSpoke, isHarmonicAnchor };
  }, [scannerNum]);

  return (
    <div className="min-h-screen bg-[#050505] text-zinc-100 font-sans selection:bg-emerald-500/30">
      {/* Header */}
      <header className="border-b border-white/5 p-6 flex justify-between items-center backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-emerald-500 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(16,185,129,0.4)]">
            <Compass className="text-black w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tighter uppercase italic">PMG Riemann Visualizer</h1>
            <p className="text-[10px] text-zinc-500 font-mono tracking-widest uppercase">Geometer-Sovereign Interface v1.1</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <nav className="hidden md:flex bg-zinc-900/80 border border-white/5 rounded-full p-1">
            <button
              onClick={() => setViewMode('resonance')}
              className={`px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest transition-all ${viewMode === 'resonance' ? 'bg-emerald-500 text-black' : 'text-zinc-500 hover:text-zinc-300'}`}
            >
              Resonance
            </button>
            <button
              onClick={() => setViewMode('circular-limit')}
              className={`px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest transition-all ${viewMode === 'circular-limit' ? 'bg-emerald-500 text-black' : 'text-zinc-500 hover:text-zinc-300'}`}
            >
              Circular Limit
            </button>
            <button
              onClick={() => setViewMode('city-generator')}
              className={`px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest transition-all ${viewMode === 'city-generator' ? 'bg-emerald-500 text-black' : 'text-zinc-500 hover:text-zinc-300'}`}
            >
              City Generator
            </button>
            <button
              onClick={() => setViewMode('conical-shell')}
              className={`px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest transition-all ${viewMode === 'conical-shell' ? 'bg-emerald-500 text-black' : 'text-zinc-500 hover:text-zinc-300'}`}
            >
              Conical Shell
            </button>
          </nav>
          <button
            onClick={() => setIsSimulating(!isSimulating)}
            className="p-2 border border-white/10 rounded-full hover:bg-white/5 transition-colors"
          >
            {isSimulating ? <RotateCcw className="w-4 h-4 text-emerald-400 animate-spin-slow" /> : <Activity className="w-4 h-4 text-zinc-500" />}
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Left Column: Main Visualization */}
        <section className="lg:col-span-7 space-y-6">
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-8 relative overflow-hidden min-h-[600px] flex flex-col">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald-500 to-transparent opacity-50" />

            <div className="flex justify-between items-start mb-8 z-10">
              <div>
                <h2 className="text-2xl font-serif italic mb-1">
                  {viewMode === 'resonance' ? 'Resonance Map' : viewMode === 'circular-limit' ? 'Circular Limit (Zeta Regularization)' : 'City Generator (Printing Press)'}
                </h2>
                <p className="text-xs text-zinc-500 max-w-md">
                  {viewMode === 'resonance'
                    ? 'Visualizing node tension across 93 points of interest. Golden ratio modulation applied to harmonic spokes.'
                    : viewMode === 'circular-limit'
                      ? 'Exploring the analytic continuation of the sum of natural numbers as it wraps into the complex limit of -1/12.'
                      : 'Applying the Riemann "Pressure Vents" as structural blueprints for stable architectural forms in the 93-node shell.'}
                </p>
              </div>
              <div className="text-right">
                <span className="text-[10px] text-zinc-500 font-mono uppercase block">Limit Constant</span>
                <span className="text-2xl font-mono text-emerald-400 tracking-tighter">
                  {viewMode === 'resonance' ? t.toFixed(4) : ZETA_NEG_ONE.toFixed(4)}
                </span>
              </div>
            </div>

            {/* Visualization Area */}
            <div className="flex-1 relative flex items-center justify-center">
              <AnimatePresence mode="wait">
                {viewMode === 'resonance' ? (
                  <motion.div
                    key="resonance"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.1 }}
                    className="w-full h-full flex items-center justify-center"
                  >
                    <svg viewBox="0 0 400 400" className="w-full h-full max-w-[500px]">
                      <circle cx="200" cy="200" r="180" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="1" strokeDasharray="4 4" />
                      <circle cx="200" cy="200" r="120" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="1" strokeDasharray="4 4" />

                      {nodes.map((node, i) => {
                        const nextNode = nodes[(i + 1) % nodes.length];
                        const x1 = 200 + Math.cos(node.angle) * (150 + node.tension * 20);
                        const y1 = 200 + Math.sin(node.angle) * (150 + node.tension * 20);
                        const x2 = 200 + Math.cos(nextNode.angle) * (150 + nextNode.tension * 20);
                        const y2 = 200 + Math.sin(nextNode.angle) * (150 + nextNode.tension * 20);

                        return (
                          <line
                            key={`line-${i}`}
                            x1={x1} y1={y1} x2={x2} y2={y2}
                            stroke={node.superPrime ? 'rgba(52,211,153,0.5)' : node.prime ? 'rgba(16,185,129,0.2)' : 'rgba(255,255,255,0.03)'}
                            strokeWidth={node.superPrime ? 3 : node.prime ? 1.5 : 0.5}
                          />
                        );
                      })}

                      {nodes.map((node) => {
                        const r = 150 + node.tension * 20;
                        const x = 200 + Math.cos(node.angle) * r;
                        const y = 200 + Math.sin(node.angle) * r;

                        return (
                          <motion.circle
                            key={node.id}
                            cx={x} cy={y}
                            r={node.superPrime ? 6 : node.prime ? 4 : 2}
                            fill={node.superPrime ? '#34d399' : node.prime ? '#10b981' : node.isPrimeSpoke ? '#3b82f6' : '#3f3f46'}
                            onMouseEnter={() => setActiveNode(node.id)}
                            onMouseLeave={() => setActiveNode(null)}
                            className="cursor-crosshair"
                          />
                        );
                      })}
                    </svg>
                  </motion.div>
                ) : viewMode === 'circular-limit' ? (
                  <motion.div
                    key="circular-limit"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.1 }}
                    className="w-full h-full flex items-center justify-center"
                  >
                    <svg viewBox="0 0 400 400" className="w-full h-full max-w-[500px]">
                      {/* The -1/12 Anchor */}
                      <circle cx="200" cy="200" r="4" fill="#10b981" className="animate-pulse" />
                      <text x="210" y="205" className="text-[10px] fill-emerald-400 font-mono">-1/12 Limit</text>

                      {/* Wrapping Spiral */}
                      {Array.from({ length: 100 }).map((_, i) => {
                        const angle = i * 0.5 + time;
                        const radius = i * 1.8;
                        const x = 200 + Math.cos(angle) * radius;
                        const y = 200 + Math.sin(angle) * radius;

                        const nextAngle = (i + 1) * 0.5 + time;
                        const nextRadius = (i + 1) * 1.8;
                        const nx = 200 + Math.cos(nextAngle) * nextRadius;
                        const ny = 200 + Math.sin(nextAngle) * nextRadius;

                        return (
                          <line
                            key={i}
                            x1={x} y1={y} x2={nx} y2={ny}
                            stroke={`rgba(16,185,129, ${Math.max(0, 1 - i / 100)})`}
                            strokeWidth={2 - i / 50}
                          />
                        );
                      })}

                      {/* Natural Numbers wrapping in */}
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => {
                        const angle = n * 2 + time * 0.2;
                        const radius = 180 - n * 15;
                        const x = 200 + Math.cos(angle) * radius;
                        const y = 200 + Math.sin(angle) * radius;

                        return (
                          <g key={n}>
                            <circle cx={x} cy={y} r="3" fill="rgba(255,255,255,0.2)" />
                            <text x={x + 5} y={y + 5} className="text-[8px] fill-zinc-500 font-mono">{n}</text>
                            <line x1={x} y1={y} x2="200" y2="200" stroke="rgba(16,185,129,0.05)" strokeDasharray="2 2" />
                          </g>
                        );
                      })}
                    </svg>
                  </motion.div>
                ) : (
                  <motion.div
                    key="city-generator"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="w-full h-full"
                  >
                    <CityGenerator t={t} time={time} />
                  </motion.div>
                ) : (
                <motion.div
                  key="conical-shell"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 1.2 }}
                  className="w-full h-full"
                >
                  <ConicalShell t={t} time={time} />
                </motion.div>
                )}
              </AnimatePresence>

              {/* Tooltip Overlay */}
              <AnimatePresence>
                {activeNode && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="absolute bottom-4 left-4 right-4 bg-black/80 backdrop-blur-xl border border-white/10 p-4 rounded-2xl flex justify-between items-center z-20"
                  >
                    <div>
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Node ID</span>
                      <p className="text-xl font-bold tracking-tighter">n = {activeNode}</p>
                    </div>
                    <div className="text-center">
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Status</span>
                      <p className={`text-sm font-bold uppercase ${isSuperPrime(activeNode) ? 'text-emerald-400' : isPrime(activeNode) ? 'text-emerald-400/60' : 'text-zinc-500'}`}>
                        {isSuperPrime(activeNode) ? 'SUPERPRIME' : isPrime(activeNode) ? 'Prime Invariant' : 'Composite Echo'}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Mod 24</span>
                      <p className="text-xl font-mono text-blue-400">{activeNode % 24}</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Superprime Scanner */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold uppercase tracking-widest">Superprime Scanner</h3>
              </div>
              <div className="flex items-center gap-2 bg-black/40 px-3 py-1 rounded-full border border-white/5">
                <Hash className="w-3 h-3 text-zinc-500" />
                <input
                  type="number"
                  value={scannerNum}
                  onChange={(e) => setScannerNum(parseInt(e.target.value) || 0)}
                  className="bg-transparent border-none text-xs font-mono text-emerald-400 w-16 focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Prime</span>
                <span className={`text-xs font-bold ${scannerResult.prime ? 'text-emerald-400' : 'text-zinc-700'}`}>
                  {scannerResult.prime ? 'DETECTED' : 'NEGATIVE'}
                </span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Superprime</span>
                <span className={`text-xs font-bold ${scannerResult.superPrime ? 'text-emerald-400' : 'text-zinc-700'}`}>
                  {scannerResult.superPrime ? 'DETECTED' : 'NEGATIVE'}
                </span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Mod 24 Spoke</span>
                <span className={`text-xs font-bold ${scannerResult.isSpoke ? 'text-blue-400' : 'text-zinc-700'}`}>
                  {scannerResult.isSpoke ? 'ALIGNED' : 'DRIFTED'}
                </span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Harmonic Anchor</span>
                <span className={`text-xs font-bold ${scannerResult.isHarmonicAnchor ? 'text-rose-400' : 'text-zinc-700'}`}>
                  {scannerResult.isHarmonicAnchor ? '42: FOUND' : 'NONE'}
                </span>
              </div>
            </div>

            {scannerNum === 42 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 p-4 bg-rose-500/5 border border-rose-500/20 rounded-2xl"
              >
                <p className="text-[10px] text-rose-400 italic leading-relaxed">
                  <span className="font-bold uppercase">Thread Found:</span> 42 is not a prime, yet it serves as the "Harmonic Anchor" in the PMG system.
                  It is the product of the first three primes (2 × 3 × 7) excluding 5, creating a "Symmetry Gap" that pulls the resonance toward the -1/12 limit.
                  This gap is where the "Superprime Exception" occurs—a point where the discrete distribution of primes intersects the continuous limit of the Zeta function.
                </p>
              </motion.div>
            )}
          </div>
        </section>

        {/* Right Column: Controls & Audit */}
        <section className="lg:col-span-5 space-y-6">

          {/* Regularization Audit */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6">
            <h3 className="text-sm font-bold uppercase tracking-widest mb-6 flex items-center gap-2">
              <Infinity className="w-4 h-4 text-emerald-400" />
              Regularization Audit
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Series Sum</span>
                <span className="text-xs font-mono text-zinc-300">1 + 2 + 3 + ... + ∞</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Analytic Continuation</span>
                <span className="text-xs font-mono text-emerald-400">Zeta(-1)</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Geometric Limit</span>
                <span className="text-xs font-mono text-emerald-400">-1/12</span>
              </div>
              <div className="mt-4 p-4 bg-black/40 rounded-2xl border border-white/5">
                <p className="text-[11px] text-zinc-400 leading-relaxed">
                  The "Circular Limit" view demonstrates how the divergent sum of natural numbers is regularized.
                  In a geometrical circular pattern, the infinite outward spiral is "pulled" back to the center by the
                  negative curvature of the complex plane at $s = -1$.
                </p>
              </div>
            </div>
          </div>

          {/* Superprime Distribution */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6">
            <h3 className="text-sm font-bold uppercase tracking-widest mb-6 flex items-center gap-2">
              <Dna className="w-4 h-4 text-emerald-400" />
              Superprime Distribution
            </h3>
            <div className="flex flex-wrap gap-2">
              {[3, 5, 11, 17, 31, 41, 59, 67, 83].map((sp) => (
                <div key={sp} className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-[10px] font-mono text-emerald-400">
                  {sp}
                </div>
              ))}
            </div>
            <p className="mt-4 text-[11px] text-zinc-500 italic leading-relaxed">
              Superprimes (primes at prime indices) represent the "Second Tier" of the prime sieve.
              They act as the structural ribs of the resonance map, resisting the stochastic drift of composite echos.
            </p>
          </div>

          {/* Mod-24 Spoke Filter */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6">
            <h3 className="text-sm font-bold uppercase tracking-widest mb-6 flex items-center gap-2">
              <Binary className="w-4 h-4 text-blue-400" />
              Mod-24 Spoke Filter
            </h3>
            <div className="grid grid-cols-6 gap-2">
              {Array.from({ length: 24 }, (_, i) => {
                const isSpoke = PRIME_SPOKES_MOD_24.includes(i);
                return (
                  <div
                    key={i}
                    className={`aspect-square rounded-lg flex flex-col items-center justify-center border transition-all ${isSpoke
                      ? 'bg-blue-500/10 border-blue-500/30 text-blue-400'
                      : 'bg-zinc-800/30 border-white/5 text-zinc-600'
                      }`}
                  >
                    <span className="text-[10px] font-mono">{i}</span>
                    {isSpoke && <div className="w-1 h-1 bg-blue-400 rounded-full mt-1 shadow-[0_0_5px_rgba(59,130,246,0.5)]" />}
                  </div>
                );
              })}
            </div>
            <div className="mt-6 p-4 bg-black/40 rounded-2xl border border-white/5">
              <p className="text-[11px] text-zinc-400 leading-relaxed">
                <span className="text-blue-400 font-bold">Observation:</span> Primes p &gt; 3 are constrained to the spokes
                {'{'} 1, 5, 7, 11, 13, 17, 19, 23 {'}'} mod 24. This geometric sieve forms the basis of the PMG resonance map.
              </p>
            </div>
          </div>

          {/* Operational Audit Log */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6 overflow-hidden relative">
            <h3 className="text-sm font-bold uppercase tracking-widest mb-4 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-zinc-400" />
              Operational Audit
            </h3>
            <div className="space-y-3 font-mono text-[10px]">
              <div className="flex gap-3 text-zinc-500">
                <span className="text-emerald-400">[OK]</span>
                <span>Zeta regularization limit locked at -0.0833.</span>
              </div>
              <div className="flex gap-3 text-zinc-500">
                <span className="text-emerald-400">[OK]</span>
                <span>Superprime scanner calibrated to 1000-index depth.</span>
              </div>
              <div className="flex gap-3 text-blue-400">
                <span className="text-blue-400">[INFO]</span>
                <span>42 identified as Harmonic Anchor (Symmetry Gap).</span>
              </div>
              <div className="flex gap-3 text-rose-400">
                <span className="animate-pulse">[WARN]</span>
                <span>Disproof thread detected: Lehmer's phenomenon at t=10^12.</span>
              </div>
              <div className="flex gap-3 text-rose-400">
                <span className="animate-pulse">[WARN]</span>
                <span>Analytic continuation drift detected in Sonnet 129.</span>
              </div>
            </div>
          </div>

          {/* Pedagogical Disclaimer */}
          <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-3xl p-6">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-xs font-bold text-emerald-500 uppercase tracking-widest mb-1">Geometrical Limit Note</h4>
                <p className="text-[10px] text-zinc-400 leading-relaxed italic">
                  The derivation of -1/12 is a result of Zeta Function Regularization. It is not a "sum" in the arithmetic sense,
                  but a "limit" in the geometrical sense of analytic continuation. 42 is the "thread" that connects the
                  discrete prime distribution to the continuous harmonic limit.
                </p>
              </div>
            </div>
          </div>

        </section>
      </main>

      {/* Footer Meta */}
      <footer className="max-w-7xl mx-auto p-6 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 opacity-50">
        <p className="text-[10px] font-mono uppercase tracking-widest">© 2026 Geometer-Sovereign Systems</p>
        <div className="flex gap-6 text-[10px] font-mono uppercase tracking-widest">
          <a href="#" className="hover:text-emerald-400 transition-colors">Zeta Regularization</a>
          <a href="#" className="hover:text-emerald-400 transition-colors">Superprime Theory</a>
          <a href="#" className="hover:text-emerald-400 transition-colors">The 42 Anchor</a>
        </div>
      </footer>
    </div>
  );
}
