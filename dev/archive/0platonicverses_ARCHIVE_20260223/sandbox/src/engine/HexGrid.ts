/**
 * PMG SANDBOX - HEXAGONAL GRID ENGINE
 * Implements Flower of Life tiling pattern
 *
 * Foundation: Hexagonal tiles prevent 90° "Logic Locks"
 * Each tile generates 60-fold vector field
 */

import {
  HexTile,
  CubeCoord,
  VectorNode,
  Biome,
  createCubeCoord,
  coordToKey,
  PMG_CONSTANTS,
} from '../types';

/**
 * Generate 60-fold vector field for a single tile
 * Each vector points in one of 60 directions (6° spacing)
 */
export function generate60FoldVectors(): VectorNode[] {
  const vectors: VectorNode[] = [];

  for (let i = 0; i < PMG_CONSTANTS.VECTOR_COUNT; i++) {
    const angle = i * (360 / PMG_CONSTANTS.VECTOR_COUNT); // 6° increments

    vectors.push({
      angle,
      magnitude: 1.0,
      phase: 'P', // Initialize at Point phase
    });
  }

  return vectors;
}

/**
 * Create hexagonal grid of specified radius
 * Uses cube coordinates (q, r, s) where q + r + s = 0
 *
 * @param radius - Grid radius (10 = ~300 tiles)
 * @returns Map of tiles keyed by "q,r,s"
 */
export function createHexGrid(radius: number): Map<string, HexTile> {
  const grid = new Map<string, HexTile>();

  // Iterate through cube coordinate space
  for (let q = -radius; q <= radius; q++) {
    for (let r = -radius; r <= radius; r++) {
      const s = -(q + r);

      // Only include coordinates where all three are within radius
      if (Math.abs(s) <= radius) {
        const coord = createCubeCoord(q, r);
        const key = coordToKey(coord);

        grid.set(key, {
          position: coord,
          biome: assignBiome(coord, radius),
          elevation: calculateElevation(coord, radius),
          vectorField: generate60FoldVectors(),
        });
      }
    }
  }

  return grid;
}

/**
 * Assign biome based on position
 * Creates concentric pattern: plaza center, buildings middle, streets outer
 */
function assignBiome(coord: CubeCoord, radius: number): Biome {
  const distanceFromCenter = Math.max(
    Math.abs(coord.q),
    Math.abs(coord.r),
    Math.abs(coord.s)
  );

  const ratio = distanceFromCenter / radius;

  if (ratio < 0.2) return 'plaza';      // Center 20%
  if (ratio < 0.5) return 'building';   // Middle 30%
  if (ratio < 0.8) return 'street';     // Outer 30%
  return 'garden';                       // Edge 20%
}

/**
 * Calculate elevation with subtle variation
 * Adds 12.37% wobble to prevent perfect flatness
 */
function calculateElevation(coord: CubeCoord, radius: number): number {
  // Base elevation from center (slight bowl shape)
  const distanceFromCenter = Math.max(
    Math.abs(coord.q),
    Math.abs(coord.r),
    Math.abs(coord.s)
  );

  const baseElevation = distanceFromCenter * 0.1;

  // Add Hades Gap wobble (12.37% variance)
  const wobble = (Math.sin(coord.q * 0.5) + Math.cos(coord.r * 0.7)) * PMG_CONSTANTS.HADES_GAP;

  return baseElevation + wobble;
}

/**
 * Get neighboring hex tiles (6 neighbors)
 * Hexagon has exactly 6 adjacent tiles
 */
export function getNeighbors(coord: CubeCoord): CubeCoord[] {
  const directions = [
    { q: 1, r: 0, s: -1 },   // East
    { q: 1, r: -1, s: 0 },   // Northeast
    { q: 0, r: -1, s: 1 },   // Northwest
    { q: -1, r: 0, s: 1 },   // West
    { q: -1, r: 1, s: 0 },   // Southwest
    { q: 0, r: 1, s: -1 },   // Southeast
  ];

  return directions.map(dir => ({
    q: coord.q + dir.q,
    r: coord.r + dir.r,
    s: coord.s + dir.s,
  }));
}

/**
 * Convert cube coordinates to pixel position
 * For isometric rendering
 *
 * @param coord - Cube coordinates
 * @param tileSize - Size of hex tile in pixels
 */
export function cubeToPixel(coord: CubeCoord, tileSize: number): { x: number; y: number } {
  const x = tileSize * (3/2 * coord.q);
  const y = tileSize * (Math.sqrt(3)/2 * coord.q + Math.sqrt(3) * coord.r);

  return { x, y };
}

/**
 * Convert pixel position to cube coordinates
 * For mouse interaction
 */
export function pixelToCube(x: number, y: number, tileSize: number): CubeCoord {
  const q = (2/3 * x) / tileSize;
  const r = (-1/3 * x + Math.sqrt(3)/3 * y) / tileSize;

  // Round to nearest hex
  return roundCube({ q, r, s: -(q + r) });
}

/**
 * Round fractional cube coordinates to nearest hex
 */
function roundCube(coord: CubeCoord): CubeCoord {
  let q = Math.round(coord.q);
  let r = Math.round(coord.r);
  let s = Math.round(coord.s);

  const qDiff = Math.abs(q - coord.q);
  const rDiff = Math.abs(r - coord.r);
  const sDiff = Math.abs(s - coord.s);

  // Ensure q + r + s = 0 by adjusting largest diff
  if (qDiff > rDiff && qDiff > sDiff) {
    q = -(r + s);
  } else if (rDiff > sDiff) {
    r = -(q + s);
  } else {
    s = -(q + r);
  }

  return { q, r, s };
}

/**
 * Update vector field based on nearby NPCs
 * NPCs influence local vector magnitudes and phases
 *
 * @param tile - Tile to update
 * @param npcPositions - Positions of all NPCs
 */
export function updateVectorField(
  tile: HexTile,
  npcPositions: Array<{ coord: CubeCoord; phase: string }>
): void {
  // For each vector in the 60-fold field
  tile.vectorField.forEach((vector, index) => {
    // Calculate influence from nearby NPCs
    let totalInfluence = 0;

    npcPositions.forEach(npc => {
      const dx = npc.coord.q - tile.position.q;
      const dy = npc.coord.r - tile.position.r;
      const distance = Math.sqrt(dx * dx + dy * dy);

      // Inverse square falloff
      if (distance > 0) {
        const influence = 1 / (distance * distance);
        totalInfluence += influence;
      }
    });

    // Update magnitude (clamped to reasonable range)
    vector.magnitude = Math.max(0.1, Math.min(2.0, 1.0 + totalInfluence * 0.5));

    // Add 12.37% wobble to prevent perfect rigidity
    const wobble = (Math.random() - 0.5) * PMG_CONSTANTS.HADES_GAP;
    vector.magnitude += wobble;
  });
}

/**
 * Validate grid geometry
 * Ensures all tiles have exactly 60 vectors at 6° spacing
 */
export function validateGrid(grid: Map<string, HexTile>): boolean {
  for (const [key, tile] of grid.entries()) {
    // Check vector count
    if (tile.vectorField.length !== PMG_CONSTANTS.VECTOR_COUNT) {
      console.error(`Tile ${key} has ${tile.vectorField.length} vectors (expected 60)`);
      return false;
    }

    // Check angle spacing
    for (let i = 0; i < tile.vectorField.length; i++) {
      const expectedAngle = i * 6; // 6° increments
      const actualAngle = tile.vectorField[i].angle;

      if (Math.abs(actualAngle - expectedAngle) > 0.1) {
        console.error(`Tile ${key} vector ${i} angle mismatch: ${actualAngle}° (expected ${expectedAngle}°)`);
        return false;
      }
    }
  }

  console.log(`✓ Grid validation passed: ${grid.size} tiles, all with 60-fold vectors at 6° spacing`);
  return true;
}
