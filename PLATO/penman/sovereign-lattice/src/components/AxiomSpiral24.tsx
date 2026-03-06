import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom, CONSTANTS } from '../types';

export default function AxiomSpiral24({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [rotation, setRotation] = useState(0);
  const [showCircle, setShowCircle] = useState(true);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const a = CONSTANTS.SPIRAL_A;
    const b = CONSTANTS.GERMINATION_B;
    const scale = 1.5;

    // Hidden Circle
    const R = 61.4 * scale;
    if (showCircle) {
      g.append('circle')
        .attr('cy', -R)
        .attr('r', R)
        .attr('fill', 'none')
        .attr('stroke', '#141414')
        .attr('stroke-width', 0.5)
        .attr('stroke-dasharray', '2,2')
        .attr('opacity', 0.3);
    }

    // Draw 24 Arms
    const arms = 24;
    for (let i = 0; i < arms; i++) {
      const offset = (i / arms) * 2 * Math.PI + rotation;
      const points: [number, number][] = [];
      const maxTheta = 8 * Math.PI / 3; // 24 steps of 20 deg

      for (let theta = 0; theta <= maxTheta; theta += 0.1) {
        const r = a * Math.exp(b * theta) * scale;
        const x = r * Math.cos(theta + offset);
        const y = r * Math.sin(theta + offset);
        points.push([x, y]);
      }

      const lineGen = d3.line().curve(d3.curveBasis);
      g.append('path')
        .datum(points)
        .attr('d', lineGen as any)
        .attr('fill', 'none')
        .attr('stroke', i % 2 === 0 ? '#8b3a1a' : '#d4a843')
        .attr('stroke-width', 0.8)
        .attr('opacity', 0.6);
    }

    // Bloom Nodes
    const drawNode = (angleDeg: number, label: string) => {
      const theta = angleDeg * (Math.PI / 180);
      const r = a * Math.exp(b * theta) * scale;
      const x = r * Math.cos(theta + rotation);
      const y = r * Math.sin(theta + rotation);

      g.append('circle')
        .attr('cx', x)
        .attr('cy', y)
        .attr('r', 4)
        .attr('fill', '#141414');

      g.append('text')
        .attr('x', x + 8)
        .attr('y', y)
        .attr('class', 'text-[8px] font-mono fill-[#141414]')
        .text(label);
    };

    drawNode(20, 'Node A (Pyramid)');
    drawNode(200, 'Node B (New World)');

    // Center Label
    g.append('text')
      .attr('y', 10)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest opacity-50')
      .text('The Folding Mechanism');

  }, [rotation, showCircle]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Rotation</label>
          <input 
            type="range" min="0" max={Math.PI * 2} step="0.01" value={rotation} 
            onChange={(e) => setRotation(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
        <div className="flex items-center gap-2">
          <input 
            type="checkbox" checked={showCircle} 
            onChange={(e) => setShowCircle(e.target.checked)}
            className="accent-[#141414]"
          />
          <label className="text-[10px] font-mono uppercase tracking-widest">Show Hidden Circle</label>
        </div>
        <div className="text-[10px] font-mono opacity-60 leading-tight">
          r(θ) = 122.77 · e^(0.0006657 · θ) <br/>
          24 arms of narrative time.
        </div>
      </div>
    </div>
  );
}
