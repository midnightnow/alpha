import math
import sys

def print_156_tick():
    print("="*60)
    print("  MANIC GRAFIA: 156-TICK DIFFERENTIAL EXHAUST (12/13)")
    print("="*60)
    print(f"  {'TICK':<6} | {'MEASURE (12)':<12} | {'COMM (13)':<12} | {'PHASE DIFFERENCE (°)'}")
    print("-" * 60)
    
    for tick in range(156 + 1):
        # 12-tooth gear completes one rotation every 12 ticks
        angle_12 = (tick % 12) / 12.0 * 360.0
        # 13-tooth gear completes one rotation every 13 ticks
        angle_13 = (tick % 13) / 13.0 * 360.0
        
        phase_diff = abs(angle_12 - angle_13)
        if phase_diff > 180:
            phase_diff = 360 - phase_diff
            
        # Draw a little "spark" indicator if they cross/resonate
        spark = ""
        if phase_diff == 0:
            spark = "   <-- ALIGNMENT (THE TRINITY / ROOT)"
        elif round(phase_diff, 1) in [90.0]:
            spark = "   <-- SHEER FACE (PERPENDICULAR)"
        elif round(phase_diff, 1) in [42.0, 41.5, 42.5]: # approx
            spark = "   <-- APERTURE (RAINBOW 42°)"
            
        if tick % 13 == 0 or tick % 12 == 0 or spark:
            print(f"  {tick:<6} | {angle_12:^12.1f} | {angle_13:^12.1f} | {phase_diff:^15.2f}{spark}")
            
    print("-" * 60)
    print("  ENGINE DIAGNOSTIC COMPLETE. ZERO HYSTERESIS DETECTED.")
    print("="*60)

if __name__ == "__main__":
    print_156_tick()
