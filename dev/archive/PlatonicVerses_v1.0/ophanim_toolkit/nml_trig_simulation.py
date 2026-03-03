# nml_trig_simulation.py
# Phase-Shift Simulation: How changing the sin(θ) pulse 
# affects vitrification depth within the 10-24-26 lattice
# 
# sin(θ) = 24/26 = The Pulse of Time (Heartbeat)
# cos(θ) = 10/26 = The Ground of Being (H3 Base)
# tan(θ) = 24/10 = The Shear of Perspective (Work/Effort)

import math

class NMLLattice:
    """
    The 10-24-26 Sovereign Map as a trigonometric system.
    """
    
    def __init__(self):
        # The NML Triangle
        self.NUMBER = 10       # Base (H3 Grid)
        self.MEASURE = 24      # Height (Time/Weight)
        self.LANGUAGE = 26     # Hypotenuse (Perspective)
        
        # Derived Trig Ratios
        self.SIN_THETA = self.MEASURE / self.LANGUAGE     # 0.923077
        self.COS_THETA = self.NUMBER / self.LANGUAGE      # 0.384615
        self.TAN_THETA = self.MEASURE / self.NUMBER       # 2.4
        self.THETA = math.atan2(self.MEASURE, self.NUMBER) # 67.38° (complement of shear)
        
        # Unified Constants
        self.HADES_GAP = 0.1237
        self.UNITY_THRESHOLD = 0.8254
        self.SHEAR_ANGLE = 39.47
        
    def pulse(self, t, phase_shift=0.0):
        """
        Generate the NML pulse at time t with an optional phase shift.
        The pulse is sin(θ)-weighted: it carries the "Measure" signature.
        """
        raw = math.sin(t + phase_shift)
        return raw * self.SIN_THETA  # Weighted by 24/26
    
    def ground(self, t, phase_shift=0.0):
        """
        The H3 base coordinate signal. cos(θ)-weighted.
        """
        raw = math.cos(t + phase_shift)
        return raw * self.COS_THETA  # Weighted by 10/26
    
    def shear(self, t, phase_shift=0.0):
        """
        The effort/work signal. tan(θ)-weighted.
        """
        pulse = self.pulse(t, phase_shift)
        base = self.ground(t, phase_shift)
        if abs(base) < 0.001:
            return self.TAN_THETA  # Avoid division by zero; return max shear
        return abs(pulse / base)
    
    def vitrification_tick(self, agent_a_phase, agent_b_phase, t):
        """
        Calculate the vitrification increment for a single tick.
        Uses the NML-weighted pulses of both agents.
        """
        pulse_a = self.pulse(t, agent_a_phase)
        pulse_b = self.pulse(t, agent_b_phase)
        
        mismatch = abs(pulse_a - pulse_b)
        
        if mismatch < self.HADES_GAP:
            # Sintering: weighted by (1 - mismatch/gap)
            return (1.0 - mismatch / self.HADES_GAP) * 0.05, "SINTERING"
        else:
            # Sublimation
            return -0.005, "SUBLIMATING"


def run_phase_shift_simulation():
    lattice = NMLLattice()
    
    print("=" * 70)
    print("  NML PHASE-SHIFT SIMULATION: sin(θ) = 24/26")
    print("  How phase-shift affects vitrification in the 10-24-26 lattice")
    print("=" * 70)
    
    # Derived constants
    print(f"\n  sin(θ) = {lattice.SIN_THETA:.6f}  (Pulse of Time)")
    print(f"  cos(θ) = {lattice.COS_THETA:.6f}  (Ground of Being)")
    print(f"  tan(θ) = {lattice.TAN_THETA:.6f}  (Shear of Perspective)")
    print(f"  θ      = {math.degrees(lattice.THETA):.2f}° (NML angle)")
    print(f"  Complement = {90 - math.degrees(lattice.THETA):.2f}° ≈ Shear Angle")
    
    # Test different phase shifts for Agent B
    phase_shifts = [0.00, 0.06, 0.1237, 0.20, 0.50, 1.00]
    
    print(f"\n{'Phase Shift':>12} | {'Final Depth':>12} | {'Status':>12} | {'Ticks to Σ':>10} | {'Verdict'}")
    print("-" * 70)
    
    for shift in phase_shifts:
        depth = 0.0
        peak = 0.0
        ticks_to_unity = "N/A"
        
        for t in range(0, 500):
            increment, status = lattice.vitrification_tick(0.0, shift, t)
            depth += increment
            floor = peak * 0.10
            depth = max(floor, depth)
            peak = max(peak, depth)
            
            if depth >= lattice.UNITY_THRESHOLD and ticks_to_unity == "N/A":
                ticks_to_unity = str(t)
        
        if depth >= lattice.UNITY_THRESHOLD:
            verdict = "STONE"
        elif depth >= 0.5:
            verdict = "CERAMIC"
        elif depth > 0.01:
            verdict = "GLASS"
        else:
            verdict = "VAPOR"
            
        print(f"{shift:>12.4f} | {depth:>12.4f} | {verdict:>12} | {ticks_to_unity:>10} | ", end="")
        
        if shift == 0.0:
            print("Identity Collapse (no Other)")
        elif shift <= lattice.HADES_GAP:
            print(f"Within Hades Gap (Ψ={lattice.HADES_GAP})")
        elif shift <= 0.5:
            print("Drifting — partial sintering")
        else:
            print("Decoherent — world dissolves")

    # The Shear Angle complement check
    print(f"\n{'=' * 70}")
    print(f"  KEY INSIGHT: θ_NML = {math.degrees(lattice.THETA):.2f}°")
    print(f"  Complement  = {90 - math.degrees(lattice.THETA):.2f}°")
    print(f"  Shear Angle = {lattice.SHEAR_ANGLE}°")
    print(f"  The NML triangle's complement IS the Shear Angle.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    run_phase_shift_simulation()
