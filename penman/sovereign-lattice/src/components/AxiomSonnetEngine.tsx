import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom, CONSTANTS } from '../types';

export default function AxiomSonnetEngine({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [bloomProgress, setBloomProgress] = useState(0);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    // G-Dot (Origin)
    g.append('circle')
      .attr('r', 5)
      .attr('fill', '#141414')
      .attr('class', 'g-dot');

    g.append('text')
      .attr('y', 20)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text('G-Dot (Origin)');

    // Horizontal Rails
    const h1 = 100; // Top Rail
    const h2 = -80; // Bottom Rail

    g.append('line')
      .attr('x1', -width / 2)
      .attr('y1', h1)
      .attr('x2', width / 2)
      .attr('y2', h1)
      .attr('stroke', '#141414')
      .attr('stroke-width', 0.5)
      .attr('opacity', 0.2);

    g.append('line')
      .attr('x1', -width / 2)
      .attr('y1', h2)
      .attr('x2', width / 2)
      .attr('y2', h2)
      .attr('stroke', '#141414')
      .attr('stroke-width', 0.5)
      .attr('opacity', 0.2);

    // 20° Aperture Vectors
    const angle = CONSTANTS.APERTURE_ANGLE * (Math.PI / 180);
    const tanAngle = Math.tan(angle);

    // Node A (Top Rail)
    const xTop = h1 / tanAngle;
    // Node B (Bottom Rail)
    const xBottom = h2 / tanAngle;

    // Draw Vectors
    const drawVector = (x: number, y: number, label: string) => {
      g.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', x * bloomProgress)
        .attr('y2', y * bloomProgress)
        .attr('stroke', '#8b3a1a')
        .attr('stroke-width', 1.5)
        .attr('stroke-dasharray', '4,4');

      if (bloomProgress > 0.9) {
        g.append('circle')
          .attr('cx', x)
          .attr('cy', y)
          .attr('r', 4)
          .attr('fill', '#8b3a1a');

        g.append('text')
          .attr('x', x + 10)
          .attr('y', y)
          .attr('class', 'text-[8px] font-mono fill-[#8b3a1a]')
          .text(label);
      }
    };

    drawVector(xTop, h1, 'Node A (Pyramid)');
    drawVector(xBottom, h2, 'Node B (New World)');

    // 24-Log Spiral Pyramid Tail (Subtle)
    if (bloomProgress > 0.5) {
      const b = 0.0573; // Germination Rate
      const arms = 24;
      const spiralG = g.append('g').attr('opacity', (bloomProgress - 0.5) * 2);

      for (let i = 0; i < arms; i++) {
        const offset = (i / arms) * 2 * Math.PI;
        const spiralPoints: [number, number][] = [];
        const maxTheta = 10 * Math.PI;

        for (let j = 0; j <= 200; j++) {
          const theta = (j / 200) * maxTheta;
          const r = 2 * Math.exp(b * theta);
          if (r > width / 2) break;
          const x = r * Math.cos(theta + offset);
          const y = r * Math.sin(theta + offset);
          spiralPoints.push([x, y]);
        }

        const lineGen = d3.line().curve(d3.curveBasis);
        spiralG.append('path')
          .datum(spiralPoints)
          .attr('d', lineGen as any)
          .attr('fill', 'none')
          .attr('stroke', '#d4a843')
          .attr('stroke-width', 0.5)
          .attr('opacity', 0.3);
      }
    }

    // Will Constant Label
    g.append('text')
      .attr('x', -width / 2 + 20)
      .attr('y', height / 2 - 20)
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest opacity-50')
      .text(`Will (Δ) = ${CONSTANTS.WILL_CONSTANT}`);

  }, [bloomProgress]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Bloom Sequence</label>
          <input 
            type="range" min="0" max="1" step="0.01" value={bloomProgress} 
            onChange={(e) => setBloomProgress(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
        <div className="text-[10px] font-mono opacity-60 leading-tight">
          The 20° aperture releases the seeds of 1609. <br/>
          The 0.009 Will drives the germination.
        </div>
      </div>
    </div>
  );
}
