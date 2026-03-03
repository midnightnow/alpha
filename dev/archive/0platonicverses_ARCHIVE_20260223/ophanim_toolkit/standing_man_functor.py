"""
STANDING MAN FUNCTOR — categorical_unification.py
Validates the Natural Transformation between Verses, Vectors, and Voices.
The identity arrow of the PMG system.
"""

import math
try:
    from .e8_hades_validator import PMGConstants
except (ImportError, ValueError):
    from e8_hades_validator import PMGConstants

class StandingManFunctor:
    """
    The Identity Functor Id: C -> C that maps Geometric Objects to Acoustic Morphisms.
    Ensures that every resonance is a morphism and every silence is a gate.
    """
    def __init__(self):
        # Canonical Constants (Ref: CONSTANTS_CANON.md)
        self.constants = PMGConstants()
        self.PRIME_17 = self.constants.PRIME_INTRUSION
        self.SHEAR_ANGLE = self.constants.SHEAR_ANGLE_DEG
        self.HADES_BEAT = self.constants.BEAT_FREQUENCY
        self.HADES_GAP = self.constants.HADES_GAP
        
    def map_vector_to_voice(self, vector_magnitude, rotation_angle):
        """
        Morphism: G (Geometry) -> S (Sound)
        """
        # A rotation of 39.4725 degrees induces an acoustic phase shift
        shear_precision = abs(rotation_angle - self.SHEAR_ANGLE)
        
        # The phonetic intensity is a function of the vector vs the prime 17 anchor
        intensity = vector_magnitude / self.PRIME_17
        
        # Return the resulting Voice Frequency
        # The base frequency (66.0) modulated by the shear precision
        freq = 66.0 * (1.0 - (shear_precision / 360.0))
        
        return {
            "frequency_hz": freq,
            "resonance_score": 1.0 - (shear_precision / self.SHEAR_ANGLE),
            "hades_active": shear_precision < self.HADES_GAP
        }

    def standing_wave_check(self, pulse_rate):
        """
        Natural Transformation: Ensures the observer (Standing Man) 
        is phase-locked to the system heartbeat.
        """
        drift = abs(pulse_rate - self.HADES_BEAT)
        is_locked = drift < 0.001
        
        return {
            "drift": drift,
            "is_functorial": is_locked,
            "state": "OBSIDIAN" if is_locked else "CLAY"
        }

if __name__ == "__main__":
    functor = StandingManFunctor()
    
    print("--- PMG STANDING MAN FUNCTOR SIMULATION ---")
    
    # Simulate a user intent: rotating toward the shear anchor
    morphism = functor.map_vector_to_voice(17.0, 39.4725)
    print(f"Morphism G->S: Freq={morphism['frequency_hz']:.4f}Hz | Res={morphism['resonance_score']:.2%}")
    
    # Check for category closure
    status = functor.standing_wave_check(0.660688)
    print(f"Category Closure: {'✓ COMPLETE' if status['is_functorial'] else '✗ DIVERGENT'}")
    print(f"Final Invariant: {status['state']}")
