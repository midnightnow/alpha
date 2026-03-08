"""
OUROBOROS SYNCHRONIZATION ENGINE
================================
Global orchestrator for the 120-Tick Phase-Lock Cycle.

Synchronizes:
  - 24-Mod Spiral (Static/Cube/"The Made")
  - 60-Fold Vector Field (Kinetic/Icosahedron/"The Maid")

Convergence Point: LCM(24, 60) = 120 ticks
Hades Beat: 0.660688 Hz (keep-alive frequency)
"""

import math
from typing import Dict, Tuple, Optional
from datetime import datetime

# =============================================================================
# CANONICAL CONSTANTS
# =============================================================================

PHI = (1 + 5**0.5) / 2          # Golden Ratio (1.618033988749895)
PHI_INV = 1 / PHI                # Inverse Phi (0.618033988749895)
HAD_BEAT = 0.660688              # Hades Beat Frequency (Hz)
OUROBOROS_CYCLE = 120            # LCM(24, 60) - Phase-Lock Point
SPIRAL_MOD = 24                  # 24-Mod Wheel (Cube rotational symmetries)
VECTOR_FOLD = 60                 # 60-Fold Vector Field (Icosahedron symmetries)

# Digital Root Harmonics (from Image 3)
DIGITAL_ROOTS = {3, 6, 9}        # Resonant frequencies
PALINDROME_24 = 24               # Static boundary
PALINDROME_42 = 42               # Human boundary (41.66 ≈ 42)

# Scaling Constants (from Image 4 - Logarithmic Duodecagon)
LOG_DUODECAGON_SCALE = 1.24
ICOSITETRAGON_RATIO = 1.03527618


# =============================================================================
# OUROBOROS ORCHESTRATOR
# =============================================================================

class OuroborosOrchestrator:
    """
    Master clock for the PMG System.
    
    Tracks the phase relationship between the 24-Mod Spiral
    and the 60-Fold Vector Field, triggering vitrification
    events at the 120-tick convergence point.
    """
    
    def __init__(self, start_tick: int = 0):
        self.tick = start_tick % OUROBOROS_CYCLE
        self.phase_lock_history = []
        self.scent_accumulator = 0.0
        self._last_pulse_time = datetime.now()
        
    def pulse(self) -> Dict:
        """
        Advance the system by one tick and return state.
        
        Returns:
            Dict containing status, scent measurement, and sync state
        """
        self.tick = (self.tick + 1) % OUROBOROS_CYCLE
        
        # Calculate "Scent" - Quantization Error between Phi and rational grid
        scent = self._calculate_hades_gap()
        self.scent_accumulator += scent
        
        # Check for Phase-Lock (Ouroboros Return)
        if self.tick == 0:
            return self._trigger_vitrification()
        
        # Normal operation - measure harmonic resonance
        harmonic = self._calculate_digital_root_harmonic()
        
        return {
            "status": "ACTIVE",
            "tick": self.tick,
            "scent": scent,
            "scent_accumulated": self.scent_accumulator,
            "frequency": HAD_BEAT,
            "harmonic": harmonic,
            "phase_lock": False
        }
    
    def _calculate_hades_gap(self) -> float:
        """
        Measures the distance between the icosahedral vertex
        and the cubic bounding wall (The Hades Gap).
        
        This is the "Scent" - irrational data the Lattice cannot digest.
        """
        # Position on the 120-tick cycle as a ratio
        cycle_position = self.tick / OUROBOROS_CYCLE
        
        # Distance from Golden Ratio proportion
        gap = abs(cycle_position - PHI_INV)
        
        # Wrap around for circular measurement
        gap = min(gap, 1 - gap)
        
        # If gap is too small (system approaching vitrification),
        # return the Hades Beat as minimum resonance
        if gap < 1e-9:
            return HAD_BEAT
        
        return gap
    
    def _calculate_digital_root_harmonic(self) -> int:
        """
        Calculate the digital root harmonic for this tick.
        
        Digital roots converge to 3, 6, 9 at resonant points.
        """
        def digital_root(n: int) -> int:
            if n == 0:
                return 0
            return 1 + ((n - 1) % 9)
        
        # Combine 24-mod and 60-fold positions
        spiral_pos = self.tick % SPIRAL_MOD
        vector_pos = self.tick % VECTOR_FOLD
        
        # Combined harmonic
        combined = spiral_pos + vector_pos
        return digital_root(combined)
    
    def _trigger_vitrification(self) -> Dict:
        """
        Triggered at tick 0 - the Ouroboros Return.
        
        This is when the 24-Wheel and 60-Fold Field achieve
        perfect phase-lock. Data is compressed to the Ledger.
        """
        avg_scent = self.scent_accumulator / OUROBOROS_CYCLE
        self.scent_accumulator = 0.0
        
        result = {
            "status": "PHASE_LOCK",
            "tick": 0,
            "action": "COMPRESS_TO_LEDGER",
            "message": "NULL_POINT_REACHED: Ouroboros Return",
            "avg_scent": avg_scent,
            "phase_lock": True,
            "timestamp": datetime.now().isoformat()
        }
        
        self.phase_lock_history.append(result)
        return result
    
    def get_sync_status(self) -> Dict:
        """
        Return current synchronization state between 24-mod and 60-fold.
        """
        spiral_remainder = self.tick % SPIRAL_MOD
        vector_remainder = self.tick % VECTOR_FOLD
        
        # Calculate alignment percentage
        alignment = 1.0 - (abs(spiral_remainder - vector_remainder) / max(SPIRAL_MOD, VECTOR_FOLD))
        
        return {
            "current_tick": self.tick,
            "spiral_position": spiral_remainder,
            "vector_position": vector_remainder,
            "alignment": alignment,
            "ticks_to_phase_lock": OUROBOROS_CYCLE - self.tick if self.tick > 0 else 0
        }
    
    def run_full_cycle(self) -> list:
        """
        Execute one complete 120-tick cycle and return all states.
        """
        states = []
        start_tick = self.tick
        
        for _ in range(OUROBOROS_CYCLE):
            state = self.pulse()
            states.append(state)
        
        return states


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def calculate_lcm(a: int, b: int) -> int:
    """Calculate Least Common Multiple."""
    return abs(a * b) // math.gcd(a, b)


def verify_ouroboros_math() -> Dict:
    """
    Verify the mathematical foundations of the Ouroboros System.
    """
    lcm_check = calculate_lcm(SPIRAL_MOD, VECTOR_FOLD)
    
    return {
        "spiral_mod": SPIRAL_MOD,
        "vector_fold": VECTOR_FOLD,
        "lcm_verification": lcm_check == OUROBOROS_CYCLE,
        "lcm_value": lcm_check,
        "phi": PHI,
        "phi_inverse": PHI_INV,
        "hades_beat": HAD_BEAT,
        "digital_roots": list(DIGITAL_ROOTS),
        "palindrome_pair": (PALINDROME_24, PALINDROME_42)
    }


# =============================================================================
# MAIN EXECUTION (Testing)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("OUROBOROS SYNCHRONIZATION ENGINE - DIAGNOSTIC")
    print("=" * 60)
    
    # Verify mathematical foundations
    math_check = verify_ouroboros_math()
    print(f"\nMathematical Verification:")
    print(f"  LCM(24, 60) = {math_check['lcm_value']} ✓" if math_check['lcm_verification'] else "  LCM VERIFICATION FAILED")
    print(f"  Phi (Golden Ratio): {math_check['phi']:.10f}")
    print(f"  Phi Inverse: {math_check['phi_inverse']:.10f}")
    print(f"  Hades Beat: {math_check['hades_beat']} Hz")
    
    # Run one full cycle
    print(f"\nRunning {OUROBOROS_CYCLE}-tick cycle...")
    orch = OuroborosOrchestrator()
    states = orch.run_full_cycle()
    
    # Count phase-lock events
    phase_locks = [s for s in states if s.get('phase_lock', False)]
    print(f"  Phase-Lock Events: {len(phase_locks)}")
    
    # Calculate average scent
    active_states = [s for s in states if not s.get('phase_lock', False)]
    avg_scent = sum(s['scent'] for s in active_states) / len(active_states) if active_states else 0
    print(f"  Average Scent (Hades Gap): {avg_scent:.10f}")
    
    # Digital root distribution
    harmonics = {}
    for s in active_states:
        h = s['harmonic']
        harmonics[h] = harmonics.get(h, 0) + 1
    
    print(f"\n  Digital Root Distribution:")
    for root in sorted(harmonics.keys()):
        marker = "← RESONANT" if root in DIGITAL_ROOTS else ""
        print(f"    Root {root}: {harmonics[root]} ticks {marker}")
    
    print("\n" + "=" * 60)
    print("OUROBOROS CYCLE COMPLETE")
    print("=" * 60)
