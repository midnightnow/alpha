# volume_3_synthesis.py
# Handles the dual-synthesis mechanics for Volume 3: Synthesis.

from local_shear_engine import CoherenceDebt, LoadBearingAnomaly

class AlephMerchant(LoadBearingAnomaly):
    """Kael's final form: The Living Ledger."""
    def __init__(self):
        super().__init__(initial_coherence=14.2)
        self.state = "INFINITE_DEBT_MODE"
        self.internal_pressure = 104.2
        
    def next_transaction(self, scribe_state):
        if self.state == "INFINITE_DEBT_MODE":
            return "DIRECTIVE_ENVIRONMENTAL_COMMUNICATION"
        return "IDENTITY_MISMATCH"

class ScribeArchitect(LoadBearingAnomaly):
    def __init__(self):
        super().__init__(initial_coherence=39.4)
        self.personal_memories = ["The Sound of the First Transaction", "Kael's Real Name"]
        self.capacity = 0.0 # Freed by Kael
        self.key_status = "ACTIVE"
        
    def perform_personal_trade(self, memory_index):
        """The Scribe pays the toll with her own history."""
        lost_data = self.personal_memories.pop(memory_index)
        self.debt += 5.0
        return f"PERSONAL_TRADE_COMPLETE: {lost_data}_REMOVED"

class SynthesisLedger:
    def __init__(self):
        self.global_infection_delta = 0.992
        self.status = "STABLE_PARADOX"
        
    def validate_toll_entry(self, data_payload):
        """Verification of the personal memory trade."""
        if "REMOVED" in data_payload:
            return "SECTOR_0_ACCESS_GRANTED: TOLL_PAID"
        return "ACCESS_DENIED: INSUFFICIENT_PERSONAL_STAKES"
