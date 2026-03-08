/**
 * GenesisSequence.js
 * 
 * A mathematical demonstration of wave interference emergence.
 * Shows how standing wave patterns arise from point sources —
 * from a single origin through to the full nodal skeleton.
 *
 * INTEGRATION: Add to index.html after main.js:
 *   <script src="GenesisSequence.js"></script>
 *
 * Then replace runGenesis() in main.js with:
 *   async runGenesis() {
 *       if (this.genesisRunning) return;
 *       this.genesisRunning = true;
 *       this.controls.btnGenesis.innerText = "Genesis Active...";
 *       const seq = new GenesisSequence(this);
 *       await seq.run();
 *       this.genesisRunning = false;
 *       this.controls.btnGenesis.innerText = "Start Genesis";
 *   }
 */

class GenesisSequence {
    constructor(mathman) {
        this.mm = mathman;

        // Create a dedicated overlay canvas that sits on top of the main canvas
        this.overlay = document.createElement('canvas');
        this.overlay.style.cssText = `
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 50;
        `;
        this.mm.canvas.parentElement.appendChild(this.overlay);
        this.ctx = this.overlay.getContext('2d');

        this.running = false;
        this.rafId = null;

        // State tracked across the animation
        this.ripples   = [];   // Active expanding wave rings
        this.nodes     = [];   // Crystallised interference nodes
        this.phase     = 0;    // Current Genesis phase index
        this.phaseTime = 0;    // Time current phase started (ms)

        // Resize overlay to match canvas
        this._resize();
        window.addEventListener('resize', () => this._resize());
    }

    // ── Public ────────────────────────────────────────────────────────────────

    async run() {
        this.running = true;
        this._saveState();
        this._resetParams();

        const totalMs = this.PHASES.reduce((s, p) => s + p.duration, 0) + 2000;
        this._startMs = performance.now();
        this._startLoop();

        await new Promise(r => setTimeout(r, totalMs));
        this._finish();
    }

    // ── Phase Definitions ─────────────────────────────────────────────────────
    // Each phase has: label (equation/description), duration (ms), enter() callback

    get PHASES() { return [
        {
            duration: 5000,
            label: "A single point. No distance. No time.",
            eq: null,
            enter: () => {
                // Complete blank — suppress main render layers
                this._hideAll();
                this.mm.params.distAB = 0;
                this.mm.params.distC  = 0;
                this.mm.params.brightness = 0;
            }
        },
        {
            duration: 7000,
            label: "One source radiates. d = ct",
            eq: "ψ(r,t) = cos(kr)",
            enter: () => {
                // Single origin A emitting rings
                this.mm.params.distAB  = 0.001; // near-zero but not zero
                this.mm.params.brightness = 0;
                this._spawnContinuous('A');
            }
        },
        {
            duration: 7000,
            label: "A second source. Separation introduces path difference.",
            eq: "Δr = |r_A − r_B|",
            enter: () => {
                this.mm.params.distAB = 4.0;
                this._spawnContinuous('B');
            }
        },
        {
            duration: 9000,
            label: "Superposition: waves add. Where crests meet, amplitude doubles.",
            eq: "ψ_total = ψ_A + ψ_B = cos(kr_A) + cos(kr_B)",
            enter: () => {
                this.mm.params.distAB    = 12.0;
                this.mm.params.brightness = 0.4;
                this.mm.params.threshold  = 0.5;
                this.mm.controls.showField.checked = true;
            }
        },
        {
            duration: 9000,
            label: "Constructive interference: Δr = nλ  →  nodal maxima lock in place.",
            eq: "I ∝ cos²(k·Δr/2)",
            enter: () => {
                this.mm.params.threshold  = 0.3;
                this.mm.params.brightness = 0.6;
                this._crystalliseNodes();
            }
        },
        {
            duration: 8000,
            label: "A third source. Three-wave superposition generates hexagonal symmetry.",
            eq: "ψ = (ψ_A + ψ_B + ψ_C) / 3",
            enter: () => {
                this.mm.params.distC   = 12.0;
                this.mm.params.threshold  = 0.2;
                this.mm.params.brightness = 0.65;
                this._spawnContinuous('C');
                this._crystalliseNodes();
            }
        },
        {
            duration: 9000,
            label: "Standing wave. Nodes fixed in space — the field has structure.",
            eq: "∂²ψ/∂t² = c²∇²ψ",
            enter: () => {
                this.mm.params.threshold  = 0.15;
                this.mm.params.brightness = 0.75;
                this.mm.controls.layerHarmonic.checked = true;
                this._crystalliseNodes();
            }
        },
        {
            duration: 9000,
            label: "The nodal skeleton — Vitruvian proportions emerge from the wave geometry.",
            eq: "Scale: √42 ≈ 6.48  (substantiation threshold)",
            enter: () => {
                this.mm.params.brightness = 0.85;
                this.mm.controls.showMathman.checked   = true;
                this.mm.controls.layerVitruvian.checked = true;
                this.mm.controls.layerAnnotations.checked = true;
            }
        }
    ]; }

    // ── Animation Loop ────────────────────────────────────────────────────────

    _startLoop() {
        let phaseIndex = -1;
        const startTime = performance.now();

        const loop = (now) => {
            if (!this.running) return;

            const elapsed = now - startTime;

            // Advance phase if needed
            let cursor = 0;
            for (let i = 0; i < this.PHASES.length; i++) {
                cursor += this.PHASES[i].duration;
                if (elapsed < cursor) {
                    if (i !== phaseIndex) {
                        phaseIndex = i;
                        this.phaseTime = now;
                        this.PHASES[i].enter();
                        this._showText(this.PHASES[i].label, this.PHASES[i].eq);
                    }
                    break;
                }
            }

            this._updateRipples();
            this._draw(now);

            this.rafId = requestAnimationFrame(loop);
        };

        this.rafId = requestAnimationFrame(loop);
    }

    // ── Drawing ───────────────────────────────────────────────────────────────

    _draw(now) {
        const W = this.overlay.width;
        const H = this.overlay.height;
        const ctx = this.ctx;

        // Soft trail — let ripples persist but fade
        // Solid background for first phase to cover main render,
        // then semi-transparent for ripple trails
        const sinceStart = now - (this._startMs || now);
        const bgAlpha = sinceStart < 5500 ? 1.0 : 0.18;
        ctx.fillStyle = `rgba(10, 8, 5, ${bgAlpha})`;
        ctx.fillRect(0, 0, W, H);

        const o = this.mm.getOrigins();

        // Draw ripples
        for (const r of this.ripples) {
            ctx.beginPath();
            ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
            ctx.strokeStyle = this._rgba(r.color, r.alpha);
            ctx.lineWidth = 1.0;
            ctx.stroke();
        }

        // Spawn continuous ripples
        const pA = this.mm.project(o.a.x, o.a.y, 0, o);
        const pB = this.mm.project(o.b.x, o.b.y, 0, o);
        const pC = this.mm.project(o.c.x, o.c.y, 0, o);

        const interval = 700; // ms between rings
        if (this._doA && (!this._tA || now - this._tA > interval)) {
            this._spawnRing(pA.x, pA.y, '#00ffff');
            this._tA = now;
        }
        if (this._doB && (!this._tB || now - this._tB > interval)) {
            this._spawnRing(pB.x, pB.y, '#ff44cc');
            this._tB = now;
        }
        if (this._doC && (!this._tC || now - this._tC > interval)) {
            this._spawnRing(pC.x, pC.y, '#ffd700');
            this._tC = now;
        }

        // Draw crystallised nodes
        if (this.nodes.length > 0) {
            const age = (now - this._nodesBorn) / 1000;
            const reveal = Math.min(1, age * 0.5);
            for (const n of this.nodes) {
                if (Math.random() > reveal && age < 2) continue; // staggered reveal
                const pulse = 0.6 + 0.4 * Math.sin(now * 0.002 + n.x * 0.1);
                ctx.beginPath();
                ctx.arc(n.sx, n.sy, n.r, 0, Math.PI * 2);
                ctx.fillStyle = this._rgba(n.color, n.alpha * pulse);
                ctx.fill();
            }
        }

        // Draw origin point markers on top
        this._drawOriginPoint(ctx, pA.x, pA.y, '#00ffff', 'A', now, this._doA || this._doB);
        if (this.mm.params.distAB > 0.1)
            this._drawOriginPoint(ctx, pB.x, pB.y, '#ff44cc', 'B', now, this._doB);
        if (this.mm.params.distC > 0.1)
            this._drawOriginPoint(ctx, pC.x, pC.y, '#ffd700', 'C', now, this._doC);
    }

    _drawOriginPoint(ctx, x, y, color, label, now, active) {
        if (!active) return;
        const pulse = active ? 0.4 + 0.3 * Math.sin(now * 0.005) : 0.3;
        // Glow ring
        ctx.beginPath();
        ctx.arc(x, y, 10 + pulse * 6, 0, Math.PI * 2);
        ctx.fillStyle = this._rgba(color, 0.08 + pulse * 0.08);
        ctx.fill();
        // Core dot
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        // Label
        ctx.font = 'bold 11px JetBrains Mono, monospace';
        ctx.fillStyle = color;
        ctx.fillText(label, x + 10, y - 8);
    }

    // ── Ripple System ─────────────────────────────────────────────────────────

    _spawnRing(x, y, color) {
        const mm = this.mm.getOrigins().mm;
        this.ripples.push({
            x, y, color,
            radius: 4,
            speed: mm * 0.09,
            alpha: 0.65,
            fade: 0.007
        });
    }

    _updateRipples() {
        for (const r of this.ripples) {
            r.radius += r.speed;
            r.alpha  -= r.fade;
        }
        this.ripples = this.ripples.filter(r => r.alpha > 0.003);
    }

    _spawnContinuous(src) {
        if (src === 'A') this._doA = true;
        if (src === 'B') this._doB = true;
        if (src === 'C') this._doC = true;
    }

    // ── Node Crystallisation ──────────────────────────────────────────────────
    // Computes actual interference maxima from wave physics and renders them

    _crystalliseNodes() {
        this.nodes = [];
        this._nodesBorn = performance.now();

        const o    = this.mm.getOrigins();
        const k    = (2 * Math.PI) / this.mm.params.lambda;
        const step = 0.5; // world-unit grid step
        const threshold = 0.72; // only strong constructive nodes

        const useC = this.mm.params.distC > 0.1;

        for (let gx = -10; gx <= 10; gx += step) {
            for (let gy = -2; gy <= 10; gy += step) {
                const dA = Math.sqrt((gx - o.a.x) ** 2 + gy ** 2);
                const dB = Math.sqrt((gx - o.b.x) ** 2 + gy ** 2);
                const dC = useC
                    ? Math.sqrt(gx ** 2 + (gy - o.c.y) ** 2)
                    : 0;

                const wA = Math.cos(k * dA);
                const wB = Math.cos(k * dB);
                const wC = useC ? Math.cos(k * dC) : 0;
                const n  = useC ? 3 : 2;
                const total = (wA + wB + (useC ? wC : 0)) / n;

                if (total > threshold) {
                    const p = this.mm.project(gx, gy, 0, o);
                    const size = 1.5 + total * 2.5;
                    // Colour by dominant source proximity
                    const color = useC
                        ? this._blendColor(dA, dB, dC)
                        : (dA < dB ? '#00ffff' : '#ff44cc');

                    this.nodes.push({
                        sx: p.x, sy: p.y,
                        r: size,
                        alpha: 0.5 + total * 0.4,
                        color
                    });
                }
            }
        }
    }

    _blendColor(dA, dB, dC) {
        const min = Math.min(dA, dB, dC);
        if (dA === min) return '#00ffff';
        if (dB === min) return '#ff44cc';
        return '#ffd700';
    }

    // ── Text Display ──────────────────────────────────────────────────────────

    _showText(label, eq) {
        const textEl = this.mm.controls.genesisText;
        if (!textEl) return;

        textEl.classList.remove('visible');
        setTimeout(() => {
            textEl.innerHTML = eq
                ? `<span style="font-size:1.4rem;letter-spacing:2px;">${label}</span>
                   <br><span style="font-size:0.95rem;opacity:0.7;font-family:monospace;color:#00ffff;">${eq}</span>`
                : `<span style="font-size:1.4rem;letter-spacing:2px;">${label}</span>`;
            textEl.classList.add('visible');
        }, 300);
    }

    // ── Utilities ─────────────────────────────────────────────────────────────

    _resize() {
        const r = devicePixelRatio || 1;
        this.overlay.width  = this.mm.canvas.width;
        this.overlay.height = this.mm.canvas.height;
    }

    _rgba(hex, alpha) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r},${g},${b},${Math.max(0, Math.min(1, alpha)).toFixed(3)})`;
    }

    _saveState() {
        this._saved = {
            distAB:     this.mm.params.distAB,
            distC:      this.mm.params.distC,
            brightness: this.mm.params.brightness,
            threshold:  this.mm.params.threshold,
        };
    }

    _resetParams() {
        this._doA = false; this._doB = false; this._doC = false;
        this._tA  = null;  this._tB  = null;  this._tC  = null;
        this.ripples = [];
        this.nodes   = [];
    }

    _hideAll() {
        // Set threshold so high nothing renders through the main loop
        this.mm.params.threshold  = 0.999;
        this.mm.params.brightness = 0;
        // Also uncheck layers for when Genesis ends
        Object.keys(this.mm.controls).forEach(k => {
            const c = this.mm.controls[k];
            if (c && c.type === 'checkbox') c.checked = false;
        });
    }

    _finish() {
        this.running = false;
        if (this.rafId) cancelAnimationFrame(this.rafId);

        // Clear overlay
        this.ctx.clearRect(0, 0, this.overlay.width, this.overlay.height);
        this.overlay.remove();

        // Restore params to working state
        this.mm.params.distAB     = this._saved.distAB;
        this.mm.params.distC      = this._saved.distC;
        this.mm.params.brightness = Math.max(this._saved.brightness, 0.7);
        this.mm.params.threshold  = Math.min(this._saved.threshold,  0.15);

        // Ensure field is visible after Genesis
        if (this.mm.controls.showField)    this.mm.controls.showField.checked    = true;
        if (this.mm.controls.showMathman)  this.mm.controls.showMathman.checked  = true;

        // Hide text
        const textEl = this.mm.controls.genesisText;
        if (textEl) textEl.classList.remove('visible');
    }
}
