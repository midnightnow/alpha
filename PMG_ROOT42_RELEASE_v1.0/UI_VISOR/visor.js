/**
 * ALPHA Visor - The Pinhole Camera of the .veth Schema
 * Implements the Manic Grafia projection: Number, Light, Darkness.
 */

const canvas = document.getElementById('visor-canvas');
const ctx = canvas.getContext('2d');
const hexLabel = document.getElementById('hex-header');
const btnDisturb = document.getElementById('btn-disturb');
const btnRepair = document.getElementById('btn-repair');
const tensionDot = document.getElementById('tension-dot');
const tensionStatus = document.getElementById('tension-status');
const hysteresisVal = document.getElementById('hysteresis-val');
const debtCard = document.getElementById('debt-card');

Math.TAU = Math.PI * 2;

// Constants (The Solid)
const C = {
    A: 5, B: 12, P: 30,  // 5-12-13 Triangle (Area=Perimeter)
    R42: Math.sqrt(42),  // The Aperture 
    R24: Math.sqrt(24),  // The Measure
    EYE: 24,             // 24mm Eyeball (Radius = 12)
    NODES: 93,           // 3+30+60 (Solid Points)
    ANG_42: (42 * Math.PI) / 180,
    BASE_HEX: '0x1F01BC1FF507F805ED8210E2'
};

// Canvas Setup
const SIZE = 600;
canvas.width = SIZE;
canvas.height = SIZE;
const CENTER = SIZE / 2;
const RADIUS = 250;

// State
let state = {
    isTaut: true,
    rotation: 0,
    wobble: 0,
    hysteresis: 0,
    nodes: [],
    // Generates the 93 points of the solid
    async loadRecord() {
        try {
            const resp = await fetch('point_001.veth');
            const data = await resp.json();
            
            // Re-render based on realistic values
            hexLabel.textContent = data.header.hex;
            this.hysteresis = data.hysteresis;
            this.isTaut = data.isTaut;
            
            // Build the string tension
            tensionDot.className = this.isTaut ? 'dot active' : 'dot warning';
            tensionStatus.textContent = this.isTaut ? 'TAUT (SHEER FACE)' : 'SLACK (HYSTERESIS DETECTED)';
            tensionStatus.style.color = this.isTaut ? 'var(--accent-green)' : 'var(--accent-red)';
            
            hysteresisVal.textContent = this.hysteresis + '°';
            
            // Build nodes from the field counts (Volume I, II, III)
            this.nodes = [];
            // Seed nodes representing fields
            const totalFields = data.header.count + data.header.measure + data.header.comm;
            for(let i=0; i<30; i++) {
                const angle = (i / 30) * Math.TAU;
                const active = i < totalFields;
                this.nodes.push({ r: RADIUS * 0.8, a: angle, type: 'seed', active: active, dR: 0, dA: 0 });
            }
            // Shell nodes
            for(let i=0; i<60; i++) {
                const angle = (i / 60) * Math.TAU;
                const r = (i % 2 === 0) ? RADIUS : RADIUS * 0.9;
                this.nodes.push({ r: r, a: angle + (Math.PI/60), type: 'shell', dR: 0, dA: 0 });
            }
            for(let i=0; i<3; i++) {
                const angle = (i / 3) * Math.TAU;
                this.nodes.push({ r: RADIUS * 0.2, a: angle, type: 'core', dR: 0, dA: 0 });
            }
            
            if (this.isTaut) {
                this.repair();
            } else {
                this.disturb();
            }

        } catch (e) {
            console.error('Failed to load record:', e);
            this.initNodes(); // fallback
        }
    },
    initNodes() {
        this.nodes = [];
        // The 30 Field Types (The Perimeter/Area)
        for (let i = 0; i < 30; i++) {
            const angle = (i / 30) * Math.TAU;
            // Radius scales to 24mm Measure mapping
            this.nodes.push({ r: RADIUS * 0.8, a: angle, type: 'seed', dR: 0, dA: 0 });
        }
        // The 60 MW-Shell Nodes
        for (let i = 0; i < 60; i++) {
            const angle = (i / 60) * Math.TAU;
            // Staggered radius
            const r = (i % 2 === 0) ? RADIUS : RADIUS * 0.9;
            this.nodes.push({ r: r, a: angle + (Math.PI / 60), type: 'shell', dR: 0, dA: 0 });
        }
        // The 3 Core Nodes (The Trinity)
        for (let i = 0; i < 3; i++) {
            const angle = (i / 3) * Math.TAU;
            this.nodes.push({ r: RADIUS * 0.2, a: angle, type: 'core', dR: 0, dA: 0 });
        }
    },

    disturb() {
        this.isTaut = false;
        this.hysteresis = 9.4623;

        // Push the nodes into disorder (The Tent Flapping)
        this.nodes.forEach(n => {
            n.dR = (Math.random() - 0.5) * 40;
            n.dA = (Math.random() - 0.5) * 0.2;
        });

        // Update UI
        hexLabel.textContent = '0x1F01BC1FF507F805ED[CORRUPT]';
        hexLabel.style.color = 'var(--accent-red)';
        hexLabel.style.borderLeftColor = 'var(--accent-red)';
        hexLabel.style.textShadow = '0 0 5px rgba(255, 51, 102, 0.5)';

        tensionDot.className = 'dot warning';
        tensionStatus.textContent = 'SLACK (HYSTERESIS DETECTED)';
        tensionStatus.style.color = 'var(--accent-red)';

        hysteresisVal.textContent = this.hysteresis + '°';
        hysteresisVal.parentElement.classList.add('warning');

        debtCard.querySelector('.value').textContent = 'ENGAGE PUMP';
        debtCard.classList.add('warning');

        btnDisturb.disabled = true;
        btnRepair.disabled = false;
    },

    repair() {
        this.isTaut = true;
        this.hysteresis = 0;

        // Snap back to integer equilibrium using easing in the render loop
        // Update UI
        hexLabel.textContent = C.BASE_HEX;
        hexLabel.style.color = 'var(--accent-cyan)';
        hexLabel.style.borderLeftColor = 'var(--accent-cyan)';
        hexLabel.style.textShadow = '0 0 5px rgba(0, 240, 255, 0.3)';

        tensionDot.className = 'dot active';
        tensionStatus.textContent = 'TAUT (ZERO HYSTERESIS)';
        tensionStatus.style.color = 'var(--accent-green)';

        hysteresisVal.textContent = '0.000000°';
        hysteresisVal.parentElement.classList.remove('warning');

        debtCard.querySelector('.value').textContent = '-1/12';
        debtCard.classList.remove('warning');

        btnDisturb.disabled = false;
        btnRepair.disabled = true;
    }
};

// Projection / Render Loop
function render() {
    ctx.clearRect(0, 0, SIZE, SIZE);

    // Smooth Transition Logic
    state.rotation += 0.005; // Base spin (The Umbrella)

    if (state.isTaut) {
        // Tension pulls the nodes back to their integer coordinates (dR, dA -> 0)
        state.nodes.forEach(n => {
            n.dR *= 0.9;
            n.dA *= 0.9;
        });
        state.wobble *= 0.95;
    } else {
        // Hysteresis introduces ongoing noise
        state.wobble = Math.sin(Date.now() / 100) * 10;
    }

    // 1. Draw the 42° Aperture Field
    ctx.beginPath();
    ctx.arc(CENTER, CENTER, RADIUS, 0, Math.TAU);
    ctx.strokeStyle = state.isTaut ? 'rgba(0, 240, 255, 0.1)' : 'rgba(255, 51, 102, 0.1)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // The Cross (24/37 axes)
    const stretchX = CENTER + Math.cos(state.rotation) * RADIUS;
    const stretchY = CENTER + Math.sin(state.rotation) * RADIUS;
    const opStretchX = CENTER + Math.cos(state.rotation + Math.PI) * RADIUS;
    const opStretchY = CENTER + Math.sin(state.rotation + Math.PI) * RADIUS;

    ctx.beginPath();
    ctx.moveTo(opStretchX, opStretchY);
    ctx.lineTo(stretchX, stretchY);
    ctx.moveTo(CENTER + Math.cos(state.rotation + Math.PI / 2) * RADIUS, CENTER + Math.sin(state.rotation + Math.PI / 2) * RADIUS);
    ctx.lineTo(CENTER + Math.cos(state.rotation - Math.PI / 2) * RADIUS, CENTER + Math.sin(state.rotation - Math.PI / 2) * RADIUS);
    ctx.strokeStyle = state.isTaut ? 'rgba(255, 255, 255, 0.05)' : 'rgba(255, 51, 102, 0.1)';
    ctx.stroke();

    // 2. Draw the Nodes (The Stitch Holes)
    ctx.save();
    ctx.translate(CENTER, CENTER);
    ctx.rotate(state.rotation + Math.cos(Date.now() / 500) * (state.isTaut ? 0.01 : 0.1));

    ctx.beginPath();
    state.nodes.forEach((n, idx) => {
        // Apply physics
        const actR = n.r + n.dR + (Math.random() * state.wobble);
        const actA = n.a + n.dA;

        const x = Math.cos(actA) * actR;
        const y = Math.sin(actA) * actR;

        if (idx === 0) ctx.moveTo(x, y);

        // Draw connections for the shell
        if (n.type === 'shell') {
            ctx.lineTo(x, y);
        }

        // Draw the point (Pinhole)
        ctx.fillStyle = state.isTaut ?
            (n.type === 'core' ? '#fff' : (n.type === 'seed' ? 'var(--accent-cyan)' : 'var(--text-dim)')) :
            'var(--accent-red)';

        let dotSize = n.type === 'core' ? 4 : (n.type === 'seed' ? 3 : 2);
        if (!state.isTaut) dotSize += Math.random() * 2; // Blur effect

        ctx.fillRect(x - dotSize / 2, y - dotSize / 2, dotSize, dotSize);

        // The 5-12-13 Connection Lines (Draw lines from shell back to core)
        if (state.isTaut && n.type === 'seed' && n.active && (idx % 3 === 0)) {
            const coreAngle = (idx % 3) * (Math.TAU / 3);
            const cx = Math.cos(coreAngle) * (RADIUS * 0.2);
            const cy = Math.sin(coreAngle) * (RADIUS * 0.2);

            ctx.save();
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(cx, cy);
            // The -1/12 Tension lines (very faint)
            ctx.strokeStyle = 'rgba(0, 255, 102, 0.05)';
            ctx.stroke();
            ctx.restore();
        }
    });

    if (state.isTaut) {
        ctx.strokeStyle = 'rgba(148, 163, 184, 0.1)'; // Suave
    } else {
        ctx.strokeStyle = 'rgba(255, 51, 102, 0.3)'; // Savage / Hairy
    }
    ctx.lineWidth = state.isTaut ? 0.5 : 2;
    ctx.stroke();

    ctx.restore();

    requestAnimationFrame(render);
}

// Init
state.loadRecord();

btnDisturb.addEventListener('click', () => state.disturb());
btnRepair.addEventListener('click', () => state.repair());

render();
