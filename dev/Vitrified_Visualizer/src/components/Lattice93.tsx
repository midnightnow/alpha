import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export const Lattice93: React.FC = () => {
    const svgRef = useRef<SVGSVGElement>(null);

    useEffect(() => {
        if (!svgRef.current) return;

        const width = 600;
        const height = 600;
        const svg = d3.select(svgRef.current)
            .attr('viewBox', `0 0 ${width} ${height}`);

        svg.selectAll('*').remove();

        const g = svg.append('g')
            .attr('transform', `translate(${width / 2},${height / 2})`);

        // Generate 93 nodes (simplified icosahedral representation)
        const nodes: any[] = [];
        const phi = (1 + Math.sqrt(5)) / 2;

        // 12 Vertices
        const vertices = [
            [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
            [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
            [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
        ];

        vertices.forEach((v, i) => {
            nodes.push({ id: `v-${i}`, type: 'vertex', pos: v, r: 6, color: '#F27D26' });
        });

        // 20 Face Centers (simplified)
        for (let i = 0; i < 20; i++) {
            const angle = (i / 20) * Math.PI * 2;
            nodes.push({
                id: `f-${i}`,
                type: 'face',
                pos: [Math.cos(angle) * 1.5, Math.sin(angle) * 1.5, 0],
                r: 4,
                color: '#E4E3E0'
            });
        }

        // 60 Edges (simplified representation as points)
        for (let i = 0; i < 60; i++) {
            const angle = (i / 60) * Math.PI * 2;
            nodes.push({
                id: `e-${i}`,
                type: 'edge',
                pos: [Math.cos(angle) * 2, Math.sin(angle) * 2, Math.sin(angle * 2)],
                r: 2,
                color: '#141414'
            });
        }

        // 1 Core
        nodes.push({ id: 'core', type: 'core', pos: [0, 0, 0], r: 8, color: '#FF4444' });

        const scale = 120;

        // Draw links (simplified)
        const links: any[] = [];
        nodes.forEach((n, i) => {
            if (n.type === 'vertex') {
                nodes.forEach((m, j) => {
                    if (m.type === 'vertex' && i < j) {
                        const dist = Math.sqrt(
                            Math.pow(n.pos[0] - m.pos[0], 2) +
                            Math.pow(n.pos[1] - m.pos[1], 2) +
                            Math.pow(n.pos[2] - m.pos[2], 2)
                        );
                        if (dist < 2.1) links.push({ source: n, target: m });
                    }
                });
            }
        });

        const linkElements = g.selectAll('.link')
            .data(links)
            .enter()
            .append('line')
            .attr('class', 'link')
            .attr('stroke', '#141414')
            .attr('stroke-opacity', 0.2)
            .attr('stroke-width', 1);

        const nodeElements = g.selectAll('.node')
            .data(nodes)
            .enter()
            .append('circle')
            .attr('class', 'node')
            .attr('r', d => d.r)
            .attr('fill', d => d.color)
            .attr('stroke', '#141414')
            .attr('stroke-width', 1);

        // Animation loop
        let angle = 0;
        let rafId: number;
        const animate = () => {
            angle += 0.01;
            const cos = Math.cos(angle);
            const sin = Math.sin(angle);

            const project = (pos: number[]) => {
                const x = pos[0] * cos - pos[2] * sin;
                const z = pos[0] * sin + pos[2] * cos;
                const y = pos[1];
                return [x * scale, y * scale];
            };

            nodeElements
                .attr('cx', d => project(d.pos)[0])
                .attr('cy', d => project(d.pos)[1]);

            linkElements
                .attr('x1', d => project(d.source.pos)[0])
                .attr('y1', d => project(d.source.pos)[1])
                .attr('x2', d => project(d.target.pos)[0])
                .attr('y2', d => project(d.target.pos)[1]);

            rafId = requestAnimationFrame(animate);
        };

        animate();

        return () => cancelAnimationFrame(rafId);
    }, []);

    return (
        <div className="flex flex-col items-center bg-[#E4E3E0] p-8 rounded-xl border border-[#141414]">
            <div className="w-full flex justify-between mb-4 font-mono text-xs uppercase tracking-widest opacity-50 text-[#141414]">
                <span>93-Node Phase Matrix</span>
                <span>Σ=4 / √42 / √51</span>
            </div>
            <svg ref={svgRef} className="w-full max-w-[500px] aspect-square" />
            <div className="mt-6 grid grid-cols-2 gap-4 w-full font-mono text-[10px] uppercase text-[#141414]">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#F27D26]" />
                    <span>12 Vertices (Outer)</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#E4E3E0] border border-[#141414]" />
                    <span>20 Face Centers (Middle)</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#141414]" />
                    <span>60 Edges (Connectivity)</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#FF4444]" />
                    <span>1 Core Node</span>
                </div>
            </div>
        </div>
    );
};
