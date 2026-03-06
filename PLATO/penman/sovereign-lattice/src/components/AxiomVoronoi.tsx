import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom } from '../types';

export default function AxiomVoronoi({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [pointsCount, setPointsCount] = useState(361);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const points: [number, number][] = Array.from({ length: pointsCount }, () => [
      Math.random() * width,
      Math.random() * height
    ]);

    const delaunay = d3.Delaunay.from(points);
    const voronoi = delaunay.voronoi([0, 0, width, height]);

    const g = svg.append('g');

    // Draw Voronoi cells
    g.append('g')
      .attr('stroke', '#141414')
      .attr('stroke-opacity', 0.2)
      .attr('fill', 'none')
      .selectAll('path')
      .data(points.map((_, i) => voronoi.renderCell(i)))
      .enter().append('path')
      .attr('d', d => d);

    // Draw points
    g.append('g')
      .attr('fill', '#141414')
      .selectAll('circle')
      .data(points)
      .enter().append('circle')
      .attr('cx', d => d[0])
      .attr('cy', d => d[1])
      .attr('r', 1.5)
      .attr('opacity', 0.5);

    // Highlight the 361st point if it's the exact count
    if (pointsCount === 361) {
      g.append('circle')
        .attr('cx', points[360][0])
        .attr('cy', points[360][1])
        .attr('r', 6)
        .attr('fill', 'none')
        .attr('stroke', '#141414')
        .attr('stroke-width', 1)
        .append('animate')
        .attr('attributeName', 'r')
        .attr('values', '4;8;4')
        .attr('dur', '2s')
        .attr('repeatCount', 'indefinite');
      
      g.append('text')
        .attr('x', points[360][0] + 10)
        .attr('y', points[360][1])
        .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
        .text('The Observer (+1)');
    }

  }, [pointsCount]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Point Density (N)</label>
          <input 
            type="range" min="10" max="1000" value={pointsCount} 
            onChange={(e) => setPointsCount(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
          <div className="flex justify-between mt-1">
            <button 
              onClick={() => setPointsCount(360)}
              className="text-[8px] font-mono border border-[#141414] px-1 hover:bg-[#141414] hover:text-[#E4E3E0]"
            >
              360 (Circle)
            </button>
            <button 
              onClick={() => setPointsCount(361)}
              className="text-[8px] font-mono border border-[#141414] px-1 hover:bg-[#141414] hover:text-[#E4E3E0]"
            >
              361 (Lattice)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
