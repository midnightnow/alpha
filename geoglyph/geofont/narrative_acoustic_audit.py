import json
import re
import sys

# LATTICE CONSTANT
LATTICE_FREQ = 66.0688

# IPA Mapping from our audit
IPA_RESONANCE = {
    'n': 0.9457, 't': 0.9457, 'a': 0.7308, 'h': 0.7285, 'b': 0.6326,
    'r': 0.6222, 'o': 0.6222, 'g': 0.5679, 'm': 0.4593, 'd': 0.4489,
    'u': 0.4050, 'l': 0.4050, 'f': 0.1856, 's': 0.0859, 'k': 0.0814,
    'i': 0.0814, 'e': 0.1357, 'p': 0.0271, 'v': 0.1313, 'z': 0.1402
}

PROXY_MAP = {
    'c': 'k', 'j': 'i', 'q': 'k', 'w': 'u', 'x': 'k', 'y': 'i'
}

NODE_MAP = {
    'n': 0, 'd': 0, 'l': 0, 'r': 0,
    's': 9, 'z': 9, 't': 9,
    'p': 7, 'b': 7, 'm': 7,
    'o': 6, 'a': 6, 'e': 6, 'i': 6, 'u': 6,
    'k': 3, 'g': 3,
    'h': 4,
    'f': 10, 'v': 10
}

def analyze_text(filepath):
    try:
        with open(filepath, 'r') as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    # Clean text to symbols
    words = re.findall(r'[a-z]+', text)
    full_str = "".join(words)
    
    char_scores = []
    node_distribution = {i: 0 for i in range(13)}
    
    total_chars = 0
    for char in full_str:
        target = PROXY_MAP.get(char, char)
        if target in IPA_RESONANCE:
            score = IPA_RESONANCE[target]
            char_scores.append(score)
            node = NODE_MAP.get(target, 6) # Default to central
            node_distribution[node] += 1
            total_chars += 1

    avg_resonance = sum(char_scores) / len(char_scores) if char_scores else 0
    sorted_nodes = sorted(node_distribution.items(), key=lambda x: x[1], reverse=True)
    
    # Analyze user targets: /m, b, p/ (currently Node 7) and Node 9
    node_7_hits = node_distribution[7]
    node_9_hits = node_distribution[9]
    node_4_hits = node_distribution[4]
    
    print(f"--- ACOUSTIC AUDIT: {filepath.split('/')[-1]} ---")
    print(f"Aggregate Resonance: {avg_resonance*100:>.2f}%")
    print(f"Total Resonant Tokens: {total_chars}")
    print("\nNodal Dominance (Top 5):")
    for node, count in sorted_nodes[:5]:
        percent = (count / total_chars) * 100
        print(f"Node {node}: {percent:>.2f}% ({count} hits)")
    
    print(f"\n--- USER CALIBRATION CHECK ---")
    print(f"Node 7 (Anchor - /m,b,p/): {(node_7_hits/total_chars)*100:>.2f}%")
    print(f"Node 9 (Turbine - /s,t,z/): {(node_9_hits/total_chars)*100:>.2f}%")
    print(f"Node 4 (Breath Gate - /h/): {(node_4_hits/total_chars)*100:>.2f}%")
    
    if (node_9_hits/total_chars) > 0.12:
        print("⚠️ WARNING: Node 9 exceeds 12% limit.")
    else:
        print("✅ Node 9 is within 12% limit.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_text(sys.argv[1])
    else:
        analyze_text("/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES/Books/Book_5_The_Transfinite_Horizon/Chapter_1_The_Nomad_of_the_Aleph.md")
