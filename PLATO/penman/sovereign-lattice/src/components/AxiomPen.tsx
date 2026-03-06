import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom } from '../types';

export default function AxiomPen({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [w, setW] = useState(40);
  const [tension, setTension] = useState(0.5);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    // Draw Grid
    const gridSize = 40;
    const gridLines = g.append('g').attr('class', 'grid opacity-10');
    for (let i = -width; i < width; i += gridSize) {
      gridLines.append('line').attr('x1', i).attr('y1', -height).attr('x2', i).attr('y2', height).attr('stroke', '#141414');
      gridLines.append('line').attr('x1', -width).attr('y1', i).attr('x2', width).attr('y2', i).attr('stroke', '#141414');
    }

    // 4w Stability Circle
    const stabilityRadius = w * 4;
    g.append('circle')
      .attr('r', stabilityRadius)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-dasharray', '4,4')
      .attr('opacity', 0.3);

    g.append('text')
      .attr('x', stabilityRadius + 10)
      .attr('y', 0)
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text(`4w Limit (${stabilityRadius}px)`);

    // Nib Visualization
    const nib = g.append('rect')
      .attr('x', -w / 2)
      .attr('y', -w / 2)
      .attr('width', w)
      .attr('height', w)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 2);

    // Curvature Visualization
    const rPeak = (4 * w) / (Math.PI * Math.PI);
    const curvePoints: [number, number][] = [];
    for (let t = -Math.PI; t <= Math.PI; t += 0.1) {
      const x = stabilityRadius * Math.cos(t) * tension;
      const y = stabilityRadius * Math.sin(t);
      curvePoints.push([x, y]);
    }

    const lineGenerator = d3.line()
      .curve(d3.curveBasis);

    g.append('path')
      .datum(curvePoints)
      .attr('d', lineGenerator as any)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', w / 4)
      .attr('opacity', 0.8);

    // R_peak circle
    g.append('circle')
      .attr('r', rPeak)
      .attr('fill', '#141414')
      .attr('opacity', 0.1);

    g.append('text')
      .attr('y', rPeak + 15)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text(`R_peak: ${rPeak.toFixed(2)}`);

  }, [w, tension]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Nib Width (w)</label>
          <input 
            type="range" min="10" max="100" value={w} 
            onChange={(e) => setW(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Ink Tension</label>
          <input 
            type="range" min="0.1" max="2" step="0.1" value={tension} 
            onChange={(e) => setTension(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
      </div>
    </div>
  );
}
