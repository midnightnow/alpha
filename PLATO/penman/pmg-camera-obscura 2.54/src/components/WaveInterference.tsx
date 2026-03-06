import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { PMG_CONSTANTS } from '../constants';

export const WaveInterference: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const width = 800;
    const height = 300;
    const svg = d3.select(svgRef.current)
      .attr('viewBox', `0 0 ${width} ${height}`);

    svg.selectAll('*').remove();

    const margin = { top: 50, right: 50, bottom: 50, left: 50 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear().domain([0, 26]).range([0, chartWidth]);
    const y = d3.scaleLinear().domain([-1.5, 1.5]).range([chartHeight, 0]);

    // Axes
    g.append('line')
      .attr('x1', 0)
      .attr('y1', chartHeight / 2)
      .attr('x2', chartWidth)
      .attr('y2', chartHeight / 2)
      .attr('stroke', '#141414')
      .attr('stroke-opacity', 0.2);

    // Points
    const points = [
      { s: 1, label: 'Apollo (s=1)', color: '#F27D26' },
      { s: 13, label: 'Hades Null (s=13)', color: '#FF4444' },
      { s: 26, label: 'Hero Terminal (s=26)', color: '#141414' }
    ];

    g.selectAll('.point')
      .data(points)
      .enter()
      .append('circle')
      .attr('cx', d => x(d.s))
      .attr('cy', chartHeight / 2)
      .attr('r', 4)
      .attr('fill', d => d.color);

    g.selectAll('.label')
      .data(points)
      .enter()
      .append('text')
      .attr('x', d => x(d.s))
      .attr('y', chartHeight / 2 + 20)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'Courier New')
      .attr('font-size', '10px')
      .text(d => d.label);

    // Wave paths
    const fwdPath = g.append('path')
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 1.5)
      .attr('stroke-opacity', 0.5);

    const refPath = g.append('path')
      .attr('fill', 'none')
      .attr('stroke', '#F27D26')
      .attr('stroke-width', 1.5)
      .attr('stroke-opacity', 0.5);

    const totalPath = g.append('path')
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 2);

    let time = 0;
    const animate = () => {
      time += 0.05;
      
      const generateWave = (isReflected: boolean) => {
        return d3.range(0, 26.1, 0.1).map(s => {
          const phase = isReflected ? -time : time;
          const amp = Math.sin(s * 0.5 - phase);
          return [x(s), y(isReflected ? -amp : amp)];
        });
      };

      const line = d3.line();

      fwdPath.attr('d', line(generateWave(false) as any));
      refPath.attr('d', line(generateWave(true) as any));

      const totalWave = d3.range(0, 26.1, 0.1).map(s => {
        const fwd = Math.sin(s * 0.5 - time);
        const ref = -Math.sin(s * 0.5 + time); // Phase inversion
        return [x(s), y(fwd + ref)];
      });

      totalPath.attr('d', line(totalWave as any));

      requestAnimationFrame(animate);
    };

    animate();

  }, []);

  return (
    <div className="bg-[#151619] p-8 rounded-xl border border-[#141414] text-white">
      <div className="flex justify-between mb-4 font-mono text-[10px] uppercase tracking-widest opacity-50">
        <span>Trivavled Eye // Phase Cancellation</span>
        <span>Ψ_total(13) = 0</span>
      </div>
      <svg ref={svgRef} className="w-full h-auto" />
      <div className="mt-4 text-[10px] font-mono opacity-60 leading-relaxed">
        Perfect destructive interference at s=13 (Hades Null). 
        Forward wave (Ψ_fwd) and reflected wave (Ψ_ref) cancel due to phase inversion at the Hero Terminal (s=26).
      </div>
    </div>
  );
};
