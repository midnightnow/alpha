import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Line, Sphere, Text, Float, OrbitControls, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';

const CameraBox = ({ position, scale, color, opacity = 0.2 }: any) => {
    return (
        <group position={position} scale={scale}>
            {/* The Chamber */}
            <mesh>
                <boxGeometry args={[1, 1, 2]} />
                <meshStandardMaterial color={color} transparent opacity={opacity} wireframe />
            </mesh>
            {/* Aperture Point */}
            <Sphere args={[0.08, 16, 16]} position={[0, 0, 1]}>
                <meshStandardMaterial color="white" emissive="white" emissiveIntensity={5} />
            </Sphere>
        </group>
    );
};

const LightRay = ({ start, aperture, end, color }: any) => {
    const points = useMemo(() => [
        new THREE.Vector3().fromArray(start),
        new THREE.Vector3().fromArray(aperture),
        new THREE.Vector3().fromArray(end)
    ], [start, aperture, end]);

    return (
        <Line
            points={points}
            color={color}
            lineWidth={1.5}
            transparent
            opacity={0.6}
            dashed
            dashScale={50}
            gapSize={1}
        />
    );
};

export const OpticChiasm: React.FC<{ time: number }> = ({ time }) => {
    const groupRef = useRef<THREE.Group>(null);

    useFrame((state) => {
        if (groupRef.current) {
            groupRef.current.rotation.y = Math.sin(time * 0.1) * 0.05;
            groupRef.current.rotation.x = Math.cos(time * 0.1) * 0.02;
        }
    });

    return (
        <group ref={groupRef}>
            {/* Primary Optic Path (Dual Eyes) */}
            <group position={[0, 0, -2]}>
                <CameraBox position={[-2.5, 0, 0]} scale={[2, 2, 2]} color="#ef4444" /> {/* Left Eye */}
                <CameraBox position={[2.5, 0, 0]} scale={[2, 2, 2]} color="#3b82f6" /> {/* Right Eye */}
            </group>

            {/* The Chiasm Aperture (s=13) */}
            <group position={[0, 0, -0.5]}>
                <Sphere args={[0.2, 32, 32]}>
                    <meshStandardMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={3} />
                </Sphere>
                <Text position={[0, 0.6, 0]} fontSize={0.2} color="white" font="/fonts/Inter-Bold.woff" anchorX="center">
                    CHIASM APERTURE (s=13)
                </Text>

                {/* Crossing Light Rays */}
                <LightRay start={[-2.5, -0.5, -1]} aperture={[0, 0, 0]} end={[2.5, 0.5, 3]} color="#ef4444" />
                <LightRay start={[2.5, -0.5, -1]} aperture={[0, 0, 0]} end={[-2.5, 0.5, 3]} color="#3b82f6" />
            </group>

            {/* The Pineal Convergence (s=93) - RECURSIVE NESTING */}
            <group position={[0, 0, 4]}>
                <Sphere args={[0.5, 64, 64]}>
                    <meshStandardMaterial color="#8b5cf6" emissive="#8b5cf6" emissiveIntensity={15} wireframe />
                </Sphere>
                <Text position={[0, 0.8, 0]} fontSize={0.3} color="#8b5cf6" font="/fonts/Inter-Bold.woff" anchorX="center">
                    PINEAL CONVERGENCE (s=93)
                </Text>

                {/* Nested Mirror Obscura (The recursively seen world) */}
                <group scale={[0.4, 0.4, 0.4]} position={[0, 0, 1.5]}>
                    <CameraBox position={[0, 0, 0]} scale={[1, 1, 1]} color="#8b5cf6" opacity={0.6} />
                    <Sphere args={[0.1, 16, 16]} position={[0, 0, -1]}>
                        <meshBasicMaterial color="#ffffff" />
                    </Sphere>
                </group>
            </group>

            {/* Static Grid / Horizon Calibration */}
            <gridHelper args={[40, 40, 0x333333, 0x111111]} rotation={[Math.PI / 2, 0, 0]} position={[0, 0, -5]} />

            <Float speed={3} rotationIntensity={0.2} floatIntensity={0.1}>
                <Text position={[0, -5, 0]} fontSize={0.6} color="#4b5563" font="/fonts/Inter-Bold.woff" anchorX="center">
                    OPTIC SYSTEM // CAMERA OBSCURA v2.0
                </Text>
            </Float>

            <ambientLight intensity={0.4} />
            <spotLight position={[0, 10, 10]} intensity={2} color="#ffffff" />
            <pointLight position={[0, 0, 4]} intensity={2} color="#8b5cf6" />
        </group>
    );
};

export default function OpticChiasmVisualizer({ time }: { time: number }) {
    return (
        <div style={{ width: '100%', height: '100%', background: '#050508' }}>
            <Canvas camera={{ position: [8, 5, 12], fov: 45 }}>
                <OrbitControls />
                <OpticChiasm time={time} />
            </Canvas>
        </div>
    );
}
