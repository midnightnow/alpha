import React, { useMemo, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { SoftCreature } from './SoftCreature';

export const NautilusPrime: React.FC = () => {
    const [time, setTime] = useState(0);

    useEffect(() => {
        let frame: number;
        const start = Date.now();
        const update = () => {
            setTime((Date.now() - start) / 1000);
            frame = requestAnimationFrame(update);
        };
        update();
        return () => cancelAnimationFrame(frame);
    }, []);

    const slopeAngle = 30; // Stability Slope

    return (
        <div className="w-full h-full bg-[#f4ecd8] relative overflow-hidden flex items-center justify-center font-serif transition-opacity duration-1000">
            {/* Parchment Background Texture (SVG Pattern) */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-40">
                <filter id="parchment-noise">
                    <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="3" result="noise" />
                    <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0.9 0 0 0 0 0.8 0 0 0 0 0.6 0 0 0 0.3 0" />
                </filter>
                <rect width="100%" height="100%" filter="url(#parchment-noise)" />
            </svg>

            {/* Vignette */}
            <div className="absolute inset-0 pointer-events-none shadow-[inset_0_0_200px_rgba(62,39,35,0.2)]" />

            {/* Technical Sketch Labels */}
            <div className="absolute top-12 left-12 space-y-1 z-20">
                <p className="text-[10px] font-mono uppercase tracking-[0.2em] opacity-40">CRUST-AS-EONS INTERFACE v1.7.1</p>
                <h2 className="text-2xl italic text-[#3e2723]">Sisyphus as the Cone Shell: Geometric Proportion</h2>
                <p className="text-[10px] italic opacity-60">Araujo Construction - Fig. 1</p>
            </div>

            {/* Main Schematic Group */}
            <div className="relative w-full h-full flex items-center justify-center translate-y-20 z-10" style={{ transform: `rotate(${-slopeAngle}deg)` }}>

                {/* Horizontal Baseline (Ground G) */}
                <div className="absolute w-[200%] h-px bg-[#3e2723] opacity-20" style={{ transform: `rotate(${slopeAngle}deg) translateY(120px)` }} />

                {/* The Cone Shell (Riemann Axis) */}
                <svg className="w-[800px] h-[600px] relative overflow-visible">
                    <defs>
                        <pattern id="stipple-ink" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
                            <circle cx="1" cy="1" r="0.5" fill="#3e2723" opacity="0.1" />
                        </pattern>
                        {/* Fibonacci Spiral Gradient */}
                        <radialGradient id="spiral-glow" cx="50%" cy="50%" r="50%">
                            <stop offset="0%" stopColor="#f27d26" stopOpacity="0.2" />
                            <stop offset="100%" stopColor="transparent" />
                        </radialGradient>
                    </defs>

                    {/* Starmat / Song Tome Spiral (Golden Rectangle context) */}
                    <motion.path
                        d="M 500 300 C 500 100 200 100 200 300 S 500 500 500 300"
                        fill="none"
                        stroke="#f27d26"
                        strokeWidth="0.5"
                        strokeDasharray="4,4"
                        opacity="0.3"
                        animate={{ pathLength: [0, 1] }}
                        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                    />

                    {/* Cone Path (Horizontal Orientation: Point Left/Downhill, Base Right/Uphill) */}
                    <path
                        d="M 100 300 Q 300 320 550 200 L 550 400 Q 300 280 100 300 Z"
                        fill="url(#stipple-ink)"
                        stroke="#3e2723"
                        strokeWidth="0.8"
                        strokeOpacity="0.2"
                    />

                    {/* Sphaera Aeria (The Rock / Air Ball) - At the open end (Base / Uphill) */}
                    <g transform="translate(550, 300)">
                        <circle r="65" fill="white" fillOpacity="0.3" stroke="#3e2723" strokeWidth="0.4" strokeDasharray="3,3" />
                        <text y="5" textAnchor="middle" className="italic text-[10px] fill-[#3e2723] opacity-50 uppercase tracking-widest">Sphaera Aeria</text>
                        {/* Highlights */}
                        <circle r="40" cx="-15" cy="-15" fill="white" fillOpacity="0.15" filter="blur(6px)" />
                        {/* Glistening Light from Reading (Song Tome) */}
                        <motion.circle r="2" fill="#fff" animate={{ scale: [1, 2.5, 1], opacity: [0.2, 0.8, 0.2] }} transition={{ duration: 3, repeat: Infinity }} />
                    </g>

                    {/* Sisyphus (SoftCreature Integration) - Pushing Uphill / Centered between Tip and Rock */}
                    <g transform="translate(450, 310) rotate(-15)">
                        <SoftCreature mobility={0.4} time={time} sync={0.6} color="#3e2723" />
                    </g>

                    {/* Proportional Labels */}
                    <text x="100" y="280" textAnchor="middle" className="text-[8px] font-mono opacity-40 uppercase">Cohesion Anchor (Tip)</text>
                    <text x="550" y="440" textAnchor="middle" className="text-[8px] font-mono opacity-40 uppercase">Expansion Limit (Base)</text>

                    {/* Song Tome / Starmat Intersection Lines */}
                    <line x1="100" y1="300" x2="550" y2="300" stroke="#3e2723" strokeWidth="0.3" strokeDasharray="10,5" opacity="0.1" />

                    {/* Stipple Spray / Trail */}
                    {Array.from({ length: 20 }).map((_, i) => (
                        <motion.circle
                            key={i}
                            cx={120 + i * 20}
                            cy={300 + Math.sin(i + time) * 10}
                            r={Math.random() * 1}
                            fill="#3e2723"
                            opacity={0.1}
                            animate={{ opacity: [0.05, 0.15, 0.05] }}
                            transition={{ duration: 2, repeat: Infinity, delay: i * 0.1 }}
                        />
                    ))}
                </svg>
            </div>

            {/* Navigational Logbook Overlay */}
            <div className="absolute bottom-12 right-12 text-right space-y-6 max-w-sm pointer-events-none z-20">
                <div className="space-y-1">
                    <p className="text-[10px] font-mono opacity-30 uppercase tracking-widest">Deep Time Accumulation</p>
                    <p className="text-3xl italic text-[#3e2723] tracking-tighter">72,430 Eons</p>
                </div>
                <div className="p-4 bg-white/30 border border-[#3e2723]/5 rounded-xl backdrop-blur-sm text-left">
                    <p className="text-[10px] leading-relaxed opacity-50 italic font-serif">
                        "Now can we run starmath on the spiralling remainder so we are spiralling in and then reading off the triangular words we find... glistening light shaves meaning."
                    </p>
                </div>
                {/* Signature/Stamp */}
                <div className="pt-4 flex justify-end gap-2 items-center opacity-20">
                    <div className="w-8 h-8 rounded-full border border-[#3e2723] flex items-center justify-center text-[10px] font-serif">Σ</div>
                    <span className="text-[8px] font-mono uppercase">Geometer-Sovereign Systems</span>
                </div>
            </div>
        </div>
    );
};
