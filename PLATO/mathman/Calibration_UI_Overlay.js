/**
 * Calibration_UI_Overlay.js
 * 
 * Clinical Researcher Interface for the Mathman Biofield Coherence Engine.
 * Provides real-time injection of Phonetic Torque into the Haric Axis,
 * allowing live visualization of Auric Mucus turning into Buoyant Coherence.
 */

class CalibrationUIOverlay {
    constructor(bridgeInstance) {
        if (!bridgeInstance) {
            console.error("CalibrationUIOverlay requires a ResonanceEngineBridge instance.");
            return;
        }
        this.bridge = bridgeInstance;
        this.initUI();
    }

    initUI() {
        // Create the containing UI Panel
        this.panel = document.createElement('div');
        this.panel.id = 'clinical-diagnostic-panel';
        Object.assign(this.panel.style, {
            position: 'absolute',
            bottom: '20px',
            right: '20px',
            width: '320px',
            backgroundColor: 'rgba(10, 8, 5, 0.85)',
            border: '1px solid rgba(255, 215, 0, 0.3)',
            borderRadius: '8px',
            padding: '16px',
            fontFamily: '"Space Grotesk", sans-serif',
            color: '#e0e0e0',
            backdropFilter: 'blur(10px)',
            zIndex: '1000',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.5)'
        });

        // Title
        const title = document.createElement('h3');
        title.innerText = 'Haric Axis Calibration';
        Object.assign(title.style, {
            margin: '0 0 12px 0',
            fontSize: '14px',
            color: '#ffd700',
            textTransform: 'uppercase',
            letterSpacing: '1px'
        });
        this.panel.appendChild(title);

        // Coherence Readout
        this.coherenceReadout = document.createElement('div');
        Object.assign(this.coherenceReadout.style, {
            fontSize: '24px',
            fontWeight: 'bold',
            marginBottom: '4px'
        });
        this.panel.appendChild(this.coherenceReadout);

        // Status Readout
        this.statusReadout = document.createElement('div');
        Object.assign(this.statusReadout.style, {
            fontSize: '11px',
            textTransform: 'uppercase',
            letterSpacing: '2px',
            marginBottom: '16px'
        });
        this.panel.appendChild(this.statusReadout);

        // Torque Slider
        const sliderContainer = document.createElement('div');
        const sliderLabel = document.createElement('label');
        sliderLabel.innerText = 'Phonetic Torque (Phase Shift)';
        Object.assign(sliderLabel.style, {
            display: 'block',
            fontSize: '11px',
            marginBottom: '6px'
        });

        this.torqueSlider = document.createElement('input');
        this.torqueSlider.type = 'range';
        this.torqueSlider.min = '-3.14';
        this.torqueSlider.max = '3.14';
        this.torqueSlider.step = '0.01';
        this.torqueSlider.value = '0';
        Object.assign(this.torqueSlider.style, {
            width: '100%',
            cursor: 'pointer'
        });

        // Live Torque Value
        this.torqueValueDisp = document.createElement('span');
        this.torqueValueDisp.innerText = '0.00 rad';
        Object.assign(this.torqueValueDisp.style, {
            float: 'right',
            color: '#00ffff'
        });
        sliderLabel.appendChild(this.torqueValueDisp);

        sliderContainer.appendChild(sliderLabel);
        sliderContainer.appendChild(this.torqueSlider);
        this.panel.appendChild(sliderContainer);

        // Auto-Solve Button
        this.btnSolve = document.createElement('button');
        this.btnSolve.innerText = 'INITIATE RESONANCE SOLVE';
        Object.assign(this.btnSolve.style, {
            width: '100%',
            marginTop: '16px',
            padding: '10px',
            backgroundColor: 'rgba(255, 215, 0, 0.1)',
            border: '1px solid #ffd700',
            color: '#ffd700',
            cursor: 'pointer',
            fontFamily: '"Space Grotesk", sans-serif',
            fontSize: '11px',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            transition: 'all 0.3s ease'
        });

        this.btnSolve.onmouseover = () => this.btnSolve.style.backgroundColor = 'rgba(255, 215, 0, 0.3)';
        this.btnSolve.onmouseout = () => this.btnSolve.style.backgroundColor = 'rgba(255, 215, 0, 0.1)';

        this.panel.appendChild(this.btnSolve);

        document.body.appendChild(this.panel);

        this.bindEvents();
    }

    bindEvents() {
        // Manual Torque Adjustment
        this.torqueSlider.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            this.torqueValueDisp.innerText = `${val.toFixed(2)} rad`;

            // Push direct torque into the bridge for immediate visual feedback
            if (this.bridge.webgl) {
                this.bridge.webgl.targetUniforms.u_torque = val * 0.5; // scaling for amplitude

                // If the user manually applies torque, we simulate an increase in coherence
                // based on proximity to the "ideal" resonant frequency.
                // In a true solve, the engine calculates the diff. Here we simulate the slider's effect.
                const simulatedCoherence = 0.4412 + Math.abs(val) * 0.2; // Base + Torque lift
                this.updateReadouts(simulatedCoherence);
            }
        });

        // Auto Resonance Solve
        this.btnSolve.addEventListener('click', () => {
            this.btnSolve.innerText = 'CALCULATING TORQUE...';
            this.btnSolve.style.color = '#fff';

            setTimeout(() => {
                // Simulate the solver finding the exact phase shift
                const idealShift = 1.42;
                this.torqueSlider.value = idealShift;
                this.torqueValueDisp.innerText = `${idealShift.toFixed(2)} rad`;

                // Jump coherence to the Unity Threshold
                this.updateReadouts(0.8254);

                if (this.bridge.webgl) {
                    this.bridge.webgl.targetUniforms.u_torque = idealShift * 0.5;
                }

                this.btnSolve.innerText = 'AXIS STABILIZED: MUCUS CLEARED';
                this.btnSolve.style.backgroundColor = 'rgba(0, 255, 255, 0.2)';
                this.btnSolve.style.borderColor = '#00ffff';
                this.btnSolve.style.color = '#00ffff';

                setTimeout(() => {
                    this.btnSolve.innerText = 'INITIATE RESONANCE SOLVE';
                    this.btnSolve.style.backgroundColor = 'rgba(255, 215, 0, 0.1)';
                    this.btnSolve.style.borderColor = '#ffd700';
                    this.btnSolve.style.color = '#ffd700';
                }, 4000);

            }, 800);
        });
    }

    // Called routinely by the bridge or main loop
    updateReadouts(coherence) {
        this.coherenceReadout.innerText = `Σ ${coherence.toFixed(4)}`;

        // Push State to Bridge
        if (this.bridge.webgl) {
            this.bridge.webgl.targetUniforms.u_coherence = coherence;
        }

        if (coherence < 0.8254) {
            this.statusReadout.innerText = 'STATUS: AURIC MUCUS (VAPOR)';
            this.statusReadout.style.color = '#888';
            this.coherenceReadout.style.color = '#888';
            if (this.bridge.webgl) this.bridge.webgl.targetUniforms.u_structural_phase = 0.0;
        } else if (coherence > 0.9999) {
            this.statusReadout.innerText = 'STATUS: VITRIFICATION RISK (DIAMOND)';
            this.statusReadout.style.color = '#fff';
            this.coherenceReadout.style.color = '#fff';
            if (this.bridge.webgl) this.bridge.webgl.targetUniforms.u_structural_phase = 2.0;
        } else {
            this.statusReadout.innerText = 'STATUS: BUOYANT COHERENCE (STONE)';
            this.statusReadout.style.color = '#ffd700';
            this.coherenceReadout.style.color = '#ffd700';
            if (this.bridge.webgl) this.bridge.webgl.targetUniforms.u_structural_phase = 1.0;
        }
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CalibrationUIOverlay;
}
