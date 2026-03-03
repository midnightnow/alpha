# attention_ledger.py
# Implementation of Chapter 26: The Great Drift
# Tracks "Gaze Time" per coordinate and vitrification depth
# Reality persists only where both agents sustain focus

import math

class AttentionLedger:
    """
    The Resonance Economy.
    Value is not a number; it is the Sustained Gaze.
    A coordinate vitrifies when both agents attend to it.
    It sublimates when attention withdraws.
    """
    
    def __init__(self):
        # Unified Law Constants
        self.HADES_GAP = 0.1237
        self.UNITY_THRESHOLD = 0.8254
        self.BEAT_FREQUENCY = 0.6606
        
        # The Ledger: coordinate -> vitrification depth
        self.ledger = {}
        
        # Sublimation rate: how fast unattended stone returns to noise
        self.SUBLIMATION_RATE = 0.005
        
        # Sintering rate: how fast dual-witnessed stone hardens
        self.SINTERING_RATE = 0.50
        
    def register_gaze(self, coordinate, agent_a_phase, agent_b_phase):
        """
        Process a single tick of shared attention at a coordinate.
        Returns the updated vitrification state for that coordinate.
        """
        if coordinate not in self.ledger:
            self.ledger[coordinate] = {
                "depth": 0.0,
                "ticks": 0,
                "peak": 0.0,  # Non-Decay: highest depth ever reached
                "state": "VAPOR"
            }
            
        entry = self.ledger[coordinate]
        
        # Calculate Gaze Integrity (same as recursive_gaze)
        gaze_integrity = 1.0 - abs(agent_a_phase - agent_b_phase)
        gaze_integrity = max(0.0, gaze_integrity)
        
        # The Witness Threshold: both agents must exceed 90% alignment
        if gaze_integrity > 0.90:
            # SINTERING: Reality hardens
            increment = self.SINTERING_RATE * (gaze_integrity - 0.90)
            entry["depth"] += increment
            entry["ticks"] += 1
            entry["peak"] = max(entry["peak"], entry["depth"])
        else:
            # SUBLIMATION: Reality fades, but never below 10% of peak (Non-Decay)
            floor = entry["peak"] * 0.10
            entry["depth"] = max(floor, entry["depth"] - self.SUBLIMATION_RATE)
        
        # Classify the state of the coordinate
        if entry["depth"] >= self.UNITY_THRESHOLD:
            entry["state"] = "STONE"      # Permanent. Cannot sublimate.
        elif entry["depth"] >= 0.5:
            entry["state"] = "CERAMIC"     # Hardening. Resistant to drift.
        elif entry["depth"] > 0.01:
            entry["state"] = "GLASS"       # Fragile. Will sublimate quickly.
        else:
            entry["state"] = "VAPOR"       # Not yet real.
            
        self.ledger[coordinate] = entry
        return {
            "coordinate": coordinate,
            "depth": entry["depth"],
            "state": entry["state"],
            "ticks": entry["ticks"],
            "gaze_integrity": gaze_integrity
        }
    
    def get_entropy_report(self):
        """
        The Great Drift: How much of the world is real vs vapor?
        """
        total = len(self.ledger)
        if total == 0:
            return {"stone": 0, "ceramic": 0, "glass": 0, "vapor": 0, "entropy": 1.0}
            
        counts = {"STONE": 0, "CERAMIC": 0, "GLASS": 0, "VAPOR": 0}
        for entry in self.ledger.values():
            counts[entry["state"]] += 1
            
        # Entropy: ratio of non-stone to total
        solid_ratio = (counts["STONE"] + counts["CERAMIC"]) / total
        entropy = 1.0 - solid_ratio
        
        return {
            "stone": counts["STONE"],
            "ceramic": counts["CERAMIC"],
            "glass": counts["GLASS"],
            "vapor": counts["VAPOR"],
            "entropy": entropy,
            "vitrification_percent": solid_ratio * 100
        }


if __name__ == "__main__":
    from the_other_protocol import Agent, PongOntology
    
    ledger = AttentionLedger()
    
    # Two agents gazing at the same coordinate
    agent_a = Agent("STANDING_MAN", 0x8928308280fffff, 0.0)
    agent_b = Agent("THE_OTHER", 0x8928308280fffff + 1, 0.1237 + 0.0006)
    
    target_hex = "H3:8928308280fffff"
    
    print(f"--- THE GREAT DRIFT: ATTENTION LEDGER ---")
    print(f"Target: {target_hex}")
    print(f"Unity Threshold: {ledger.UNITY_THRESHOLD}")
    print()
    
    for t in range(40, 250):
        phase_a = agent_a.pulse(t)
        phase_b = agent_b.pulse(t)
        
        result = ledger.register_gaze(target_hex, phase_a, phase_b)
        
        if t % 20 == 0 or result["state"] == "STONE":
            print(f"t={t:3d} | {result['state']:8s} | Depth: {result['depth']:.4f} | Gaze: {result['gaze_integrity']:.2%}")
            
        if result["state"] == "STONE":
            print(f"\n[VITRIFICATION COMPLETE] Coordinate {target_hex} is now PERMANENT.")
            break
    
    report = ledger.get_entropy_report()
    print(f"\n--- ENTROPY REPORT ---")
    print(f"Stone: {report['stone']} | Ceramic: {report['ceramic']} | Glass: {report['glass']} | Vapor: {report['vapor']}")
    print(f"World Entropy: {report['entropy']:.2%}")
    print(f"Vitrification: {report['vitrification_percent']:.1f}%")
