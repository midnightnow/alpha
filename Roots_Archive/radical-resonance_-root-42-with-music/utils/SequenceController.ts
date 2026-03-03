import { SimulationParams } from '../types';
import { toneEngine } from './toneEngine';
import { youtubeExporter } from './recorder';

export interface SequenceStep {
    time: number;
    distortion: number;
    fracture: boolean;
}

export class SequenceController {
    private startTime: number = 0;
    private isRunning: boolean = false;
    private animationFrameId: number | null = null;
    private onUpdate: (params: Partial<SimulationParams>) => void;
    private onComplete: () => void;

    // The Breach Sequence Timeline (0-60s) - MATCHING ARCHIVIST SPEC
    private timeline: SequenceStep[] = [
        { time: 0, distortion: 0.25, fracture: false },
        { time: 20, distortion: 0.25, fracture: false }, // End The Gaze
        { time: 50, distortion: 0.74, fracture: false }, // End The Stress Exponential Ramp
        { time: 50.1, distortion: 0.74, fracture: true }, // THE BREACH
        { time: 60, distortion: 0.74, fracture: true }    // Final Hold
    ];

    constructor(
        onUpdate: (params: Partial<SimulationParams>) => void,
        onComplete: () => void
    ) {
        this.onUpdate = onUpdate;
        this.onComplete = onComplete;
    }

    async start(canvas: HTMLCanvasElement) {
        if (this.isRunning) return;

        // 1. Initialize Engines
        await toneEngine.init();
        toneEngine.start();

        // 2. Start Recording
        youtubeExporter.start(canvas);

        // 3. Start Sequence
        this.startTime = performance.now();
        this.isRunning = true;
        this.animate();

        console.log("SequenceController: THE BREACH initiated.");
    }

    stop() {
        this.isRunning = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        toneEngine.stop();
        youtubeExporter.stop('Root42_PhaseII_TheBreach_Master');
        this.onComplete();
    }

    private animate() {
        if (!this.isRunning) return;

        const elapsed = (performance.now() - this.startTime) / 1000;

        if (elapsed >= 60) {
            this.stop();
            return;
        }

        // Find current interpolated params
        const params = this.interpolate(elapsed);

        // Update visual params
        this.onUpdate({
            distortion: params.distortion,
            fracture: params.fracture
        });

        // Update audio engine
        toneEngine.setDistortion(params.distortion);

        // Special trigger for the drop
        if (params.fracture && elapsed >= 55 && elapsed < 55.2) {
            toneEngine.triggerDrop();
        }

        this.animationFrameId = requestAnimationFrame(() => this.animate());
    }

    private interpolate(time: number): SequenceStep {
        // Ensure chronological order
        for (let i = 0; i < this.timeline.length - 1; i++) {
            const start = this.timeline[i];
            const end = this.timeline[i + 1];

            if (time >= start.time && time < end.time) {
                const t = (time - start.time) / (end.time - start.time);
                return {
                    time,
                    distortion: start.distortion + (end.distortion - start.distortion) * t,
                    fracture: start.fracture
                };
            }
        }
        return this.timeline[this.timeline.length - 1];
    }
}
