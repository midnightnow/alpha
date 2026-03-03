import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { calculateHullData } from '../math/geometry';

interface Props {
  points: number[][];
  width?: number;
  height?: number;
}

const LatticeVisualizer: React.FC<Props> = ({ points, width = 600, height = 400 }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    // Projection settings
    const margin = 40;
    const xExtent = d3.extent(points, p => p[0]) as [number, number];
    const yExtent = d3.extent(points, p => p[1]) as [number, number];
    const zExtent = d3.extent(points, p => p[2]) as [number, number];

    const xScale = d3.scaleLinear().domain(xExtent).range([margin, width - margin]);
    const yScale = d3.scaleLinear().domain(zExtent).range([height - margin, margin]);
    
    // Color scale based on depth (y-axis in our projection)
    const colorScale = d3.scaleSequential(d3.interpolateViridis).domain(yExtent);

    // Get Hull Data (The Shell)
    const { facets } = calculateHullData(points);

    // Draw Facets (The Shell) - Wireframe
    svg.append('g')
      .selectAll('path')
      .data(facets)
      .enter()
      .append('path')
      .attr('d', d => {
        const p1 = points[d[0]];
        const p2 = points[d[1]];
        const p3 = points[d[2]];
        return `M ${xScale(p1[0])} ${yScale(p1[2])} L ${xScale(p2[0])} ${yScale(p2[2])} L ${xScale(p3[0])} ${yScale(p3[2])} Z`;
      })
      .attr('fill', 'rgba(16, 185, 129, 0.03)')
      .attr('stroke', 'rgba(255, 255, 255, 0.05)')
      .attr('stroke-width', 0.5);

    // Draw points (The Net)
    svg.append('g')
      .selectAll('circle')
      .data(points)
      .enter()
      .append('circle')
      .attr('cx', d => xScale(d[0]))
      .attr('cy', d => yScale(d[2]))
      .attr('r', 2.5)
      .attr('fill', d => colorScale(d[1]))
      .attr('opacity', 0.9)
      .attr('stroke', '#fff')
      .attr('stroke-width', 0.5);

    // Add labels
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height - 10)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] fill-white/50 font-mono uppercase tracking-widest')
      .text('S-Axis (Growth)');

  }, [points, width, height]);

  return (
    <div className="relative bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden shadow-2xl">
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-1">
        <div className="text-[10px] font-mono text-white/40 uppercase tracking-widest">Hollow Kinetic Polytope</div>
        <div className="text-xs font-mono text-white/80">The Shell (Hull) wrapping the Net (Nodes)</div>
      </div>
      <svg
        ref={svgRef}
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        className="w-full h-auto"
      />
      <div className="absolute bottom-4 right-4 flex gap-4">
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-emerald-500/20 border border-emerald-500/40"></div>
          <span className="text-[8px] font-mono text-white/40 uppercase">The Shell</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-white/80"></div>
          <span className="text-[8px] font-mono text-white/40 uppercase">The Net</span>
        </div>
      </div>
    </div>
  );
};

export default LatticeVisualizer;
