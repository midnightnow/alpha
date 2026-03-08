/**
 * resonance_engine_bridge.js
 * 
 * The Semantic Bridge connecting the Mathman Physics Engine (Javascript) 
 * to the Diagnostic Sieve (WebGL Shaders) and the Sovereign Ledger (JSON-LD).
 * 
 * Maps internal coordinates and intensities to PMG coherent forms:
 * - coherence       -> u_coherence
 * - torque          -> u_torque (vertex displacement amplitude)
 * - structuralPhase -> VAPOR (blue/gray), STONE (gold), DIAMOND (white)
 */

if (typeof SimulationController === 'undefined') {
    console.warn("SimulationController not found. Ensure Simulation_Controller.js is loaded first.");
}

class ResonanceEngineBridge {
    constructor(mathmanInstance, webglController, calibrationModule) {
        this.mathman = mathmanInstance;
        this.webgl = webglController;
        this.calibration = calibrationModule;

        // Ensure webgl uniforms have these base values added
        this.initExtendedUniforms();

        console.log("Resonance Engine Bridge Initialized. Torque mappings bound.");
    }

    initExtendedUniforms() {
        if (!this.webgl || !this.webgl.material) return;

        const uniforms = this.webgl.material.uniforms;

        // Add PMG specific tracking uniforms
        uniforms.u_coherence = { value: 0.8254 };
        uniforms.u_torque = { value: 0.0 };
        uniforms.u_structural_phase = { value: 1.0 }; // 0: Vapor, 1: Stone, 2: Diamond

        this.webgl.targetUniforms.u_coherence = 0.8254;
        this.webgl.targetUniforms.u_torque = 0.0;
        this.webgl.targetUniforms.u_structural_phase = 1.0;

        // Inject extended update logic into WebGL's animate loop
        const originalAnimate = this.webgl.animate.bind(this.webgl);
        this.webgl.animate = () => {
            if (!this.webgl.isRunning) return;

            const delta = this.webgl.clock.getDelta();
            const lerpFactor = 2.0 * delta;

            // Apply standard PMG lerps
            uniforms.u_coherence.value += (this.webgl.targetUniforms.u_coherence - uniforms.u_coherence.value) * lerpFactor;
            uniforms.u_torque.value += (this.webgl.targetUniforms.u_torque - uniforms.u_torque.value) * lerpFactor;
            uniforms.u_structural_phase.value += (this.webgl.targetUniforms.u_structural_phase - uniforms.u_structural_phase.value) * lerpFactor;

            // Allow original frame loop to render
            originalAnimate(true); // Call original with flag to prevent infinite recursion if badly scoped
        };

        // Update original animation logic to not re-request frame if called from bridge
        this.webgl.renderFrame = () => {
            const time = this.webgl.clock.getElapsedTime();
            uniforms.u_time.value = time;

            // Existing smooth interpolation (Lerp)
            const delta = this.webgl.clock.getDelta();
            const lerpFactor = 2.0 * delta;
            uniforms.u_haric_phase.value += (this.webgl.targetUniforms.u_haric_phase - uniforms.u_haric_phase.value) * lerpFactor;
            uniforms.u_auric_density.value += (this.webgl.targetUniforms.u_auric_density - uniforms.u_auric_density.value) * lerpFactor;
            uniforms.u_physical_ground.value += (this.webgl.targetUniforms.u_physical_ground - uniforms.u_physical_ground.value) * lerpFactor;

            // New extended interpolation
            uniforms.u_coherence.value += (this.webgl.targetUniforms.u_coherence - uniforms.u_coherence.value) * lerpFactor;
            uniforms.u_torque.value += (this.webgl.targetUniforms.u_torque - uniforms.u_torque.value) * lerpFactor;
            uniforms.u_structural_phase.value += (this.webgl.targetUniforms.u_structural_phase - uniforms.u_structural_phase.value) * lerpFactor;

            this.webgl.renderer.render(this.webgl.scene, this.webgl.camera);
        };

        this.webgl.animate = () => {
            if (!this.webgl.isRunning) return;
            requestAnimationFrame(() => this.webgl.animate());
            this.webgl.renderFrame();
        };
    }

    /**
     * Samples the current central point in the Mathman planar projection
     * and maps the physical wave properties into PMG Shader uniforms.
     */
    updateBridge() {
        if (!this.mathman) return;

        // 1. Measure: Extract intensity near the Haric axis (X=0, Y=scanY)
        const origins = this.mathman.getOrigins();
        const time = performance.now() / 1000;
        const k = (2 * Math.PI) / this.mathman.params.lambda;

        // Center of awareness (the scanned slice)
        const targetY = this.mathman.params.scanY;
        const intensityData = this.mathman.getIntensity(0, targetY, 0, origins, k, time, true);

        // 2. Decode Coherence & Stagnation
        // Lower abs intensity or higher stagnation = Auric Mucus
        const coherenceRaw = intensityData.intensity;
        const stagnation = intensityData.stagnation;

        // Map to PMG Thresholds
        const UNITY = 0.8254;
        const HADES_SLACK = 0.005566;

        // Assume maximum harmony leads to 1.0 (or greater limit)
        // Adjust formula for normalized coherence
        let coherenceMapped = Math.abs(coherenceRaw) * (1.0 - stagnation * 0.5);
        if (coherenceMapped > 1.0) coherenceMapped = 1.0;

        let structuralPhase = 1.0; // STONE
        let torquePhase = 0.0;

        if (coherenceMapped < UNITY) {
            structuralPhase = 0.0; // VAPOR / MUCUS
            // Try to solve for resonance using calibration module if available
            if (this.calibration) {
                const solution = this.calibration.solveForResonance({
                    id: "FocusRing",
                    intensity: coherenceMapped,
                    sourcePhase: this.mathman.params.phiB
                });

                if (solution.action === "INJECT_LIFT") {
                    torquePhase = solution.newPhase - this.mathman.params.phiB;
                    // For visualization, map torque to a visible amplitude spike
                    this.webgl.targetUniforms.u_torque = torquePhase * 0.5;
                }
            }
        } else if (coherenceMapped > 0.9999) {
            structuralPhase = 2.0; // DIAMOND / VITRIFICATION
        } else {
            // Healthy Buoyant/Stone state
            this.webgl.targetUniforms.u_torque = 0.0; // No torque needed
        }

        // 4. Inject visual state to WebGL Target Uniforms
        if (this.webgl) {
            this.webgl.targetUniforms.u_coherence = coherenceMapped;
            this.webgl.targetUniforms.u_structural_phase = structuralPhase;

            // Update Base Variables
            this.webgl.targetUniforms.u_haric_phase = this.mathman.params.phiB / 360;
            this.webgl.targetUniforms.u_auric_density = 1.0 - stagnation;
            this.webgl.targetUniforms.u_physical_ground = 1.0;
        }
    }

    /**
     * To be called during Mathman's render loop to sync state.
     */
    tick() {
        this.updateBridge();
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResonanceEngineBridge;
}
