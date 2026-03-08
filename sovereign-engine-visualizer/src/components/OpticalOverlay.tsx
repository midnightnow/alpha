import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useSovereignStore } from '../store/useSovereignStore';

export function OpticalOverlay({ visible }: { visible: boolean }) {
    const { fractalZoom, currentWeek } = useSovereignStore();

    const meshRef = useRef<THREE.Group>(null);
    const irisRef = useRef<THREE.Mesh>(null);
    const focalPlaneRef = useRef<THREE.Mesh>(null);
    const airyDiskRef = useRef<THREE.Mesh>(null);
    const raysRef = useRef<THREE.LineSegments>(null);

    // Optical Constants
    const FOCAL_LENGTH = 12;
    const DIFFRACTION_LIMIT = 0.037; // operating temperature

    // Ray structure
    const RAY_COUNT = 33; // number of marginal rays

    // Pre-allocate geometry for rays
    const raysGeometry = useMemo(() => {
        const geo = new THREE.BufferGeometry();
        const positions = new Float32Array(RAY_COUNT * 2 * 3);
        geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        return geo;
    }, []);

    useFrame((state) => {
        if (!visible) return;
        const t = state.clock.getElapsedTime();

        // Map fractalZoom (0..1) to Aperture Radius n (0.5 to 5.0)
        // 0 = Poppy (0.5), 0.5 = Mustard (1.5), 1 = Pomegranate (5.0)
        const n = 0.5 + Math.pow(fractalZoom, 1.5) * 4.5;

        // Clubs waveform modulates the iris breathing
        const clubsPulse = (currentWeek >= 27 && currentWeek <= 39)
            ? Math.pow(Math.sin(Math.PI * (currentWeek - 27) / 12), 2)
            : 0;

        // Dynamic aperture radius (breathing slightly)
        const currentAperture = n * (1 + 0.05 * Math.sin(t * 2) + 0.1 * clubsPulse);

        // Update Iris (Aperture Stop)
        if (irisRef.current) {
            // 12-sided polygon for 12-tick pulse
            irisRef.current.scale.setScalar(currentAperture);
            irisRef.current.rotation.z = t * 0.1;
        }

        // Update Focal Plane (Z = 12)
        if (focalPlaneRef.current) {
            focalPlaneRef.current.position.z = FOCAL_LENGTH;
            focalPlaneRef.current.scale.setScalar(1 + 0.05 * Math.sin(t));
            // Pulse opacity with Clubs waveform
            (focalPlaneRef.current.material as THREE.MeshBasicMaterial).opacity = 0.15 + clubsPulse * 0.15;
        }

        // Update Airy Disk
        if (airyDiskRef.current) {
            airyDiskRef.current.position.z = FOCAL_LENGTH + 0.01;
            // Visual scale for 0.037
            const airyScale = DIFFRACTION_LIMIT * 50; // Scaled up to be visible
            airyDiskRef.current.scale.setScalar(airyScale * (1 + 0.1 * Math.sin(t * 5)));
        }

        // Update Rays
        if (raysRef.current) {
            const positions = raysGeometry.attributes.position.array as Float32Array;

            for (let i = 0; i < RAY_COUNT; i++) {
                const theta = (i / RAY_COUNT) * Math.PI * 2 + (t * 0.2);

                // Start point: Edge of aperture
                positions[i * 6 + 0] = Math.cos(theta) * currentAperture;
                positions[i * 6 + 1] = Math.sin(theta) * currentAperture;
                positions[i * 6 + 2] = 0;

                // End point: focal point at Z=12 (all converge to center)
                positions[i * 6 + 3] = 0;
                positions[i * 6 + 4] = 0;
                positions[i * 6 + 5] = FOCAL_LENGTH;
            }
            raysGeometry.attributes.position.needsUpdate = true;

            // Calculate Faithfulness Metric for color
            // F = 13 / sqrt(n^2 + 12^2)
            const F = 13 / Math.sqrt(n * n + FOCAL_LENGTH * FOCAL_LENGTH);
            const isBolted = Math.abs(F - 1.0) < 0.1;

            const mat = raysRef.current.material as THREE.LineBasicMaterial;
            const targetColor = isBolted ? new THREE.Color('#ffaa00') : new THREE.Color('#44aaff');
            mat.color.lerp(targetColor, 0.1);
            mat.opacity = 0.3 + clubsPulse * 0.3;
        }
    });

    if (!visible) return null;

    return (
        <group ref={meshRef}>
            {/* Aperture Iris (12-sided) */}
            <mesh ref={irisRef} rotation={[0, 0, 0]}>
                <ringGeometry args={[0.9, 1.0, 12]} />
                <meshBasicMaterial color="#2a1040" transparent opacity={0.8} side={THREE.DoubleSide} />
            </mesh>

            {/* Outer Iris bounds (solid umber blocking the rest) */}
            <mesh ref={irisRef}>
                <ringGeometry args={[1.0, 10.0, 32]} />
                <meshBasicMaterial color="#1a0828" transparent opacity={0.6} side={THREE.DoubleSide} />
            </mesh>

            {/* Lens Center (Jordan Slurry visualization is handled in main engine, this is just a subtle marker) */}

            {/* Focal Plane (Z = 12) */}
            <mesh ref={focalPlaneRef}>
                <circleGeometry args={[5, 32]} />
                <meshBasicMaterial color="#00ffff" transparent opacity={0.2} depthWrite={false} side={THREE.DoubleSide} />
            </mesh>

            {/* Airy Disk (Diffraction Limit visualizer) */}
            <mesh ref={airyDiskRef}>
                <circleGeometry args={[1, 32]} />
                <meshBasicMaterial color="#00ffff" transparent opacity={0.8} depthWrite={false} blending={THREE.AdditiveBlending} />
            </mesh>
            <mesh ref={airyDiskRef}>
                <circleGeometry args={[2, 32]} />
                <meshBasicMaterial color="#00ffff" transparent opacity={0.3} depthWrite={false} blending={THREE.AdditiveBlending} />
            </mesh>

            {/* Ray Traces */}
            <lineSegments ref={raysRef} geometry={raysGeometry}>
                <lineBasicMaterial color="#44aaff" transparent opacity={0.4} blending={THREE.AdditiveBlending} />
            </lineSegments>
        </group>
    );
}
