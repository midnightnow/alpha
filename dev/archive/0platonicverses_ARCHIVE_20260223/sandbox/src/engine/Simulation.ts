/**
 * PMG SANDBOX - SIMULATION ENGINE
 * Main simulation loop coordinating grid, NPCs, and vector fields
 *
 * "The bustling world is the proof."
 */

import {
  SimulationState,
  WorldConfig,
  NPC,
  Vocation,
  createCubeCoord,
  coordToKey,
  PMG_CONSTANTS,
} from '../types';

import {
  createHexGrid,
  validateGrid,
  updateVectorField,
} from './HexGrid';

import {
  createNPC,
  updateNPC,
  validateNPCCycles,
  getPLATODistribution,
} from './NPCEngine';

/**
 * Initialize simulation with default configuration
 */
export function createSimulation(config?: Partial<WorldConfig>): SimulationState {
  const defaultConfig: WorldConfig = {
    gridSize: 10,
    npcCount: 10,
    refreshRate: 60,
    vectorRefreshRate: 777_000_000, // 777M iterations/sec (theoretical)
    hadesGap: PMG_CONSTANTS.HADES_GAP,
    enableZoom: true,
  };

  const finalConfig = { ...defaultConfig, ...config };

  // Create hexagonal grid (Flower of Life foundation)
  const grid = createHexGrid(finalConfig.gridSize);

  // Validate grid geometry
  if (!validateGrid(grid)) {
    throw new Error('Grid validation failed - 60-fold vectors not properly configured');
  }

  // Create NPCs (Vitruvian Instances)
  const npcs = createInitialNPCs(finalConfig.npcCount, grid);

  return {
    frame: 0,
    time: 0,
    npcs,
    grid,
    paused: false,
  };
}

/**
 * Create initial NPCs distributed across grid
 */
function createInitialNPCs(count: number, grid: Map<string, any>): NPC[] {
  const npcs: NPC[] = [];
  const vocations: Vocation[] = ['Miller', 'Gauger', 'Paver', 'Merchant', 'Scribe'];

  // Find plaza tiles for NPC spawning
  const plazaTiles = Array.from(grid.values()).filter(tile => tile.biome === 'plaza');

  if (plazaTiles.length === 0) {
    throw new Error('No plaza tiles found for NPC spawning');
  }

  for (let i = 0; i < count; i++) {
    // Cycle through vocations
    const vocation = vocations[i % vocations.length];

    // Place at random plaza tile
    const spawnTile = plazaTiles[Math.floor(Math.random() * plazaTiles.length)];

    const npc = createNPC(`npc_${i}`, spawnTile.position, vocation);
    npcs.push(npc);
  }

  return npcs;
}

/**
 * Update simulation by one frame
 * This is the main game loop
 */
export function updateSimulation(state: SimulationState): void {
  if (state.paused) return;

  // Update frame counter
  state.frame++;
  state.time = state.frame / 60; // Assuming 60 FPS

  // Update all NPCs (PLATO cycles)
  state.npcs.forEach(npc => {
    updateNPC(npc, state.grid, state.npcs);
  });

  // Update vector fields based on NPC positions
  const npcPositions = state.npcs.map(npc => ({
    coord: npc.position,
    phase: npc.platoState.current,
  }));

  state.grid.forEach(tile => {
    updateVectorField(tile, npcPositions);
  });
}

/**
 * Run simulation for specified number of frames
 * Used for validation testing
 */
export function runSimulation(
  state: SimulationState,
  frames: number,
  onFrame?: (state: SimulationState) => void
): void {
  for (let i = 0; i < frames; i++) {
    updateSimulation(state);

    if (onFrame) {
      onFrame(state);
    }
  }
}

/**
 * Validate simulation correctness
 * Tests all PMG geometric properties
 */
export function validateSimulation(state: SimulationState): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  // Test 1: Grid has 60-fold vectors at 6° spacing
  if (!validateGrid(state.grid)) {
    errors.push('Grid validation failed: Vectors not correctly configured');
  }

  // Test 2: All NPCs have completed at least one PLATO cycle
  // (Run 500 frames = ~8 seconds at 60fps, enough for 1+ cycles)
  if (state.frame >= 500) {
    if (!validateNPCCycles(state.npcs, 1)) {
      errors.push('NPC validation failed: Not all NPCs completed PLATO cycles');
    }
  }

  // Test 3: Check Hades Gap tolerance
  state.npcs.forEach(npc => {
    if (Math.abs(npc.wobble) > PMG_CONSTANTS.HADES_GAP) {
      errors.push(`NPC ${npc.id} wobble ${npc.wobble} exceeds Hades Gap (${PMG_CONSTANTS.HADES_GAP})`);
    }
  });

  // Test 4: Verify PLATO phase distribution is reasonable
  // (Should have NPCs in all 5 phases over time)
  if (state.frame >= 500) {
    const distribution = getPLATODistribution(state.npcs);
    const phasesWithNPCs = Object.values(distribution).filter(count => count > 0).length;

    if (phasesWithNPCs < 4) {
      errors.push(`PLATO distribution too narrow: Only ${phasesWithNPCs}/5 phases active`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Get simulation statistics for debugging
 */
export function getSimulationStats(state: SimulationState): {
  frame: number;
  time: string;
  npcCount: number;
  tileCount: number;
  totalVectors: number;
  platoDistribution: Record<string, number>;
  averageCycles: number;
} {
  const distribution = getPLATODistribution(state.npcs);
  const averageCycles = state.npcs.reduce((sum, npc) =>
    sum + npc.platoState.cycleCount, 0
  ) / state.npcs.length;

  return {
    frame: state.frame,
    time: `${state.time.toFixed(2)}s`,
    npcCount: state.npcs.length,
    tileCount: state.grid.size,
    totalVectors: state.grid.size * PMG_CONSTANTS.VECTOR_COUNT,
    platoDistribution: distribution,
    averageCycles: Math.round(averageCycles * 10) / 10,
  };
}

/**
 * Reset simulation to initial state
 */
export function resetSimulation(state: SimulationState, config?: Partial<WorldConfig>): void {
  const newState = createSimulation(config);

  state.frame = newState.frame;
  state.time = newState.time;
  state.npcs = newState.npcs;
  state.grid = newState.grid;
  state.paused = false;
}

/**
 * Pause/unpause simulation
 */
export function togglePause(state: SimulationState): void {
  state.paused = !state.paused;
}

/**
 * Export simulation state for analysis
 */
export function exportState(state: SimulationState): string {
  return JSON.stringify({
    frame: state.frame,
    time: state.time,
    npcs: state.npcs.map(npc => ({
      id: npc.id,
      position: npc.position,
      vocation: npc.vocation,
      phase: npc.platoState.current,
      cycles: npc.platoState.cycleCount,
    })),
    stats: getSimulationStats(state),
  }, null, 2);
}
