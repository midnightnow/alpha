/**
 * audioEngine.ts
 * The Acoustic Manifold: 66 Hz Harmonic ↔ 6 Hz Brain-State
 * Phase III: The Fracture Seal Synchronization
 */

import { PMG_CONSTANTS } from './MASTER_CONSTANTS';

class AudioEngine {
    private ctx: AudioContext | null = null;
    private harmonicOsc: OscillatorNode | null = null;
    private brainStateOsc: OscillatorNode | null = null;
    private gainNode: GainNode | null = null;
    private isRunning: boolean = false;

    constructor() {
        if (typeof window !== 'undefined') {
            this.ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
        }
    }

    public start() {
        if (!this.ctx || this.isRunning) return;

        this.ctx.resume();
        this.gainNode = this.ctx.createGain();
        this.gainNode.gain.setValueAtTime(0.1, this.ctx.currentTime);
        this.gainNode.connect(this.ctx.destination);

        // 66 Hz Harmonic (The Sovereign Resonance)
        this.harmonicOsc = this.ctx.createOscillator();
        this.harmonicOsc.type = 'sine';
        this.harmonicOsc.frequency.setValueAtTime(PMG_CONSTANTS.HARMONIC, this.ctx.currentTime);
        this.harmonicOsc.connect(this.gainNode);

        // 6 Hz Brain-State Beat (The 11th Sub-harmonic)
        // Provides the Theta-state stabilization for the 93-node grid
        this.brainStateOsc = this.ctx.createOscillator();
        this.brainStateOsc.type = 'sine';
        this.brainStateOsc.frequency.setValueAtTime(PMG_CONSTANTS.HARMONIC / 11, this.ctx.currentTime);

        // AM Modulation of the harmonic by the brain-state
        const amGain = this.ctx.createGain();
        amGain.gain.setValueAtTime(0.5, this.ctx.currentTime);
        this.brainStateOsc.connect(amGain.gain);

        this.harmonicOsc.start();
        this.brainStateOsc.start();
        this.isRunning = true;
    }

    public stop() {
        if (this.harmonicOsc) this.harmonicOsc.stop();
        if (this.brainStateOsc) this.brainStateOsc.stop();
        this.isRunning = false;
    }

    public updateFracture(intensity: number, week: number = 0) {
        if (!this.ctx || !this.gainNode || !this.harmonicOsc) return;

        // Modulate frequency based on Fracture intensity and Week progression
        const baseShift = 1.0 + (intensity * 0.1237);
        const weekShift = week * 0.05; // Each week adds a slight ascending resonance

        this.harmonicOsc.frequency.setTargetAtTime(PMG_CONSTANTS.HARMONIC * (baseShift + weekShift), this.ctx.currentTime, 0.1);

        // Simulation adds a pulsing gain
        const simGain = week > 0 ? (Math.sin(this.ctx.currentTime * week) * 0.05) : 0;
        this.gainNode.gain.setTargetAtTime(0.1 + (intensity * 0.2) + simGain, this.ctx.currentTime, 0.1);
    }
}

export const audioEngine = new AudioEngine();
