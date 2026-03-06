/**
 * AxiomValidator.js - The "Hardened Sieve"
 * 
 * Universe A: Deterministic Gating.
 * Checks for field convergence using the Biquadratic Law.
 */

class AxiomValidator {
    constructor(mathman) {
        this.mm = mathman;
        this.HADES_GAP = Math.E / 22; // ≈ 0.12355
        this.lastRemainder = Infinity;
        this.history = [];
    }

    /**
     * Samples normalized interference at the midpoint between A and B.
     */
    sampleField() {
        const o = this.mm.getOrigins();
        const k = (2 * Math.PI) / this.mm.params.lambda;

        // Canonical probe = midpoint between A and B
        const mx = (o.a.x + o.b.x) / 2;
        const my = 0;

        // Distance from sample point to sources
        const dA = Math.sqrt((mx - o.a.x) ** 2 + my ** 2);
        const dB = Math.sqrt((mx - o.b.x) ** 2 + my ** 2);

        // Interference amplitude x in range [-1, 1]
        const x = (Math.cos(k * dA) + Math.cos(k * dB)) / 2;

        return x;
    }

    /**
     * Computes the Biquadratic Remainder: R(x) = x⁴ − 186x² + 81
     */
    computeRemainder(x) {
        return Math.pow(x, 4) - 186 * Math.pow(x, 2) + 81;
    }

    /**
     * Derivative for Newton-Raphson: R'(x) = 4x³ − 372x
     */
    computeDerivative(x) {
        return 4 * Math.pow(x, 3) - 372 * x;
    }

    /**
     * Standardized sintering check against the Hades Gap.
     */
    isSintered(remainder) {
        return Math.abs(remainder) <= this.HADES_GAP;
    }

    /**
     * Samples normalized interference at a specific vertical node (altitude).
     */
    sampleFieldAtNode(y) {
        if (this.mm.sampleFieldAtNode) {
            return this.mm.sampleFieldAtNode(y);
        }
        return this.sampleField();
    }

    /**
     * Gating check: Has the field vitrified?
     */
    canAdvance() {
        const x = this.sampleField();
        const r = this.computeRemainder(x);

        this.lastRemainder = r;

        // The field must naturally converge to a root
        const vitrified = this.isSintered(r);

        if (vitrified) {
            console.log(`[Geometric Sieve] VITRIFIED: R(${x.toFixed(4)}) = ${r.toFixed(4)} ≤ Hades Gap`);
        }

        return vitrified;
    }

    getRemainder() {
        return this.lastRemainder;
    }

    logProof(axiomId, label) {
        const x = this.sampleField();
        const r = this.computeRemainder(x);
        this.history.push({
            axiomId,
            label,
            timestamp: Date.now(),
            remainder: r.toFixed(6),
            intensity: x.toFixed(6)
        });
    }

    exportProof() {
        return JSON.stringify({
            "@context": "https://w3id.org/sovereign/axiom/v1",
            "@type": "ConstructionProof",
            "axioms": this.history
        }, null, 2);
    }
}
