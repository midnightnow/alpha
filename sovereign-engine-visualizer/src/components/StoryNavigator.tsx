import React from 'react';
import { useSovereignStore } from '../store/useSovereignStore';

export const StoryNavigator = () => {
    const { fractalZoom, setFractalZoom } = useSovereignStore();

    const modes = [
        { label: 'SEED (√10)', value: 0.0, description: 'Concentrated Potential' },
        { label: 'AWAKENING', value: 0.5, description: 'nⁿ(ln n + 1) Pulse' },
        { label: 'WORLD (10)', value: 1.0, description: 'The Flower Manifest' }
    ];

    return (
        <div style={{
            position: 'fixed',
            bottom: '80px',
            left: '50%',
            transform: 'translateX(-50%)',
            display: 'flex',
            gap: '10px',
            zIndex: 1000,
            pointerEvents: 'auto'
        }}>
            {modes.map((mode) => (
                <button
                    key={mode.label}
                    onClick={() => setFractalZoom(mode.value)}
                    style={{
                        background: fractalZoom === mode.value ? 'rgba(255, 215, 0, 0.2)' : 'rgba(0, 0, 0, 0.6)',
                        border: fractalZoom === mode.value ? '1px solid #ffd700' : '1px solid #10b981',
                        color: fractalZoom === mode.value ? '#ffd700' : '#10b981',
                        padding: '10px 20px',
                        fontFamily: 'monospace',
                        fontSize: '0.75rem',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        minWidth: '120px',
                        backdropFilter: 'blur(5px)',
                        boxShadow: fractalZoom === mode.value ? '0 0 15px rgba(255, 215, 0, 0.3)' : 'none'
                    }}
                >
                    <span style={{ fontWeight: 'bold', marginBottom: '4px' }}>{mode.label}</span>
                    <span style={{ fontSize: '0.6rem', opacity: 0.7 }}>{mode.description}</span>
                </button>
            ))}
        </div>
    );
};
