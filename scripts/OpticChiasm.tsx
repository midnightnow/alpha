import React, { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Line, Sphere, Html } from '@react-three/drei';
import * as THREE from 'three';

const OpticSnakes = () => {
    const steps = 94; // 0 to 93

    // Compute geometry inside useMemo for performance
    const { path1, path2 } = useMemo(() => {
        const p1 = [];
        const p2 = [];

        for (let i = 0; i < steps; i++) {
            // Radius pinch at 13 (Chiasm), convergence at 93 (Pineal)
            let R = 0;
            if (i <= 13) {
                R = 3.0 * Math.cos((Math.PI / 2) * (i / 13));
            } else {
                R = 5.0 * Math.sin(Math.PI * (i - 13) / 80);
            }

            // +5 stepping mapped to radians
            const thetaStep = 5 * ((2 * Math.PI) / 24);
            const theta1 = i * thetaStep;
            const theta2 = theta1 + Math.PI; // Opposite phase

            // Z scaled down visually for the component
            const z = i * 0.2;

            p1.push(new THREE.Vector3(R * Math.cos(theta1), R * Math.sin(theta1), z));
            p2.push(new THREE.Vector3(R * Math.cos(theta2), R * Math.sin(theta2), z));
        }

        return { path1: p1, path2: p2 };
    }, []);

    // Chiasm (s=13) and Pineal (s=93) coordinates
    const chiasmZ = 13 * 0.2;
    const pinealZ = 93 * 0.2;

    return (
        <group position={[0, 0, -10]}>
            {/* Snake 1: Left Eye */}
            <Line points={path1} color="red" lineWidth={3} />
            {/* Snake 2: Right Eye */}
            <Line points={path2} color="cyan" lineWidth={3} />

            {/* Optic Chiasm Marker */}
            <Sphere position={[0, 0, chiasmZ]} args={[0.3, 16, 16]}>
                <meshStandardMaterial color="yellow" emissive="yellow" emissiveIntensity={2} />
                <Html distanceFactor={15} center>
                    <div style={{ color: 'yellow', fontWeight: 'bold', textShadow: '0 0 5px black' }}>
                        Optic Chiasm (s=13)
                    </div>
                </Html>
            </Sphere>

            {/* Pineal Gland Marker */}
            <Sphere position={[0, 0, pinealZ]} args={[0.5, 32, 32]}>
                <meshStandardMaterial color="gold" emissive="orange" emissiveIntensity={2} />
                <Html distanceFactor={15} center>
                    <div style={{ color: 'gold', fontWeight: 'bold', textShadow: '0 0 5px black', marginTop: '-30px' }}>
                        Pineal Gland (s=93)
                    </div>
                </Html>
            </Sphere>

            {/* Lighting */}
            <ambientLight intensity={0.5} />
            <pointLight position={[0, 5, 5]} intensity={1} />
        </group>
    );
};

export default function OpticChiasmVisualizer() {
    return (
        <div style={{ width: '100vw', height: '100vh', background: '#0a0a0f' }}>
            <Canvas camera={{ position: [10, 10, 10], fov: 60 }}>
                <OrbitControls autoRotate autoRotateSpeed={0.5} />
                <OpticSnakes />
            </Canvas>
        </div>
    );
}
