import math

def calculate_torque_curve():
    print("======================================================================")
    print("  THE SOUL STAR: 156-TICK TORQUE CURVE & GAUSSIAN CURVATURE MAP")
    print("======================================================================")
    print(f"{'TICK':<6} | {'PHASE SHIFT (Δθ)':<18} | {'CLUTCH ENGAGEMENT (K)':<25} | {'GEOMETRIC STATE'}")
    print("-" * 75)

    # Constants
    GEAR_MEASURE = 12
    GEAR_COMM = 13
    INPUT_SHAFT = math.sqrt(42)  # 6.48074...
    
    for t in range(157):
        # Calculate angular position of each gear in degrees
        theta_12 = (360.0 * (t / GEAR_MEASURE)) % 360.0
        theta_13 = (360.0 * (t / GEAR_COMM)) % 360.0
        
        # Phase difference between the count and measure
        delta_theta = abs(theta_12 - theta_13)
        if delta_theta > 180:
            delta_theta = 360 - delta_theta
            
        # Gaussian Curvature / Torque is maximal when delta_theta is 0 (Singularity)
        # It slips when delta_theta is maximal (180 degrees)
        # K = f(delta_theta). When delta_theta is 0, K = Root 42.
        
        # Let's normalize clutch engagement from 0.0 (Slipping) to 1.0 (Fully Engaged)
        engagement = 1.0 - (delta_theta / 180.0)
        
        # Calculate actual curvature applying Root 42 mod 24 tension
        # Modulo 24 acts as the "axial container". The Riemann lock is -1/12.
        curvature_k = engagement * INPUT_SHAFT * (1 + (1/12))
        
        # Only log significant ticks to avoid 156 lines of output
        # Significant ticks: 0, 12, 13, 24, 26, 39, 42, 78, 156
        if t in [0, 12, 13, 26, 42, 65, 78, 156]:
            state = "Transitional"
            if t == 0 or t == 156:
                state = "100% BITING (The Singularity / Taut)"
            elif t == 42:
                state = "THE APERTURE (42° Glide / O-Loop)"
            elif t == 78:
                state = "THE HALF-TURN (180° Reflection / K=0)"
            elif t in [12, 13, 26]:
                state = "PADDOCK MESH (Letter Strut formed)"
            
            print(f"  {t:<4} | {delta_theta:>7.2f}°           | K = {curvature_k:>6.4f} ({(engagement*100):>5.1f}%) | {state}")

    print("======================================================================")
    print("  [SYSTEM] The 93-Point Solid is held Taut by K-Max at Tick 156.")
    print("  [SYSTEM] The 10-24-26 LSD absorbs the Phase Shift via the Alphabet.")
    print("======================================================================")

if __name__ == "__main__":
    calculate_torque_curve()
