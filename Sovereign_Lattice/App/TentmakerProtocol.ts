/**
 * 🏕️ TENTMAKER PROTOCOL — The 0.876553 Vitrification State Machine
 * ============================================================================
 * 
 * This module embodies the transition from the Rigid Lithic Architecture (Saul/Compression/Stone)
 * to the Flexible Tensegrity Model (Paul/Tension/Tent).
 * 
 * The system monitors the phase accumulation and triggers a phase-lock ("Apo-still")
 * when the 0.876553 Diamond Lock threshold is reached.
 */

// We import relevant constants directly from the Master Constants file if present.
// For the sake of zero-dependency isolation, we define the critical values here.

export const DIAMOND_LOCK_THRESHOLD = 0.876553;
export const ALPHA_51213_TENSION = [5, 12, 13];

export enum SystemState {
    SAUL_PADDOCK = "SAUL_PADDOCK", // The 42.0° Stone Pyramid - Compression, Overcoiled DNA, 12-13 Beat Oscillation
    PAUL_TENT = "PAUL_TENT"        // The 51.8° Flexible Tent - Tension, 12-strand Stack, Alpha 5-12-13 Phase-Lock
}

export interface TransitionLog {
    timestamp: number;
    phase: number;
    previousState: SystemState;
    newState: SystemState;
    message: string;
}

export class TentmakerProtocol {
    private currentState: SystemState;
    private currentPhase: number;
    private auditLog: TransitionLog[];

    constructor(initialPhase: number = 0) {
        this.currentState = SystemState.SAUL_PADDOCK;
        this.currentPhase = initialPhase;
        this.auditLog = [];
    }

    /**
     * Updates the tension of the membrane by advancing the phase.
     * @param phase - The current 0-1 phase state of the engine.
     * @returns True if a phase transition occurred, false otherwise.
     */
    public updatePhase(phase: number): boolean {
        this.currentPhase = phase;

        // Calculate the "Diamond Potential" as scaled by the engine logic
        // Following Phase-Lock logic: potential = 0.1000 + (phase * 0.776553)
        const diamondPotential = 0.1000 + (this.currentPhase * 0.776553);
        const isThresholdReached = diamondPotential >= DIAMOND_LOCK_THRESHOLD;

        if (this.currentState === SystemState.SAUL_PADDOCK && isThresholdReached) {
            this.transitionToApostolic();
            return true;
        } else if (this.currentState === SystemState.PAUL_TENT && !isThresholdReached) {
            // Reverting back is structurally unsound, but the math supports fluctuation
            this.transitionToLithic();
            return true;
        }

        return false;
    }

    private transitionToApostolic(): void {
        this.audit(
            SystemState.SAUL_PADDOCK,
            SystemState.PAUL_TENT,
            "APO-STILL ENGAGED: 12-13 Beat normalized. Alpha 5-12-13 tension achieved. System collapsed from Overcoiled to Icosidodecahedral Stack."
        );
        this.currentState = SystemState.PAUL_TENT;
    }

    private transitionToLithic(): void {
        this.audit(
            SystemState.PAUL_TENT,
            SystemState.SAUL_PADDOCK,
            "TENSION LOSS: The Pall sagging. Reverting to compression-based lithic structure. 12-13 Beat hunting oscillation resumed."
        );
        this.currentState = SystemState.SAUL_PADDOCK;
    }

    private audit(prev: SystemState, next: SystemState, msg: string): void {
        const logEntry: TransitionLog = {
            timestamp: Date.now(),
            phase: this.currentPhase,
            previousState: prev,
            newState: next,
            message: msg
        };
        this.auditLog.push(logEntry);

        // Dispatching custom DOM event to broadcast state changes universally
        if (typeof window !== "undefined") {
            window.dispatchEvent(new CustomEvent('tentmaker:transition', { detail: logEntry }));
        }
    }

    public getState(): SystemState {
        return this.currentState;
    }

    public getStatusReport(): string {
        if (this.currentState === SystemState.PAUL_TENT) {
            return `PORTABLE MERKABA DEPLOYED. Tension: ${DIAMOND_LOCK_THRESHOLD}. Status: APO-STILL (Phase-Locked).`;
        }
        return `STONE PADDOCK COMPRESSING. Phase: ${this.currentPhase.toFixed(6)}. Status: HUNTING (12-13 Beat).`;
    }

    public getAuditLog(): TransitionLog[] {
        return [...this.auditLog];
    }
}
