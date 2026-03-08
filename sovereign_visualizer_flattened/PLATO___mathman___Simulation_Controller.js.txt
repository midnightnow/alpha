/**
 * Simulation_Controller.js
 * Bridges the PMG Logic (Haric_Calibration_Module) with WebGL Rendering 
 * Provides real-time uniform updates for the Auric Mucus visualization.
 */

if (typeof THREE === 'undefined') {
    console.warn("THREE.js is not defined. Ensure it is loaded before Simulation_Controller.");
}

class SimulationController {
    constructor(visualizerCanvas, calibrationModule) {
        this.canvas = visualizerCanvas;
        this.calibration = calibrationModule;

        // PMG Base Invariants
        this.UNITY_THRESHOLD = 0.8254;
        this.HADES_SLACK = 0.005566;

        this.initWebGL();
        this.initShaderMaterial();

        // Animation loop state
        this.clock = new THREE.Clock();
        this.isRunning = false;

        // Target uniforms for smooth interpolation
        this.targetUniforms = {
            u_haric_phase: 1.0,
            u_auric_density: 0.8,
            u_physical_ground: 1.0
        };
    }

    initWebGL() {
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true, alpha: true });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        this.scene = new THREE.Scene();
        this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 10);
        this.camera.position.z = 1;

        // A simple full-screen plane to run the shader
        const geometry = new THREE.PlaneGeometry(2, 2);
        this.mesh = new THREE.Mesh(geometry);
        this.scene.add(this.mesh);

        // Handle Resizing
        window.addEventListener('resize', () => {
            this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        });
    }

    initShaderMaterial() {
        // Fetch shader code dynamically or rely on it being pre-loaded. 
        // For this bridge, we assume the shader string is accessible.
        // In a production setup, this would be an async fetch to `Auric_Mucus_Shader.glsl`.

        const vertexShader = `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `;

        // Dummy fragment for fallback, replacing with the actual glsl string via fetch later
        const defaultFragment = `
            uniform float u_time;
            varying vec2 vUv;
            void main() { gl_FragColor = vec4(vUv, sin(u_time), 1.0); }
        `;

        this.material = new THREE.ShaderMaterial({
            vertexShader: vertexShader,
            fragmentShader: defaultFragment, // Will be overridden
            uniforms: {
                u_time: { value: 0.0 },
                u_haric_phase: { value: 1.0 },       // Lift Vector
                u_auric_density: { value: 0.8 },     // Measure
                u_physical_ground: { value: 1.0 },    // Origin 10 String
                u_field_remainder: { value: 1.0 },   // Hades Gap Remainder
                u_unfold_progress: { value: 0.0 },    // Hinge-Unfold state
                u_stations: { value: [0.0, 1.0, 4.0, 5.0, 6.0, 7.0, 8.0] }, // Spinal Altitudes
                u_multiplicity: { value: [1, 2, 1, 4, 1, 2, 1] }            // Cadence
            }
        });

        this.mesh.material = this.material;
        this.loadMucusShader();
    }

    async loadMucusShader() {
        try {
            const response = await fetch('./Auric_Mucus_Shader.glsl');
            if (response.ok) {
                const fragmentCode = await response.text();
                this.material.fragmentShader = fragmentCode;
                this.material.needsUpdate = true;
                console.log("Mucus Shader successfully deployed to Plane.");
            } else {
                console.warn("Could not load Auric_Mucus_Shader.glsl. Using default fragment.");
            }
        } catch (e) {
            console.error("Fetch failed for shader:", e);
        }
    }

    /**
     * Bridges an external state change into a smooth uniform interpolation
     * @param {Object} newState 
     */
    applyDiagnosticState(newState) {
        if (newState.haric !== undefined) this.targetUniforms.u_haric_phase = newState.haric;
        if (newState.auric !== undefined) this.targetUniforms.u_auric_density = newState.auric;
        if (newState.physical !== undefined) this.targetUniforms.u_physical_ground = newState.physical;

        // Direct updates for construction uniforms (no lerp for these usually)
        if (newState.remainder !== undefined) this.material.uniforms.u_field_remainder.value = newState.remainder;
        if (newState.unfold !== undefined) this.material.uniforms.u_unfold_progress.value = newState.unfold;
    }

    /**
     * The Main Loop. Updates time and lerps the uniforms to their target values
     * to prevent visual flickering when a "Resonance Solve" is applied.
     */
    animate() {
        if (!this.isRunning) return;
        requestAnimationFrame(() => this.animate());

        const delta = this.clock.getDelta();
        const time = this.clock.getElapsedTime();

        // 1. Update Time
        this.material.uniforms.u_time.value = time;

        // 2. Smooth Interpolation (Lerp) of Diagnostic Uniforms
        const lerpFactor = 2.0 * delta; // Adjust speed of phase transition

        this.material.uniforms.u_haric_phase.value += (this.targetUniforms.u_haric_phase - this.material.uniforms.u_haric_phase.value) * lerpFactor;
        this.material.uniforms.u_auric_density.value += (this.targetUniforms.u_auric_density - this.material.uniforms.u_auric_density.value) * lerpFactor;
        this.material.uniforms.u_physical_ground.value += (this.targetUniforms.u_physical_ground - this.material.uniforms.u_physical_ground.value) * lerpFactor;

        this.renderer.render(this.scene, this.camera);
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.clock.start();
        this.animate();
    }

    stop() {
        this.isRunning = false;
        this.clock.stop();
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SimulationController;
}
