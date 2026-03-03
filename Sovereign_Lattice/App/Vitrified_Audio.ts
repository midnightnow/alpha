/**
 * 🏛️ SOVEREIGN LATTICE — VITRIFIED AUDIO ENGINE
 * ================================================
 * Generates the 6 Hz Hades Beat by playing 66 Hz (Root 42) and 60 Hz (Root 51)
 * triadic chords in a stereo heterodyne (L/R) configuration.
 *
 * The "Whisper" is louder than the "Scream":
 *   Left channel  → 66 Hz (Matter / √42)
 *   Right channel → 60 Hz (Time / √51)
 *   Phantom beat  → 6 Hz (The Hades Gap)
 *
 * Attack/Decay follows LOG-SCALE SYMMETRY:
 *   log(A) = log(√42) − λ|t|
 *   The apparent asymmetry is a coordinate illusion.
 *
 * Consolidated from: radical-resonance_-root-42/utils/audioEngine.ts
 * Status: VITRIFIED
 */

import {
    ROOT_42,
    ROOT_51,
    FREQ_MATTER,
    FREQ_TIME,
    HADES_BEAT_HZ,
    BEAT_FREQUENCY,
    TRIAD_AMPLITUDES,
    DECAY_LAMBDA,
    HADES_GAP,
} from './Constants';

// ============================================================================
// AUDIO ENGINE — The Sensory Seal
// ============================================================================

export class VitrifiedAudioEngine {
    private ctx: AudioContext | null = null;
    private masterGain: GainNode | null = null;

    // Triadic oscillators
    private oscMatter: OscillatorNode | null = null;   // 66 Hz (Left)
    private oscTime: OscillatorNode | null = null;      // 60 Hz (Right)
    private oscResolution: OscillatorNode | null = null; // 3rd harmonic

    // LFO for the breathing envelope
    private lfo: OscillatorNode | null = null;
    private lfoGain: GainNode | null = null;

    // Stereo panner nodes for heterodyne separation
    private panLeft: StereoPannerNode | null = null;
    private panRight: StereoPannerNode | null = null;

    // Voice (Naming Ceremony)
    private voiceOsc: OscillatorNode | null = null;
    private voiceGain: GainNode | null = null;

    // State
    private isPlaying = false;

    constructor() { }

    // --------------------------------------------------------------------------
    // INITIALIZATION
    // --------------------------------------------------------------------------

    private init(): void {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
            this.masterGain = this.ctx.createGain();
            this.masterGain.connect(this.ctx.destination);
        }
    }

    // --------------------------------------------------------------------------
    // HADES BEAT — The 6 Hz Heterodyne
    // --------------------------------------------------------------------------

    /**
     * Play the Hades Beat: 66 Hz (L) + 60 Hz (R) producing a 6 Hz phantom.
     * The third harmonic is calculated from the Resonance Ladder progression.
     *
     * @param masterVolume - Overall volume (0.0 to 1.0)
     */
    playHadesBeat(masterVolume: number = 0.15): void {
        this.init();
        if (!this.ctx || !this.masterGain) return;

        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }

        // Stop any existing playback
        this.stop();

        const t = this.ctx.currentTime;

        // --- STEREO PANNERS for heterodyne separation ---
        this.panLeft = this.ctx.createStereoPanner();
        this.panLeft.pan.value = -1.0; // Full left
        this.panRight = this.ctx.createStereoPanner();
        this.panRight.pan.value = 1.0; // Full right

        // --- OSCILLATOR 1: MATTER (66 Hz → Left) ---
        this.oscMatter = this.ctx.createOscillator();
        this.oscMatter.type = 'sine';
        this.oscMatter.frequency.setValueAtTime(FREQ_MATTER, t);

        const gainMatter = this.ctx.createGain();
        gainMatter.gain.value = TRIAD_AMPLITUDES.hexagon; // 0.5

        this.oscMatter.connect(gainMatter);
        gainMatter.connect(this.panLeft);

        // --- OSCILLATOR 2: TIME (60 Hz → Right) ---
        this.oscTime = this.ctx.createOscillator();
        this.oscTime.type = 'sine';
        this.oscTime.frequency.setValueAtTime(FREQ_TIME, t);

        const gainTime = this.ctx.createGain();
        gainTime.gain.value = TRIAD_AMPLITUDES.lattice; // 0.4

        this.oscTime.connect(gainTime);
        gainTime.connect(this.panRight);

        // --- OSCILLATOR 3: RESOLUTION (3rd harmonic, centered) ---
        // Derived from the Ladder: √(51² + 9) × scaling
        const thirdFreq = Math.sqrt(ROOT_51 * ROOT_51 + 9) * 10;
        this.oscResolution = this.ctx.createOscillator();
        this.oscResolution.type = 'sine';
        this.oscResolution.frequency.setValueAtTime(thirdFreq, t);

        const gainResolution = this.ctx.createGain();
        gainResolution.gain.value = TRIAD_AMPLITUDES.resolution; // 0.25

        this.oscResolution.connect(gainResolution);

        // --- SUMMING NODE ---
        const sumNode = this.ctx.createGain();
        sumNode.gain.value = 1.0;

        this.panLeft.connect(sumNode);
        this.panRight.connect(sumNode);
        gainResolution.connect(sumNode);

        // --- LFO: Breathing Effect (Beat Frequency ≈ 0.66 Hz) ---
        this.lfo = this.ctx.createOscillator();
        this.lfo.frequency.setValueAtTime(BEAT_FREQUENCY, t);

        this.lfoGain = this.ctx.createGain();
        this.lfoGain.gain.value = 0.1; // Modulation depth ±0.1

        this.lfo.connect(this.lfoGain);
        this.lfoGain.connect(sumNode.gain);

        // --- CONNECT TO MASTER ---
        sumNode.connect(this.masterGain);

        // --- ENVELOPE: Log-Symmetric Attack ---
        // Attack follows exponential curve (symmetric with decay in log space)
        this.masterGain.gain.cancelScheduledValues(t);
        this.masterGain.gain.setValueAtTime(0.0001, t);
        // Exponential ramp for log-symmetric attack (2 seconds)
        this.masterGain.gain.exponentialRampToValueAtTime(masterVolume, t + 2.0);

        // --- START ALL ---
        this.oscMatter.start(t);
        this.oscTime.start(t);
        this.oscResolution.start(t);
        this.lfo.start(t);

        this.isPlaying = true;
    }

    /**
     * Play a custom triadic chord (backward-compatible with original audioEngine).
     */
    playTriad(freqA: number, freqB: number, freqC: number, masterVolume: number): void {
        this.init();
        if (!this.ctx || !this.masterGain) return;

        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }

        this.stop();

        const t = this.ctx.currentTime;

        this.oscMatter = this.ctx.createOscillator();
        this.oscMatter.type = 'sine';
        this.oscMatter.frequency.setValueAtTime(freqA, t);

        this.oscTime = this.ctx.createOscillator();
        this.oscTime.type = 'sine';
        this.oscTime.frequency.setValueAtTime(freqB, t);

        this.oscResolution = this.ctx.createOscillator();
        this.oscResolution.type = 'sine';
        this.oscResolution.frequency.setValueAtTime(freqC, t);

        const gainA = this.ctx.createGain();
        gainA.gain.value = TRIAD_AMPLITUDES.hexagon;
        const gainB = this.ctx.createGain();
        gainB.gain.value = TRIAD_AMPLITUDES.lattice;
        const gainC = this.ctx.createGain();
        gainC.gain.value = TRIAD_AMPLITUDES.resolution;

        this.oscMatter.connect(gainA);
        this.oscTime.connect(gainB);
        this.oscResolution.connect(gainC);

        const sumNode = this.ctx.createGain();
        sumNode.gain.value = 1.0;
        gainA.connect(sumNode);
        gainB.connect(sumNode);
        gainC.connect(sumNode);

        // LFO breathing
        const beatFreq = Math.abs(freqB - freqA) / 100;
        this.lfo = this.ctx.createOscillator();
        this.lfo.frequency.setValueAtTime(beatFreq, t);
        this.lfoGain = this.ctx.createGain();
        this.lfoGain.gain.value = 0.1;
        this.lfo.connect(this.lfoGain);
        this.lfoGain.connect(sumNode.gain);

        sumNode.connect(this.masterGain);

        this.masterGain.gain.cancelScheduledValues(t);
        this.masterGain.gain.setValueAtTime(0, t);
        this.masterGain.gain.linearRampToValueAtTime(masterVolume, t + 2.0);

        this.oscMatter.start(t);
        this.oscTime.start(t);
        this.oscResolution.start(t);
        this.lfo.start(t);

        this.isPlaying = true;
    }

    // --------------------------------------------------------------------------
    // VOICE — The Naming Ceremony
    // --------------------------------------------------------------------------

    /**
     * "Sing" an H3 index address. Each hex address produces a unique frequency.
     * Hades indices use sawtooth (gritty); normal indices use triangle (smooth).
     */
    singName(h3Index: string, isHades: boolean): void {
        if (!this.ctx || !this.masterGain) return;
        const t = this.ctx.currentTime;

        // Stop previous voice
        if (this.voiceOsc) {
            try { this.voiceOsc.stop(t); } catch (_) { }
        }

        // Derive frequency from hex character density
        const bits = h3Index.split('').reduce((acc, ch) => acc + parseInt(ch, 16), 0);
        const baseFreq = isHades ? 33 : 132;
        const singFreq = baseFreq + (bits * 2);

        this.voiceOsc = this.ctx.createOscillator();
        this.voiceOsc.type = isHades ? 'sawtooth' : 'triangle';
        this.voiceOsc.frequency.setValueAtTime(singFreq, t);

        this.voiceGain = this.ctx.createGain();
        this.voiceGain.gain.setValueAtTime(0, t);
        this.voiceGain.gain.exponentialRampToValueAtTime(0.2, t + 0.05);
        this.voiceGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.4);

        this.voiceOsc.connect(this.voiceGain);
        this.voiceGain.connect(this.masterGain);

        this.voiceOsc.start(t);
        this.voiceOsc.stop(t + 0.5);
    }

    // --------------------------------------------------------------------------
    // RESONANCE MEASUREMENT
    // --------------------------------------------------------------------------

    /**
     * Returns current resonance level (0.0 to 1.0).
     * Used by the Stress Anchor system to detect when fracture events occur.
     */
    getResonance(): number {
        if (!this.ctx || !this.masterGain || !this.isPlaying) return 0;
        // Approximate resonance from the master gain value
        return Math.min(1.0, this.masterGain.gain.value / 0.15);
    }

    // --------------------------------------------------------------------------
    // STOP & CLEANUP
    // --------------------------------------------------------------------------

    stop(): void {
        const t = this.ctx?.currentTime || 0;

        // Log-symmetric decay (exponential release)
        if (this.masterGain) {
            try {
                this.masterGain.gain.cancelScheduledValues(t);
                this.masterGain.gain.setTargetAtTime(0, t, 0.1);
            } catch (_) { }
        }

        const stopNode = (node: OscillatorNode | null) => {
            if (node) {
                try { node.stop(t + 0.2); } catch (_) { }
                setTimeout(() => { try { node.disconnect(); } catch (_) { } }, 300);
            }
        };

        stopNode(this.oscMatter);
        stopNode(this.oscTime);
        stopNode(this.oscResolution);
        stopNode(this.lfo);
        stopNode(this.voiceOsc);

        this.oscMatter = null;
        this.oscTime = null;
        this.oscResolution = null;
        this.lfo = null;
        this.voiceOsc = null;
        this.isPlaying = false;
    }

    // --------------------------------------------------------------------------
    // VOLUME CONTROL
    // --------------------------------------------------------------------------

    setVolume(vol: number): void {
        if (this.masterGain && this.ctx) {
            this.masterGain.gain.setTargetAtTime(vol, this.ctx.currentTime, 0.1);
        }
    }

    /** Check if audio is currently playing */
    getIsPlaying(): boolean {
        return this.isPlaying;
    }
}

// ============================================================================
// SINGLETON EXPORT — The Vitrified Audio
// ============================================================================

export const audioEngine = new VitrifiedAudioEngine();
