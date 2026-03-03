import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Axiom } from '../types';

export default function AxiomSpiral({ axiom }: { axiom: Axiom }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [rotations, setRotations] = useState(5);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    // b = ln(361/360) / 2π
    const b = Math.log(361 / 360) / (2 * Math.PI);
    const a = 50; // Initial radius

    const spiralPoints: [number, number][] = [];
    const steps = 500;
    const maxTheta = rotations * 2 * Math.PI;

    for (let i = 0; i <= steps; i++) {
      const theta = (i / steps) * maxTheta;
      const r = a * Math.exp(b * theta);
      const x = r * Math.cos(theta);
      const y = r * Math.sin(theta);
      spiralPoints.push([x, y]);
    }

    const lineGenerator = d3.line()
      .curve(d3.curveBasis);

    // Draw the spiral
    g.append('path')
      .datum(spiralPoints)
      .attr('d', lineGenerator as any)
      .attr('fill', 'none')
      .attr('stroke', '#141414')
      .attr('stroke-width', 1.5)
      .attr('class', 'spiral-path');

    // Draw radial lines for the 361st point
    const radialLines = 12;
    for (let i = 0; i < radialLines; i++) {
      const angle = (i / radialLines) * 2 * Math.PI;
      g.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', Math.cos(angle) * width)
        .attr('y2', Math.sin(angle) * width)
        .attr('stroke', '#141414')
        .attr('stroke-width', 0.5)
        .attr('opacity', 0.1);
    }

    // Animate points along the spiral
    const circle = g.append('circle')
      .attr('r', 4)
      .attr('fill', '#141414');

    function animate() {
      circle.transition()
        .duration(5000)
        .ease(d3.easeLinear)
        .attrTween('transform', () => {
          return (t: number) => {
            const theta = t * maxTheta;
            const r = a * Math.exp(b * theta);
            const x = r * Math.cos(theta);
            const y = r * Math.sin(theta);
            return `translate(${x}, ${y})`;
          };
        })
        .on('end', animate);
    }
    animate();

    // Text labels
    g.append('text')
      .attr('x', 20)
      .attr('y', -height / 2 + 40)
      .attr('class', 'text-[10px] font-mono uppercase tracking-widest')
      .text(`b constant: ${b.toExponential(4)}`);

  }, [rotations]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
      <div className="absolute bottom-4 right-4 bg-[#E4E3E0] border border-[#141414] p-4 flex flex-col gap-4 min-w-[240px]">
        <div>
          <label className="text-[10px] font-mono uppercase tracking-widest block mb-1">Expansion Rotations</label>
          <input 
            type="range" min="1" max="20" value={rotations} 
            onChange={(e) => setRotations(Number(e.target.value))}
            className="w-full accent-[#141414]"
          />
        </div>
      </div>
    </div>
  );
}
