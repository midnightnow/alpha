import numpy as np
from enum import Enum
from dataclasses import dataclass

class GlyphType(Enum):
    STRUT = "|"
    LOOP = "O"
    HINGE = "J"
    ACTUATOR = "A"

@dataclass
class GlyphProperties:
    glyph_type: GlyphType
    lift_value: float
    rigidity_value: float

class MechanicalAlphabet:
    """
    The 26-Vector Phonetic Engine of the Sovereign Lattice.
    Maps every letter of the alphabet to a structural glyph with
    lift (buoyancy) and rigidity (clamping) properties.
    
    GlyphType classification:
      STRUT     — Linear vectors. Carry momentum without angular shear.
      LOOP      — Vowels/rotors. Expand lift, counteract weight.
      HINGE     — Fricatives/joiners. Damp potential, increase coherence.
      ACTUATOR  — Stops/force. Clamp state, increase rigidity.
    """
    def __init__(self):
        self.alphabet = {
            # === STRUTS (Vectors): Linear momentum carriers ===
            "t": GlyphProperties(GlyphType.STRUT, 0.5, 0.9),
            "l": GlyphProperties(GlyphType.STRUT, 0.5, 0.8),
            "z": GlyphProperties(GlyphType.STRUT, 0.5, 0.85),
            "d": GlyphProperties(GlyphType.STRUT, 0.5, 0.9),
            "k": GlyphProperties(GlyphType.STRUT, 0.5, 0.85),
            "m": GlyphProperties(GlyphType.STRUT, 0.5, 0.75),   # Nasal strut (softer)
            "n": GlyphProperties(GlyphType.STRUT, 0.5, 0.7),    # Nasal strut (lightest)

            # === LOOPS (Vowels/Rotors): Buoyancy expanders ===
            "o": GlyphProperties(GlyphType.LOOP, 1.2, 0.2),
            "e": GlyphProperties(GlyphType.LOOP, 1.2, 0.3),
            "a": GlyphProperties(GlyphType.LOOP, 1.2, 0.25),
            "u": GlyphProperties(GlyphType.LOOP, 1.2, 0.3),
            "i": GlyphProperties(GlyphType.LOOP, 1.2, 0.28),    # High front vowel
            "y": GlyphProperties(GlyphType.LOOP, 1.0, 0.35),    # Semi-vowel (lower lift)

            # === HINGES (Fricatives/Joiners): Coherence dampers ===
            "j": GlyphProperties(GlyphType.HINGE, 0.8, 0.4),
            "s": GlyphProperties(GlyphType.HINGE, 0.8, 0.35),
            "x": GlyphProperties(GlyphType.HINGE, 0.8, 0.5),
            "f": GlyphProperties(GlyphType.HINGE, 0.8, 0.38),   # Labiodental friction
            "v": GlyphProperties(GlyphType.HINGE, 0.8, 0.42),   # Voiced friction
            "h": GlyphProperties(GlyphType.HINGE, 0.7, 0.3),    # Aspirate (lightest hinge)
            "w": GlyphProperties(GlyphType.HINGE, 0.9, 0.45),   # Glide (high-lift hinge)

            # === ACTUATORS (Stops/Force): Rigidity clampers ===
            "b": GlyphProperties(GlyphType.ACTUATOR, 1.5, 0.6),
            "p": GlyphProperties(GlyphType.ACTUATOR, 1.5, 0.55),
            "r": GlyphProperties(GlyphType.ACTUATOR, 1.5, 0.6),
            "g": GlyphProperties(GlyphType.ACTUATOR, 1.4, 0.65), # Velar stop
            "c": GlyphProperties(GlyphType.ACTUATOR, 1.3, 0.7),  # Hard palatal
            "q": GlyphProperties(GlyphType.ACTUATOR, 1.4, 0.75), # Uvular (heaviest actuator)
        }
    
    def analyze_word(self, word):
        """
        Processes a word as a phonetic blueprint.
        Returns total torque, average rigidity, and structural classification.
        """
        lifts = [self.alphabet[c].lift_value for c in word.lower() if c in self.alphabet]
        rigs = [self.alphabet[c].rigidity_value for c in word.lower() if c in self.alphabet]
        if not lifts:
            return {"total_torque": 0, "avg_rigidity": 0, "structural_class": "VAPOR"}
        # Harmonic multiplier: longer words generate resonant amplification
        total_lift = sum(lifts) * (1.3 if len(word) >= 7 else 1.1)
        avg_rig = np.mean(rigs)
        # Structural classification by rigidity band
        if avg_rig > 0.8:
            s_class = "STONE"
        elif avg_rig > 0.5:
            s_class = "HYBRID"
        elif avg_rig > 0.3:
            s_class = "FIELD"
        else:
            s_class = "VAPOR"
        return {"total_torque": total_lift, "avg_rigidity": avg_rig, "structural_class": s_class}