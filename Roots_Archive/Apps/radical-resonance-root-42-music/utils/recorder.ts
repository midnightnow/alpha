import { toneEngine } from './toneEngine';

export class YouTubeExporter {
    private recorder: MediaRecorder | null = null;
    private chunks: Blob[] = [];

    start(canvas: HTMLCanvasElement) {
        const stream = canvas.captureStream(30); // 30 FPS for stability
        const audioDest = toneEngine.getStream();
        
        // Mix audio if available
        if (audioDest.stream.getAudioTracks().length > 0) {
            stream.addTrack(audioDest.stream.getAudioTracks()[0]);
        }

        // Prefer VP9 for high quality, fallback to VP8 or H264
        let mimeType = 'video/webm; codecs=vp9';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm; codecs=vp8';
        }
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm';
        }

        this.recorder = new MediaRecorder(stream, { 
            mimeType,
            videoBitsPerSecond: 5000000 // 5 Mbps
        });

        this.chunks = [];
        this.recorder.ondataavailable = (e) => {
            if (e.data.size > 0) this.chunks.push(e.data);
        };

        this.recorder.start();
        console.log("YouTubeExporter: Recording started");
    }

    async stop(filename: string = 'radical_resonance_export') {
        return new Promise<void>((resolve) => {
            if (!this.recorder || this.recorder.state === 'inactive') {
                resolve();
                return;
            }

            this.recorder.onstop = () => {
                const blob = new Blob(this.chunks, { type: 'video/webm' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `${filename}_${Date.now()}.webm`;
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                }, 100);
                console.log("YouTubeExporter: Recording saved");
                resolve();
            };

            this.recorder.stop();
        });
    }
}

export const youtubeExporter = new YouTubeExporter();
