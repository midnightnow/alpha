
import math

class RotationalTargetingMap:
    def __init__(self, modulus=420):
        self.M = modulus # The Master Key
        self.base_tick = 15 # 24 units = 360 degrees (15 deg per unit)
        
    def calculate_intercept(self, chaser_freq=24, target_freq=30, rotation_speed=1):
        """
        Model: CAT (24) vs MICE (30) on a rotating pyramid.
        The system rotates, moving the 'Goal' as the chaser moves.
        """
        # Relative frequencies on the 420 wheel
        # CAT has the 3-phase structural advantage
        # MICE has the 5-phase organic flow
        
        # At what angle do they resonate (intercept)?
        # 120 is the Grand Ordinance where 24 and 30 both overlap (catches).
        resonance_nodes = [n for n in range(0, self.M + 1, 120)]
        
        # Calculate the 'Tarry' error for linear movement
        # If the CAT tries to walk straight to where the MICE started at t=0
        linear_error = (target_freq / self.M) * 360 * rotation_speed
        
        # The Spiral Intercept calculates the lead
        angular_lead = linear_error * (1 - 0.1237) # Adjusted for Hades Gap
        
        return {
            "Resonance Nodes (Intercepts)": resonance_nodes,
            "Linear Tarry Error (Deg)": f"{round(linear_error, 2)}°",
            "Spiral Lead Angle (Deg)": f"{round(angular_lead, 2)}°",
            "Next Capture Phase": "120° (South-East / Apex Flight)"
        }

if __name__ == "__main__":
    map = RotationalTargetingMap()
    print("--- ROTATIONAL TARGETING MAP: THE CAT/MICE INTERCEPT ---")
    data = map.calculate_intercept()
    for k, v in data.items():
        print(f"{k}: {v}")
    print("\nLOGIC: The CAT waits at the 120° Node while the MICE spiral into it.")
    print("This satisfies the 12.37% Breath Debt by avoiding the Tarry.")
