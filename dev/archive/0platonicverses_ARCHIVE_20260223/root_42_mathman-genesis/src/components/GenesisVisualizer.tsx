import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { PMG_CONSTANTS } from '../constants';
import { MathmanConsistency, Vertex } from '../lib/MathmanConsistency';

const vertexShader = `
  varying vec2 vUv;
  varying vec3 vPosition;
  varying float vDist;
  
  void main() {
    vUv = uv;
    vPosition = position;
    vDist = length(position);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const fragmentShader = `
  uniform float uTime;
  uniform float uResonance;
  uniform float uHadesGap;
  uniform float uShearAngle;
  uniform float uFocus;
  uniform float uLayerType; // 0: Core, 1: Mantle, 2: Aura, 3: Skeleton
  
  varying vec2 vUv;
  varying vec3 vPosition;
  varying float vDist;

  void main() {
    float dist = vDist;
    float pulse = sin(uTime * 2.0 + dist * uResonance);
    
    // The 5-6-7 Stack Interference (3D)
    float w5 = sin(vPosition.x * 5.0 + vPosition.y * 5.0 + uTime);
    float w6 = sin(vPosition.y * 6.0 + vPosition.z * 6.0 + uTime);
    float w7 = sin(vPosition.z * 7.0 + vPosition.x * 7.0 + uTime);
    float interference = (w5 + w6 + w7) / 3.0;
    
    vec3 color = vec3(0.0);
    float alpha = 0.0;
    
    if (uLayerType < 0.5) {
      // 1. Inner Core (Number: 10)
      float intensity = smoothstep(0.8, 1.0, interference + pulse);
      color = mix(vec3(0.1, 0.4, 0.8), vec3(0.0, 1.0, 1.0), intensity);
      alpha = intensity * 0.8;
    } else if (uLayerType < 1.5) {
      // 2. Mantle (Measure: 24)
      float teeth = abs(sin(vPosition.x * 51.0) * sin(vPosition.y * 51.0));
      float visibility = step(0.95, interference + teeth * 0.2);
      color = vec3(0.5, 0.7, 1.0);
      alpha = visibility * 0.4;
    } else if (uLayerType < 2.5) {
      // 3. Aura (Language: 26)
      float lens = uFocus * (1.1237 - length(vPosition.xy) / 50.0);
      color = vec3(0.0, 0.8, 0.6) * lens;
      alpha = lens * 0.2;
    } else {
      // 4. Primitive Skeleton (12/13 Fractal)
      float grid = abs(sin(vPosition.x * 12.0) * sin(vPosition.y * 13.0) * sin(vPosition.z * 12.0));
      float shine = step(0.98, grid + pulse * 0.1);
      color = vec3(1.0, 0.9, 0.4); // Gold/Spectral Glow
      alpha = shine * (0.6 + 0.4 * sin(uTime * 5.0)); // Rapid Fractal Pulse
    }
    
    // Apply Shear Angle
    float angle = atan(vPosition.y, vPosition.x);
    float shear = cos(angle - radians(uShearAngle));
    alpha *= (0.8 + 0.2 * shear);

    // ─── INTERNAL SHADOW (Light Leakage Logic) ───
    // Stable words (uFocus -> 1.0) contain the light.
    // Entropic words (uFocus -> 0.0) let it leak.
    float leakage = (1.0 - uFocus) * (0.5 + 0.5 * pulse);
    alpha += leakage * 0.15; // The "Glow of Decay"

    gl_FragColor = vec4(color, alpha);
  }
`;

export const GenesisVisualizer: React.FC<{ resonance: number; focus: number }> = ({ resonance, focus }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const validator = useRef(new MathmanConsistency());
  const fractalMode = useRef(false);

  useEffect(() => {
    if (!containerRef.current) return;

    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(75, containerRef.current.clientWidth / containerRef.current.clientHeight, 0.1, 1000);
    camera.position.set(0, 20, 60);
    camera.lookAt(0, 0, 0);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // ─── THE WATTS (PointLight) ───
    const heartLight = new THREE.PointLight(0xff6060, 2, 100);
    heartLight.position.set(0, 0, 0);
    scene.add(heartLight);

    const group = new THREE.Group();
    scene.add(group);

    // ─── THE HEART (vitruvianHeart) ───
    const heartGeometry = new THREE.IcosahedronGeometry(2, 2);
    const heartMaterial = new THREE.MeshBasicMaterial({ color: 0xff4040, wireframe: true });
    const heart = new THREE.Mesh(heartGeometry, heartMaterial);
    scene.add(heart);

    // Create Volumetric Shells (Manifestation Triad: 10-24-26 + 12/13 Primitive)
    const createShell = (radius: number, type: number, detail: number) => {
      const geometry = new THREE.IcosahedronGeometry(radius, detail);
      const material = new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 },
          uResonance: { value: resonance },
          uHadesGap: { value: PMG_CONSTANTS.HADES_GAP },
          uShearAngle: { value: PMG_CONSTANTS.SHEAR_ANGLE },
          uFocus: { value: focus },
          uLayerType: { value: type },
        },
        vertexShader,
        fragmentShader,
        transparent: true,
        side: THREE.DoubleSide,
        depthWrite: false,
      });

      // Register with Validator
      const vertices: Vertex[] = [];
      const posAttr = geometry.getAttribute('position');
      for (let i = 0; i < posAttr.count; i++) {
        vertices.push({
          id: `v_${type}_${i}`,
          coordinates: new THREE.Vector3(posAttr.getX(i), posAttr.getY(i), posAttr.getZ(i)),
          resonance: resonance,
          dimension: 3
        });
      }
      validator.current.vitrifyLayer(type + 1, vertices);

      return new THREE.Mesh(geometry, material);
    };

    const core = createShell(PMG_CONSTANTS.BRACING_TRIAD[0], 0, 3);   // Number (10)
    const mantle = createShell(PMG_CONSTANTS.BRACING_TRIAD[1], 1, 2); // Measure (24)
    const aura = createShell(PMG_CONSTANTS.BRACING_TRIAD[2], 2, 2);   // Language (26)
    const skeleton = createShell(12, 3, 2); // Primitive (12/13)

    group.add(core);
    group.add(mantle);
    group.add(aura);
    group.add(skeleton);

    // Fractal Toggler Listener (F key)
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'f') {
        fractalMode.current = !fractalMode.current;
        console.log(`FRACTAL_MODE: ${fractalMode.current ? 'ENGAGED' : 'DISENGAGED'}`);
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    const animate = (time: number) => {
      const t = time / 1000;
      const phi = PMG_CONSTANTS.PHI;
      const bpm = PMG_CONSTANTS.HEART_FREQUENCY;

      // ─── TRI-AXIAL BRACING (The Golden Ratio Tumble) ───
      // X: Modern Velocity, Y: Elemental Stability, Z: Mythic Depth
      group.rotation.x = t * (0.1 * phi);
      group.rotation.y = t * (0.05 * phi);
      group.rotation.z = t * (0.02 * phi);

      // Heart Pulse
      const pulse = Math.sin(t * bpm);
      heart.scale.setScalar(1 + 0.1 * pulse);
      heartLight.intensity = 2 + pulse;

      group.children.forEach((child, idx) => {
        if (child instanceof THREE.Mesh && child.material instanceof THREE.ShaderMaterial) {
          child.material.uniforms.uTime.value = t;

          // Fractal Toggler Logic: skeleton visibility
          if (idx === 3) {
            child.visible = fractalMode.current || Math.sin(t) > 0.8; // Pulse visibility if not toggled
          }
        }
      });

      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    };

    requestAnimationFrame(animate);

    const handleResize = () => {
      if (!containerRef.current || !cameraRef.current || !rendererRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight;
      cameraRef.current.aspect = w / h;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('keydown', handleKeyDown);
      renderer.dispose();
      if (containerRef.current) containerRef.current.removeChild(renderer.domElement);
    };
  }, []);

  useEffect(() => {
    if (sceneRef.current) {
      sceneRef.current.traverse((child) => {
        if (child instanceof THREE.Mesh && child.material instanceof THREE.ShaderMaterial) {
          child.material.uniforms.uResonance.value = resonance;
          child.material.uniforms.uFocus.value = focus;
        }
      });
    }
  }, [resonance, focus]);

  return <div ref={containerRef} className="w-full h-full" id="canvas-container" />;
};

