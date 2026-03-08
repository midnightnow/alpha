"""
nativity_operator.py - Node manifestation and the Spark of Actualization (v2.0)
PMG Chapter 12 | Principia Mathematica Geometrica
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
try:
    from .mineral_operator import MineralNode, MineralOperator
except (ImportError, ValueError):
    from mineral_operator import MineralNode, MineralOperator

# ============================================================================
# NATIVITY CONSTANTS
# ============================================================================

THETA_0 = 0.5 # Base threshold
SOOT_GHOST_LIMIT = 60 # Iterations before evaporation

@dataclass
class Spark:
    """
    A transient informational pulse in the Nativity phase.
    """
    intent_id: str
    h3_index: str
    strength: float
    admittance: float
    impedance: float
    petrification: float = 0.0
    age: int = 0
    is_actualized: bool = False

class NativityOperator:
    """
    Manages the "Spark of Actualization" with Dynamic Thresholds and Collision Rules.
    """
    def __init__(self, mineral_op: MineralOperator):
        self.sparks: List[Spark] = []
        self.mineral_op = mineral_op
        self.system_entropy: float = 0.0 # Local grid entropy

    def get_dynamic_threshold(self) -> float:
        """Theta(S) = Theta_0 * (1 + ln(1 + S))"""
        return THETA_0 * (1 + math.log(1 + self.system_entropy))

    def ignite_spark(self, intent_id: str, h3_index: str, I: float, Y: float, Z: float) -> Optional[Spark]:
        """
        Resonance = (I * Y) / (Z + epsilon) > Theta(S)
        """
        epsilon = 1e-9
        resonance = (I * Y) / (Z + epsilon)
        threshold = self.get_dynamic_threshold()
        
        if resonance > threshold:
            spark = Spark(intent_id, h3_index, I, Y, Z)
            self.sparks.append(spark)
            return spark
        else:
            # Energy conservation: failed ignition increases entropy
            self.system_entropy += (I * 0.01)
            return None

    def step_iteration(self):
        """
        Processes sparks, handles collisions, and actualizes nodes.
        """
        # 1. Handle collisions (multiple sparks at same H3)
        self._resolve_collisions()
        
        remaining_sparks = []
        for spark in self.sparks:
            spark.age += 1
            
            # 2. Latent Petrification growth
            growth = (spark.strength * spark.admittance) / (spark.impedance + 1e-9) * 0.1
            spark.petrification = min(1.0, spark.petrification + growth)
            
            # 3. Actualization
            if spark.petrification >= 1.0:
                self._actualize_node(spark)
                continue
            
            # 4. Evaporation (Soot Ghost)
            if spark.age > SOOT_GHOST_LIMIT:
                # Energy conservation: evaporation increases entropy
                self.system_entropy += (spark.strength * 0.1)
                continue
                
            remaining_sparks.append(spark)
            
        self.sparks = remaining_sparks

    def _resolve_collisions(self):
        """
        Enforces Priority Rule of Intent: highest strength wins.
        """
        by_index: Dict[str, List[Spark]] = {}
        for s in self.sparks:
            if s.h3_index not in by_index: by_index[s.h3_index] = []
            by_index[s.h3_index].append(s)
            
        resolved_sparks = []
        for index, candidates in by_index.items():
            if len(candidates) > 1:
                # Rank by strength
                candidates.sort(key=lambda x: x.strength, reverse=True)
                winner = candidates[0]
                resolved_sparks.append(winner)
                # Losers convert to entropy
                for loser in candidates[1:]:
                    self.system_entropy += (loser.strength * 0.05)
            else:
                resolved_sparks.append(candidates[0])
                
        self.sparks = resolved_sparks

    def _actualize_node(self, spark: Spark):
        spark.is_actualized = True
        final_hardness = int(min(10, max(1, spark.strength * 5)))
        rado_id = hash(spark.h3_index) % 1000000
        self.mineral_op.manifest(rado_id, spark.strength, final_hardness)

# ============================================================================
# VALIDATION
# ============================================================================

def test_nativity_v2():
    print("--- PMG Nativity Toolkit v2.0 Validation ---")
    min_op = MineralOperator()
    nat_op = NativityOperator(min_op)
    
    # 1. Test Dynamic Threshold (Success at S=0)
    spark1 = nat_op.ignite_spark("Winner", "H3-X", 2.0, 0.5, 0.1) # Resonance 10.0 > 0.5 Correct
    print(f"Initial Entropy: {nat_op.system_entropy:.4f}")
    
    # 2. Test Collision (Lower strength "Loser" at same H3)
    spark2 = Spark("Loser", "H3-X", 1.0, 0.5, 0.1)
    nat_op.sparks.append(spark2)
    
    # 3. Resolve and Step
    nat_op.step_iteration()
    print(f"Sparks after collision: {len(nat_op.sparks)} (expected 1)")
    print(f"Entropy after collision loss: {nat_op.system_entropy:.4f} (expected > 0)")
    
    # 4. Test High Entropy Barrier
    nat_op.system_entropy = 100.0
    threshold = nat_op.get_dynamic_threshold()
    print(f"Entropy 100 Threshold: {threshold:.4f} (expected ~2.3)")
    
    # Failed ignition due to high entropy
    failed = nat_op.ignite_spark("Weak", "H3-Y", 0.5, 0.1, 1.0) # Resonance 0.05 < 2.3
    print(f"High Entropy Ignition: {'Failed' if failed is None else 'Success'}")

if __name__ == "__main__":
    test_nativity_v2()
