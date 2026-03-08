import React from 'react';
import { useSovereignStore } from '../store/useSovereignStore';
import { audioEngine } from '../audioEngine';

export const InterfaceHUD = () => {
    const {
        hadesValue,
        setHadesValue,
        currentWeek,
        isSimulating,
        startSimulation,
        nextWeek,
        arc,
        amplitude,
        entropy,
        lockStatus,
        isSealed,
        jumpToZenith,
        showMergedStream,
        setShowMergedStream,
        ingestPayload,
        fractalZoom,
        setFractalZoom,
        seedResonance,
        worldResonance,
        showOpticalOverlay, // ADDED
        setShowOpticalOverlay // ADDED
    } = useSovereignStore();

    const isFractured = hadesValue > 0.5;

    const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = parseFloat(e.target.value);
        setHadesValue(val);
        audioEngine.start();
        audioEngine.updateFracture(val, currentWeek);
    };

    const handleStartSim = () => {
        audioEngine.start();
        startSimulation();
        audioEngine.updateFracture(hadesValue, 14);
    };

    const handleNextWeek = () => {
        nextWeek();
        const targetWeek = currentWeek < 52 ? currentWeek + 1 : 1;
        audioEngine.updateFracture(hadesValue, targetWeek);
    };

    const handleJumpToZenith = () => {
        audioEngine.start();
        jumpToZenith();
        audioEngine.updateFracture(hadesValue, 26);
    };

    const handleIngest = async () => {
        try {
            const response = await fetch('/src/data/sample_payload.veth.json');
            const data = await response.json();
            ingestPayload(data);
            audioEngine.start();
        } catch (error) {
            console.error("Ingestion error:", error);
        }
    };

    const isZenith = currentWeek === 26 && arc === 'DIAMONDS';

    // UMBER FOCUS CALCULATION
    const n_val = 93 + fractalZoom * 10;
    const gn_val = Math.sqrt(n_val * (n_val + 1));
    const delta_n = (n_val + 0.5) - gn_val;
    // Focus = 1 - | δn - 0.037 | / 0.037
    const focusMetric = Math.max(0, 1 - Math.abs(delta_n - 0.037) / 0.037);

    const getArcLabel = () => {
        if (arc === 'DIAMONDS') return "DIAMONDS: WEALTH ALGEBRA";
        if (arc === 'CLUBS') return "CLUBS: MOTORBIKE PHASE";
        return "STANDBY";
    };

    return (
        <>
            {/* DFA METRICS OVERLAY (Right Side) */}
            <div style={{
                position: 'fixed',
                top: '20px',
                right: '20px',
                padding: '15px',
                backgroundColor: 'rgba(0, 0, 0, 0.85)',
                border: '1px solid #10b981',
                borderRadius: '5px',
                color: '#10b981',
                fontFamily: 'monospace',
                fontSize: '14px',
                zIndex: 1000,
                pointerEvents: 'none',
                boxShadow: '0 0 15px rgba(16, 185, 129, 0.3)',
                width: '240px'
            }}>
                <div style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '10px', borderBottom: '1px solid #10b981', color: isSealed ? '#ffd700' : '#10b981' }}>
                    ENGINE: {isSealed ? "VITRIFIED" : "CALIBRATING"}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '8px' }}>
                    <span>Σ ENTROPY:</span> <span style={{ color: '#ff4400' }}>{entropy.toFixed(2)}</span>
                    <span>LOCK STATUS:</span> <span style={{ color: '#00ffff' }}>{lockStatus.toFixed(1)}%</span>
                    <span>HADES GAP:</span> <span>12.37%</span>
                    <span>UMBER FOCUS:</span> <span style={{ color: '#aa44ff' }}>{(focusMetric * 100).toFixed(1)}%</span>
                </div>
                <div style={{ marginTop: '12px', paddingTop: '8px', borderTop: '1px solid rgba(16, 185, 129, 0.3)', color: isSealed ? '#ffd700' : '#888', textAlign: 'center', fontSize: '1rem', fontWeight: 'bold' }}>
                    {isSealed ? "AMEN 33 SEALED" : "SEAL PENDING..."}
                </div>
            </div>

            {/* MAIN CONTROLS (Left Side) */}
            <div style={{ position: 'absolute', top: 20, left: 20, color: '#00ffcc', fontFamily: 'monospace', pointerEvents: 'none', zIndex: 100 }}>
                <div style={{ border: '1px solid #00ffcc', padding: '10px', background: 'rgba(0, 20, 0, 0.8)', backdropFilter: 'blur(5px)', width: '320px', pointerEvents: 'auto' }}>
                    <h2 style={{ margin: 0, fontSize: '1.2rem' }}>SOVEREIGN ENGINE v1.1</h2>
                    <p style={{ fontSize: '0.8rem', opacity: 0.8 }}>
                        STATUS: {isSimulating ? `SIMULATING WEEK ${currentWeek}` : isFractured ? 'PHASE II: FRACTURE SEAL' : 'PHASE I: VITRIFIED'}
                    </p>
                    <hr style={{ border: 'none', borderTop: '1px solid #00ffcc', margin: '10px 0' }} />

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px', fontSize: '0.75rem' }}>
                        <span>BEAT: 0.660 HZ</span>
                        <span>HARMONIC: 66 HZ</span>
                        <span>DELTA: 0.000585</span>
                        <span>SHEAR: 39.4°</span>
                    </div>

                    <div style={{ marginTop: '15px' }}>
                        <label style={{ fontSize: '0.7rem', display: 'block', marginBottom: '5px' }}>
                            FRACTAL ZOOM: {fractalZoom < 0.3 ? 'POPPY SEED' : fractalZoom > 0.7 ? 'POMEGRANATE' : 'TRANSITION'}
                        </label>
                        <input
                            type="range"
                            min="0"
                            max="1"
                            step="0.01"
                            value={fractalZoom}
                            onChange={(e) => setFractalZoom(parseFloat(e.target.value))}
                            style={{ width: '100%', accentColor: '#ffd700', cursor: 'pointer' }}
                        />
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.6rem', opacity: 0.6, marginTop: '2px' }}>
                            <span>nⁿ (SEED)</span>
                            <span style={{ marginLeft: 'auto' }}>(10n)ⁿ (FRUIT)</span>
                        </div>
                    </div>

                    <div style={{ marginTop: '15px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        <div style={{ fontSize: '0.65rem', display: 'flex', justifyContent: 'space-between' }}>
                            <span style={{ color: '#ff00ff' }}>UMBER RESONANCE (√10)</span>
                            <span>{(useSovereignStore.getState().seedResonance * 100).toFixed(1)}%</span>
                        </div>
                        <div style={{ height: '3px', background: '#310047', width: '100%', position: 'relative' }}>
                            <div style={{
                                height: '100%',
                                background: '#ff00ff',
                                width: `${useSovereignStore.getState().seedResonance * 100}%`,
                                transition: 'width 0.2s ease'
                            }} />
                        </div>

                        <div style={{ fontSize: '0.65rem', display: 'flex', justifyContent: 'space-between', marginTop: '5px' }}>
                            <span style={{ color: '#00ffcc' }}>WORLD RESONANCE (10)</span>
                            <span>{(useSovereignStore.getState().worldResonance * 100).toFixed(1)}%</span>
                        </div>
                        <div style={{ height: '3px', background: '#003322', width: '100%', position: 'relative' }}>
                            <div style={{
                                height: '100%',
                                background: '#00ffcc',
                                width: `${useSovereignStore.getState().worldResonance * 100}%`,
                                transition: 'width 0.2s ease'
                            }} />
                        </div>
                    </div>

                    <div style={{ marginTop: '20px', borderTop: '1px solid #00ffcc', paddingTop: '10px' }}>
                        <div style={{ fontSize: '0.8rem', marginBottom: '10px', color: isSimulating ? '#ffcc00' : '#00ffcc' }}>
                            {getArcLabel()}: {currentWeek === 0 ? 'STANDBY' : `WEEK ${currentWeek}`}
                        </div>
                        {!isSimulating ? (
                            <div style={{ display: 'flex', gap: '5px' }}>
                                <button onClick={handleStartSim} style={btnStyle}>ENGAGE WK 14</button>
                                <button onClick={handleJumpToZenith} style={{ ...btnStyle, background: 'rgba(255, 204, 0, 0.1)', borderColor: '#ffcc00', color: '#ffcc00' }}>JUMP TO ZENITH</button>
                            </div>
                        ) : (
                            <button onClick={handleNextWeek} style={{ ...btnStyle, width: '100%', color: '#ffcc00', borderColor: '#ffcc00' }}>
                                {currentWeek === 26 ? "TRIGGER MOTORBIKE (WK 27)" : `ADVANCE TO WEEK ${currentWeek + 1 > 52 ? 1 : currentWeek + 1}`}
                            </button>
                        )}
                    </div>

                    <div style={{ marginTop: '15px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.8rem' }}>
                            <input
                                type="checkbox"
                                checked={showMergedStream}
                                onChange={(e) => setShowMergedStream(e.target.checked)}
                                style={{ accentColor: '#00ffcc' }}
                            />
                            SHOW MERGED SPECTRUM (M)
                        </label>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.8rem' }}>
                            <input
                                type="checkbox"
                                checked={showOpticalOverlay}
                                onChange={(e) => setShowOpticalOverlay(e.target.checked)}
                                style={{ accentColor: '#aa44ff' }}
                            />
                            OPTICAL FOCAL PLANE (O)
                        </label>

                        <button onClick={handleIngest} style={{ ...btnStyle, background: 'rgba(255, 68, 255, 0.1)', borderColor: '#ff44ff', color: '#ff44ff', width: '100%' }}>
                            INGEST .VETH PAYLOAD
                        </button>
                    </div>

                    {isSimulating && (
                        <div style={{ marginTop: '10px', borderTop: '1px solid rgba(0, 255, 204, 0.3)', paddingTop: '5px', fontSize: '0.65rem' }}>
                            <div style={{ color: '#00ffcc' }}>DEBUG: ARC = {arc} | AMP = {amplitude.toFixed(4)}</div>
                            <div style={{ color: isZenith ? '#ffff00' : '#888' }}>
                                ZENITH REACHED: {isZenith ? '✅ (READY FOR MOTORBIKE)' : '❌'}
                            </div>
                        </div>
                    )}

                    {isFractured && (
                        <div style={{ marginTop: '10px', color: '#ff4400', fontSize: '0.8rem', fontWeight: 'bold', textAlign: 'center' }}>
                            WARNING: TEETH OF STONES AUDIBLE
                        </div>
                    )}
                </div>
            </div>
        </>
    );
};

const btnStyle = {
    flex: 1,
    background: 'transparent',
    border: '1px solid #00ffcc',
    color: '#00ffcc',
    padding: '8px',
    cursor: 'pointer',
    fontSize: '0.75rem',
    fontFamily: 'monospace',
    transition: 'all 0.2s ease'
};
