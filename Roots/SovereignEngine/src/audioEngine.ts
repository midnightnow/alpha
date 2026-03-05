import * as Tone from 'tone';

class HeterodyneAudioEngine {
    private isInitialized = false;
    private letterOsc: Tone.Synth | null = null;
    private readonly GEOFON_TONES: Record<string, number> = {
        'A': 428.49, 'B': 436.64, 'C': 444.79, 'D': 452.94, 'E': 461.09, 'F': 469.24, 'G': 477.39,
        'H': 485.54, 'I': 493.69, 'J': 501.84, 'K': 509.99, 'L': 518.14, 'M': 526.29,
        'N': 648.07, // Root 42 Base for Descending
        'O': 0.00,   // The Pivot (Void)
        'P': 664.37, 'Q': 672.52, 'R': 680.67, 'S': 688.82, 'T': 696.97, 'U': 705.12,
        'V': 713.27, 'W': 721.42, 'X': 729.57, 'Y': 737.72, 'Z': 745.87
    };

    async init() {
        if (this.isInitialized) return;
        await Tone.start();

        this.mainVolume = new Tone.Volume(-12).toDestination();

        // Left Ear (Root 42 / Hexagonal - 66Hz)
        this.beatPanner42 = new Tone.Panner(-1).connect(this.mainVolume);
        this.root42Osc = new Tone.Oscillator(66, "sine").connect(this.beatPanner42);

        // Right Ear (Root 51 / Fracture - 60Hz)
        this.beatPanner51 = new Tone.Panner(1).connect(this.mainVolume);
        this.root51Osc = new Tone.Oscillator(60, "sine").connect(this.beatPanner51);

        // Geofont Letter Synth
        this.letterOsc = new Tone.Synth({
            oscillator: { type: "square" }, // Aggressive "Acoustic Hum" texture
            envelope: {
                attack: 0.01,
                decay: 0.1,
                sustain: 0.3,
                release: 1
            }
        }).connect(this.mainVolume);

        this.isInitialized = true;
    }

    play() {
        if (!this.isInitialized) return;
        this.root42Osc?.start();
        this.root51Osc?.start();
    }

    playLetter(letter: string) {
        if (!this.isInitialized || !this.letterOsc) return;
        const freq = this.GEOFON_TONES[letter];
        if (freq && freq > 0) {
            this.letterOsc.triggerAttackRelease(freq, "16n");
        }
    }

    stop() {
        this.root42Osc?.stop();
        this.root51Osc?.stop();
    }

    updatePhase(phase: number) {
        if (!this.isInitialized) return;

        if (this.root42Osc) {
            this.root42Osc.volume.rampTo(Tone.gainToDb(1 - phase * 0.5), 0.1);
        }
        if (this.root51Osc) {
            this.root51Osc.volume.rampTo(Tone.gainToDb(0.5 + phase * 0.5), 0.1);
        }
    }
}

export const audioEngine = new HeterodyneAudioEngine();
