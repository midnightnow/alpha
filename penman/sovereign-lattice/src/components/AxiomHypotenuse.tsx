import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom } from '../types';

export default function AxiomHypotenuse({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [scale, setScale] = useState(30);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2 - (12 * scale) / 2}, ${height / 2 + (5 * scale) / 2})`);

    // 5-12-13 Triangle
    const p1: [number, number] = [0, 0];
    const p2: [number, number] = [12 * scale, 0];
    const p3: [number, number] = [12 * scale, -5 * scale];

    // Draw Sides
    // Umber (Downstroke) - 12
    g.append('line')
      .attr('x1', p1[0]).attr('y1', p1[1])
      .attr('x2', p2[0]).attr('y2', p2[1])
      .attr('stroke', '#141414')
      .attr('stroke-width', 12)
      .attr('opacity', 0.8);
    
    g.append('text')
      .attr('x', p2[0] / 2).attr('y', 25)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text('Umber (12)');

    // Ember (Hairline) - 5
    g.append('line')
      .attr('x1', p2[0]).attr('y1', p2[1])
      .attr('x2', p3[0]).attr('y2', p3[1])
      .attr('stroke', '#141414')
      .attr('stroke-width', 1)
      .attr('opacity', 0.8);

    g.append('text')
      .attr('x', p2[0] + 10).attr('y', p3[1] / 2)
      .attr('transform', `rotate(90, ${p2[0] + 10}, ${p3[1] / 2})`)
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text('Ember (5)');

    // The Arc (Hypotenuse) - 13
    const arcPath = d3.path();
    arcPath.moveTo(p1[0], p1[1]);
    arcPath.quadraticCurveTo(p1[0] + 2 * scale, p3[1] - 2 * scale, p3[0], p3[1]);

    g.append('path')
      .attr('d', arcPath.toString())
      .attr('fill', 'none')
      .attr('stroke', '#8b3a1a')
      .attr('stroke-width', 3)
      .attr('stroke-dasharray', '5,5');

    g.append('line')
      .attr('x1', p1[0]).attr('y1', p1[1])
      .attr('x2', p3[0]).attr('y2', p3[1])
      .attr('stroke', '#8b3a1a')
      .attr('stroke-width', 1)
      .attr('opacity', 0.3);

    g.append('text')
      .attr('x', p3[0] / 2).attr('y', p3[1] / 2 - 10)
      .attr('transform', `rotate(${Math.atan2(p3[1], p3[0]) * (180 / Math.PI)}, ${p3[0] / 2}, ${p3[1] / 2})`)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest fill-[#8b3a1a]')
      .text('The Meaning (13)');

    // Square the circle visualization
    g.append('rect')
      .attr('x', p2[0] - 20).attr('y', p2[1] - 20)
      .attr('width', 20).attr('height', 20)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 0.5)
      .attr('opacity', 0.2);

  }, [scale]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Geometric Scale</label>
          <input 
            type="range" min="10" max="60" value={scale} 
            onChange={(e) => setScale(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
      </div>
    </div>
  );
}
