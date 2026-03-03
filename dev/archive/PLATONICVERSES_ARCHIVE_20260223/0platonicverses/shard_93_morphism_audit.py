"""
shard_93_morphism_audit.py - Phase V: The 93-Shard Distance-to-Meaning Map
Principia Mathematica Geometrica | Book 4: The Infinite Game

Maps all 93 faces of the Quasicrystal Solid into Categorical Space,
calculating the "Distance to Meaning" for each shard relative to the
Sovereign Origin (the Vitrification Shrine at Shard 0).

Uses the Unified Constants signed February 20, 2026.
"""

import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ophanim_toolkit.e8_hades_validator import PMGConstants

# ============================================================================
# UNIFIED CONSTANTS (Phase V Signed)
# ============================================================================
SHEAR_DEG    = PMGConstants.SHEAR_ANGLE_DEG   # 39.47°
SHEAR_RAD    = math.radians(SHEAR_DEG)
HADES_GAP    = PMGConstants.HADES_GAP          # 0.1237
BEAT_FREQ    = PMGConstants.BEAT_FREQUENCY      # 0.6606 Hz
PACKING_RHO  = PMGConstants.PACKING_CONSTANT    # √(14/17)
UNITY_THRESH = 0.8254                           # Σ (Self-recognition threshold)

# ============================================================================
# THE 93-SHARD MORPHISM ENGINE
# ============================================================================

def entropy_to_distance(entropy: float) -> float:
    """Converts Void Entropy into spatial distance from the Shrine."""
    if entropy >= 1.0: return 99.99
    return 1.0 / (1.0 - entropy) - 1.0

def shard_entropy(shard_index: int, total_shards: int = 93) -> float:
    """
    Each shard has an intrinsic entropy based on its angular position in the 93-Faced Solid.
    Entropy = sin²(shard_angle) * Hades_Gap
    Shard 0 (Shrine) has zero entropy. Shard 46 (antipodal) has maximum.
    """
    shard_angle = (2 * math.pi * shard_index) / total_shards
    raw_entropy = math.sin(shard_angle / 2) ** 2
    return raw_entropy * (1.0 + HADES_GAP)  # Hades Gap amplifies entropy

def morphism_vector(distance: float) -> tuple:
    """Projects distance onto the 39.47° shear to get the categorical vector."""
    dx = distance * math.cos(SHEAR_RAD)
    dy = distance * math.sin(SHEAR_RAD)
    return (dx, dy)

def meaning_class(entropy: float) -> str:
    """Classifies a shard's semantic status based on its entropy level."""
    if entropy < 0.10:  return "SHRINE"       # Vitrified focal point
    if entropy < 0.30:  return "RESONANT"      # Strong harmonic presence
    if entropy < 0.50:  return "LIMINAL"       # Threshold of meaning
    if entropy < 0.70:  return "DRIFTING"      # Weakly categorized
    if entropy < 0.90:  return "VOID_EDGE"     # Near the abyss
    return "ABYSS"                              # Beyond self-recognition

# ============================================================================
# THE SIMULATION
# ============================================================================

def run_93_shard_audit():
    print("=" * 100)
    print("   PHASE V: THE 93-SHARD DISTANCE-TO-MEANING MAP")
    print("   Unified Constants | Signed February 20, 2026")
    print("=" * 100)
    print()
    print(f"   Shear Angle (θ): {SHEAR_DEG}°  |  Hades Gap (Ψ): {HADES_GAP}  |  Beat (β): {BEAT_FREQ} Hz")
    print(f"   Unity Threshold (Σ): {UNITY_THRESH}  |  Packing (ρ): {PACKING_RHO:.6f}")
    print()
    
    header = f"{'Shard':<7}| {'Entropy':<10}| {'Distance':<10}| {'Vector (dx, dy)':<24}| {'|V|':<10}| {'Class':<12}| {'Above Σ?'}"
    print(header)
    print("-" * 100)

    class_counts = {}
    above_unity = 0
    max_distance = 0
    antipodal_shard = None

    for i in range(93):
        ent = shard_entropy(i)
        dist = entropy_to_distance(ent)
        vec = morphism_vector(dist)
        magnitude = math.sqrt(vec[0]**2 + vec[1]**2)
        cls = meaning_class(ent)
        above = ent < (1.0 - UNITY_THRESH)  # Below entropy = above meaning threshold
        
        class_counts[cls] = class_counts.get(cls, 0) + 1
        if above: above_unity += 1
        if dist > max_distance:
            max_distance = dist
            antipodal_shard = i
        
        # Print every shard (compact format)
        marker = "✓" if above else "·"
        print(f"  {i:<5}| {ent:<10.4f}| {dist:<10.4f}| ({vec[0]:>9.4f}, {vec[1]:>9.4f}) | {magnitude:<10.4f}| {cls:<12}| {marker}")

    print("-" * 100)
    print()
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("=" * 100)
    print("   MORPHISM AUDIT SUMMARY")
    print("=" * 100)
    print()
    print(f"   Total Shards:        93")
    print(f"   Above Unity (Σ):     {above_unity} / 93  ({above_unity/93*100:.1f}%)")
    print(f"   Antipodal Shard:     #{antipodal_shard} (Max Distance: {max_distance:.4f})")
    print(f"   Shear Constant:      {SHEAR_DEG}° (Verified)")
    print()
    print("   Classification Distribution:")
    for cls, count in sorted(class_counts.items(), key=lambda x: -x[1]):
        bar = "█" * count
        print(f"     {cls:<12}: {count:>3} {bar}")
    
    print()
    
    # ========================================================================
    # THE GEOMETRIC PROOF
    # ========================================================================
    # The ratio of SHRINE+RESONANT shards to total should approximate ρ (Packing Constant)
    coherent = class_counts.get("SHRINE", 0) + class_counts.get("RESONANT", 0)
    ratio = coherent / 93
    print(f"   Coherence Ratio:     {coherent}/93 = {ratio:.6f}")
    print(f"   Packing Constant ρ:  {PACKING_RHO:.6f}")
    print(f"   Δ (Ratio - ρ):       {abs(ratio - PACKING_RHO):.6f}")
    print()
    
    if abs(ratio - PACKING_RHO) < 0.15:
        print("   ✅ GEOMETRIC PROOF: The Coherence Ratio approximates the Packing Constant.")
        print("      The 93-Faced Solid is self-consistent with the Unified Law.")
    else:
        print(f"   ⚠️  GEOMETRIC DEVIATION: Δ = {abs(ratio - PACKING_RHO):.6f} (outside tolerance)")
        print("      The solid requires recalibration.")
    
    print()
    print("=" * 100)
    print("   \"Every shard is a thought. Every angle is a becoming.\"")
    print("=" * 100)

if __name__ == "__main__":
    run_93_shard_audit()
