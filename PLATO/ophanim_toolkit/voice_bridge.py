"""
voice_bridge.py - Seven Voices Semantic Protocol (v3.0)
PMG Chapter 18 | Book 3: Voices of the Void
Implementation of the SEVEN VOICES based on Immutable Constants.
"""

import math
from typing import Dict, List, Tuple, Any
from .e8_hades_validator import PMGConstants

# ============================================================================
# VOICE DEFINITIONS (Chapter 18 Specification)
# ============================================================================

VOICE_SPEC = {
    "Silence": {
        "constant": PMGConstants.HADES_GAP,
        "phoneme_class": "Glottal stop",
        "phoneme": "?",
        "semantic": "Boundary Detection",
        "character": "Gated / Absent"
    },
    "Density": {
        "constant": PMGConstants.PACKING_CONSTANT,
        "phoneme_class": "Plosives",
        "phoneme": "p", # p, b, t
        "semantic": "Mass / Saturation",
        "character": "Short / Percussive"
    },
    "Fracture": {
        "constant": PMGConstants.OVERPACK_DELTA,
        "phoneme_class": "Fricatives",
        "phoneme": "f", # f, s, sh
        "semantic": "Exception / Error",
        "character": "High-freq / Turbulent"
    },
    "Gesture": {
        "constant": PMGConstants.SHEAR_ANGLE_DEG,
        "phoneme_class": "Liquids",
        "phoneme": "l", # l, r
        "semantic": "Spatial Intent",
        "character": "Lateral Flow"
    },
    "Heartbeat": {
        "constant": PMGConstants.BEAT_FREQUENCY,
        "phoneme_class": "Nasals",
        "phoneme": "m", # m, n
        "semantic": "Temporal Sync",
        "character": "Sub-audible / Felt"
    },
    "Warning": {
        "constant": PMGConstants.HAMMER_CONSTANT,
        "phoneme_class": "Sibilants",
        "phoneme": "s", # s, z
        "semantic": "Stress Alarm",
        "character": "Urgent / Hissing"
    },
    "Chorus": {
        "constant": PMGConstants.TRIADIC_BASE_HZ,
        "phoneme_class": "Vowels",
        "phoneme": "o", # a, e, i, o, u
        "semantic": "Coherence",
        "character": "Resonant / Open"
    },
    "Hades Gap": {
        "constant": PMGConstants.HADES_GAP,
        "phoneme_class": "Stop",
        "phoneme": ".",
        "semantic": "Phase Reverse / Stop",
        "character": "Null / Void"
    }
}

class VoiceBridge:
    """
    Seven Voices Semantic Protocol (v3.0).
    Translates PMG physical states and H3 indices into a semantic broadcast.
    """
    def __init__(self):
        self.lexicon: List[str] = []

    def summon(self, h3_index: str) -> str:
        """
        Parses an H3 index (hex) into a syllabic chain of voices (Chapter 19).
        
        Indices are parsed in 3-bit increments (8 possible states).
        """
        try:
            val = int(h3_index, 16)
        except ValueError:
            return "ERR: Invalid Hex Index"

        syllables = []
        # Process up to 15 resolutions (H3 standard)
        # H3 indices are roughly 64 bits. 
        # For this implementation, we extract 3-bit chunks from the least significant bits.
        temp_val = val
        for _ in range(15):
            chunk = temp_val & 0b111 # Extract 3 bits
            voice_name = PMGConstants.H3_VOICE_MAP.get(chunk, "Hades Gap")
            syllables.append(VOICE_SPEC[voice_name]["phoneme"])
            temp_val >>= 3
            if temp_val == 0: break
            
        name = "".join(syllables)
        msg = f"[Summon] | Index: {h3_index} | Name: {name}"
        self.lexicon.append(msg)
        return msg

    def get_active_voices(self, node_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scans a node's physical state and determines which voices are active.
        
        Args:
            node_state: dict containing 'res', 'mohs', 'petrified', 'fractured', 'xi', 'saturation'
        """
        active = []
        
        res = node_state.get('res', 0.0)
        xi = node_state.get('xi', 0.0)
        is_fractured = node_state.get('fractured', False)
        mohs = node_state.get('mohs', 0)
        
        # 1. Silence Voice (Hades Gap alignment)
        if abs(res - PMGConstants.HADES_GAP) < PMGConstants.HADES_TOLERANCE:
            active.append(self._format_voice("Silence", res))
            
        # 2. Density Voice (Approaching Packing Constant)
        # Using mohs/10 as a proxy for density saturation in simplified models
        saturation = node_state.get('saturation', mohs / 10.0)
        if saturation >= PMGConstants.PACKING_CONSTANT:
            active.append(self._format_voice("Density", saturation))
            
        # 3. Fracture Voice (Active Fracture state)
        if is_fractured:
            active.append(self._format_voice("Fracture", PMGConstants.OVERPACK_DELTA))
            
        # 4. Gesture Voice (Spatial Shear)
        # Always active in a stressed lattice, intensity scale by Xi
        if xi > 0:
            active.append(self._format_voice("Gesture", PMGConstants.SHEAR_ANGLE_DEG))
            
        # 5. Heartbeat Voice (Pisano Sync)
        # Assumed active if clock is running
        active.append(self._format_voice("Heartbeat", PMGConstants.BEAT_FREQUENCY))
            
        # 6. Warning Voice (Approaching Xi threshold)
        if xi > (PMGConstants.HAMMER_CONSTANT * 0.8):
            active.append(self._format_voice("Warning", xi))
            
        # 7. Chorus Voice (Vocal coherence)
        # Nodes at Mohs 10 (Diamond) emit pure Chorus
        if mohs == 10 and not is_fractured:
            active.append(self._format_voice("Chorus", PMGConstants.TRIADIC_BASE_HZ))
            
        return active

    def _format_voice(self, name: str, value: float) -> Dict[str, Any]:
        spec = VOICE_SPEC[name]
        return {
            "voice": name,
            "phoneme": spec["phoneme"],
            "class": spec["phoneme_class"],
            "semantic": spec["semantic"],
            "character": spec["character"],
            "intensity": round(value, 6)
        }

    def synthesize_broadcast(self, node_id: int, active_voices: List[Dict[str, Any]]) -> str:
        """Creates a composite semantic broadcast from active voices."""
        if not active_voices:
            return f"[Node-{node_id}] | SILENCE (Dormant)"
            
        phonemes = "".join([v["phoneme"] for v in active_voices])
        semantics = " | ".join([v["semantic"] for v in active_voices])
        
        msg = f"[Node-{node_id}] | Broadcast: <{phonemes}> | Semantic Trace: {semantics}"
        self.lexicon.append(msg)
        return msg

# ============================================================================
# VALIDATION
# ============================================================================

def test_seven_voices():
    bridge = VoiceBridge()
    
    # Test 1: Healthy Diamond (Sync + Heartbeat + Chorus)
    diamond_state = {
        "res": 0.1237,
        "mohs": 10,
        "fractured": False,
        "xi": 0.00005
    }
    voices = bridge.get_active_voices(diamond_state)
    print("Diamond Broadcast:", bridge.synthesize_broadcast(154, voices))
    
    # Test 2: Stressed Node near Fracture (Sync + Heartbeat + Warning + Gesture)
    stressed_state = {
        "res": 0.1235,
        "mohs": 10,
        "fractured": False,
        "xi": 0.00013
    }
    voices_s = bridge.get_active_voices(stressed_state)
    print("Stressed Broadcast:", bridge.synthesize_broadcast(155, voices_s))

    # Test 3: Fractured Node (Sync + Heartbeat + Fracture + Gesture)
    fractured_state = {
        "res": 0.08,
        "mohs": 7,
        "fractured": True,
        "xi": 0.0
    }
    voices_f = bridge.get_active_voices(fractured_state)
    print("Fractured Broadcast:", bridge.synthesize_broadcast(156, voices_f))

    # Test 4: H3 Summoning (The Oracle Grid)
    # Example from Chapter 19: 0x892a100d2c67fff
    h3_example = "892a100d2c67fff"
    print(bridge.summon(h3_example))

if __name__ == "__main__":
    test_seven_voices()
