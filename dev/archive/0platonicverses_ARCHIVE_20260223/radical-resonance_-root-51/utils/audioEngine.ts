export class AudioEngine {
  private ctx: AudioContext | null = null;
  private oscA: OscillatorNode | null = null;
  private oscB: OscillatorNode | null = null;
  private oscC: OscillatorNode | null = null;
  private lfo: OscillatorNode | null = null;
  private lfoGain: GainNode | null = null;
  private masterGain: GainNode | null = null;
  private voiceOsc: OscillatorNode | null = null;
  private voiceGain: GainNode | null = null;
  private analyser: AnalyserNode | null = null;
  private freqData: Uint8Array = new Uint8Array(0);

  constructor() { }

  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
      this.masterGain = this.ctx.createGain();

      this.analyser = this.ctx.createAnalyser();
      this.analyser.fftSize = 256;
      this.freqData = new Uint8Array(this.analyser.frequencyBinCount);

      this.masterGain.connect(this.analyser);
      this.analyser.connect(this.ctx.destination);
    }
  }

  getResonance(): number {
    if (!this.analyser) return 0;
    this.analyser.getByteFrequencyData(this.freqData);
    // Return average of low bands for "The Hum"
    let sum = 0;
    const bands = 8;
    for (let i = 0; i < bands; i++) {
      sum += this.freqData[i];
    }
    return sum / (bands * 255);
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
      } catch (e) { }
    }

    const stopNode = (node: OscillatorNode | null) => {
      if (node) {
        try { node.stop(t + 0.2); } catch (e) { }
        setTimeout(() => { try { node.disconnect(); } catch (e) { } }, 300);
      }
    };

    stopNode(this.oscA);
    stopNode(this.oscB);
    stopNode(this.oscC);
    stopNode(this.lfo);
    stopNode(this.voiceOsc);

    this.oscA = null;
    this.oscB = null;
    this.oscC = null;
    this.lfo = null;
    this.voiceOsc = null;
  }

  singName(h3_index: string, isHades: boolean) {
    if (!this.ctx || !this.masterGain) return;
    const t = this.ctx.currentTime;

    // Stop previous voice pulse
    if (this.voiceOsc) {
      try { this.voiceOsc.stop(t); } catch (e) { }
    }

    // Calculate bit-density for frequency modulation
    // We use the hex characters to derive a unique "Singing" frequency
    const bits = h3_index.split('').reduce((acc, char) => acc + parseInt(char, 16), 0);
    const baseFreq = isHades ? 33 : 132; // Lower for Hades Gap
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

  setVolume(vol: number) {
    if (this.masterGain && this.ctx) {
      this.masterGain.gain.setTargetAtTime(vol, this.ctx.currentTime, 0.1);
    }
  }
}

export const audioEngine = new AudioEngine();