import React, { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Float, Stars, Text, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';
import { calculateHullData } from '../math/geometry';

interface Props {
  points: number[][];
  epsilon: number;
}

const LatticeModel: React.FC<{ points: number[][] }> = ({ points }) => {
  const { facets } = useMemo(() => calculateHullData(points), [points]);

  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    const vertices = new Float32Array(facets.length * 3 * 3);
    
    facets.forEach((facet, i) => {
      const p1 = points[facet[0]];
      const p2 = points[facet[1]];
      const p3 = points[facet[2]];
      
      const idx = i * 9;
      vertices[idx] = p1[0] - 13; // Center around s=13
      vertices[idx+1] = p1[1];
      vertices[idx+2] = p1[2];
      
      vertices[idx+3] = p2[0] - 13;
      vertices[idx+4] = p2[1];
      vertices[idx+5] = p2[2];
      
      vertices[idx+6] = p3[0] - 13;
      vertices[idx+7] = p3[1];
      vertices[idx+8] = p3[2];
    });
    
    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    geo.computeVertexNormals();
    return geo;
  }, [points, facets]);

  return (
    <group>
      {/* The Shell (Hull) */}
      <mesh geometry={geometry}>
        <meshPhongMaterial 
          color="#10b981" 
          transparent 
          opacity={0.15} 
          side={THREE.DoubleSide}
          wireframe={false}
          shininess={100}
        />
      </mesh>
      
      {/* The Wireframe */}
      <mesh geometry={geometry}>
        <meshBasicMaterial 
          color="#10b981" 
          wireframe 
          transparent 
          opacity={0.1} 
        />
      </mesh>

      {/* The Net (Nodes) */}
      {points.map((p, i) => (
        <mesh key={i} position={[p[0] - 13, p[1], p[2]]}>
          <sphereGeometry args={[0.15, 8, 8]} />
          <meshStandardMaterial 
            color={i < 26 ? "#10b981" : "#ffffff"} 
            emissive={i < 26 ? "#10b981" : "#ffffff"}
            emissiveIntensity={0.5}
          />
        </mesh>
      ))}
    </group>
  );
};

const Lattice3D: React.FC<Props> = ({ points, epsilon }) => {
  return (
    <div className="w-full h-[500px] bg-[#050505] rounded-2xl border border-white/5 overflow-hidden relative shadow-2xl">
      <div className="absolute top-6 left-6 z-10 pointer-events-none">
        <div className="text-[10px] font-mono text-emerald-500 uppercase tracking-[0.2em] mb-2">3D Manifold Projection</div>
        <h3 className="text-xl font-medium text-white tracking-tight">The HERO 93 Solid</h3>
        <div className="flex items-center gap-2 mt-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-[10px] font-mono text-white/40 uppercase tracking-widest">Attractor State ε = {epsilon.toFixed(8)}</span>
        </div>
      </div>

      <div className="absolute bottom-6 right-6 z-10 pointer-events-none text-right">
        <div className="text-[10px] font-mono text-white/20 uppercase tracking-widest mb-1">Invariant Target</div>
        <div className="text-3xl font-mono text-emerald-500 font-bold">42.000</div>
      </div>

      <Canvas shadows dpr={[1, 2]}>
        <PerspectiveCamera makeDefault position={[25, 15, 25]} fov={35} />
        <OrbitControls 
          enablePan={false} 
          autoRotate 
          autoRotateSpeed={0.5} 
          maxDistance={60} 
          minDistance={10}
        />
        
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
        
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#10b981" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#ffffff" />
        <spotLight position={[0, 20, 0]} angle={0.3} penumbra={1} intensity={2} castShadow />

        <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
          <LatticeModel points={points} />
        </Float>

        {/* Ground Plane Reflection (Subtle) */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -10, 0]}>
          <planeGeometry args={[100, 100]} />
          <MeshDistortMaterial
            transparent
            opacity={0.05}
            color="#10b981"
            distort={0.1}
            speed={2}
          />
        </mesh>
      </Canvas>
    </div>
  );
};

export default Lattice3D;
