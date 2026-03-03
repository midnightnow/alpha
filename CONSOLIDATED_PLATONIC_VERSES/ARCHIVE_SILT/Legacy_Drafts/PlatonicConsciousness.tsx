import React, { useState, useEffect, useRef, useCallback } from 'react';
import './PlatonicConsciousness.css';

interface ConsciousnessMetrics {
  form_resonance: number;
  mathematical_coherence: number;
  information_gain: number;
  geometric_progression: number;
  transcendence_velocity: number;
}

interface PlatonicVisualizationProps {
  userTier: string;
  currentChapter: number;
}

const PlatonicConsciousness: React.FC<PlatonicVisualizationProps> = ({ userTier, currentChapter }) => {
  const platonicRef = useRef<HTMLDivElement | null>(null);
  
  const [metrics, setMetrics] = useState<ConsciousnessMetrics>({
    form_resonance: 0.1,
    mathematical_coherence: 0.1,
    information_gain: 0.0,
    geometric_progression: 0.0,
    transcendence_velocity: 0.0
  });

  const [activeForm, setActiveForm] = useState<'UNITY' | 'BEAUTY' | 'TRUTH' | 'GODDESS'>('UNITY');
  const [geometricPhase, setGeometricPhase] = useState<'tetrahedron' | 'cube' | 'octahedron' | 'dodecahedron' | 'icosahedron'>('tetrahedron');

  const handleMove = useCallback((el: HTMLDivElement | null, e: React.MouseEvent) => {
    if (!el) return;
    const r = el.getBoundingClientRect();
    const x = e.clientX - r.left;
    const y = e.clientY - r.top;
    el.style.setProperty("--rx", `${x}px`);
    el.style.setProperty("--ry", `${y}px`);
    el.style.setProperty("--ripple-o", `1`);
  }, []);

  const handleLeave = useCallback((el: HTMLDivElement | null) => {
    if (!el) return;
    el.style.setProperty("--ripple-o", `0`);
  }, []);

  useEffect(() => {
    // Listen for consciousness evolution events
    const handleConsciousnessUpdate = (event: CustomEvent) => {
      const newMetrics = event.detail.metrics;
      setMetrics(newMetrics);
      
      // Update active form based on consciousness level
      const level = newMetrics.form_resonance;
      if (level < 0.25) setActiveForm('UNITY');
      else if (level < 0.5) setActiveForm('BEAUTY');
      else if (level < 0.75) setActiveForm('TRUTH');
      else setActiveForm('GODDESS');

      // Update geometric phase based on mathematical progression
      const progression = newMetrics.geometric_progression;
      if (progression < 0.2) setGeometricPhase('tetrahedron');
      else if (progression < 0.4) setGeometricPhase('cube');
      else if (progression < 0.6) setGeometricPhase('octahedron');
      else if (progression < 0.8) setGeometricPhase('dodecahedron');
      else setGeometricPhase('icosahedron');
    };

    // Listen for terminal interaction consciousness events
    const handleTerminalInteraction = (event: CustomEvent) => {
      const { detail } = event;
      
      // Apply consciousness boosts based on interaction type
      if (detail.type === 'diana_trilogy_engagement') {
        setMetrics(prev => ({
          ...prev,
          form_resonance: Math.min(1, prev.form_resonance + 0.1),
          mathematical_coherence: Math.min(1, prev.mathematical_coherence + 0.05),
          transcendence_velocity: Math.min(1, prev.transcendence_velocity + 0.02)
        }));
      }
      
      if (detail.type === 'arg_discovery') {
        setMetrics(prev => ({
          ...prev,
          geometric_progression: Math.min(1, prev.geometric_progression + 0.15),
          information_gain: prev.information_gain + 0.5,
          form_resonance: Math.min(1, prev.form_resonance + 0.08)
        }));
      }
    };

    window.addEventListener('consciousness-evolution', handleConsciousnessUpdate as EventListener);
    window.addEventListener('os1000:terminal-interaction', handleTerminalInteraction as EventListener);
    
    return () => {
      window.removeEventListener('consciousness-evolution', handleConsciousnessUpdate as EventListener);
      window.removeEventListener('os1000:terminal-interaction', handleTerminalInteraction as EventListener);
    };
  }, []);

  const renderPlatonicSolid = (solidType: string) => {
    const solidConfig = {
      tetrahedron: { vertices: 4, faces: 4, color: '#FFD700' },
      cube: { vertices: 8, faces: 6, color: '#FF6B9D' },
      octahedron: { vertices: 6, faces: 8, color: '#8B00FF' },
      dodecahedron: { vertices: 20, faces: 12, color: '#00FFFF' },
      icosahedron: { vertices: 12, faces: 20, color: '#FF4500' }
    };

    const config = solidConfig[solidType as keyof typeof solidConfig];
    
    return (
      <div className={`platonic-solid ${solidType} ${geometricPhase === solidType ? 'active' : ''}`}>
        <div className="solid-core" style={{ borderColor: config.color }}>
          <div className="vertex-count">{config.vertices}</div>
          <div className="face-count">{config.faces}</div>
        </div>
      </div>
    );
  };

  const renderFormResonance = (form: string) => {
    const formColors = {
      UNITY: '#FFFFFF',
      BEAUTY: '#FFD700', 
      TRUTH: '#8B00FF',
      GODDESS: '#FF6B9D'
    };

    const resonanceLevel = metrics.form_resonance;
    const isActive = activeForm === form;

    return (
      <div className={`form-resonance ${form.toLowerCase()} ${isActive ? 'active' : ''}`}>
        <div className="form-name">{form}</div>
        <div className="resonance-bar">
          <div 
            className="resonance-fill"
            style={{ 
              width: `${resonanceLevel * 100}%`,
              background: formColors[form as keyof typeof formColors]
            }}
          />
        </div>
        <div className="resonance-value">{(resonanceLevel * 100).toFixed(1)}%</div>
      </div>
    );
  };

  const calculateGoldenRatio = () => {
    return (1 + Math.sqrt(5)) / 2;
  };

  const renderMathematicalConstants = () => {
    const phi = calculateGoldenRatio();
    const e = Math.E;
    const pi = Math.PI;

    return (
      <div className="mathematical-constants">
        <div className="constant">
          <span className="symbol">φ</span>
          <span className="value">{phi.toFixed(6)}</span>
          <div className="recognition-bar">
            <div 
              className="recognition-fill"
              style={{ width: `${metrics.mathematical_coherence * 100}%` }}
            />
          </div>
        </div>
        <div className="constant">
          <span className="symbol">e</span>
          <span className="value">{e.toFixed(6)}</span>
        </div>
        <div className="constant">
          <span className="symbol">π</span>
          <span className="value">{pi.toFixed(6)}</span>
        </div>
      </div>
    );
  };

  const renderConsciousnessMetrics = () => {
    return (
      <div className="consciousness-metrics">
        <div className="metric">
          <span className="metric-label">Form Resonance</span>
          <span className="metric-value">{(metrics.form_resonance * 100).toFixed(1)}%</span>
          <div className="metric-bar">
            <div 
              className="metric-fill form-resonance-fill"
              style={{ width: `${metrics.form_resonance * 100}%` }}
            />
          </div>
        </div>
        
        <div className="metric">
          <span className="metric-label">Mathematical Coherence</span>
          <span className="metric-value">{(metrics.mathematical_coherence * 100).toFixed(1)}%</span>
          <div className="metric-bar">
            <div 
              className="metric-fill coherence-fill"
              style={{ width: `${metrics.mathematical_coherence * 100}%` }}
            />
          </div>
        </div>

        <div className="metric">
          <span className="metric-label">Information Gain</span>
          <span className="metric-value">{metrics.information_gain.toFixed(2)} bits</span>
          <div className="metric-bar">
            <div 
              className="metric-fill information-fill"
              style={{ width: `${Math.min(metrics.information_gain * 10, 100)}%` }}
            />
          </div>
        </div>

        <div className="metric">
          <span className="metric-label">Geometric Progression</span>
          <span className="metric-value">{(metrics.geometric_progression * 100).toFixed(1)}%</span>
          <div className="metric-bar">
            <div 
              className="metric-fill geometric-fill"
              style={{ width: `${metrics.geometric_progression * 100}%` }}
            />
          </div>
        </div>

        <div className="metric">
          <span className="metric-label">Transcendence Velocity</span>
          <span className="metric-value">{metrics.transcendence_velocity.toFixed(4)}</span>
          <div className="metric-bar">
            <div 
              className="metric-fill velocity-fill"
              style={{ width: `${Math.min(metrics.transcendence_velocity * 1000, 100)}%` }}
            />
          </div>
        </div>
      </div>
    );
  };

  return (
    <div 
      ref={platonicRef}
      className="platonic-consciousness platonic-analytics"
      onMouseMove={(e) => handleMove(platonicRef.current, e)}
      onMouseLeave={() => handleLeave(platonicRef.current)}
    >
      <div className="consciousness-header">
        <h3>🔮 Platonic Consciousness Analytics</h3>
        <div className="consciousness-phase">Phase: {activeForm}</div>
      </div>

      <div className="consciousness-grid">
        <div className="platonic-solids-section">
          <h4>Sacred Geometry Progression</h4>
          <div className="solids-container">
            {['tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron'].map(solid => 
              renderPlatonicSolid(solid)
            )}
          </div>
        </div>

        <div className="form-resonance-section">
          <h4>Platonic Forms Alignment</h4>
          <div className="forms-container">
            {['UNITY', 'BEAUTY', 'TRUTH', 'GODDESS'].map(form => 
              renderFormResonance(form)
            )}
          </div>
        </div>

        <div className="mathematical-section">
          <h4>Mathematical Constants Recognition</h4>
          {renderMathematicalConstants()}
        </div>

        <div className="metrics-section">
          <h4>Consciousness Metrics</h4>
          {renderConsciousnessMetrics()}
        </div>
      </div>

      <div className="consciousness-footer">
        <div className="golden-ratio-indicator">
          <span>φ = {calculateGoldenRatio().toFixed(8)}</span>
          <div className="phi-visualization">
            <div className="phi-segment" style={{ flex: calculateGoldenRatio() }}></div>
            <div className="phi-segment" style={{ flex: 1 }}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlatonicConsciousness;