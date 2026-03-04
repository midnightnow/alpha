/**
 * GenesisSequence.js - The 1:3:3:1 Octave Kiln
 * 
 * Replaces timed animation with Kinetic Axiomatic Construction.
 * Transitions are gated by the Biquadratic Law (Hades Gap).
 * The human form is extracted as an 8-unit octave.
 */

class GenesisSequence {
    constructor(mathman) {
        this.mm = mathman;

        this.overlay = document.createElement('canvas');
        this.overlay.style.cssText = `
            position: absolute; top: 0; left: 0;
            width: 100%; height: 100%; pointer-events: none; z-index: 200;
        `;
        this.mm.canvas.parentElement.appendChild(this.overlay);
        this.ctx = this.overlay.getContext('2d');

        this.running = false;
        this.rafId = null;
        this.ripples = [];
        this.nodes = [];
        this.phaseIndex = -1;
        this.phaseStartTime = 0;
        this.currentProgress = 0;

        if (typeof AxiomValidator !== 'undefined') {
            this.validator = new AxiomValidator(this.mm);
        }

        this._resize();
        window.addEventListener('resize', () => this._resize());
    }

    get PHASES() {
        return [
            {
                name: "Singularity",
                desc: "Time establishes Measure. Origin A is seed.",
                setup: () => {
                    this._hideAll();
                    this.mm.params.distAB = 0;
                    this.mm.params.brightness = 0;
                    this._spawnContinuous('A');
                }
            },
            {
                name: "Measure (0-1)",
                desc: "A 1x1 grounded square stabilizes. The Unit Foot.",
                setup: () => {
                    this.mm.params.distAB = 0.01;
                    this.mm.params.brightness = 0.2;
                    this._spawnContinuous('B');
                },
                update: (now) => {
                    // Sweep until base stability (Foot station)
                    if (this.mm.params.distAB < 1.0) this.mm.params.distAB += 0.02;
                },
                targetHeight: 0.0
            },
            {
                name: "Pedestal Unfold (1-4)",
                desc: "Perimeter peels vertically. Target: Perineum Station.",
                setup: () => {
                    this.mm.params.brightness = 0.4;
                    this.currentProgress = 0;
                },
                update: (now) => {
                    const x = this.validator.sampleFieldAtNode(4.0);
                    const r = this.validator.computeRemainder(x);

                    if (!this.validator.isSintered(r)) {
                        this._applyVisualWobble(r);
                        // Search sweep for the gearbox (distAB)
                        this.mm.params.distAB += 0.03;
                        if (this.mm.params.distAB > 16) this.mm.params.distAB = 1.0;
                    } else {
                        if (this.currentProgress < 1.0) this.currentProgress += 0.05;
                    }
                },
                targetHeight: 4.0
            },
            {
                name: "Reflection (4-7)",
                desc: "Terrestrial Mirroring. Body manifest from Perineum.",
                setup: () => {
                    this.mm.params.brightness = 0.6;
                    this._crystalliseNodes(7.0);
                }
            },
            {
                name: "Mind Induction (7-8)",
                desc: "Celestial Capstone. Point C induction at unit 8.",
                setup: () => {
                    this.mm.params.distC = 12.0;
                    this.mm.params.brightness = 0.85;
                    this.mm.controls.showMathman.checked = true;
                    this._spawnContinuous('C');
                }
            }
        ];
    }

    /**
     * Active Newton-Raphson hunt for the biquadratic root.
     * f(x) = x^4 - 186x^2 + 81
     */
    activeResonanceSolve(targetStation) {
        if (!this.validator) return 1.0;

        let x = this.validator.sampleFieldAtNode(targetStation);
        const r = this.validator.computeRemainder(x);

        if (this.validator.isSintered(r)) return r;

        // Newton-Raphson Step
        const df = this.validator.computeDerivative(x);
        if (Math.abs(df) > 0.0001) {
            // We adjust distAB as our proxy for 'tuning' the field
            // This is a simplification: in reality, we'd adjust the geometric constants
            const delta = r / df;
            this.mm.params.distAB -= delta * 0.1;
        } else {
            // Avoid singularity, nudge distAB
            this.mm.params.distAB += 0.05;
        }

        // Clamp distAB to valid range
        this.mm.params.distAB = Math.max(0.1, Math.min(20.0, this.mm.params.distAB));

        return r;
    }

    _startLoop() {
        const loop = (now) => {
            if (!this.running) return;

            if (this.phaseIndex === -1) {
                this._advancePhase(now);
            } else {
                const phase = this.PHASES[this.phaseIndex];

                // Active Solving
                const remainder = this.activeResonanceSolve(phase.targetHeight || 0);
                const sintered = this.validator.isSintered(remainder);

                // Update Shader Uniforms via Controller
                if (this.mm.controller) {
                    this.mm.controller.applyDiagnosticState({
                        remainder: remainder,
                        unfold: this.currentProgress
                    });
                }

                // GATING: Only advance if the field has vitrified (Sintered)
                if (sintered) {
                    // Update Hinge Unfold for specific phases
                    if (this.phaseIndex === 2 && this.currentProgress < 1.0) {
                        this.currentProgress += 0.02;
                    }

                    const progressMet = (this.phaseIndex === 2) ? (this.currentProgress >= 1.0) : true;
                    const minTimeMet = (now - this.phaseStartTime) > 3000;

                    if (progressMet && minTimeMet) {
                        if (this.phaseIndex < this.PHASES.length - 1) {
                            this._advancePhase(now);
                        } else if ((now - this.phaseStartTime) > 8000) {
                            this._finish();
                            return;
                        }
                    }
                } else {
                    // Vapor Wobble feedback
                    this._applyVisualWobble(remainder);
                }
            }

            const currentPhase = this.PHASES[this.phaseIndex];
            if (currentPhase && currentPhase.update) currentPhase.update(now);

            this._updateRipples();
            this._draw(now);
            this.rafId = requestAnimationFrame(loop);
        };
        this.rafId = requestAnimationFrame(loop);
    }

    _draw(now) {
        const W = this.overlay.width;
        const H = this.overlay.height;
        const ctx = this.ctx;

        const sinceStart = now - (this._startMs || now);
        const bgAlpha = sinceStart < 4000 ? 1.0 : 0.2;
        ctx.fillStyle = `rgba(10, 8, 5, ${bgAlpha})`;
        ctx.fillRect(0, 0, W, H);

        const o = this.mm.getOrigins();
        const pA = this.mm.project(o.a.x, o.a.y, 0, o);
        const pB = this.mm.project(o.b.x, o.b.y, 0, o);

        // Ripples
        for (const r of this.ripples) {
            ctx.beginPath();
            ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
            ctx.strokeStyle = this._rgba(r.color, r.alpha);
            ctx.stroke();
        }

        // The Hinge Unfold Visual (Kinematic logic)
        if (this.phaseIndex >= 2) {
            this._drawHingeUnfold(pA, pB);
        }

        this._updateEmitters(now, pA, pB);
    }

    _drawHingeUnfold(pA, pB) {
        const ctx = this.ctx;
        const progress = this.currentProgress || 0;
        const x = (pA.x + pB.x) / 2;
        const footY = pA.y;
        const height = 120 * progress; // Visual height for the 3-unit lift

        ctx.beginPath();
        ctx.moveTo(x - 20, footY);
        ctx.lineTo(x + 20, footY);
        ctx.strokeStyle = progress >= 1.0 ? '#ffd700' : '#00ffff';
        ctx.lineWidth = 3;
        ctx.stroke();

        if (progress > 0) {
            ctx.beginPath();
            ctx.moveTo(x, footY);
            ctx.lineTo(x, footY - height);
            ctx.setLineDash([5, 5]);
            ctx.stroke();
            ctx.setLineDash([]);
        }
    }

    _applyVisualWobble(remainder) {
        const offset = Math.sin(performance.now() * 0.1) * remainder * 10;
        this.overlay.style.transform = `translate(${offset}px, 0)`;
        this.mm.params.brightness = 0.4 + Math.sin(performance.now() * 0.05) * 0.1;
    }

    _advancePhase(now) {
        this.phaseIndex++;
        const phase = this.PHASES[this.phaseIndex];
        this.phaseStartTime = now;
        this._showText(phase.name, phase.desc);
        if (this.validator) this.validator.logProof(this.phaseIndex, phase.name);
        this.overlay.style.transform = 'none';
    }

    // Boilerplate helpers...
    _updateEmitters(now, pA, pB) {
        const interval = 800;
        if (this._doA && (!this._tA || now - this._tA > interval)) { this._spawnRing(pA.x, pA.y, '#00ffff'); this._tA = now; }
        if (this._doB && (!this._tB || now - this._tB > interval)) { this._spawnRing(pB.x, pB.y, '#ff44cc'); this._tB = now; }
        if (this._doC) {
            const pC = this.mm.project(0, 8, 0, this.mm.getOrigins()); // Induced crown
            if (!this._tC || now - this._tC > interval) { this._spawnRing(pC.x, pC.y, '#ffd700'); this._tC = now; }
        }
    }

    _spawnRing(x, y, color) {
        this.ripples.push({ x, y, color, radius: 4, speed: 1.5, alpha: 0.6, fade: 0.01 });
    }

    _updateRipples() {
        for (const r of this.ripples) { r.radius += r.speed; r.alpha -= r.fade; }
        this.ripples = this.ripples.filter(r => r.alpha > 0.01);
    }

    _spawnContinuous(src) { this[`_do${src}`] = true; }

    _showText(title, desc) {
        const el = this.mm.controls.genesisText;
        if (!el) return;
        el.classList.remove('visible');
        setTimeout(() => {
            el.innerHTML = `<span style="font-size:1.4rem;color:#ffd700;">${title}</span><br><span style="opacity:0.8;font-family:monospace;">${desc}</span>`;
            el.classList.add('visible');
        }, 300);
    }

    _resize() { this.overlay.width = this.mm.canvas.width; this.overlay.height = this.mm.canvas.height; }
    _rgba(hex, alpha) { const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16); return `rgba(${r},${g},${b},${Math.max(0, alpha).toFixed(3)})`; }
    _saveState() { this._saved = { dAB: this.mm.params.distAB, br: this.mm.params.brightness, th: this.mm.params.threshold }; }
    _resetParams() { this._doA = this._doB = this._doC = false; this.ripples = []; this.nodes = []; this.phaseIndex = -1; }
    _hideAll() { this.mm.params.threshold = 0.999; this.mm.params.brightness = 0; }

    _finish() {
        this.running = false;
        if (this.rafId) cancelAnimationFrame(this.rafId);
        this.overlay.remove();
        this.mm.params.brightness = 0.8;
        this.mm.params.threshold = 0.15;
        if (this.mm.controls.genesisText) this.mm.controls.genesisText.classList.remove('visible');
    }
}
