import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import {
  Icosahedron,
  Octahedron,
  Dodecahedron,
  MeshDistortMaterial,
  Float,
  Points,
  PointMaterial,
  MeshTransmissionMaterial,
  Ring,
  Stars,
  Html,
} from '@react-three/drei';
import * as THREE from 'three';
import { PMG_CONSTANTS, SOVEREIGN_CONSTANTS } from '../MASTER_CONSTANTS';
import { useSovereignStore } from '../store/useSovereignStore';
import { geometricBridge, bridgeDrift, zoomToCascade } from '../fractalBridge';
import { OpticalOverlay } from './OpticalOverlay'; // ADDED
import boltedData from '../data/boltedCoords.json';

// J-Invariant: 1728 * g2^3 / delta ≈ 21778.2
const J_INVARIANT = 21778.2;
const SANTA_VECTOR_LENGTH = Math.sqrt(51); // 7.1414
// Supplementary Archives (Outer Court)
const OUTER_COURT_DOCS = [
  { tick: 276, name: "APPENDIX_C_THE_ASP_PROTOCOL.veth", startColor: "#ff44ff", endColor: "#aa44ff" },
  { tick: 277, name: "CAMERA_OBSCURA_MANUAL.veth", startColor: "#aa44ff", endColor: "#44ffff" },
  { tick: 278, name: "GEOMETRIC_93_MAP.veth", startColor: "#44ffff", endColor: "#ffaa44" },
  { tick: 279, name: "HERO_93_IN_FLIGHT_BALL_ARC.veth", startColor: "#ffaa44", endColor: "#ff44ff" },
  { tick: 280, name: "93_FACED_SOLID_ANALYSIS.veth", startColor: "#ff44ff", endColor: "#ffffff" },
  { tick: 281, name: "288_STEP_DIAGRAM.veth", startColor: "#ffffff", endColor: "#ff44ff" }
];

const DOC_TIERS = {
  PROVEN: { count: 21, color: "#ffd700" }, // Gold
  INTERNAL: { count: 3, color: "#00ffff" }, // Cyan
  INTERPRETIVE: { count: 2, color: "#9370db" } // Purple (Interpretive)
};

// Biquadratic Roots: x^4 - 186x^2 + 81 = 0
const ROOTS = {
  OUTER: 13.622169,
  BEAT: 0.660687
};

const GHOST_PATH_START = 276;
const GHOST_PATH_END = 287;

const clubsWaveform = (week: number) => {
  if (week < 27 || week > 39) return 0;
  const k = week - 27;
  return Math.pow(Math.sin((Math.PI * k) / 12), 2);
};

function getSpherePoints(count: number, radius: number) {
  const pts = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const u = Math.random();
    const v = Math.random();
    const theta = u * 2.0 * Math.PI;
    const phi = Math.acos(2.0 * v - 1.0);
    const r = Math.cbrt(Math.random()) * radius;
    pts[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    pts[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    pts[i * 3 + 2] = r * Math.cos(phi);
  }
  return pts;
}

function getApollonicSnakePoints(count: number) {
  const pts = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const t = (i / count) * Math.PI * 8; // 4 full turns
    const r = 0.5 * Math.exp(0.15 * t); // Logarithmic spiral
    pts[i * 3] = r * Math.cos(t);
    pts[i * 3 + 1] = (i / count) * 6 - 3; // Vertical spread
    pts[i * 3 + 2] = r * Math.sin(t);
  }
  return pts;
}

export function SovereignEngine() {
  const coreRef = useRef<THREE.Mesh>(null);
  const midRef = useRef<THREE.Mesh>(null);
  const membraneRef = useRef<THREE.Mesh>(null);
  const registryRef = useRef<THREE.Group>(null);
  const solidRef = useRef<THREE.Group>(null);
  const snakeRef = useRef<THREE.Group>(null);
  const apertureRef = useRef<THREE.Mesh>(null);
  const lensRef = useRef<THREE.Mesh>(null);
  const bridgeRingRef = useRef<THREE.Mesh>(null);
  const node94Ref = useRef<THREE.Mesh>(null);

  const {
    hadesValue,
    isSimulating,
    currentWeek,
    entropy,
    lockStatus,
    isSealed,
    activeArchive,
    setActiveArchive,
    showMergedStream,
    setShowMergedStream,
    fractalZoom,
    showOpticalOverlay // ADDED
  } = useSovereignStore();

  const emberMatRef = useRef<THREE.PointsMaterial>(null);
  const hadesMatRef = useRef<THREE.PointsMaterial>(null);
  const vertexMatRef = useRef<THREE.PointsMaterial>(null);

  const PHI2 = 2.61803398875;

  // Fractal Position Logic: n^n (Seed) vs (10n)^n (Pomegranate)
  const calculateFractalPosition = (n: number, zoom: number) => {
    // Interpolate base from n to 10n
    const base = n * (1 + 9 * zoom);
    // Use logarithmic scaling to keep values within visual range (0.1 power)
    const magnitude = Math.pow(base, n * 0.1) * (1 + zoom * 5);

    return new THREE.Vector3(
      magnitude * Math.cos(n * PHI2),
      magnitude * Math.sin(n * PHI2),
      0.037 * n // Residual entropy drift
    );
  };

  const GHOST_PATH_LENGTH = 12;

  // 1. Bolted 93-Node Solid from Registry
  const masterGridPts = useMemo(() => {
    const pts = new Float32Array(93 * 3);
    boltedData.nodes.forEach((node, i) => {
      // Normalize from (5,12,13) manifold to visual scale
      pts[i * 3] = node.bolted_coord[0] * 0.2;
      pts[i * 3 + 1] = node.bolted_coord[1] * 0.2;
      pts[i * 3 + 2] = (node.bolted_coord[2] - 13) * 0.2;
    });
    return pts;
  }, []);

  // 2. Registry Ring (288 Ticks)
  const registryPts = useMemo(() => {
    const pts = new Float32Array(288 * 3);
    for (let i = 0; i < 288; i++) {
      const angle = (i / 288) * Math.PI * 2;
      pts[i * 3] = Math.cos(angle) * 4.2;
      pts[i * 3 + 1] = 0;
      pts[i * 3 + 2] = Math.sin(angle) * 4.2;
    }
    return pts;
  }, []);

  const emberPts = useMemo(() => getSpherePoints(42, 0.8), []); // Core Light
  const hadesPts = useMemo(() => getSpherePoints(24, 2.0), []); // Jordan Buffer
  const vertexPts = useMemo(() => getSpherePoints(27, 2.6), []); // Vertex Layer
  const umberPts = useMemo(() => getSpherePoints(156, 3.2), []); // Pulse Field
  const snakePts = useMemo(() => getApollonicSnakePoints(156), []);

  // Keyboard shortcut M for Merged Stream and Wheel for Fractal Zoom
  useMemo(() => {
    if (typeof window === 'undefined') return;
    const handleKey = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'm') setShowMergedStream(!showMergedStream);
    };
    const handleWheel = (e: WheelEvent) => {
      if (Math.abs(e.deltaY) > 0) {
        const delta = e.deltaY * 0.001;
        const newVal = Math.max(0, Math.min(1, useSovereignStore.getState().fractalZoom + delta));
        useSovereignStore.getState().setFractalZoom(newVal);
      }
    };
    window.addEventListener('keydown', handleKey);
    window.addEventListener('wheel', handleWheel, { passive: true });
    return () => {
      window.removeEventListener('keydown', handleKey);
      window.removeEventListener('wheel', handleWheel);
    };
  }, [showMergedStream, setShowMergedStream]);

  // Hexagonal Grid Positions for Pomegranate Clustering
  const clusterOffsets = useMemo(() => {
    const offsets = [];
    const radius = 12;
    for (let q = -2; q <= 2; q++) {
      for (let r = -2; r <= 2; r++) {
        if (Math.abs(q + r) <= 2) {
          if (q === 0 && r === 0) continue; // Skip center (handled by main solid)
          const x = radius * (Math.sqrt(3) * q + Math.sqrt(3) / 2 * r);
          const z = radius * (1.5 * r);
          offsets.push([x, 0, z]);
        }
      }
    }
    return offsets;
  }, []);

  useFrame((state) => {
    const t = state.clock.getElapsedTime();

    // PMG & Sovereign Constants
    const { PHI, ZENITH_WEALTH, ARCS } = SOVEREIGN_CONSTANTS;
    const beat = Math.sin(t * Math.PI * 2 * PMG_CONSTANTS.BEAT);
    const pulse = t * PMG_CONSTANTS.PULSE * (isSimulating ? 1.0 + currentWeek * 0.05 : 1.0);
    const gear = PMG_CONSTANTS.GEAR_LOCK;
    const riemann = -0.083333; // -1/12 Singularity

    // DYNAMIC PALETTE INTERPOLATION
    const palette = SOVEREIGN_CONSTANTS.PALETTE;
    const emberColor = new THREE.Color(palette.UMBER.pulse).lerp(new THREE.Color(palette.WORLD.pulse), fractalZoom);
    const hadesColor = new THREE.Color(palette.UMBER.core).lerp(new THREE.Color(palette.WORLD.core), fractalZoom);
    const vertexColor = new THREE.Color(palette.UMBER.glow).lerp(new THREE.Color(palette.WORLD.glow), fractalZoom);

    if (emberMatRef.current) emberMatRef.current.color.copy(emberColor);
    if (hadesMatRef.current) hadesMatRef.current.color.copy(hadesColor);
    if (vertexMatRef.current) vertexMatRef.current.color.copy(vertexColor);

    // 1. WAVEFORM LOGIC
    let seasonalAmplitude = 0;
    let motorRPM = 1.0;

    if (currentWeek >= ARCS.DIAMONDS.start && currentWeek <= ARCS.DIAMONDS.end) {
      // WEALTH ALGEBRA: W(k) = PHI^(k/6)
      const k = currentWeek - ARCS.DIAMONDS.start;
      seasonalAmplitude = Math.pow(PHI, k / 6);
    } else if (currentWeek >= ARCS.CLUBS.start && currentWeek <= ARCS.CLUBS.end) {
      // MOTORBIKE PHASE: C(k) = PHI^2 * sin^2(pi*k/12)
      const k = currentWeek - ARCS.CLUBS.start;
      seasonalAmplitude = ZENITH_WEALTH * Math.pow(Math.sin((Math.PI * k) / 12), 2);
      motorRPM = 1.0 + (seasonalAmplitude * 2); // Accelerate rotation based on stroke
    }

    // 2. J-INVARIANT RESONANCE (Harmonic 1728)
    // The j-invariant 21778.2 acts as the fundamental resonance.
    const jResonance = Math.abs(Math.sin(t * (J_INVARIANT / 1000))) < 0.1 ? 0 : 1;

    // 3. MOTORBIKE VECTOR (A') IGNITION
    // Transition spark when jumping from Week 26 (Zenith) to 27 (Clubs)
    const isTransitioning = currentWeek === 26 || currentWeek === 27;
    const ignitionSpark = isTransitioning ? Math.abs(Math.sin(t * 20)) * 2 : 0;

    // Rotation Speeds (24:13 Sync)
    const innerRotation = t * (13 / 24) * 0.2;
    const outerRotation = t * (24 / 24) * 0.2;
    const pulseRotation = t * 0.1 * motorRPM;

    // 1. CORE LIGHT (√42)
    if (coreRef.current) {
      const corePulse = 1 + Math.sin(t * 10) * 0.05 + (seasonalAmplitude * 0.1) + ignitionSpark;
      coreRef.current.scale.setScalar(corePulse);
      coreRef.current.position.y = riemann + (Math.sin(t * 2) * 0.1 * jResonance);

      // Hades Sink Logic (Week 10 Transition)
      const coreMat = coreRef.current.material as THREE.MeshBasicMaterial;
      if (coreMat) {
        if (currentWeek >= 10) {
          // Fracture Seal: Core transitions to Translucent Umber
          coreMat.color.lerp(new THREE.Color(palette.UMBER.core), 0.05);
          coreMat.opacity = THREE.MathUtils.lerp(coreMat.opacity, 0.4, 0.05);
        } else {
          // Pre-Week 10: Fractured Obsidian/Cyan
          coreMat.color.lerp(new THREE.Color(hadesValue > 0.5 ? '#1a1a1a' : '#00ffff'), 0.05);
          coreMat.opacity = THREE.MathUtils.lerp(coreMat.opacity, 0.8, 0.05);
        }
      }
    }

    // 2. LOCUST APERTURE (√42 mod 24)
    if (apertureRef.current) {
      apertureRef.current.rotation.z = t * 0.5 * motorRPM;
      apertureRef.current.scale.setScalar(0.5 + Math.abs(beat) * 0.2 + (seasonalAmplitude * 0.05) + (ignitionSpark * 0.5));
    }

    // 3. JORDAN SLURRY LENS (12.37% Buffer) 
    if (lensRef.current) {
      lensRef.current.rotation.y = pulse * 0.001;
      const pulseScale = 2.0 + (Math.sin(t) * 0.1) + (seasonalAmplitude * 0.2);
      lensRef.current.scale.setScalar(pulseScale);
    }

    // 4. RED MEMBRANE (SANTA LAYER - 156-TICK)
    if (membraneRef.current) {
      membraneRef.current.rotation.y = pulseRotation;
      const wobble = Math.sin(t * 15.6) * 0.05 * (1 + ignitionSpark);

      // AMEN_33 Vitrification Pulse (Week 33)
      const isWeek33 = currentWeek === 33;
      const vitrificationForce = isWeek33 ? 3.0 + Math.sin(t * 30) * 0.5 : 1.0;

      const targetScale = 1.5 + wobble + (seasonalAmplitude * 0.1);
      membraneRef.current.scale.setScalar(targetScale);

      const intensity = (0.5 + Math.abs(Math.sin(t * 1.56)) * 0.5 + (seasonalAmplitude * 0.5)) * vitrificationForce * jResonance;
      (membraneRef.current.material as THREE.MeshStandardMaterial).emissiveIntensity = intensity * 3.5 + ignitionSpark;
      (membraneRef.current.material as THREE.MeshStandardMaterial).color.set(isWeek33 ? "#ff3300" : "#ff0000");
    }

    // 5. REGISTRY AND GEAR RINGS (The Matrix of Translation)
    if (registryRef.current) {
      // Outer Gear (24) - Primary Rotation
      registryRef.current.rotation.y = -outerRotation;

      // Matrix of Translation: Using 24 and 13 as eigenvalues for precessional shear
      // theta = t * (Measure + Frequency) / Registry
      const shearAngle = Math.sin(t * (24 + 13) / 288) * 0.05 * seasonalAmplitude;
      registryRef.current.rotation.x = shearAngle;
      registryRef.current.rotation.z = shearAngle * 0.5;

      // Inner Gear (13) - Counter-torque
      if (registryRef.current.children[2]) {
        registryRef.current.children[2].rotation.y = innerRotation;
        registryRef.current.children[2].rotation.x = -shearAngle * 2;
      }
    }

    // 6. 93-NODE SOLID (Categorized Lattice with Vitality Logic)
    if (solidRef.current) {
      // THE LIFE DIAL: Fractal Zoom as a state change
      const n_depth = 0.1 + fractalZoom * 9.9; // Map 0-1 to 0.1-10
      const nPowerN = Math.pow(n_depth, n_depth);
      const lifeFactor = nPowerN * (Math.log(n_depth) + 1); // Derivative: n^n(ln n + 1)

      const baseScale = 1.0 + fractalZoom * 8.0;
      const fractalScale = Math.pow(baseScale, 1.2) * 0.8;

      // APPLY VITALITY THEOREM: Psi_P(d)
      const dissipation = Math.exp(-0.037 * n_depth);
      const psi_vitality = fractalScale * lifeFactor * dissipation * 0.01; // Scale for visual stability

      solidRef.current.scale.setScalar(psi_vitality * (1.0 + (seasonalAmplitude * 0.05)));

      solidRef.current.rotation.y = pulseRotation;
      solidRef.current.position.y = riemann - (fractalZoom * 2);
      solidRef.current.position.z = -fractalZoom * 5;

      // Dynamic FOV & State Change (Seed: High-Detail/Slow | Fruit: Dynamic/Wide)
      const motorStateAdjustment = 1.0 + (fractalZoom * 2.0); // Fruit view is more dynamic
      const cam = state.camera as THREE.PerspectiveCamera;
      if (cam.fov !== undefined) {
        cam.fov = 45 - (fractalZoom * 15);
        cam.updateProjectionMatrix();
      }

      // HIGH-ENTROPY GRIT INPUT (Σ) - Jitter nodes modulated by Life Factor
      if (isSimulating) {
        const hadesJitter = hadesValue * (1 - seasonalAmplitude / ZENITH_WEALTH);
        // Grit is the friction of life
        const grit = (Math.sin(t * 100) * hadesJitter * (1 + fractalZoom));

        solidRef.current.children.forEach((child, i) => {
          // Ember nodes (first 42) pulse with the Awakening Factor
          const awakening = i < 42 ? 1.0 + 0.2 * Math.sin(t * lifeFactor * 0.1) : 1.0;
          child.scale.setScalar(awakening + grit * (i % 5 === 0 ? 1.5 : 1.0));
        });
      }
    }

    // 6b. GENERATIONAL BRIDGE RING (√(93×94) ≈ 93.4986)
    // Mathematical basis: geometric mean as multiplicative midpoint
    // Pell identity: (2n+1)² - 4·n(n+1) = 1 (always exact)
    const GEN = SOVEREIGN_CONSTANTS.GENERATIONAL;
    const cascadeState = zoomToCascade(fractalZoom, GEN.PARENT);
    const bridgeProximity = 1 - Math.abs(fractalZoom - 0.5) * 2; // peaks at zoom=0.5

    // The bridge drift δ_n ≈ 1/(8n) — the "slack in the gears"
    const drift = bridgeDrift(GEN.PARENT); // ≈ 0.00134 for n=93

    if (bridgeRingRef.current) {
      bridgeRingRef.current.rotation.z = t * 0.3;

      // MEAN PULSE SHIMMER: oscillate radius between geometric mean and arithmetic mean
      // Inner boundary: g_93 ≈ 93.49866 (preserves area/information volume)
      // Outer boundary: 93.5 (the arithmetic/perimeter mean)
      // The shimmer width IS the drift (0.00134), amplified for visibility
      const shimmerPhase = Math.sin(t * GEN.OPERATING_TEMP * 170);
      const visualDrift = drift * 200; // Amplify for visibility (0.00134 → 0.268)
      const baseRadius = GEN.BRIDGE * 0.04;
      const currentRadius = baseRadius + shimmerPhase * visualDrift * 0.5;
      bridgeRingRef.current.scale.setScalar(currentRadius / (GEN.BRIDGE * 0.04));

      // Pulse intensifies near the transition zone
      const clubsPulse = clubsWaveform(currentWeek);
      const basePulse = 0.15 + bridgeProximity * 0.4;
      const bridgePulse = basePulse + 0.1 * shimmerPhase + clubsPulse * 0.15;
      (bridgeRingRef.current.material as THREE.MeshBasicMaterial).opacity = Math.min(0.8, bridgePulse);

      // Color shift: Umber (parent) → Cyan (bridge) → Pomegranate (child)
      const phaseColor = cascadeState.phase === 'parent'
        ? new THREE.Color(palette.UMBER.pulse)
        : cascadeState.phase === 'bridge'
          ? new THREE.Color(palette.BRIDGE.core)
          : new THREE.Color(palette.WORLD.pulse);
      const bridgeColor = phaseColor.lerp(
        new THREE.Color(palette.BRIDGE.glow),
        0.5 + 0.5 * Math.sin(t * 2)
      );
      bridgeColor.multiplyScalar(0.6 + bridgeProximity * 0.8);
      (bridgeRingRef.current.material as THREE.MeshBasicMaterial).color.copy(bridgeColor);

      // Altitude spike at the bridge threshold
      bridgeRingRef.current.position.y = bridgeProximity * GEN.DRIFT * 0.5;
    }

    // 6c. NODE 94 INHERITANCE ANIMATION
    if (node94Ref.current) {
      // Emergence progress cycles over 20s, completing in 8s
      const emergenceProgress = isSimulating ? Math.min(1, (t % 20) / 8) : 0;
      // Node 94 visible during transition zone when simulating
      const node94Visible = fractalZoom > 0.3 && isSimulating;
      node94Ref.current.visible = node94Visible;

      if (node94Visible) {
        const bridgeRadius = GEN.BRIDGE * 0.04; // Visual scale mapping
        const approachAngle = t * 0.5;

        // Phase 1 (0-0.5): Approach — spiral inward toward the bridge ring
        // Phase 2 (0.5-0.8): Rotational Reflection — occupy same space as Parent
        // Phase 3 (0.8-1.0): Birth — emerge from center with altitude spike
        const phase = emergenceProgress;

        let radius: number, yPos: number;
        if (phase < 0.5) {
          // Spiraling inward from outer court toward bridge
          radius = bridgeRadius * (2.0 - phase * 3.0);
          yPos = 0;
        } else if (phase < 0.8) {
          // Rotational Reflection: lock to bridge radius, vibrate
          const reflectionIntensity = Math.sin((phase - 0.5) * Math.PI / 0.3);
          radius = bridgeRadius + reflectionIntensity * 0.1 * Math.sin(t * 20);
          yPos = reflectionIntensity * 0.3;
        } else {
          // Birth: emerge upward with altitude spike at g_93
          const birthProgress = (phase - 0.8) / 0.2;
          radius = bridgeRadius * (1 - birthProgress * 0.5);
          // Altitude spike — peak at the geometric mean
          yPos = GEN.DRIFT * birthProgress * 3;
        }

        node94Ref.current.position.set(
          radius * Math.cos(approachAngle),
          yPos,
          radius * Math.sin(approachAngle)
        );

        // Scale: small during approach, grows during birth
        const node94Scale = phase < 0.8
          ? 0.05 + phase * 0.1
          : 0.13 + (phase - 0.8) * 0.5;
        node94Ref.current.scale.setScalar(node94Scale);

        // Opacity builds through all phases
        (node94Ref.current.material as THREE.MeshBasicMaterial).opacity = phase * 0.9;

        // Color: Cyan (approach) → Magenta (reflection) → Pomegranate Red (birth)
        let node94Color: THREE.Color;
        if (phase < 0.5) {
          node94Color = new THREE.Color('#00e5ff');
        } else if (phase < 0.8) {
          node94Color = new THREE.Color('#00e5ff').lerp(new THREE.Color('#ff00ff'), (phase - 0.5) / 0.3);
        } else {
          node94Color = new THREE.Color('#ff00ff').lerp(new THREE.Color('#ff3300'), (phase - 0.8) / 0.2);
        }
        (node94Ref.current.material as THREE.MeshBasicMaterial).color.copy(node94Color);
      }
    }

    if (snakeRef.current) {
      // The Snake acts as the Motorbike Vector (A') - Discharge Effect
      snakeRef.current.rotation.y = -t * 0.2 * motorRPM;
      const ghostSink = t * 0.05 % 5;

      // Background Depth Pomegranate Scaling
      const snakeFractal = 1.0 + fractalZoom * 15.0;
      snakeRef.current.scale.setScalar(snakeFractal * (1.0 + (seasonalAmplitude * 0.2) + ignitionSpark));

      snakeRef.current.position.y = riemann + Math.cos(t * 0.5) - (ghostSink * (1 - jResonance));
      snakeRef.current.position.z = -fractalZoom * 20;

      // Color shift during discharge
      if (snakeRef.current.children[0]) {
        const mat = (snakeRef.current.children[0] as THREE.Points).material as THREE.PointsMaterial;
        if (isTransitioning) {
          mat.color.setHSL(0.5 + Math.sin(t * 10) * 0.1, 1, 0.5); // Oscillate near Cyan
        } else {
          mat.color.set("#10b981");
        }
        mat.opacity = 0.4 + (fractalZoom * 0.4);
      }
    }
  });

  return (
    <group>
      <ambientLight intensity={0.2} />
      <pointLight position={[0, 5, 0]} intensity={1.5} color="#00ffff" />
      <pointLight position={[5, -5, 5]} intensity={1} color="#ff3300" />

      {/* RITUAL APPARATUS STACK */}
      <Float speed={1.56} rotationIntensity={0.5} floatIntensity={0.5}>

        {/* 0. CORE LIGHT (Λ = √42) */}
        <mesh ref={coreRef}>
          <sphereGeometry args={[0.2, 32, 32]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={0.8} />
          <Points positions={emberPts}>
            <PointMaterial transparent color="#ffffff" size={0.15} sizeAttenuation depthWrite={false} blending={THREE.AdditiveBlending} />
          </Points>
        </mesh>

        {/* 1. LOCUST APERTURE (f = 6.48) */}
        <mesh ref={apertureRef} position={[0, 0, 1.3]}>
          <torusGeometry args={[0.5, 0.05, 16, 24]} />
          <meshPhysicalMaterial color="#ffd700" emissive="#ffd700" emissiveIntensity={2} metalness={1} roughness={0} />
        </mesh>

        {/* 2. JORDAN SLURRY LENS (Dielectric Buffer) */}
        <mesh ref={lensRef}>
          <sphereGeometry args={[1.2, 64, 64]} />
          <MeshTransmissionMaterial
            backside
            samples={16}
            thickness={2}
            anisotropy={1}
            chromaticAberration={0.1237}
            distortion={0.5}
            distortionScale={0.5}
            temporalDistortion={0.1}
            color="#0066cc"
          />
        </mesh>

        {/* 3. RED MEMBRANE (SANTA LAYER - 156-TICK) */}
        <mesh ref={membraneRef}>
          <dodecahedronGeometry args={[1.5, 2]} />
          <meshStandardMaterial
            color="#ff0000"
            emissive="#ff0000"
            emissiveIntensity={2}
            wireframe
            transparent
            opacity={0.3}
          />
        </mesh>

        {/* 4. REGISTRY RINGS (24:13 Gear Ratio with 26 Document Markers) */}
        <group ref={registryRef}>
          {/* Outer Ring (24 Sectors) */}
          <Ring args={[3.8, 4.0, 24]} rotation={[Math.PI / 2, 0, 0]}>
            <meshBasicMaterial color="#ffffff" wireframe transparent opacity={0.1} />
          </Ring>

          {/* Ghost Path Buffer Zone (Ticks 276-287) */}
          <Ring args={[4.1, 4.2, 12, 1, (GHOST_PATH_START / 288) * Math.PI * 2, (12 / 288) * Math.PI * 2]} rotation={[Math.PI / 2, 0, 0]}>
            <meshBasicMaterial color="#ff0000" transparent opacity={0.1} />
          </Ring>

          {/* UNIFIED GHOST PATH SPECTRUM (v1.8 Merged Overlay) */}
          {showMergedStream && <MergedGhostTrail currentWeek={currentWeek} activeArchive={activeArchive} />}

          <Points positions={registryPts}>
            <PointMaterial transparent color="#ffd700" size={0.06} sizeAttenuation depthWrite={false} />
          </Points>

          {/* 26 Core Document Canonical Markers (Beatty Mapping - Tier Coded) */}
          {Array.from({ length: 26 }).map((_, n) => {
            const tick = n * 11;
            const angle = (tick / 288) * Math.PI * 2;
            const x = Math.cos(angle) * 4.2;
            const z = Math.sin(angle) * 4.2;
            const isWeek33 = currentWeek === 33;

            // Tier Logic
            let color = DOC_TIERS.PROVEN.color;
            if (n >= 21 && n < 24) color = DOC_TIERS.INTERNAL.color;
            if (n >= 24) color = DOC_TIERS.INTERPRETIVE.color;

            return (
              <mesh key={n} position={[x, 0, z]}>
                <sphereGeometry args={[0.08, 16, 16]} />
                <meshStandardMaterial
                  color={isWeek33 ? "#ffffff" : color}
                  emissive={isWeek33 ? "#ffffff" : color}
                  emissiveIntensity={isWeek33 ? 4 : 2}
                  transparent
                  opacity={0.9}
                />
              </mesh>
            );
          })}

          {/* 6 Supplementary Archive Markers (Outer Court) */}
          {OUTER_COURT_DOCS.map((doc, i) => {
            const angle = (doc.tick / 288) * Math.PI * 2;
            const x = Math.cos(angle) * 4.25;
            const z = Math.sin(angle) * 4.25;
            const isWeek33 = currentWeek === 33;
            const isActive = activeArchive === doc.tick;

            return (
              <group key={`outer-${i}`} position={[x, 0.1, z]}>
                <mesh onClick={(e) => {
                  e.stopPropagation();
                  setActiveArchive(doc.tick);
                }}>
                  <sphereGeometry args={[isActive ? 0.08 : 0.05, 12, 12]} />
                  <meshStandardMaterial
                    color={isActive ? doc.startColor : "#9370db"}
                    emissive={isActive ? doc.startColor : "#9370db"}
                    emissiveIntensity={isActive ? 8 : 2}
                    transparent
                    opacity={0.8}
                  />
                </mesh>
                <Html distanceFactor={10}>
                  <div style={{
                    color: isActive ? doc.startColor : '#9370db',
                    fontSize: '10px',
                    fontWeight: 'bold',
                    fontFamily: 'monospace',
                    padding: '4px',
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: isActive ? `1px solid ${doc.startColor}` : '1px solid rgba(147, 112, 219, 0.3)',
                    borderRadius: '4px',
                    pointerEvents: 'none',
                    whiteSpace: 'nowrap',
                    boxShadow: isActive ? `0 0 10px ${doc.startColor}` : 'none',
                    opacity: activeArchive && !isActive ? 0.3 : 1
                  }}>
                    {doc.name}
                  </div>
                </Html>

                {/* Highlight Trail (Kinetic Trace) */}
                {isActive && (
                  <GhostTrail
                    startTick={doc.tick}
                    startColor={doc.startColor}
                    endColor={doc.endColor}
                    currentWeek={currentWeek}
                  />
                )}
              </group>
            );
          })}

          {/* Inner Gear (13 Ticks) */}
          <Ring args={[2.2, 2.3, 13]} rotation={[Math.PI / 2, 0, 0]}>
            <meshBasicMaterial color="#ffd700" wireframe transparent opacity={0.3} />
          </Ring>
        </group>

        {/* 4.5. 13th GHOST PATH (ANOMALY SINK - VIOLET) */}
        <mesh position={[0, -2.5, 0]} rotation={[0, 0, 0]}>
          <cylinderGeometry args={[0.02, 0.05, 5, 8]} />
          <meshBasicMaterial color="#8A2BE2" transparent opacity={0.4} />
        </mesh>

        {/* 5. 93-NODE SOLID (Categorized Lattice) */}
        <group ref={solidRef}>
          {/* Ember Nodes (42) - Yellow/Pulse */}
          <Points positions={masterGridPts.slice(0, 42 * 3)}>
            <PointMaterial
              ref={emberMatRef}
              transparent
              size={0.15}
              sizeAttenuation
              depthWrite={false}
              blending={THREE.AdditiveBlending}
            />
          </Points>
          {/* Hades Nodes (24) - Red/Core */}
          <Points positions={masterGridPts.slice(42 * 3, 66 * 3)}>
            <PointMaterial
              ref={hadesMatRef}
              transparent
              size={0.18}
              sizeAttenuation
              depthWrite={false}
              blending={THREE.AdditiveBlending}
            />
          </Points>
          {/* Vertex Nodes (27) - Cyan/Glow */}
          <Points positions={masterGridPts.slice(66 * 3, 93 * 3)}>
            <PointMaterial
              ref={vertexMatRef}
              transparent
              size={0.14}
              sizeAttenuation
              depthWrite={false}
              blending={THREE.AdditiveBlending}
            />
          </Points>

          {/* INNER SEED VITRIFICATION (Node 1) - The Life of the Poppy */}
          {fractalZoom < 0.4 && (
            <mesh
              position={[masterGridPts[0], masterGridPts[1], masterGridPts[2]]}
              scale={0.2 * (1 - fractalZoom)}
            >
              <dodecahedronGeometry args={[0.5, 0]} />
              <meshBasicMaterial
                color="#ffffff"
                wireframe
                transparent
                opacity={Math.max(0, 1 - (fractalZoom * 2.5))}
              />
            </mesh>
          )}

          {/* POMEGRANATE CLUSTERS (Systemic Expansion) */}
          {fractalZoom > 0.6 && clusterOffsets.map((pos, idx) => (
            <group key={`cluster-${idx}`} position={pos} scale={fractalZoom * 0.5}>
              <Points positions={masterGridPts}>
                <PointMaterial
                  transparent
                  color={idx % 2 === 0 ? "#ff3300" : "#ffd700"}
                  size={0.05 * fractalZoom}
                  opacity={(fractalZoom - 0.6) * 2}
                />
              </Points>
            </group>
          ))}

          {/* √(93×94) GENERATIONAL BRIDGE RING */}
          <mesh ref={bridgeRingRef} rotation={[Math.PI / 2, 0, 0]}>
            <ringGeometry args={[
              SOVEREIGN_CONSTANTS.GENERATIONAL.BRIDGE * 0.04 - 0.03,
              SOVEREIGN_CONSTANTS.GENERATIONAL.BRIDGE * 0.04 + 0.03,
              64
            ]} />
            <meshBasicMaterial
              color="#00e5ff"
              transparent
              opacity={0.3}
              side={THREE.DoubleSide}
              blending={THREE.AdditiveBlending}
            />
          </mesh>

          {/* NODE 94: THE CHILD (Inheritance Target) */}
          <mesh ref={node94Ref} visible={false}>
            <icosahedronGeometry args={[1, 0]} />
            <meshBasicMaterial
              color="#00e5ff"
              wireframe
              transparent
              opacity={0}
            />
          </mesh>
        </group>

        {/* THE SANTA VECTOR (√51 Tension lines) */}
        <Float speed={2} rotationIntensity={0.1} floatIntensity={0.1}>
          <Icosahedron args={[3.5, 1]}>
            <meshBasicMaterial wireframe color="#10b981" transparent opacity={0.05} />
          </Icosahedron>
        </Float>

        {/* THE GHOST PATH SINK */}
        <group ref={snakeRef}>
          <Points positions={snakePts}>
            <PointMaterial transparent color="#10b981" size={0.06} sizeAttenuation depthWrite={false} opacity={0.4} />
          </Points>
        </group>

      </Float>

      {/* BACKGROUND DEPTH */}
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

      {/* OPTICAL GEOMETRY OF FAITH OVERLAY */}
      <OpticalOverlay visible={showOpticalOverlay} />
    </group>
  );
}

// KINETIC GHOST TRAIL COMPONENT (v1.7 Spectral Enhanced)
function GhostTrail({ startTick, startColor, endColor, currentWeek }: {
  startTick: number,
  startColor: string,
  endColor: string,
  currentWeek: number
}) {
  const pointsRef = useRef<THREE.Points>(null);
  const particleCount = 150;

  const { ZENITH_WEALTH } = SOVEREIGN_CONSTANTS;
  const wave = clubsWaveform(currentWeek);

  const [positions, colors, ticksArray] = useMemo(() => {
    const pos = new Float32Array(particleCount * 3);
    const cols = new Float32Array(particleCount * 3);
    const ticks = new Float32Array(particleCount);

    const c1 = new THREE.Color(startColor);
    const c2 = new THREE.Color(endColor);

    for (let i = 0; i < particleCount; i++) {
      const t = i / particleCount;
      ticks[i] = startTick + (t * 2); // 2-tick segment length
      const angle = (ticks[i] / 288) * Math.PI * 2;
      pos[i * 3] = Math.cos(angle) * 4.25;
      pos[i * 3 + 1] = 0.1;
      pos[i * 3 + 2] = Math.sin(angle) * 4.25;

      const particleColor = c1.clone().lerp(c2, t);
      cols[i * 3] = particleColor.r;
      cols[i * 3 + 1] = particleColor.g;
      cols[i * 3 + 2] = particleColor.b;
    }
    return [pos, cols, ticks];
  }, [startTick, startColor, endColor]);

  useFrame((state) => {
    if (!pointsRef.current) return;
    const t = state.clock.getElapsedTime();
    const posAttr = pointsRef.current.geometry.attributes.position;
    const pos = posAttr.array as Float32Array;

    const segmentLength = 2.0;

    for (let i = 0; i < particleCount; i++) {
      let tick = ticksArray[i];
      tick += 0.015; // Increased Flow speed
      if (tick > startTick + segmentLength) tick = startTick;

      ticksArray[i] = tick;
      const angle = (tick / 288) * Math.PI * 2;
      pos[i * 3] = Math.cos(angle) * 4.25;
      // Vertical oscillation with waveform scaling
      pos[i * 3 + 1] = 0.1 + Math.sin(t * 12 + i * 0.4) * 0.04 * (1 + wave);
      pos[i * 3 + 2] = Math.sin(angle) * 4.25;
    }
    posAttr.needsUpdate = true;
  });

  return (
    <Points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={colors.length / 3}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <PointMaterial
        transparent
        vertexColors // Spectral Gradients enabled
        size={0.07 + (wave * 0.05)}
        sizeAttenuation
        depthWrite={false}
        opacity={0.5 + (wave * 0.4)}
        blending={THREE.AdditiveBlending}
      />
    </Points>
  );
}

// UNIFIED GHOST PATH SPECTRUM (v1.8 Merged)
function MergedGhostTrail({ currentWeek, activeArchive }: { currentWeek: number, activeArchive: number | null }) {
  const pointsRef = useRef<THREE.Points>(null);
  const particleCount = 360;
  const segmentLength = 12; // GHOST_PATH_LENGTH

  const wave = clubsWaveform(currentWeek);
  const { ZENITH_WEALTH } = SOVEREIGN_CONSTANTS;

  const [positions, colors, ticksArray] = useMemo(() => {
    const pos = new Float32Array(particleCount * 3);
    const cols = new Float32Array(particleCount * 3);
    const ticks = new Float32Array(particleCount);

    // Gradient stops for six archives across 12 ticks
    const stops = [
      { tick: 276, color: new THREE.Color("#ff44ff") }, // magenta
      { tick: 278, color: new THREE.Color("#cc33cc") },
      { tick: 280, color: new THREE.Color("#9922ff") },
      { tick: 282, color: new THREE.Color("#6611ff") },
      { tick: 284, color: new THREE.Color("#3300ff") },
      { tick: 286, color: new THREE.Color("#00aaff") }  // cyan
    ];

    for (let i = 0; i < particleCount; i++) {
      const t = (i / particleCount);
      const tick = GHOST_PATH_START + t * segmentLength;
      ticks[i] = tick;

      const angle = (tick / 288) * Math.PI * 2;
      const r = 4.25;
      pos[i * 3] = Math.cos(angle) * r;
      pos[i * 3 + 1] = 0.6 + 0.25 * Math.sin(t * Math.PI * 3);
      pos[i * 3 + 2] = Math.sin(angle) * r;

      // Interpolate color along gradient stops
      let color = new THREE.Color(0xff44ff);
      for (let s = 0; s < stops.length - 1; s++) {
        if (tick >= stops[s].tick && tick < stops[s + 1].tick) {
          const localT = (tick - stops[s].tick) / (stops[s + 1].tick - stops[s].tick);
          color = stops[s].color.clone().lerp(stops[s + 1].color, localT);
          break;
        }
      }
      // Fade tail effect in vertex colors
      color.multiplyScalar(0.3 + 0.7 * (1 - t));

      cols[i * 3] = color.r;
      cols[i * 3 + 1] = color.g;
      cols[i * 3 + 2] = color.b;
    }
    return [pos, cols, ticks];
  }, []);

  useFrame((state) => {
    if (!pointsRef.current) return;
    const t = state.clock.getElapsedTime();
    const posAttr = pointsRef.current.geometry.attributes.position;
    const array = posAttr.array as Float32Array;

    for (let i = 0; i < particleCount; i++) {
      let tick = ticksArray[i];
      tick += 0.012; // flow speed
      if (tick > GHOST_PATH_START + segmentLength) {
        tick = GHOST_PATH_START + (tick - (GHOST_PATH_START + segmentLength));
      }
      ticksArray[i] = tick;

      const angle = (tick / 288) * Math.PI * 2;
      const normalizedT = (tick - GHOST_PATH_START) / segmentLength;
      const r = 4.25;

      array[i * 3] = Math.cos(angle) * r;
      // Continuous Ribbon Oscillation (Waveform + Time displacement)
      array[i * 3 + 1] = 0.6 + 0.25 * Math.sin(normalizedT * Math.PI * 3 + t * 2.0);
      array[i * 3 + 2] = Math.sin(angle) * r;
    }
    posAttr.needsUpdate = true;
  });

  return (
    <Points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={positions.length / 3} array={positions} itemSize={3} />
        <bufferAttribute attach="attributes-color" count={colors.length / 3} array={colors} itemSize={3} />
      </bufferGeometry>
      <PointMaterial
        transparent
        vertexColors
        size={0.12 + (wave * 0.04)}
        sizeAttenuation
        depthWrite={false}
        opacity={activeArchive ? 0.35 : 0.4 + (wave * 0.35)} // Dim when individual isolation active
        blending={THREE.AdditiveBlending}
      />
    </Points>
  );
}
