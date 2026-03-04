"""
mineral_operator.py - Mineral Operator implementing R(i) Decay and Hammer Constant (Xi)
PMG Chapter 4 | Principia Mathematica Geometrica
"""

import math
from typing import Dict, List
from dataclasses import dataclass

# ============================================================================
# CONSTANTS & SCALES
# ============================================================================

HAMMER_CONSTANT_THRESHOLD = 0.00014  # Xi > 0.014% cumulative drift

@dataclass
class MineralNode:
    """A persistent manifested node in the PMG Lattice"""
    node_id: int
    rado_id: int
    r0: float          # Initial Resonance
    hardness: int     # Mohs Scale (1-10)
    iterations: int = 0
    is_petrified: bool = False
    is_fractured: bool = False
    hammer_accumulation: float = 0.0 # Integral of |delta_psi|

    def calculate_resonance(self) -> float:
        """R(i) = R0 * e^(-H * i)"""
        return self.r0 * math.exp(-self.hardness * (self.iterations / 100.0))

    def get_stability_limit(self) -> int:
        """Stability Duration from Chapter 4 Table"""
        if self.hardness <= 3: return 5
        if self.hardness <= 6: return 60
        if self.hardness <= 9: return 1000
        return 99999999  # Permanent (Diamond)

class MineralOperator:
    """
    Manages the manifestation of Rado vertices into Mineral Stones.
    Implements LatticePetrification and the Hammer Constant FractureProtocol.
    """
    def __init__(self):
        self.nodes: Dict[int, MineralNode] = {}
        
    def manifest(self, rado_id: int, initial_resonance: float, hardness: int) -> MineralNode:
        node = MineralNode(
            node_id=len(self.nodes),
            rado_id=rado_id,
            r0=initial_resonance,
            hardness=hardness
        )
        self.nodes[node.node_id] = node
        return node

    def step_iteration(self, hades_gap_drift: float):
        """Advances the system clock, applying decay and checking protocols"""
        limit_reached = []
        
        for node_id, node in self.nodes.items():
            node.iterations += 1
            
            # 1. Evaporation check (Ghost nodes)
            if node.hardness <= 3 and node.iterations >= node.get_stability_limit():
                limit_reached.append(node_id)
                continue
            
            # 2. Lattice Petrification check (Resonant Anchors)
            if 4 <= node.hardness <= 9 and node.iterations >= node.get_stability_limit():
                node.is_petrified = True
                
            # 3. Hammer Constant Protocol check (Diamond)
            if node.hardness == 10:
                # Xi = sum(|drift|) * initial_resonance (Simplified integral)
                node.hammer_accumulation += abs(hades_gap_drift) * node.r0
                
                if node.hammer_accumulation > HAMMER_CONSTANT_THRESHOLD:
                    self._fracture(node)
                else:
                    node.is_petrified = True # Diamond is petrified until fractured

        for node_id in limit_reached:
            del self.nodes[node_id]

    def _fracture(self, node: MineralNode):
        """Breaks a Crystal Lock via reaching Hammer Constant (Xi). Drops to Quartz (7)."""
        node.is_fractured = True
        node.hardness = 7 
        node.is_petrified = False
        node.iterations = 0 # Resonance resets
        node.hammer_accumulation = 0.0
        # print(f"CRITICAL: Node {node.node_id} FRACTURED. Xi threshold reached.")

    def get_lattice_state(self) -> List[dict]:
        return [
            {
                "id": n.node_id,
                "rado_id": n.rado_id,
                "mohs": n.hardness,
                "res": n.calculate_resonance(),
                "petrified": n.is_petrified,
                "fractured": n.is_fractured,
                "xi": n.hammer_accumulation
            } for n in self.nodes.values()
        ]

# ============================================================================
# VALIDATION
# ============================================================================

def test_hammer_protocol():
    op = MineralOperator()
    
    # Test Diamond (Crystal Lock)
    diamond = op.manifest(rado_id=2, initial_resonance=0.1237, hardness=10)
    
    # Drift slowly
    for _ in range(10):
        op.step_iteration(0.00001) # 1e-5 drift per step
        
    print(f"Diamond Xi: {diamond.hammer_accumulation:.6f}")
    print(f"Diamond petrified: {diamond.is_petrified}")
    print(f"Diamond fractured before threshold: {diamond.is_fractured}")
    
    # Sudden large drift to cross threshold
    op.step_iteration(0.001) 
    print(f"Diamond Xi after jump (1): {diamond.hammer_accumulation:.6f}")
    print(f"Diamond fractured (1): {diamond.is_fractured}")
    
    op.step_iteration(0.001)
    print(f"Diamond Xi after jump (2): {diamond.hammer_accumulation:.6f}")
    print(f"Diamond fractured (2): {diamond.is_fractured}")
    print(f"Diamond new hardness: {diamond.hardness}")

if __name__ == "__main__":
    test_hammer_protocol()
