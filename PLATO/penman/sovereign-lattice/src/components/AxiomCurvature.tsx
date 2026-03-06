import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom } from '../types';

export default function AxiomCurvature({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [lOverW, setLOverW] = useState(4);
  const [w, setW] = useState(30);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const margin = { top: 60, right: 60, bottom: 60, left: 80 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    // Scales
    const xScale = d3.scaleLinear().domain([1, 12]).range([0, chartWidth]);
    const yScale = d3.scaleLinear().domain([0, 4]).range([chartHeight, 0]);

    // Axes
    g.append('g')
      .attr('transform', `translate(0, ${chartHeight})`)
      .call(d3.axisBottom(xScale).ticks(12))
      .attr('class', 'font-mono text-[8px]');

    g.append('g')
      .call(d3.axisLeft(yScale).ticks(5))
      .attr('class', 'font-mono text-[8px]');

    // Labels
    g.append('text')
      .attr('x', chartWidth / 2)
      .attr('y', chartHeight + 40)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text('Wavelength Ratio (L/w)');

    g.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -chartHeight / 2)
      .attr('y', -50)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text('Radius Ratio (R_peak/w)');

    // Stability Boundary (R = w)
    g.append('line')
      .attr('x1', 0)
      .attr('y1', yScale(1))
      .attr('x2', chartWidth)
      .attr('y2', yScale(1))
      .attr('stroke', '#8b3a1a')
      .attr('stroke-dasharray', '4,4')
      .attr('opacity', 0.5);

    g.append('text')
      .attr('x', chartWidth - 10)
      .attr('y', yScale(1) - 5)
      .attr('text-anchor', 'end')
      .attr('class', 'text-[8px] font-mono fill-[#8b3a1a]')
      .text('Stability Floor (R = w)');

    // 2π Marker
    const twoPi = 2 * Math.PI;
    g.append('line')
      .attr('x1', xScale(twoPi))
      .attr('y1', 0)
      .attr('x2', xScale(twoPi))
      .attr('y2', chartHeight)
      .attr('stroke', '#141414')
      .attr('stroke-dasharray', '2,2')
      .attr('opacity', 0.3);

    g.append('text')
      .attr('x', xScale(twoPi) + 5)
      .attr('y', 10)
      .attr('class', 'text-[8px] font-mono')
      .text('2π ≈ 6.28');

    // Curvature Curve: R/w = (L/w)^2 / 4π^2
    const lineData = d3.range(1, 12.1, 0.1).map(l => ({
      l,
      r: (l * l) / (4 * Math.PI * Math.PI)
    }));

    const line = d3.line<any>()
      .x(d => xScale(d.l))
      .y(d => yScale(d.r));

    g.append('path')
      .datum(lineData)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 1.5)
      .attr('d', line);

    // Current Point
    const currentR = (lOverW * lOverW) / (4 * Math.PI * Math.PI);
    const isStable = currentR >= 1;

    g.append('circle')
      .attr('cx', xScale(lOverW))
      .attr('cy', yScale(currentR))
      .attr('r', 6)
      .attr('fill', isStable ? '#141414' : '#8b3a1a');

    // Visual Feedback Area
    const feedbackG = svg.append('g')
      .attr('transform', `translate(${width - 150}, ${height / 2})`);

    // Draw the actual curve segment
    const segmentPoints: [number, number][] = [];
    const L = lOverW * w;
    for (let x = -L/2; x <= L/2; x += 1) {
      const y = w * Math.cos((2 * Math.PI * x) / L);
      segmentPoints.push([x / 2, y / 2]);
    }

    const curveGen = d3.line().curve(d3.curveBasis);
    
    feedbackG.append('path')
      .datum(segmentPoints)
      .attr('d', curveGen as any)
      .attr('fill', 'none')
      .attr('stroke', isStable ? '#141414' : '#8b3a1a')
      .attr('stroke-width', w / 2)
      .attr('opacity', 0.8);

    feedbackG.append('text')
      .attr('y', 50)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text(isStable ? 'SEEMLY' : 'UGLY');

  }, [lOverW, w]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">L/w Ratio: {lOverW.toFixed(2)}</label>
          <input 
            type="range" min="1" max="12" step="0.1" value={lOverW} 
            onChange={(e) => setLOverW(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
        <div className="text-[10px] font-mono opacity-60 leading-tight">
          R_peak = L² / (4π²w) <br/>
          Stability requires L ≥ 2πw.
        </div>
      </div>
    </div>
  );
}
