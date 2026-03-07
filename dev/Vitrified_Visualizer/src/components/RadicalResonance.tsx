import React, { useMemo, useRef, useState, useCallback, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Environment, ContactShadows, Line } from '@react-three/drei';
import * as THREE from 'three';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, Layers, Box, ChevronsUp, Zap, Play, Pause, RefreshCw } from 'lucide-react';
import { ViewMode, SimulationParams, LADDER_STEPS } from '../types/resonance';

const SHEAR_ANGLE = Math.atan(14 / 17);

const computeVertex = (theta: number, phi: number, params: SimulationParams) => {
    const { interferenceA, interferenceB, distortion, fracture } = params;
    const intensity = Math.abs(
        Math.sin(interferenceA * theta) * Math.sin(interferenceB * phi) +
        Math.sin(interferenceB * theta) * Math.sin(interferenceA * phi)
    );
    const pulseFreq = (interferenceA + interferenceB) / 2;
    const pulse = Math.sin(pulseFreq * theta) * (distortion * 0.5);
    let r = 1 + (intensity * distortion) + pulse;

    if (fracture) {
        const microTremor = Math.sin(theta * 100) * Math.sin(phi * 80) * 0.1;
        const stress = Math.abs(Math.sin(17 * theta + SHEAR_ANGLE));
        const noisyStress = stress * (1 + microTremor);
        if (noisyStress > 0.85) {
            const directionNoise = Math.sin(theta * 50 + phi * 50);
            const direction = directionNoise > 0 ? 1 : -1;
            const magnitude = direction > 0 ? 0.03 : -0.05;
            r += magnitude * stress;
        }
    }

    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    return new THREE.Vector3(x, y, z);
};

const InterferenceMesh = ({ mode, params }: { mode: ViewMode, params: SimulationParams }) => {
    const meshRef = useRef<THREE.Mesh>(null);
    const geometry = useMemo(() => {
        const geo = new THREE.SphereGeometry(1, 128, 128);
        const posAttribute = geo.attributes.position;
        const vertex = new THREE.Vector3();
        for (let i = 0; i < posAttribute.count; i++) {
            vertex.fromBufferAttribute(posAttribute, i);
            const r_base = vertex.length();
            const theta = Math.atan2(vertex.y, vertex.x);
            const phi = Math.acos(vertex.z / r_base);
            const newPos = computeVertex(theta, phi, params);
            posAttribute.setXYZ(i, newPos.x, newPos.y, newPos.z);
        }
        geo.computeVertexNormals();
        return geo;
    }, [params.interferenceA, params.interferenceB, params.distortion, params.fracture]);

    useFrame((state, delta) => {
        if (meshRef.current) {
            meshRef.current.rotation.y += params.rotationSpeed * delta;
            const t = state.clock.elapsedTime;
            const wobble = 0.02 * Math.sin(params.interferenceA * t * 2) + 0.02 * Math.sin(params.interferenceB * t * 2);
            meshRef.current.rotation.z = wobble;
        }
    });

    return (
        <mesh ref={meshRef} geometry={geometry}>
            {mode === ViewMode.FIELD && <meshStandardMaterial color="#4f46e5" wireframe emissive="#220033" roughness={0.2} metalness={0.8} />}
            {mode === ViewMode.SOLID && (
                <meshPhysicalMaterial
                    color={params.harmonicMode === 'fracture' ? "#0a0a0a" : "#e0e7ff"}
                    roughness={params.harmonicMode === 'fracture' ? 0.2 : 0.05}
                    metalness={params.harmonicMode === 'fracture' ? 0.8 : 0.1}
                    transmission={params.harmonicMode === 'fracture' ? 0 : 0.65}
                    thickness={1.5}
                    ior={1.45}
                    clearcoat={1}
                    flatShading={params.fracture}
                    emissive={params.harmonicMode === 'fracture' ? "#330000" : "#9933ff"}
                    emissiveIntensity={params.harmonicMode === 'fracture' ? 0.5 : 0.2}
                />
            )}
            {mode === ViewMode.CRYSTAL && <meshNormalMaterial flatShading />}
        </mesh>
    );
};

export const RadicalResonance: React.FC = () => {
    const [mode, setMode] = useState<ViewMode>(ViewMode.FIELD);
    const [params, setParams] = useState<SimulationParams>({
        interferenceA: Math.sqrt(42),
        interferenceB: Math.sqrt(51),
        distortion: 0.25,
        rotationSpeed: 0.2,
        activeStep: 1,
        fracture: true,
        harmonicMode: 'fracture'
    });

    const handleStepSelect = (step: number) => {
        const info = LADDER_STEPS[step];
        setParams(prev => ({
            ...prev,
            interferenceB: Math.sqrt(info.radicand),
            activeStep: step
        }));
    };

    return (
        <div className="relative w-full h-full bg-[#050508]">
            <Canvas camera={{ position: [3, -3, 1.5], fov: 45 }}>
                <Suspense fallback={null}>
                    <InterferenceMesh mode={mode} params={params} />
                    <Environment preset="city" />
                    <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
                    <ambientLight intensity={0.1} />
                    <directionalLight position={[5, 5, 5]} intensity={3.0} color="#cce0ff" />
                    <spotLight position={[0, 0, 5]} angle={0.6} penumbra={0.5} intensity={50.0} color="#9933ff" />
                    <OrbitControls />
                </Suspense>
            </Canvas>

            {/* Interface Overlay */}
            <div className="absolute inset-0 pointer-events-none p-8 flex flex-col justify-between">
                <div className="pointer-events-auto">
                    <h2 className="text-2xl font-black italic tracking-tighter text-white">RADICAL<span className="text-cyan-400">RESONANCE</span></h2>
                    <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest mt-1">√42 Genetic Ladder // Phase IV Calibration</p>
                </div>

                <div className="pointer-events-auto self-start w-80 space-y-6">
                    {/* Ladder Controls */}
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 p-4 rounded-xl shadow-2xl">
                        <div className="flex items-center gap-2 text-[10px] font-bold text-cyan-400 mb-4 uppercase tracking-[0.2em] animate-pulse">
                            <ChevronsUp size={14} /> Radical Ladder
                        </div>
                        <div className="grid grid-cols-4 gap-2">
                            {LADDER_STEPS.map((step, i) => (
                                <button
                                    key={i}
                                    onClick={() => handleStepSelect(i)}
                                    className={`flex flex-col items-center py-2 border rounded-lg transition-all ${params.activeStep === i ? 'bg-cyan-500/20 border-cyan-400 text-cyan-300' : 'bg-white/5 border-white/5 text-zinc-500 hover:bg-white/10'}`}
                                >
                                    <span className="text-lg font-black">{step.step}</span>
                                    <span className="text-[8px] uppercase">{step.label}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Simulation Parameters */}
                    <div className="bg-black/60 backdrop-blur-xl border border-white/10 p-4 rounded-xl space-y-4">
                        {[
                            { label: 'Harmonic A (√42)', value: params.interferenceA, key: 'interferenceA', min: 1, max: 12 },
                            { label: 'Harmonic B (√N)', value: params.interferenceB, key: 'interferenceB', min: 1, max: 12 },
                            { label: 'Distortion', value: params.distortion, key: 'distortion', min: 0, max: 1 }
                        ].map(slider => (
                            <div key={slider.key}>
                                <div className="flex justify-between text-[8px] font-mono text-zinc-400 mb-1 uppercase tracking-widest">
                                    <span>{slider.label}</span>
                                    <span>{slider.value.toFixed(3)}</span>
                                </div>
                                <input
                                    type="range" min={slider.min} max={slider.max} step="0.01"
                                    value={slider.value}
                                    onChange={(e) => setParams(prev => ({ ...prev, [slider.key]: parseFloat(e.target.value), activeStep: null }))}
                                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                                />
                            </div>
                        ))}
                    </div>

                    {/* Mode Toggles */}
                    <div className="flex gap-1 overflow-x-auto pb-2">
                        {Object.values(ViewMode).map(m => (
                            <button
                                key={m}
                                onClick={() => setMode(m)}
                                className={`px-3 py-1.5 rounded-full text-[8px] font-black uppercase tracking-widest transition-all ${mode === m ? 'bg-indigo-500 text-white shadow-lg' : 'bg-zinc-900 text-zinc-500 hover:bg-zinc-800'}`}
                            >
                                {m}
                            </button>
                        ))}
                    </div>

                    <button
                        onClick={() => setParams(prev => ({ ...prev, fracture: !prev.fracture }))}
                        className={`w-full py-2 rounded-lg text-[10px] font-bold flex items-center justify-center gap-2 border transition-all ${params.fracture ? 'bg-orange-500/10 border-orange-500 text-orange-400 animate-pulse' : 'bg-zinc-900 border-zinc-800 text-zinc-500'}`}
                    >
                        <Zap size={14} /> {params.fracture ? 'FRACTURE SYNTHESIS ACTIVE' : 'ENABLE FRACTURE SYNTHESIS'}
                    </button>
                </div>

                <div className="self-end pointer-events-none">
                    <div className="flex flex-col items-end gap-1">
                        <span className="text-[10px] font-black text-rose-500 uppercase tracking-widest">Archive Sealed</span>
                        <div className="text-[40px] font-black italic text-white/5 tracking-tighter leading-none select-none">√42.93</div>
                    </div>
                </div>
            </div>
        </div>
    );
};
