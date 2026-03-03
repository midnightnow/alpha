import sys
import re
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../Code/ophanim_toolkit'))
from lexical_geometry import LexicalGeometer

def audit_narrative_bridge(filepath):
    print(f"Executing Acoustic Bridge Audit on: {os.path.basename(filepath)}")
    with open(filepath, 'r') as f:
        text = f.read()

    words = re.findall(r'\b[A-Za-z]+\b', text.lower())
    if not words:
        print("VOID - No data.")
        return

    # Total phonemes
    total_phonemes = sum(len(w) for w in words)

    # Node 9 (Hiss / Mist)
    sibilants = ['s', 'sh', 'th', 'f', 'v', 'z', 'ch']
    hiss_count = 0
    for w in words:
        for p in sibilants:
            hiss_count += w.count(p)

    hiss_ratio = hiss_count / total_phonemes if total_phonemes else 0

    # Node 0 (Bone Density - Structure / Plosives / Gutturals)
    bone_phonemes = ['b', 'c', 'd', 'g', 'k', 'p', 't', 'q']
    bone_count = sum(sum(w.count(p) for p in bone_phonemes) for w in words)
    bone_ratio = bone_count / total_phonemes if total_phonemes else 0

    print("==================================================")
    print("BRIDGE ABLATION STATUS")
    print("==================================================")
    print(f"Hiss Migration (Node 9 Sibilance): {hiss_ratio:.4%} (Target: ~12-13%)")
    print(f"Bone Density (Node 0 Structure): {bone_ratio:.4%} (Threshold: >25%)")
    
    geometer = LexicalGeometer()
    lock_data = geometer.audit_h4_alphabet_lock(text)
    
    print("\n--- BASE H(4) LOCK DATA ---")
    print(f"Geometric Divergence: {lock_data['geometric_divergence']}")
    print(f"Base Ratio: {lock_data['base_ratio']} (Ideal: 0.615)")
    print(f"Sym Ratio: {lock_data['sym_ratio']} (Ideal: 0.269)")
    print(f"Pillar Ratio: {lock_data['pillar_ratio']} (Ideal: 0.115)")
    print(f"Mastery Scale Target: {lock_data['mastery_scale_target']}")
    print(f"Alphabet Lock Status: {lock_data['alphabet_lock_status']}")
    
    print("\n==================================================")
    
    hiss_ok = 0.10 <= hiss_ratio <= 0.15 # Acceptable slow climb range
    bone_ok = bone_ratio >= 0.25
    
    if hiss_ok and bone_ok:
        print("BRIDGE STATUS: STABLE. No Ablation Required.")
    else:
        print("BRIDGE STATUS: UNSTABLE. Ablation/Refinement Recommended.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES/Books/Book_5_The_Transfinite_Horizon/Chapter_4_The_7th_Symmetry.md'
    audit_narrative_bridge(target)
