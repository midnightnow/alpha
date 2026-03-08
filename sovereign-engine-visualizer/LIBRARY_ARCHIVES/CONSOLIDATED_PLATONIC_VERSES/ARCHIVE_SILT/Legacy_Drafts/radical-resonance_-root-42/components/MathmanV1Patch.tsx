import React, { useMemo, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Sphere, Text, Line } from '@react-three/drei';
import * as THREE from 'three';

import { SimulationParams } from '../types';
import { UNITY_THRESHOLD, COLORS } from '../constants';

interface Props {
    params: SimulationParams;
}

const SCALING_FACTOR = Math.sqrt(42);

export const MathmanV1Patch: React.FC<Props> = ({ params: simParams }) => {
    // Map SimulationParams to the internal logic of the patch
    const params = useMemo(() => ({
        wavelength: 1.5, // Standard wavelength for this visualization
        towerElevation: simParams.fracture ? 5 : 0, // Elevation tied to fracture state for now
        phasePhi: 0,
        phasePsi: Math.PI / 4,
        // Using interferenceB as a proxy for frequency mapping if needed
        scaling: simParams.interferenceB / Math.sqrt(42)
    }), [simParams.interferenceB, simParams.fracture]);

    const origins = [
        { id: 'A', pos: [0, 0, 0] as [number, number, number], color: COLORS.originA },
        { id: 'B', pos: [12, 0, 0] as [number, number, number], color: COLORS.originB },
    ];

    // Memoize grid to prevent re-calculating points every frame
    const gridPoints = useMemo(() => {
        const points = [];
        const wavelength = params.wavelength;
        const towerElevation = params.towerElevation;
        const scaling = params.scaling;

        for (let x = -10; x < 22; x += 0.8) {
            for (let y = -10; y < 10; y += 0.8) {
                const distA = Math.sqrt(x ** 2 + y ** 2);
                const distB = Math.sqrt((x - 12) ** 2 + y ** 2);

                // Interference logic with Chapter 21 scaling
                const waveA = Math.sin((distA / wavelength) * SCALING_FACTOR + params.phasePhi);
                const waveB = Math.sin((distB / wavelength) * SCALING_FACTOR + params.phasePsi);
                const intensity = (waveA + waveB) / 2 * scaling;

                // Map intensity to Unity Threshold ρ
                const opacity = Math.min(Math.abs(intensity) / UNITY_THRESHOLD, 1.0);

                if (opacity > 0.2) {
                    points.push({ x, y, opacity, intensity });
                }
            }
        }
        return points;
    }, [params]);

    return (
        <div className="absolute inset-0 z-0 bg-[#050505]">
            <Canvas camera={{ position: [6, -15, 15], fov: 50 }}>
                <OrbitControls />
                <ambientLight intensity={0.4} />
                <pointLight position={[10, 10, 10]} />

                {/* Origin Points */}
                {origins.map((o) => (
                    <group key={o.id} position={o.pos}>
                        <Sphere args={[0.4, 32, 32]}>
                            <meshStandardMaterial color={o.color} emissive={o.color} emissiveIntensity={0.5} />
                        </Sphere>
                        <Text position={[0, -1, 0]} fontSize={0.5} color="white">Origin {o.id}</Text>
                    </group>
                ))}

                {/* The Tower & Person at 5 (Echo Logic) */}
                <group position={[6, 0, 0]}>
                    <Line
                        points={[[0, 0, 0], [0, 0, params.towerElevation]]}
                        color={COLORS.echo}
                        lineWidth={2}
                    />
                    <Sphere args={[0.3, 16, 16]} position={[0, 0, params.towerElevation]}>
                        <meshStandardMaterial color={COLORS.echo} emissive={COLORS.echo} />
                    </Sphere>
                    <Text position={[0, 0, params.towerElevation + 0.8]} fontSize={0.4} color={COLORS.echo}>
                        Person at {params.towerElevation} (Ψ_debt)
                    </Text>
                </group>

                {/* Wave Interference Mesh */}
                {gridPoints.map((p, i) => (
                    <Sphere key={i} args={[0.08, 8, 8]} position={[p.x, p.y, p.intensity * 0.5]}>
                        <meshStandardMaterial
                            color={p.intensity > 0 ? COLORS.originA : COLORS.originB}
                            transparent
                            opacity={p.opacity}
                        />
                    </Sphere>
                ))}

                <gridHelper args={[40, 40, 0x222222, 0x111111]} rotation={[Math.PI / 2, 0, 0]} />
            </Canvas>
        </div>
    );
}
