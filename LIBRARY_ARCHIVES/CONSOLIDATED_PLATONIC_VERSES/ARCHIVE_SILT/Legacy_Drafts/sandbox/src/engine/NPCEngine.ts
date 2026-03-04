/**
 * PMG SANDBOX - NPC ENGINE
 * Implements PLATO State Machine (P → L → A → T → O)
 *
 * Each NPC is a "Vitruvian Instance" executing geometric cycles
 * The "bustling world" emerges from NPCs following PLATO phases
 */

import {
  NPC,
  PLATOPhase,
  PLATOState,
  Vocation,
  CubeCoord,
  Vector3,
  createCubeCoord,
  coordToKey,
  hexDistance,
  PMG_CONSTANTS,
} from '../types';

/**
 * Create NPC at specified position
 */
export function createNPC(
  id: string,
  position: CubeCoord,
  vocation: Vocation
): NPC {
  return {
    id,
    position,
    targetPosition: null,
    vocation,
    platoState: {
      current: 'P',
      duration: 0,
      nextTransition: getPhaseDuration('P', vocation),
      cycleCount: 0,
    },
    vectorField: generate60VectorsForNPC(),
    velocity: { x: 0, y: 0, z: 0 },
    wobble: (Math.random() - 0.5) * PMG_CONSTANTS.HADES_GAP,
  };
}

/**
 * Generate 60-fold vector field for NPC
 * Personal vectors radiate from NPC position
 */
function generate60VectorsForNPC(): Vector3[] {
  const vectors: Vector3[] = [];

  for (let i = 0; i < PMG_CONSTANTS.VECTOR_COUNT; i++) {
    const angleRad = i * PMG_CONSTANTS.VECTOR_ANGLE_STEP;

    vectors.push({
      x: Math.cos(angleRad),
      y: Math.sin(angleRad),
      z: 0,
    });
  }

  return vectors;
}

/**
 * Get phase duration in frames
 * Different vocations have different timing
 */
function getPhaseDuration(phase: PLATOPhase, vocation: Vocation): number {
  // Base durations for each phase (in frames at 60fps)
  const baseDurations: Record<PLATOPhase, number> = {
    P: 30,  // Point - Establish origin (0.5 sec)
    L: 60,  // Line - Extend toward goal (1.0 sec)
    A: 45,  // Angle - Calculate approach (0.75 sec)
    T: 90,  // Cross - Execute action (1.5 sec)
    O: 60,  // Circle - Complete and return (1.0 sec)
  };

  // Vocation multipliers
  const vocationMultipliers: Record<Vocation, number> = {
    Miller: 1.2,    // Slower, methodical
    Gauger: 0.9,    // Faster, precise
    Paver: 1.0,     // Standard pace
    Merchant: 0.8,  // Quick, darting
    Scribe: 1.3,    // Slowest, contemplative
  };

  const baseDuration = baseDurations[phase];
  const multiplier = vocationMultipliers[vocation];

  // Add 12.37% Hades Gap variation
  const wobble = 1.0 + (Math.random() - 0.5) * PMG_CONSTANTS.HADES_GAP;

  return Math.floor(baseDuration * multiplier * wobble);
}

/**
 * Update NPC state - executes one frame of PLATO cycle
 */
export function updateNPC(
  npc: NPC,
  grid: Map<string, any>,
  otherNPCs: NPC[]
): void {
  // Increment duration in current phase
  npc.platoState.duration++;

  // Check for phase transition
  if (npc.platoState.duration >= npc.platoState.nextTransition) {
    transitionToNextPhase(npc);
  }

  // Execute current phase behavior
  switch (npc.platoState.current) {
    case 'P':
      executePPhase(npc, grid);
      break;
    case 'L':
      executeLPhase(npc, grid);
      break;
    case 'A':
      executeAPhase(npc, grid, otherNPCs);
      break;
    case 'T':
      executeTPhase(npc, grid);
      break;
    case 'O':
      executeOPhase(npc);
      break;
  }

  // Update personal 60-fold vectors
  updateNPCVectors(npc);
}

/**
 * P PHASE: Point - Establish Origin
 * NPC selects a stable point (goal) to move toward
 */
function executePPhase(npc: NPC, grid: Map<string, any>): void {
  if (!npc.targetPosition) {
    // Find nearest stable point (plaza or building)
    npc.targetPosition = findNearestStablePoint(npc.position, grid);
  }

  // Stand still, orienting
  npc.velocity = { x: 0, y: 0, z: 0 };
}

/**
 * L PHASE: Line - Extend Toward Goal
 * NPC moves in straight line toward target
 */
function executeLPhase(npc: NPC, grid: Map<string, any>): void {
  if (!npc.targetPosition) {
    // Fallback: pick random adjacent tile
    const neighbors = getValidNeighbors(npc.position, grid);
    npc.targetPosition = neighbors[Math.floor(Math.random() * neighbors.length)];
  }

  // Calculate direction vector
  const dx = npc.targetPosition.q - npc.position.q;
  const dy = npc.targetPosition.r - npc.position.r;
  const distance = Math.sqrt(dx * dx + dy * dy);

  if (distance > 0.1) {
    // Move toward target
    npc.velocity = {
      x: (dx / distance) * 0.1,
      y: (dy / distance) * 0.1,
      z: 0,
    };

    // Update position (fractional)
    const newQ = npc.position.q + npc.velocity.x;
    const newR = npc.position.r + npc.velocity.y;

    // Round to nearest hex tile
    const roundedQ = Math.round(newQ);
    const roundedR = Math.round(newR);

    npc.position = createCubeCoord(roundedQ, roundedR);
  }
}

/**
 * A PHASE: Angle - Calculate Approach
 * NPC adjusts path based on obstacles and other NPCs
 */
function executeAPhase(npc: NPC, grid: Map<string, any>, otherNPCs: NPC[]): void {
  // Check for nearby NPCs
  const nearbyNPCs = otherNPCs.filter(other => {
    if (other.id === npc.id) return false;
    return hexDistance(npc.position, other.position) < 3;
  });

  // If crowded, adjust target to avoid collision
  if (nearbyNPCs.length > 2) {
    const neighbors = getValidNeighbors(npc.position, grid);
    // Pick least crowded neighbor
    const bestNeighbor = neighbors.reduce((best, neighbor) => {
      const crowding = otherNPCs.filter(other =>
        hexDistance(neighbor, other.position) < 2
      ).length;

      const bestCrowding = otherNPCs.filter(other =>
        hexDistance(best, other.position) < 2
      ).length;

      return crowding < bestCrowding ? neighbor : best;
    }, neighbors[0]);

    npc.targetPosition = bestNeighbor;
  }

  // Slow down while calculating
  npc.velocity.x *= 0.5;
  npc.velocity.y *= 0.5;
}

/**
 * T PHASE: Cross - Execute Action
 * NPC performs vocation-specific action at target
 */
function executeTPhase(npc: NPC, grid: Map<string, any>): void {
  // Stop moving
  npc.velocity = { x: 0, y: 0, z: 0 };

  // Vocation-specific action (future: trigger animation)
  switch (npc.vocation) {
    case 'Miller':
      // Rotate in place (grinding motion)
      break;
    case 'Gauger':
      // Measure surroundings (checking motion)
      break;
    case 'Paver':
      // Place imaginary tile (hammering motion)
      break;
    case 'Merchant':
      // Exchange gesture (offering motion)
      break;
    case 'Scribe':
      // Write in air (recording motion)
      break;
  }
}

/**
 * O PHASE: Circle - Complete and Return
 * NPC completes cycle, ready to select new point
 */
function executeOPhase(npc: NPC): void {
  // Clear target (ready for new P phase)
  npc.targetPosition = null;

  // Gentle wobble (12.37% Hades Gap)
  npc.velocity = {
    x: (Math.random() - 0.5) * PMG_CONSTANTS.HADES_GAP,
    y: (Math.random() - 0.5) * PMG_CONSTANTS.HADES_GAP,
    z: 0,
  };
}

/**
 * Transition to next PLATO phase
 */
function transitionToNextPhase(npc: NPC): void {
  const phaseSequence: PLATOPhase[] = ['P', 'L', 'A', 'T', 'O'];
  const currentIndex = phaseSequence.indexOf(npc.platoState.current);
  const nextIndex = (currentIndex + 1) % phaseSequence.length;

  npc.platoState.current = phaseSequence[nextIndex];
  npc.platoState.duration = 0;
  npc.platoState.nextTransition = getPhaseDuration(npc.platoState.current, npc.vocation);

  // Increment cycle count when returning to P
  if (npc.platoState.current === 'P') {
    npc.platoState.cycleCount++;
  }
}

/**
 * Find nearest stable point (plaza or building biome)
 */
function findNearestStablePoint(from: CubeCoord, grid: Map<string, any>): CubeCoord {
  let nearest: CubeCoord = from;
  let minDistance = Infinity;

  for (const [key, tile] of grid.entries()) {
    if (tile.biome === 'plaza' || tile.biome === 'building') {
      const distance = hexDistance(from, tile.position);
      if (distance < minDistance && distance > 0) {
        minDistance = distance;
        nearest = tile.position;
      }
    }
  }

  return nearest;
}

/**
 * Get valid neighboring tiles (not water)
 */
function getValidNeighbors(coord: CubeCoord, grid: Map<string, any>): CubeCoord[] {
  const directions = [
    { q: 1, r: 0, s: -1 },
    { q: 1, r: -1, s: 0 },
    { q: 0, r: -1, s: 1 },
    { q: -1, r: 0, s: 1 },
    { q: -1, r: 1, s: 0 },
    { q: 0, r: 1, s: -1 },
  ];

  return directions
    .map(dir => ({
      q: coord.q + dir.q,
      r: coord.r + dir.r,
      s: coord.s + dir.s,
    }))
    .filter(neighbor => {
      const key = coordToKey(neighbor);
      const tile = grid.get(key);
      return tile && tile.biome !== 'water';
    });
}

/**
 * Update NPC's personal 60-fold vectors
 * Vectors rotate based on movement and phase
 */
function updateNPCVectors(npc: NPC): void {
  const phaseAngles: Record<PLATOPhase, number> = {
    P: 0,      // 0°
    L: 12,     // 12°
    A: 24,     // 24°
    T: 36,     // 36°
    O: 48,     // 48°
  };

  const rotationOffset = phaseAngles[npc.platoState.current];

  npc.vectorField.forEach((vector, index) => {
    const baseAngle = index * PMG_CONSTANTS.VECTOR_ANGLE_STEP;
    const rotatedAngle = baseAngle + (rotationOffset * Math.PI / 180);

    vector.x = Math.cos(rotatedAngle);
    vector.y = Math.sin(rotatedAngle);

    // Add Hades Gap wobble
    const wobble = npc.wobble * Math.sin(rotatedAngle * 2);
    vector.x += wobble * 0.1;
    vector.y += wobble * 0.1;
  });
}

/**
 * Validate NPC PLATO cycles
 * Check that NPCs have completed full cycles
 */
export function validateNPCCycles(npcs: NPC[], minCycles: number = 1): boolean {
  for (const npc of npcs) {
    if (npc.platoState.cycleCount < minCycles) {
      console.warn(`NPC ${npc.id} has only completed ${npc.platoState.cycleCount} cycles (expected ${minCycles})`);
      return false;
    }
  }

  console.log(`✓ NPC validation passed: All ${npcs.length} NPCs completed ${minCycles}+ PLATO cycles`);
  return true;
}

/**
 * Get PLATO phase statistics
 * Returns distribution of NPCs across phases
 */
export function getPLATODistribution(npcs: NPC[]): Record<PLATOPhase, number> {
  const distribution: Record<PLATOPhase, number> = {
    P: 0,
    L: 0,
    A: 0,
    T: 0,
    O: 0,
  };

  npcs.forEach(npc => {
    distribution[npc.platoState.current]++;
  });

  return distribution;
}
