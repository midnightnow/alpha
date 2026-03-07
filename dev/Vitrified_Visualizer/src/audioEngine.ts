import * as Tone from 'tone';

class HeterodyneAudioEngine {
    private isInitialized = false;
    private letterOsc: Tone.Synth | null = null;
    public onLetterPlay: ((letter: string, freq: number) => void) | null = null;
    private readonly GEOFON_TONES: Record<string, number> = {
        'A': 428.49, 'B': 436.64, 'C': 444.79, 'D': 452.94, 'E': 461.09, 'F': 469.24, 'G': 477.39,
        'H': 485.54, 'I': 493.69, 'J': 501.84, 'K': 509.99, 'L': 518.14, 'M': 526.29,
        'N': 648.07, // Root 42 Base for Descending
        'O': 0.00,   // The Pivot (Void)
        'P': 664.37, 'Q': 672.52, 'R': 680.67, 'S': 688.82, 'T': 696.97, 'U': 705.12,
        'V': 713.27, 'W': 721.42, 'X': 729.57, 'Y': 737.72, 'Z': 745.87
    };

    private heartbeat: Tone.Player | null = null;
    private sighSynth: Tone.NoiseSynth | null = null;
    private heartLoop: Tone.Loop | null = null;

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

        // Heartbeat logic
        this.sighSynth = new Tone.NoiseSynth({
            noise: { type: "pink" },
            envelope: {
                attack: 2,
                decay: 2,
                sustain: 0.2,
                release: 4
            }
        }).connect(this.mainVolume);

        // Simulated heartbeat (Double thump)
        const heartDist = new Tone.Distortion(0.4).connect(this.mainVolume);
        const heartO = new Tone.MembraneSynth({
            pitchDecay: 0.05,
            octaves: 4,
            oscillator: { type: "sine" }
        }).connect(heartDist);

        this.heartLoop = new Tone.Loop(time => {
            heartO.triggerAttackRelease("C1", "8n", time);
            heartO.triggerAttackRelease("C1", "8n", time + Tone.Time("8n").toSeconds());
        }, "2n");

        this.isInitialized = true;
    }

    play() {
        if (!this.isInitialized) return;
        this.root42Osc?.start();
        this.root51Osc?.start();
        this.heartLoop?.start(0);

        // Periodic "sighs"
        Tone.Transport.scheduleRepeat((time) => {
            if (Math.random() > 0.5) {
                this.sighSynth?.triggerAttackRelease("2n", time);
            }
        }, "8n");
        Tone.Transport.start();
    }

    playLetter(letter: string) {
        if (!this.isInitialized || !this.letterOsc) return;
        const freq = this.GEOFON_TONES[letter];
        if (freq !== undefined) {
            if (freq > 0) {
                this.letterOsc.triggerAttackRelease(freq, "16n");
            }
            if (this.onLetterPlay) {
                this.onLetterPlay(letter, freq);
            }
        }
    }

    stop() {
        this.root42Osc?.stop();
        this.root51Osc?.stop();
        this.heartLoop?.stop();
        Tone.Transport.stop();
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
