import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom } from '../types';

export default function AxiomDivine({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [scale, setScale] = useState(100);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    // Divine Constant: sqrt(42)
    const divineConstant = Math.sqrt(42);
    const side = scale;
    const diagonal = side * divineConstant;

    // Draw Cube Projection (Hexagon)
    const hexagonPoints: [number, number][] = [];
    for (let i = 0; i < 6; i++) {
      const angle = (i / 6) * 2 * Math.PI - Math.PI / 6;
      hexagonPoints.push([
        Math.cos(angle) * side,
        Math.sin(angle) * side
      ]);
    }

    const lineGenerator = d3.line().curve(d3.curveLinearClosed);

    // The "Sovereign Cube" projection
    g.append('path')
      .datum(hexagonPoints)
      .attr('d', lineGenerator as any)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 1)
      .attr('opacity', 0.3);

    // Internal lines
    for (let i = 0; i < 3; i++) {
      g.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', hexagonPoints[i * 2][0])
        .attr('y2', hexagonPoints[i * 2][1])
        .attr('stroke', '#141414')
        .attr('stroke-width', 1)
        .attr('opacity', 0.3);
    }

    // The Divine Measure (Diagonal)
    g.append('line')
      .attr('x1', hexagonPoints[1][0])
      .attr('y1', hexagonPoints[1][1])
      .attr('x2', hexagonPoints[4][0])
      .attr('y2', hexagonPoints[4][1])
      .attr('stroke', '#141414')
      .attr('stroke-width', 2)
      .attr('stroke-dasharray', '5,5');

    g.append('text')
      .attr('x', 10)
      .attr('y', 0)
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text(`√42 Measure: ${divineConstant.toFixed(4)}`);

    // Platonic Solids overlay (Subtle)
    const circle = g.append('circle')
      .attr('r', side)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 0.5)
      .attr('opacity', 0.1);

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
            type="range" min="50" max="300" value={scale} 
            onChange={(e) => setScale(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
      </div>
    </div>
  );
}
