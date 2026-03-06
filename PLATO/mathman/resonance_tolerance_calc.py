import math
import numpy as np

def calculate_resonance_tolerance():
    # Canonical Constants
    SQRT_42 = math.sqrt(42)  # 6.4807
    SQRT_51 = math.sqrt(51)  # 7.1414
    BASE_FREQ = 66.0         # Hz
    BEAT_FREQ = SQRT_51 - SQRT_42  # ~0.6607 Hz
    
    BOUNDARY_D = 4.0        # Platonic 4 Space
    IDEAL_RATE = 1.0        # 1 pulse/s
    HADES_GAP = 0.1237
    
    print(f"--- Resonance Tolerance Analysis ---")
    print(f"Platonic Boundary: {BOUNDARY_D} units")
    print(f"Beat Frequency: {BEAT_FREQ:.4f} Hz")
    print(f"Hades Gap: {HADES_GAP}")
    
    # Standing Man Coherence Logic
    # D = 4, Rate = 1 => Travel time (round trip) = 8s
    # In one pulse cycle (1s), the wave covers 1/8th of the return trip.
    
    vibration_range = np.linspace(0, 0.5, 50)
    coherence_scores = []
    
    for drift in vibration_range:
        # Phase shift caused by boundary drift
        # Delta Phase = (2 * Delta D) / wavelength
        # Here wavelength is roughly IDEAL_RATE * Pulse_Duration (1s) = 1.0
        delta_phase = (2 * drift) / 1.0
        
        # Coherence is the constructive interference of Outbound and Inbound
        # Coherence = cos(Delta Phase / 2)
        score = math.cos(delta_phase * math.pi) # Simplified phase coherence
        coherence_scores.append(max(0, score))
        
    # Find Decoherence Point (Score < 0.5)
    decoherence_threshold = 0.5
    tolerance_limit = 0
    for i, score in enumerate(coherence_scores):
        if score < decoherence_threshold:
            tolerance_limit = vibration_range[i]
            break
            
    print(f"\nMax Resonance Tolerance: {tolerance_limit:.4f} units")
    print(f"Coherence at limit: {coherence_scores[i]:.4f}")
    
    if tolerance_limit < HADES_GAP:
        print("WARNING: Tolerance is below Hades Gap. Standing Man fragmentation imminent.")
    else:
        print("STATUS: Standing Man Coherence Stable within Hades Gap.")

    return tolerance_limit

if __name__ == "__main__":
    calculate_resonance_tolerance()
