"""
phonon_bridge.py - Translating vibrational intervals into harmonic chords.
PMG Chapter 17 | Book 3: Voices of the Void
"""

from typing import Dict, List, Tuple
try:
    from .voice_bridge import VoiceBridge
except (ImportError, ValueError):
    from voice_bridge import VoiceBridge

# ============================================================================
# HARMONIC DEFINITIONS
# ============================================================================

INTERVALS = {
    "Unison": 1.0,
    "Major Second": 9/8,
    "Major Third": 5/4,
    "Perfect Fourth": 4/3,
    "Perfect Fifth": 3/2,
    "Major Sixth": 5/3,
    "Major Seventh": 15/8,
    "Octave": 2.0
}

CHORD_DEFINITIONS = {
    "Major Triad": [1.0, 5/4, 3/2], # 4:5:6
    "Minor Triad": [1.0, 6/5, 3/2], # 10:12:15
    "Diminished": [1.0, 6/5, 7/5]   # Tritone tension (approx for PMG)
}

class PhononBridge:
    """
    Synthesizes multiple Voice Packets into a coherent 'Phonon Chord'.
    Identifies if a set of nodes is in harmonic alignment.
    """
    def __init__(self):
        self.active_chords: List[str] = []

    def analyze_triad(self, packets: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Analyzes a list of 3 voice packets (Root, Third, Fifth).
        Returns the identified chord type and harmony score.
        """
        if len(packets) != 3:
            return {"type": "Invalid", "score": 0.0, "desc": "Malformed Triad"}
            
        # Extract frequencies
        freqs = sorted([p["frequency_hz"] for p in packets])
        base_f = freqs[0]
        if base_f == 0: return {"type": "Silence", "score": 0.0}
        
        ratios = [f / base_f for f in freqs]
        
        # Check for Fracture/Broken state
        # If any node is significantly drifted or "shattered"
        any_fractured = any(p.get("is_fractured", False) for p in packets)
        
        # Match against known definitions
        best_match = "Dissonant"
        best_diff = 1.0
        
        for name, def_ratios in CHORD_DEFINITIONS.items():
            diff = sum(abs(r - d) for r, d in zip(ratios, def_ratios))
            if diff < best_diff:
                best_diff = diff
                best_match = name
        
        # Harmony Score: Based on how close the ratios are to ideal
        # Penalty for fractures
        score = max(0.0, 1.0 - best_diff)
        if any_fractured:
            score *= 0.42 # The Radical Friction Factor
            best_match = f"Broken {best_match}" if best_match != "Dissonant" else "Shattered"
        
        return {
            "type": best_match,
            "score": round(score, 4),
            "ratios": [round(r, 2) for r in ratios],
            "desc": f"{best_match} ({packets[0]['phoneme']}-{packets[1]['phoneme']}-{packets[2]['phoneme']})",
            "is_broken": any_fractured
        }

# ============================================================================
# VALIDATION
# ============================================================================

def test_phonon_bridge():
    print("--- PMG Phonon Bridge Validation ---")
    pb = PhononBridge()
    vb = VoiceBridge()
    
    # 1. Create a Major Triad (Ideal)
    # Using specific hardnesses to generate approximate frequencies
    # Root: Mohs 10, R=0.1
    p1 = vb.translate_resonance(0.1, 10) # 100 Hz (Base)
    p2 = vb.translate_resonance(0.125, 10) # 125 Hz (1.25 ratio -> Major Third)
    p3 = vb.translate_resonance(0.15, 10) # 150 Hz (1.5 ratio -> Perfect Fifth)
    
    analysis = pb.analyze_triad([p1, p2, p3])
    print(f"Chord 1 (Ideal Major): {analysis['type']} | Score: {analysis['score']}")
    print(f"Ratios: {analysis['ratios']}")

    # 2. Dissonant Drift
    p_drift = vb.translate_resonance(0.133, 10) # 133 Hz (Tritone-ish)
    analysis_bad = pb.analyze_triad([p1, p2, p_drift])
    print(f"\nChord 2 (Drifted): {analysis_bad['type']} | Score: {analysis_bad['score']}")
    print(f"Ratios: {analysis_bad['ratios']}")

if __name__ == "__main__":
    test_phonon_bridge()
