import numpy as np
import matplotlib.pyplot as plt

def simulate_gallery_resonance():
    """
    Simulates the Grand Gallery acoustic resonance to verify stability 
    against the 12.37% Hades Gap tolerance.
    """
    print("--- REGISTER 2: ACOUSTIC TRANSDUCTOR SIMULATION ---")
    
    # Constants
    V_SOUND_GRANITE = 5950  # m/s
    GALLERY_LENGTH = 46.5   # m
    HADES_GAP = 0.1237      # 12.37%
    TARGET_FREQ = 64.0      # Hz
    
    # Calculate Fundamental Frequency
    fundamental_freq = V_SOUND_GRANITE / (2 * GALLERY_LENGTH)
    
    print(f"Material Velocity:                {V_SOUND_GRANITE} m/s")
    print(f"Gallery Length:                   {GALLERY_LENGTH} m")
    print(f"Calculated Fundamental Frequency: {fundamental_freq:.2f} Hz")
    print(f"Target Frequency:                 {TARGET_FREQ} Hz")
    
    # Check Deviation
    deviation = abs(fundamental_freq - TARGET_FREQ) / TARGET_FREQ
    print(f"\nDeviation from Target:            {deviation * 100:.4f}%")
    
    # Stability Check against Hades Gap
    if deviation <= HADES_GAP:
        print("\n[VERIFIED] Resonance falls within the 12.37% Hades Gap tolerance.")
        print("The structure is acoustically stable within the PMG framework.")
    else:
        print("\n[WARNING] Resonance exceeds Hades Gap tolerance.")
        
    # Simulate Harmonic Coupling with Hades Beat (0.660688 Hz)
    hades_beat = 0.660688
    coupling_ratio = TARGET_FREQ / hades_beat
    print(f"\nHades Beat Coupling Ratio:        {coupling_ratio:.2f}")
    print(f"Modulus 24 Check:                 {coupling_ratio / 24:.4f} (Should be near integer)")
    
    # Plot Resonance Curve
    frequencies = np.linspace(60, 70, 500)
    # Lorentzian resonance curve
    resonance = 1 / (1 + ((frequencies - fundamental_freq) / (fundamental_freq * HADES_GAP))**2)
    
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, resonance, label='Acoustic Resonance', color='purple')
    plt.axvline(x=TARGET_FREQ, color='red', linestyle='--', label='Target 64 Hz')
    plt.axvspan(TARGET_FREQ * (1-HADES_GAP), TARGET_FREQ * (1+HADES_GAP), color='green', alpha=0.2, label='Hades Gap Tolerance')
    plt.title('Grand Gallery Acoustic Stability Simulation')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Relative Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('gallery_resonance_simulation.png')
    print("\n[SAVE] Resonance plot saved as 'gallery_resonance_simulation.png'")

if __name__ == "__main__":
    simulate_gallery_resonance()
