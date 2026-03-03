import math
import time
from typing import Optional
from sovereign_ledger_manager import SovereignLedgerManager

# Core limits
OVERPACK_DELTA_TOLERANCE = 0.000585
MAX_DELTA_MULTIPLIER = 10.0

class VitrificationHandler:
    """
    Acts as a governor for the Sovereign Lattice.
    Monitors pressure at Salience Nodes. Deforms elastically at Σ₄/Σ₅.
    Does not halt the simulation unless sovereignty is genuinely compromised.
    """
    def __init__(self):
        self.ledger = SovereignLedgerManager()

    def check_node_pressure(self, node_id: str, angle_deg: float, current_delta: float) -> float:
        """
        Evaluate node pressure against the Overpack Delta (δ ≈ 0.000585).
        Returns the effective delta (deformed elastically if needed).
        """
        if current_delta <= OVERPACK_DELTA_TOLERANCE:
            return current_delta  # Normal pressure, no vitrification

        # Delta exceeded standard tolerance -> catastrophic drift. Hard crash.
        if current_delta > OVERPACK_DELTA_TOLERANCE * MAX_DELTA_MULTIPLIER:
            action = "CRITICAL FAILURE: Sovereignty Compromised"
            self.ledger.log_event(node_id, angle_deg, current_delta, OVERPACK_DELTA_TOLERANCE, action)
            raise RuntimeError(
                f"Lattice shattered at node {node_id}. "
                f"Delta {current_delta:.6f} exceeds 10x tolerance."
            )

        # Between 1x and 10x tolerance -> elastic deformation (warning threshold)
        deformed_delta = OVERPACK_DELTA_TOLERANCE + math.log(1 + (current_delta - OVERPACK_DELTA_TOLERANCE))
        action = f"Elastic Yield (Capped at {deformed_delta:.6f})"
        
        self.ledger.log_event(node_id, angle_deg, current_delta, OVERPACK_DELTA_TOLERANCE, action)
        
        return deformed_delta

    def check_ouroboros_sync(self, tick_count: int) -> str:
        """
        Triggers ledger compression when the 24-wheel 
        and 60-vector field achieve phase-lock.
        The Convergence: LCM(24, 60) = 120.
        """
        if tick_count % 120 == 0:
            return "NULL_POINT_REACHED: Compressing Silt to Ledger..."
        return "STABLE_DRIFT"

    def dump_log(self):
        """No longer strictly needed as we output to MD, but kept for legacy."""
        print("Vitrification Ledger now stored in ../SOVEREIGN_LEDGER.md")
