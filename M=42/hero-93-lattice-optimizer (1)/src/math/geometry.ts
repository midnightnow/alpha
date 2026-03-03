/**
 * HERO 93 Lattice Geometry Math
 */

import convexHull from 'convex-hull';

export interface Point3D {
  x: number;
  y: number;
  z: number;
}

/**
 * Generates the HERO 93 lattice points for a given phase offset epsilon.
 */
export function generateLatticePoints(epsilon: number): number[][] {
  const points: number[][] = [];

  // Forward nodes (s = 1 to 26)
  for (let s = 1; s <= 26; s++) {
    const r = Math.exp((s - 13) / 13);
    const phi = (Math.PI * (s - 1)) / 13 + epsilon;
    const eta_real = r * Math.cos(phi);
    const eta_imag = r * Math.sin(phi);
    
    // fwd = [s, |real(eta)|, imag(eta)]
    points.push([s, Math.abs(eta_real), eta_imag]);
  }

  // Torsion closure (67 nodes)
  for (let k = 0; k < 67; k++) {
    const theta = Math.PI + (2 * Math.PI * k) / 67;
    // tor = [13.0, cos(theta), sin(theta)]
    points.push([13.0, Math.cos(theta), Math.sin(theta)]);
  }

  return points;
}

/**
 * Calculates the volume and facets of the convex hull of a set of 3D points.
 */
export function calculateHullData(points: number[][]): { volume: number; facets: number[][] } {
  if (points.length < 4) return { volume: 0, facets: [] };

  const facets = convexHull(points);
  let volume = 0;

  // We use the signed volume of tetrahedra formed by the origin and each facet.
  for (const facet of facets) {
    const p1 = points[facet[0]];
    const p2 = points[facet[1]];
    const p3 = points[facet[2]];

    const cpX = p2[1] * p3[2] - p2[2] * p3[1];
    const cpY = p2[2] * p3[0] - p2[0] * p3[2];
    const cpZ = p2[0] * p3[1] - p2[1] * p3[0];

    const signedVol = (p1[0] * cpX + p1[1] * cpY + p1[2] * cpZ) / 6;
    volume += signedVol;
  }

  return { volume: Math.abs(volume), facets };
}

/**
 * Calculates just the volume (legacy wrapper).
 */
export function calculateHullVolume(points: number[][]): number {
  return calculateHullData(points).volume;
}

/**
 * Root-finding using bisection method to find epsilon such that volume = target.
 */
export function findOptimalEpsilon(
  target: number,
  low: number,
  high: number,
  tolerance: number = 1e-8,
  maxIterations: number = 100
): { epsilon: number; volume: number; iterations: number; converged: boolean } {
  let a = low;
  let b = high;
  
  let vA = calculateHullVolume(generateLatticePoints(a)) - target;
  let vB = calculateHullVolume(generateLatticePoints(b)) - target;

  if (vA * vB > 0) {
    // No sign change, try expanding
    return { epsilon: 0, volume: 0, iterations: 0, converged: false };
  }

  let mid = 0;
  let iterations = 0;
  while (iterations < maxIterations) {
    mid = (a + b) / 2;
    const vMid = calculateHullVolume(generateLatticePoints(mid)) - target;

    if (Math.abs(vMid) < tolerance || (b - a) / 2 < tolerance) {
      return { epsilon: mid, volume: vMid + target, iterations, converged: true };
    }

    if (vMid * vA > 0) {
      a = mid;
      vA = vMid;
    } else {
      b = mid;
    }
    iterations++;
  }

  return { epsilon: mid, volume: calculateHullVolume(generateLatticePoints(mid)), iterations, converged: true };
}
