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
  Hash,
  Building2,
  Box,
  Layers,
  Printer
} from 'lucide-react';

import { SoftCreature } from './components/SoftCreature';
import { CityGenerator } from './components/CityGenerator';

// --- Constants ---
const PHI = (1 + Math.sqrt(5)) / 2;
const ROOT_42 = Math.sqrt(42); // ≈ 6.4807 — The Harmonic Anchor
const HADES_GAP = 0.1237;       // The Phase V Constant (12.37%)
const TOTAL_NODES = 93;          // Icosahedral Phase Matrix: 12V + 20F + 60E + 1C
const PRIME_SPOKES_MOD_24 = [1, 5, 7, 11, 13, 17, 19, 23];
const ZETA_NEG_ONE = -1 / 12;
const V_93_CAPACITY = 93;        // Geofont 13 Vitrification Criterion

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

const getPrimes = (limit: number) => {
  const primes = [];
  for (let i = 2; i <= limit; i++) {
    if (isPrime(i)) primes.push(i);
  }
  return primes;
};

const PRIMES_LIST = getPrimes(1000);

const getMobius = (n: number) => {
  if (n === 1) return 1;
  let p = 0;
  let temp = n;
  for (let i = 2; i * i <= temp; i++) {
    if (temp % i === 0) {
      temp /= i;
      p++;
      if (temp % i === 0) return 0;
    }
  }
  if (temp > 1) p++;
  return p % 2 === 0 ? 1 : -1;
};

const getLi = (n: number) => {
  if (n < 2) return 0;
  // Simple approximation for Li(n) ~ n/ln(n)
  return n / Math.log(n);
};

const getVonMangoldt = (n: number) => {
  if (n <= 1) return 0;
  // Check if n is a power of a prime
  for (let p of PRIMES_LIST) {
    if (p > n) break;
    let temp = n;
    while (temp % p === 0) {
      temp /= p;
    }
    if (temp === 1) return Math.log(p);
  }
  return 0;
};

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
  const [viewMode, setViewMode] = useState<'resonance' | 'circular-limit' | 'city-press' | 'stabilisated-cone' | 'nautilus-prime'>('resonance');
  const [scannerNum, setScannerNum] = useState(42);
  const [cityBase, setCityBase] = useState(24);
  const [pressDepth, setPressDepth] = useState(0.8);
  const [platonicRatio, setPlatonicRatio] = useState<'1:1' | '2:3' | '3:4' | '4:5'>('1:1');
  const [civDensity, setCivDensity] = useState(0.5);
  const [vitrification, setVitrification] = useState(0.42);
  const [softMobility, setSoftMobility] = useState(0.5);
  const [bioSync, setBioSync] = useState(0.42);
  const [aFrameStability, setAFrameStability] = useState(30);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [rollingFrequency, setRollingFrequency] = useState(0);

  // Diamond Dust Trail State — the snail eats its own ketheric wake
  const [dustTrails, setDustTrails] = useState<{ x: number, y: number, age: number, phi: number }[]>([]);

  // Accumulate diamond dust trails from navigation path
  useEffect(() => {
    if (!isSimulating || vitrification < 0.1) return;
    const interval = setInterval(() => {
      setDustTrails(prev => {
        // Emit new dust particles along the √42 radiation arms
        const newDust = Array.from({ length: Math.floor(vitrification * 6) }, (_, i) => {
          const armAngle = (i / 6) * Math.PI * 2 + time * 0.1;
          const radius = 50 + Math.sin(time * ROOT_42 + i) * 80;
          return {
            x: Math.cos(armAngle) * radius,
            y: Math.sin(armAngle) * radius,
            age: 0,
            phi: armAngle * PHI
          };
        });
        // Age existing trails, remove old ones, keep max 200
        const aged = prev.map(d => ({ ...d, age: d.age + 1 })).filter(d => d.age < 120);
        return [...aged, ...newDust].slice(-200);
      });
    }, 100);
    return () => clearInterval(interval);
  }, [isSimulating, vitrification, time]);

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
    const ratioMap = { '1:1': 1, '2:3': 1.5, '3:4': 1.33, '4:5': 1.25 };
    const multiplier = ratioMap[platonicRatio];

    // Riemann Zeta Zeros (Imaginary Parts)
    const zeros = [14.1347, 21.0220, 25.0108, 30.4248, 32.9350];
    let totalEntropy = 0;

    const computedNodes = Array.from({ length: TOTAL_NODES }, (_, i) => {
      const n = i + 1;
      const modBase = n % cityBase;
      const mod24 = n % 24;
      const isPrimeSpoke = PRIME_SPOKES_MOD_24.includes(mod24);
      const prime = isPrime(n);
      const superPrime = isSuperPrime(n);
      const mobius = getMobius(n);
      const li = getLi(n);
      const vonMangoldt = getVonMangoldt(n);
      const actualPrimes = PRIMES_LIST.filter(p => p <= n).length;
      const liError = actualPrimes - li;

      // Necessary Math: Multi-zero superposition resonance
      let nodeTension = 0;
      zeros.forEach((gamma, idx) => {
        nodeTension += Math.sin(gamma * Math.log(n + 1) * multiplier + time * (1 + rollingFrequency)) / (idx + 1);
      });
      nodeTension = (nodeTension / zeros.length) + (mobius * 0.1) + (vonMangoldt * 0.05);

      const height = (Math.abs(nodeTension) * 100 * pressDepth) + (prime ? 40 : 10);
      totalEntropy += Math.abs(nodeTension);

      // Cone coordinates (Golden Spiral expansion)
      const coneRadius = 160 * (1 - n / (TOTAL_NODES * 1.2)) * (1 / PHI) * zoomLevel;
      const coneAngle = (mod24 / 24) * Math.PI * 2 + (n * 0.05) + (time * rollingFrequency);
      const coneZ = n * 3 * zoomLevel;

      // Root 42 Radiation Arms
      const isRadiationArm = n % 42 === 0 || 42 % n === 0 || Math.abs(n - 42) < 3;

      // Generate satellites for primes
      const satellites = prime ? Array.from({ length: Math.floor(civDensity * 4) }, (_, j) => ({
        id: j,
        angle: (j / 4) * Math.PI * 2 + time,
        dist: 15 + Math.sin(time + n) * 5,
        h: height * 0.3
      })) : [];

      return {
        id: n,
        modBase,
        mod24,
        isPrimeSpoke,
        prime,
        superPrime,
        mobius,
        liError,
        vonMangoldt,
        tension: nodeTension,
        height,
        angle: (i / TOTAL_NODES) * Math.PI * 2,
        coneX: Math.cos(coneAngle) * coneRadius,
        coneY: Math.sin(coneAngle) * coneRadius,
        coneZ,
        isRadiationArm,
        gridX: i % 10,
        gridY: Math.floor(i / 10),
        satellites
      };
    });

    return { nodes: computedNodes, entropy: (totalEntropy / TOTAL_NODES).toFixed(4) };
  }, [t, time, cityBase, pressDepth, platonicRatio, civDensity, zoomLevel, rollingFrequency]);

  const { nodes: nodeList, entropy: geometricEntropy } = nodes;

  const scannerResult = useMemo(() => {
    const prime = isPrime(scannerNum);
    const superPrime = isSuperPrime(scannerNum);
    const mod24 = scannerNum % 24;
    const isSpoke = PRIME_SPOKES_MOD_24.includes(mod24);
    const isHarmonicAnchor = scannerNum === 42;
    const mobius = getMobius(scannerNum);
    const vonMangoldt = getVonMangoldt(scannerNum);

    // Find gap to nearest prime
    let lower = scannerNum, upper = scannerNum;
    while (lower > 1 && !isPrime(lower)) lower--;
    while (!isPrime(upper)) upper++;
    const gap = upper - lower;

    return { prime, superPrime, mod24, isSpoke, isHarmonicAnchor, mobius, gap, vonMangoldt };
  }, [scannerNum]);

  return (
    <div className="min-h-screen bg-[#050505] text-zinc-100 font-sans selection:bg-emerald-500/30">
      {/* Header */}
      <header className="border-b border-white/5 p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-emerald-500 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(16,185,129,0.4)] shrink-0">
            <Compass className="text-black w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tighter uppercase italic">PMG Diamond Navigator</h1>
            <p className="text-[10px] text-zinc-500 font-mono tracking-widest uppercase">CRYSTALLISED FORM v2.0.0 — √42 TUNED</p>
          </div>
        </div>
        <div className="flex items-center gap-4 w-full md:w-auto overflow-x-auto no-scrollbar pb-1 md:pb-0">
          <nav className="flex gap-1 bg-zinc-900/80 border border-white/5 rounded-full p-1 shrink-0">
            {['resonance', 'circular-limit', 'city-press', 'stabilisated-cone', 'nautilus-prime'].map((mode) => (
              <button
                key={mode}
                onClick={() => setViewMode(mode as any)}
                className={`whitespace-nowrap px-3 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest transition-all ${viewMode === mode ? 'bg-emerald-500 text-black' : 'text-zinc-500 hover:text-zinc-300'}`}
              >
                {mode.replace('-', ' ')}
              </button>
            ))}
          </nav>
          <button
            onClick={() => setIsSimulating(!isSimulating)}
            className="p-2 border border-white/10 rounded-full hover:bg-white/5 transition-colors shrink-0"
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
                  {viewMode === 'resonance' ? 'Resonance Navigation' : viewMode === 'circular-limit' ? 'Circular Limit' : viewMode === 'city-press' ? 'City Press: Generative Proof' : viewMode === 'stabilisated-cone' ? 'Stabilisated Cone: Root 42 Axis' : 'Nautilus Prime: Crystallised Navigator'}
                </h2>
                <p className="text-xs text-zinc-500 max-w-md">
                  {viewMode === 'resonance' && 'Navigating node tension across 93 points of interest.'}
                  {viewMode === 'circular-limit' && 'Exploring the analytic continuation of natural numbers toward -1/12.'}
                  {viewMode === 'city-press' && 'Pressing the Riemann Hypothesis into architectural form. Stability is the proof.'}
                  {viewMode === 'stabilisated-cone' && 'Stabilisating rotation along Root 42 radiation arms. Vitrifying the shell.'}
                  {viewMode === 'nautilus-prime' && 'Navigating the precipitates of silt and carbon. Perfectly crystallised time.'}
                </p>
              </div>
              <div className="text-right">
                <span className="text-[10px] text-zinc-500 font-mono uppercase block">
                  {viewMode === 'city-press' ? 'Press Depth' : viewMode === 'stabilisated-cone' ? 'Vitrification' : 'Limit Constant'}
                </span>
                <span className="text-2xl font-mono text-emerald-400 tracking-tighter">
                  {viewMode === 'resonance' ? t.toFixed(4) : viewMode === 'circular-limit' ? ZETA_NEG_ONE.toFixed(4) : viewMode === 'city-press' ? pressDepth.toFixed(2) : vitrification.toFixed(2)}
                </span>
              </div>
            </div>

            {/* Visualization Area */}
            <div className="flex-1 relative flex items-center justify-center">
              <AnimatePresence mode="wait">
                {viewMode === 'resonance' && (
                  <motion.div
                    key="resonance"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.1 }}
                    className="w-full h-full flex items-center justify-center"
                  >
                    <svg viewBox="0 0 400 400" className="w-full h-full max-w-[500px]">
                      <g transform={`translate(200, 200) scale(${zoomLevel}) translate(-200, -200)`}>
                        <circle cx="200" cy="200" r="180" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="1" strokeDasharray="4 4" />
                        {nodeList.map((node, i) => {
                          const nextNode = nodeList[(i + 1) % nodeList.length];
                          const x1 = 200 + Math.cos(node.angle) * (150 + node.tension * 20);
                          const y1 = 200 + Math.sin(node.angle) * (150 + node.tension * 20);
                          const x2 = 200 + Math.cos(nextNode.angle) * (150 + nextNode.tension * 20);
                          const y2 = 200 + Math.sin(nextNode.angle) * (150 + nextNode.tension * 20);
                          return (
                            <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={node.prime ? 'rgba(16,185,129,0.2)' : 'rgba(255,255,255,0.03)'} strokeWidth={node.prime ? 1.5 : 0.5} />
                          );
                        })}
                        {nodeList.map((node) => (
                          <circle key={node.id} cx={200 + Math.cos(node.angle) * (150 + node.tension * 20)} cy={200 + Math.sin(node.angle) * (150 + node.tension * 20)} r={node.prime ? 4 : 2} fill={node.prime ? '#10b981' : '#3f3f46'} onMouseEnter={() => setActiveNode(node.id)} onMouseLeave={() => setActiveNode(null)} />
                        ))}
                      </g>
                    </svg>
                  </motion.div>
                )}

                {viewMode === 'circular-limit' && (
                  <motion.div
                    key="circular-limit"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.1 }}
                    className="w-full h-full flex items-center justify-center"
                  >
                    <svg viewBox="0 0 400 400" className="w-full h-full max-w-[500px]">
                      <g transform={`translate(200, 200) scale(${zoomLevel}) translate(-200, -200)`}>
                        <circle cx="200" cy="200" r="4" fill="#10b981" className="animate-pulse" />
                        {Array.from({ length: 100 }).map((_, i) => {
                          const angle = i * 0.5 + time * (1 + rollingFrequency);
                          const radius = i * 1.8;
                          const x = 200 + Math.cos(angle) * radius;
                          const y = 200 + Math.sin(angle) * radius;
                          return <circle key={i} cx={x} cy={y} r="1" fill={`rgba(16,185,129, ${1 - i / 100})`} />;
                        })}
                      </g>
                    </svg>
                  </motion.div>
                )}

                {viewMode === 'city-press' && (
                  <motion.div
                    key="city-press"
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -50 }}
                    className="w-full h-full flex items-center justify-center p-12"
                  >
                    <svg viewBox="0 0 600 600" className="w-full h-full">
                      <g transform={`translate(300, 150) rotate(45) scale(${zoomLevel}, ${0.5 * zoomLevel})`}>
                        {/* Grid Floor */}
                        <rect x="-250" y="-250" width="500" height="500" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.05)" />

                        {/* Buildings */}
                        {nodeList.map((node) => {
                          const size = 25;
                          const spacing = 40;
                          const x = (node.id % 10 - 5) * spacing;
                          const y = (Math.floor(node.id / 10) - 5) * spacing;
                          const h = node.height;

                          return (
                            <g key={node.id} transform={`translate(${x}, ${y})`}>
                              {/* Base */}
                              <rect x={-size / 2} y={-size / 2} width={size} height={size} fill={node.prime ? 'rgba(16,185,129,0.2)' : 'rgba(255,255,255,0.05)'} />

                              {/* Satellites (Civilization) */}
                              {node.satellites.map(sat => (
                                <g key={sat.id} transform={`translate(${Math.cos(sat.angle) * sat.dist}, ${Math.sin(sat.angle) * sat.dist})`}>
                                  <rect x={-size / 8} y={-size / 8 - sat.h} width={size / 4} height={sat.h} fill="rgba(16,185,129,0.3)" />
                                  <rect x={-size / 8} y={-size / 8 - sat.h} width={size / 4} height={size / 4} fill="#10b981" />
                                </g>
                              ))}

                              {/* Vertical "Press" extrusion (simulated 3D) */}
                              <motion.g
                                initial={{ opacity: 0, scaleZ: 0 }}
                                animate={{ opacity: 1, scaleZ: 1 }}
                                transition={{ delay: node.id * 0.005 }}
                              >
                                {/* Left Side */}
                                <path
                                  d={`M ${-size / 2} ${-size / 2} L ${-size / 2} ${-size / 2} L ${-size / 2} ${-size / 2 - h} L ${-size / 2} ${-size / 2 - h} Z`}
                                  fill={node.prime ? '#064e3b' : '#18181b'}
                                  transform="rotate(-45) scale(1.414, 1)"
                                />

                                {/* Tiers for Superprimes */}
                                {node.superPrime && (
                                  <g transform={`translate(0, -${h * 0.5})`}>
                                    <rect x={-size / 1.5} y={-size / 1.5} width={size * 1.33} height={size * 1.33} fill="rgba(52, 211, 153, 0.1)" stroke="rgba(52, 211, 153, 0.3)" />
                                  </g>
                                )}

                                {/* Top Face */}
                                <rect
                                  x={-size / 2} y={-size / 2 - h}
                                  width={size} height={size}
                                  fill={node.superPrime ? '#34d399' : node.prime ? '#10b981' : node.id === 42 ? '#f43f5e' : '#3f3f46'}
                                  stroke="rgba(0,0,0,0.3)"
                                  onMouseEnter={() => setActiveNode(node.id)}
                                  onMouseLeave={() => setActiveNode(null)}
                                  className="cursor-pointer transition-colors"
                                />
                                {node.prime && (
                                  <rect
                                    x={-size / 4} y={-size / 4 - h}
                                    width={size / 2} height={size / 2}
                                    fill="rgba(255,255,255,0.2)"
                                  />
                                )}

                                {/* Civilization Lights & Glistening People */}
                                {node.prime && civDensity > 0.3 && (
                                  <g>
                                    <circle cx={0} cy={-h - size / 4} r={1.5} fill="#fff" className="animate-pulse" />
                                    {/* Glistening People (visible at high rolling frequency) */}
                                    {rollingFrequency > 0.5 && Array.from({ length: Math.floor(civDensity * 10) }).map((_, pIdx) => (
                                      <motion.circle
                                        key={`person-${pIdx}`}
                                        cx={(Math.random() - 0.5) * size * 0.8}
                                        cy={-h - size / 2 + (Math.random() - 0.5) * size * 0.8}
                                        r={0.5}
                                        fill="#fbbf24"
                                        animate={{
                                          opacity: [0, 1, 0],
                                          x: [(Math.random() - 0.5) * size, (Math.random() - 0.5) * size]
                                        }}
                                        transition={{
                                          duration: 1 / rollingFrequency,
                                          repeat: Infinity,
                                          delay: Math.random()
                                        }}
                                      />
                                    ))}
                                  </g>
                                )}
                              </motion.g>
                            </g>
                          );
                        })}
                      </g>
                    </svg>
                  </motion.div>
                )}

                {viewMode === 'stabilisated-cone' && (
                  <motion.div
                    key="stabilisated-cone"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 1.2 }}
                    className="w-full h-full flex items-center justify-center"
                  >
                    <svg viewBox="-200 -200 400 400" className="w-full h-full max-w-[500px]">
                      <g transform={`scale(${zoomLevel})`}>
                        {/* Vitrification Shell */}
                        <circle cx="0" cy="0" r="180" fill="none" stroke="rgba(16,185,129,0.05)" strokeWidth={vitrification * 20} strokeDasharray="2 10" className="animate-spin-slow" />

                        {/* Diamond Dust Trails — Ketheric Wake */}
                        {dustTrails.map((dust, i) => (
                          <circle
                            key={`dust-${i}`}
                            cx={dust.x}
                            cy={dust.y}
                            r={0.5 + (1 - dust.age / 120) * 1.5}
                            fill={`rgba(200, 240, 255, ${(1 - dust.age / 120) * vitrification * 0.6})`}
                            stroke={`rgba(16, 185, 129, ${(1 - dust.age / 120) * vitrification * 0.3})`}
                            strokeWidth="0.3"
                          />
                        ))}

                        {/* Graphene Sheet Arcs — φ-spaced spiral vitrification lines */}
                        {vitrification > 0.3 && Array.from({ length: Math.floor(vitrification * 12) }, (_, i) => {
                          const r1 = 20 + i * PHI * 12;
                          const r2 = r1 + 8;
                          const startAngle = i * PHI + time * 0.02;
                          const arcLength = Math.PI * (0.5 + vitrification * 0.5);
                          return (
                            <path
                              key={`graphene-${i}`}
                              d={`M ${Math.cos(startAngle) * r1} ${Math.sin(startAngle) * r1} A ${r1} ${r1} 0 0 1 ${Math.cos(startAngle + arcLength) * r2} ${Math.sin(startAngle + arcLength) * r2}`}
                              fill="none"
                              stroke={`rgba(160, 220, 255, ${vitrification * 0.15})`}
                              strokeWidth="0.5"
                              strokeLinecap="round"
                            />
                          );
                        })}

                        {/* Radiation Arms (Root 42) */}
                        {[0, 1, 2, 3, 4, 5].map(i => (
                          <line
                            key={i}
                            x1="0" y1="0"
                            x2={Math.cos(i * Math.PI / 3) * 200}
                            y2={Math.sin(i * Math.PI / 3) * 200}
                            stroke="rgba(244,63,94,0.1)"
                            strokeWidth="1"
                            strokeDasharray="5 5"
                          />
                        ))}

                        {/* Cone Nodes */}
                        {nodeList.map((node) => (
                          <g key={node.id} transform={`translate(${node.coneX}, ${node.coneY})`}>
                            {/* Connection to center (Stabilisation) */}
                            <line x1="0" y1="0" x2={-node.coneX} y2={-node.coneY} stroke={node.isRadiationArm ? 'rgba(244,63,94,0.1)' : 'rgba(255,255,255,0.02)'} strokeWidth="0.5" />

                            <circle
                              r={node.prime ? 3 : 1.5}
                              fill={node.id === 42 ? '#f43f5e' : node.isRadiationArm ? '#fb7185' : node.prime ? '#10b981' : '#3f3f46'}
                              className={node.isRadiationArm ? 'animate-pulse' : ''}
                              onMouseEnter={() => setActiveNode(node.id)}
                              onMouseLeave={() => setActiveNode(null)}
                            />

                            {node.superPrime && (
                              <circle r="6" fill="none" stroke="#34d399" strokeWidth="0.5" strokeDasharray="2 2" className="animate-spin-slow" />
                            )}
                          </g>
                        ))}
                      </g>
                    </svg>
                  </motion.div>
                )}

                {viewMode === 'nautilus-prime' && (
                  <motion.div
                    key="nautilus-prime"
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 50 }}
                    className="w-full h-full flex items-center justify-center p-8 relative overflow-hidden"
                    style={{ backgroundColor: '#f4ecd8' }} // Parchment background
                  >
                    {/* Vintage Vignette Overlay */}
                    <div className="absolute inset-0 pointer-events-none" style={{
                      background: 'radial-gradient(circle, transparent 50%, rgba(139, 115, 85, 0.4) 150%)'
                    }} />

                    <svg viewBox="-200 -200 400 650" className="w-full h-full max-w-[550px]">
                      <defs>
                        <linearGradient id="silt-layer" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="rgba(62, 39, 35, 0.8)" />
                          <stop offset="50%" stopColor="rgba(93, 64, 55, 0.6)" />
                          <stop offset="100%" stopColor="rgba(62, 39, 35, 0.8)" />
                        </linearGradient>
                        <pattern id="stippled-pattern" width="4" height="4" patternUnits="userSpaceOnUse">
                          <circle cx="1" cy="1" r="0.5" fill="rgba(62, 39, 35, 0.3)" />
                          <circle cx="3" cy="3" r="0.5" fill="rgba(62, 39, 35, 0.2)" />
                        </pattern>
                      </defs>

                      {/* Technical Geometric Blueprint Framing */}
                      <g className="blueprint-framing" stroke="rgba(62, 39, 35, 0.3)" strokeWidth="0.5" fill="none">
                        {/* Golden Ratio Grid */}
                        <rect x="-180" y="-150" width="360" height="580" />
                        <line x1="-180" y1="0" x2="180" y2="0" strokeDasharray="2 4" />
                        <line x1="0" y1="-150" x2="0" y2="430" strokeDasharray="2 4" />
                        <circle cx="0" cy="140" r="140" strokeDasharray="1 3" />
                        <circle cx="0" cy="140" r="226" strokeDasharray="1 3" />

                        {/* Fibonacci Spiral Ornament */}
                        <path d="M 0 140 A 140 140 0 0 1 140 0 A 226 226 0 0 1 -86 226" stroke="rgba(62, 39, 35, 0.4)" strokeWidth="1" />

                        {/* Proportional Labels */}
                        <text x="-170" y="-135" fill="rgba(62, 39, 35, 0.6)" fontSize="8" className="font-serif tracking-widest uppercase">Sisyphus as the Cone Shell: Geometric Proportion</text>
                        <text x="170" y="420" textAnchor="end" fill="rgba(62, 39, 35, 0.5)" fontSize="6" className="font-serif">Araujo Construction - Fig. 1</text>
                      </g>

                      {/* A-Frame Stability Incline Container */}
                      <g transform={`scale(${zoomLevel}) rotate(-${aFrameStability}) translate(0, 50)`}>
                        {/* The Slope Line */}
                        <line x1="-300" y1="350" x2="300" y2="350" stroke="rgba(62, 39, 35, 0.4)" strokeWidth="1" />
                        <text x="-150" y="340" fill="rgba(62, 39, 35, 0.6)" fontSize="8" className="font-serif italic">30° Incline</text>

                        {/* Gravity/Ground G Baseline (Horizontal relative to viewport) */}
                        <g transform={`rotate(${aFrameStability})`}>
                          <line x1="-400" y1="200" x2="400" y2="200" stroke="rgba(62, 39, 35, 0.3)" strokeWidth="1" strokeDasharray="4 4" />
                          <text x="150" y="215" fill="rgba(62, 39, 35, 0.5)" fontSize="8" className="font-serif uppercase tracking-widest">Gravity / Ground G</text>
                        </g>

                        {/* Side View Vitrified Shell (Silt & Carbon Layers) */}
                        {/* Rotated -90 to lay horizontally, pointing left (downhill) and expanding right (uphill) */}
                        <g transform="translate(140, 290) rotate(-90)">
                          {nodeList.map((node, i) => {
                            const z = node.coneZ;
                            // Scale rx to max 60 to match the rock (Sphaera Aeria)
                            const rx = (Math.abs(node.coneX) / 200) * 30 + (z / 200) * 30;
                            const ry = (z / 200) * 20;
                            const op = 0.05 + (node.prime ? 0.2 : 0);
                            return (
                              <g key={i}>
                                <ellipse
                                  cx="0"
                                  cy={z}
                                  rx={rx}
                                  ry={ry}
                                  fill="none"
                                  stroke="url(#silt-layer)"
                                  strokeWidth={vitrification * 4}
                                  opacity={0.3}
                                />
                                <ellipse
                                  cx="0"
                                  cy={z}
                                  rx={rx * 0.8}
                                  ry={ry * 0.8}
                                  fill="none"
                                  stroke={node.isRadiationArm ? "rgba(194, 65, 12, 0.4)" : "rgba(15, 118, 110, 0.3)"}
                                  strokeWidth={vitrification * 2}
                                  opacity={op}
                                />
                              </g>
                            );
                          })}

                          {/* Tree Roots: Crystallised Time Navigation */}
                          <g className="tree-roots" opacity="0.3">
                            {nodeList.filter(n => n.prime || n.id % 42 === 0).map((node, i) => {
                              const z = node.coneZ;
                              const rx = (Math.abs(node.coneX) / 200) * 30 + (z / 200) * 30;
                              const rootX = node.coneX > 0 ? rx : -rx;
                              return (
                                <motion.path
                                  key={`root-${node.id}`}
                                  d={`M 0 0 Q ${rootX * 1.5} ${z / 2} ${rootX} ${z}`}
                                  stroke={node.prime ? "#0f766e" : "rgba(194, 65, 12, 0.4)"}
                                  strokeWidth="0.5"
                                  fill="none"
                                  initial={{ pathLength: 0 }}
                                  animate={{ pathLength: 1 }}
                                  transition={{ duration: 3, delay: i * 0.02 }}
                                />
                              );
                            })}
                          </g>

                          {/* Trifold Time Triangle (Now relative to the cone's base) */}
                          <g transform="translate(0, 200)" className="trifold-triangle">
                            {(() => {
                              const p1 = { x: 0, y: -40 };
                              const p2 = { x: -35, y: 20 };
                              const p3 = { x: 35, y: 20 };
                              const points = `${p1.x},${p1.y} ${p2.x},${p2.y} ${p3.x},${p3.y}`;
                              return (
                                <motion.polygon
                                  points={points}
                                  fill="none"
                                  stroke="rgba(62, 39, 35, 0.6)"
                                  strokeWidth="1"
                                  strokeDasharray="4 2"
                                  animate={{
                                    opacity: [0.3, 0.7, 0.3],
                                    rotate: [0, 360]
                                  }}
                                  transition={{
                                    opacity: { duration: 4, repeat: Infinity },
                                    rotate: { duration: 20, repeat: Infinity, ease: "linear" }
                                  }}
                                />
                              );
                            })()}
                          </g>
                        </g>

                        {/* Sphaera Aeria (Air-filled Exercise Ball) - Positioned at the open end of the cone */}
                        <motion.g transform="translate(340, 290)">
                          <motion.circle
                            r="60"
                            fill="rgba(244, 236, 216, 0.5)"
                            stroke="rgba(62, 39, 35, 0.6)"
                            strokeWidth="1.5"
                            animate={{ scale: [1, 1.02, 1], rotate: [0, 360] }}
                            transition={{ duration: 8 / (1 + rollingFrequency), repeat: Infinity, ease: "linear" }}
                          />
                          {/* Inner air reflections */}
                          <motion.g
                            animate={{ rotate: [0, 360] }}
                            transition={{ duration: 8 / (1 + rollingFrequency), repeat: Infinity, ease: "linear" }}
                          >
                            <path d="M -40 -20 Q -20 -40 0 -45" fill="none" stroke="rgba(62, 39, 35, 0.3)" strokeWidth="1.5" strokeLinecap="round" />
                            <path d="M 20 30 Q 40 10 45 0" fill="none" stroke="rgba(62, 39, 35, 0.2)" strokeWidth="1" strokeLinecap="round" />
                            <circle r="4" fill="rgba(62, 39, 35, 0.4)" className="animate-pulse" />
                          </motion.g>
                          <text y="-70" textAnchor="middle" className="text-[8px] fill-[rgba(62,39,35,0.7)] font-serif uppercase tracking-widest">Sphaera Aeria</text>
                        </motion.g>

                        {/* A-Frame Stability Schematic (Triangle Pose) - Positioned between cone tip and rock */}
                        <g transform={`translate(${Math.sin(time) * 10 + 260}, 310)`}>
                          {/* Force Vectors */}
                          <line x1="0" y1="0" x2="80" y2="-40" stroke="rgba(62, 39, 35, 0.4)" strokeWidth="1" strokeDasharray="2 2" />
                          <line x1="0" y1="0" x2="-40" y2="40" stroke="rgba(62, 39, 35, 0.4)" strokeWidth="1" strokeDasharray="2 2" />

                          {/* A-Frame Lines */}
                          <polygon points="0,-60 -40,40 60,40" fill="rgba(62, 39, 35, 0.05)" stroke="rgba(62, 39, 35, 0.3)" strokeWidth="1" />
                          <circle cx="0" cy="-60" r="3" fill="rgba(62, 39, 35, 0.6)" />
                          <circle cx="-40" cy="40" r="3" fill="rgba(62, 39, 35, 0.6)" />
                          <circle cx="60" cy="40" r="3" fill="rgba(62, 39, 35, 0.6)" />

                          <text x="0" y="-75" textAnchor="middle" className="text-[8px] fill-[rgba(62,39,35,0.7)] font-serif uppercase tracking-widest">A-Frame Core</text>

                          {/* The Creature (Soft Navigator - doing the pose) */}
                          {/* Rotated to face uphill and align with the A-Frame */}
                          <g transform="rotate(30) scale(0.8)">
                            <SoftCreature mobility={softMobility} time={time} sync={bioSync} color="rgba(62, 39, 35, 0.7)" />
                          </g>
                        </g>
                        {/* Navigational Anchor (Moved to cone tip) */}
                        <motion.circle
                          cx="140" cy="290" r="5"
                          fill="#fb7185"
                          animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
                          transition={{ duration: 2, repeat: Infinity }}
                        />
                      </g>
                    </svg>
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
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Structure ID</span>
                      <p className="text-xl font-bold tracking-tighter">n = {activeNode}</p>
                    </div>
                    <div className="text-center">
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Integrity</span>
                      <p className={`text-sm font-bold uppercase ${isSuperPrime(activeNode) ? 'text-emerald-400' : isPrime(activeNode) ? 'text-emerald-400/60' : 'text-zinc-500'}`}>
                        {isSuperPrime(activeNode) ? 'MONOLITH' : isPrime(activeNode) ? 'STABLE SPIRE' : 'ECHO BLOCK'}
                      </p>
                    </div>
                    <div className="text-center">
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Möbius μ(n)</span>
                      <p className={`text-sm font-bold ${nodeList.find(n => n.id === activeNode)?.mobius === 0 ? 'text-zinc-500' : 'text-blue-400'}`}>
                        {nodeList.find(n => n.id === activeNode)?.mobius}
                      </p>
                    </div>
                    <div className="text-center">
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Li(n) Error</span>
                      <p className="text-sm font-bold text-rose-400">
                        {nodeList.find(n => n.id === activeNode)?.liError.toFixed(2)}
                      </p>
                    </div>
                    <div className="text-center">
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Von Mangoldt Λ(n)</span>
                      <p className="text-sm font-bold text-emerald-400">
                        {nodeList.find(n => n.id === activeNode)?.vonMangoldt.toFixed(2)}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] text-zinc-500 font-mono uppercase">Height (Resonance)</span>
                      <p className="text-xl font-mono text-blue-400">{(nodeList.find(n => n.id === activeNode)?.height || 0).toFixed(1)}m</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Resonance Controls */}
          {viewMode === 'resonance' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6 grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-emerald-400" />
                  <h3 className="text-sm font-bold uppercase tracking-widest">Resonance Tuning</h3>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-[10px] text-zinc-500 uppercase">Tension Scalar (t)</label>
                    <span className="text-xs font-mono text-emerald-400">{t.toFixed(4)}</span>
                  </div>
                  <input
                    type="range" min="0" max="50" step="0.0001" value={t}
                    onChange={(e) => setT(parseFloat(e.target.value))}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-[10px] text-zinc-500 uppercase">Zoom Level</label>
                    <span className="text-xs font-mono text-emerald-400">{zoomLevel.toFixed(2)}x</span>
                  </div>
                  <input
                    type="range" min="0.5" max="5" step="0.1" value={zoomLevel}
                    onChange={(e) => setZoomLevel(parseFloat(e.target.value))}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                </div>
              </div>
              <div className="p-4 bg-black/40 rounded-2xl border border-white/5 flex flex-col justify-center">
                <p className="text-[11px] text-zinc-400 leading-relaxed italic">
                  "The full work is revealed at any level of zoom - light lines, heavy lines and arcs as we zoom in keep revealing higher and higher levels of the root 42 unfolding flower."
                </p>
              </div>
            </motion.div>
          )}

          {/* City Press Controls */}
          {viewMode === 'city-press' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6 grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <Printer className="w-4 h-4 text-emerald-400" />
                  <h3 className="text-sm font-bold uppercase tracking-widest">Press Configuration</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-[10px] text-zinc-500 uppercase">Base Modulo</label>
                      <span className="text-xs font-mono text-emerald-400">{cityBase}</span>
                    </div>
                    <input
                      type="range" min="2" max="48" step="1" value={cityBase}
                      onChange={(e) => setCityBase(parseInt(e.target.value))}
                      className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                    />
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-[10px] text-zinc-500 uppercase">Press Depth</label>
                      <span className="text-xs font-mono text-emerald-400">{pressDepth.toFixed(2)}</span>
                    </div>
                    <input
                      type="range" min="0.1" max="2.0" step="0.01" value={pressDepth}
                      onChange={(e) => setPressDepth(parseFloat(e.target.value))}
                      className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-[10px] text-zinc-500 uppercase block mb-2">Platonic Ratio</label>
                    <select
                      value={platonicRatio}
                      onChange={(e) => setPlatonicRatio(e.target.value as any)}
                      className="bg-black/40 border border-white/10 rounded-lg px-2 py-1 text-[10px] font-mono text-emerald-400 w-full focus:outline-none"
                    >
                      <option value="1:1">1:1 (Unison)</option>
                      <option value="2:3">2:3 (Fifth)</option>
                      <option value="3:4">3:4 (Fourth)</option>
                      <option value="4:5">4:5 (Third)</option>
                    </select>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-[10px] text-zinc-500 uppercase">Civ Density</label>
                      <span className="text-xs font-mono text-emerald-400">{(civDensity * 100).toFixed(0)}%</span>
                    </div>
                    <input
                      type="range" min="0" max="1" step="0.1" value={civDensity}
                      onChange={(e) => setCivDensity(parseFloat(e.target.value))}
                      className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                    />
                  </div>
                </div>
              </div>
              <div className="p-4 bg-black/40 rounded-2xl border border-white/5 flex flex-col justify-center">
                <p className="text-[11px] text-zinc-400 leading-relaxed italic">
                  "If Plato is right, certain ratios generate civilizations."
                  The Platonic Ratio modulates the harmonic frequency of the press.
                  High Civ Density triggers satellite structures around Stable Spires, simulating the growth of a mathematical society.
                </p>
              </div>
            </motion.div>
          )}

          {/* Stabilisated Cone Controls */}
          {viewMode === 'stabilisated-cone' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6 grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <Layers className="w-4 h-4 text-rose-400" />
                  <h3 className="text-sm font-bold uppercase tracking-widest">Cone Stabilisation</h3>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-[10px] text-zinc-500 uppercase">Vitrification Factor</label>
                    <span className="text-xs font-mono text-rose-400">{vitrification.toFixed(2)}</span>
                  </div>
                  <input
                    type="range" min="0" max="1" step="0.01" value={vitrification}
                    onChange={(e) => setVitrification(parseFloat(e.target.value))}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-rose-500"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-[10px] text-zinc-500 uppercase">Rolling Frequency (Sun)</label>
                    <span className="text-xs font-mono text-rose-400">{rollingFrequency.toFixed(2)}</span>
                  </div>
                  <input
                    type="range" min="0" max="5" step="0.1" value={rollingFrequency}
                    onChange={(e) => setRollingFrequency(parseFloat(e.target.value))}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-rose-500"
                  />
                </div>
                <div className="p-3 bg-rose-500/5 border border-rose-500/20 rounded-xl">
                  <span className="text-[8px] text-rose-400 uppercase font-bold block mb-1">Active Axis</span>
                  <p className="text-[10px] text-zinc-400 font-mono">ROOT_42_RADIATION_ARM_V2</p>
                </div>
              </div>
              <div className="p-4 bg-black/40 rounded-2xl border border-white/5 flex flex-col justify-center">
                <p className="text-[11px] text-zinc-400 leading-relaxed italic">
                  "Vitrify the shell along a second root 42 axis."
                  The conical wrap to n*mod24 locks the rotation, preventing stochastic drift.
                  Radiation arms (Rose) provide the structural tension required to vitrify the mathematical shell.
                </p>
              </div>
            </motion.div>
          )}

          {/* Nautilus Prime Controls */}
          {viewMode === 'nautilus-prime' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6 grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <Waves className="w-4 h-4 text-emerald-400" />
                  <h3 className="text-sm font-bold uppercase tracking-widest">Biological Resonance</h3>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-[10px] text-zinc-500 uppercase">Soft Mobility</label>
                    <span className="text-xs font-mono text-emerald-400">{(softMobility * 100).toFixed(0)}%</span>
                  </div>
                  <input
                    type="range" min="0.1" max="1.0" step="0.01" value={softMobility}
                    onChange={(e) => setSoftMobility(parseFloat(e.target.value))}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-[10px] text-zinc-500 uppercase">Limit Constant</label>
                    <span className="text-xs font-mono text-emerald-400">{bioSync.toFixed(2)}</span>
                  </div>
                  <input
                    type="range" min="0" max="1" step="0.01" value={bioSync}
                    onChange={(e) => setBioSync(parseFloat(e.target.value))}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-[10px] text-zinc-500 uppercase">A-Frame Stability (Slope)</label>
                    <span className="text-xs font-mono text-emerald-400">{aFrameStability.toFixed(1)}°</span>
                  </div>
                  <input
                    type="range" min="10" max="60" step="1" value={aFrameStability}
                    onChange={(e) => setAFrameStability(parseFloat(e.target.value))}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                </div>
                <div className="p-3 bg-emerald-500/5 border border-emerald-500/20 rounded-xl">
                  <span className="text-[8px] text-emerald-400 uppercase font-bold block mb-1">Creature State</span>
                  <p className="text-[10px] text-zinc-400 font-mono">NAUTILUS_PRIME_ACTIVE</p>
                </div>
              </div>
              <div className="p-4 bg-black/40 rounded-2xl border border-white/5 flex flex-col justify-center">
                <p className="text-[11px] text-zinc-400 leading-relaxed italic">
                  "In a way we are only pressing silt, calcium and carbon - but the time is already woven in by nature."
                  Trace elements and radioactive decay provide the perfect luminescence crystallised
                  as sculptures by living molluscs. The past has been precipitated into the
                  hardcard of form. (4 e^2vr?)
                </p>
              </div>
            </motion.div>
          )}

          {/* Superprime Scanner (Shared) */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold uppercase tracking-widest">Structure Scanner</h3>
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
            <div className="mb-6">
              <input
                type="range" min="1" max="1000" step="1" value={scannerNum}
                onChange={(e) => setScannerNum(parseInt(e.target.value))}
                className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
              />
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Prime</span>
                <span className={`text-xs font-bold ${scannerResult.prime ? 'text-emerald-400' : 'text-zinc-700'}`}>{scannerResult.prime ? 'DETECTED' : 'NEGATIVE'}</span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Superprime</span>
                <span className={`text-xs font-bold ${scannerResult.superPrime ? 'text-emerald-400' : 'text-zinc-700'}`}>{scannerResult.superPrime ? 'DETECTED' : 'NEGATIVE'}</span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Mod 24 Spoke</span>
                <span className={`text-xs font-bold ${scannerResult.isSpoke ? 'text-blue-400' : 'text-zinc-700'}`}>{scannerResult.isSpoke ? 'ALIGNED' : 'DRIFTED'}</span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Möbius μ(n)</span>
                <span className={`text-xs font-bold ${scannerResult.mobius === 0 ? 'text-zinc-500' : 'text-blue-400'}`}>{scannerResult.mobius}</span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Local Gap</span>
                <span className={`text-xs font-bold text-amber-400`}>{scannerResult.gap} U</span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Von Mangoldt Λ(n)</span>
                <span className={`text-xs font-bold text-emerald-400`}>{scannerResult.vonMangoldt.toFixed(2)}</span>
              </div>
              <div className="p-4 bg-black/20 rounded-2xl border border-white/5 flex flex-col items-center">
                <span className="text-[8px] text-zinc-500 uppercase mb-1">Harmonic Anchor</span>
                <span className={`text-xs font-bold ${scannerResult.isHarmonicAnchor ? 'text-rose-400' : 'text-zinc-700'}`}>{scannerResult.isHarmonicAnchor ? '42: FOUND' : 'NONE'}</span>
              </div>
            </div>
          </div>
        </section>

        {/* Right Column: Controls & Audit */}
        <section className="lg:col-span-5 space-y-6">

          {/* Generative Architecture Audit */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6">
            <h3 className="text-sm font-bold uppercase tracking-widest mb-6 flex items-center gap-2">
              <Building2 className="w-4 h-4 text-emerald-400" />
              Generative Audit
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Base Seed</span>
                <span className="text-xs font-mono text-zinc-300">Mod-{cityBase}</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Structural Logic</span>
                <span className="text-xs font-mono text-emerald-400">Prime-Extrusion</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Stability Index</span>
                <span className="text-xs font-mono text-emerald-400">{(nodeList.filter(n => n.prime).length / nodeList.length * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Platonic Harmony</span>
                <span className="text-xs font-mono text-emerald-400">{platonicRatio}</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Civ Population</span>
                <span className="text-xs font-mono text-emerald-400">{nodeList.reduce((acc, n) => acc + n.satellites.length, 0)} Units</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Stabilisation Axis</span>
                <span className="text-xs font-mono text-rose-400">Root 42 (Locked)</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Vitrification State</span>
                <span className="text-xs font-mono text-rose-400">{vitrification > 0.8 ? 'VITRIFIED' : 'CRYSTALLIZING'}</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Biological Sync</span>
                <span className="text-xs font-mono text-emerald-400">{(softMobility * vitrification * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Tentacle Count</span>
                <span className="text-xs font-mono text-emerald-400">{Math.floor(softMobility * 12) + 4}</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Deep Time Accumulation</span>
                <span className="text-xs font-mono text-amber-400">{(time * 1000).toFixed(0)} Eons</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">A-Frame Stability</span>
                <span className="text-xs font-mono text-emerald-400">{aFrameStability.toFixed(2)}°</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Effort Scalar</span>
                <span className="text-xs font-mono text-amber-400">{(parseFloat(geometricEntropy) * 100).toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Eternal Constant</span>
                <span className="text-xs font-mono text-amber-400">{(4 * Math.exp(2 * Math.PI)).toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Crystallised Time</span>
                <span className="text-xs font-mono text-amber-400">3-FOLD_SYNC</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Root Navigation</span>
                <span className="text-xs font-mono text-emerald-400">ACTIVE</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Material Composition</span>
                <span className="text-xs font-mono text-zinc-400">SILT / CA / C</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Trace Luminescence</span>
                <span className="text-xs font-mono text-emerald-400">CRYSTALLISED</span>
              </div>
              <div className="flex justify-between items-end border-b border-white/5 pb-2">
                <span className="text-[10px] text-zinc-500 uppercase">Radioactive Decay</span>
                <span className="text-xs font-mono text-amber-400">DEEP_TIME_TRACE</span>
              </div>

              {/* Geofont 13 Phase Matrix */}
              <div className="mt-4 p-4 bg-cyan-500/5 border border-cyan-500/20 rounded-2xl">
                <h4 className="text-[8px] text-cyan-400 uppercase font-bold tracking-widest mb-3">Geofont 13 Phase Matrix</h4>
                <div className="grid grid-cols-3 gap-2 mb-3">
                  <div className="text-center">
                    <span className="text-[8px] text-zinc-500 uppercase block">V₉₃ Nodes</span>
                    <span className="text-xs font-mono text-cyan-400">{V_93_CAPACITY}</span>
                  </div>
                  <div className="text-center">
                    <span className="text-[8px] text-zinc-500 uppercase block">√42 Anchor</span>
                    <span className="text-xs font-mono text-rose-400">{ROOT_42.toFixed(4)}</span>
                  </div>
                  <div className="text-center">
                    <span className="text-[8px] text-zinc-500 uppercase block">Hades Gap</span>
                    <span className="text-xs font-mono text-amber-400">{(HADES_GAP * 100).toFixed(2)}%</span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-[8px] text-zinc-500 uppercase">Vitrification Criterion</span>
                  <span className={`text-[10px] font-mono font-bold ${vitrification > 0.8 ? 'text-cyan-400' : vitrification > 0.4 ? 'text-amber-400' : 'text-zinc-500'}`}>
                    {vitrification > 0.8 ? 'DIAMOND SHELL' : vitrification > 0.4 ? 'CRYSTALLIZING' : 'ARAGONITE'}
                  </span>
                </div>
                <div className="flex justify-between items-center mt-1">
                  <span className="text-[8px] text-zinc-500 uppercase">Diamond Dust Trails</span>
                  <span className="text-[10px] font-mono text-cyan-400">{dustTrails.length} ACTIVE</span>
                </div>
              </div>

              <div className="mt-4 p-4 bg-black/40 rounded-2xl border border-white/5">
                <p className="text-[11px] text-zinc-400 leading-relaxed">
                  The snail eats its own diamond dust to vitrify the shell to pure diamond —
                  perfectly scrolled graphene sheets spiralled into pandimensional hyperdiamond.
                  The 42 Anchor (Rose) acts as the central symmetry point.
                </p>
              </div>
            </div>
          </div>

          {/* Superprime Distribution */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6">
            <h3 className="text-sm font-bold uppercase tracking-widest mb-6 flex items-center gap-2">
              <Dna className="w-4 h-4 text-emerald-400" />
              Superprime Monoliths
            </h3>
            <div className="flex flex-wrap gap-2">
              {[3, 5, 11, 17, 31, 41, 59, 67, 83].map((sp) => (
                <div key={sp} className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-[10px] font-mono text-emerald-400">
                  {sp}
                </div>
              ))}
            </div>
            <p className="mt-4 text-[11px] text-zinc-500 italic leading-relaxed">
              In the City Press, Superprimes are "Monoliths"—structures with the highest integrity.
              They are the "proof" that the prime sieve is not random, but indexed by its own internal logic.
            </p>
          </div>

          {/* Navigational Logbook */}
          <div className="bg-zinc-900/50 border border-white/5 rounded-3xl p-6 overflow-hidden relative">
            <h3 className="text-sm font-bold uppercase tracking-widest mb-4 flex items-center gap-2">
              <Compass className="w-4 h-4 text-zinc-400" />
              Navigational Logbook
            </h3>
            <div className="space-y-3 font-mono text-[10px]">
              <div className="flex gap-3 text-zinc-500">
                <span className="text-emerald-400">[OK]</span>
                <span>Navigation locked along Root 42 radiation arms.</span>
              </div>
              <div className="flex gap-3 text-emerald-400">
                <span className="text-emerald-400">[OK]</span>
                <span>Nautilus Navigator: ACTIVE.</span>
              </div>
              <div className="flex gap-3 text-rose-400">
                <span className="animate-pulse">[WARN]</span>
                <span>Eternal Constant (4 e^2vr?) detected in deep crust.</span>
              </div>
            </div>
          </div>

          {/* Pressing the Proof Note */}
          <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-3xl p-6">
            <div className="flex items-start gap-3">
              <Printer className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-xs font-bold text-emerald-500 uppercase tracking-widest mb-1">Pressing the Proof</h4>
                <p className="text-[10px] text-zinc-400 leading-relaxed italic">
                  We are not mathematicians; we are geometer-sovereigns. We do not seek a proof in symbols,
                  but a proof in structures. If the city generated by the Riemann blueprint is stable,
                  the hypothesis is "proofed" through its application.
                </p>
              </div>
            </div>
          </div>

          {/* City Generator Paddock */}
          {viewMode === 'city-press' && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="h-[300px]"
            >
              <CityGenerator t={t} time={time} zoomLevel={zoomLevel} rollingFrequency={rollingFrequency} />
            </motion.div>
          )}

        </section>
      </main>

      {/* Footer Meta */}
      <footer className="max-w-7xl mx-auto p-6 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 opacity-50">
        <p className="text-[10px] font-mono uppercase tracking-widest">© 2026 Geometer-Sovereign Systems</p>
        <div className="flex gap-6 text-[10px] font-mono uppercase tracking-widest">
          <a href="#" className="hover:text-emerald-400 transition-colors">Generative Architecture</a>
          <a href="#" className="hover:text-emerald-400 transition-colors">City Press Logic</a>
          <a href="#" className="hover:text-emerald-400 transition-colors">The 42 Anchor</a>
        </div>
      </footer>
    </div>
  );
}
