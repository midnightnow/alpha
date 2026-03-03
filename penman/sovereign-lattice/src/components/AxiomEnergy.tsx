import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom, CONSTANTS } from '../types';

export default function AxiomEnergy({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [m, setM] = useState(5);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    // E = m * phi^2
    const phi = (1 + Math.sqrt(5)) / 2;
    const cSquared = phi * phi;
    const E = m * cSquared;

    const scale = 20;

    // Draw the transformation
    // Mass (m) as a square
    g.append('rect')
      .attr('x', -m * scale / 2)
      .attr('y', -m * scale / 2)
      .attr('width', m * scale)
      .attr('height', m * scale)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 2)
      .attr('opacity', 0.3);

    g.append('text')
      .attr('y', -m * scale / 2 - 10)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text(`Mass (m) = ${m}`);

    // Energy (E) as the expanded circle
    const energyRadius = Math.sqrt(E) * scale;
    g.append('circle')
      .attr('r', energyRadius)
      .attr('fill', 'none')
      .attr('stroke', '#8b3a1a')
      .attr('stroke-width', 1)
      .attr('stroke-dasharray', '4,4');

    g.append('text')
      .attr('y', energyRadius + 20)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest fill-[#8b3a1a]')
      .text(`Energy (E) ≈ ${E.toFixed(2)}`);

    // The "123 to 133" DNA Remix
    const dnaPoints = 10;
    for (let i = 0; i < dnaPoints; i++) {
      const angle = (i / dnaPoints) * 2 * Math.PI;
      g.append('line')
        .attr('x1', Math.cos(angle) * (m * scale / 2))
        .attr('y1', Math.sin(angle) * (m * scale / 2))
        .attr('x2', Math.cos(angle) * energyRadius)
        .attr('y2', Math.sin(angle) * energyRadius)
        .attr('stroke', '#d4a843')
        .attr('stroke-width', 0.5)
        .attr('opacity', 0.4);
    }

    // Constants Label
    g.append('text')
      .attr('x', -width / 2 + 20)
      .attr('y', height / 2 - 40)
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest opacity-50')
      .text(`c² = φ² ≈ ${cSquared.toFixed(4)}`);

  }, [m]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Mass Input (m)</label>
          <input 
            type="range" min="1" max="20" value={m} 
            onChange={(e) => setM(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
        <div className="text-[10px] font-mono opacity-60 leading-tight">
          The transformation of the Count (5) into the Meaning (13) via the Golden Ratio.
        </div>
      </div>
    </div>
  );
}
