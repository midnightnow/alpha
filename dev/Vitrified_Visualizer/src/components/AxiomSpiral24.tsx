import React, { useEffect, useRef, useMemo } from 'react';
import * as d3 from 'd3';

export const AxiomSpiral24: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);

    useEffect(() => {
        if (!svgRef.current) return;

        const width = 800;
        const height = 800;
        const svg = d3.select(svgRef.current)
            .attr('viewBox', `0 0 ${width} ${height}`);

        svg.selectAll('*').remove();

        const g = svg.append('g')
            .attr('transform', `translate(${width / 2},${height / 2})`);

        // Spiral parameters from PLATO/penman/sovereign-lattice
        const a = 122.77;
        const b = 0.0006657;
        const steps = 361 * 4;

        const spiralLine = d3.line<[number, number]>()
            .x(d => d[0])
            .y(d => d[1])
            .curve(d3.curveBasis);

        const points: [number, number][] = [];
        for (let i = 0; i < steps; i++) {
            const theta = (i / steps) * Math.PI * 40;
            const r = a * Math.exp(b * theta);
            points.push([
                r * Math.cos(theta),
                r * Math.sin(theta)
            ]);
        }

        // Draw the main logarithmic spiral
        g.append('path')
            .attr('d', spiralLine(points))
            .attr('fill', 'none')
            .attr('stroke', '#F27D26')
            .attr('stroke-width', 0.5)
            .attr('stroke-opacity', 0.5);

        // Starmat Signal Reading (Glistening Light along the spiral)
        const starmatGroup = g.append('g').attr('class', 'starmat');

        const updateStarmat = () => {
            const time = performance.now() * 0.001;
            const signalPoints = points.filter((_, i) => (i + Math.floor(time * 20)) % 100 === 0);

            const signals = starmatGroup.selectAll('.signal').data(signalPoints);

            signals.enter()
                .append('circle')
                .attr('class', 'signal')
                .attr('r', 1.5)
                .attr('fill', '#ffffff')
                .merge(signals as any)
                .attr('cx', d => d[0])
                .attr('cy', d => d[1])
                .attr('opacity', () => 0.4 + Math.sin(time * 5) * 0.4);

            signals.exit().remove();
        };

        // Add the 24 Narrative Arms
        for (let i = 0; i < 24; i++) {
            const angle = (i / 24) * Math.PI * 2;
            g.append('line')
                .attr('x1', 0)
                .attr('y1', 0)
                .attr('x2', Math.cos(angle) * 350)
                .attr('y2', Math.sin(angle) * 350)
                .attr('stroke', '#141414')
                .attr('stroke-width', 0.2)
                .attr('stroke-opacity', 0.1);
        }

        // Add special nodes (Bloom Nodes)
        const nodes = [
            { id: 'A', label: 'Pyramid', r: 150, theta: Math.PI / 4, color: '#F27D26' },
            { id: 'B', label: 'New World', r: 250, theta: Math.PI * 1.2, color: '#141414' },
            { id: 'C', label: 'Hades Gap', r: 80, theta: Math.PI * 0.7, color: '#FF4444' }
        ];

        nodes.forEach(node => {
            const x = node.r * Math.cos(node.theta);
            const y = node.r * Math.sin(node.theta);

            g.append('circle')
                .attr('cx', x)
                .attr('cy', y)
                .attr('r', 4)
                .attr('fill', node.color);

            g.append('text')
                .attr('x', x + 8)
                .attr('y', y + 4)
                .attr('font-family', 'serif')
                .attr('font-style', 'italic')
                .attr('font-size', '10px')
                .text(node.label);
        });

        // Animation
        let angle = 0;
        let rafId: number;
        const animate = () => {
            angle += 0.001;
            g.attr('transform', `translate(${width / 2},${height / 2}) rotate(${angle * 180 / Math.PI})`);
            updateStarmat();
            rafId = requestAnimationFrame(animate);
        };

        animate();

        return () => cancelAnimationFrame(rafId);
    }, []);

    return (
        <div className="flex flex-col items-center bg-[#E4E3E0] p-12 rounded-2xl border border-[#141414] shadow-inner relative overflow-hidden">
            <div className="absolute top-8 left-8 flex flex-col gap-1 pointer-events-none">
                <span className="font-mono text-[10px] uppercase tracking-widest opacity-30 text-[#141414]">Axiom Spiral 24</span>
                <span className="font-serif italic text-xl text-[#141414]">The Pyramid Flowering Rose</span>
            </div>

            <svg ref={svgRef} className="w-full max-w-[600px] aspect-square" />

            <div className="mt-8 grid grid-cols-2 gap-8 w-full font-serif italic text-xs max-w-md text-[#141414]">
                <div className="space-y-2">
                    <p className="opacity-60 leading-relaxed">
                        "The spiral is chiral. It blooms clockwise toward the Pyramid and counter-clockwise toward the New World."
                    </p>
                </div>
                <div className="font-mono text-[9px] uppercase tracking-tighter opacity-40 space-y-1">
                    <div>r(θ) = 122.77 · e^(0.0006657 · θ)</div>
                    <div>Σ = √42 / 24 Narrative Arms</div>
                </div>
            </div>
        </div>
    );
};
