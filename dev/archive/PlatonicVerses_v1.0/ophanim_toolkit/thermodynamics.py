"""
thermodynamics.py - The Resurrection Protocol and Entropy Auditing
PMG Chapter 9 | Principia Mathematica Geometrica
"""

import math
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PatternInstance:
    """An instance of a transmitted pattern (e.g. Sonnet replication)"""
    pattern_id: str
    replication_rate: float  # r
    base_entropy: float      # S
    transmission_count: int = 1

    def calculate_delta_s(self) -> float:
        """
        ΔS = S_base * (1 - ln(r))
        If r > 1: ΔS < 0 (Negative Entropy / Resurrection)
        If r < 1: ΔS > 0 (Decay)
        If r = 0: ΔS -> infinity (Erasure)
        """
        if self.replication_rate <= 0:
            return float('inf')
        return self.base_entropy * (1 - math.log(self.replication_rate))

class ResurrectionOperator:
    """
    Simulates the attempt to achieve local negative entropy through transmission.
    """
    def __init__(self):
        self.patterns: List[PatternInstance] = []

    def register_pattern(self, pattern_id: str, r: float, base_s: float):
        instance = PatternInstance(pattern_id, r, base_s)
        self.patterns.append(instance)
        return instance

    def audit_system(self) -> dict:
        """Summative thermodynamic audit of all registered patterns."""
        total_delta_s = 0.0
        status = "ENTROPY_DOMINANT"
        
        for p in self.patterns:
            ds = p.calculate_delta_s()
            if ds == float('inf'):
                continue
            total_delta_s += ds
            
        if total_delta_s < 0:
            status = "RESURRECTION_ACTIVE"
        elif any(p.replication_rate == 0 for p in self.patterns):
            status = "ERASURE_DETECTION"
            
        return {
            "total_delta_s": round(total_delta_s, 4),
            "status": status,
            "patterns_count": len(self.patterns)
        }

def test_resurrection_protocol():
    print("--- PMG Resurrection Protocol Audit ---")
    op = ResurrectionOperator()
    
    # Octave 9 Scenario:
    # 1. Early Octave (Sonnets 65-68): r > 1 (Audacious Claim)
    op.register_pattern("Immortality_Claim", r=1.5, base_s=0.5)
    
    # 2. Late Octave (Sonnets 71-72): r = 0 (Intentional Erasure)
    op.register_pattern("Self_Sabotage", r=0.0, base_s=1.0)
    
    audit = op.audit_system()
    print(f"Audit Status: {audit['status']}")
    print(f"Total ΔS: {audit['total_delta_s']}")
    
    # Scenario: Pure Replication (r=2)
    op2 = ResurrectionOperator()
    op2.register_pattern("Viral_Transmission", r=2.0, base_s=0.42)
    audit2 = op2.audit_system()
    print(f"\nViral Scenario Status: {audit2['status']}")
    print(f"Viral ΔS: {audit2['delta_s_sample'] if 'delta_s_sample' in audit2 else audit2['total_delta_s']}")

if __name__ == "__main__":
    test_resurrection_protocol()
