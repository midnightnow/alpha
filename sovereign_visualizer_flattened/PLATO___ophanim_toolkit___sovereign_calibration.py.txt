"""
sovereign_calibration.py - Tracking the Sovereignty Constant (Σ) (v1.0)
PMG Book 4: The Sovereign Lattice | Phase V

NARRATIVE ORIGIN: The "Sovereignty Meter" used in the final chapters 
to reveal that the Observer (the User) is the final missing constant.
"""

from typing import List, Dict
import math
import time

class SovereignCalibration:
    """
    Tracks the growth of Sovereignty (Sigma) and the decay of Void Debt (Psi).
    Logs the "Freedom Margin" earned by the geometer.
    """
    def __init__(self, baseline_sigma: float = 1.0):
        self.history: List[Dict[str, float]] = []
        self.current_sigma = baseline_sigma
        self.freedom_margin: float = 0.1237 # Initial Hades Gap
        
    def audit_session(self, void_debt: float, active_voices: int):
        """
        Updates Σ based on the current state.
        Σ = (1 / (void_debt + 0.01237)) * (active_voices / 7.0)
        """
        # We divide by 7 because there are 7 canonical voices. 
        # Harmonizing all voices increases sovereignty.
        voice_participation = active_voices / 7.0
        epsilon = 0.01237
        
        self.current_sigma = (1.0 / (void_debt + epsilon)) * voice_participation
        
        # Freedom Margin increases as Sigma exceeds the "Baseline of Constraint" (66.0)
        # 66.0 represents the 66Hz beat frequency of the Ideal Solid.
        if self.current_sigma > 66.0:
            growth = (self.current_sigma - 66.0) * 0.001
            self.freedom_margin += growth
            
        record = {
            "timestamp": time.time(),
            "void_debt": void_debt,
            "sigma": self.current_sigma,
            "freedom_margin": self.freedom_margin
        }
        self.history.append(record)
        return record

    def get_report(self):
        print("====================================================================")
        print("   SOVEREIGN CALIBRATION REPORT: THE EMERGENCE OF Σ                ")
        print("====================================================================\n")
        
        if not self.history:
            print("No session data recorded.")
            return

        latest = self.history[-1]
        print(f"📊 Current Sovereignty (Σ): {latest['sigma']:.4f}")
        print(f"🕊️  Freedom Margin: {latest['freedom_margin']:.2%} (Hades Expansion)")
        print(f"⚠️  External Debt: {latest['void_debt']:.4f}\n")

        status = "BONDAGE"
        if latest['sigma'] > 1.0: status = "AWAKENING"
        if latest['sigma'] > 12.37: status = "GEOMETER"
        if latest['sigma'] > 66.0: status = "SOVEREIGN"
        if latest['sigma'] > 99.999: status = "ARCHITECT_EXILE"
        
        print(f"⚖️  Sovereignty Tier: {status}")
        print("====================================================================\n")

if __name__ == "__main__":
    cal = SovereignCalibration()
    
    # Simulate a transition from High Debt to Zero Debt
    print("Simulating Session Calibration...")
    
    # 1. High Debt, Single Voice
    cal.audit_session(void_debt=0.4948, active_voices=1)
    
    # 2. Resolving 2 chapters, 3 voices
    cal.audit_session(void_debt=0.2474, active_voices=3)
    
    # 3. All debt resolved, 7 voices harmonized
    cal.audit_session(void_debt=0.0, active_voices=7)
    
    cal.get_report()
