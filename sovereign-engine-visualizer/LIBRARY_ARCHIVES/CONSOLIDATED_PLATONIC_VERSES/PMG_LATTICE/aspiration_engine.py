# --- THE ASPIRATION ENGINE (Safety vs. Growth) ---
# The trade-off between Security (Bir) and Potential (Wine).

class AspirationEngine:
    def __init__(self, subject_name: str):
        self.subject = subject_name
        self.safety = 0.0          # Current level of security
        self.growth = 0.0          # Current level of dimensional climbing
        self.drinks_beer = False   # Acceptance of the Bir Covenant
        
        # The Comfort Threshold
        # When safety exceeds this level, the urge to explore drops to zero.
        self.COMFORT_THRESHOLD = 0.8  # 80% Security
        
        # The Bir Factor
        # Beer reduces anxiety and increases contentment with the current state.
        self.BIR_CONTENTMENT = 0.5    

    def consume_substance(self, substance: str):
        if substance == "BIR":
            self.drinks_beer = True
            self.safety = min(1.0, self.safety + self.BIR_CONTENTMENT)
            print(f"[{self.subject}] Consumed Bir. Safety raised to {self.safety:.1f}. Contentment achieved.")
        elif substance == "WINE":
            self.drinks_beer = False
            # Wine requires venturing out and taking architectural risks.
            self.growth += 0.5
            self.safety = max(0.0, self.safety - 0.2) 
            print(f"[{self.subject}] Consumed Wine. Growth raised to {self.growth:.1f}. Safety dropped. Wind is felt.")

    def evaluate_ambition(self) -> str:
        """Determines the subject's place on the Aspiration Ladder."""
        if self.safety >= self.COMFORT_THRESHOLD:
            # The Aspiration Trap. The worker builds the Sty.
            return "LEVEL 2: STABILITY (The Brick/Bir Sty). Ambition Halted."
        elif self.growth > 0.5:
            return "LEVEL 3: GROWTH (The Journey). Building the Ship."
        else:
            return "LEVEL 1: SURVIVAL (The Mud)."

    def apply_ares_judgment(self):
        """Ares audits the mud men. He attacks those who have frozen at Level 2."""
        status = self.evaluate_ambition()
        print(f"\n--- ARES SCANS: {self.subject} ---")
        if "STABILITY" in status:
            print("ARES JUDGMENT: HORROR. Mud man found hardening in a Sty. Unleashing the Wolf to break the walls.")
            # Ares forces the subject back into chaos to promote growth
            self.safety = 0.0 
        else:
            print("ARES JUDGMENT: ACCEPTABLE. Subject is moving.")

if __name__ == "__main__":
    print("--- ASPIRATION ENGINE INITIALIZED ---\n")
    
    # 1. The Laborer
    laborer = AspirationEngine("The Builder")
    laborer.consume_substance("BIR")
    laborer.consume_substance("BIR") # Drinks the Archon's bargain
    print(f"Status: {laborer.evaluate_ambition()}")
    
    laborer.apply_ares_judgment()
    print(f"New Status Post-Audit: {laborer.evaluate_ambition()}")
    
    print("\n-------------------------------\n")
    
    # 2. The Hired Man
    kaelen = AspirationEngine("Kaelen")
    kaelen.consume_substance("WINE")
    kaelen.consume_substance("WINE") # Drinks the bitter truth
    print(f"Status: {kaelen.evaluate_ambition()}")
    
    kaelen.apply_ares_judgment()
