import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Environment, ContactShadows } from '@react-three/drei';
import { InterferenceShaderMesh } from './InterferenceShaderMesh';
import { SimulationParams, ViewMode } from '../types';

interface Props {
  mode: ViewMode;
  params: SimulationParams;
}

export const Scene: React.FC<Props> = ({ mode, params }) => {
  return (
    // Camera positioned at (3, -3, 1.5) to catch the shear lines as per Render Spec
    <Canvas camera={{ position: [3, -3, 1.5], fov: 45 }} dpr={[1, 2]}>
      <color attach="background" args={['#050508']} />

      <Suspense fallback={null}>
        <group>
          <InterferenceShaderMesh mode={mode} params={params} />
        </group>

        <Environment preset="city" />
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

        {/* Render Specification Lighting: Phase III */}
        <ambientLight intensity={0.1} />

        {/* Cold Key (Sun) - Location (5, 5, 5) */}
        <directionalLight
          position={[5, 5, 5]}
          intensity={3.0}
          color="#cce0ff" // Cold Ice Blue
          castShadow
        />

        {/* Cyan Rim (Whisper) - Location (0, 0, 5) */}
        <spotLight
          position={[0, 0, 5]}
          angle={0.6}
          penumbra={0.5}
          intensity={50.0}
          color="#00ffff" // Cyan Whisper
          distance={10}
        />

        {/* Fill Light for depth in cracks */}
        <pointLight
          position={[-3, -3, -2]}
          intensity={0.5}
          color="#003333" // Deep teal in shadows
        />

        {mode === ViewMode.SOLID && (
          <ContactShadows position={[0, -1.8, 0]} opacity={0.6} scale={10} blur={2.5} far={4} color="#00ffff" />
        )}
      </Suspense>

      <OrbitControls autoRotate={false} />
    </Canvas>
  );
};