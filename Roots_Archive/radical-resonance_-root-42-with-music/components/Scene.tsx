import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Environment, ContactShadows } from '@react-three/drei';
import { InterferenceMesh } from './InterferenceMesh';
import { InSceneHUD } from './InSceneHUD';
import { SimulationParams, ViewMode } from '../types';

interface Props {
  mode: ViewMode;
  params: SimulationParams;
}

export const Scene: React.FC<Props> = ({ mode, params }) => {
  return (
    // Camera positioned at (3, -3, 1.5) to catch the shear lines as per Render Spec
    <Canvas 
        camera={{ position: [3, -3, 1.5], fov: 45 }} 
        dpr={[1, 2]}
        gl={{ preserveDrawingBuffer: true }}
    >
      <color attach="background" args={['#050508']} />
      
      <Suspense fallback={null}>
        <group>
            <InterferenceMesh mode={mode} params={params} />
        </group>
        
        <Environment preset="city" />
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
        
        {/* Render Specification Lighting: Phase II */}
        <ambientLight intensity={0.1} />
        
        {/* Cold Key (Sun) - Location (5, 5, 5) */}
        <directionalLight 
            position={[5, 5, 5]} 
            intensity={3.0} 
            color="#cce0ff" // Cold Ice Blue (0.8, 0.9, 1.0)
            castShadow
        />
        
        {/* Purple Rim (Hum) - Location (0, 0, 5) approx top/back */}
        <spotLight 
            position={[0, 0, 5]} 
            angle={0.6} 
            penumbra={0.5} 
            intensity={50.0} 
            color="#9933ff" // Purple Hum (0.6, 0.2, 1.0)
            distance={10}
        />
        
        {/* Fill Light for depth in cracks */}
        <pointLight 
            position={[-3, -3, -2]} 
            intensity={0.5} 
            color="#fbbf24" // Warmth in the shadows
        />
        
        {(mode === ViewMode.SOLID || mode === ViewMode.SANDBOX) && (
             <ContactShadows position={[0, -1.8, 0]} opacity={0.6} scale={10} blur={2.5} far={4} color="#9933ff" />
        )}

        {/* In-Scene HUD for Recording - Wrapped in Suspense to avoid blocking main scene */}
        <Suspense fallback={null}>
            <InSceneHUD params={params} visible={mode === ViewMode.SANDBOX} />
        </Suspense>

      </Suspense>
      
      <OrbitControls autoRotate={false} />
    </Canvas>
  );
};