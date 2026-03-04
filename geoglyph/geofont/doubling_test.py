import json
import math

class SanskritResonanceTester:
    def __init__(self):
        # Sanskrit Varga (Consonants)
        # 5 Places * 4 (Voiceless/Voiced x Unasp/Asp)
        self.vargas = {
            "Velar": ["k", "kh", "g", "gh"],
            "Palatal": ["c", "ch", "j", "jh"],
            "Retroflex": ["ṭ", "ṭh", "ḍ", "ḍh"],
            "Dental": ["t", "th", "d", "dh"],
            "Labial": ["p", "ph", "b", "bh"]
        }
        self.nasals = ["ṅ", "ñ", "ṇ", "n", "m"]
        self.semi_vowels = ["y", "r", "l", "v"]
        self.sibilants = ["ś", "ṣ", "s", "h"]
        self.vowels = ["a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "e", "ai", "o", "au"]

    def test_26_node_linear(self):
        """Doubling the nodes to 26, 2 slots per node."""
        all_chars = self.vowels + [c for v in self.vargas.values() for c in v] + self.nasals + self.semi_vowels + self.sibilants
        node_slots = 26 * 2
        fit_score = len(all_chars) / node_slots
        return {
            "name": "26-Node Linear Expansion",
            "capacity": node_slots,
            "char_count": len(all_chars),
            "fit_ratio": fit_score,
            "description": "Linear expansion to 26 nodes (360/26 deg). Each node has CW/CCW polarity."
        }

    def test_13_node_quadratic(self):
        """13 nodes, but 4 slots per node (Male/Female x Handedness)."""
        # Mapping Sanskrit Varga to Nodes
        # Place of Articulation = Node
        # 4 combinations = Gender/Handedness splits
        varga_nodes = 5 # Nodes 0-4
        nasal_node = 5
        semi_vowel_node = 6
        sibilant_node = 7
        vowel_nodes = [8, 9, 10, 11, 12] # Spread vowels
        
        node_slots = 13 * 4
        all_chars = self.vowels + [c for v in self.vargas.values() for c in v] + self.nasals + self.semi_vowels + self.sibilants
        
        return {
            "name": "13-Node Quadratic (Quadrants)",
            "capacity": node_slots,
            "char_count": len(all_chars),
            "fit_ratio": len(all_chars) / node_slots,
            "description": "Keep 13 nodes (360/13 deg) but add Gender (Voiced/Unvoiced) and Handedness (Asp/Unasp) layers. 4 slots per node."
        }

def run_test():
    tester = SanskritResonanceTester()
    results = [
        tester.test_26_node_linear(),
        tester.test_13_node_quadratic()
    ]
    
    print("--- SANSKRIT CAPACITY TEST: DOUBLING STRATEGIES ---")
    for res in results:
        print(f"\nModel: {res['name']}")
        print(f"  Capacity: {res['capacity']} slots")
        print(f"  Load: {res['char_count']} characters")
        print(f"  Fit Ratio: {res['fit_ratio']*100:.1f}%")
        print(f"  Logic: {res['description']}")

if __name__ == "__main__":
    run_test()
