import React, { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { SimulationParams, ViewMode } from '../types';
import { useOracleGrid } from '../utils/useOracleGrid'; // Integrating the SDK Hook

interface Props {
  mode: ViewMode;
  params: SimulationParams;
}

const SHEAR_ANGLE = Math.atan(14 / 17);

// Function to map sphere coordinates to our interference field
const computeVertex = (theta: number, phi: number, params: SimulationParams) => {
  const { interferenceA, interferenceB, distortion, fracture } = params;

  // The Biquadratic Field Equation visualization
  // F(θ,φ) = |sin(√A·θ)·sin(√B·φ) + sin(√B·θ)·sin(√A·φ)|

  const intensity = Math.abs(
    Math.sin(interferenceA * theta) * Math.sin(interferenceB * phi) +
    Math.sin(interferenceB * theta) * Math.sin(interferenceA * phi)
  );

  // Radial pulse logic
  const pulseFreq = (interferenceA + interferenceB) / 2;
  const pulse = Math.sin(pulseFreq * theta) * (distortion * 0.5);

  let r = 1 + (intensity * distortion) + pulse;

  // Fracture Synthesis Logic
  // Apply 14/17 Shear Stress displacement with "Micro-Tremors"
  if (fracture) {
    // Deterministic pseudo-noise for "organic" jaggedness
    // Using high frequency sine waves to simulate random noise
    const microTremor = Math.sin(theta * 100) * Math.sin(phi * 80) * 0.1;

    // 17-fold fracture symmetry
    const stress = Math.abs(Math.sin(17 * theta + SHEAR_ANGLE));

    // Combined stress threshold (Threshold ~0.85)
    // Modulate threshold with noise so cracks aren't perfect lines
    const noisyStress = stress * (1 + microTremor);

    if (noisyStress > 0.85) {
      // Determine if ridge (push out) or crack (pull in)
      // Again, use pseudo-noise to decide direction
      const directionNoise = Math.sin(theta * 50 + phi * 50);
      const direction = directionNoise > 0 ? 1 : -1;

      // Ridge: +0.03, Crack: -0.05 (roughly)
      const magnitude = direction > 0 ? 0.03 : -0.05;

      r += magnitude * stress;
    }
  }

  const x = r * Math.sin(phi) * Math.cos(theta);
  const y = r * Math.sin(phi) * Math.sin(theta);
  const z = r * Math.cos(phi);

  return new THREE.Vector3(x, y, z);
};

export const InterferenceMesh = React.forwardRef<THREE.Mesh, Props>(({ mode, params }, ref) => {
  const localRef = useRef<THREE.Mesh>(null);

  React.useImperativeHandle(ref, () => localRef.current as THREE.Mesh);


  const geometry = useMemo(() => {
    // High resolution sphere to capture the "field" and sharp fracture edges
    const geo = new THREE.SphereGeometry(1, 256, 256);

    const posAttribute = geo.attributes.position;
    const vertex = new THREE.Vector3();

    for (let i = 0; i < posAttribute.count; i++) {
      vertex.fromBufferAttribute(posAttribute, i);
      // Convert to spherical
      const r_base = vertex.length();
      const theta = Math.atan2(vertex.y, vertex.x); // Azimuthal
      const phi = Math.acos(vertex.z / r_base);     // Polar

      const newPos = computeVertex(theta, phi, params);
      posAttribute.setXYZ(i, newPos.x, newPos.y, newPos.z);
    }

    geo.computeVertexNormals();
    return geo;
  }, [params.interferenceA, params.interferenceB, params.distortion, params.fracture]);

  useFrame((state, delta) => {
    if (localRef.current) {
      // Base rotation
      localRef.current.rotation.y += params.rotationSpeed * delta;

      // The Triadic Wobble (The "Shiver")
      const t = state.clock.elapsedTime;
      const wobble =
        0.02 * Math.sin(params.interferenceA * t * 2) +
        0.02 * Math.sin(params.interferenceB * t * 2);

      localRef.current.rotation.z = wobble;
      localRef.current.rotation.x = wobble * 0.5;
    }
  });

  return (
    <mesh ref={localRef} geometry={geometry}>
      {mode === ViewMode.FIELD && (
        <meshStandardMaterial
          color="#4f46e5"
          wireframe={true}
          emissive="#220033"
          roughness={0.2}
          metalness={0.8}
        />
      )}
      {mode === ViewMode.SOLID && (
        <>
          <meshPhysicalMaterial
            color={params.harmonicMode === 'fracture' ? "#0a0a0a" : "#e0e7ff"} // Obsidian Black vs Ice White
            roughness={params.harmonicMode === 'fracture' ? 0.2 : 0.05}
            metalness={params.harmonicMode === 'fracture' ? 0.8 : 0.1}
            transmission={params.harmonicMode === 'fracture' ? 0.0 : 0.65} // Opaque vs Translucent
            thickness={1.5}
            ior={1.45}
            clearcoat={1}
            flatShading={params.fracture}
            emissive={params.harmonicMode === 'fracture' ? "#330000" : "#9933ff"}
            emissiveIntensity={params.harmonicMode === 'fracture' ? 0.5 : 0.2}
          />
          {/* H3 Planetary Lattice Overlay */}
          <mesh visible={params.showGrid}>
            <sphereGeometry args={[1.01, 64, 64]} />
            <meshStandardMaterial
              wireframe
              transparent
              opacity={0.3}
              color="#00ffff"
              emissive="#00ffff"
              emissiveIntensity={0.5}
            />
          </mesh>
        </>
      )}
      {mode === ViewMode.CRYSTAL && (
        <meshNormalMaterial wireframe={false} flatShading={true} />
      )}
    </mesh>
  );
});