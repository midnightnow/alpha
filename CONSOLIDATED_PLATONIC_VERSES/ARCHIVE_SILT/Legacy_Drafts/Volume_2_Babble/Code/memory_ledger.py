# memory_ledger.py
# VOLUME 3: THE LEDGER OF EROSION
# STATUS: ACTIVE

class MemoryTier:
    def __init__(self, min_debt, max_debt, hazard_type, consequence, hazard):
        self.min_debt = min_debt
        self.max_debt = max_debt
        self.hazard_type = hazard_type
        self.consequence = consequence
        self.hazard = hazard

LEDGER_OF_EROSION = [
    MemoryTier(0.0, 5.0, "Static Tinnitus", "Digital whining in quiet rooms", "HUD elements flicker; minor UI lag"),
    MemoryTier(5.1, 14.0, "Semantic Satiation", "Common words lose meaning; faces blur", "Objective markers become 'Corrupted Poetry'"),
    MemoryTier(14.1, 25.0, "The Fog of Kinship", "Forgot the Scribe’s name or history", "Inversion Risk: Movement keys occasionally invert"),
    MemoryTier(25.1, 40.0, "The Void of Purpose", "Forgot why they are fighting", "Map data replaced by 'Residual Images'"),
    MemoryTier(40.1, 999.0, "Recursive Loop", "Kael becomes an NPC", "Permadeath: Absorbed by the Hades Beat")
]

def check_debt_status(current_debt, floating_point_error=False):
    """Returns the current narrative and mechanical hazards based on debt."""
    if floating_point_error or str(current_debt) == "NaN":
        return {
            "Title": "FLOATING POINT ERROR",
            "Consequence": "Debt is unmeasurable. Reality is unmapped.",
            "Mechanical": "STERROR: MEASUREMENT_FAILURE. All thresholds are active simultaneously."
        }
        
    for tier in LEDGER_OF_EROSION:
        if current_debt <= tier.max_debt:
            return {
                "Title": tier.hazard_type,
                "Consequence": tier.consequence,
                "Mechanical": tier.hazard
            }
    return None
