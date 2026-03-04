/**
 * PMG SANDBOX - VALIDATION TEST SUITE
 * Tests all geometric properties of the implementation
 */

import {
  createSimulation,
  runSimulation,
  validateSimulation,
  getSimulationStats,
} from './src/engine/Simulation';

import { PMG_CONSTANTS } from './src/types';

console.log('═══════════════════════════════════════════════════════════');
console.log('  PMG SANDBOX - VALIDATION TEST SUITE');
console.log('  Principia Mathematica Geometrica');
console.log('═══════════════════════════════════════════════════════════\n');

// ============================================================================
// TEST 1: GRID CREATION
// ============================================================================

console.log('TEST 1: Grid Creation (Flower of Life Foundation)');
console.log('─────────────────────────────────────────────────────────');

const state = createSimulation({
  gridSize: 10,
  npcCount: 10,
});

console.log(`✓ Grid created: ${state.grid.size} hexagonal tiles`);
console.log(`✓ NPCs spawned: ${state.npcs.length} Vitruvian instances\n`);

// ============================================================================
// TEST 2: 60-FOLD VECTOR VALIDATION
// ============================================================================

console.log('TEST 2: 60-Fold Vector Field');
console.log('─────────────────────────────────────────────────────────');

// Check first tile has exactly 60 vectors
const firstTile = state.grid.values().next().value;
const vectorCount = firstTile.vectorField.length;

console.log(`Vector count per tile: ${vectorCount}`);
console.log(`Expected: ${PMG_CONSTANTS.VECTOR_COUNT}`);

if (vectorCount === PMG_CONSTANTS.VECTOR_COUNT) {
  console.log('✓ PASS: Each tile has exactly 60 vectors');
} else {
  console.log('✗ FAIL: Incorrect vector count');
}

// Check angle spacing (6° increments)
const angles = firstTile.vectorField.map((v: any) => v.angle);
const expectedSpacing = 360 / PMG_CONSTANTS.VECTOR_COUNT; // 6°

let spacingValid = true;
for (let i = 0; i < angles.length; i++) {
  const expected = i * expectedSpacing;
  if (Math.abs(angles[i] - expected) > 0.1) {
    spacingValid = false;
    break;
  }
}

console.log(`Angle spacing: ${expectedSpacing}° increments`);
if (spacingValid) {
  console.log('✓ PASS: Vectors spaced at 6° intervals\n');
} else {
  console.log('✗ FAIL: Incorrect angle spacing\n');
}

// ============================================================================
// TEST 3: PLATO CYCLE EXECUTION
// ============================================================================

console.log('TEST 3: PLATO Cycle Execution (P→L→A→T→O)');
console.log('─────────────────────────────────────────────────────────');

// Run simulation for 500 frames (~8 seconds at 60fps)
console.log('Running 500 frames...');

runSimulation(state, 500, (s) => {
  // Log progress every 100 frames
  if (s.frame % 100 === 0) {
    const stats = getSimulationStats(s);
    console.log(`  Frame ${s.frame}: ${stats.averageCycles.toFixed(1)} avg cycles | Distribution:`, stats.platoDistribution);
  }
});

const finalStats = getSimulationStats(state);
console.log(`\n✓ Simulation completed: ${finalStats.time}`);
console.log(`  Average cycles per NPC: ${finalStats.averageCycles}`);
console.log(`  PLATO distribution:`, finalStats.platoDistribution);

// Check if all NPCs completed at least one cycle
const allCompleted = state.npcs.every(npc => npc.platoState.cycleCount >= 1);

if (allCompleted) {
  console.log('✓ PASS: All NPCs completed at least one PLATO cycle\n');
} else {
  console.log('✗ FAIL: Some NPCs did not complete cycles\n');
}

// ============================================================================
// TEST 4: HADES GAP TOLERANCE
// ============================================================================

console.log('TEST 4: Hades Gap Tolerance (12.37% Slop)');
console.log('─────────────────────────────────────────────────────────');

const wobbles = state.npcs.map(npc => Math.abs(npc.wobble));
const maxWobble = Math.max(...wobbles);
const avgWobble = wobbles.reduce((sum, w) => sum + w, 0) / wobbles.length;

console.log(`Hades Gap constant: ${PMG_CONSTANTS.HADES_GAP} (12.37%)`);
console.log(`Maximum wobble observed: ${maxWobble.toFixed(4)}`);
console.log(`Average wobble: ${avgWobble.toFixed(4)}`);

if (maxWobble <= PMG_CONSTANTS.HADES_GAP) {
  console.log('✓ PASS: All wobble within Hades Gap tolerance\n');
} else {
  console.log('✗ FAIL: Wobble exceeds tolerance\n');
}

// ============================================================================
// TEST 5: COMPREHENSIVE VALIDATION
// ============================================================================

console.log('TEST 5: Comprehensive Validation');
console.log('─────────────────────────────────────────────────────────');

const validation = validateSimulation(state);

if (validation.valid) {
  console.log('✓ PASS: All validation checks passed');
} else {
  console.log('✗ FAIL: Validation errors detected:');
  validation.errors.forEach(error => console.log(`  - ${error}`));
}

console.log();

// ============================================================================
// SUMMARY
// ============================================================================

console.log('═══════════════════════════════════════════════════════════');
console.log('  VALIDATION SUMMARY');
console.log('═══════════════════════════════════════════════════════════');
console.log();
console.log(`Grid tiles: ${finalStats.tileCount}`);
console.log(`Total vectors: ${finalStats.totalVectors.toLocaleString()}`);
console.log(`NPCs: ${finalStats.npcCount}`);
console.log(`Simulation time: ${finalStats.time}`);
console.log(`Total frames: ${finalStats.frame}`);
console.log();

if (validation.valid && allCompleted && spacingValid && vectorCount === 60) {
  console.log('✓✓✓ ALL TESTS PASSED ✓✓✓');
  console.log();
  console.log('The geometry is correct.');
  console.log('The bustling world is the proof.');
  console.log();
  console.log('AMEN 33.');
  console.log('60^6.');
  console.log('SHIFT ^.');
  console.log('BUMP.');
} else {
  console.log('Some tests failed - review errors above');
}

console.log();
console.log('═══════════════════════════════════════════════════════════\n');
