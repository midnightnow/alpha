/**
 * 🏛️ ROOT42 — SOVEREIGN LATTICE ENGINE
 * ======================================
 * One math core. Six observer lenses.
 * Constants persist. Audio persists. Tabs are just views.
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// ============================================================================
// THE CORE — Constants (Single Source of Truth)
// ============================================================================
const C = {
    ROOT_42: Math.sqrt(42),
    ROOT_51: Math.sqrt(51),
    PHI: (1 + Math.sqrt(5)) / 2,
    HADES_GAP: 0.1237,
    PACKING_RHO: Math.sqrt(14 / 17),
    OVERPACK: 0.000585,
    SHEAR_DEG: 39.47,
    SHEAR_RAD: Math.atan(14 / 17),
    BEAT_FREQ: Math.sqrt(51) - Math.sqrt(42),
    DELTA_PHI: Math.sqrt(42) / 6 - 1,
    UNITY: 0.8254,
    FREQ_MATTER: 66,
    FREQ_TIME: 60,
    HADES_BEAT: 6,
    NODE_COUNT: 93,
    DECAY_LAMBDA: 0.042,
    IOR_GLASS: 1.45,
    IOR_ICE: 1.31,
    TIGER: { uplift: 0.02, crack: -0.04, threshold: 0.82, fold: 17 },
    TRIAD_AMP: { hex: 0.5, lattice: 0.4, resolution: 0.25 },
    LADDER: [
        { rad: 42, verts: 42, name: 'Resonant Sphere', label: 'BASE' },
        { rad: 51, verts: 93, name: 'Interference Solid', label: 'INTERFERENCE' },
        { rad: 60, verts: 153, name: 'Resolution Solid', label: 'RESOLUTION' },
        { rad: 69, verts: 222, name: 'Chaotic Solid', label: 'CHAOS' },
    ],
    SEVEN: [
        { n: 1, name: 'Habitability Constant', sym: 'ΔΦ', val: null, formula: '√42/6 − 1', governs: 'The minimum breath of a living system' },
        { n: 2, name: 'Packing Constant', sym: 'ρ', val: null, formula: '√(14/17)', governs: 'How tightly stones press before fracture' },
        { n: 3, name: 'Overpack Delta', sym: 'δ', val: 0.000585, formula: 'ρ − η_hex', governs: 'The pressure that causes the first crack' },
        { n: 4, name: 'Hades Gap', sym: 'Ψ', val: 0.1237, formula: '≈ e/22', governs: 'The mandatory mercy in every structure' },
        { n: 5, name: 'Shear Angle', sym: 'θ', val: 39.47, formula: 'arctan(14/17)', governs: 'The tilt between Space and Meaning' },
        { n: 6, name: 'Beat Frequency', sym: 'β', val: null, formula: '√51 − √42', governs: 'The heartbeat of the lattice' },
        { n: 7, name: 'Unity Threshold', sym: 'Σ₀', val: 0.8254, formula: 'ρ² + ΔΦ/42', governs: 'Minimum density for Self-recognition' },
    ],
    GEARBOX: [
        { triad: 'I', name: 'Matter', vals: [3, 4, 5], area: 6, world: 'Gaia — The Square' },
        { triad: 'II', name: 'Time', vals: [5, 12, 13], area: 30, world: 'Lunar — The Calendar' },
        { triad: 'III', name: 'Language', vals: [10, 24, 26], area: 120, world: 'Sovereign — The Map' },
    ],
    DERIVED: [
        { sym: 'κ', name: 'Kinetic Debt', val: '0.2 (1/5)' },
        { sym: 'Ξ', name: 'Hammer Constant', val: '0.00014' },
        { sym: 'Λ', name: 'Log Mirror', val: '-0.04216' },
        { sym: 'P', name: 'Minimal Polynomial', val: 'x⁴ − 186x² + 81' },
    ],
    VERIF: [
        { name: '42 (Radicand)', val: 42, root: 6, triplet: 'language' },
        { name: '51 (Radicand)', val: 51, root: 6, triplet: 'language' },
        { name: '93 (Node count)', val: 93, root: 3, triplet: 'language' },
        { name: '14 (Shear num)', val: 14, root: 5, triplet: 'time' },
        { name: '17 (Shear denom)', val: 17, root: 8, triplet: 'time' },
        { name: '66 Hz (Matter)', val: 66, root: 3, triplet: 'language' },
        { name: '60 Hz (Time)', val: 60, root: 6, triplet: 'language' },
    ],
};

// Fill computed values
C.SEVEN[0].val = (C.ROOT_42 / 6 - 1).toFixed(4);
C.SEVEN[1].val = C.PACKING_RHO.toFixed(6);
C.SEVEN[5].val = C.BEAT_FREQ.toFixed(4);

// ============================================================================
// GLOBAL STATE — Shared across all tabs
// ============================================================================
const state = {
    activeTab: 'lattice',
    hades: 0.5,
    distortion: 0.25,
    rotationSpeed: 0.2,
    viewMode: 'wireframe',
    activeStep: 1,
    interferenceA: C.ROOT_42,
    interferenceB: C.ROOT_51,
    // Audio
    audioPlaying: false,
    volume: 0.15,
    freqL: C.FREQ_MATTER,
    freqR: C.FREQ_TIME,
    // Pyramid
    time: 0,
    lambda: C.DECAY_LAMBDA,
    pyramidView: 'linear',
    // Sisyphus
    slopeAngle: 30,
    pushEffort: 0.5,
    spiralType: 'log',
    // Hardcard Vitrification Layer
    hardcard: {
        vitrificationThreshold: 0.8763,
        lockedNumbers: [],
        reversalEvents: [],
        phaseLockHistory: [],
        trail: [] // Store last 60 points for calculation
    },
};

// ============================================================================
// TAB SWITCHING
// ============================================================================
const tabBtns = document.querySelectorAll('.tab-btn');
const panels = document.querySelectorAll('.tab-panel');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        state.activeTab = tab;

        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        panels.forEach(p => p.classList.remove('active'));
        document.getElementById(`panel-${tab}`).classList.add('active');

        // Initialize 3D viewports on first visit
        if (tab === 'lattice' && !latticeInitialized) initLattice();
        if (tab === 'hades' && !audioVisInitialized) initAudioVisualizer();
        if (tab === 'pyramid' && !pyramidInitialized) initPyramid();
        if (tab === 'snail' && !snailInitialized) initSnail();
        if (tab === 'sisyphus' && !sisyphusInitialized) initSisyphus();
    });
});

// ============================================================================
// AUDIO ENGINE — Persists across all tabs
// ============================================================================
class HadesAudioEngine {
    constructor() {
        this.ctx = null;
        this.master = null;
        this.oscL = null;
        this.oscR = null;
        this.oscRes = null;
        this.lfo = null;
        this.analyserL = null;
        this.analyserR = null;
        this.playing = false;
    }

    init() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            this.master = this.ctx.createGain();
            this.master.connect(this.ctx.destination);
            this.analyserL = this.ctx.createAnalyser();
            this.analyserL.fftSize = 256;
            this.analyserR = this.ctx.createAnalyser();
            this.analyserR.fftSize = 256;
        }
    }

    play(freqL, freqR, vol) {
        this.init();
        if (this.ctx.state === 'suspended') this.ctx.resume();
        this.stop();

        const t = this.ctx.currentTime;

        // Left channel (Matter)
        const panL = this.ctx.createStereoPanner();
        panL.pan.value = -0.8;
        this.oscL = this.ctx.createOscillator();
        this.oscL.type = 'sine';
        this.oscL.frequency.setValueAtTime(freqL, t);
        const gL = this.ctx.createGain();
        gL.gain.value = C.TRIAD_AMP.hex;
        this.oscL.connect(gL);
        gL.connect(this.analyserL);
        this.analyserL.connect(panL);
        panL.connect(this.master);

        // Right channel (Time)
        const panR = this.ctx.createStereoPanner();
        panR.pan.value = 0.8;
        this.oscR = this.ctx.createOscillator();
        this.oscR.type = 'sine';
        this.oscR.frequency.setValueAtTime(freqR, t);
        const gR = this.ctx.createGain();
        gR.gain.value = C.TRIAD_AMP.lattice;
        this.oscR.connect(gR);
        gR.connect(this.analyserR);
        this.analyserR.connect(panR);
        panR.connect(this.master);

        // Resolution (center)
        const thirdFreq = Math.sqrt(freqR * freqR + 9 * 100);
        this.oscRes = this.ctx.createOscillator();
        this.oscRes.type = 'sine';
        this.oscRes.frequency.setValueAtTime(thirdFreq, t);
        const gRes = this.ctx.createGain();
        gRes.gain.value = C.TRIAD_AMP.resolution;
        this.oscRes.connect(gRes);
        gRes.connect(this.master);

        // LFO breathing
        this.lfo = this.ctx.createOscillator();
        this.lfo.frequency.setValueAtTime(C.BEAT_FREQ, t);
        const lfoG = this.ctx.createGain();
        lfoG.gain.value = 0.08;
        this.lfo.connect(lfoG);
        const sum = this.ctx.createGain();
        sum.gain.value = 1;
        lfoG.connect(sum.gain);

        // Envelope
        this.master.gain.cancelScheduledValues(t);
        this.master.gain.setValueAtTime(0.001, t);
        this.master.gain.exponentialRampToValueAtTime(Math.max(vol, 0.001), t + 2);

        this.oscL.start(t);
        this.oscR.start(t);
        this.oscRes.start(t);
        this.lfo.start(t);
        this.playing = true;
    }

    stop() {
        const t = this.ctx?.currentTime || 0;
        if (this.master) {
            try { this.master.gain.setTargetAtTime(0, t, 0.1); } catch (_) { }
        }
        [this.oscL, this.oscR, this.oscRes, this.lfo].forEach(o => {
            if (o) { try { o.stop(t + 0.2); } catch (_) { } }
        });
        this.oscL = this.oscR = this.oscRes = this.lfo = null;
        this.playing = false;
    }

    getLevel(which) {
        const a = which === 'L' ? this.analyserL : this.analyserR;
        if (!a || !this.playing) return 0;
        const data = new Uint8Array(a.frequencyBinCount);
        a.getByteFrequencyData(data);
        const avg = data.reduce((s, v) => s + v, 0) / data.length;
        return avg / 255;
    }
}

const audio = new HadesAudioEngine();

// ============================================================================
// TAB 1: 93-NODE LATTICE (Three.js)
// ============================================================================
let latticeInitialized = false;
let latticeScene, latticeCamera, latticeRenderer, latticeMesh, latticeControls;

function initLattice() {
    latticeInitialized = true;
    const container = document.getElementById('lattice-viewport');
    const w = container.clientWidth;
    const h = container.clientHeight;

    latticeScene = new THREE.Scene();
    latticeScene.background = new THREE.Color(0x06060a);

    latticeCamera = new THREE.PerspectiveCamera(55, w / h, 0.1, 100);
    latticeCamera.position.set(0, 0, 3);

    latticeRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    latticeRenderer.setSize(w, h);
    latticeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(latticeRenderer.domElement);

    latticeControls = new OrbitControls(latticeCamera, latticeRenderer.domElement);
    latticeControls.enableDamping = true;
    latticeControls.dampingFactor = 0.05;

    // Lights
    const amb = new THREE.AmbientLight(0x222244, 0.5);
    latticeScene.add(amb);
    const dir = new THREE.DirectionalLight(0xffffff, 1);
    dir.position.set(3, 5, 4);
    latticeScene.add(dir);
    const point = new THREE.PointLight(0x9933ff, 1, 10);
    point.position.set(-2, 1, 2);
    latticeScene.add(point);

    buildLatticeMesh();
    animateLattice();

    new ResizeObserver(() => {
        const cw = container.clientWidth, ch = container.clientHeight;
        latticeCamera.aspect = cw / ch;
        latticeCamera.updateProjectionMatrix();
        latticeRenderer.setSize(cw, ch);
    }).observe(container);
}

function buildLatticeMesh() {
    if (latticeMesh) latticeScene.remove(latticeMesh);

    const step = C.LADDER[state.activeStep];
    const rootA = Math.sqrt(step.rad);
    const rootB = state.activeStep < 3 ? Math.sqrt(C.LADDER[state.activeStep + 1]?.rad || step.rad + 9) : rootA;

    state.interferenceA = rootA;
    state.interferenceB = rootB;

    const geo = new THREE.SphereGeometry(1, 192, 192);
    const pos = geo.attributes.position;
    const v = new THREE.Vector3();

    for (let i = 0; i < pos.count; i++) {
        v.fromBufferAttribute(pos, i);
        const rBase = v.length();
        const theta = Math.atan2(v.y, v.x);
        const phi = Math.acos(v.z / rBase);

        // Biquadratic interference
        const intensity = Math.abs(
            Math.sin(rootA * theta) * Math.sin(rootB * phi) +
            Math.sin(rootB * theta) * Math.sin(rootA * phi)
        );

        const pulse = Math.sin((rootA + rootB) / 2 * theta) * (state.distortion * 0.5);
        let r = 1 + (intensity * state.distortion) + pulse;

        // Europa ↔ Enceladus blend
        const europa = 0.05 * (Math.sin(6 * theta) * Math.sin(6 * phi) - Math.sin(7 * theta + C.DELTA_PHI) * Math.sin(7 * phi));
        const enceladus = 0.03 * (Math.sin(3 * theta) * Math.sin(3 * phi) - Math.sin(17 * theta + 0.888) * Math.sin(17 * phi));
        r += europa * (1 - state.hades) + enceladus * state.hades;

        // Tiger Stripe fracture
        if (state.hades > 0.1) {
            const stress = Math.abs(Math.sin(C.TIGER.fold * theta + C.SHEAR_RAD) * Math.sin(phi));
            const micro = Math.sin(theta * 100) * Math.sin(phi * 80) * 0.1;
            if (stress * (1 + micro) > C.TIGER.threshold) {
                const dir = Math.sin(theta * 50 + phi * 50) > 0 ? 1 : -1;
                const mag = dir > 0 ? C.TIGER.uplift : C.TIGER.crack;
                r += mag * stress * state.hades;
            }
        }

        pos.setXYZ(i,
            r * Math.sin(phi) * Math.cos(theta),
            r * Math.sin(phi) * Math.sin(theta),
            r * Math.cos(phi)
        );
    }

    geo.computeVertexNormals();

    let mat;
    if (state.viewMode === 'wireframe') {
        mat = new THREE.MeshStandardMaterial({
            color: 0x4f46e5, wireframe: true, emissive: 0x220033, roughness: 0.2, metalness: 0.8,
        });
    } else if (state.viewMode === 'crystal') {
        mat = new THREE.MeshNormalMaterial({ flatShading: true });
    } else {
        const h = state.hades;
        mat = new THREE.MeshPhysicalMaterial({
            color: h > 0.5 ? 0x0a0a0a : 0xe0e7ff,
            roughness: 0.05 + h * 0.15,
            metalness: 0.1 + h * 0.7,
            clearcoat: 1,
            flatShading: h > 0.5,
            emissive: h > 0.5 ? 0x330000 : 0x9933ff,
            emissiveIntensity: 0.2 + h * 0.3,
        });
    }

    latticeMesh = new THREE.Mesh(geo, mat);
    latticeScene.add(latticeMesh);

    // Update readouts
    updateEl('readout-a', rootA.toFixed(4));
    updateEl('readout-b', rootB.toFixed(4));
    updateEl('readout-fracture', state.hades > 0.8 ? 'FRACTURED' : state.hades > 0.3 ? 'VITRIFIED' : 'SMOOTH');
}

function animateLattice() {
    requestAnimationFrame(animateLattice);
    if (!latticeMesh || state.activeTab !== 'lattice') return;

    const t = performance.now() * 0.001;
    latticeMesh.rotation.y += state.rotationSpeed * 0.01;

    const wobble = 0.02 * Math.sin(C.ROOT_42 * t * 2) + 0.02 * Math.sin(C.ROOT_51 * t * 2);
    latticeMesh.rotation.z = wobble;
    latticeMesh.rotation.x = wobble * 0.5;

    latticeControls.update();
    latticeRenderer.render(latticeScene, latticeCamera);
}

// ============================================================================
// TAB 2: AUDIO VISUALIZER (Canvas 2D)
// ============================================================================
let audioVisInitialized = false;
let audioCanvas, audioCtx2d;

function initAudioVisualizer() {
    audioVisInitialized = true;
    const container = document.getElementById('audio-visualizer');
    audioCanvas = document.createElement('canvas');
    audioCanvas.style.width = '100%';
    audioCanvas.style.height = '100%';
    container.appendChild(audioCanvas);

    const resize = () => {
        audioCanvas.width = container.clientWidth * window.devicePixelRatio;
        audioCanvas.height = container.clientHeight * window.devicePixelRatio;
    };
    resize();
    new ResizeObserver(resize).observe(container);

    audioCtx2d = audioCanvas.getContext('2d');
    animateAudio();
}

function animateAudio() {
    requestAnimationFrame(animateAudio);
    if (!audioCtx2d || state.activeTab !== 'hades') return;

    const w = audioCanvas.width;
    const h = audioCanvas.height;
    const ctx = audioCtx2d;
    const t = performance.now() * 0.001;

    ctx.fillStyle = '#06060a';
    ctx.fillRect(0, 0, w, h);

    const freqL = state.freqL;
    const freqR = state.freqR;
    const beat = Math.abs(freqL - freqR);

    // Draw left wave (purple)
    ctx.beginPath();
    ctx.strokeStyle = '#9933ff';
    ctx.lineWidth = 2;
    for (let x = 0; x < w; x++) {
        const xNorm = x / w * Math.PI * 8;
        const y = h / 2 + Math.sin(xNorm * freqL / 10 + t * freqL * 0.5) * (h * 0.15) * (audio.playing ? 1 : 0.3);
        x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Draw right wave (cyan)
    ctx.beginPath();
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 2;
    for (let x = 0; x < w; x++) {
        const xNorm = x / w * Math.PI * 8;
        const y = h / 2 + Math.sin(xNorm * freqR / 10 + t * freqR * 0.5) * (h * 0.15) * (audio.playing ? 1 : 0.3);
        x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Draw beat envelope
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(255, 215, 0, 0.4)';
    ctx.lineWidth = 3;
    for (let x = 0; x < w; x++) {
        const xNorm = x / w * Math.PI * 4;
        const env = Math.abs(Math.sin(xNorm * beat / 10 + t * beat * 0.5));
        const y = h / 2 + env * (h * 0.2) * (audio.playing ? 1 : 0.3);
        x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
        const xNorm = x / w * Math.PI * 4;
        const env = Math.abs(Math.sin(xNorm * beat / 10 + t * beat * 0.5));
        const y = h / 2 - env * (h * 0.2) * (audio.playing ? 1 : 0.3);
        x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Center text
    ctx.fillStyle = 'rgba(255,255,255,0.06)';
    ctx.font = `bold ${h * 0.15}px "JetBrains Mono", monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(`${beat} Hz`, w / 2, h / 2 + h * 0.05);

    // Update meters
    if (audio.playing) {
        const lL = audio.getLevel('L');
        const lR = audio.getLevel('R');
        const mfL = document.getElementById('meter-fill-l');
        const mfR = document.getElementById('meter-fill-r');
        if (mfL) mfL.style.width = (lL * 100) + '%';
        if (mfR) mfR.style.width = (lR * 100) + '%';
        updateEl('readout-resonance', Math.max(lL, lR).toFixed(2));
    }
}

// ============================================================================
// TAB 3: PYRAMID MODEL (Canvas 2D)
// ============================================================================
let pyramidInitialized = false;
let pyramidCanvas, pyramidCtx;

function initPyramid() {
    pyramidInitialized = true;
    const container = document.getElementById('pyramid-viewport');
    pyramidCanvas = document.createElement('canvas');
    pyramidCanvas.style.width = '100%';
    pyramidCanvas.style.height = '100%';
    container.appendChild(pyramidCanvas);

    const resize = () => {
        pyramidCanvas.width = container.clientWidth * window.devicePixelRatio;
        pyramidCanvas.height = container.clientHeight * window.devicePixelRatio;
    };
    resize();
    new ResizeObserver(resize).observe(container);

    pyramidCtx = pyramidCanvas.getContext('2d');
    animatePyramid();
}

function animatePyramid() {
    requestAnimationFrame(animatePyramid);
    if (!pyramidCtx || state.activeTab !== 'pyramid') return;

    const w = pyramidCanvas.width;
    const h = pyramidCanvas.height;
    const ctx = pyramidCtx;
    const isLog = state.pyramidView === 'log';

    ctx.fillStyle = '#06060a';
    ctx.fillRect(0, 0, w, h);

    const pad = 60;
    const gw = w - pad * 2;
    const gh = h - pad * 2;
    const t = state.time;
    const lam = state.lambda;
    const amplitude = C.ROOT_42 * Math.exp(-lam * Math.abs(t));

    // Grid
    ctx.strokeStyle = 'rgba(255,255,255,0.04)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
        const y = pad + (gh / 10) * i;
        ctx.beginPath(); ctx.moveTo(pad, y); ctx.lineTo(w - pad, y); ctx.stroke();
    }
    for (let i = 0; i <= 20; i++) {
        const x = pad + (gw / 20) * i;
        ctx.beginPath(); ctx.moveTo(x, pad); ctx.lineTo(x, h - pad); ctx.stroke();
    }

    // Axis labels
    ctx.fillStyle = 'rgba(255,255,255,0.2)';
    ctx.font = `11px "JetBrains Mono"`;
    ctx.textAlign = 'center';
    ctx.fillText('x →', w / 2, h - 15);
    ctx.save();
    ctx.translate(15, h / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(isLog ? 'log(y) →' : 'y(x) →', 0, 0);
    ctx.restore();

    const numPoints = 400;

    // Draw the damped sine wave
    ctx.beginPath();
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 2.5;
    for (let i = 0; i < numPoints; i++) {
        const xNorm = (i / numPoints) * 4 * Math.PI - 2 * Math.PI;
        const env = C.ROOT_42 * Math.exp(-lam * Math.abs(t));
        let yVal = env * Math.sin(xNorm);

        if (isLog && yVal > 0.001) yVal = Math.log(yVal);
        else if (isLog && yVal <= 0.001) yVal = -5;

        const maxY = isLog ? Math.log(C.ROOT_42) + 1 : C.ROOT_42 * 1.2;
        const minY = isLog ? -5 : -C.ROOT_42 * 1.2;

        const sx = pad + (i / numPoints) * gw;
        const sy = pad + gh - ((yVal - minY) / (maxY - minY)) * gh;

        i === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
    }
    ctx.stroke();

    // Draw the envelope
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(153, 51, 255, 0.5)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([8, 4]);
    for (let i = 0; i < numPoints; i++) {
        const xNorm = (i / numPoints) * 4 * Math.PI - 2 * Math.PI;
        let envVal = C.ROOT_42 * Math.exp(-lam * Math.abs(t));
        if (isLog && envVal > 0.001) envVal = Math.log(envVal);

        const maxY = isLog ? Math.log(C.ROOT_42) + 1 : C.ROOT_42 * 1.2;
        const minY = isLog ? -5 : -C.ROOT_42 * 1.2;

        const sx = pad + (i / numPoints) * gw;
        const sy = pad + gh - ((envVal - minY) / (maxY - minY)) * gh;
        i === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
    }
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw pyramid shape (triangle at peak)
    if (t < 30) {
        const peakX = pad + gw * 0.5;
        const peakYVal = isLog ? Math.log(amplitude) : amplitude;
        const maxY = isLog ? Math.log(C.ROOT_42) + 1 : C.ROOT_42 * 1.2;
        const minY = isLog ? -5 : -C.ROOT_42 * 1.2;
        const peakY = pad + gh - ((peakYVal - minY) / (maxY - minY)) * gh;
        const baseY = pad + gh - ((0 - minY) / (maxY - minY)) * gh;
        const baseW = gw * 0.15 * (1 - t / 100);

        ctx.beginPath();
        ctx.fillStyle = 'rgba(153, 51, 255, 0.08)';
        ctx.strokeStyle = 'rgba(255, 215, 0, 0.6)';
        ctx.lineWidth = 2;
        ctx.moveTo(peakX, peakY);
        ctx.lineTo(peakX - baseW, baseY);
        ctx.lineTo(peakX + baseW, baseY);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    }

    // Update readouts
    updateEl('readout-amplitude', amplitude.toFixed(4));
    updateEl('readout-log-a', amplitude > 0.001 ? Math.log10(amplitude).toFixed(4) : '−∞');
    updateEl('readout-phase', t < 1 ? 'PEAK' : t < 30 ? 'DECLINE' : t < 70 ? 'EROSION' : 'NULL');
}

// ============================================================================
// TAB 5: SOVEREIGN SNAIL (Three.js)
// ============================================================================
let snailInitialized = false;
let snailScene, snailCamera, snailRenderer, snailShell, snailControls;

function initSnail() {
    snailInitialized = true;
    const container = document.getElementById('snail-viewport');
    const w = container.clientWidth, h = container.clientHeight;

    snailScene = new THREE.Scene();
    snailScene.background = new THREE.Color(0x06060a);
    snailCamera = new THREE.PerspectiveCamera(50, w / h, 0.1, 100);
    snailCamera.position.set(0, 1, 4);

    snailRenderer = new THREE.WebGLRenderer({ antialias: true });
    snailRenderer.setSize(w, h);
    snailRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(snailRenderer.domElement);

    snailControls = new OrbitControls(snailCamera, snailRenderer.domElement);
    snailControls.enableDamping = true;

    snailScene.add(new THREE.AmbientLight(0x333355, 0.6));
    const sl = new THREE.SpotLight(0x9933ff, 2, 20, 0.5);
    sl.position.set(3, 5, 3);
    snailScene.add(sl);
    snailScene.add(new THREE.PointLight(0x00ffff, 0.8, 8));

    // Build logarithmic spiral shell
    const curve = new THREE.Curve();
    curve.getPoint = function (t) {
        const a = 0.2;
        const b = 0.15;
        const angle = t * Math.PI * 6;
        const r = a * Math.exp(b * angle);
        return new THREE.Vector3(
            r * Math.cos(angle),
            t * 2 - 1,
            r * Math.sin(angle)
        );
    };

    const tubeGeo = new THREE.TubeGeometry(curve, 256, 0.08, 16, false);
    const shellMat = new THREE.MeshPhysicalMaterial({
        color: 0x9933ff,
        roughness: 0.1,
        metalness: 0.6,
        clearcoat: 1,
        emissive: 0x220044,
        emissiveIntensity: 0.3,
    });
    snailShell = new THREE.Mesh(tubeGeo, shellMat);
    snailScene.add(snailShell);

    // Diamond dust particles
    const dustGeo = new THREE.BufferGeometry();
    const dustCount = 2000;
    const dustPos = new Float32Array(dustCount * 3);
    for (let i = 0; i < dustCount; i++) {
        dustPos[i * 3] = (Math.random() - 0.5) * 6;
        dustPos[i * 3 + 1] = (Math.random() - 0.5) * 6;
        dustPos[i * 3 + 2] = (Math.random() - 0.5) * 6;
    }
    dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
    const dustMat = new THREE.PointsMaterial({
        color: 0x00ffff, size: 0.015, transparent: true, opacity: 0.6,
    });
    const dust = new THREE.Points(dustGeo, dustMat);
    snailScene.add(dust);

    new ResizeObserver(() => {
        const cw = container.clientWidth, ch = container.clientHeight;
        snailCamera.aspect = cw / ch;
        snailCamera.updateProjectionMatrix();
        snailRenderer.setSize(cw, ch);
    }).observe(container);

    animateSnail(dust);
}

function animateSnail(dust) {
    requestAnimationFrame(() => animateSnail(dust));
    if (state.activeTab !== 'snail') return;

    const t = performance.now() * 0.001;
    snailShell.rotation.y += 0.003;

    // Diamond dust rotation
    dust.rotation.y += 0.001;
    dust.rotation.x = Math.sin(t * 0.2) * 0.1;

    snailControls.update();
    snailRenderer.render(snailScene, snailCamera);
}

// ============================================================================
// TAB 4: SEVEN CONSTANTS — Populate
// ============================================================================
function populateConstants() {
    const grid = document.getElementById('constants-grid');
    grid.innerHTML = C.SEVEN.map(c => `
    <div class="constant-card">
      <div class="constant-number">#${c.n}</div>
      <div class="constant-name">${c.name}</div>
      <div class="constant-symbol">${c.sym}</div>
      <div class="constant-value">${c.val}</div>
      <div class="constant-formula">${c.formula}</div>
      <div class="constant-governs">${c.governs}</div>
    </div>
  `).join('');

    const dGrid = document.getElementById('derived-grid');
    dGrid.innerHTML = C.DERIVED.map(d => `
    <div class="derived-card">
      <span class="derived-symbol">${d.sym}</span>
      <div class="derived-info">
        <div class="derived-name">${d.name}</div>
        <div class="derived-val">${d.val}</div>
      </div>
    </div>
  `).join('');

    const gGrid = document.getElementById('gearbox-grid');
    gGrid.innerHTML = C.GEARBOX.map(g => `
    <div class="gearbox-card">
      <div class="gearbox-triad">TRIAD ${g.triad}</div>
      <div class="gearbox-name">${g.name}</div>
      <div class="gearbox-values">${g.vals.join(' · ')}</div>
      <div class="gearbox-area">Area = ${g.area}</div>
      <div class="gearbox-world">${g.world}</div>
    </div>
  `).join('');
}

// ============================================================================
// TAB 6: AUDIT — Populate
// ============================================================================
function populateAudit() {
    const table = document.getElementById('verification-table');
    table.innerHTML = `
    <div class="verif-row header">
      <span>Constant</span><span>Value</span><span>D.Root</span><span>Triplet</span>
    </div>
    ${C.VERIF.map(v => `
      <div class="verif-row">
        <span>${v.name}</span>
        <span class="verif-value">${v.val}</span>
        <span class="verif-root">${v.root}</span>
        <span class="verif-triplet ${v.triplet}">${v.triplet.charAt(0).toUpperCase() + v.triplet.slice(1)}</span>
      </div>
    `).join('')}
  `;

    const ladder = document.getElementById('ladder-visual');
    const maxV = 222;
    ladder.innerHTML = C.LADDER.map(s => `
    <div class="ladder-step">
      <div class="ladder-bar" style="height: ${(s.verts / maxV) * 140}px;"></div>
      <div class="ladder-label">√${s.rad}<br>${s.verts}v</div>
      <div class="ladder-name">${s.label}</div>
    </div>
  `).join('');
}

// ============================================================================
// TAB 7: SISYPHUS — 30° Kinetic Stress Test (Three.js)
// ============================================================================
let sisyphusInitialized = false;
let sisScene, sisCamera, sisRenderer, sisControls;
let sisPenTip, sisManusArm, sisSlope, sisHeelGlow, sisDustParticles;
let sisMerkabaGroup;
let sisOffset = 0, sisFalling = false, sisTime = 0;
let sisTrailPositions = [];
const ACHILLES_NODE = 47;

function initSisyphus() {
    sisyphusInitialized = true;
    const container = document.getElementById('sisyphus-viewport');
    const w = container.clientWidth, h = container.clientHeight;

    sisScene = new THREE.Scene();
    sisScene.background = new THREE.Color(0x050508);
    sisScene.fog = new THREE.Fog(0x050508, 15, 40);

    sisCamera = new THREE.PerspectiveCamera(50, w / h, 0.1, 100);
    sisCamera.position.set(12, 8, 15);
    sisCamera.lookAt(0, 2, 0);

    sisRenderer = new THREE.WebGLRenderer({ antialias: true });
    sisRenderer.setSize(w, h);
    sisRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    sisRenderer.shadowMap.enabled = true;
    container.appendChild(sisRenderer.domElement);

    sisControls = new OrbitControls(sisCamera, sisRenderer.domElement);
    sisControls.enableDamping = true;
    sisControls.target.set(0, 2, 0);

    // Lighting
    sisScene.add(new THREE.AmbientLight(0x222233, 0.4));
    const sunLight = new THREE.DirectionalLight(0xffeeba, 1.2);
    sunLight.position.set(8, 15, 5);
    sunLight.castShadow = true;
    sisScene.add(sunLight);
    const rimLight = new THREE.PointLight(0x00ffff, 0.6, 20);
    rimLight.position.set(-5, 8, -3);
    sisScene.add(rimLight);
    const heelLight = new THREE.PointLight(0xff0000, 0, 5);
    heelLight.position.set(0, 3, 0);
    sisScene.add(heelLight);

    // === THE SLOPE (30° inclined plane) ===
    const slopeLen = 20, slopeW = 10;
    const slopeGeo = new THREE.PlaneGeometry(slopeLen, slopeW, 32, 12);
    const slopeMat = new THREE.MeshStandardMaterial({
        color: 0x1a1a2e,
        roughness: 0.85,
        metalness: 0.1,
        wireframe: false,
    });
    sisSlope = new THREE.Mesh(slopeGeo, slopeMat);
    sisSlope.receiveShadow = true;
    const slopeRad = (state.slopeAngle * Math.PI) / 180;
    sisSlope.rotation.x = -Math.PI / 2 + slopeRad;
    sisSlope.position.set(0, slopeLen / 2 * Math.sin(slopeRad) / 2, 0);
    sisScene.add(sisSlope);

    const gridHelper = new THREE.GridHelper(slopeLen, 24, 0x333355, 0x1a1a33);
    gridHelper.rotation.x = slopeRad;
    gridHelper.position.copy(sisSlope.position);
    sisScene.add(gridHelper);

    // === THE MANUS PEN & CUBIT PLATFORM ===

    // The glowing golden pen tip
    const penGeo = new THREE.SphereGeometry(0.3, 32, 32);
    const penMat = new THREE.MeshStandardMaterial({
        color: 0xffd700,
        emissive: 0xd4af37,
        emissiveIntensity: 0.5,
        roughness: 0.2,
        metalness: 0.8
    });
    sisPenTip = new THREE.Mesh(penGeo, penMat);
    sisPenTip.castShadow = true;
    sisScene.add(sisPenTip);

    // The Manus Lever Arm (6 units = 1 Cubit)
    const armLen = 6;
    const armGeo = new THREE.CylinderGeometry(0.08, 0.15, armLen, 16);
    armGeo.translate(0, armLen / 2, 0); // pivot at base
    const armMat = new THREE.MeshStandardMaterial({
        color: 0xc9a84c,
        roughness: 0.5,
        metalness: 0.6,
        transparent: true,
        opacity: 0.8
    });
    sisManusArm = new THREE.Mesh(armGeo, armMat);
    sisScene.add(sisManusArm);

    // Achilles Heel glow (at the pen tip pushing interface)
    const heelGeo = new THREE.SphereGeometry(0.4, 16, 16);
    const heelMat = new THREE.MeshBasicMaterial({
        color: 0xff0000,
        transparent: true,
        opacity: 0.8,
    });
    sisHeelGlow = new THREE.Mesh(heelGeo, heelMat);
    sisScene.add(sisHeelGlow);

    // === GRANT ICOSIDODECAHEDRON MERKABA ===
    sisMerkabaGroup = new THREE.Group();
    const tet1Geo = new THREE.TetrahedronGeometry(1.5, 0);
    const tet2Geo = new THREE.TetrahedronGeometry(1.5, 0);
    tet2Geo.rotateZ(Math.PI);
    tet2Geo.rotateY(Math.PI / 4); // Realign for precise star tetrahedron
    const merkabaMat = new THREE.LineBasicMaterial({ color: 0x00ffff, transparent: true, opacity: 0.3 });
    const tetEdges1 = new THREE.EdgesGeometry(tet1Geo);
    const tetEdges2 = new THREE.EdgesGeometry(tet2Geo);
    const tet1 = new THREE.LineSegments(tetEdges1, merkabaMat);
    const tet2 = new THREE.LineSegments(tetEdges2, merkabaMat);

    // Icosidodecahedron (Icosahedron + Dodecahedron)
    const icoGeo = new THREE.IcosahedronGeometry(0.85, 0);
    const dodecGeo = new THREE.DodecahedronGeometry(0.85, 0);
    const icoMat = new THREE.LineBasicMaterial({ color: 0xc9a84c, transparent: true, opacity: 0.5 });
    const icoEdges = new THREE.EdgesGeometry(icoGeo);
    const dodecEdges = new THREE.EdgesGeometry(dodecGeo);
    const ico = new THREE.LineSegments(icoEdges, icoMat);
    const dodec = new THREE.LineSegments(dodecEdges, icoMat);

    sisMerkabaGroup.add(tet1);
    sisMerkabaGroup.add(tet2);
    sisMerkabaGroup.add(ico);
    sisMerkabaGroup.add(dodec);
    sisScene.add(sisMerkabaGroup);

    // === TORSIONAL INK TRAIL ===
    const trailCount = 5000;
    const trailGeo = new THREE.BufferGeometry();
    const tPos = new Float32Array(trailCount * 3);
    const tCol = new Float32Array(trailCount * 3);
    for (let i = 0; i < trailCount; i++) {
        tPos[i * 3] = 0; tPos[i * 3 + 1] = -100; tPos[i * 3 + 2] = 0;
        tCol[i * 3] = 0; tCol[i * 3 + 1] = 1; tCol[i * 3 + 2] = 1;
    }
    trailGeo.setAttribute('position', new THREE.BufferAttribute(tPos, 3));
    trailGeo.setAttribute('color', new THREE.BufferAttribute(tCol, 3));
    const trailMat = new THREE.PointsMaterial({
        size: 0.08,
        vertexColors: true,
        transparent: true,
        opacity: 0.9,
        blending: THREE.AdditiveBlending,
    });
    sisDustParticles = new THREE.Points(trailGeo, trailMat);
    sisScene.add(sisDustParticles);
    sisTrailPositions = tPos;

    new ResizeObserver(() => {
        const cw = container.clientWidth, ch = container.clientHeight;
        sisCamera.aspect = cw / ch;
        sisCamera.updateProjectionMatrix();
        sisRenderer.setSize(cw, ch);
    }).observe(container);

    animateSisyphus(heelLight);
}

let sisDustIdx = 0;

function animateSisyphus(heelLight) {
    requestAnimationFrame(() => animateSisyphus(heelLight));
    if (state.activeTab !== 'sisyphus') return;

    if (!sisFalling) sisTime += 0.016;
    else sisTime -= 0.032;

    const t = sisTime;
    const effort = state.pushEffort;
    const slopeRad = (state.slopeAngle * Math.PI) / 180;

    // === KINETIC LOOP: Pen pushed up, falls down ===
    if (!sisFalling) {
        sisOffset += 0.0015 + effort * 0.004;
        if (sisOffset >= 1) {
            sisFalling = true;
            sisOffset = 1;
        }
    } else {
        sisOffset -= 0.015 + (1 - effort) * 0.02;
        if (sisOffset <= 0) {
            sisFalling = false;
            sisOffset = 0;
            sisDustIdx = 0; // Clear ink on reset
        }
    }

    // === GRANT 12-STRAND: ICOSIDODECAHEDRON STACK ===
    // We treat the upward push as progress along the Root 42 / DNA geometric axis.
    const dnaProgress = sisOffset * 60; // Up to 60 base pairs / stack levels
    const dnaPitch = 3.4;   // 3-Logic (Pythagorean Rise)
    const dnaRadius = 2.0;  // 4-Logic (Density width / Icosidodecahedron radius)
    const basePairs = 10;   // 5-Logic (Decagonal Partition) 36 deg per base

    // We project the 12-strand helix onto the slope plane.
    const helixTheta = (dnaProgress / basePairs) * Math.PI * 2;

    const root42Scale = 1.4142; // Root 42 axis alignment approximation
    const helixLift = (dnaProgress / 10) * dnaPitch * root42Scale; // Z-axis lift before slope map

    // === MITOCHONDRIAL CRISTAE & STRAND EMERGENCE ===
    // 6→7 Leaning: At lower effort (6/Compression), only 2 strands are visible.
    // Higher effort (7/Expansion) activates dormant strands linearly up to 12.
    let activeStrands = 2;
    if (effort > 0.45) {
        activeStrands = 2 + Math.floor((effort - 0.45) * 22);
    }
    if (activeStrands > 12) activeStrands = 12;

    // Calculate 12 strands emerging from the Icosidodecahedron stellations
    const strandPositions = [];
    for (let i = 0; i < 12; i++) {
        const strandOffset = (i / 12) * Math.PI * 2;

        // Dormant strands sit at radius 0, active strands pop into geometry.
        const stellationRadius = (i < activeStrands) ? (dnaRadius * (0.5 + effort * 0.5)) : 0;

        const strX = Math.cos(helixTheta + strandOffset) * stellationRadius;
        const strZ = Math.sin(helixTheta + strandOffset) * stellationRadius;

        // Slope projection
        const sX = strX;
        const sY = 0.5 + Math.sin(slopeRad) * (helixLift + 4);
        const sZ = Math.cos(slopeRad) * (helixLift + 4) + strZ;
        strandPositions.push(new THREE.Vector3(sX, sY, sZ));
    }

    // The main Pen Tip follows Strand 0 to center the viewpoint and stress calculations
    sisPenTip.position.copy(strandPositions[0]);

    // Position Manus Arm (pushing from behind and below)
    const armLen = 6;
    const wobbleOffset = (Math.sin(6 * t) - Math.sin(7 * t)) * 0.15 * effort;
    const pushAngle = slopeRad + wobbleOffset;

    // Compute pushing unit vector and place the arm so its tip is at the pen tip
    const pushDx = Math.cos(pushAngle);
    const pushDy = Math.sin(pushAngle);
    sisManusArm.position.copy(sisPenTip.position).add(new THREE.Vector3(0, -armLen / 2 * pushDy, -armLen / 2 * pushDx));
    sisManusArm.lookAt(sisPenTip.position);

    // Track the trail for Hardcard
    state.hardcard.trail.push(sisPenTip.position.clone());
    if (state.hardcard.trail.length > 120) state.hardcard.trail.shift();

    // === APPLY HARDCARD ===
    const hcResult = applyHardcard(sisPenTip.position, state.hardcard.trail, state.slopeAngle);

    // Map Node 47 (Achilles Heel) to a T-G Mutation
    // When we hit base pair 47 in the sequence, simulate a "Soft Spot"
    const currentBP = Math.floor(dnaProgress);
    const isMutation = (currentBP === ACHILLES_NODE);
    if (isMutation) {
        hcResult.vitrificationPotential *= 0.1; // Rupture the hardcard potential
        hcResult.isLocked = false;
    }

    // === OVERPACK DELTA STRESS GLOW ===
    let stressNorm = hcResult.vitrificationPotential;
    if (isMutation) stressNorm = 1.0; // Max stress on mutation

    sisHeelGlow.position.copy(sisPenTip.position);
    sisHeelGlow.scale.setScalar(0.8 + stressNorm * 3);
    sisHeelGlow.material.opacity = 0.1 + stressNorm * 0.7;
    sisHeelGlow.material.color.setHex(isMutation ? 0xff0000 : (stressNorm > 0.8 ? 0x00ffff : 0xffd700));
    heelLight.intensity = stressNorm * 2;
    heelLight.position.copy(sisHeelGlow.position);

    // === POSITION & ANIMATE THE MERKABA CORE ===
    sisMerkabaGroup.position.copy(sisPenTip.position);
    sisMerkabaGroup.rotation.y = t * 0.8;
    sisMerkabaGroup.rotation.x = t * 0.5;
    sisMerkabaGroup.scale.setScalar(0.8 + effort * 0.7);

    // Flash Merkaba based on Vitrification status
    if (isMutation) {
        sisMerkabaGroup.scale.setScalar((0.8 + effort * 0.7) * (1 + Math.sin(t * 20) * 0.1)); // Shudder on mutation
        sisMerkabaGroup.children[2].material.color.setHex(0xff0000); // Inner icosidodecahedron turns red
        sisMerkabaGroup.children[3].material.color.setHex(0xff0000);
    } else if (hcResult.isLocked) {
        sisMerkabaGroup.children[2].material.color.setHex(0x00ffff); // Turns cyan when locked/ATP created
        sisMerkabaGroup.children[3].material.color.setHex(0x00ffff);
    } else {
        sisMerkabaGroup.children[2].material.color.setHex(0xc9a84c); // Dormant gold
        sisMerkabaGroup.children[3].material.color.setHex(0xc9a84c);
    }

    // === TORSIONAL INK DEPOSITION (12-Strand Geometry) ===
    if (!sisFalling && Math.random() < 0.6 + effort * 0.4) {
        const idx = sisDustIdx % (sisTrailPositions.length / 3);

        // Randomly pick an *active* strand to trace, creating the geometric effect
        const randomStrandIdx = Math.floor(Math.random() * activeStrands);
        const activeStrand = strandPositions[randomStrandIdx];

        sisTrailPositions[idx * 3] = activeStrand.x;
        sisTrailPositions[idx * 3 + 1] = activeStrand.y - 0.2;
        sisTrailPositions[idx * 3 + 2] = activeStrand.z + wobbleOffset * 2;

        // Ink Color based on Phase Lock & Mutation
        const dustColors = sisDustParticles.geometry.attributes.color.array;
        if (isMutation) {
            dustColors[idx * 3] = 1.0; dustColors[idx * 3 + 1] = 0.0; dustColors[idx * 3 + 2] = 0.2; // T-G Mismatch (Red)
        } else if (hcResult.isLocked) {
            // Give each of the 12 strands a slightly varying cyan/blue hue when vitrified
            dustColors[idx * 3] = (randomStrandIdx / 12) * 0.3;
            dustColors[idx * 3 + 1] = 0.8 + (randomStrandIdx / 12) * 0.2;
            dustColors[idx * 3 + 2] = 1.0; // Vitrified Fold (Cyan variant)
        } else {
            dustColors[idx * 3] = 0.8; dustColors[idx * 3 + 1] = 0.6; dustColors[idx * 3 + 2] = 0.2; // Fluid Vapor (Gold)
        }
        sisDustParticles.geometry.attributes.color.needsUpdate = true;
        sisDustIdx++;
    }
    sisDustParticles.geometry.attributes.position.needsUpdate = true;

    // Fade old ink slowly (Gravity drip)
    const totalParticles = sisTrailPositions.length / 3;
    for (let i = 0; i < 20; i++) {
        const fadeIdx = Math.floor(Math.random() * totalParticles);
        if (sisTrailPositions[fadeIdx * 3 + 1] > -50) {
            sisTrailPositions[fadeIdx * 3 + 1] -= 0.02;
            sisTrailPositions[fadeIdx * 3] -= 0.02 * Math.cos(slopeRad);
        }
    }

    // Update UI readouts
    updateEl('readout-boulder-phase', sisFalling ? 'UNWINDING' : 'SYNTHESIZING');
    updateEl('readout-slope', state.slopeAngle + '°');
    const vitriState = isMutation ? 'T-G MISMATCH' : (hcResult.isLocked ? 'VITRIFIED FOLD' : 'FLUID VAPOR');
    updateEl('readout-vitri', vitriState);
    updateEl('stress-percent', (stressNorm * 100).toFixed(1) + '%');

    // Updates for new Hardcard Panel
    updateEl('val-vit-pot', hcResult.vitrificationPotential.toFixed(3));
    updateEl('val-reversal', hcResult.reversal?.type ?? '—');

    // Check ATP Strike and Phase Lock
    let displayStrands = activeStrands;
    let atpStrike = hcResult.vitrificationPotential >= 0.8763; // The Hades Threshold
    if (atpStrike) displayStrands = 12; // Complete vitrification locks all 12 strands!

    updateEl('val-strands', displayStrands);

    const phaseLockInd = document.getElementById('phase-lock-indicator');
    if (hcResult.phaseLock || hcResult.isLocked) {
        if (phaseLockInd) phaseLockInd.classList.add('active');
        updateEl('val-locked-number', hcResult.phaseLock ? hcResult.phaseLock.value.toFixed(4) : "6.4807 (R42)");
    } else {
        if (phaseLockInd) phaseLockInd.classList.remove('active');
        updateEl('val-locked-number', '—');
    }

    const atpInd = document.getElementById('atp-indicator');
    if (atpStrike && !isMutation) {
        if (atpInd) atpInd.classList.add('active');
    } else {
        if (atpInd) atpInd.classList.remove('active');
    }

    const sfill = document.getElementById('stress-fill');
    if (sfill) {
        sfill.style.width = (stressNorm * 100) + '%';
        sfill.style.background = isMutation
            ? 'linear-gradient(90deg, #ff0000, #ff0000)'
            : (hcResult.isLocked
                ? 'linear-gradient(90deg, #00ffff, #00ff88)'
                : 'linear-gradient(90deg, #ffd700, #ff6f61)');
    }
    const sStatus = document.getElementById('stress-status');
    if (sStatus) {
        sStatus.textContent = isMutation
            ? '⚠️ NODE 47 FRACTURE: T-G Mismatch Detected!'
            : (hcResult.isLocked
                ? '✓ 33-Node Resonance: Protein Fold Vitrified'
                : '⚡ Scanning base pairs... Torsional Force increasing');
    }

    sisControls.update();
    sisRenderer.render(sisScene, sisCamera);
}

// ============================================================================
// CONTROL BINDINGS — Wire everything up
// ============================================================================
function updateEl(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
}

function bindControls() {
    // Hades slider
    bind('hades-slider', 'hades-val', v => {
        state.hades = v;
        if (latticeInitialized) buildLatticeMesh();
    });

    // Distortion
    bind('distortion-slider', 'distortion-val', v => {
        state.distortion = v;
        if (latticeInitialized) buildLatticeMesh();
    });

    // Rotation
    bind('rotation-slider', 'rotation-val', v => { state.rotationSpeed = v; });

    // View modes
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.viewMode = btn.dataset.mode;
            if (latticeInitialized) buildLatticeMesh();
        });
    });

    // Ladder steps
    document.querySelectorAll('.step-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.step-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.activeStep = parseInt(btn.dataset.step);
            if (latticeInitialized) buildLatticeMesh();
        });
    });

    // Audio controls
    document.getElementById('play-hades').addEventListener('click', () => {
        if (audio.playing) {
            audio.stop();
            state.audioPlaying = false;
            document.getElementById('play-hades').classList.remove('playing');
            updateEl('play-icon', '▶');
            updateEl('play-label', 'Play Hades Beat');
        } else {
            audio.play(state.freqL, state.freqR, state.volume);
            state.audioPlaying = true;
            document.getElementById('play-hades').classList.add('playing');
            updateEl('play-icon', '■');
            updateEl('play-label', 'Stop Hades Beat');
        }
    });

    bind('volume-slider', 'volume-val', v => { state.volume = v; });
    bind('freq-l-slider', 'freq-l-val', v => {
        state.freqL = v;
        updateEl('freq-l-val', v + ' Hz');
        updateEl('readout-beat', Math.abs(state.freqL - state.freqR).toFixed(2) + ' Hz');
        if (audio.playing) audio.play(state.freqL, state.freqR, state.volume);
    }, true);
    bind('freq-r-slider', 'freq-r-val', v => {
        state.freqR = v;
        updateEl('freq-r-val', v + ' Hz');
        updateEl('readout-beat', Math.abs(state.freqL - state.freqR).toFixed(2) + ' Hz');
        if (audio.playing) audio.play(state.freqL, state.freqR, state.volume);
    }, true);

    // Pyramid controls
    bind('time-slider', 'time-val', v => { state.time = v; });
    bind('lambda-slider', 'lambda-val', v => { state.lambda = v; });

    document.querySelectorAll('.pyramid-view-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.pyramid-view-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.pyramidView = btn.dataset.view;
        });
    });

    // Sisyphus controls
    bind('effort-slider', 'effort-val', v => {
        state.pushEffort = v;
    });
    bind('slope-slider', 'slope-val', v => {
        state.slopeAngle = v;
        updateEl('slope-val', v + '°');
        if (sisyphusInitialized) {
            sisSlope.rotation.x = -Math.PI / 2 + (v * Math.PI) / 180;
            sisOffset = 0; // reset climb
            sisDustIdx = 0; // clear ink
            for (let i = 0; i < sisTrailPositions.length; i++) sisTrailPositions[i] = -100;
        }
    }, true);

    document.querySelectorAll('.spiral-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.spiral-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            state.spiralType = e.target.dataset.spiral;
            if (sisyphusInitialized) {
                sisOffset = 0; // Reset climb
                sisDustIdx = 0; // Clear ink
                for (let i = 0; i < sisTrailPositions.length; i++) sisTrailPositions[i] = -100;
            }
        });
    });
}

function bind(sliderId, badgeId, callback, isInt = false) {
    const slider = document.getElementById(sliderId);
    if (!slider) return;
    slider.addEventListener('input', () => {
        const v = isInt ? parseInt(slider.value) : parseFloat(slider.value);
        if (!isInt) updateEl(badgeId, v.toFixed(2));
        callback(v);
    });
}

// ============================================================================
// HARD CARD MODULE: Vitrification Layer for Penman-Sisyphus
// ============================================================================

function exportLockedNumbers(format = 'json') {
    const artifact = {
        metadata: {
            title: "Hardcard Vitrification Record",
            invariant: "1 - Hades Gap = 0.8763",
            phase_lock_threshold: "33-node coherence > 87.63%",
            generated: new Date().toISOString()
        },
        lockedEvents: state.hardcard.lockedNumbers.filter(e =>
            e.vitrificationPotential >= 0.8763 || e.lockedNumber || e.reversalType
        ),
        summary: {
            totalLocked: state.hardcard.lockedNumbers.length,
            phaseLocks: state.hardcard.lockedNumbers.filter(e => e.lockedNumber).length,
            reversals: state.hardcard.lockedNumbers.filter(e => e.reversalType).length,
            avgVitrification: state.hardcard.lockedNumbers.reduce((s, e) => s + e.vitrificationPotential, 0) /
                Math.max(1, state.hardcard.lockedNumbers.length)
        }
    };

    if (format === 'json') {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(artifact, null, 2));
        const dlAnchorElem = document.createElement('a');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", "diamond_precipitation_log.json");
        dlAnchorElem.click();
        return;
    }
}

// Make export globally available
window.exportLockedNumbers = exportLockedNumbers;

function computeTorsion(trail, idx) {
    if (trail.length < 4 || idx < 3) return 0;
    const p1 = trail[idx - 3], p2 = trail[idx - 2], p3 = trail[idx - 1], p4 = trail[idx];
    const d1 = new THREE.Vector3().subVectors(p2, p1);
    const d2 = new THREE.Vector3().subVectors(p3, p2);
    const d3 = new THREE.Vector3().subVectors(p4, p3);
    const cross = new THREE.Vector3().crossVectors(d1, d2);
    return Math.abs(d3.dot(cross)) / (cross.lengthSq() + 0.0001) * 10;
}

function computeCurvature(p1, p2, p3) {
    const d1 = new THREE.Vector3().subVectors(p2, p1);
    const d2 = new THREE.Vector3().subVectors(p3, p2);
    const dp = d1.normalize().dot(d2.normalize());
    return 1 - dp;
}

function computeSexagesimalCoherence(pt, base = 60) {
    const radius = pt.length();
    const angle = Math.atan2(pt.y, pt.x);
    // Radial alignment
    const radialDeviation = Math.abs(radius % (base / 12)) / (base / 12);
    const radialCoherence = 1 - Math.min(1, radialDeviation * 2);
    // Angular alignment with 30° sectors
    const sectorAngle = Math.PI * 2 / 12;
    const angularDeviation = Math.abs(angle % sectorAngle - sectorAngle / 2) / (sectorAngle / 2);
    const angularCoherence = 1 - angularDeviation;
    return (radialCoherence + angularCoherence) / 2;
}

function detectPhaseLock(fieldSamples, base = 60) {
    if (fieldSamples.length < 33) return null;
    let avgCoherence = 0;
    for (const val of fieldSamples) {
        avgCoherence += 1 - Math.abs((val % 60) - 33) / 60; // Simplified perfect fifth anchor check
    }
    avgCoherence /= fieldSamples.length;

    if (avgCoherence > 0.8763) {
        return {
            value: fieldSamples[fieldSamples.length - 1],
            phase: 33,
            certainty: avgCoherence,
            vitrified: true
        };
    }
    return null;
}

function applyHardcard(pt, trail, slopeDeg) {
    if (trail.length < 5) return { vitrificationPotential: 0, isLocked: false };

    const torsion = computeTorsion(trail, trail.length - 1);
    const cur = computeCurvature(trail[trail.length - 3], trail[trail.length - 2], trail[trail.length - 1]);
    const density = Math.min(1, 1 / (cur + 0.001));
    const coherence = computeSexagesimalCoherence(pt, 60);

    const vitrificationPotential = torsion * coherence * density;
    const isLocked = vitrificationPotential >= state.hardcard.vitrificationThreshold;

    const phaseLock = detectPhaseLock(
        trail.slice(-60).map(p => p.length()),
        60
    );

    let reversal = null;
    if (trail.length >= 7) {
        const recentCurvatures = [
            computeCurvature(trail[trail.length - 5], trail[trail.length - 4], trail[trail.length - 3]),
            computeCurvature(trail[trail.length - 4], trail[trail.length - 3], trail[trail.length - 2]),
            cur
        ];
        const dCurv = recentCurvatures[2] - recentCurvatures[1];
        const prevDCurv = recentCurvatures[1] - recentCurvatures[0];
        if (Math.sign(dCurv) !== Math.sign(prevDCurv) && Math.abs(dCurv) > 0.15) {
            reversal = { type: 'spiral-edge', position: pt };
        }
    }

    if (isLocked || phaseLock || reversal) {
        state.hardcard.lockedNumbers.push({
            t: performance.now(),
            position: pt.toArray(),
            torsion, curvature: cur, density, coherence,
            vitrificationPotential,
            lockedNumber: phaseLock?.value,
            reversalType: reversal?.type,
            slope: slopeDeg
        });
        if (state.hardcard.lockedNumbers.length > 200) state.hardcard.lockedNumbers.shift();
    }

    return { isLocked, phaseLock, reversal, vitrificationPotential };
}

// ============================================================================
// BOOT
// ============================================================================
populateConstants();
populateAudit();
bindControls();
initLattice(); // Start with lattice visible
