import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

export const CameraObscura: React.FC = () => {
    const [step, setStep] = useState(0);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    const steps = [
        { title: "Σ=4 Enclosure", description: "Establish the 4-boundary region (Tetrahedron floor)." },
        { title: "Aperture (O)", description: "Define the 1/7th radius aperture at the center." },
        { title: "Object (OB)", description: "Position the external reality to be projected." },
        { title: "Visual Rays", description: "Trace the paths through the point of inversion." },
        { title: "Phase Inversion", description: "Apply the 'Ink' medium reflection at the boundary." },
        { title: "Projection", description: "The inverted, proportional image crystallizes." }
    ];

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const width = canvas.width;
        const height = canvas.height;
        ctx.clearRect(0, 0, width, height);

        // Styling
        ctx.strokeStyle = '#141414';
        ctx.fillStyle = '#141414';
        ctx.lineWidth = 1;

        const centerX = width / 2;
        const centerY = height / 2;

        // Step 1: Σ=4 Enclosure (Triangle T1 and T2)
        if (step >= 0) {
            ctx.beginPath();
            ctx.moveTo(centerX, 50);
            ctx.lineTo(50, height - 50);
            ctx.lineTo(width - 50, height - 50);
            ctx.closePath();
            ctx.stroke();
            ctx.fillText('T1 (Outer)', centerX - 25, 40);

            if (step >= 1) {
                ctx.beginPath();
                ctx.arc(centerX, centerY, 10, 0, Math.PI * 2);
                ctx.stroke();
                ctx.fillText('O (Aperture)', centerX + 15, centerY);
            }

            if (step >= 2) {
                // Object
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(centerX - 150, centerY - 40);
                ctx.lineTo(centerX - 150, centerY + 40);
                ctx.stroke();
                ctx.lineWidth = 1;
                ctx.fillText('OB (Object)', centerX - 180, centerY - 50);
            }

            if (step >= 3) {
                // Rays
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(centerX - 150, centerY - 40);
                ctx.lineTo(centerX + 150, centerY + 40);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(centerX - 150, centerY + 40);
                ctx.lineTo(centerX + 150, centerY - 40);
                ctx.stroke();
                ctx.setLineDash([]);
            }

            if (step >= 5) {
                // Projected Image
                ctx.lineWidth = 3;
                ctx.strokeStyle = '#F27D26';
                ctx.beginPath();
                ctx.moveTo(centerX + 150, centerY - 40);
                ctx.lineTo(centerX + 150, centerY + 40);
                ctx.stroke();
                ctx.fillStyle = '#F27D26';
                ctx.fillText('B\'\'\'T\'\'\' (Inverted)', centerX + 130, centerY + 60);
            }
        }
    }, [step]);

    return (
        <div className="bg-white p-8 rounded-xl border border-[#141414] shadow-sm text-[#141414]">
            <div className="flex justify-between items-start mb-8">
                <div>
                    <h3 className="font-serif italic text-xl mb-1">{steps[step].title}</h3>
                    <p className="text-sm opacity-60 max-w-md">{steps[step].description}</p>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={() => setStep(Math.max(0, step - 1))}
                        className="px-3 py-1 border border-[#141414] text-xs uppercase hover:bg-[#141414] hover:text-white transition-colors"
                    >
                        Prev
                    </button>
                    <button
                        onClick={() => setStep(Math.min(steps.length - 1, step + 1))}
                        className="px-3 py-1 border border-[#141414] text-xs uppercase hover:bg-[#141414] hover:text-white transition-colors"
                    >
                        Next
                    </button>
                </div>
            </div>

            <div className="relative aspect-video bg-[#f9f9f9] border border-[#eee] rounded overflow-hidden">
                <canvas
                    ref={canvasRef}
                    width={800}
                    height={450}
                    className="w-full h-full"
                />

                <div className="absolute bottom-4 left-4 font-mono text-[10px] opacity-40">
                    PROJECTION OPERATOR v1.0 // Σ=4 // Ψ=0.1237
                </div>
            </div>

            <div className="mt-8 grid grid-cols-6 gap-2">
                {steps.map((_, i) => (
                    <div
                        key={i}
                        className={`h-1 rounded-full transition-colors ${i <= step ? 'bg-[#F27D26]' : 'bg-gray-200'}`}
                    />
                ))}
            </div>
        </div>
    );
};
