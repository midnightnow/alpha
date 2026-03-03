import * as Tone from 'tone';

export class ToneEngine {
  private isInitialized = false;
  private isPlaying = false;

  // --- LAYERS ---
  private bass: Tone.MembraneSynth | null = null;
  private pad: Tone.PolySynth | null = null;
  private glitch: Tone.MetalSynth | null = null;
  private noise: Tone.NoiseSynth | null = null;

  // --- EFFECTS ---
  private reverb: Tone.Reverb | null = null;
  private delay: Tone.FeedbackDelay | null = null;
  private limiter: Tone.Limiter | null = null;
  private distortion: Tone.Distortion | null = null;
  private bitcrusher: Tone.BitCrusher | null = null;
  private filter: Tone.Filter | null = null;

  // --- LOOPS ---
  private loopPad: Tone.Loop | null = null;
  private loopGlitch: Tone.Loop | null = null;
  private loopBass: Tone.Loop | null = null;
  private crystal: Tone.FMSynth | null = null;
  private currentStep: number = 1;

  // --- ANALYSIS ---
  public analyzer: Tone.Analyser | null = null;

  constructor() { }

  async init() {
    if (this.isInitialized) return;

    await Tone.start();

    // Master Chain
    this.limiter = new Tone.Limiter(-1).toDestination();
    this.reverb = new Tone.Reverb({ decay: 4, wet: 0.3 }).connect(this.limiter);
    this.delay = new Tone.FeedbackDelay("8n", 0.2).connect(this.reverb);
    this.bitcrusher = new Tone.BitCrusher(4).connect(this.delay); // 4-bit crush
    this.bitcrusher.wet.value = 0; // Start clean
    this.distortion = new Tone.Distortion(0).connect(this.bitcrusher); // Start clean
    this.filter = new Tone.Filter(200, "lowpass").connect(this.distortion); // Start closed (200Hz)

    // Analyzer for Visuals
    this.analyzer = new Tone.Analyser("fft", 256);
    this.limiter.connect(this.analyzer);

    // Layer 1: Root 42 Bass (The Hex Engine)
    // Deep sine/triangle foundation
    this.bass = new Tone.MembraneSynth({
      pitchDecay: 0.05,
      octaves: 4,
      oscillator: { type: "sine" },
      envelope: { attack: 0.001, decay: 0.4, sustain: 0.01, release: 1.4 }
    }).connect(this.filter);

    // Layer 2: Root 51 Pad (The Lattice)
    // Glassy FM texture
    this.pad = new Tone.PolySynth(Tone.FMSynth, {
      harmonicity: Math.sqrt(51) / Math.sqrt(42), // The 1.1019 ratio
      modulationIndex: 10,
      oscillator: { type: "sine" },
      envelope: { attack: 0.5, decay: 0.2, sustain: 0.5, release: 1 },
      modulation: { type: "square" },
      modulationEnvelope: { attack: 0.5, decay: 0.01, sustain: 1, release: 0.5 }
    }).connect(this.reverb); // Pad bypasses heavy distortion chain for clarity, goes straight to reverb

    // Layer 3: Root 60 Glitch (The 9-Gap)
    // Metallic, cold, high frequency
    this.glitch = new Tone.MetalSynth({
      frequency: 200,
      envelope: { attack: 0.001, decay: 0.1, release: 0.01 },
      harmonicity: 5.1,
      modulationIndex: 32,
      resonance: 4000,
      octaves: 1.5
    }).connect(this.filter); // Glitch goes through the filter/distortion chain

    // Layer 4: Noise (Texture)
    this.noise = new Tone.NoiseSynth({
      noise: { type: 'pink' },
      envelope: { attack: 0.005, decay: 0.1, sustain: 0 }
    }).connect(this.filter);

    // Layer 5: Crystal (The Resolution) - Phase III Activation
    this.crystal = new Tone.FMSynth({
      harmonicity: 3.0,
      modulationIndex: 10,
      oscillator: { type: "sine" },
      envelope: { attack: 0.01, decay: 0.3, sustain: 0.1, release: 1 },
      modulation: { type: "square" },
      modulationEnvelope: { attack: 0.5, decay: 0.1, sustain: 1, release: 0.5 }
    }).connect(this.reverb!);
    this.crystal.volume.value = -Infinity; // Start muted

    this.setupLoops();
    this.isInitialized = true;
  }

  private setupLoops() {
    // Kick Loop: 4/4 Anchor
    this.loopBass = new Tone.Loop((time) => {
      this.bass?.triggerAttackRelease("C1", "8n", time);
    }, "4n");

    // Pad Loop: Evolving chords based on the Triad
    const chords = [
      ["C3", "E3", "G3"], // Root
      ["C3", "F3", "A3"], // 4th
      ["B2", "D3", "G3"], // 5th
      ["C3", "Eb3", "G3"] // Minor (Tension)
    ];

    this.loopPad = new Tone.Loop((time) => {
      const chord = chords[Math.floor(Math.random() * chords.length)];
      this.pad?.triggerAttackRelease(chord, "2n", time);
    }, "1m");

    // Glitch Loop: 14/17 Euclidean Rhythm
    // 14 events distributed across 17 steps
    const euclidean14_17 = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1];
    let step = 0;

    this.loopGlitch = new Tone.Loop((time) => {
      // For Step 2+ (Resolution), pattern becomes more stable/regular
      const pattern = this.currentStep >= 2
        ? [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0] // 8/16 Stable
        : [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1]; // 14/17 Euclidean

      const mod = this.currentStep >= 2 ? 16 : 17;

      if (pattern[step % mod] === 1) {
        // Pitch is modulated by the 39.4° Shear Angle (tan(39.4) approx 0.82)
        const pitchOffset = Math.tan(39.4 * (Math.PI / 180)) * 100; // ~82Hz

        // Trigger glitch
        this.glitch?.triggerAttackRelease("32n", time, 0.7 + Math.random() * 0.3);

        // Trigger Crystal if in Resolution mode (Step 2+)
        if (this.currentStep >= 2 && Math.random() > 0.5) {
          this.crystal?.triggerAttackRelease("C5", "32n", time, 0.4);
        }

        // Occasionally trigger noise for texture
        if (Math.random() > 0.8) {
          this.noise?.triggerAttackRelease("32n", time);
        }
      }
      step++;
    }, "16n");
  }

  async start() {
    if (!this.isInitialized) return;

    await Tone.start();

    // Reset Transport
    Tone.Transport.stop();
    Tone.Transport.position = 0;

    // Cancel previous scheduling to avoid "Start time must be strictly greater" error
    this.loopBass?.cancel(0);
    this.loopPad?.cancel(0);
    this.loopGlitch?.cancel(0);

    // Schedule loops
    this.loopBass?.start(0);
    this.loopPad?.start(0);
    this.loopGlitch?.start(0);

    Tone.Transport.start();
    this.isPlaying = true;
  }

  stop() {
    Tone.Transport.stop();
    this.loopBass?.stop();
    this.loopPad?.stop();
    this.loopGlitch?.stop();
    this.isPlaying = false;
  }

  // --- DYNAMIC CONTROL ---

  setMasterVolume(volume: number): void {
    Tone.Destination.volume.rampTo(volume === 0 ? -Infinity : 20 * Math.log10(volume), 0.1);
  }

  setMuted(muted: boolean): void {
    Tone.Destination.mute = muted;
  }

  setPlaybackSpeed(speed: number): void {
    if (Tone.Transport.state === 'started') {
      Tone.Transport.bpm.rampTo(120 * speed, 0.5);
    } else {
      Tone.Transport.bpm.value = 120 * speed;
    }
  }

  setStep(step: number) {
    this.currentStep = step;

    // Adjust synth parameters based on Step
    if (step >= 2) {
      // Crystalline Stabilization
      this.crystal?.volume.rampTo(-10, 2);
      if (this.pad) this.pad.harmonicity.rampTo(Math.sqrt(60) / Math.sqrt(42), 2);
      if (this.reverb) this.reverb.wet.rampTo(0.5, 2); // More "Space" for Resolution
    } else {
      // Interference Turbulence
      this.crystal?.volume.rampTo(-Infinity, 1);
      if (this.pad) this.pad.harmonicity.rampTo(Math.sqrt(51) / Math.sqrt(42), 1);
      if (this.reverb) this.reverb.wet.rampTo(0.3, 1);
    }
  }

  setLayerState(layer: 'kick' | 'lattice' | 'glitch', enabled: boolean): void {
    // Mute individual synths when disabled
    if (layer === 'kick' && this.bass) {
      this.bass.volume.rampTo(enabled ? 0 : -Infinity, 0.1);
    }
    if (layer === 'lattice' && this.pad) {
      this.pad.volume.rampTo(enabled ? 0 : -Infinity, 0.1);
    }
    if (layer === 'glitch' && this.glitch) {
      this.glitch.volume.rampTo(enabled ? -15 : -Infinity, 0.1); // Default glitch vol is -15
    }
  }

  setDistortion(amount: number) {
    // Map 0-1 to 0-1 (Tone.Distortion takes 0-1)
    if (this.distortion) this.distortion.distortion = amount;

    // Map Distortion to BitCrusher Wetness (0.0 - 0.9)
    // As distortion increases, the signal gets more "crushed"
    if (this.bitcrusher) this.bitcrusher.wet.value = amount * 0.8;

    // Map Distortion to Filter Cutoff (400Hz - 12000Hz)
    // The filter "opens up" as tension rises
    if (this.filter) {
      // Higher step = higher frequency floor
      const base = this.currentStep >= 2 ? 800 : 400;
      const freq = base + (amount * (12000 - base));
      this.filter.frequency.rampTo(freq, 0.1);
    }
  }

  setStress(amount: number) {
    // Map Stress to Reverb Decay (0.5s - 10s)
    // Creates the "Breach" explosion effect
    if (this.reverb) {
      // Note: Changing decay in real-time can be heavy, but Tone.Reverb handles it reasonably well
      // or we just set it.
      const decay = 0.5 + (amount * 9.5);
      this.reverb.decay = decay;
    }
  }

  setFilter(freq: number) {
    if (this.filter) this.filter.frequency.rampTo(freq, 0.1);
  }

  triggerDrop() {
    // The "Drop" logic
    if (!this.bass || !this.glitch || !this.distortion) return;

    const now = Tone.now();

    // 1. Cut the pad
    this.pad?.releaseAll(now);

    // 2. Maximize distortion momentarily
    this.distortion.distortion = 0.8;

    // 3. Heavy Bass Impact
    this.bass.triggerAttackRelease("C0", "1n", now);

    // 4. Glitch frenzy
    this.glitch.harmonicity = 10;
    this.glitch.triggerAttackRelease("32n", now);
    this.glitch.triggerAttackRelease("32n", now + 0.1);
    this.glitch.triggerAttackRelease("32n", now + 0.2);

    // 5. Restore after 2 seconds
    setTimeout(() => {
      if (this.distortion) this.distortion.distortion = 0.1;
      if (this.glitch) this.glitch.harmonicity = 5.1;
    }, 2000);
  }
  // --- RECORDING ---
  getStream(): MediaStreamAudioDestinationNode {
    const ctx = Tone.getContext().rawContext as AudioContext;
    const dest = ctx.createMediaStreamDestination();
    if (this.limiter) {
      this.limiter.connect(dest);
    }
    return dest;
  }
}

export const toneEngine = new ToneEngine();
