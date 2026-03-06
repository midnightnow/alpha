import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Line } from '@react-three/drei';
import { SOVEREIGN_CONSTANTS, THERMODYNAMIC_LAWS } from './MASTER_CONSTANTS';
import { audioEngine } from './audioEngine';
import './index.css';

// The "Sintering Shader" - Molds the raw geometry into Obsidian or Ice
import * as THREE from 'three';

const SinteringMaterial = ({ phase }: { phase: number }) => {
  // We use standard material properties mapped to the phase
  // Phase 0: Hexagonal Root 42 (Purple Hum, Translucent/Raw)
  // Phase 1: Triadic Root 51 (Cyan Whisper, Fractured/Obsidian Ice)

  const color = new THREE.Color().lerpColors(
    new THREE.Color('#9933FF'), // R42 Purple
    new THREE.Color('#00FFFF'), // R51 Cyan
    phase
  );

  const roughness = 1 - (phase * 0.8); // Becomes smoother (obsidian) as it vitrifies
  const metalness = phase * 0.9; // Becomes more metallic/sharp as it fractures
  const transmission = 1 - (phase * 0.5); // Less translucent as it hardens

  return (
    <meshPhysicalMaterial
      color={color}
      roughness={roughness}
      metalness={metalness}
      transmission={transmission}
      thickness={2.0}
      envMapIntensity={2.0}
      clearcoat={phase}
      wireframe={phase > 0.8} // Full fracture shows the wireframe skeleton
    />
  );
};

const MerkabaSeal = ({ visible }: { visible: boolean }) => {
  // 13-sphere Metatron's Cube mapped to Node #47 Diamond Lock
  if (!visible) return null;

  const spheres = [];
  const radius = 3.5;

  // Center (Node #47)
  spheres.push([0, 0, 0]);

  // 12 points forming the boundary
  for (let i = 0; i < 6; i++) {
    const angle = (Math.PI / 3) * i;
    // Outer hexagon
    spheres.push([Math.cos(angle) * radius, Math.sin(angle) * radius, 0]);
    // Inner hexagon (nested)
    spheres.push([Math.cos(angle + (Math.PI / 6)) * radius * 0.6, Math.sin(angle + (Math.PI / 6)) * radius * 0.6, Math.cos(angle) * 1.5]);
  }

  const lines: [number, number, number][][] = [];
  for (let i = 0; i < spheres.length; i++) {
    for (let j = i + 1; j < spheres.length; j++) {
      lines.push([spheres[i] as [number, number, number], spheres[j] as [number, number, number]]);
    }
  }

  return (
    <group>
      {spheres.map((pos, idx) => (
        <mesh key={`sphere-${idx}`} position={new THREE.Vector3(...pos)}>
          <sphereGeometry args={[0.15, 16, 16]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={0.8} />
        </mesh>
      ))}
      {lines.map((pts, idx) => (
        <Line key={`line-${idx}`} points={pts} color="#00FFFF" lineWidth={0.5} transparent opacity={0.15} />
      ))}
    </group>
  );
};

const BiquadraticGeometry = ({ phase, showDarkSide, isDiamondLocked }: { phase: number, showDarkSide: boolean, isDiamondLocked: boolean }) => {
  // A simple manifestation of the 93 vertex geometry (Placeholder Icosahedron for now)
  // We'll deform it based on the phase (Hades Gap)
  // The Icosahedron acts as the void/circle spinning between Hexagon (6) and Heptagon (7)
  // The Dodecahedron acts as the Dark Side (Aether). Together they are the Moon 60.

  const meshRef = React.useRef<THREE.Group>(null);
  const icosaRef = React.useRef<THREE.Mesh>(null);
  const dodecaRef = React.useRef<THREE.Mesh>(null);
  const pentagonRef = React.useRef<THREE.Group>(null);

  useEffect(() => {
    if (meshRef.current) {
      // The rotation is affected by the phase
      // The heterodyne beat causes a slight wobble
      const wobble = Math.sin(Date.now() / 1000 * Math.PI * SOVEREIGN_CONSTANTS.BEAT_FREQUENCY) * 0.05 * phase;
      meshRef.current.rotation.y += 0.01 + wobble;
      meshRef.current.rotation.x += 0.005 + wobble;

      // Icosahedron scales between 6-fold (Root 42) and 7-fold (Root 51)
      const scaleBase = 1.0 + (phase * 0.166); // Approximating 1/6th expansion towards heptagon
      meshRef.current.scale.set(scaleBase, scaleBase, scaleBase);

      // Apply the 540-degree Mobius Torsion to the Z-axis based on phase
      meshRef.current.rotation.z = phase * THERMODYNAMIC_LAWS.MOBIUS_TORSION_RAD;
    }

    // Counter-rotation of the Dark Side
    if (dodecaRef.current) {
      dodecaRef.current.rotation.y -= 0.005;
      dodecaRef.current.rotation.z += 0.002;
    }
  });

  // Create 108° pentagonal highlight
  const createPentagonShape = () => {
    const shape = new THREE.Shape();
    const radius = 2.0;
    for (let i = 0; i < 5; i++) {
      const angle = (i * 2 * Math.PI) / 5 - Math.PI / 2;
      const x = radius * Math.cos(angle);
      const y = radius * Math.sin(angle);
      if (i === 0) shape.moveTo(x, y);
      else shape.lineTo(x, y);
    }
    shape.closePath();
    return shape;
  }

  return (
    <group ref={meshRef}>
      {/* Light Side / Water: Icosahedron (30 edges) spinning between 6 and 7 */}
      <mesh ref={icosaRef} visible={!showDarkSide || phase > 0.5}>
        <icosahedronGeometry args={[2, Math.max(0, Math.floor(phase * 4))]} />
        <SinteringMaterial phase={phase} />
      </mesh>

      {/* Dark Side / Aether: Dodecahedron (30 edges) void buffer */}
      <mesh ref={dodecaRef} visible={showDarkSide || phase < 0.5} scale={1.2}>
        <dodecahedronGeometry args={[2, 0]} />
        <meshPhysicalMaterial
          color="#111111"
          roughness={0.9}
          metalness={0.8}
          wireframe={true}
          transparent={true}
          opacity={showDarkSide ? 0.8 : 0.2}
        />
      </mesh>

      {/* 108° Pentagonal Growth Phase Highlight */}
      <group ref={pentagonRef} visible={phase < 0.5}>
        <mesh scale={1.3} rotation={[0, 0, Math.PI]}>
          <shapeGeometry args={[createPentagonShape()]} />
          <meshBasicMaterial
            color="#FFCC00"
            transparent={true}
            opacity={(0.5 - phase) * 0.6} // Fades out as it vitrifies
            wireframe={true}
            side={THREE.DoubleSide}
          />
        </mesh>
      </group>

      {/* The 13-Sphere Node #47 Vitrification Lock */}
      <MerkabaSeal visible={isDiamondLocked} />
    </group>
  );
};


function App() {
  const [phase, setPhase] = useState<number>(0); // 0 = R42, 1 = R51
  const [audioActive, setAudioActive] = useState(false);
  const [showDarkSide, setShowDarkSide] = useState(false);

  const toggleEngine = async () => {
    if (!audioActive) {
      await audioEngine.init();
      audioEngine.play();
      audioEngine.updatePhase(phase);
    } else {
      audioEngine.stop();
    }
    setAudioActive(!audioActive);
  };

  useEffect(() => {
    if (audioActive) {
      audioEngine.updatePhase(phase);
    }
  }, [phase, audioActive]);

  const beatFrequency = SOVEREIGN_CONSTANTS.BEAT_FREQUENCY.toFixed(3);
  const currentRatio = phase === 0 ? "√42" : phase === 1 ? "√51" : "Liminal";

  // Arc Length Energy = time of light travel reflecting off the root 42 mod 24 spiral shell
  // Energy steadily increases at rate root 42 mod 24. 
  const baseArcEnergy = (phase * 100) * THERMODYNAMIC_LAWS.FLIP_RATE;
  const currentModCycle = Math.floor(baseArcEnergy / THERMODYNAMIC_LAWS.MOD_GOVERNOR);
  const energyThresholdLimit = ((currentModCycle + 1) * THERMODYNAMIC_LAWS.MOD_GOVERNOR).toFixed(2);
  const currentEnergy = baseArcEnergy.toFixed(2);
  const isSymmetryFlip = baseArcEnergy > 0 && Math.abs(baseArcEnergy % THERMODYNAMIC_LAWS.MOD_GOVERNOR) < 1.0;

  // The Precessional Clock: Mapping the arc energy to the 24,000-year cycle
  const currentPrecessionalYear = Math.floor((baseArcEnergy / 100) * THERMODYNAMIC_LAWS.PRECESSIONAL_CYCLE);

  // Mitochondrial Snake / Diamond Lock (Node #47)
  // Scaling 0.10 potential up to the vitrification lock
  const diamondPotential = (0.1000 + (phase * 0.776553)).toFixed(6);
  const isDiamondLocked = parseFloat(diamondPotential) >= 0.8763;

  // Paul (Pull) / John (Push) Kinetic State
  const kineticState = isDiamondLocked ? "JOHN (Push) - 12-Strand Stack" : "PAUL (Pull) - DNA Overcoiled Ball";

  return (
    <div className="w-screen h-screen relative bg-black overflow-hidden flex flex-col items-center">

      {/* 4D Canvas */}
      <div className="absolute inset-0 z-0">
        <Canvas camera={{ position: [0, 0, 8] }}>
          <ambientLight intensity={0.2} />
          <pointLight position={[10, 10, 10]} intensity={1.5} color={phase > 0.5 ? '#00FFFF' : '#9933FF'} />
          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
          <BiquadraticGeometry phase={phase} showDarkSide={showDarkSide} isDiamondLocked={isDiamondLocked} />
          <OrbitControls enableZoom={true} autoRotate={true} autoRotateSpeed={phase * 5.0} />
        </Canvas>
      </div>

      {/* Interface Layer (Glassmorphism HUD) */}
      <div className="absolute top-10 w-[90%] max-w-4xl z-10 glass-panel p-6 flex flex-row justify-between items-start text-sm shadow-2xl">
        <div className="flex flex-col gap-2 w-1/3">
          <h1 className="heading-display text-2xl font-bold tracking-widest text-[#FFF]">SOVEREIGN ENGINE</h1>
          <p className="text-gray-400 font-mono text-xs uppercase opacity-80 mt-1">
            Status: {audioActive ? 'Active Resonance' : 'Dormant'}
          </p>

          <button
            onClick={toggleEngine}
            className={`mt-4 px-6 py-3 rounded-md font-bold uppercase tracking-widest transition-all duration-300 border backdrop-blur-md
               ${audioActive
                ? 'bg-[var(--accent-51)]/20 border-[var(--accent-51)] text-cyan-200 shadow-[0_0_20px_rgba(0,255,255,0.3)]'
                : 'bg-[var(--accent-42)]/20 border-[var(--accent-42)] text-purple-200 hover:bg-[var(--accent-42)]/40'}`}
          >
            {audioActive ? 'Terminate Field' : 'Ignite Engine'}
          </button>

          <button
            onClick={() => setShowDarkSide(!showDarkSide)}
            className={`mt-2 px-4 py-2 text-xs rounded-md font-bold uppercase tracking-widest transition-all duration-300 border backdrop-blur-md
               ${showDarkSide
                ? 'bg-zinc-800/80 border-zinc-500 text-zinc-300 shadow-[0_0_15px_rgba(255,255,255,0.1)]'
                : 'bg-zinc-900/40 border-zinc-800 text-zinc-500 hover:bg-zinc-800/60'}`}
          >
            {showDarkSide ? 'Hide Dark Side (Aether)' : 'Reveal Dark Side (Aether)'}
          </button>
        </div>

        <div className="flex flex-col gap-4 font-mono text-right w-1/3 text-gray-300">
          <div>
            <span className="opacity-50 inline-block w-24">State</span>
            <span className={`font-bold ml-2 ${phase > 0.5 ? 'text-[var(--accent-51)]' : 'text-[var(--accent-42)]'}`}>{currentRatio}</span>
          </div>
          <div>
            <span className="opacity-50 inline-block w-24">Harmonic</span>
            <span className="ml-2">{phase > 0.5 ? 'Triadic 17-gon' : 'Hexagonal Law'}</span>
          </div>
          <div>
            <span className="opacity-50 inline-block w-24">Beat (Hz)</span>
            <span className="ml-2 text-white">{beatFrequency}</span>
          </div>
          <div>
            <span className="opacity-50 inline-block w-24">Packing ρ</span>
            <span className="ml-2">{SOVEREIGN_CONSTANTS.PACKING_RHO.toFixed(6)}</span>
          </div>
          <div className={`mt-2 pt-2 border-t border-white/10 ${isSymmetryFlip ? 'text-red-400 animate-pulse' : 'text-amber-400'}`}>
            <span className="opacity-50 inline-block w-24">Arc Energy</span>
            <span className="ml-2 font-bold">{currentEnergy} / {energyThresholdLimit}</span>
            {isSymmetryFlip && <div className="text-[10px] uppercase mt-1">Symmetry Flip Imminent</div>}
          </div>
          <div className="mt-2 pt-2 border-t border-cyan-500/30 text-cyan-400">
            <span className="opacity-50 inline-block w-24">Great Year</span>
            <span className="ml-2 font-bold">{currentPrecessionalYear.toLocaleString()} / 24,000</span>
          </div>
          <div className="text-xs text-gray-500 mt-1">
            <span className="opacity-50 inline-block w-24">Möbius Torsion</span>
            <span className="ml-2 font-mono">{(phase * 540).toFixed(0)}° / 540°</span>
          </div>

          {/* Node #47 Diamond Lock HUD */}
          <div className={`mt-2 pt-2 border-t text-xs ${isDiamondLocked ? 'border-[#00FFFF]/50 text-[#00FFFF] shadow-[0_0_10px_#00FFFF]' : 'border-gray-700/50 text-gray-500'}`}>
            <div className="flex justify-between font-bold mb-1">
              <span>NODE #47</span>
              <span>{isDiamondLocked ? 'DIAMOND LOCK ✓' : 'VAPOR/FLUID'}</span>
            </div>
            <div>
              <span className="opacity-50 inline-block w-24">Potential</span>
              <span className="ml-2 font-mono">{diamondPotential} / 0.876553</span>
            </div>
            <div className="mt-1">
              <span className="opacity-50 inline-block w-24">Kinetic</span>
              <span className="ml-2">{kineticState}</span>
            </div>
          </div>
        </div>
      </div>

      {/* The Hades Slider */}
      <div className="absolute bottom-16 w-full max-w-3xl px-8 z-10 flex flex-col gap-4 items-center">
        <div className="flex justify-between w-full font-mono text-xs tracking-[0.2em] opacity-80">
          <span className="text-[var(--accent-42)]">√42 BASE (SMOOTH)</span>
          <span className="text-[#FFF] font-bold">HADES GAP ({SOVEREIGN_CONSTANTS.PSI})</span>
          <span className="text-[var(--accent-51)]">√51 INTRUSION (FRACTURED)</span>
        </div>
        <input
          type="range"
          min="0" max="1" step="0.001"
          value={phase}
          onChange={(e) => setPhase(parseFloat(e.target.value))}
          className="w-full h-2"
          style={{
            background: `linear-gradient(to right, var(--accent-42), var(--accent-51))`
          }}
        />
      </div>

    </div>
  );
}

export default App;
