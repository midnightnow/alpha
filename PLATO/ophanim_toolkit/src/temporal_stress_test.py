
import math
import time

def simulate_stress_test(eta=0.95, psi=0.1237):
    print(f"--- VOID STRESS TEST (ETA={eta}, PSI={psi}) ---")
    phi = (1 + math.sqrt(5)) / 2
    distortion = 0.0
    decay = 0.5
    t = 0
    dt = 0.016 # 60fps
    
    slag_threshold = 5.0 # Distortion above this is considered 'Slag'
    vitrified_count = 0
    total_steps = 1000 # ~16 seconds
    
    for _ in range(total_steps):
        t += dt
        tension = math.sin(t * 12) % phi
        
        # Apply metabolic stress
        if tension > eta:
            vitrified_count += 1
            # The PMG pressure formula
            distortion += (tension - eta) * 5.0 * (1 / psi)
            
        # Natural thermodynamic cooling
        distortion = max(0.0, distortion * math.exp(-dt * decay))
        
        if distortion > slag_threshold:
            print(f"ALERT: Logic Lock at T={t:.2f}s | Distortion: {distortion:.4f} | System: SLAG")
            return False
            
    print(f"SUCCESS: System Stable. Total Vitrification Events: {vitrified_count}")
    print(f"Average System Pressure: {(vitrified_count / total_steps) * 100:.2f}%")
    return True

if __name__ == "__main__":
    # Test 1: Canonical Stability
    simulate_stress_test(0.95, 0.1237)
    
    # Test 2: Reduced Hades Gap (Increased Pressure)
    print("\n[ TESTING SYSTEM BOUNDARY: PSI=0.08 ]")
    simulate_stress_test(0.95, 0.08)
    
    # Test 3: Lowered Vitrification Threshold (Increased Sensitivity)
    print("\n[ TESTING SYSTEM BOUNDARY: ETA=0.85 ]")
    simulate_stress_test(0.85, 0.1237)
