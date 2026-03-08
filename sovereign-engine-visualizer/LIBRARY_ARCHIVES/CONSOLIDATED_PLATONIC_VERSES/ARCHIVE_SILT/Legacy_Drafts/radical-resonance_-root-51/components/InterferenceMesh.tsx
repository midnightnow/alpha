import React, { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { SimulationParams, ViewMode } from '../types';
import {
  SHEAR_ANGLE_RAD,
  PACKING_CONSTANT,
  HADES_GAP,
  ROOT_51,
  ROOT_60
} from '@platonic/core';

interface Props {
  mode: ViewMode;
  params: SimulationParams;
}

// Function to map sphere coordinates to our interference field
const computeVertex = (theta: number, phi: number, params: SimulationParams) => {
  const { interferenceA, interferenceB, distortion, fracture } = params;

  // The Biquadratic Field Equation visualization
  // F(θ,φ) = |sin(√A·θ)·sin(√B·φ) + sin(√B·θ)·sin(√A·φ)|
  // For Root 51: A=51, B=60

  const intensity = Math.abs(
    Math.sin(interferenceA * theta) * Math.sin(interferenceB * phi) +
    Math.sin(interferenceB * theta) * Math.sin(interferenceA * phi)
  );

  // Radial pulse logic
  const pulseFreq = (interferenceA + interferenceB) / 2;
  const pulse = Math.sin(pulseFreq * theta) * (distortion * 0.5);

  let r = 1 + (intensity * distortion) + pulse;

  // PRIME 17 INTERFERENCE LAYER
  // The signature of the Sibling Resonance (Root 51 = 3 * 17)

  if (fracture) {
    // 17-fold symmetry wave (The "Tiger Stripes")
    const primeWave = Math.sin(17 * theta + SHEAR_ANGLE_RAD);

    // Hades Gap Jitter (The "Whisper") based on Grid
    // We use a high frequency 17*3 = 51 harmonic
    const whisper = Math.sin(51 * phi) * HADES_GAP * 0.5;

    // Apply Shear Stress at the defined angle
    // The "Teeth" appear where the shear aligns with the prime wave
    const shearStress = Math.abs(Math.cos(theta - SHEAR_ANGLE_RAD));

    // Combined Fracture Logic
    // If stress exceeds Packing Constant threshold, we fracture
    if (shearStress > PACKING_CONSTANT - 0.1) {
      // Enceladus-style "Tiger Stripes" (Deep fissures)
      // Modulated by the Prime 17 wave
      const fissureDepth = (primeWave > 0 ? 0.05 : -0.08) * (1 + whisper);
      r += fissureDepth;
    }

    // Micro-tremors (Hades Gap noise)
    r += (Math.random() - 0.5) * HADES_GAP * 0.2;
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
      // Use Root 51/60 basis for the wobble
      const wobble =
        0.02 * Math.sin(ROOT_51 * t * 2) +
        0.02 * Math.sin(ROOT_60 * t * 2);

      localRef.current.rotation.z = wobble;
      localRef.current.rotation.x = wobble * 0.5;
    }
  });

  return (
    <mesh ref={localRef} geometry={geometry}>
      {mode === ViewMode.FIELD && (
        <meshStandardMaterial
          color="#00ffff" // Cyan for Root 51
          wireframe={true}
          emissive="#003333"
          roughness={0.2}
          metalness={0.8}
        />
      )}
      {mode === ViewMode.SOLID && (
        <>
          <meshPhysicalMaterial
            color={params.harmonicMode === 'fracture' ? "#050505" : "#ccfbf1"} // Obsidian vs Ice Cyan
            roughness={params.harmonicMode === 'fracture' ? 0.3 : 0.1} // Rougher for Enceladus ice
            metalness={params.harmonicMode === 'fracture' ? 0.7 : 0.2}
            transmission={params.harmonicMode === 'fracture' ? 0.0 : 0.75}
            thickness={1.5}
            ior={1.31} // Ice IOR
            clearcoat={1}
            flatShading={params.fracture}
            emissive={params.harmonicMode === 'fracture' ? "#ff0000" : "#00ffff"} // Red fracture vs Cyan glow
            emissiveIntensity={params.harmonicMode === 'fracture' ? 0.4 : 0.2}
          />
        </>
      )}
      {mode === ViewMode.CRYSTAL && (
        <meshNormalMaterial wireframe={false} flatShading={true} />
      )}
    </mesh>
  );
});