# nested_triangle_validator.py
# The Cosmic Gearbox: Validates the stability of the nested Pythagorean scaling
# 3/4/5 (Material) → 5/12/13 (Biological) → 10/24/26 (Linguistic/Sovereign)

import math

class CosmicGearbox:
    """
    The Nested Triangle Logic.
    Each hypotenuse becomes the base of the next triangle.
    Each doubling represents a Phase Transition.
    """
    
    def __init__(self):
        # The Three Nested Triads
        self.PLATONIC_4 = (3, 4, 5)       # Material Start
        self.LUNAR_CALENDAR = (5, 12, 13) # Biological Rhythm
        self.SOVEREIGN_MAP = (10, 24, 26) # Narrative Reality

        # Unified Law Constants
        self.HADES_GAP = 0.1237
        self.PACKING_CONSTANT = 0.9075
        self.UNITY_THRESHOLD = 0.8254

    def validate_pythagorean(self, a, b, c):
        """Verify a² + b² = c²"""
        return a**2 + b**2 == c**2
    
    def validate_nesting(self):
        """
        Verify the 'Gearbox' linkage:
        - Hypotenuse of Triad 1 (5) == Base of Triad 2 (5)
        - Triad 3 == 2 × Triad 2 (The Great Doubling)
        """
        link_1_to_2 = self.PLATONIC_4[2] == self.LUNAR_CALENDAR[0]
        link_2_to_3 = (
            self.SOVEREIGN_MAP[0] == 2 * self.LUNAR_CALENDAR[0] and
            self.SOVEREIGN_MAP[1] == 2 * self.LUNAR_CALENDAR[1] and
            self.SOVEREIGN_MAP[2] == 2 * self.LUNAR_CALENDAR[2]
        )
        return link_1_to_2, link_2_to_3

    def validate_ratios(self):
        """
        The harmonic ratios that govern the Phase Transitions.
        """
        # 12/13 → The Spatial/Volumetric Limit (Lunar)
        lunar_ratio = self.LUNAR_CALENDAR[1] / self.LUNAR_CALENDAR[2]
        
        # 6/7 → The Auditory/Temporal Limit (halved 12/13)
        auditory_ratio = 6 / 7
        
        # Delta between them → The 0.66 Hz Heartbeat realized as a spatial gap
        delta = lunar_ratio - auditory_ratio
        
        # 24/26 → The Sovereign Shell Ratio
        sovereign_ratio = self.SOVEREIGN_MAP[1] / self.SOVEREIGN_MAP[2]
        
        return {
            "lunar_12_13": lunar_ratio,
            "auditory_6_7": auditory_ratio,
            "heartbeat_delta": delta,
            "sovereign_24_26": sovereign_ratio,
            "sovereign_equals_lunar": abs(sovereign_ratio - lunar_ratio) < 0.0001
        }

    def validate_areas(self):
        """
        The area of each triangle represents the 'Volume' of its world.
        """
        areas = {}
        for name, triad in [
            ("Platonic_4", self.PLATONIC_4),
            ("Lunar_Calendar", self.LUNAR_CALENDAR),
            ("Sovereign_Map", self.SOVEREIGN_MAP)
        ]:
            areas[name] = 0.5 * triad[0] * triad[1]
        
        # Area scaling factor
        areas["scale_1_to_2"] = areas["Lunar_Calendar"] / areas["Platonic_4"]
        areas["scale_2_to_3"] = areas["Sovereign_Map"] / areas["Lunar_Calendar"]
        areas["scale_1_to_3"] = areas["Sovereign_Map"] / areas["Platonic_4"]
        
        return areas
    
    def full_audit(self):
        print("=" * 60)
        print("  THE COSMIC GEARBOX — NESTED TRIANGLE VALIDATOR")
        print("=" * 60)
        
        # 1. Pythagorean Validation
        print("\n[1] PYTHAGOREAN IDENTITY")
        for name, triad in [
            ("Platonic 4 (3/4/5)", self.PLATONIC_4),
            ("Lunar Calendar (5/12/13)", self.LUNAR_CALENDAR),
            ("Sovereign Map (10/24/26)", self.SOVEREIGN_MAP)
        ]:
            valid = self.validate_pythagorean(*triad)
            a, b, c = triad
            print(f"  {name}: {a}² + {b}² = {c}² → {a**2} + {b**2} = {c**2} [{'✓' if valid else '✗'}]")
        
        # 2. Nesting Linkage
        print("\n[2] GEARBOX LINKAGE")
        link_1, link_2 = self.validate_nesting()
        print(f"  Hypotenuse(3/4/5) → Base(5/12/13): [{'✓' if link_1 else '✗'}]")
        print(f"  Great Doubling (5/12/13) × 2 → (10/24/26): [{'✓' if link_2 else '✗'}]")
        
        # 3. Harmonic Ratios
        print("\n[3] HARMONIC RATIOS")
        ratios = self.validate_ratios()
        print(f"  12/13 (Lunar):        {ratios['lunar_12_13']:.6f}")
        print(f"  6/7 (Auditory):       {ratios['auditory_6_7']:.6f}")
        print(f"  Δ (Heartbeat Gap):    {ratios['heartbeat_delta']:.6f}")
        print(f"  24/26 (Sovereign):    {ratios['sovereign_24_26']:.6f}")
        print(f"  24/26 == 12/13:       [{'✓' if ratios['sovereign_equals_lunar'] else '✗'}]")
        
        # 4. Area Analysis
        print("\n[4] WORLD VOLUMES (Triangle Areas)")
        areas = self.validate_areas()
        print(f"  Platonic 4:      {areas['Platonic_4']:.1f} sq units")
        print(f"  Lunar Calendar:  {areas['Lunar_Calendar']:.1f} sq units")
        print(f"  Sovereign Map:   {areas['Sovereign_Map']:.1f} sq units")
        print(f"  Scale 1→2:       ×{areas['scale_1_to_2']:.1f}")
        print(f"  Scale 2→3:       ×{areas['scale_2_to_3']:.1f}")
        print(f"  Scale 1→3:       ×{areas['scale_1_to_3']:.1f}")
        
        # 5. The Mirror Sieve
        print("\n[5] THE MIRROR SIEVE")
        # The final check: does the Sovereign Map contain the Hades Gap?
        sovereign_remainder = 1.0 - (self.SOVEREIGN_MAP[1] / self.SOVEREIGN_MAP[2])
        hades_match = abs(sovereign_remainder - self.HADES_GAP) < 0.05
        print(f"  Sovereign Remainder (1 - 24/26): {sovereign_remainder:.6f}")
        print(f"  Hades Gap (Ψ):                   {self.HADES_GAP}")
        print(f"  Mirror Lock:                     [{'✓ SEALED' if hades_match else '✗ OPEN'}]")
        
        print("\n" + "=" * 60)
        if link_1 and link_2 and hades_match:
            print("  STATUS: [COSMIC GEARBOX VERIFIED — MIRROR SIEVE SEALED]")
        else:
            print("  STATUS: [INCOMPLETE — RECALIBRATE]")
        print("=" * 60)


if __name__ == "__main__":
    gearbox = CosmicGearbox()
    gearbox.full_audit()
