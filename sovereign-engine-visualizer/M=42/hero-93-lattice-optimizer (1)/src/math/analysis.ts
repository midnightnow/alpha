import convexHull from 'convex-hull';

export interface LatticeConfig {
  nodes: number;
  kDenom: number;
  epsilon: number;
}

export interface AnalysisResult {
  nodes: number;
  kDenom: number;
  volume: number;
  gap: number;
  rho: number;
}

export function testLatticeConfig(config: LatticeConfig): number {
  const { nodes, kDenom, epsilon } = config;
  const points: number[][] = [];

  // Forward nodes (s = 1 to 26)
  for (let s = 1; s <= 26; s++) {
    const r = Math.exp((s - kDenom) / kDenom);
    const phi = (Math.PI * (s - 1)) / kDenom + epsilon;
    const eta_real = r * Math.cos(phi);
    const eta_imag = r * Math.sin(phi);
    points.push([s, Math.abs(eta_real), eta_imag]);
  }

  // Closure nodes
  const nClosure = nodes - 26;
  for (let k = 0; k < nClosure; k++) {
    const theta = Math.PI + (2 * Math.PI * k) / nClosure;
    points.push([kDenom, Math.cos(theta), Math.sin(theta)]);
  }

  if (points.length < 4) return 0;
  const hull = convexHull(points);
  let volume = 0;

  for (const facet of hull) {
    const p1 = points[facet[0]];
    const p2 = points[facet[1]];
    const p3 = points[facet[2]];
    const cpX = p2[1] * p3[2] - p2[2] * p3[1];
    const cpY = p2[2] * p3[0] - p2[0] * p3[2];
    const cpZ = p2[0] * p3[1] - p2[1] * p3[0];
    const signedVol = (p1[0] * cpX + p1[1] * cpY + p1[2] * cpZ) / 6;
    volume += signedVol;
  }

  return Math.abs(volume);
}

export function runComparativeAnalysis(): AnalysisResult[] {
  const results: AnalysisResult[] = [];
  const nodeCounts = [92, 93, 94];
  const kDenoms = [12, 13, 14];
  const target = 42.0;

  for (const n of nodeCounts) {
    for (const k of kDenoms) {
      const v = testLatticeConfig({ nodes: n, kDenom: k, epsilon: 0 });
      results.push({
        nodes: n,
        kDenom: k,
        volume: v,
        gap: Math.abs(v - target),
        rho: target / v
      });
    }
  }

  return results;
}
