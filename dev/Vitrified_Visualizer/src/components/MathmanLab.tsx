import React, { useMemo, useRef, useState, useCallback, Suspense, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Environment, Text } from '@react-three/drei';
import * as THREE from 'three';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Zap, Play, Info } from 'lucide-react';
import { audioEngine } from '../audioEngine';

// Logic from PLATO/mathman/PointCloudRenderer.js and GenesisSequence.js
// Simplified for React/Three integration

const SHEAR_ANGLE = Math.atan(14 / 17);

const MathmanMesh = ({ resonance }: { resonance: number }) => {
    const meshRef = useRef<THREE.InstancedMesh>(null);
    const tempObject = new THREE.Object3D();

    // Harmonic Grid count
    const count = 13 * 13;

    useFrame((state) => {
        if (!meshRef.current) return;

        let i = 0;
        for (let x = -6; x <= 6; x++) {
            for (let z = -6; z <= 6; z++) {
                const px = x * 0.5;
                const pz = z * 0.5;
                const dist = Math.sqrt(px * px + pz * pz);
                const py = Math.sin(dist * resonance - state.clock.elapsedTime) * 0.2;

                tempObject.position.set(px, py, pz);
                tempObject.updateMatrix();
                meshRef.current.setMatrixAt(i++, tempObject.matrix);
            }
        }
        meshRef.current.instanceMatrix.needsUpdate = true;
        meshRef.current.rotation.y = state.clock.elapsedTime * 0.1;
    });

    return (
        <group>
            <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
                <sphereGeometry args={[0.02, 8, 8]} />
                <meshStandardMaterial color="#00f2ff" emissive="#00f2ff" emissiveIntensity={2} />
            </instancedMesh>

            {/* The Vitruvian Arc */}
            <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
                <ringGeometry args={[2.9, 3, 128]} />
                <meshBasicMaterial color="#ffffff" transparent opacity={0.1} side={THREE.DoubleSide} />
            </mesh>
        </group>
    );
};

export const MathmanLab: React.FC = () => {
    const [resonance, setResonance] = useState(Math.sqrt(42));
    const [isGenesisActive, setIsGenesisActive] = useState(false);

    const toggleAudio = () => {
        audioEngine.init().then(() => {
            audioEngine.play();
        });
    };

    return (
        <div className="relative w-full h-full bg-[#050508] text-white">
            <Canvas camera={{ position: [5, 5, 5], fov: 45 }}>
                <Suspense fallback={null}>
                    <MathmanMesh resonance={resonance} />
                    <Environment preset="city" />
                    <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
                    <OrbitControls />

                    {/* Labels */}
                    <Text position={[0, 3.5, 0]} fontSize={0.2} color="white" font="/fonts/Inter-Bold.otf">
                        VITRUVIAN ARC // √42 Calibration
                    </Text>
                </Suspense>
            </Canvas>

            {/* UI Overlay */}
            <div className="absolute inset-0 pointer-events-none p-8 flex flex-col justify-between">
                <div className="flex justify-between items-start pointer-events-auto">
                    <div>
                        <h2 className="text-2xl font-black italic text-cyan-400">MATHMAN<span className="text-white">LAB</span></h2>
                        <p className="text-[10px] font-mono opacity-50 uppercase tracking-widest">Phase IV: Volumetric Materialization</p>
                    </div>
                    <button
                        onClick={toggleAudio}
                        className="p-4 bg-rose-500/20 border border-rose-500 rounded-full text-rose-500 hover:bg-rose-500 hover:text-white transition-all animate-pulse"
                    >
                        <Play size={24} />
                    </button>
                </div>

                <div className="pointer-events-auto w-80 space-y-4">
                    <div className="bg-black/80 backdrop-blur-xl border border-white/10 p-4 rounded-xl">
                        <div className="flex justify-between text-[10px] font-mono mb-2 text-cyan-400 uppercase">
                            <span>Resonance Factor</span>
                            <span>{resonance.toFixed(4)}</span>
                        </div>
                        <input
                            type="range" min="1" max="12" step="0.001"
                            value={resonance}
                            onChange={(e) => setResonance(parseFloat(e.target.value))}
                            className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-[10px] font-mono">
                        <div className="p-3 bg-white/5 border border-white/10 rounded-lg">
                            <span className="opacity-40 block mb-1">STATION</span>
                            <span className="text-cyan-400">NAVEL (4.2)</span>
                        </div>
                        <div className="p-3 bg-white/5 border border-white/10 rounded-lg">
                            <span className="opacity-40 block mb-1">DRIFT</span>
                            <span className="text-rose-500">0.009 (WILL)</span>
                        </div>
                    </div>

                    <button
                        onClick={() => setIsGenesisActive(true)}
                        className="w-full py-4 bg-cyan-500/10 border border-cyan-500 text-cyan-400 font-black text-xs uppercase tracking-widest hover:bg-cyan-500 hover:text-white transition-all"
                    >
                        Initiate Genesis Sequence
                    </button>
                </div>
            </div>

            {/* Genesis Overlay */}
            <AnimatePresence>
                {isGenesisActive && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-[200] bg-black/90 flex flex-col items-center justify-center p-12 pointer-events-auto"
                    >
                        <div className="max-w-xl text-center space-y-6">
                            <h3 className="text-3xl font-serif italic text-cyan-400">Genesis Phase 01: Singularity</h3>
                            <p className="text-lg opacity-80 leading-relaxed font-serif">
                                Time establishes Measure. Origin A is the seed. In the beginning, there was only the 1,
                                the point that defines the space before space was known.
                            </p>
                            <div className="pt-8 flex gap-4 justify-center">
                                <button
                                    onClick={() => setIsGenesisActive(false)}
                                    className="px-8 py-2 border border-white/20 text-xs uppercase hover:bg-white hover:text-black transition-all"
                                >
                                    Abort
                                </button>
                                <button className="px-8 py-2 bg-rose-500 text-white text-xs uppercase hover:bg-rose-600 transition-all font-bold">
                                    Next Phase
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
