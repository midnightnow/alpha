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
import { audioEngine } from '../utils/audioEngine';

interface Props {
  mode: ViewMode;
  params: SimulationParams;
}

/**
 * THE PROOF OF REJECTION — GLSL Implementation
 * 
 * This shader contains TWO distinct displacement models:
 * 
 * 1. SMOOTH (√48): Clean sinusoidal interference. No prime decomposition.
 *    The harmonic resolves perfectly — creating a "dead", symmetric solid.
 *    Beat frequency: √48 - √42 ≈ 0.447 Hz (no Hades Gap alignment).
 *
 * 2. FRACTURE (√51): Prime-17 interference. The 17-fold symmetry
 *    introduces irreducible complexity — "Tiger Stripes" that cannot
 *    be smoothed away. Beat frequency: 0.660 Hz (EXACT Hades alignment).
 *
 * The toggle between these states IS the proof that √48 was rejected
 * by the Geometric Sieve, not by aesthetic preference.
 */

const vertexShader = `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vViewPosition;
  varying float vFractureIntensity; // Pass fracture data to fragment
  
  uniform float uInterferenceA;
  uniform float uInterferenceB;
  uniform float uDistortion;
  uniform float uFracture;      // Fracture synthesis toggle
  uniform float uSmooth;        // 0.0 = √51 (Fracture), 1.0 = √48 (Smooth)
  uniform float uTime;
  uniform float uHadesGap;
  uniform float uShearAngle;
  uniform float uPackingConstant;
  uniform float uAudioResonance;

  float hash(float n) { return fract(sin(n) * 43758.5453123); }

  void main() {
    vUv = uv;
    vec3 pos = position;
    
    float r_base = length(pos);
    float theta = atan(pos.y, pos.x);
    float phi = acos(pos.z / max(r_base, 0.0001));

    // === COMMON: Biquadratic Field Equation ===
    float intensity = abs(
      sin(uInterferenceA * theta) * sin(uInterferenceB * phi) +
      sin(uInterferenceB * theta) * sin(uInterferenceA * phi)
    );

    float pulseFreq = (uInterferenceA + uInterferenceB) / 2.0;
    float pulse = sin(pulseFreq * theta) * (uDistortion * (0.5 + uAudioResonance));
    float r = 1.0 + (intensity * uDistortion) + pulse;

    vFractureIntensity = 0.0;

    // === PATH A: SMOOTH (√48) — The Rejected Harmonic ===
    if (uSmooth > 0.5) {
      // √48 = 4√3 — perfectly reducible. Clean divisors.
      // The solid breathes gently but has NO teeth.
      // No prime-17 wave. No shear stress. No fissures.
      
      // Gentle sine breathing only — "The Boring Minor Third"
      float smoothBreathing = sin(uTime * 0.447) * 0.008; // 0.447 Hz = √48 - √42
      r += smoothBreathing;
      
      // Smooth harmonic ripples (no sharp features)
      float smoothRipple = sin(6.0 * theta) * sin(6.0 * phi) * 0.02;
      r += smoothRipple;
    }

    // === PATH B: FRACTURE (√51) — The Prime Intrusion ===
    else if (uFracture > 0.5) {
      // √51 = √(3×17) — irreducible. Prime 17 creates the teeth.
      
      // 17-fold symmetry wave (The "Tiger Stripes")
      float primeWave = sin(17.0 * theta + uShearAngle);
      
      // 51-harmonic whisper (17 × 3 = 51)
      float whisper = sin(51.0 * phi) * uHadesGap * 0.5;

      // Shear stress at the canonical angle
      float shearStress = abs(cos(theta - uShearAngle));
      
      // Fracture threshold: Packing Constant
      if (shearStress > uPackingConstant - 0.1) {
          float fissureDepth = (primeWave > 0.0 ? 0.05 : -0.08) * (1.0 + whisper + uAudioResonance * 2.0);
          r += fissureDepth;
          vFractureIntensity = abs(fissureDepth) * 10.0;
      }
      
      // Hades Gap micro-tremors + breathing at 0.660 Hz
      float breathing = sin(uTime * 0.660 * 6.2832) * 0.005;
      float audioJitter = (hash(theta * 37.0 + phi * 19.0 + uTime) - 0.5) * uAudioResonance * 0.1;
      r += (hash(theta * 13.0 + phi * 7.0 + uTime * 0.1) - 0.5) * uHadesGap * 0.2 + breathing + audioJitter;
    }

    vec3 newPos;
    newPos.x = r * sin(phi) * cos(theta);
    newPos.y = r * sin(phi) * sin(theta);
    newPos.z = r * cos(phi);

    vNormal = normalize(normalMatrix * normal);
    vec4 mvPosition = modelViewMatrix * vec4(newPos, 1.0);
    vViewPosition = -mvPosition.xyz;
    gl_Position = projectionMatrix * mvPosition;
  }
`;

const fragmentShader = `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vViewPosition;
  varying float vFractureIntensity;
  
  uniform vec3 uColorSmooth;    // Ghostly translucent (√48)
  uniform vec3 uColorFracture;  // Obsidian/Cyan (√51)
  uniform vec3 uEmissive;
  uniform float uEmissiveIntensity;
  uniform float uOpacity;
  uniform float uSmooth;
  uniform float uAudioResonance;

  void main() {
    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(vViewPosition);
    
    float rim = 1.0 - max(dot(viewDir, normal), 0.0);
    rim = pow(rim, 3.0);
    
    float resonanceGlow = uAudioResonance * 2.0;
    
    // === SMOOTH: Ghostly, translucent, boring ===
    if (uSmooth > 0.5) {
      // Pale, washed-out appearance — "Clay that fires smooth and silent"
      vec3 ghostColor = uColorSmooth;
      vec3 ghostEmissive = vec3(0.3, 0.3, 0.5); // Faint blue-grey
      vec3 finalColor = ghostColor + (ghostEmissive * 0.15) + (ghostEmissive * rim * 0.5);
      gl_FragColor = vec4(finalColor, 0.6); // Semi-transparent — it's a ghost
    }
    
    // === FRACTURE: Obsidian with cyan fracture lines ===
    else {
      vec3 baseColor = uColorFracture;
      
      // Fracture lines glow hot cyan
      vec3 fractureGlow = vec3(0.0, 1.0, 1.0) * vFractureIntensity;
      
      vec3 finalColor = baseColor 
        + (uEmissive * (uEmissiveIntensity + resonanceGlow)) 
        + (uEmissive * rim * (2.0 + resonanceGlow))
        + fractureGlow;
      
      gl_FragColor = vec4(finalColor, uOpacity);
    }
  }
`;

export const InterferenceShaderMesh = React.forwardRef<THREE.Mesh, Props>(({ mode, params }, ref) => {
  const localRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<THREE.ShaderMaterial>(null);

  React.useImperativeHandle(ref, () => localRef.current as THREE.Mesh);

  const isSmooth = params.harmonicMode === 'smooth';

  const uniforms = useMemo(() => ({
    uInterferenceA: { value: params.interferenceA },
    uInterferenceB: { value: params.interferenceB },
    uDistortion: { value: params.distortion },
    uFracture: { value: params.fracture ? 1.0 : 0.0 },
    uSmooth: { value: isSmooth ? 1.0 : 0.0 },
    uTime: { value: 0 },
    uHadesGap: { value: HADES_GAP },
    uShearAngle: { value: SHEAR_ANGLE_RAD },
    uPackingConstant: { value: PACKING_CONSTANT },
    uAudioResonance: { value: 0 },
    uColorSmooth: { value: new THREE.Color("#b0b8c8") },     // Pale ghost
    uColorFracture: { value: new THREE.Color("#050505") },    // Obsidian
    uEmissive: { value: new THREE.Color("#00ffff") },         // Cyan whisper
    uEmissiveIntensity: { value: 0.3 },
    uOpacity: { value: mode === ViewMode.FIELD ? 0.8 : 1.0 }
  }), [params, mode, isSmooth]);

  useFrame((state, delta) => {
    if (localRef.current) {
      localRef.current.rotation.y += params.rotationSpeed * delta;
      const t = state.clock.elapsedTime;

      // Wobble differs between modes
      const wobbleA = isSmooth ? Math.sqrt(48) : ROOT_51;
      const wobbleB = isSmooth ? Math.sqrt(54) : ROOT_60;
      const wobble = 0.02 * Math.sin(wobbleA * t * 2) + 0.02 * Math.sin(wobbleB * t * 2);
      localRef.current.rotation.z = wobble;
      localRef.current.rotation.x = wobble * 0.5;

      const resonance = audioEngine.getResonance();

      if (materialRef.current) {
        materialRef.current.uniforms.uTime.value = t;
        materialRef.current.uniforms.uInterferenceA.value = params.interferenceA;
        materialRef.current.uniforms.uInterferenceB.value = params.interferenceB;
        materialRef.current.uniforms.uDistortion.value = params.distortion;
        materialRef.current.uniforms.uFracture.value = params.fracture ? 1.0 : 0.0;
        materialRef.current.uniforms.uSmooth.value = isSmooth ? 1.0 : 0.0;
        materialRef.current.uniforms.uAudioResonance.value = resonance;
      }
    }
  });

  return (
    <mesh ref={localRef}>
      <sphereGeometry args={[1, 512, 512]} />
      <shaderMaterial
        ref={materialRef}
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
        transparent={true}
        wireframe={mode === ViewMode.FIELD}
      />
    </mesh>
  );
});
