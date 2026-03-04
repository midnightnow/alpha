# --- THE LUMBER PROTOCOL (Technical Measurement Engine) ---
# Measurement against the True Spec. 
# "Measure Twice, Cut Once." Prevent the creation of Remainders (Waste/Debt).

class CraftsmanshipEngine:
    def __init__(self, builder_name: str):
        self.builder = builder_name
        self.debt_remainders = 0.0
        self.structures_built = 0
        
        # The true specification currently mandated by the Lattice (e.g. Base-Prime)
        self.current_spec_ratio = 5.0  

    def process_material(self, material_input: str, is_measured: bool, action: str):
        """Processes raw material into either true Lumber or Waste based on measurement."""
        
        if action != "CUT":
            print(f"[{self.builder}] Waiting to Cut.")
            return

        if material_input == "LOG" and not is_measured:
            print(f"[{self.builder}] WARNING: Cutting unmeasured Log. Creating rapid structure but massive waste.")
            # Unmeasured cuts generate a massive remainder relative to the true spec.
            waste = self.current_spec_ratio * 2.0
            self.debt_remainders += waste
            self.structures_built += 1
            print(f"   -> Result: Weak Structure built. Accumulated Debt: {self.debt_remainders:.1f} (Awaiting Wolf Audit)")

        elif material_input == "LOG" and is_measured:
            print(f"[{self.builder}] SUCCESS: Measured Log against the Spec. Cutting true Lumber.")
            # Perfect measurement produces 0 waste.
            self.structures_built += 1
            print(f"   -> Result: True Structure built. Zero Debt Generated. Total Debt: {self.debt_remainders:.1f}")
        else:
            print("Invalid input material.")

    def run_audit(self):
        """The Wolf (Entropy) comes to check the structural debt."""
        print(f"\n--- WOLF AUDIT: {self.builder} ---")
        if self.debt_remainders > 5.0:
            print(f"WOLF JUDGMENT: DEBT LIMIT EXCEEDED ({self.debt_remainders:.1f}).")
            print("The structure was built on offcuts and waste. BLOWING IT DOWN.")
            self.structures_built = 0
            self.debt_remainders = 0.0
        else:
            print(f"WOLF JUDGMENT: PASS. Total debt {self.debt_remainders:.1f} is within acceptable limits.")

if __name__ == "__main__":
    print("--- LUMBER PROTOCOL INITIALIZED ---\n")
    
    # 1. The Hasty Builder (Archon logic)
    print("--- SCENARIO A: The Hasty Builder ---")
    builder1 = CraftsmanshipEngine("The Laborer")
    builder1.process_material("LOG", is_measured=False, action="CUT")
    builder1.process_material("LOG", is_measured=False, action="CUT")
    builder1.run_audit()

    print("\n-------------------------------\n")

    # 2. The Master Craftsman (Hired Man logic)
    print("--- SCENARIO B: The Surveyor ---")
    builder2 = CraftsmanshipEngine("Kaelen")
    # Kaelen measures before he cuts
    builder2.process_material("LOG", is_measured=True, action="CUT")
    builder2.process_material("LOG", is_measured=True, action="CUT")
    builder2.run_audit()
