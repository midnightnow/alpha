import React, { useMemo, useRef, useEffect } from 'react';
import { useFrame, extend } from '@react-three/fiber';
import * as THREE from 'three';
import { SimulationParams, ViewMode } from '../types';
import { toneEngine } from '../utils/toneEngine';
import { FractureMaterial } from './FractureMaterial';
import { STLExporter } from 'three/examples/jsm/exporters/STLExporter';

// Register the custom material
extend({ FractureMaterial });

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

const createLogoTexture = () => {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d');
  if (ctx) {
    // Transparent background - CLEAN SLATE
    ctx.fillStyle = 'rgba(0,0,0,0)';
    ctx.clearRect(0, 0, 512, 512);

    // --- PROJECTION MAPPING GUIDE (FOR FUTURE TRANSFORMATIONS) ---
    // To project a custom pattern or brand onto the fracture surface:
    // 
    // 1. Load Image:
    //    const img = new Image();
    //    img.src = '/path/to/texture.png'; // Ensure PNG transparency
    //
    // 2. Draw to Canvas (in onload):
    //    ctx.drawImage(img, 0, 0, 512, 512);
    //    tex.needsUpdate = true;
    //
    // 3. Shader Logic:
    //    The FractureMaterial uses 'uLogoTexture' mapped via spherical UVs.
    //    The 'uDistortion' uniform warps this texture with the geometry.
    //
    // 4. Activation:
    //    Set materialRef.current.uHasLogo = 1.0 in the useFrame loop.
  }
  const tex = new THREE.CanvasTexture(canvas);
  return tex;
};

export const InterferenceMesh: React.FC<Props> = ({ mode, params }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<any>(null);

  const logoTex = useMemo(() => createLogoTexture(), []);

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
  }, [params.interferenceA, params.interferenceB, mode === ViewMode.SANDBOX ? 0 : params.distortion, params.fracture]);

  // Materialize (STL Export) Listener
  useEffect(() => {
    const handleExport = () => {
      if (!meshRef.current) return;

      const exporter = new STLExporter();
      const str = exporter.parse(meshRef.current, { binary: true });
      const blob = new Blob([str], { type: 'application/octet-stream' });
      const link = document.createElement('a');
      link.style.display = 'none';
      document.body.appendChild(link);
      link.href = URL.createObjectURL(blob);
      link.download = `radical_resonance_root42_step${params.activeStep !== null ? params.activeStep : 'custom'}.stl`;
      link.click();
      document.body.removeChild(link);
    };

    window.addEventListener('radical-resonance-materialize', handleExport);
    return () => window.removeEventListener('radical-resonance-materialize', handleExport);
  }, [params.activeStep]);

  useFrame((state, delta) => {
    if (meshRef.current) {
      // Base rotation
      meshRef.current.rotation.y += params.rotationSpeed * delta;

      // The Triadic Wobble (The "Shiver")
      const t = state.clock.elapsedTime;
      const wobble =
        0.02 * Math.sin(params.interferenceA * t * 2) +
        0.02 * Math.sin(params.interferenceB * t * 2);

      meshRef.current.rotation.z = wobble;
      meshRef.current.rotation.x = wobble * 0.5;

      // Audio Reactivity for Sandbox Mode
      if (mode === ViewMode.SANDBOX && materialRef.current && toneEngine.analyzer) {
        const values = toneEngine.analyzer.getValue();
        // values is Float32Array of decibels (-100 to 0 usually)
        // We need to map to 0-1

        // Simple 3-band split (very rough approximation from FFT data)
        const lowerBound = 0;
        const midBound = Math.floor(values.length / 3);
        const highBound = Math.floor(2 * values.length / 3);

        const getAvg = (start: number, end: number) => {
          let sum = 0;
          for (let i = start; i < end; i++) {
            sum += (values[i] as number) + 100; // Shift to positive
          }
          return Math.max(0, sum / (end - start)) / 100;
        };

        const low = getAvg(lowerBound, midBound);
        const mid = getAvg(midBound, highBound);
        const high = getAvg(highBound, values.length);

        materialRef.current.uTime = t;
        materialRef.current.uAudioLow = low;
        materialRef.current.uAudioMid = mid;
        materialRef.current.uAudioHigh = high;
        materialRef.current.uDistortion = params.distortion;
        materialRef.current.uFracture = params.fracture ? 1.0 : 0.0;

        // Phase III Resolution Logic (Step 2+)
        const isResolution = params.activeStep !== null && params.activeStep >= 2;
        // Smooth lerp could be done here, but immediate switch is fine for now
        materialRef.current.uResolution = isResolution ? 1.0 : 0.0;

        materialRef.current.uLogoTexture = logoTex;
        materialRef.current.uHasLogo = 0.0; // Set to 1.0 to enable projection logic
      }
    }
  });

  return (
    <mesh ref={meshRef} geometry={geometry} name="InterferenceMesh">
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
        <meshPhysicalMaterial
          color="#e0e7ff"
          roughness={0.15} // Increased roughness for fracture ridges
          metalness={0.2}
          transmission={0.65} // Higher transmission
          thickness={1.5}
          ior={1.45} // Interference Glass IOR
          clearcoat={1}
          flatShading={params.fracture} // Enhance fracture visibility
          emissive="#9933ff" // The "Purple Hum" (0.6, 0.2, 1.0)
          emissiveIntensity={0.2} // Visible glow through cracks
        />
      )}
      {mode === ViewMode.CRYSTAL && (
        <meshNormalMaterial wireframe={false} flatShading={true} />
      )}
      {mode === ViewMode.SANDBOX && (
        // @ts-ignore
        <fractureMaterial
          ref={materialRef}
          transparent={true}
          side={THREE.DoubleSide}
        />
      )}
    </mesh>
  );
};