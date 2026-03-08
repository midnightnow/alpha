/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useRef, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { SovereignEngine } from './components/SovereignEngine';
import { NarrativePanel } from './components/NarrativePanel';
import { InterfaceHUD } from './components/InterfaceHUD';
import { StoryNavigator } from './components/StoryNavigator';
import HyperbolaBridge from './components/HyperbolaBridge';
import GenerationalCascade from './components/GenerationalCascade';

export default function App() {
  const [uploadedVeths, setUploadedVeths] = useState<{ id: string, content: string }[]>([]);
  const [showHyperbola, setShowHyperbola] = useState(false);
  const [showCascade, setShowCascade] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // H key toggles Hyperbola Bridge diagnostic
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement).tagName === 'INPUT') return;
      if (e.key === 'h' || e.key === 'H') {
        setShowHyperbola(prev => !prev);
        setShowCascade(false);
      }
      if (e.key === 'g' || e.key === 'G') {
        setShowCascade(prev => !prev);
        setShowHyperbola(false);
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, []);

  useEffect(() => {
    const filesToLoad = [
      '/COMPLETE_VETH_ARCHIVE.veth',
      '/PMG_MASTER_CANON.veth',
      '/THE_60_FOLD_VECTOR_FIELD.veth',
      '/THE_HIRED_MANS_FIELD_GUIDE.veth',
      '/PLATO_THE_FRACTAL_NAME_ANALYSIS.veth',
      '/DEEP_ONOMATOPOEIA_DICTIONARY.veth',
      '/SANDBOX_WORLD_ARCHITECTURE.veth',
      '/PLATONIC_VERSES_STAGING_PROTOCOL.veth',
      '/SYSTEM_ARCHITECTURE_OLYMPIAN_STANDARD.veth',
      '/THE_60_FOLD_VECTOR_FIELD_VISUALIZER.veth',
      '/GEOMETRICA_THE_MANUS_PROTOCOL.veth',
      '/MANIC_GRAPHIA_THE_MATHEMATICS_OF_MADNESS.veth',
      '/PLATONIC_VERSES_THE_FIRST_DIALOGUE.veth'
    ];

    filesToLoad.forEach(file => {
      fetch(file)
        .then(res => res.text())
        .then(text => {
          if (text && !text.startsWith('<!DOCTYPE')) {
            const idMatch = text.match(/ID:\s*(.+)/);
            const id = idMatch ? idMatch[1].trim() : file.replace('/', '');
            setUploadedVeths(prev => {
              if (prev.some(v => v.id === id)) return prev;
              return [...prev, { id, content: text }];
            });
          }
        })
        .catch(console.error);
    });
  }, []);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files) return;

    Array.from(files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        // Extract ID from the .VETH HEADER if present, otherwise use filename
        const idMatch = text.match(/ID:\s*(.+)/);
        const id = idMatch ? idMatch[1].trim() : file.name;

        setUploadedVeths(prev => {
          // Avoid duplicates by ID
          if (prev.some(v => v.id === id)) return prev;
          return [...prev, { id, content: text }];
        });
      };
      reader.readAsText(file);
    });

    // Reset input so the same files can be uploaded again if needed
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full h-screen bg-black overflow-hidden relative">
      <div className="absolute top-0 left-0 w-full p-6 z-10 pointer-events-none flex justify-between items-start">
        <div>
          <h1 className="text-white font-mono text-xl tracking-widest uppercase opacity-80">Sovereign Engine</h1>
          <p className="text-emerald-400 font-mono text-xs tracking-widest mt-1 opacity-60">PRINCIPIA MATHEMATICA GEOMETRICA</p>
          <p className="text-emerald-600 font-mono text-[10px] tracking-widest mt-2 opacity-50">PMG_SOVEREIGN_v4.2</p>
          <p className="text-emerald-700 font-mono text-[10px] tracking-widest mt-1 opacity-40">STATUS: CANONICAL CRYSTALLIZATION COMPLETE</p>
        </div>
        <div className="text-right">
          <div className="text-white font-mono text-xs opacity-50">PULSE: 156-TICKS</div>
          <div className="text-white font-mono text-xs mt-1 opacity-50">MODULUS: 6.480740698 (SQRT_42)</div>
          <div className="text-white font-mono text-xs mt-1 opacity-50">SKYBOX: 7.141428428 (SQRT_51)</div>
          <div className="text-white font-mono text-xs mt-1 opacity-50">GRID: 93-NODE HYPERDIAMOND</div>
          <div className="text-white font-mono text-xs mt-1 opacity-50">BODY LAW: 10-24-26</div>
          <div className="text-white font-mono text-xs mt-1 opacity-50">HADES GAP: 12.37%</div>
          <div className="text-emerald-500 font-mono text-xs mt-2 opacity-60">OPHANIM: 288 HZ</div>
          <div className="text-emerald-500 font-mono text-xs mt-1 opacity-60">RIEMANN ANCHOR: -1/12</div>
          <div className="text-emerald-500 font-mono text-xs mt-1 opacity-60">TAU RATIO: 1.44</div>
          <div className="text-emerald-500 font-mono text-xs mt-1 opacity-60">SHEAR ANGLE: 39.4°</div>
          <div className="text-emerald-500 font-mono text-xs mt-1 opacity-60">OVERPACK DELTA: 0.000585</div>
          <div className="text-emerald-500 font-mono text-xs mt-1 opacity-60">HARMONIC: 66 HZ</div>
          <div className="text-emerald-500 font-mono text-xs mt-1 opacity-60">MEAN: 46</div>
        </div>
      </div>

      <div className="absolute bottom-6 left-6 z-20">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileUpload}
          accept=".veth,.md,.txt"
          multiple
          className="hidden"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          className="bg-emerald-900/50 hover:bg-emerald-800/80 text-emerald-400 border border-emerald-500/30 px-4 py-2 font-mono text-xs tracking-widest uppercase transition-colors"
        >
          INGEST MASTER ARCHIVE
        </button>
      </div>

      <Canvas camera={{ position: [0, 0, 8], fov: 45 }} gl={{ logarithmicDepthBuffer: true }}>
        <color attach="background" args={['#020202']} />
        <SovereignEngine />
        <OrbitControls
          enablePan={false}
          enableZoom={true}
          minDistance={1}
          maxDistance={100}
        />
      </Canvas>

      <NarrativePanel uploadedVeths={uploadedVeths} />
      <InterfaceHUD />
      <StoryNavigator />

      {/* HYPERBOLA BRIDGE DIAGNOSTIC — Press H to toggle */}
      {showHyperbola && (
        <div style={{
          position: 'fixed', inset: 0, zIndex: 100,
          overflowY: 'auto',
        }}>
          <button
            onClick={() => setShowHyperbola(false)}
            style={{
              position: 'fixed', top: 16, right: 16, zIndex: 101,
              background: 'rgba(0,255,238,0.1)', border: '1px solid #00ffee33',
              color: '#00ffee', padding: '8px 16px', cursor: 'pointer',
              fontFamily: "'Courier New', monospace", fontSize: 10,
              letterSpacing: 2,
            }}
          >
            CLOSE [H]
          </button>
          <HyperbolaBridge />
        </div>
      )}

      {/* GENERATIONAL CASCADE — Press G to toggle */}
      {showCascade && (
        <div style={{
          position: 'fixed', inset: 0, zIndex: 100,
          overflowY: 'auto',
        }}>
          <button
            onClick={() => setShowCascade(false)}
            style={{
              position: 'fixed', top: 16, right: 16, zIndex: 101,
              background: 'rgba(0,255,238,0.1)', border: '1px solid #00ffee33',
              color: '#00ffee', padding: '8px 16px', cursor: 'pointer',
              fontFamily: "'Courier New', monospace", fontSize: 10,
              letterSpacing: 2,
            }}
          >
            CLOSE [G]
          </button>
          <GenerationalCascade />
        </div>
      )}
    </div>
  );
}
