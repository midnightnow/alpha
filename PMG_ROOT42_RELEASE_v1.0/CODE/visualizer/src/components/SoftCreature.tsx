import React, { useEffect, useRef, useState, useMemo } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { PivotValidator } from './PivotValidator';

// Torsion Constants
const RADIUS_INNER = 1.0;
const RADIUS_OUTER = 2.5;
const NEURAL_FOLD_ANGLE = 39.4 * (Math.PI / 180);

interface SimulationMetrics {
  pivot: number;
  shellBoundary: number;
  currentEntropy: number;
  maxRadialDrift: number;
  isPhaseLocked: boolean;
  torsion: number;
  shearAngle: number;
  overpackDelta: number;
}

export const SoftCreature: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [metrics, setMetrics] = useState<SimulationMetrics | null>(null);
  const [points, setPoints] = useState<{ x: number, y: number, z: number, layer: string }[]>([]);
  const [highlightNode, setHighlightNode] = useState<{ index: number, timestamp: number }>({ index: -1, timestamp: 0 });

  // Three.js refs
  const sceneRef = useRef<THREE.Scene | null>(null);
  const meshRef = useRef<THREE.InstancedMesh | null>(null);
  const coreRef = useRef<THREE.Mesh | null>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  // 1. Load Anatomy (93 Points)
  useEffect(() => {
    fetch('http://127.0.0.1:8975/data/05_anatomy_relative.csv')
      .then(res => res.text())
      .then(csv => {
        const lines = csv.trim().split('\n').slice(1);
        const parsed = lines.map(line => {
          const [x, y, z] = line.split(',').map(Number);
          const r = Math.sqrt(x * x + y * y + z * z);
          let layer = 'shell';
          if (r < 0.2) layer = 'core';
          else if (r < 1.1) layer = 'seed';
          return { x, y, z, layer };
        });
        setPoints(parsed);
      });
  }, []);

  // 1.5 Geometry Sync listener
  useEffect(() => {
    const handleLatticeLetter = (e: any) => {
      const { nodeIndex, timestamp } = e.detail;
      if (nodeIndex >= 0 && nodeIndex < 93) {
        setHighlightNode({ index: nodeIndex, timestamp });
      }
    };
    window.addEventListener('lattice:letter' as any, handleLatticeLetter);
    return () => window.removeEventListener('lattice:letter' as any, handleLatticeLetter);
  }, []);

  // 2. WebSocket Stream (The Möbius Pulse)
  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8975/ws');
    ws.onmessage = (event) => setMetrics(JSON.parse(event.data));
    return () => ws.close();
  }, []);

  // 3. Scene Setup
  useEffect(() => {
    if (!containerRef.current) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(8, 5, 8);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    containerRef.current.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // The "Black Ball" (Singularity/Gastrula Core)
    const coreGeom = new THREE.SphereGeometry(0.5, 32, 32);
    const coreMat = new THREE.MeshStandardMaterial({
      color: 0x000000,
      roughness: 0,
      metalness: 1,
      emissive: 0x110022,
      emissiveIntensity: 0.5
    });
    const core = new THREE.Mesh(coreGeom, coreMat);
    scene.add(core);
    coreRef.current = core;

    // Instanced Points (The 93-Faced Interference Solid)
    const pointGeom = new THREE.SphereGeometry(0.08, 12, 12);
    const pointMat = new THREE.MeshPhongMaterial({ shininess: 100 });
    const mesh = new THREE.InstancedMesh(pointGeom, pointMat, 100); // 93 + padding
    scene.add(mesh);
    meshRef.current = mesh;

    // Ambient Lighting
    scene.add(new THREE.AmbientLight(0x404040, 2));
    const pointLight = new THREE.PointLight(0x9933ff, 50, 20);
    pointLight.position.set(2, 5, 2);
    scene.add(pointLight);

    sceneRef.current = scene;

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
    };
  }, []);

  // 4. Neurulation Morph (The Rolling and Twisting)
  useEffect(() => {
    if (!meshRef.current || !points.length || !metrics) return;

    const { torsion, overpackDelta } = metrics;
    // Morph Factor: how much of the "sphere" has rolled into the "tube"
    const morph = Math.min(torsion / 540, 1.0);

    points.forEach((p, i) => {
      // 1. Start with the original spherical coordinates
      let targetX = p.x;
      let targetY = p.y;
      let targetZ = p.z;

      // 2. The Next Right Move (Invagination Transform)
      if (morph > 0) {
        // Shift 1: The Radial Fold (90-deg)
        // Transitions the flat shell lattice to a hemicylindrical fold
        const foldAngle = (p.y / metrics.shellBoundary) * (Math.PI / 2) * morph;
        const radius1 = THREE.MathUtils.lerp(p.x, Math.cos(foldAngle) * RADIUS_OUTER, morph);

        // Shift 2: The Phase-Flip Bury (180-deg total)
        // This is the literal 'burying of the positive in the negative'
        const buryPhase = (p.z / metrics.shellBoundary) * (Math.PI / 2) * morph;
        const finalY = Math.sin(foldAngle) * RADIUS_OUTER * (1 - morph * 0.7); // Sucking inward
        const finalZ = p.z - (Math.cos(buryPhase) * RADIUS_INNER * morph);

        targetX = radius1;
        targetY = finalY;
        targetZ = finalZ;

        // 3. Sovereign Rotation (Symmetry Breaking)
        // Using the 'torsion' metric as a pure rotation parameter
        const rotAngle = (metrics.torsion * Math.PI / 180);
        const cosR = Math.cos(rotAngle);
        const sinR = Math.sin(rotAngle);

        const tx = targetX * cosR - targetY * sinR;
        const ty = targetX * sinR + targetY * cosR;
        targetX = tx;
        targetY = ty;
      }

      dummy.position.set(targetX, targetY, targetZ);

      // 4. Color and Scale (The Structural Shockwave)
      const isHighlighted = i === highlightNode.index && (Date.now() - highlightNode.timestamp < 300);

      // Update Scale
      let scale = 0.8 + Math.sin(Date.now() * 0.01 + i) * overpackDelta * 10;
      if (isHighlighted) scale *= 2.5;
      dummy.scale.set(scale, scale, scale);

      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);

      // Update Color
      let color = new THREE.Color(isHighlighted ? 0xffaa00 : 0xf43f5e); // Shell (Rose-500)
      if (!isHighlighted) {
        if (p.layer === 'core') color = new THREE.Color(0x333333); // Core (Dark)
        if (p.layer === 'seed') color = new THREE.Color(0xffffff); // Seed (Bright)

        if (!metrics.isPhaseLocked) {
          color.lerp(new THREE.Color(0x000000), 0.5); // Fade in Hades Gap
        }

        // As it twists, colors "bleed" (Neural fusion)
        if (morph > 0.5) {
          color.lerp(new THREE.Color(0x9d174d), morph - 0.5); // Deep Rose
        }
      }
      meshRef.current!.setColorAt(i, color);
    });

    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) meshRef.current.instanceColor.needsUpdate = true;

    // Swallowing the Black Ball (Core reacts to the fold)
    if (coreRef.current) {
      coreRef.current.scale.set(1 - morph * 0.5, 1 - morph * 0.5, 1 - morph * 0.5);
      coreRef.current.material.emissiveIntensity = 0.5 + morph * 2;
    }

  }, [metrics, points, highlightNode]);

  return (
    <div ref={containerRef} className="w-full h-full relative overflow-hidden bg-black">
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_center,_transparent_0%,_black_90%)]" />
      <PivotValidator />
    </div>
  );
};
