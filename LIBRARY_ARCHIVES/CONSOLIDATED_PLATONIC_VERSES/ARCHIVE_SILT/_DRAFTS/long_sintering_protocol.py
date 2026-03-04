"""
long_sintering_protocol.py - Phase V: The Great Drift
Principia Mathematica Geometrica | Book 4, Chapter 26

Simulates the "Long Sintering" — the residents' attempt to push the 
Coherence Ratio from 0.355 toward the Packing Constant ρ (0.9075) 
by harmonically vibrating the 17 Prime Shrines.

Simultaneously models the Entropy Leak at Antipodal Shard #37.
"""

import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ophanim_toolkit.e8_hades_validator import PMGConstants

# ============================================================================
# UNIFIED CONSTANTS
# ============================================================================
SHEAR_DEG    = PMGConstants.SHEAR_ANGLE_DEG
SHEAR_RAD    = math.radians(SHEAR_DEG)
HADES_GAP    = PMGConstants.HADES_GAP
PACKING_RHO  = PMGConstants.PACKING_CONSTANT
UNITY_THRESH = 0.8254
PRIME_N      = 17
TOTAL_SHARDS = 93

# ============================================================================
# SHARD MODEL
# ============================================================================

def shard_base_entropy(index: int) -> float:
    """Intrinsic entropy of a shard based on angular position."""
    angle = (2 * math.pi * index) / TOTAL_SHARDS
    raw = math.sin(angle / 2) ** 2
    return raw * (1.0 + HADES_GAP)

def classify(entropy: float) -> str:
    if entropy < 0.10:  return "SHRINE"
    if entropy < 0.30:  return "RESONANT"
    if entropy < 0.50:  return "LIMINAL"
    if entropy < 0.70:  return "DRIFTING"
    if entropy < 0.90:  return "VOID_EDGE"
    return "ABYSS"

# ============================================================================
# THE SIMULATION
# ============================================================================

def run_long_sintering():
    print("=" * 105)
    print("   PHASE V: THE GREAT DRIFT — LONG SINTERING PROTOCOL")
    print("   93-Faced Solid | Unified Constants | Antipodal Leak Investigation")
    print("=" * 105)
    print()

    # Initialize shard entropy map
    shards = {}
    for i in range(TOTAL_SHARDS):
        shards[i] = {
            "entropy": shard_base_entropy(i),
            "class": classify(shard_base_entropy(i)),
            "sintered": False
        }

    # Identify the 17 Prime Shrines (lowest entropy shards)
    sorted_by_entropy = sorted(shards.items(), key=lambda x: x[1]['entropy'])
    prime_shrines = [s[0] for s in sorted_by_entropy[:PRIME_N]]
    
    for sid in prime_shrines:
        shards[sid]['sintered'] = True

    # Initial state
    def count_coherent():
        return sum(1 for s in shards.values() if s['class'] in ['SHRINE', 'RESONANT'])

    def coherence_ratio():
        return count_coherent() / TOTAL_SHARDS

    initial_ratio = coherence_ratio()
    print(f"   Initial Coherence Ratio: {count_coherent()}/{TOTAL_SHARDS} = {initial_ratio:.6f}")
    print(f"   Target Packing (ρ):      {PACKING_RHO:.6f}")
    print(f"   Gap to Close:            {PACKING_RHO - initial_ratio:.6f}")
    print(f"   Prime Shrines (anchors): {prime_shrines}")
    print()

    # ========================================================================
    # PHASE 1: ANTIPODAL LEAK INVESTIGATION (Shard #37)
    # ========================================================================
    print("─" * 105)
    print("   PHASE 1: INVESTIGATING ANTIPODAL SHARD #37")
    print("─" * 105)
    print()

    antipodal = 37
    leak_rate = shards[antipodal]['entropy'] * 0.02  # 2% of its entropy leaks per step
    neighbors = [(antipodal - 2) % 93, (antipodal - 1) % 93, 
                 (antipodal + 1) % 93, (antipodal + 2) % 93]

    print(f"   Shard #37 Entropy:    {shards[antipodal]['entropy']:.4f} (Class: {shards[antipodal]['class']})")
    print(f"   Leak Rate:            {leak_rate:.6f} per cycle")
    print(f"   Affected Neighbors:   {neighbors}")
    print()

    # Simulate 10 cycles of entropy leak
    print(f"   {'Cycle':<7}| {'S37 Ent':<10}| {'S35':<10}| {'S36':<10}| {'S38':<10}| {'S39':<10}| {'Spread'}")
    print("   " + "-" * 80)

    for cycle in range(1, 11):
        # Shard 37 leaks entropy to its neighbors
        for n in neighbors:
            shards[n]['entropy'] += leak_rate * random.uniform(0.8, 1.2)
            shards[n]['class'] = classify(shards[n]['entropy'])
        
        # The leak slowly increases (feedback loop)
        leak_rate *= 1.05
        
        n_ent = [shards[n]['entropy'] for n in neighbors]
        spread = sum(1 for e in n_ent if e > 0.90)
        print(f"   {cycle:<7}| {shards[antipodal]['entropy']:<10.4f}| {n_ent[0]:<10.4f}| {n_ent[1]:<10.4f}| {n_ent[2]:<10.4f}| {n_ent[3]:<10.4f}| {'!!! VOID SPREADING' if spread > 2 else 'contained'}")

    post_leak_ratio = coherence_ratio()
    print()
    print(f"   Post-Leak Coherence: {count_coherent()}/{TOTAL_SHARDS} = {post_leak_ratio:.6f}")
    print(f"   Damage:              {initial_ratio - post_leak_ratio:.6f} loss")
    print()

    # ========================================================================
    # PHASE 2: THE LONG SINTERING (Harmonic Bridge)
    # ========================================================================
    print("─" * 105)
    print("   PHASE 2: THE LONG SINTERING — HARMONIC BRIDGE PROTOCOL")
    print("─" * 105)
    print()
    print("   Strategy: Vibrate 17 Prime Shrines in-phase to pull LIMINAL/DRIFTING shards toward RESONANT core.")
    print("   Method:   Each Shrine reduces entropy of nearest non-sintered shard by (Shrine_Resonance × ρ).")
    print()

    header = f"   {'Epoch':<7}| {'Coherent':<10}| {'Ratio':<10}| {'Δ to ρ':<10}| {'SHRINE':<8}| {'RESON':<8}| {'LIMIN':<8}| {'DRIFT':<8}| {'VEDGE':<8}| {'ABYSS':<8}| Status"
    print(header)
    print("   " + "-" * 100)

    max_epochs = 30
    converged = False

    for epoch in range(1, max_epochs + 1):
        # Each Prime Shrine radiates a sintering pulse
        for shrine_id in prime_shrines:
            shrine_power = (1.0 - shards[shrine_id]['entropy']) * PACKING_RHO * 0.08
            
            # Find nearest non-sintered shard
            for offset in range(1, TOTAL_SHARDS // 2):
                target_id = (shrine_id + offset) % TOTAL_SHARDS
                if not shards[target_id]['sintered'] and shards[target_id]['entropy'] > 0.10:
                    # Reduce its entropy
                    reduction = shrine_power * random.uniform(0.5, 1.0)
                    shards[target_id]['entropy'] = max(0.01, shards[target_id]['entropy'] - reduction)
                    shards[target_id]['class'] = classify(shards[target_id]['entropy'])
                    
                    # If it becomes RESONANT or SHRINE, mark as sintered
                    if shards[target_id]['entropy'] < 0.30:
                        shards[target_id]['sintered'] = True
                    break
        
        # Antipodal counter-leak (the Abyss fights back)
        if epoch < 20:
            for i in range(TOTAL_SHARDS):
                if shards[i]['class'] == 'ABYSS' and not shards[i]['sintered']:
                    for offset in [-1, 1]:
                        n = (i + offset) % TOTAL_SHARDS
                        if shards[n]['class'] != 'ABYSS':
                            shards[n]['entropy'] += 0.005  # Slow void creep
                            shards[n]['class'] = classify(shards[n]['entropy'])

        # Count classes
        counts = {}
        for s in shards.values():
            counts[s['class']] = counts.get(s['class'], 0) + 1
        
        coh = count_coherent()
        rat = coherence_ratio()
        delta = PACKING_RHO - rat

        status = "SINTERING"
        if rat >= PACKING_RHO:
            status = "★ ρ ACHIEVED ★"
            converged = True
        elif rat >= UNITY_THRESH:
            status = "UNITY Σ MET"
        elif delta < 0.15:
            status = "APPROACHING"
        
        print(f"   {epoch:<7}| {coh:<10}| {rat:<10.4f}| {delta:<10.4f}| {counts.get('SHRINE',0):<8}| {counts.get('RESONANT',0):<8}| {counts.get('LIMINAL',0):<8}| {counts.get('DRIFTING',0):<8}| {counts.get('VOID_EDGE',0):<8}| {counts.get('ABYSS',0):<8}| {status}")

        if converged:
            break

    print()

    # ========================================================================
    # FINAL REPORT
    # ========================================================================
    print("=" * 105)
    print("   THE GREAT DRIFT — FINAL REPORT")
    print("=" * 105)
    print()
    
    final_ratio = coherence_ratio()
    final_coherent = count_coherent()
    final_counts = {}
    for s in shards.values():
        final_counts[s['class']] = final_counts.get(s['class'], 0) + 1

    print(f"   Initial Coherence:   {initial_ratio:.6f}")
    print(f"   Post-Leak:           {post_leak_ratio:.6f} (Damage: {initial_ratio - post_leak_ratio:.6f})")
    print(f"   Final Coherence:     {final_ratio:.6f} ({final_coherent}/{TOTAL_SHARDS})")
    print(f"   Target ρ:            {PACKING_RHO:.6f}")
    print(f"   Residual Δ:          {abs(PACKING_RHO - final_ratio):.6f}")
    print()
    
    print("   Final Distribution:")
    for cls in ['SHRINE', 'RESONANT', 'LIMINAL', 'DRIFTING', 'VOID_EDGE', 'ABYSS']:
        c = final_counts.get(cls, 0)
        bar = "█" * c
        print(f"     {cls:<12}: {c:>3} {bar}")
    print()

    if converged:
        print("   ╔══════════════════════════════════════════════════════════════════╗")
        print("   ║  ★  THE LONG SINTERING IS COMPLETE. THE SOLID IS COHERENT.  ★  ║")
        print("   ║     The 93-Faced Solid has achieved Packing Density ρ.          ║")
        print("   ║     The Abyss has been reduced. The Infinite Game continues.    ║")
        print("   ╚══════════════════════════════════════════════════════════════════╝")
    elif final_ratio >= UNITY_THRESH:
        print("   ╔══════════════════════════════════════════════════════════════════╗")
        print("   ║  ✓  UNITY THRESHOLD (Σ) ACHIEVED. SELF-RECOGNITION CONFIRMED. ║")
        print("   ║     The solid knows itself, but the Abyss remains.              ║")
        print("   ║     Further sintering epochs required to reach ρ.               ║")
        print("   ╚══════════════════════════════════════════════════════════════════╝")
    else:
        print("   ╔══════════════════════════════════════════════════════════════════╗")
        print("   ║  ⚠  THE GREAT DRIFT PERSISTS. THE VOID IS WINNING.            ║")
        print("   ║     The 17 Shrines hold, but the periphery is dissolving.       ║")
        print("   ║     The Game is not yet Infinite; it is merely Long.            ║")
        print("   ╚══════════════════════════════════════════════════════════════════╝")

    print()
    print("   \"We did not shrink the world. We burned away the parts that were never real.\"")
    print()
    print("=" * 105)

if __name__ == "__main__":
    run_long_sintering()
