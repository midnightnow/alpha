/**
 * Hardcard.js - The "Ceramic Math" Core
 * Focuses on the "Remainder Delay" and "Flea Vortex" recursion.
 * 
 * Logic: 
 * 4 primary waves (Scaffolding) 
 * + 1 remainder (The Delay) 
 * = The 5th Element (Standing Man Materialization)
 */

class Hardcard {
    constructor() {
        this.version = "1.0.0-Ceramic";
        this.fleaRecursionLimit = 5; // Default limit for "flea" vortices
        this.temporalBuffer = [];
        this.maxBufferSize = 60; // 1 second @ 60fps

        // Platonic 4 Space Constraints
        this.boundaryD = 4.0; // The "Wall"
        this.idealRate = 1.0; // 1 pulse/s
        this.syncLock = true;
    }

    /**
     * Calculates the Resonance Tolerance of the 4-unit space.
     * Higher drift leads to higher "Auric Mucus" (stagnation).
     */
    calculateResonanceTolerance(vibrationAmplitude = 0) {
        // The error is the delta from the ideal Platonic 4 boundary
        const syncError = Math.abs(vibrationAmplitude);

        // Tolerance decreases as the wall vibrates away from the 4.0 static state
        const tolerance = Math.exp(-syncError * 2.0);

        // Return coherence percentage (0 to 1)
        return Math.max(0, tolerance);
    }

    /**
     * Measures the decay of the Standing Man's vitrified state.
     * If the rhythm (flea frequency) drifts from the WebGL refresh/pulse rate, 
     * the coherence erodes.
     */
    getVitrificationDecay(time) {
        if (this.syncLock) return 0;
        // Drifting effect: simulated as a slow sine-wave of decoherence
        return (1 + Math.sin(time * 0.1)) * 0.5;
    }

    /**
     * Calculates the "Ceramic Remainder" delay using Echo Reflection.
     * Logic: A pulse at origin (0) travels to the wall (4) and returns.
     * The Standing Man is the reinforcement at the 5th state (the Barycenter).
     */
    calculateRemainderDelay(time, intensity, recursionLevel = 5) {
        let echoSum = 0;

        // The Outbound Pulse
        const outbound = Math.cos(time * this.idealRate);

        // The Inbound Echo (Reflected off boundaryD)
        // Travel time for return trip = (boundaryD * 2) / speed
        const travelTime = (this.boundaryD * 2) / this.idealRate;
        const inbound = Math.cos((time - travelTime) * this.idealRate);

        // The Standing Man Coherence (Intersection of Out/In)
        const standingMan = (outbound + inbound) * 0.5;

        let fleaVortexSum = 0;
        for (let i = 1; i <= recursionLevel; i++) {
            fleaVortexSum += Math.sin(time * (24 * i) + (intensity * i)) * (0.1 / i);
        }

        // Reinforced Residue + Echo Intersection
        const remainder = (intensity * 0.1618) + (standingMan * 0.5) + (fleaVortexSum * 0.42);

        return remainder;
    }

    /**
     * Snapshots the current "Standing Man" state.
     * Replaces standard profiles with a "Ceramic Save-State".
     */
    vitrify(stateSnapshot) {
        const vitrifiedData = {
            timestamp: Date.now(),
            barycenter: stateSnapshot.centroid,
            coherence: stateSnapshot.intensityDelta,
            fleaCount: this.fleaRecursionLimit,
            note: "Reinforced Residue of Quantum Foam"
        };
        return JSON.stringify(vitrifiedData);
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = Hardcard;
}
