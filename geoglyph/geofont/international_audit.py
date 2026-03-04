import numpy as np
import json

class GematriaCompass:
    def __init__(self):
        # Greek Isopsephy
        self.greek_values = {
            'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ζ': 7, 'η': 8, 'θ': 9,
            'ι': 10, 'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70, 'π': 80,
            'ρ': 100, 'σ': 200, 'ς': 200, 'τ': 300, 'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800
        }
        
        # Hebrew Gematria
        self.hebrew_values = {
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
            'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
            'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
        }

        # Latin Simple Cipher (A=1...)
        self.latin_values = {chr(i+97): i+1 for i in range(26)}

        # 13-Node Angles
        self.nodes = 13
        self.angle_step = 360 / self.nodes

    def calculate_gematria(self, text, table):
        total = 0
        for char in text.lower():
            if char in table:
                total += table[char]
        return total

    def map_to_nodes_sequential(self, alphabet, node_count=13):
        # Maps alphabet to nodes (2 chars per node)
        mapping = {}
        for i, char in enumerate(alphabet):
            node = (i // 2) % node_count
            mapping[char] = node
        return mapping

    def analyze_word(self, word, value_table, node_mapping):
        node_indices = []
        values = []
        for char in word.lower():
            if char in node_mapping:
                node_indices.append(node_mapping[char])
            if char in value_table:
                values.append(value_table[char])
        
        # Calculate Angular Centroid
        angles = [idx * self.angle_step for idx in node_indices]
        rads = np.deg2rad(angles)
        x = np.cos(rads)
        y = np.sin(rads)
        
        if len(node_indices) == 0:
            return None
            
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        centroid_angle = np.rad2deg(np.arctan2(mean_y, mean_x)) % 360
        magnitude = np.sqrt(mean_x**2 + mean_y**2) # 1.0 = highly centered in one direction, 0.0 = balanced
        
        return {
            "gematria": sum(values),
            "nodes": node_indices,
            "centroid_angle": round(centroid_angle, 2),
            "coherence": round(magnitude, 4)
        }

def run_investigation():
    gc = GematriaCompass()
    
    # 1. Greek "Jesus Christ"
    greek_alphabet = "αβγδεζηθικλμνξοπρστυφχψω"
    greek_nodes = gc.map_to_nodes_sequential(greek_alphabet)
    # Note: σ and ς are the same value, usually σ is used.
    jesous = "ιησους"
    christos = "χριστος"
    greek_result = gc.analyze_word(jesous + christos, gc.greek_values, greek_nodes)
    
    # 2. Hebrew "Yehoshua HaMashiach" (from user's image)
    hebrew_alphabet = "אבגדהוזחטיכלמנסעפצקרשת"
    hebrew_nodes = gc.map_to_nodes_sequential(hebrew_alphabet)
    yehoshua = "יהושע"
    hamashiach = "המשיח"
    hebrew_result = gc.analyze_word(yehoshua + hamashiach, gc.hebrew_values, hebrew_nodes)
    
    print("--- INTERNATIONAL GEMATRIA AUDIT ---")
    print(f"Greek 'Iesous Christos':")
    print(f"  Gematria: {greek_result['gematria']}")
    print(f"  Nodes: {greek_result['nodes']}")
    print(f"  Centroid Angle: {greek_result['centroid_angle']}°")
    print(f"  Coherence: {greek_result['coherence']}")
    
    print(f"\nHebrew 'Yehoshua HaMashiach':")
    print(f"  Gematria: {hebrew_result['gematria']}")
    print(f"  Nodes: {hebrew_result['nodes']}")
    print(f"  Centroid Angle: {hebrew_result['centroid_angle']}°")
    print(f"  Coherence: {hebrew_result['coherence']}")
    
    if greek_result['gematria'] > 0 and hebrew_result['gematria'] > 0:
        ratio = greek_result['gematria'] / hebrew_result['gematria']
        print(f"\nRatio (Greek/Hebrew): {ratio:.5f}")
        print(f"Difference from Pi: {abs(ratio - np.pi):.5f}")

    # Sanskrit effort (limited)
    # Sanskrit uses Katapayadi for numbers, but alpha-node mapping is harder due to size.
    print("\nSanskrit Status: Limited Effort.")
    print("  Challenge: Alphabet size (50+) exceeds 13-node container (max 26 slots at 2/node).")
    print("  Correlation check: Sanskrit 'Ishvara' or 'Shiva' values to be explored.")

if __name__ == "__main__":
    run_investigation()
