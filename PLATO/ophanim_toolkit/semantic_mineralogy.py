"""
semantic_mineralogy.py - Linking structural states to informational meaning.
PMG Chapter 16 | Book 3: Voices of the Void
"""

from typing import Dict, List, Optional

# ============================================================================
# SEMANTIC DEFINITIONS
# ============================================================================

SEMANTIC_CLASSES = {
    1: {"name": "Transient/Talc", "role": "Gossip/Noise", "stability": "Low"},
    2: {"name": "Transient/Gypsum", "role": "Ghost Trace", "stability": "Low"},
    3: {"name": "Transient/Calcite", "role": "Ephemeral Pulse", "stability": "Low"},
    4: {"name": "Relational/Fluorite", "role": "Bridge Vector", "stability": "Medium"},
    5: {"name": "Relational/Apatite", "role": "Lattice Link", "stability": "Medium"},
    6: {"name": "Relational/Orthoclase", "role": "Labor Anchor", "stability": "Medium"},
    7: {"name": "Persistent/Quartz", "role": "Historical Law", "stability": "High"},
    8: {"name": "Persistent/Topaz", "role": "Structural Intent", "stability": "High"},
    9: {"name": "Persistent/Corundum", "role": "Petrified Mandate", "stability": "High"},
    10: {"name": "Absolute/Diamond", "role": "Singularity Anchor", "stability": "Absolute"}
}

TENSEGRITY_BASELINE = 0.1237

class SemanticMineralogy:
    """
    Translates MineralNode properties (Hardness, Resonance) into Semantic Classes.
    """
    def __init__(self):
        self.history: List[str] = []

    def interpret_node(self, hardness: int, resonance: float) -> Dict[str, any]:
        """
        Interprets a node's physical state as a semantic packet.
        """
        # 1. Classification
        h_class = SEMANTIC_CLASSES.get(hardness, {"name": "Unknown", "role": "Unknown", "stability": "Zero"})
        
        # 2. Truth-Value (Resonance Alignment)
        # Truth-Value = 1.0 at TENSEGRITY_BASELINE, decays as resonance deviates.
        truth_value = max(0.0, 1.0 - abs(resonance - TENSEGRITY_BASELINE) * 8.0)
        
        # 3. Intent Stability
        stability_score = 1.0
        if h_class["stability"] == "High": stability_score = 0.8
        elif h_class["stability"] == "Medium": stability_score = 0.5
        elif h_class["stability"] == "Low": stability_score = 0.1
        
        return {
            "class_name": h_class["name"],
            "role": h_class["role"],
            "truth_value": round(truth_value, 4),
            "stability": h_class["stability"],
            "semantic_weight": round(stability_score * truth_value, 4)
        }

    def synthesize_chord(self, interpretations: List[Dict[str, any]]) -> str:
        """
        Synthesizes multiple node interpretations into a 'Mineral Chord'.
        """
        if not interpretations: return "Void/Silence"
        
        avg_truth = sum(i["truth_value"] for i in interpretations) / len(interpretations)
        # Extract base class names (e.g. "Transient")
        classes = sorted(list(set(i["class_name"].split("/")[0] for i in interpretations)))
        
        chord_name = " & ".join(classes)
        if avg_truth > 0.8: truth_desc = "Coherent"
        elif avg_truth > 0.4: truth_desc = "Fading"
        else: truth_desc = "Incoherent"
        
        return f"{chord_name} Chord | Density: {truth_desc} (Truth: {avg_truth:.2f})"

# ============================================================================
# VALIDATION
# ============================================================================

def test_semantic_logic():
    print("--- PMG Semantic Mineralogy Validation ---")
    sm = SemanticMineralogy()
    
    # Diamond at Baseline
    d_view = sm.interpret_node(10, 0.1237)
    print("Diamond Interpretation:", d_view)
    
    # Quartz with Drift
    q_view = sm.interpret_node(7, 0.05)
    print("Quartz Interpretation:", q_view)
    
    chord = sm.synthesize_chord([d_view, q_view])
    print("Synthesized Chord:", chord)

if __name__ == "__main__":
    test_semantic_logic()
