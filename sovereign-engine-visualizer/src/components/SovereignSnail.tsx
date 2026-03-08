import { useRef, useMemo, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { Cone, Sphere, Float, Html } from '@react-three/drei';
import * as THREE from 'three';
import boltedData from '../data/boltedCoords.json';
import { useSovereignStore } from '../store/useSovereignStore';

// Phase 1: Sovereign Snail (Nautilus-042, Arthur)
export function SovereignSnail() {
    const snailGroupRef = useRef<THREE.Group>(null);
    const shellRef = useRef<THREE.Mesh>(null);
    const trailRef = useRef<THREE.InstancedMesh>(null);
    const { hadesValue } = useSovereignStore();

    const TRAIL_LENGTH = 150;

    // Create a canvas texture for the shell (Text Rendering)
    const canvasTexture = useMemo(() => {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');
        if (ctx) {
            ctx.fillStyle = '#00ffff';
            ctx.fillRect(0, 0, 512, 256);
            ctx.font = 'bold 36px monospace';
            ctx.fillStyle = '#000000';
            ctx.textAlign = 'center';
            ctx.fillText('ROOT 42 RESIDUE', 256, 128);
        }
        const tex = new THREE.CanvasTexture(canvas);
        return tex;
    }, []);

    const updateTextureText = (title: string, veth: string) => {
        const canvas = canvasTexture.image;
        const ctx = canvas.getContext('2d');
        if (ctx) {
            // Background (changes depending on hades value, simulating Europa/Enceladus)
            const isFractured = hadesValue > 0.5;
            ctx.fillStyle = isFractured ? '#1a0033' : '#00ffff'; // Purple if fractured, Cyan if smooth
            ctx.fillRect(0, 0, 512, 256);

            ctx.fillStyle = isFractured ? '#ff00ff' : '#000000';
            ctx.font = 'bold 32px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(title, 256, 100);

            ctx.font = '16px monospace';
            ctx.fillStyle = isFractured ? '#aaaaaa' : '#333333';
            ctx.fillText(veth, 256, 150);

            canvasTexture.needsUpdate = true;
        }
    };

    // Pre-calculate path points from the bolted data
    const pathPoints = useMemo(() => {
        return boltedData.nodes.map(n => new THREE.Vector3(
            n.bolted_coord[0] * 0.2,
            n.bolted_coord[1] * 0.2,
            (n.bolted_coord[2] - 13) * 0.2
        ));
    }, []);

    // Trail state
    const trailCurrentIndex = useRef(0);
    const trailPositions = useMemo(() => new Float32Array(TRAIL_LENGTH * 3), []);
    const dummy = useMemo(() => new THREE.Object3D(), []);

    // Audio heartbeat setup
    const audioCtxRef = useRef<AudioContext | null>(null);
    const lastHeartbeatRef = useRef(0);

    useEffect(() => {
        // Initialize standard web audio for the 6Hz Phantom center heartbeat
        const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
        if (AudioContext) {
            audioCtxRef.current = new AudioContext();
        }
        return () => {
            if (audioCtxRef.current) audioCtxRef.current.close();
        }
    }, []);

    const playHeartbeat = () => {
        if (!audioCtxRef.current || audioCtxRef.current.state !== 'running') return;
        const ctx = audioCtxRef.current;

        const t = ctx.currentTime;

        // Left ear 66Hz
        const oscL = ctx.createOscillator();
        const panL = ctx.createStereoPanner();
        panL.pan.value = -1;
        oscL.frequency.value = 66;

        // Right ear 60Hz
        const oscR = ctx.createOscillator();
        const panR = ctx.createStereoPanner();
        panR.pan.value = 1;
        oscR.frequency.value = 60;

        const gainNode = ctx.createGain();
        gainNode.gain.setValueAtTime(0, t);
        gainNode.gain.linearRampToValueAtTime(0.1, t + 0.1); // Attack
        gainNode.gain.exponentialRampToValueAtTime(0.001, t + 0.5); // Decay

        oscL.connect(panL).connect(gainNode);
        oscR.connect(panR).connect(gainNode);
        gainNode.connect(ctx.destination);

        oscL.start(t);
        oscR.start(t);
        oscL.stop(t + 0.6);
        oscR.stop(t + 0.6);
    };

    useFrame((state) => {
        const t = state.clock.getElapsedTime();

        // 1. Move along the path
        const pathDuration = 5.0; // Seconds per point
        const activeIndex = Math.floor(t / pathDuration) % pathPoints.length;
        const nextIndex = (activeIndex + 1) % pathPoints.length;
        const prog = (t % pathDuration) / pathDuration;

        // Easing for smooth crawling
        const ease = prog < 0.5 ? 2 * prog * prog : -1 + (4 - 2 * prog) * prog;

        const p1 = pathPoints[activeIndex];
        const p2 = pathPoints[nextIndex];

        const currentPos = new THREE.Vector3().lerpVectors(p1, p2, ease);

        if (snailGroupRef.current) {
            snailGroupRef.current.position.copy(currentPos);
            // Look at the next point
            snailGroupRef.current.lookAt(p2);
        }

        // 2. Play heartbeat / breathing at nodes
        if (prog < 0.02 && t - lastHeartbeatRef.current > pathDuration * 0.9) {
            playHeartbeat();
            lastHeartbeatRef.current = t;
            // Update canvas text when we hit a new node
            const node = boltedData.nodes[activeIndex];
            updateTextureText(`NODE ${node.node}`, `[${node.bolted_coord[0].toFixed(2)}, ${node.bolted_coord[1].toFixed(2)}]`);
        }

        // 3. Update Trail
        if (trailRef.current) {
            // Add point every so often
            if (Math.floor(t * 10) % 2 === 0) {
                trailCurrentIndex.current = (trailCurrentIndex.current + 1) % TRAIL_LENGTH;
                const i = trailCurrentIndex.current;
                trailPositions[i * 3] = currentPos.x;
                trailPositions[i * 3 + 1] = currentPos.y;
                trailPositions[i * 3 + 2] = currentPos.z;

                // Root 42 modulation for scale: sin(t * sqrt(42))
                const root42 = 6.480740698;
                const scaleMod = 0.5 + Math.abs(Math.sin(t * root42)) * 0.5;

                dummy.position.copy(currentPos);
                dummy.scale.setScalar(scaleMod * (0.05 + Math.random() * 0.05));
                dummy.updateMatrix();
                trailRef.current.setMatrixAt(i, dummy.matrix);
                trailRef.current.instanceMatrix.needsUpdate = true;
            }
        }

        // 4. Shell State (Europa vs Enceladus vs Vitrified)
        if (shellRef.current) {
            const mat = shellRef.current.material as THREE.MeshPhysicalMaterial;
            if (hadesValue < 0.3) {
                // Europa (Smooth Cyan)
                mat.roughness = 0.1;
                mat.metalness = 0.8;
            } else if (hadesValue > 0.8) {
                // Enceladus (Fractured/Striated)
                mat.roughness = 0.9;
                mat.metalness = 0.2;
            } else {
                // Vitrified
                mat.roughness = 0.4;
                mat.metalness = 0.5;
            }
        }
    });

    return (
        <group>
            {/* ARTHUR THE SNAIL */}
            <group ref={snailGroupRef}>
                <Float speed={5} rotationIntensity={0.2} floatIntensity={0.5}>
                    {/* Shell (Nautilus Logarithmic spiral abstraction in Phase 1: Cone) */}
                    <mesh ref={shellRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, -0.2]}>
                        <coneGeometry args={[0.3, 0.8, 16]} />
                        <meshPhysicalMaterial
                            map={canvasTexture}
                            transparent
                            opacity={0.9}
                            transmission={0.5}
                            thickness={0.5}
                        />
                    </mesh>
                    {/* Head / Eye */}
                    <Sphere args={[0.15, 16, 16]} position={[0, 0, 0.3]}>
                        <meshStandardMaterial color="#8A2BE2" emissive="#4B0082" emissiveIntensity={2} />
                    </Sphere>
                    {/* Label for development */}
                    <Html position={[0, 0.5, 0]} center distanceFactor={10}>
                        <div className="bg-black/80 text-cyan-400 font-mono text-[8px] px-1 border border-cyan-900 shadow-[0_0_8px_rgba(0,255,255,0.5)] whitespace-nowrap">
                            NAUTILUS-042 [ARTHUR]
                        </div>
                    </Html>
                </Float>
            </group>

            {/* DIAMOND DUST TRAIL */}
            <instancedMesh ref={trailRef} args={[undefined, undefined, TRAIL_LENGTH]}>
                <sphereGeometry args={[1, 8, 8]} />
                <meshBasicMaterial color="#ffffff" transparent opacity={0.6} blending={THREE.AdditiveBlending} />
            </instancedMesh>
        </group>
    );
}
