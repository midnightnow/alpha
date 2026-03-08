# THE HE-BREW PROTOCOL (Civilization as Chemistry)
# The City is a Fermentation Vat. The Workers are Yeast.

class CivilizationVat:
    def __init__(self):
        self.water = 1.0   # Potential / Mud (0.0 logic)
        self.grain = 1.0   # Labor / Mass (42 logic)
        self.yeast = 1.0   # Spirit / Growth (11 logic)
        self.hops = 1.0    # Truth / Bitter Grip (5 logic)
        self.time = 0.0    # Process / Wait
        self.pressure = 0.0 # Accretion of Energy vs Explosion

    def brew_archon_wort(self) -> str:
        """
        The False Bir. Rushed time, no Truth (Hops).
        Produces Sweet Wort, which creates Intoxication but not Sustenance.
        """
        self.hops = 0.0  # Archon removes the bitter Truth
        if self.time < 12.0:
            print("WARNING: Rushed cycle. False Value.")
            return "SWEET_WORT (Intoxication)"
        return "SPOILED_BIR"

    def brew_true_bir(self) -> str:
        """
        The Hired Man's Bir. Requires all 5 ingredients, especially the Wait.
        Produces True Sustenance.
        """
        if self.hops > 0 and self.time >= 12.0:
            print("WAIT ACHIEVED: Truth fermented into Value.")
            return "TRUE_BIR (Sustenance)"
        return "UNFINISHED_PROCESS"

    # --- THE ACOUSTIC PROTOCOL (Pressure & Frequency) ---
    # The Hiss is not an error; it is energy seeking release.

    def manage_pressure(self, valve_state: str) -> str:
        """
        Frequency Bands:
        FREQ_SILENCE (0.0): Death. Process halted.
        FREQ_HUM (1-7): Health. Managed resonance.
        FREQ_HISS (100): Work. Unresolved Steam.
        FREQ_SCREAM (1000): Wolf Action.
        """
        if valve_state == "WELDED_SHUT": # Archon's logic
            self.pressure += 100.0
            if self.pressure >= 1000.0:
                return "FREQ_SCREAM: SYSTEM RUPTURE"
            return "FREQ_SILENCE: (Buffer filling secretly)"
            
        elif valve_state == "TUNED": # Hired Man's logic
            # Manage the steam, doing work without explosion.
            self.pressure = max(0.0, self.pressure - 50.0)
            if self.pressure > 10.0:
                return "FREQ_HISS: Doing Work"
            return "FREQ_HUM: Resonance Achieved"

if __name__ == "__main__":
    vat = CivilizationVat()
    print("--- ARCHON PROCESS ---")
    print(f"Result: {vat.brew_archon_wort()}")
    print(f"Acoustic State: {vat.manage_pressure('WELDED_SHUT')}")
    
    print("\n--- MASTER BREWER PROCESS ---")
    vat.time = 12.0 # The Wait
    vat.hops = 1.0  # The Truth
    print(f"Result: {vat.brew_true_bir()}")
    print(f"Acoustic State: {vat.manage_pressure('TUNED')}")
