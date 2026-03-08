/**
 * @license
 * FractalZoomModule.tsx - The Sovereign Geometry Bridge
 * Distinguishing Potentiality (Poppy Seed) from Manifestation (Pomegranate)
 */

import React, { useMemo } from 'react';
import * as THREE from 'three';
import { Points, PointMaterial } from '@react-three/drei';

const PHI2 = 2.61803398875;
const RESIDUAL_ENTROPY = 0.037;

/**
 * 1. THE MATHEMATICAL HEART: FRACTAL POSITIONING
 * Maps nodes across the 10-24-26 manifold based on n^n (Seed) or (10n)^n (Fruit) scaling.
 */
export const calculateFractalPosition = (n: number, zoom: number): THREE.Vector3 => {
    // Zoom 0.0 (Seed) -> Base = n
    // Zoom 1.0 (Fruit) -> Base = 10n
    const base = n * (1 + 9 * zoom);

    // Logarithmic magnitude to maintain visual handleability
    // Actual formula: (base)^n
    // Visual Projection: (base)^(n * 0.1) * scale_multiplier
    const magnitude = Math.pow(base, n * 0.1) * (1 + zoom * 8);

    return new THREE.Vector3(
        magnitude * Math.cos(n * PHI2),
        magnitude * Math.sin(n * PHI2),
        RESIDUAL_ENTROPY * n // The persistent Z-axis drift
    );
};

/**
 * 2. THE SKELETON MODULE: FRACTAL TRANSITION
 */
interface FractalZoomModuleProps {
    zoom: number; // 0.0 (Seed) to 1.0 (Fruit)
    life: number; // Seasonal Amplitude (The Life of the Poppy)
    nodeCount?: number;
}

export const FractalZoomModule: React.FC<FractalZoomModuleProps> = ({
    zoom,
    life = 1.0,
    nodeCount = 93
}) => {

    // 3. LOGARITHMIC INTERPOLATOR
    // Maps linear input to exponential rendering depths
    const depth = useMemo(() => Math.exp(zoom * 2.3025), [zoom]); // 1 to 10 scale

    // 4. THE 3x33 WING GENERATOR
    // Spawns miniature "Triangles of Intent" inside the central node
    const wingPoints = useMemo(() => {
        const pts = new Float32Array(99 * 3); // 3x33
        for (let i = 0; i < 99; i++) {
            const angle = (i / 33) * Math.PI * 2;
            const r = 0.5 * (i % 3 + 1);
            pts[i * 3] = r * Math.cos(angle);
            pts[i * 3 + 1] = r * Math.sin(angle);
            pts[i * 3 + 2] = (i / 99) * 0.1;
        }
        return pts;
    }, []);

    // 5. SHADER-LITE OPACITY CONTROLLER
    // Handles the cross-fade between potential and manifest
    const seedOpacity = Math.max(0, 1 - zoom * 3);
    const fruitOpacity = Math.max(0, (zoom - 0.5) * 2);

    return (
        <group>
            {/* INNER SEED CORE (The life of the poppy) */}
            {zoom < 0.4 && (
                <group scale={(0.1 + life * 0.1) * (1 - zoom)}>
                    <Points positions={wingPoints}>
                        <PointMaterial
                            transparent
                            color="#ffffff"
                            size={0.05}
                            opacity={seedOpacity}
                            depthWrite={false}
                        />
                    </Points>
                    <mesh>
                        <dodecahedronGeometry args={[0.5, 0]} />
                        <meshBasicMaterial
                            color="#ffd700"
                            wireframe
                            transparent
                            opacity={seedOpacity * 0.5}
                        />
                    </mesh>
                </group>
            )}

            {/* MANIFEST POMEGRANATE (The external expansion) */}
            {zoom > 0.6 && (
                <group scale={zoom * 10}>
                    {/* Placeholder for clustered 93-point solids */}
                    <Stars radius={5} depth={10} count={100} factor={1} saturation={0} />
                </group>
            )}
        </group>
    );
};

/**
 * STARS HELPER (Standalone projection)
 */
function Stars({ radius, depth, count, factor, saturation }: any) {
    const pts = useMemo(() => {
        const p = new Float32Array(count * 3);
        for (let i = 0; i < count; i++) {
            const r = radius + Math.random() * depth;
            const theta = Math.random() * Math.PI * 2;
            p[i * 3] = r * Math.cos(theta);
            p[i * 3 + 1] = (Math.random() - 0.5) * 5;
            p[i * 3 + 2] = r * Math.sin(theta);
        }
        return p;
    }, [count, radius, depth]);

    return (
        <Points positions={pts}>
            <PointMaterial transparent color="#ff3300" size={0.05} sizeAttenuation={false} opacity={0.5} />
        </Points>
    );
}
