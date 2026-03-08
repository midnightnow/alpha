/**
 * 🎨 PUPIL MODE — The Transition from Soft to Hardened
 * ============================================================================
 * 
 * Manages the aesthetic and behavioral shift as the Pupil (The Ideal Platonic MAN)
 * refines their "Set Triangles" and "Set Squares" from graphite sketches
 * into vitrified Sovereign constants.
 */

import { INFLATION_SETS, PUPIL_COLORS } from './Constants';

export enum TechnicalState {
    GRAPHITE = 'GRAPHITE', // Soft tools, 12-measure constraints
    HARDENING = 'HARDENING', // The transition phase
    SOVEREIGN = 'SOVEREIGN', // Emerald glow, zero jitter
}

export interface PupilModeState {
    technical: TechnicalState;
    hardening: number; // 0.0 to 1.0
    activeSet: keyof typeof INFLATION_SETS;
}

export class PupilModeManager {
    private state: PupilModeState;

    constructor(initialSet: keyof typeof INFLATION_SETS = 'TRIANGLE') {
        this.state = {
            technical: TechnicalState.GRAPHITE,
            hardening: 0,
            activeSet: initialSet,
        };
    }

    /**
     * Updates the hardening factor and determines the technical state.
     */
    public setHardening(value: number): void {
        this.state.hardening = Math.max(0, Math.min(1, value));

        if (this.state.hardening < 0.2) {
            this.state.technical = TechnicalState.GRAPHITE;
        } else if (this.state.hardening > 0.8) {
            this.state.technical = TechnicalState.SOVEREIGN;
        } else {
            this.state.technical = TechnicalState.HARDENING;
        }
    }

    /**
     * Returns the color associated with the current hardening state.
     */
    public getRenderColor(): string {
        if (this.state.technical === TechnicalState.GRAPHITE) {
            return PUPIL_COLORS.GRAPHENE;
        } else if (this.state.technical === TechnicalState.SOVEREIGN) {
            return PUPIL_COLORS.EMERALD;
        }

        // Linear interpolation for HARDENING state (Graphene -> Emerald)
        return this.lerpColor(PUPIL_COLORS.GRAPHENE, PUPIL_COLORS.EMERALD, this.state.hardening);
    }

    /**
     * Returns the line dash property for "Soft" tools.
     */
    public getLineStyle(): number[] {
        if (this.state.technical === TechnicalState.GRAPHITE) {
            return [5, 5]; // Dotted line like a sketch
        }
        return []; // Solid line for hardened geometry
    }

    private lerpColor(c1: string, c2: string, t: number): string {
        const r1 = parseInt(c1.substring(1, 3), 16);
        const g1 = parseInt(c1.substring(3, 5), 16);
        const b1 = parseInt(c1.substring(5, 7), 16);

        const r2 = parseInt(c2.substring(1, 3), 16);
        const g2 = parseInt(c2.substring(3, 5), 16);
        const b2 = parseInt(c2.substring(5, 7), 16);

        const r = Math.round(r1 + (r2 - r1) * t).toString(16).padStart(2, '0');
        const g = Math.round(g1 + (g2 - g1) * t).toString(16).padStart(2, '0');
        const b = Math.round(b1 + (b2 - b1) * t).toString(16).padStart(2, '0');

        return `#${r}${g}${b}`;
    }

    public getState(): PupilModeState {
        return { ...this.state };
    }
}
