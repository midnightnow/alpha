import * as Tone from 'tone';

class HeterodyneAudioEngine {
    private isInitialized = false;
    private root42Osc: Tone.Oscillator | null = null;
    private root51Osc: Tone.Oscillator | null = null;
    private beatPanner42: Tone.Panner | null = null;
    private beatPanner51: Tone.Panner | null = null;
    private mainVolume: Tone.Volume | null = null;

    async init() {
        if (this.isInitialized) return;
        await Tone.start();

        // Stereophonic Beat: 66 Hz in one ear, 60 Hz in the other, producing 6 Hz Heterodyne Beat
        // Note: We use the 42 and 51 frequencies respectively for the full effect, but the prompt mentioned 66 and 60.
        // Let's use 66Hz for 42 side, and 60Hz for 51 side to create the 6Hz difference.

        this.mainVolume = new Tone.Volume(-12).toDestination();

        // Left Ear (Root 42 / Hexagonal - 66Hz)
        this.beatPanner42 = new Tone.Panner(-1).connect(this.mainVolume);
        this.root42Osc = new Tone.Oscillator(66, "sine").connect(this.beatPanner42);

        // Right Ear (Root 51 / Fracture - 60Hz)
        this.beatPanner51 = new Tone.Panner(1).connect(this.mainVolume);
        this.root51Osc = new Tone.Oscillator(60, "sine").connect(this.beatPanner51);

        this.isInitialized = true;
    }

    play() {
        if (!this.isInitialized) return;
        this.root42Osc?.start();
        this.root51Osc?.start();
    }

    stop() {
        this.root42Osc?.stop();
        this.root51Osc?.stop();
    }

    // Phase is a value between 0 (Root 42 ) and 1 (Root 51)
    updatePhase(phase: number) {
        if (!this.isInitialized) return;

        // As we move towards 51, the 60Hz signal gets stronger and 66Hz gets slightly weaker
        if (this.root42Osc) {
            this.root42Osc.volume.rampTo(Tone.gainToDb(1 - phase * 0.5), 0.1);
        }
        if (this.root51Osc) {
            this.root51Osc.volume.rampTo(Tone.gainToDb(0.5 + phase * 0.5), 0.1);
        }

        // Add harmonic distortion/grit as phase approaches 1 (fracture)
        // We could add a bitcrusher or distortion effect here for the "ceramic" teeth sound
    }
}

export const audioEngine = new HeterodyneAudioEngine();
