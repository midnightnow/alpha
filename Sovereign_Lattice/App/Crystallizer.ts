/**
 * 💎 CRYSTALLIZER — The Language of Angles
 * ============================================================================
 * 
 * Activated only when the TentmakerProtocol achieves "Apo-Still" (Phase-Lock).
 * When the outer rotation ceases, the internal symmetries are unlocked.
 * 
 * This module translates the static geometric angles of the Sovereign Lattice
 * into audible frequencies ("The Language of Angles").
 */

export interface AngularSymmetry {
    name: string;
    angleDegrees: number;
    frequencyHz: number;
    meaning: string;
}

export class Crystallizer {
    private isCrystallized: boolean = false;
    private symmetries: AngularSymmetry[] = [];

    // The base resonant frequency of the vacuum (White Point)
    private readonly BASE_FREQ = 432.0;

    constructor() {
        this.initializeSymmetries();
    }

    private initializeSymmetries(): void {
        this.symmetries = [
            {
                name: "The Paddock (Saul)",
                angleDegrees: 42.0,
                frequencyHz: this.calculateFrequency(42.0),
                meaning: "Mothering Limit / Raindrop Tension"
            },
            {
                name: "The Pyramid (Paul)",
                angleDegrees: 51.84, // Exact angle of Giza
                frequencyHz: this.calculateFrequency(51.84),
                meaning: "Fathering Reach / 12-Strand Uncoil"
            },
            {
                name: "The Shear (Heartbeat)",
                angleDegrees: 39.47, // arctan(14/17)
                frequencyHz: this.calculateFrequency(39.47),
                meaning: "Tensegrity / The Stone in the Shoe"
            },
            {
                name: "The Golden Heart",
                angleDegrees: 137.5,
                frequencyHz: this.calculateFrequency(137.5),
                meaning: "Fibonacci Spacing / Node #47"
            }
        ];
    }

    /**
     * Translates a geometric angle into an acoustic frequency.
     * Uses the 5-12-13 ratio to step the base frequency.
     */
    private calculateFrequency(angle: number): number {
        // The frequency is the Base multiplied by the angle's ratio to 360,
        // scaled by the Alpha 13 hypotenuse for tension.
        return this.BASE_FREQ * (angle / 360.0) * 13;
    }

    /**
     * Triggered by the TentmakerProtocol when 0.876553 is reached.
     */
    public triggerCrystallization(): void {
        this.isCrystallized = true;
        this.broadcastLanguage();
    }

    /**
     * When crystallized, the geometry stops moving and starts 'speaking'.
     */
    private broadcastLanguage(): void {
        if (!this.isCrystallized) return;

        console.log("💎 CRYSTALLIZATION ACHIEVED. THE ANGLES SPEAK:");
        this.symmetries.forEach(sym => {
            console.log(`› ${sym.name}: ${sym.angleDegrees}° -> ${sym.frequencyHz.toFixed(2)} Hz`);
        });

        // In a live environment, this dispatches to the Web Audio API
        if (typeof window !== "undefined") {
            window.dispatchEvent(new CustomEvent('crystallizer:speak', {
                detail: { symmetries: this.symmetries }
            }));
        }
    }

    public getStatus(): boolean {
        return this.isCrystallized;
    }
}
