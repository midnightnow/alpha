/**
 * Mathman in Flatland v103.0 - "The Vitruvian Arc"
 * Tree of Life | Flower of Life | 12x12 Harmonic | Arc Paths
 */

class MathmanFlatland {
    takeSnapshot() {
        const link = document.createElement('a');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        link.download = `mathman-field-capture-${timestamp}.png`;
        link.href = this.canvas.toDataURL('image/png', 1.0);
        link.click();
    }

    exportResearchData() {
        const data = {
            "@context": "https://schema.org",
            "@type": "MedicalEntity",
            "name": "Mathman Interference Field State",
            "datePublished": new Date().toISOString(),
            "parameters": this.params,
            "anatomicalLevels": this.anatomicalLevels,
            "haricPoints": this.haricPoints,
            "sephiroticNodes": this.sephiroticNodes
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/ld+json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `mathman-research-data-${new Date().getTime()}.jsonld`;
        link.click();
        URL.revokeObjectURL(url);
    }
    constructor() {
        this.canvas = document.getElementById('visualizer');
        this.ctx = this.canvas.getContext('2d');

        const get = (id) => document.getElementById(id);
        this.controls = {
            separation: get('separation'),
            cOffset: get('c-offset'),
            scanHeight: get('scan-height'),
            nestDepth: get('nest-depth'),
            chakraSelector: get('chakra-selector'),
            alphaLogos: get('alpha-logos'),
            divineX: get('divine-x'),
            omegaPathos: get('omega-pathos'),
            wavelength: get('wavelength'),
            phiB: get('phase-offset-b'),
            phiC: get('phase-offset-c'),
            brightness: get('wave-brightness'),
            nodeSize: get('node-size'),
            weight: get('wave-weight'),
            threshold: get('field-threshold'),
            nodalBudget: get('nodal-budget'),
            zoomSlider: get('global-zoom'),
            triggerPulse: get('trigger-pulse'),
            boundaryDrift: get('boundary-drift'),
            resonanceLock: get('resonance-lock'),
            showOracle: get('show-oracle'),
            showMathman: get('show-mathman'),
            showField: get('show-field'),
            showProportions: get('show-proportions'),
            showTopDown: get('show-topdown'),
            primePulse: get('prime-pulse'),
            mirrorFactor: get('mirror-factor'),
            quaternionMode: get('quaternion-mode'),
            resonanceLock: get('resonance-lock'),
            showGrid: get('show-grid'),
            gridOpacity: get('grid-opacity'),
            layerFoundation: get('layer-foundation'),
            layerFlower: get('layer-flower'),
            layerEarthMoon: get('layer-earthmoon'),
            layerCipher: get('layer-cipher'),
            layerDivine7: get('layer-divine7'),
            layerPrime24: get('layer-prime24'),
            layerPlatonic: get('layer-platonic'),
            layerSephiroth: get('layer-sephiroth'),
            layerHarmonic: get('layer-harmonic'),
            layerVitruvian: get('layer-vitruvian'),
            layerHaric: get('layer-haric'),
            layerCoreStar: get('layer-core-star'),
            layerMucus: get('layer-mucus'),
            layerAnnotations: get('layer-annotations'),
            // Projection Mode Controls
            projectionMode: get('projection-mode'),
            layerSeparation: get('layer-separation'),
            // Genesis Controls
            btnGenesis: get('btn-genesis'),
            genesisOverlay: get('genesis-overlay'),
            genesisText: get('genesis-text'),
            // Research Presets
            btnPresetGround: get('btn-preset-ground'),
            btnPresetExpand: get('btn-preset-expand')
        };

        // Initialize Hardcard (Ceramic Math)
        if (typeof Hardcard !== 'undefined') {
            this.hardcard = new Hardcard();
        }

        this.constants = {
            SQRT_42: 6.4807406984, // Material Plane / Navel (Substantiation)
            SQRT_51: 7.1414284285, // Resonant Sphere / Heart (Elevation)
        };

        this.anatomicalLevels = [
            { id: 1, name: "Root (Coccyx)", y: 0.0, freq: "C" },
            { id: 2, name: "Sacral (Pubic)", y: 1.2, freq: "D" },
            { id: 3, name: "Solar Plexus (T12)", y: 4.2, freq: "E" }, // 4.2 Matches √42 resonance
            { id: 4, name: "Heart (T5)", y: 4.8, freq: "F" },
            { id: 5, name: "Throat (C3)", y: 5.8, freq: "G" },
            { id: 6, name: "Brow (Center Head)", y: 6.5, freq: "A" },
            { id: 7, name: "Crown (Top Head)", y: 7.0, freq: "B" },
        ];

        this.haricPoints = {
            idPoint: 11.3,
            soulSeat: 5.0,
            tanTien: 3.54,
            coreStar: 3.95,
            earthCore: -200
        };

        this.sephiroticNodes = [
            { name: 'Kether', id: 'K', x: 0, y: 7.0 },
            { name: 'Chokmah', id: 'C', x: 1.2, y: 6.0 },
            { name: 'Binah', id: 'B', x: -1.2, y: 6.0 },
            { name: 'Chesed', id: 'Ch', x: 3.5, y: 5.2 },
            { name: 'Geburah', id: 'G', x: -3.5, y: 5.2 },
            { name: 'Tiphareth', id: 'T', x: 0, y: 4.32 },
            { name: 'Netzach', id: 'N', x: 3.0, y: 1.5 },
            { name: 'Hod', id: 'H', x: -3.0, y: 1.5 },
            { name: 'Yesod', id: 'Y', x: 0, y: 3.2 },
            { name: 'Malkuth', id: 'M', x: 0, y: 0 },
        ];

        this.params = {
            distAB: 1.2, distC: 12, scanY: 4.2, nest: 3, chakra: 4,
            alpha: 0.73, divineX: 2.4, omega: 0.571, lambda: 1.0,
            phiB: 0, phiC: 0, brightness: 0.3, nodeSize: 0.5, weight: 1.0,
            threshold: 0.15, // Reduced from 0.3 to match parallel version
            budget: 2000,    // Increased from 1400 to match parallel version
            zoom: 0.9,       // Adjusted from 0.85
            gridOp: 0.6,
            pulseIntensity: 0, layerSep: 2.0
        };

        // Layer Z-depths for Projection Mode (Plato's Cave)
        // Each layer emanates from origin point at Z = -layerSep * 11
        this.layerDepths = {
            origin: -22,       // The "light source" / zero point
            foundation: 0,     // Layer 0: Vitruvian Man
            flower: 1,         // Layer 1: Flower of Life
            earthMoon: 2,      // Layer 2: Earth-Moon proportions
            cipher: 3,         // Layer 3: 10-24-26 Triangle
            divine7: 4,        // Layer 4: Heptagon/Spiral
            prime24: 5,        // Layer 5: Prime Lattice
            platonic: 6,       // Layer 6: Platonic Solids
            sephiroth: 7,      // Layer 7: Tree of Life
            harmonic: 8,       // Layer 8: 432Hz Spine
            vitruvian: 9,      // Layer 9: Vitruvian Skeleton
            merkaba: 10        // Layer 10: Merkaba
        };

        // Camera state - controls zoom, pan, and rotation
        this.camera = {
            zoom: 0.85,
            x: 0,
            y: 0,
            yaw: 0,
            pitch: 0,
            isRotating: false,
            isPanning: false,
            lx: 0,
            ly: 0
        };

        // Research Controls
        const btnSnapshot = get('btn-snapshot');
        const btnExport = get('btn-export');

        if (btnSnapshot) btnSnapshot.onclick = () => this.takeSnapshot();
        if (btnExport) btnExport.onclick = () => this.exportResearchData();

        this.drawLeonardo.drawPrimeClock = (origins) => this._drawPrimeClock(origins || this.getOrigins());

        // Load Vitruvian Image
        this.vitruvianImg = new Image();
        this.vitruvianImg.src = 'vitruvian.png';
        this.vitruvianImg.onload = () => {
            console.log('Vitruvian image loaded');
            this.init();
        };
        this.vitruvianImg.onerror = () => {
            console.error('Failed to load Vitruvian image');
            this.init(); // Start anyway
        };
    }

    init() {
        if (this.initialized) return; // Prevent double init
        this.initialized = true;

        this.resize();
        window.onresize = () => this.resize();
        this.setupEventListeners();
        this.setupCameraEvents();
        this.syncInitialUI();
        this.animate();
    }

    syncInitialUI() {
        const updateText = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
        Object.keys(this.controls).forEach(key => {
            const ctrl = this.controls[key];
            if (ctrl && ctrl.type === 'range') {
                const paramMap = {
                    separation: 'distAB', cOffset: 'distC', scanHeight: 'scanY', nestDepth: 'nest',
                    alphaLogos: 'alpha', divineX: 'divineX', omegaPathos: 'omega', wavelength: 'lambda',
                    phiB: 'phiB', phiC: 'phiC', brightness: 'brightness', nodeSize: 'nodeSize',
                    weight: 'weight', threshold: 'threshold', nodalBudget: 'budget', gridOpacity: 'gridOp'
                };
                const valIdMap = {
                    separation: 'dist-val', cOffset: 'c-offset-val', scanHeight: 'height-val', nestDepth: 'depth-val',
                    alphaLogos: 'alpha-val', divineX: 'divine-x-val', omegaPathos: 'omega-pathos-val', wavelength: 'wave-val',
                    phiB: 'phi-val', phiC: 'phi-val-c', brightness: 'bright-val', nodeSize: 'node-size-val',
                    weight: 'weight-val', threshold: 'thresh-val', nodalBudget: 'budget-val', gridOpacity: 'grid-val'
                };
                const pk = paramMap[key];
                if (pk) {
                    ctrl.value = this.params[pk];
                    const mult = pk === 'distAB' ? 10 : 1;
                    const fix = (pk === 'alpha' || pk === 'brightness' || pk === 'threshold') ? 2 : (pk === 'omega' ? 3 : 1);
                    updateText(valIdMap[key], (this.params[pk] * mult).toFixed(fix));
                }
            }
        });
    }

    setupEventListeners() {
        const updateText = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
        const setupCtrl = (ctrl, pKey, labelId, mult = 1, fixed = 1) => {
            if (!ctrl) return;
            ctrl.oninput = (e) => {
                const val = parseFloat(e.target.value);
                this.params[pKey] = val;
                if (labelId) updateText(labelId, (val * mult).toFixed(fixed));
            };
        };

        setupCtrl(this.controls.separation, 'distAB', 'dist-val', 10);
        setupCtrl(this.controls.cOffset, 'distC', 'c-offset-val');
        setupCtrl(this.controls.scanHeight, 'scanY', 'height-val');
        setupCtrl(this.controls.nestDepth, 'nest', 'depth-val', 1, 0);
        setupCtrl(this.controls.alphaLogos, 'alpha', 'alpha-val', 1, 2);
        setupCtrl(this.controls.divineX, 'divineX', 'divine-x-val');
        setupCtrl(this.controls.omegaPathos, 'omega', 'omega-pathos-val', 1, 3);
        setupCtrl(this.controls.wavelength, 'lambda', 'wave-val', 1, 2);
        setupCtrl(this.controls.phiB, 'phiB', 'phi-val', 1, 0);
        setupCtrl(this.controls.phiC, 'phiC', 'phi-val-c', 1, 0);
        setupCtrl(this.controls.brightness, 'brightness', 'bright-val', 1, 2);
        setupCtrl(this.controls.nodeSize, 'nodeSize', 'node-size-val', 1, 2);
        setupCtrl(this.controls.weight, 'weight', 'weight-val');
        setupCtrl(this.controls.threshold, 'threshold', 'thresh-val', 1, 2);
        setupCtrl(this.controls.nodalBudget, 'budget', 'budget-val', 1, 0);
        setupCtrl(this.controls.gridOpacity, 'gridOp', 'grid-val');

        if (this.controls.zoomSlider) this.controls.zoomSlider.oninput = (e) => { this.camera.zoom = parseFloat(e.target.value); updateText('zoom-val', this.camera.zoom.toFixed(1)); };

        if (this.controls.chakraSelector) {
            this.controls.chakraSelector.onchange = (e) => {
                const cMap = [0, 0, 1.5, 3.2, 4.32, 5.2, 6.0, 7.0];
                this.params.scanY = -cMap[parseInt(e.target.value)]; // Use negative for Y-up
                this.controls.scanHeight.value = Math.abs(this.params.scanY);
                updateText('height-val', Math.abs(this.params.scanY).toFixed(1));
            };
        }

        if (this.controls.triggerPulse) { this.controls.triggerPulse.onclick = () => { this.params.pulseIntensity = 1.0; }; }

        // Layer Separation slider for Projection Mode
        if (this.controls.layerSeparation) {
            this.controls.layerSeparation.oninput = (e) => {
                this.params.layerSep = parseFloat(e.target.value);
                updateText('layer-sep-val', this.params.layerSep.toFixed(1));
            };
        }

        if (this.controls.boundaryDrift) {
            this.controls.boundaryDrift.oninput = (e) => {
                updateText('drift-val', parseFloat(e.target.value).toFixed(2));
            };
        }

        if (this.controls.btnGenesis) {
            this.controls.btnGenesis.onclick = () => this.runGenesis();
        }

        if (this.controls.btnPresetGround) {
            this.controls.btnPresetGround.onclick = () => this.applyPreset('grounding');
        }

        if (this.controls.btnPresetExpand) {
            this.controls.btnPresetExpand.onclick = () => this.applyPreset('expansion');
        }
    }
    // Get Z-offset for a layer in Projection Mode (Plato's Cave view)
    getLayerZ(layerName) {
        if (!this.controls.projectionMode?.checked) return 0;
        const depth = this.layerDepths[layerName] || 0;
        return depth * this.params.layerSep;
    }

    // Draw projection rays from origin to all layers (visible in side view)
    drawProjectionRays(origins) {
        if (!this.controls.projectionMode?.checked) return;

        const sep = this.params.layerSep;
        const originZ = this.layerDepths.origin * sep;
        const maxLayerZ = 10 * sep;

        this.ctx.save();
        this.ctx.strokeStyle = 'rgba(255, 200, 100, 0.15)';
        this.ctx.lineWidth = 0.5;

        // Draw rays from origin point to corners of each layer plane
        const rayTargets = [
            { x: -4, y: -7 }, { x: 4, y: -7 },
            { x: -4, y: 0 }, { x: 4, y: 0 },
            { x: 0, y: -3.5 } // Center
        ];

        rayTargets.forEach(target => {
            const pOrigin = this.project(0, -3.5, originZ, origins);
            const pTarget = this.project(target.x, target.y, maxLayerZ, origins);
            this.ctx.beginPath();
            this.ctx.moveTo(pOrigin.x, pOrigin.y);
            this.ctx.lineTo(pTarget.x, pTarget.y);
            this.ctx.stroke();
        });

        // Draw the origin point (the "light" / zero point / Plato's fire)
        const pZero = this.project(0, -3.5, originZ, origins);
        this.ctx.fillStyle = 'rgba(255, 220, 100, 0.9)';
        this.ctx.shadowBlur = 20;
        this.ctx.shadowColor = 'rgba(255, 200, 50, 0.8)';
        this.ctx.beginPath();
        this.ctx.arc(pZero.x, pZero.y, 8, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.shadowBlur = 0;

        // Label the origin
        this.ctx.fillStyle = 'rgba(255, 220, 100, 0.9)';
        this.ctx.font = 'bold 11px Space Grotesk';
        this.ctx.fillText('ORIGIN (Zero Point)', pZero.x + 15, pZero.y + 4);

        this.ctx.restore();
    }

    setupCameraEvents() {
        this.canvas.onmousedown = (e) => {
            // Left Click (0) = Rotate, Right Click (2) or Shift+Left = Pan
            if (e.button === 2 || (e.button === 0 && e.shiftKey)) {
                this.camera.isPanning = true;
                this.camera.lx = e.clientX;
                this.camera.ly = e.clientY;
                e.preventDefault();
            } else if (e.button === 0) {
                this.camera.isRotating = true;
                this.camera.lx = e.clientX;
                this.camera.ly = e.clientY;
            }
        };
        // Disable context menu for right-click panning
        this.canvas.oncontextmenu = (e) => e.preventDefault();

        window.onmousemove = (e) => {
            if (!this.camera.isPanning && !this.camera.isRotating) return;
            const dx = e.clientX - this.camera.lx;
            const dy = e.clientY - this.camera.ly;

            if (this.camera.isPanning) {
                // Adjust pan sensitivity
                this.camera.x += dx * 1.5;
                this.camera.y += dy * 1.5;
            } else if (this.camera.isRotating) {
                this.camera.yaw += dx * 0.005;
                this.camera.pitch = Math.max(-1.5, Math.min(1.5, this.camera.pitch + dy * 0.005));
            }
            this.camera.lx = e.clientX;
            this.camera.ly = e.clientY;
        };

        window.onmouseup = () => {
            this.camera.isPanning = false;
            this.camera.isRotating = false;
        };

        this.canvas.onwheel = (e) => {
            e.preventDefault();
            // Zoom at mouse pointer logic could be added, but keeping simple zoom for now
            const zoomSpeed = 0.001;
            this.camera.zoom = Math.max(0.1, Math.min(10, this.camera.zoom - e.deltaY * zoomSpeed * this.camera.zoom));
            if (this.controls.zoomSlider) this.controls.zoomSlider.value = this.camera.zoom;
        };
    }

    resize() {
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = this.canvas.parentElement.clientWidth * dpr; this.canvas.height = this.canvas.parentElement.clientHeight * dpr;
        this.ctx.scale(dpr, dpr);
    }

    project(px, py, pz, origins) {
        const { cx, cy, mm } = origins;
        if (this.controls.showTopDown.checked) return { x: cx + px * mm, y: cy + py * mm, z: 0 };
        let x = px * Math.cos(this.camera.yaw) - pz * Math.sin(this.camera.yaw);
        let z = px * Math.sin(this.camera.yaw) + pz * Math.cos(this.camera.yaw);
        let y = py * Math.cos(this.camera.pitch) - z * Math.sin(this.camera.pitch);
        z = py * Math.sin(this.camera.pitch) + z * Math.cos(this.camera.pitch);
        const f = 800 / (800 + z * mm);
        return { x: cx + x * mm * f, y: cy + y * mm * f, z: z };
    }

    getOrigins() {
        const cw = this.canvas.width / devicePixelRatio, ch = this.canvas.height / devicePixelRatio;
        const mm = (ch * 0.07) * this.camera.zoom;
        let cx = cw / 2 + this.camera.x, cy = ch * 0.8 + this.camera.y;
        const hD = (this.params.distAB * 10) / 2;

        if (this.genesisRunning) {
            // Anchor Point A visually at the center by offsetting the projection
            cx += hD * mm;
        }

        return { a: { x: -hD, y: 0, z: 0 }, b: { x: hD, y: 0, z: 0 }, c: { x: 0, y: -this.params.distC, z: 0 }, cx, cy, mm };
    }

    getIntensity(x, y, z, origins, k, time, returnObject = false) {
        const { a, b, c } = origins;
        let ox = x, oy = y, oz = z;
        if (this.controls.mirrorFactor.checked) ox = Math.abs(x);
        if (this.controls.quaternionMode.checked) { ox = Math.abs(x); oy = Math.abs(y); }
        const da = Math.sqrt((ox - a.x) ** 2 + (oy - a.y) ** 2 + (oz - a.z) ** 2);
        const db = Math.sqrt((ox - b.x) ** 2 + (oy - b.y) ** 2 + (oz - b.z) ** 2);
        const dc = Math.sqrt((ox - c.x) ** 2 + (oy - c.y) ** 2 + (oz - c.z) ** 2);
        const pulse = Math.sin(time * 0.5);
        const ia = Math.cos(k * da) * pulse;
        const ib = Math.cos(k * db + this.params.phiB * Math.PI / 180) * pulse;
        const ic = Math.cos(k * dc + this.params.phiC * Math.PI / 180) * pulse;
        let total = (ia + ib + ic) / 3;

        // Calculate Stagnation (Auric Mucus)
        // Now reinforced by Hardcard Resonance Tolerance
        const potential = (Math.abs(ia) + Math.abs(ib) + Math.abs(ic)) / 3;
        let stagnation = Math.max(0, potential - Math.abs(total));

        if (this.hardcard && this.controls.boundaryDrift) {
            const tolerance = this.hardcard.calculateResonanceTolerance(parseFloat(this.controls.boundaryDrift.value));
            // Invert tolerance: High tolerance = low mucus
            stagnation += (1.0 - tolerance) * 0.5;
        }

        const result = total + this.params.pulseIntensity * (Math.random() - 0.5) * 0.4;

        // APPLY HARDCARD REINFORCEMENT (The 5th Element)
        // Injecting the remainder_delay to prevent phase erosion of the "Standing Man"
        let reinforcedIntensity = result;
        if (this.hardcard) {
            const delay = this.hardcard.calculateRemainderDelay(time, result);
            reinforcedIntensity += delay;
        }

        // For backwards compatibility, if returnObject is false, return the number
        return returnObject ? { intensity: reinforcedIntensity, stagnation } : reinforcedIntensity;
    }

    drawLeonardo(origins) {
        const time = performance.now() / 1000;
        this.ctx.save();

        // Draw projection rays first (behind all layers)
        this.drawProjectionRays(origins);

        // LAYER: Foundation (Vitruvian Background Image)
        if (this.controls.layerFoundation?.checked && this.vitruvianImg && this.vitruvianImg.complete) {
            const zOffset = this.getLayerZ('foundation');
            this.ctx.globalAlpha = 0.15;
            const imgW = 9.0;
            const imgH = 9.0 * (this.vitruvianImg.height / this.vitruvianImg.width);
            const pCenter = this.project(0, -3.5, zOffset, origins);
            const scale = origins.mm * (imgW / this.vitruvianImg.width);

            this.ctx.save();
            this.ctx.translate(pCenter.x, pCenter.y);
            this.ctx.scale(scale, scale);
            this.ctx.drawImage(this.vitruvianImg, -this.vitruvianImg.width / 2, -this.vitruvianImg.height / 2);
            this.ctx.restore();
            this.ctx.globalAlpha = 1.0;
        }

        if (!this.controls.showProportions.checked) {
            this.ctx.restore();
            return;
        }

        // --- DESIGN AESTHETICS: COLOR PALETTE ---
        const palette = {
            gold: 'rgba(255, 215, 0, 0.8)',
            goldDim: 'rgba(255, 215, 0, 0.4)',
            cyan: 'rgba(0, 220, 255, 0.8)',
            cyanGlow: 'rgba(0, 220, 255, 0.4)',
            magenta: 'rgba(255, 100, 255, 0.8)',
            magentaDim: 'rgba(255, 100, 255, 0.3)',
            glass: 'rgba(255, 255, 255, 0.1)',
            textMain: 'rgba(255, 255, 255, 0.9)',
            textDim: 'rgba(200, 200, 200, 0.7)',
            pyramidFill: 'rgba(240, 220, 180, 0.15)',
            pyramidStroke: 'rgba(255, 200, 100, 0.6)'
        };

        const scribe = (col, wid) => { this.ctx.strokeStyle = col; this.ctx.lineWidth = wid; };
        // const time = performance.now() / 1000; // Already defined above

        // LAYER: Flower of Life Grid
        if (this.controls.layerFlower?.checked) {
            const zOffset = this.getLayerZ('flower');
            const rad = 1.0;
            scribe('rgba(139, 69, 19, 0.15)', 0.8);
            for (let j = -8; j <= 2; j++) {
                for (let i = -7; i <= 7; i++) {
                    const off = (j % 2 === 0) ? 0 : rad * 0.866;
                    const fx = i * rad * 1.732 + off;
                    const fy = j * rad * 1.5;
                    if (Math.abs(fx) < 8 && Math.abs(fy) < 13) {
                        this.ctx.beginPath();
                        for (let k = 0; k <= 24; k++) {
                            const a = (k / 24) * Math.PI * 2;
                            const p = this.project(fx + Math.cos(a) * rad, fy + Math.sin(a) * rad, zOffset, origins);
                            if (k === 0) this.ctx.moveTo(p.x, p.y); else this.ctx.lineTo(p.x, p.y);
                        }
                        this.ctx.stroke();
                    }
                }
            }
        }

        // LAYER: Earth-Moon Proportions (New Jerusalem / Squaring the Circle)
        if (this.controls.layerEarthMoon?.checked) {
            const zOffset = this.getLayerZ('earthMoon');
            const sEarth = 7.0;
            const dMoon = sEarth * (2160 / 7920);
            const rOuter = (sEarth / 2) + (dMoon / 2);

            // Earth Square (7x7)
            scribe(palette.glass, 2.0);
            const sq = [[-3.5, 0], [3.5, 0], [3.5, -7], [-3.5, -7]].map(p => this.project(p[0], p[1], zOffset, origins));
            this.ctx.beginPath(); this.ctx.moveTo(sq[0].x, sq[0].y); sq.forEach(p => this.ctx.lineTo(p.x, p.y));
            this.ctx.closePath(); this.ctx.stroke();

            // Outer Squaring Circle
            scribe(palette.cyanGlow, 1.2);
            this.ctx.setLineDash([8, 4]);
            const pOC = this.project(0, -3.5, zOffset, origins);
            this.ctx.beginPath(); this.ctx.arc(pOC.x, pOC.y, rOuter * origins.mm, 0, Math.PI * 2); this.ctx.stroke();
            this.ctx.setLineDash([]);

            // Moon Circle
            scribe(palette.glass, 1.5);
            const pMC = this.project(0, -(sEarth + dMoon / 2), zOffset, origins);
            this.ctx.beginPath(); this.ctx.arc(pMC.x, pMC.y, (dMoon / 2) * origins.mm, 0, Math.PI * 2); this.ctx.stroke();

            // Giza Pyramid (Golden Ratio)
            const pyrAngle = 51.843 * Math.PI / 180;
            const pyrH = 7.0;
            const pyrBaseHalf = pyrH / Math.tan(pyrAngle);
            const pPyrApex = this.project(0, -7.0, zOffset, origins);
            const pPyrBL = this.project(-pyrBaseHalf, 0, zOffset, origins);
            const pPyrBR = this.project(pyrBaseHalf, 0, zOffset, origins);

            this.ctx.fillStyle = palette.pyramidFill;
            this.ctx.beginPath();
            this.ctx.moveTo(pPyrApex.x, pPyrApex.y);
            this.ctx.lineTo(pPyrBL.x, pPyrBL.y);
            this.ctx.lineTo(pPyrBR.x, pPyrBR.y);
            this.ctx.closePath();
            this.ctx.fill();
            scribe(palette.pyramidStroke, 1.5);
            this.ctx.stroke();

            // Vesica Piscis (Portal)
            const vRad = 2.5;
            const vCX = 0, vCY = -3.5;
            const vPulse = 0.15 + 0.1 * Math.sin(time * 1.2);
            const vpCenter = this.project(vCX, vCY, zOffset, origins);
            const gradient = this.ctx.createRadialGradient(vpCenter.x, vpCenter.y, 0, vpCenter.x, vpCenter.y, vRad * origins.mm);
            gradient.addColorStop(0, `rgba(255, 100, 255, ${vPulse})`);
            gradient.addColorStop(0.5, `rgba(255, 100, 255, ${vPulse * 0.5})`);
            gradient.addColorStop(1, 'rgba(255, 100, 255, 0)');
            this.ctx.save();
            this.ctx.fillStyle = gradient;
            this.ctx.fillRect(vpCenter.x - vRad * origins.mm, vpCenter.y - vRad * origins.mm, vRad * 2 * origins.mm, vRad * 2 * origins.mm);
            this.ctx.restore();

            scribe(`rgba(255, 100, 255, ${0.4 + vPulse})`, 1.5);
            const vpL = this.project(vCX - vRad / 2, vCY, zOffset, origins);
            this.ctx.beginPath(); this.ctx.arc(vpL.x, vpL.y, vRad * origins.mm, 0, Math.PI * 2); this.ctx.stroke();
            const vpR = this.project(vCX + vRad / 2, vCY, zOffset, origins);
            this.ctx.beginPath(); this.ctx.arc(vpR.x, vpR.y, vRad * origins.mm, 0, Math.PI * 2); this.ctx.stroke();
        }


        // LAYER: 10-24-26 Cipher Triangle (Robert Edward Grant)
        if (this.controls.layerCipher?.checked) {
            const zOffset = this.getLayerZ('cipher');
            scribe(palette.gold, 2);
            const pApex = this.project(0, -7.0, zOffset, origins);
            const pFootL = this.project(-3.0, 0, zOffset, origins);
            const pFootR = this.project(3.0, 0, zOffset, origins);
            this.ctx.beginPath();
            this.ctx.moveTo(pApex.x, pApex.y);
            this.ctx.lineTo(pFootL.x, pFootL.y);
            this.ctx.lineTo(pFootR.x, pFootR.y);
            this.ctx.closePath();
            this.ctx.stroke();

            // Cipher labels (annotations layer controls these texts)
            if (this.controls.layerAnnotations?.checked) {
                const trinityPulse = 0.7 + 0.3 * Math.sin(time * 2);
                this.ctx.shadowBlur = 15;
                this.ctx.shadowColor = `rgba(255, 215, 0, ${trinityPulse})`;
                this.ctx.fillStyle = palette.gold;
                this.ctx.font = 'bold 13px Space Grotesk';
                const drawTextZ = (t, x, y) => { const p = this.project(x, y, zOffset, origins); this.ctx.fillText(t, p.x, p.y); };
                drawTextZ("10 [MATHS]", -0.7, 0.4);
                drawTextZ("24 [MEASURES]", -1.8, -2.8);
                drawTextZ("26 [LANGUAGE]", 1.6, -2.8);
                this.ctx.shadowBlur = 0;

                this.ctx.fillStyle = 'rgba(200, 255, 200, 0.9)';
                this.ctx.font = '11px Space Grotesk';
                drawTextZ("V = a + 2b + c (Projection Theorem)", -1.5, -6.5);
                drawTextZ("Validation: V - E + F = 2", -1.5, -6.2);
                this.ctx.fillStyle = palette.magenta;
                drawTextZ("Unity Harmonica: Electrum Regime", 1.8, -6.5);
                this.ctx.fillStyle = 'rgba(100, 255, 255, 0.8)';
                this.ctx.font = '10px Space Grotesk';
                drawTextZ("Universal Constant: 1 / .137... = 7.29...", 1.8, -6.2);

                const shimmer = 0.85 + 0.15 * Math.sin(time * 1.5);
                this.ctx.fillStyle = `rgba(255, 255, 255, ${shimmer})`;
                this.ctx.font = '14px Space Grotesk';
                drawTextZ("Infinite DELTA", -3.2, -4.8);
                drawTextZ("Infinite SUM", 2.2, -4.8);
                this.ctx.font = '11px Space Grotesk';
                drawTextZ("Δ = (Σ/2)² / (∞!)²", -3.2, -4.2);
                drawTextZ("Σ ∞ / 2", 2.2, -4.2);
                this.ctx.fillStyle = `rgba(200, 255, 255, ${shimmer})`;
                drawTextZ("= 1/.26", -1.8, -3.5);
                drawTextZ("= 1/.24", 0.8, -3.5);
                drawTextZ("= 1/.312", -2.5, 0.5);
                drawTextZ("= √624 = 24.979", 1.2, 0.5);
                this.ctx.font = 'italic 10px Space Grotesk';
                drawTextZ("A Mirrored Reciprocal Inverse Symmetry", -1.8, -1.2);
            }
        }

        // Helper for text drawing (with current layer Z)
        let currentLayerZ = 0;
        const drawText = (t, x, y) => { const p = this.project(x, y, currentLayerZ, origins); this.ctx.fillText(t, p.x, p.y); };

        // LAYER: Divine 7 (Heptagon + Spiral + Heptagram)
        if (this.controls.layerDivine7?.checked) {
            const zOffset = this.getLayerZ('divine7');
            currentLayerZ = zOffset;

            // Perfect Heptagon
            const hGlow = 0.6 + 0.4 * Math.sin(time * 3.5);
            const heptRot = time * 0.05;
            scribe(`rgba(0, 220, 255, ${hGlow})`, 2.5);
            const hRad = 2.68;
            const hCenter = { x: 0, y: -4.32 };
            this.ctx.beginPath();
            for (let i = 0; i < 7; i++) {
                const a = (i * 2 * Math.PI / 7) - Math.PI / 2 + heptRot;
                const p = this.project(hCenter.x + Math.cos(a) * hRad, hCenter.y + Math.sin(a) * hRad, zOffset, origins);
                if (i === 0) this.ctx.moveTo(p.x, p.y); else this.ctx.lineTo(p.x, p.y);
            }
            this.ctx.closePath();
            this.ctx.stroke();

            if (this.controls.layerAnnotations?.checked) {
                this.ctx.shadowBlur = 10;
                this.ctx.shadowColor = `rgba(0, 240, 255, ${hGlow})`;
                this.ctx.fillStyle = `rgba(0, 240, 255, ${hGlow})`;
                this.ctx.font = 'bold 13px Space Grotesk';
                const pRatioLabel = this.project(1.4, -2.1, zOffset, origins);
                this.ctx.fillText("0.867 (Divine)", pRatioLabel.x, pRatioLabel.y);
                this.ctx.shadowBlur = 0;
            }

            // Fibonacci Golden Spiral
            scribe('rgba(255, 215, 0, 0.3)', 1.2);
            const phi = 1.618033988749;
            const spiralCenter = { x: 0, y: -4.32 };
            const spiralRot = time * 0.015;
            this.ctx.beginPath();
            let r = 0.08;
            let theta = spiralRot;
            const spiralStart = this.project(spiralCenter.x + r * Math.cos(theta), spiralCenter.y + r * Math.sin(theta), zOffset, origins);
            this.ctx.moveTo(spiralStart.x, spiralStart.y);
            for (let i = 0; i < 180; i++) {
                theta += 0.12;
                r = 0.08 * Math.pow(phi, theta / (2 * Math.PI));
                if (r > 3.5) break;
                const p = this.project(spiralCenter.x + r * Math.cos(theta + spiralRot), spiralCenter.y + r * Math.sin(theta + spiralRot), zOffset, origins);
                this.ctx.lineTo(p.x, p.y);
            }
            this.ctx.stroke();

            if (this.controls.layerAnnotations?.checked) {
                this.ctx.fillStyle = 'rgba(255, 215, 0, 0.6)';
                this.ctx.font = 'italic 9px Space Grotesk';
                drawText("φ = 1.618...", -2.8, -4.5);
            }

            // Heptagram at Feet
            const heptagramRot = time * 0.025;
            scribe(palette.cyanGlow, 1.4);
            const drawHeptagram = (cx, cy, rH) => {
                this.ctx.beginPath();
                for (let i = 0; i < 7; i++) {
                    const a1 = (i * 2 * Math.PI / 7) - Math.PI / 2 + heptagramRot;
                    const a2 = ((i + 2) * 2 * Math.PI / 7) - Math.PI / 2 + heptagramRot;
                    const p1 = this.project(cx + Math.cos(a1) * rH, cy + Math.sin(a1) * rH, zOffset, origins);
                    const p2 = this.project(cx + Math.cos(a2) * rH, cy + Math.sin(a2) * rH, zOffset, origins);
                    if (i === 0) this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                }
                this.ctx.closePath(); this.ctx.stroke();
            };
            drawHeptagram(0, 0, 1.8);
        }
        // LAYER: Platonic Solids (Nested Cubes)
        if (this.controls.layerPlatonic?.checked) {
            const cubeRot = time * 0.06;
            const drawCube = (size, color, rotSpeed) => {
                const rot = cubeRot * rotSpeed;
                const pts = [
                    { x: -size, y: -size, z: -size }, { x: size, y: -size, z: -size },
                    { x: size, y: size, z: -size }, { x: -size, y: size, z: -size },
                    { x: -size, y: -size, z: size }, { x: size, y: -size, z: size },
                    { x: size, y: size, z: size }, { x: -size, y: size, z: size }
                ];
                const rotatedPts = pts.map(p => ({
                    x: p.x * Math.cos(rot) - p.z * Math.sin(rot),
                    y: p.y,
                    z: p.x * Math.sin(rot) + p.z * Math.cos(rot)
                }));
                const projected = rotatedPts.map(p => this.project(p.x, p.y, p.z, origins));
                const edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
                this.ctx.strokeStyle = color;
                this.ctx.lineWidth = 1.2;
                edges.forEach(([i, j]) => {
                    this.ctx.beginPath();
                    this.ctx.moveTo(projected[i].x, projected[i].y);
                    this.ctx.lineTo(projected[j].x, projected[j].y);
                    this.ctx.stroke();
                });
            };
            drawCube(1.2, 'rgba(150, 200, 255, 0.7)', 1.0);
            drawCube(0.8, 'rgba(150, 255, 200, 0.6)', -1.3);
            drawCube(0.4, 'rgba(255, 150, 200, 0.5)', 0.7);
        }
        // LAYER: Harmonic Spine (432Hz)
        if (this.controls.layerHarmonic?.checked) {
            this.ctx.fillStyle = 'rgba(255, 180, 50, 0.9)';
            this.ctx.font = 'bold 13px Space Grotesk';
            drawText("PRECISE TEMPERAMENT", -5.5, -1.5);
            this.ctx.font = '11px Space Grotesk';
            drawText("Seed: A4 = 432Hz / 216Hz", -5.5, -1.0);
            this.ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
            drawText("CUBE OF DELOS: 1.26³ = 2.0", -5.5, -0.5);
            drawText("Major 3rd Problem Solved: 1.26 CONSTANT", -5.5, 0.0);

            this.ctx.fillStyle = 'rgba(255, 215, 0, 0.9)';
            this.ctx.font = 'bold 11px Space Grotesk';
            const drawLabel = (txt, x, y) => { const p = this.project(x, y, 0, origins); this.ctx.fillText(txt, p.x, p.y); };
            drawLabel("432Hz (Zenith)", 4.5, -7.0);
            drawLabel("324Hz (Perfect 5th)", 4.5, -6.0);
            drawLabel("216Hz (A4 / Navel)", 4.5, -4.32);
            drawLabel("144Hz (D3 / Mid)", 4.5, -3.2);
            drawLabel("108Hz (Earth / Base)", 4.5, -1.0);
            drawLabel("54Hz (Ground)", 4.5, 0.0);
            this.ctx.fillStyle = 'rgba(255, 100, 255, 0.7)';
            drawText("Σ = 9 mod 9", 4.5, -7.5);
        }

        // LAYER: Sephirotic Graph (Tree of Life)
        if (this.controls.layerSephiroth?.checked) {
            const zOffset = this.getLayerZ('sephiroth');
            scribe(palette.gold, 2);

            // Draw Links (Paths)
            const drawLink = (id1, id2) => {
                const n1 = this.sephiroticNodes.find(n => n.id === id1);
                const n2 = this.sephiroticNodes.find(n => n.id === id2);
                if (n1 && n2) {
                    const p1 = this.project(n1.x, -n1.y, zOffset, origins);
                    const p2 = this.project(n2.x, -n2.y, zOffset, origins);
                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.stroke();
                }
            };

            // Traditional Tree of Life Paths
            drawLink('K', 'C'); drawLink('K', 'B'); drawLink('C', 'B');
            drawLink('C', 'Ch'); drawLink('B', 'G'); drawLink('C', 'T');
            drawLink('B', 'T'); drawLink('Ch', 'G'); drawLink('Ch', 'T');
            drawLink('G', 'T'); drawLink('Ch', 'N'); drawLink('G', 'H');
            drawLink('T', 'N'); drawLink('T', 'H'); drawLink('T', 'Y');
            drawLink('N', 'H'); drawLink('N', 'Y'); drawLink('H', 'Y');
            drawLink('Y', 'M');

            // Draw Nodes (Sephirot)
            this.sephiroticNodes.forEach(node => {
                const p = this.project(node.x, -node.y, zOffset, origins);
                this.ctx.fillStyle = palette.gold;
                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, 5 * p.scale, 0, Math.PI * 2);
                this.ctx.fill();

                if (this.controls.layerAnnotations?.checked) {
                    this.ctx.fillStyle = palette.textDim;
                    this.ctx.font = '10px Space Grotesk';
                    this.ctx.textAlign = 'center';
                    this.ctx.fillText(node.name, p.x, p.y - 10);
                }
            });
        }

        // LAYER: Haric Level & Core Star
        if (this.controls.layerHaric?.checked || this.controls.layerCoreStar?.checked) {
            const zOffset = this.getLayerZ('merkaba'); // Use deeper depth

            if (this.controls.layerHaric?.checked) {
                // Haric Line (Laser Line)
                const pTop = this.project(0, -this.haricPoints.idPoint, zOffset, origins);
                const pBot = this.project(0, 2, zOffset, origins); // Rooted in earth

                scribe('rgba(255, 215, 0, 0.6)', 3);
                this.ctx.beginPath();
                this.ctx.moveTo(pTop.x, pTop.y);
                this.ctx.lineTo(pBot.x, pBot.y);
                this.ctx.stroke();

                // ID Point (Inverted Funnel)
                const pID = this.project(0, -this.haricPoints.idPoint, zOffset, origins);
                this.ctx.fillStyle = 'rgba(200, 200, 255, 0.9)';
                this.ctx.beginPath();
                this.ctx.moveTo(pID.x - 5, pID.y - 10);
                this.ctx.lineTo(pID.x + 5, pID.y - 10);
                this.ctx.lineTo(pID.x, pID.y);
                this.ctx.fill();

                // Soul Seat (Diffuse Light)
                const pSS = this.project(0, -this.haricPoints.soulSeat, zOffset, origins);
                const ssGrad = this.ctx.createRadialGradient(pSS.x, pSS.y, 1, pSS.x, pSS.y, 15 * pSS.scale);
                ssGrad.addColorStop(0, 'rgba(180, 180, 255, 0.9)');
                ssGrad.addColorStop(1, 'rgba(180, 180, 255, 0.0)');
                this.ctx.fillStyle = ssGrad;
                this.ctx.beginPath();
                this.ctx.arc(pSS.x, pSS.y, 15 * pSS.scale, 0, Math.PI * 2);
                this.ctx.fill();

                // Tan Tien (Ball of Power)
                const pTT = this.project(0, -this.haricPoints.tanTien, zOffset, origins);
                this.ctx.fillStyle = '#ff4500';
                this.ctx.beginPath();
                this.ctx.arc(pTT.x, pTT.y, 6 * pTT.scale, 0, Math.PI * 2);
                this.ctx.fill();
                scribe('#ffd700', 2);
                this.ctx.stroke();
            }

            if (this.controls.layerCoreStar?.checked) {
                const pCS = this.project(0, -this.haricPoints.coreStar, zOffset, origins);
                this.ctx.save();
                this.ctx.translate(pCS.x, pCS.y);
                this.ctx.rotate(time * 0.2);

                const rays = 12;
                this.ctx.fillStyle = 'white';
                this.ctx.beginPath();
                for (let i = 0; i < rays * 2; i++) {
                    const rad = (i % 2 === 0) ? 20 * pCS.scale : 4 * pCS.scale;
                    const a = (i / (rays * 2)) * Math.PI * 2;
                    this.ctx.lineTo(Math.cos(a) * rad, Math.sin(a) * rad);
                }
                this.ctx.fill();

                const csGrad = this.ctx.createRadialGradient(0, 0, 2, 0, 0, 40 * pCS.scale);
                csGrad.addColorStop(0, 'rgba(255, 255, 255, 1)');
                csGrad.addColorStop(0.4, 'rgba(200, 240, 255, 0.5)');
                csGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
                this.ctx.fillStyle = csGrad;
                this.ctx.beginPath();
                this.ctx.arc(0, 0, 40 * pCS.scale, 0, Math.PI * 2);
                this.ctx.fill();
                this.ctx.restore();
            }
        }
        // 7. PYRAMID CONSTRUCTION (Already handled by filled pyramid above, removing old lines)

        // 8. SALVATOR MUNDI 'X' (138.157°)
        scribe(palette.glass, 2.2);
        const hC_sm = { x: 0, y: -4.32 }; const xL = 1.35; // Renamed hC to hC_sm to avoid conflict
        const xA = (138.157 - 90) * Math.PI / 180;
        const x1 = this.project(hC_sm.x - Math.cos(xA) * xL, hC_sm.y - Math.sin(xA) * xL, 0, origins);
        const x2 = this.project(hC_sm.x + Math.cos(xA) * xL, hC_sm.y + Math.sin(xA) * xL, 0, origins);
        const x3 = this.project(hC_sm.x - Math.cos(-xA) * xL, hC_sm.y - Math.sin(-xA) * xL, 0, origins);
        const x4 = this.project(hC_sm.x + Math.cos(-xA) * xL, hC_sm.y + Math.sin(-xA) * xL, 0, origins);
        this.ctx.beginPath(); this.ctx.moveTo(x1.x, x1.y); this.ctx.lineTo(x2.x, x2.y); this.ctx.stroke();
        this.ctx.beginPath(); this.ctx.moveTo(x3.x, x3.y); this.ctx.lineTo(x4.x, x4.y); this.ctx.stroke();

        // GOLDEN ANGLE ANNOTATION (137.5)
        scribe('rgba(255, 215, 0, 0.6)', 1.2);
        const gRad = 1.0;
        const gCenter = this.project(5.5, -4.32, 0, origins);
        this.ctx.beginPath();
        this.ctx.arc(gCenter.x, gCenter.y, gRad * origins.mm, 0, Math.PI * 2);
        this.ctx.stroke();
        const gA = (137.5 * Math.PI / 180) - Math.PI / 2;
        this.ctx.beginPath(); this.ctx.moveTo(gCenter.x, gCenter.y);
        this.ctx.lineTo(gCenter.x + Math.cos(gA) * gRad * origins.mm, gCenter.y + Math.sin(gA) * gRad * origins.mm);
        this.ctx.stroke();
        this.ctx.fillText("137.5° (Φ)", gCenter.x - 25, gCenter.y + gRad * origins.mm + 18);

        // Barycenter Shift (The 5th Element)
        // Moves between Platonic 4.0 and Harmonic 4.32 based on Resonance Lock
        let navelY = -4.32;
        if (this.controls.resonanceLock?.checked) {
            navelY = -4.0;
        } else if (this.hardcard) {
            // Add slight drift decay if unlocked
            navelY -= this.hardcard.getVitrificationDecay(time) * 0.1;
        }
        const bY = navelY;

        // LAYER: Vitruvian Skeleton
        if (this.controls.layerVitruvian?.checked) {
            const zOffset = this.getLayerZ('vitruvian');
            scribe('rgba(220, 150, 80, 1)', 3.0);
            this.ctx.shadowBlur = 20;
            this.ctx.shadowColor = 'rgba(220, 150, 80, 0.8)';
            const drawBody = (pose) => {
                const hY = -7.0, gY = -3.2;
                const pHead = this.project(0, hY, zOffset, origins), pGroin = this.project(0, gY, zOffset, origins);
                this.ctx.beginPath(); this.ctx.moveTo(pHead.x, pHead.y); this.ctx.lineTo(pGroin.x, pGroin.y); this.ctx.stroke();
                this.ctx.beginPath(); this.ctx.arc(pHead.x, pHead.y, 0.45 * origins.mm, 0, Math.PI * 2); this.ctx.stroke();
                [1, -1].forEach(side => {
                    const sY = -6.0, pS = this.project(0.9 * side, sY, zOffset, origins);
                    const iC = pose === 'circle';
                    const armT = iC ? { x: 3.5 * side, y: -5.4 } : { x: 3.5 * side, y: -6.4 };
                    const footT = iC ? { x: 2.2 * side, y: 0 } : { x: 0.5 * side, y: 0 };
                    const pH = this.project(armT.x, armT.y, zOffset, origins), pF = this.project(footT.x, footT.y, zOffset, origins);
                    this.ctx.beginPath(); this.ctx.moveTo(pS.x, pS.y);
                    if (iC) this.ctx.quadraticCurveTo(this.project(side * 2.5, -7.0, zOffset, origins).x, this.project(side * 2.5, -7.0, zOffset, origins).y, pH.x, pH.y);
                    else this.ctx.lineTo(pH.x, pH.y);
                    this.ctx.stroke();
                    this.ctx.beginPath(); this.ctx.moveTo(pGroin.x, pGroin.y);
                    if (iC) this.ctx.quadraticCurveTo(this.project(side * 1.5, -1.8, zOffset, origins).x, this.project(side * 1.5, -1.8, zOffset, origins).y, pF.x, pF.y);
                    else this.ctx.lineTo(pF.x, pF.y);
                    this.ctx.stroke();
                });
            };
            drawBody('square'); drawBody('circle');
            this.ctx.shadowBlur = 0;
        }

        // 10. METATRON'S CUBE (CENTRED AT NAVEL) - With BARYCENTER shift
        const drawMetatron = (cx, cy, r) => {
            const rotAngle = time * 0.1; // Slow rotation
            scribe('rgba(255, 255, 255, 0.2)', 1.2); // Slightly more visible
            const circles = [];
            circles.push({ x: cx, y: cy }); // center
            for (let i = 0; i < 6; i++) {
                const a = i * Math.PI / 3 + rotAngle;
                circles.push({ x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r });
                circles.push({ x: cx + Math.cos(a) * r * 2, y: cy + Math.sin(a) * r * 2 });
            }
            // Draw lines between all centers
            this.ctx.beginPath();
            for (let i = 0; i < circles.length; i++) {
                for (let j = i + 1; j < circles.length; j++) {
                    const p1 = this.project(circles[i].x, circles[i].y, 0, origins);
                    const p2 = this.project(circles[j].x, circles[j].y, 0, origins);
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                }
            }
            this.ctx.stroke();

            // Dodecahedron (Space) - Pentagon Faces (Simplified)
            scribe('rgba(200, 100, 255, 0.5)', 1.4);
            const drawPentagon = (cx, cy, r, rot) => {
                this.ctx.beginPath();
                for (let i = 0; i < 5; i++) {
                    const a = (i * 2 * Math.PI / 5) + rot + rotAngle;
                    const p = this.project(cx + Math.cos(a) * r, cy + Math.sin(a) * r, 0, origins);
                    if (i === 0) this.ctx.moveTo(p.x, p.y); else this.ctx.lineTo(p.x, p.y);
                }
                this.ctx.closePath();
                this.ctx.stroke();
            };

            // 11. THE ORACLE GRID (H3 Hexagonal Indexing)
            // Integrates the "Auric Mucus" stagnation data into a discretised H3 mesh
            if (this.controls.showOracle?.checked && typeof h3 !== 'undefined') {
                const h3Resolution = 7; // RIS Threshold (Resolution 7.5 simulated at 7)
                const centerLat = 0; // Mapping Flatland Y to Latitude
                const centerLng = 0; // Mapping Flatland X to Longitude

                // Generate a ring of hexes around the Barycenter
                const centerHex = h3.latLngToCell(centerLat, centerLng, h3Resolution);
                const kRing = h3.gridDisk(centerHex, 3); // 3-ring radius

                kRing.forEach(hex => {
                    const hexCenter = h3.cellToLatLng(hex);
                    // Simple projection: Lat/Lng -> Y/X
                    // Scaling factor to match Mathman units (mm)
                    const scale = 5.0;
                    const hX = hexCenter[1] * scale;
                    const hY = hexCenter[0] * scale + bY; // Centered at Barycenter

                    // Check resonance at this hex center
                    // We use the same getIntensity function to "listen" to the field at this hex
                    const intensity = this.getIntensity(hX, hY, 0, origins, k, time, true);

                    // Color based on Bit-Density (Stagnation vs Flow)
                    const density = intensity.stagnation; // 0 to 1
                    const alpha = Math.min(0.8, density * 1.5);

                    if (density > 0.2) { // Only render if "something" is there
                        const boundary = h3.cellToBoundary(hex);
                        this.ctx.beginPath();
                        boundary.forEach((coord, i) => {
                            // Project H3 boundary to Canvas
                            const bx = coord[1] * scale;
                            const by = coord[0] * scale + bY;
                            const p = this.project(bx, by, 0, origins);
                            if (i === 0) this.ctx.moveTo(p.x, p.y);
                            else this.ctx.lineTo(p.x, p.y);
                        });
                        this.ctx.closePath();

                        // Visual Style: "Iron/Rust" for Stagnation, "Cyber" for Flow
                        this.ctx.fillStyle = `rgba(255, ${255 - (density * 200)}, 0, ${alpha * 0.4})`;
                        this.ctx.strokeStyle = `rgba(255, 255, 255, ${alpha * 0.8})`;
                        this.ctx.lineWidth = 1;
                        this.ctx.fill();
                        this.ctx.stroke();
                    }
                });
            }
            // Resume Dodecahedron
            // 11b. Draw Pentagons (Dodecahedron)
            drawPentagon(cx, cy, r * 0.6, -Math.PI / 2);

            // Icosahedron (Water) - Triangle Faces (Simplified)
            scribe('rgba(100, 200, 255, 0.5)', 1.4); // More visible
            const drawTri = (cx, cy, r, rot) => {
                this.ctx.beginPath();
                for (let i = 0; i < 3; i++) {
                    const a = (i * 2 * Math.PI / 3) + rot - rotAngle;
                    const p = this.project(cx + Math.cos(a) * r, cy + Math.sin(a) * r, 0, origins);
                    if (i === 0) this.ctx.moveTo(p.x, p.y); else this.ctx.lineTo(p.x, p.y);
                }
                this.ctx.closePath(); this.ctx.stroke();
            };
            drawTri(cx, cy, r * 0.7, -Math.PI / 6);
            drawTri(cx, cy, r * 0.7, Math.PI / 2);
        };
        drawMetatron(0, -4.32, 1.0); // Size 1.0 at Navel

        this.ctx.restore();
    }

    drawField(origins) {
        const { mm } = origins;
        const time = performance.now() / 1000;
        const k = (2 * Math.PI) / this.params.lambda;
        const res = Math.max(3, Math.floor(6 / this.camera.zoom));
        let nodes = [];
        for (let ix = -8; ix <= 8; ix += res / mm) {
            for (let iy = -13; iy <= 2; iy += res / mm) {
                const data = this.getIntensity(ix, iy, 0, origins, k, time, true);
                const absVal = Math.abs(data.intensity);
                let density = 1.0;
                if (iy > -3.2 && iy < 0) density = 0.3; // Limbs
                if (iy < -7.0) density = 0.1; // External field

                if (absVal > this.params.threshold && Math.random() < density) {
                    const p = this.project(ix, iy, 0, origins);
                    nodes.push({ px: p.x, py: p.y, s: absVal, pol: data.intensity > 0 ? 1 : -1, type: 'field' });
                }

                // Higher probability for mucus if stagnation is high and random chance
                if (this.controls.layerMucus?.checked && data.stagnation > 0.4 && Math.random() < 0.05 * density) {
                    const p = this.project(ix, iy, 0, origins);
                    nodes.push({ px: p.x, py: p.y, s: data.stagnation, type: 'mucus' });
                }
            }
        }
        nodes.sort((a, b) => b.s - a.s);
        const top = nodes.slice(0, Math.min(this.params.budget, nodes.length));
        if (this.controls.showMathman.checked) {
            top.forEach(n => {
                const a = (n.s - this.params.threshold) / (1 - this.params.threshold);
                if (n.type === 'mucus') {
                    // Auric Mucus: Sickly green/grey diffuse particles
                    this.ctx.fillStyle = `rgba(180, 200, 150, ${n.s * 0.4})`;
                    this.ctx.beginPath(); this.ctx.arc(n.px, n.py, mm * 0.15, 0, Math.PI * 2); this.ctx.fill();
                } else {
                    this.ctx.fillStyle = n.pol > 0 ? `rgba(160, 82, 45, ${a * 0.8})` : `rgba(255, 255, 255, ${a * 0.35})`;
                    this.ctx.beginPath(); this.ctx.arc(n.px, n.py, mm * this.params.nodeSize * 0.1, 0, Math.PI * 2); this.ctx.fill();
                }
            });
        }

        if (this.controls.showMerkaba.checked) {
            const zOffset = this.getLayerZ('merkaba');
            const rot = time * 0.22;
            const drawT = (male, alpha) => {
                this.ctx.save();
                const s = male ? 1 : -1; // Sign multiplier for tetrahedron orientation
                const glow = 0.2 * Math.sin(time * 2);
                this.ctx.strokeStyle = male ? `rgba(100, 220, 255, ${alpha + glow})` : `rgba(255, 255, 255, ${alpha + glow})`;
                this.ctx.lineWidth = 1.8;
                const R = 4.45;
                const rB = R * Math.sqrt(8) / 3, yB = -R / 3;
                const raw = [{ x: 0, y: R * s, z: 0 }, { x: rB, y: yB * s, z: 0 }, { x: -rB / 2, y: yB * s, z: rB * Math.sqrt(3) / 2 }, { x: -rB / 2, y: yB * s, z: -rB * Math.sqrt(3) / 2 }];
                const pts = raw.map(p => {
                    const rx = p.x * Math.cos(rot) - p.z * Math.sin(rot);
                    const rz = p.x * Math.sin(rot) + p.z * Math.cos(rot) + zOffset;
                    return this.project(rx, -3.5 + p.y, rz, origins); // Centered at Vitruvian navel + layer offset
                });
                [[0, 1], [0, 2], [0, 3], [1, 2], [2, 3], [3, 1]].forEach(([i, j]) => {
                    this.ctx.beginPath(); this.ctx.moveTo(pts[i].x, pts[i].y); this.ctx.lineTo(pts[j].x, pts[j].y); this.ctx.stroke();
                });
                this.ctx.restore();
            };
            drawT(true, 0.85); drawT(false, 0.55);
        }
    }

    render() {
        const cw = this.canvas.width / devicePixelRatio, ch = this.canvas.height / devicePixelRatio;
        this.ctx.clearRect(0, 0, cw, ch);
        const o = this.getOrigins();
        const time = performance.now() / 1000;

        this.ctx.fillStyle = '#0a0805';
        this.ctx.fillRect(0, 0, cw, ch);

        if (this.controls.showGrid.checked) {
            this.ctx.strokeStyle = `rgba(139, 69, 19, ${this.params.gridOp * 0.2})`;
            for (let i = -10; i <= 10; i++) {
                let p1 = this.project(i * 10, 0, -100, o), p2 = this.project(i * 10, 0, 100, o);
                this.ctx.beginPath(); this.ctx.moveTo(p1.x, p1.y); this.ctx.lineTo(p2.x, p2.y); this.ctx.stroke();
                p1 = this.project(-100, 0, i * 10, o); p2 = this.project(100, 0, i * 10, o);
                this.ctx.beginPath(); this.ctx.moveTo(p1.x, p1.y); this.ctx.lineTo(p2.x, p2.y); this.ctx.stroke();
            }
        }

        this.drawOrigins(o);
        this.drawLeonardo(o);
        this.drawField(o);

        // Update stats
        const phaseEl = document.getElementById('phase-coord');
        if (phaseEl) phaseEl.innerText = (time % (Math.PI * 2)).toFixed(2);

        this.params.pulseIntensity *= 0.94;
        requestAnimationFrame(() => this.render());
    }

    drawOrigins(origins) {
        // Draw Origin A (Cyan)
        const pA = this.project(origins.a.x, origins.a.y, 0, origins);
        this.ctx.fillStyle = '#00ffff';
        this.ctx.beginPath(); this.ctx.arc(pA.x, pA.y, 4, 0, Math.PI * 2); this.ctx.fill();
        this.ctx.fillStyle = 'rgba(0, 255, 255, 0.5)';
        this.ctx.fillText("A", pA.x + 8, pA.y + 4);

        // Draw Origin B (Magenta)
        const pB = this.project(origins.b.x, origins.b.y, 0, origins);
        this.ctx.fillStyle = '#ff00ff';
        this.ctx.beginPath(); this.ctx.arc(pB.x, pB.y, 4, 0, Math.PI * 2); this.ctx.fill();
        this.ctx.fillStyle = 'rgba(255, 0, 255, 0.5)';
        this.ctx.fillText("B", pB.x + 8, pB.y + 4);

        // Draw Origin C (Sun - Gold)
        if (!this.genesisRunning) {
            const pC = this.project(origins.c.x, origins.c.y, 0, origins);
            this.ctx.fillStyle = '#ffd700';
            this.ctx.beginPath(); this.ctx.arc(pC.x, pC.y, 6, 0, Math.PI * 2); this.ctx.fill();
            this.ctx.fillStyle = 'rgba(255, 215, 0, 0.5)';
            this.ctx.fillText("C", pC.x + 10, pC.y + 4);
        }
    }

    async runGenesis() {
        if (this.genesisRunning) return;
        this.genesisRunning = true;
        this.controls.btnGenesis.disabled = true;
        this.controls.btnGenesis.innerText = "Genesis Active...";

        const seq = new GenesisSequence(this);
        await seq.run();

        this.genesisRunning = false;
        this.controls.btnGenesis.disabled = false;
        this.controls.btnGenesis.innerText = "Start Genesis";
    }

    applyPreset(type) {
        // Reset all layers first
        Object.keys(this.controls).forEach(k => {
            if (k.startsWith('layer') && this.controls[k].type === 'checkbox') {
                this.controls[k].checked = false;
            }
        });

        if (type === 'grounding') {
            this.params.scanY = 0.0; // Root
            this.params.threshold = 0.45;
            this.params.lambda = 0.8;
            this.params.brightness = 0.4;
            this.params.distAB = 1.0;
            this.controls.layerFoundation.checked = true;
            this.controls.layerPrime24.checked = true;
            this.controls.layerVitruvian.checked = true;
            this.controls.chakraSelector.value = "1";
        } else if (type === 'expansion') {
            this.params.scanY = -7.0; // Crown
            this.params.threshold = 0.12;
            this.params.lambda = 1.5;
            this.params.brightness = 0.6;
            this.params.distAB = 1.6;
            this.controls.layerDivine7.checked = true;
            this.controls.layerSephiroth.checked = true;
            this.controls.layerCoreStar.checked = true;
            this.controls.layerAnnotations.checked = true;
            this.controls.chakraSelector.value = "7";
        }

        this.syncInitialUI();
    }

    animate() {
        this.render();
        requestAnimationFrame(() => this.animate());
    }
}
window.onload = () => new MathmanFlatland();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = MathmanFlatland;
}
