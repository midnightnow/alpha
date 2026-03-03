export class AudioEngine {
  private ctx: AudioContext | null = null;
  private oscA: OscillatorNode | null = null;
  private oscB: OscillatorNode | null = null;
  private oscC: OscillatorNode | null = null;
  private lfo: OscillatorNode | null = null;
  private lfoGain: GainNode | null = null;
  private masterGain: GainNode | null = null;

  constructor() {}

  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
      this.masterGain = this.ctx.createGain();
      this.masterGain.connect(this.ctx.destination);
    }
  }

  playTriad(freqA: number, freqB: number, freqC: number, masterVolume: number) {
    this.init();
    if (!this.ctx || !this.masterGain) return;

    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }

    // Stop existing sounds before starting new ones
    this.stop();

    const t = this.ctx.currentTime;

    // --- OSCILLATOR SETUP ---
    this.oscA = this.ctx.createOscillator();
    this.oscA.type = 'sine';
    this.oscA.frequency.setValueAtTime(freqA, t);

    this.oscB = this.ctx.createOscillator();
    this.oscB.type = 'sine';
    this.oscB.frequency.setValueAtTime(freqB, t);

    this.oscC = this.ctx.createOscillator();
    this.oscC.type = 'sine';
    this.oscC.frequency.setValueAtTime(freqC, t);

    // --- MIXING (Amplitudes from Seal Spec) ---
    // Layer 1 (Hexagon): 0.5
    const gainA = this.ctx.createGain();
    gainA.gain.value = 0.5;
    
    // Layer 2 (Lattice): 0.4
    const gainB = this.ctx.createGain();
    gainB.gain.value = 0.4;
    
    // Layer 3 (Resolution): 0.25
    const gainC = this.ctx.createGain();
    gainC.gain.value = 0.25;

    this.oscA.connect(gainA);
    this.oscB.connect(gainB);
    this.oscC.connect(gainC);

    // --- SUMMING & MODULATION ---
    const sumNode = this.ctx.createGain();
    sumNode.gain.value = 1.0; // Base gain

    gainA.connect(sumNode);
    gainB.connect(sumNode);
    gainC.connect(sumNode);

    // --- LFO (Breathing Effect) ---
    // Beat Frequency = (FreqB - FreqA) / 100 approx 0.66Hz
    // LFO Model: 1.0 + 0.1 * sin(wt)
    const beatFreq = Math.abs(freqB - freqA) / 100;

    this.lfo = this.ctx.createOscillator();
    this.lfo.frequency.setValueAtTime(beatFreq, t);

    this.lfoGain = this.ctx.createGain();
    this.lfoGain.gain.value = 0.1; // Modulation depth (+/- 0.1)

    // Connect LFO to the Gain AudioParam of the sumNode
    // This adds the LFO output to the base value (1.0) of sumNode.gain
    this.lfo.connect(this.lfoGain);
    this.lfoGain.connect(sumNode.gain);

    // Connect Sum to Master
    sumNode.connect(this.masterGain);

    // --- ENVELOPE ---
    this.masterGain.gain.cancelScheduledValues(t);
    this.masterGain.gain.setValueAtTime(0, t);
    this.masterGain.gain.linearRampToValueAtTime(masterVolume, t + 2.0); // Slow 2s fade in for "Atmosphere"

    // --- START ---
    this.oscA.start(t);
    this.oscB.start(t);
    this.oscC.start(t);
    this.lfo.start(t);
  }

  stop() {
    const t = this.ctx?.currentTime || 0;
    
    // Gentle release
    if (this.masterGain) {
         try {
            this.masterGain.gain.cancelScheduledValues(t);
            this.masterGain.gain.setTargetAtTime(0, t, 0.1);
         } catch(e) {}
    }

    const stopNode = (node: OscillatorNode | null) => {
        if (node) {
            try { node.stop(t + 0.2); } catch(e) {}
            setTimeout(() => { try { node.disconnect(); } catch(e) {} }, 300);
        }
    };
    
    stopNode(this.oscA);
    stopNode(this.oscB);
    stopNode(this.oscC);
    stopNode(this.lfo);
    
    this.oscA = null;
    this.oscB = null;
    this.oscC = null;
    this.lfo = null;
  }

  setVolume(vol: number) {
    if (this.masterGain && this.ctx) {
      this.masterGain.gain.setTargetAtTime(vol, this.ctx.currentTime, 0.1);
    }
  }
}

export const audioEngine = new AudioEngine();