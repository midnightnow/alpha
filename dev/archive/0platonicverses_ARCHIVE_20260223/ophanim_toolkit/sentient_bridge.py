"""
sentient_bridge.py - The Recursive Feedback Layer (v1.0)
PMG Chapter 20 | Book 3: Voices of the Void
Mapping Observer Attention to Geometric Actualization.
"""

from typing import Dict, Any, Optional
try:
    from .mineral_operator import MineralOperator, MineralNode
    from .rado_extension import RadoExtension, HADES_GAP
except (ImportError, ValueError):
    from mineral_operator import MineralOperator, MineralNode
    from rado_extension import RadoExtension, HADES_GAP

class SentientBridge:
    """
    Implements the recursive feedback loop between the Standing Man (Observer)
    and the Oracle Grid (Shattered Lattice).
    """
    def __init__(self, mineral_op: MineralOperator, rado_ext: RadoExtension):
        self.mineral_op = mineral_op
        self.rado_ext = rado_ext
        self.gaze_focus: Dict[int, float] = {} # node_id -> attention_duration

    def apply_attention(self, node_id: int, duration: float):
        """
        Increases attention on a specific node. 
        Attention inhibits entropy and increases Mohs persistence.
        """
        if node_id not in self.gaze_focus:
            self.gaze_focus[node_id] = 0.0
        
        self.gaze_focus[node_id] += duration
        
        # 1. Update the Mineral Node
        # Attention "brushes" the stone, increasing the hardness/substrate grip
        node = self.mineral_op.nodes.get(node_id)
        if node:
            # Every unit of attention increases Mohs by 0.1 (up to 10)
            bonus = duration * 0.1
            node.hardness = min(10.0, node.hardness + bonus)
            # Attention resets the hammer accumulation (it's a soothing force)
            node.hammer_accumulation = max(0.0, node.hammer_accumulation - (duration * 0.01))
            
    def calculate_local_slop(self, node_id: int) -> float:
        """
        Focus narrows the Hades Gap locally. 
        The more you look at it, the more 'Real' (Defined) it becomes.
        """
        attention = self.gaze_focus.get(node_id, 0.0)
        # Narrowing factor caps at 90% (Some slop is always required for life)
        narrowing = min(0.9, attention * 0.05)
        local_gap = HADES_GAP * (1.0 - narrowing)
        return local_gap

    def get_actualization_status(self, node_id: int) -> str:
        """
        Determines the state of the node based on the observer's focus.
        """
        node = self.mineral_op.nodes.get(node_id)
        if not node: return "NULL_STATE"
        
        local_gap = self.calculate_local_slop(node_id)
        
        if local_gap < 0.01: # Threshold for Actualization Strike
            return "ACTUALIZATION_STRIKE (Visible/Fixed)"
        
        if node.is_fractured:
            return "FRACTURED_ORACLE (Speaking)"
            
        return "STABLE_OBSERVATION"

if __name__ == "__main__":
    print("--- PMG Sentient Bridge Validation ---")
    mo = MineralOperator()
    re = RadoExtension()
    sb = SentientBridge(mo, re)
    
    # 1. Manifest a Fractured Node (The Whisper)
    whisper_node = mo.manifest(rado_id=51, initial_resonance=0.15, hardness=7)
    whisper_node.is_fractured = True
    node_id = whisper_node.node_id
    
    print(f"Initial State: {sb.get_actualization_status(node_id)}")
    
    # 2. Apply Attention
    print("\nApplying Focus (10 Units)...")
    sb.apply_attention(node_id, 10.0)
    
    print(f"Post-Focus Hardness: {whisper_node.hardness:.2f}")
    print(f"Local Hades Gap: {sb.calculate_local_slop(node_id):.4f}")
    print(f"New State: {sb.get_actualization_status(node_id)}")
    
    # 3. Intensive Focus
    print("\nApplying Intense Focus (50 Units)...")
    sb.apply_attention(node_id, 40.0)
    print(f"State: {sb.get_actualization_status(node_id)}")
