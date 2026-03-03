/**
 * PMG SANDBOX - TYPE DEFINITIONS
 * The Principia Mathematica Geometrica Sandbox Prototype
 *
 * Core types for the 60-fold vector field implementation
 */

// ============================================================================
// GEOMETRIC PRIMITIVES
// ============================================================================

/**
 * Hexagonal tile using cube coordinates (q + r + s = 0)
 * Foundation: Flower of Life tiling pattern
 */
export interface HexTile {
  position: CubeCoord;
  biome: Biome;
  elevation: number;
  vectorField: VectorNode[];  // 60-fold vectors at this tile
}

/**
 * Cube coordinates for hexagonal grid
 * Constraint: q + r + s = 0 (enforced by constructor)
 */
export interface CubeCoord {
  q: number;  // Column
  r: number;  // Row
  s: number;  // Diagonal (computed: -(q + r))
}

/**
 * Vector3D for 60-fold field calculations
 */
export interface Vector3 {
  x: number;
  y: number;
  z: number;
}

/**
 * Vector node in the 60-fold field
 * Each tile generates 60 vectors in all directions
 */
export interface VectorNode {
  angle: number;      // 0-360° in 6° increments (60 total)
  magnitude: number;  // Influence strength
  phase: PLATOPhase;  // Current PLATO state
}

// ============================================================================
// PLATO CYCLE SYSTEM
// ============================================================================

/**
 * The 5 phases of the PLATO cycle
 * P → L → A → T → O → P (infinite loop)
 */
export type PLATOPhase = 'P' | 'L' | 'A' | 'T' | 'O';

/**
 * PLATO phase configuration
 */
export interface PLATOState {
  current: PLATOPhase;
  duration: number;      // Frames in current phase
  nextTransition: number; // Frame count until next phase
  cycleCount: number;    // Complete cycles executed
}

// ============================================================================
// NPC SYSTEM (VITRUVIAN INSTANCES)
// ============================================================================

/**
 * Vocation types for NPCs
 * Each vocation has different PLATO cycle timing
 */
export type Vocation =
  | 'Miller'    // Grinding/rotating motion
  | 'Gauger'    // Measuring/calibrating
  | 'Paver'     // Laying/building
  | 'Merchant'  // Trading/exchanging
  | 'Scribe';   // Recording/documenting

/**
 * Non-Player Character (Vitruvian Instance)
 * Each NPC is a circle ∩ square geometric unit executing PLATO cycles
 */
export interface NPC {
  id: string;
  position: CubeCoord;
  targetPosition: CubeCoord | null;
  vocation: Vocation;
  platoState: PLATOState;
  vectorField: Vector3[];  // Personal 60-fold vectors
  velocity: Vector3;
  wobble: number;  // 12.37% Hades Gap deviation
}

// ============================================================================
// WORLD CONFIGURATION
// ============================================================================

/**
 * Biome types for tiles
 */
export type Biome =
  | 'street'    // Open pathways
  | 'building'  // Structures
  | 'garden'    // Green spaces
  | 'water'     // Rivers/fountains
  | 'plaza';    // Gathering points

/**
 * World grid configuration
 */
export interface WorldConfig {
  gridSize: number;        // Grid radius (10 = 10×10 grid)
  npcCount: number;        // Number of NPCs (default: 10)
  refreshRate: number;     // Hz (default: 60)
  vectorRefreshRate: number; // 60-fold vectors refresh (777M/sec theoretical)
  hadesGap: number;        // Tolerance constant (12.37%)
  enableZoom: boolean;     // Fractal zoom capability
}

/**
 * Simulation state
 */
export interface SimulationState {
  frame: number;
  time: number;  // Seconds elapsed
  npcs: NPC[];
  grid: Map<string, HexTile>;  // Key: "q,r,s"
  paused: boolean;
}

// ============================================================================
// VALIDATION CONSTANTS
// ============================================================================

/**
 * PMG Validation Constants
 * Used for testing geometric correctness
 */
export const PMG_CONSTANTS = {
  VECTOR_COUNT: 60,              // Vectors per node
  VECTOR_ANGLE_STEP: Math.PI / 30,  // 6° in radians
  PI_FRAME_RATIO: 22 / 7,        // Archimedean approximation
  HADES_GAP: 0.1237,             // 12.37% tolerance
  GOLDEN_RATIO: 1.618033988749,  // φ
  RAIMENT_ANGLE: 138.157,        // Golden angle in degrees
  HEART_RESONANCE: Math.sqrt(42), // √42 ≈ 6.48
} as const;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Create cube coordinate from q,r (s computed automatically)
 */
export function createCubeCoord(q: number, r: number): CubeCoord {
  return { q, r, s: -(q + r) };
}

/**
 * Convert cube coordinates to grid key
 */
export function coordToKey(coord: CubeCoord): string {
  return `${coord.q},${coord.r},${coord.s}`;
}

/**
 * Parse grid key back to coordinates
 */
export function keyToCoord(key: string): CubeCoord {
  const [q, r, s] = key.split(',').map(Number);
  return { q, r, s };
}

/**
 * Calculate distance between two hex tiles
 */
export function hexDistance(a: CubeCoord, b: CubeCoord): number {
  return (Math.abs(a.q - b.q) + Math.abs(a.r - b.r) + Math.abs(a.s - b.s)) / 2;
}
