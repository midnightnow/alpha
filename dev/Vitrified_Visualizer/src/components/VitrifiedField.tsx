import React, { useMemo, useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Sphere, Text, Float, Stars, Environment } from '@react-three/drei';
import * as THREE from 'three';

const HeroSolid = ({ time }: { time: number }) => {
    const groupRef = useRef<THREE.Group>(null);

    // Harmonic Geometry Generation (93 Vertices)
    const { vertices, edges } = useMemo(() => {
        const verts = [];
        const count = 93;
        const R = 4.2;

        for (let i = 0; i < count; i++) {
            const phi = Math.acos(-1 + (2 * i) / count);
            const theta = Math.sqrt(count * Math.PI) * phi;

            const x = R * Math.sin(phi) * Math.cos(theta);
            const y = R * Math.sin(phi) * Math.sin(theta);
            const z = R * Math.cos(phi);
            verts.push(new THREE.Vector3(x, y, z));
        }

        const lines: [THREE.Vector3, THREE.Vector3][] = [];
        for (let i = 0; i < count; i++) {
            for (let j = i + 1; j < count; j++) {
                if (verts[i].distanceTo(verts[j]) < 1.8) {
                    lines.push([verts[i], verts[j]]);
                }
            }
        }

        return { vertices: verts, edges: lines };
    }, []);

    useFrame((state) => {
        if (groupRef.current) {
            groupRef.current.rotation.y = time * 0.05;
            groupRef.current.rotation.z = Math.sin(time * 0.1) * 0.02;
        }
    });

    return (
        <group ref={groupRef}>
            {/* Bracing lines */}
            {edges.map((edge, i) => (
                <Line
                    key={`edge-${i}`}
                    points={[edge[0], edge[1]]}
                    color="#00ffff"
                    lineWidth={0.5}
                    transparent
                    opacity={0.1}
                />
            ))}

            {/* Vertices */}
            {vertices.map((v, i) => {
                const isGenesis = i === 15 || i === 45;
                const color = i === 15 ? "#ff3c64" : i === 45 ? "#3b82f6" : "#ffffff";

                return (
                    <group key={i} position={[v.x, v.y, v.z]}>
                        <Sphere args={[isGenesis ? 0.08 : 0.03, 8, 8]}>
                            <meshStandardMaterial
                                color={color}
                                emissive={color}
                                emissiveIntensity={isGenesis ? 10 : 2}
                            />
                        </Sphere>
                        {isGenesis && (
                            <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
                                <Text
                                    position={[0, 0.4, 0]}
                                    fontSize={0.2}
                                    color={color}
                                    font="/fonts/Inter-Bold.woff"
                                    anchorX="center"
                                >
                                    {i === 15 ? "EST (PRESENCE)" : "WEST (ENTROPY)"}
                                </Text>
                            </Float>
                        )}
                    </group>
                );
            })}

            {/* Internal Core (Zero Point) */}
            <Sphere args={[0.5, 32, 32]}>
                <meshStandardMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={2} transparent opacity={0.05} wireframe />
            </Sphere>
        </group>
    );
};

export const VitrifiedField: React.FC<{ time: number }> = ({ time }) => {
    return (
        <div className="w-full h-full bg-[#050508] relative">
            <Canvas camera={{ position: [10, 5, 10], fov: 45 }}>
                <Suspense fallback={null}>
                    <color attach="background" args={['#050508']} />
                    <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
                    <Environment preset="night" />

                    <HeroSolid time={time} />

                    <ambientLight intensity={0.2} />
                    <pointLight position={[10, 10, 10]} intensity={1} color="#00ffff" />
                    <spotLight position={[-10, 10, 5]} angle={0.3} penumbra={1} intensity={2} color="#ff3c64" />

                    <OrbitControls />
                </Suspense>
            </Canvas>

            {/* HUD Overlay for Hero 93 */}
            <div className="absolute top-10 right-10 text-right pointer-events-none z-10">
                <h2 className="text-xl font-black italic text-zinc-600 uppercase tracking-tighter">Vitrified Solid</h2>
                <div className="flex flex-col gap-1 mt-2">
                    <div className="text-[10px] font-mono text-cyan-500 font-bold uppercase tracking-widest">
                        93 Vertices Locked // Zero Hysteresis
                    </div>
                    <div className="text-[10px] font-mono text-zinc-700 uppercase">
                        Ψ = 12.37% Tensegrity Constant
                    </div>
                </div>
            </div>

            <div className="absolute bottom-10 inset-x-10 flex justify-between items-end pointer-events-none z-10">
                <div className="max-w-xs">
                    <p className="text-[9px] font-mono text-zinc-500 leading-relaxed italic">
                        "The 93-faced solid functions as a geometric memory buffer, vitrifying the fractal resonance of the 171 spiral."
                    </p>
                </div>
                <div className="text-[40px] font-black italic text-white/5 select-none tracking-tighter">
                    HERO.93
                </div>
            </div>
        </div>
    );
};
