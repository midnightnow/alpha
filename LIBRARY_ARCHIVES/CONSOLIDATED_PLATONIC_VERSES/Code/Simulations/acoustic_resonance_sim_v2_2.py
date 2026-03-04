import numpy as np
import matplotlib.pyplot as plt

def simulate_gallery_resonance_v2_2():
    """
    Simulates the Grand Gallery acoustic resonance at 66.0688 Hz
    (100× Hades Beat) with environmental temperature refinement.
    """
    print("--- REGISTER 2: 66.0688 Hz PHONON BRIDGE SIMULATION (v2.2) ---")
    
    # Constants
    HADES_BEAT = 0.660688  # Hz (√51 - √42)
    TARGET_FREQ = HADES_BEAT * 100  # 66.0688 Hz (Human-scale amplification)
    GALLERY_LENGTH = 46.5  # meters (88 royal cubits)
    HADES_GAP = 0.1237  # 12.37% tolerance
    
    # Material properties
    V_SOUND_GRANITE_BASE = 5950  # m/s at 20°C
    TEMP_COEFFICIENT = 0.005  # 0.5% per 10°C = 0.0005 per °C
    TEMP_RANGE = (15, 25)  # Typical Gallery temperature range (°C)
    
    # Calculate required velocity at target frequency
    required_velocity = 2 * GALLERY_LENGTH * TARGET_FREQ
    
    print(f"Hades Beat (Planetary):           {HADES_BEAT:.6f} Hz")
    print(f"Target Frequency (Human):         {TARGET_FREQ:.4f} Hz")
    print(f"Gallery Length:                   {GALLERY_LENGTH} m")
    print(f"Required Sound Velocity:          {required_velocity:.0f} m/s")
    print(f"Base Granite Velocity (20°C):     {V_SOUND_GRANITE_BASE} m/s")
    print(f"Temperature Coefficient:          {TEMP_COEFFICIENT*100:.2f}% per 10°C")
    
    # Temperature-adjusted velocity range
    v_min = V_SOUND_GRANITE_BASE * (1 + TEMP_COEFFICIENT * (TEMP_RANGE[0] - 20))
    v_max = V_SOUND_GRANITE_BASE * (1 + TEMP_COEFFICIENT * (TEMP_RANGE[1] - 20))
    
    print(f"\nVelocity Range ({TEMP_RANGE[0]}–{TEMP_RANGE[1]}°C): {v_min:.0f}–{v_max:.0f} m/s")
    print(f"Target within Range: {'✓ YES' if v_min <= required_velocity <= v_max else '✗ NO'}")
    
    # √19 Convergence Check
    separations = 288
    ratio = separations / TARGET_FREQ
    sqrt_19 = np.sqrt(19)
    deviation = abs(ratio - sqrt_19) / sqrt_19
    
    print(f"\n288 Separations / {TARGET_FREQ:.4f} Hz = {ratio:.4f}")
    print(f"√19 = {sqrt_19:.4f}")
    print(f"Deviation: {deviation * 100:.3f}%")
    
    if deviation < HADES_GAP:
        print("[VERIFIED] √19 convergence falls within Hades Gap tolerance.")
    
    # Plot resonance curve with temperature envelope
    frequencies = np.linspace(60, 75, 1000)
    Q = 50  # Quality factor for granite
    resonance = 1 / (1 + Q**2 * ((frequencies - TARGET_FREQ) / TARGET_FREQ)**2)
    
    # Temperature-induced frequency spread
    freq_min = TARGET_FREQ * (v_min / required_velocity)
    freq_max = TARGET_FREQ * (v_max / required_velocity)
    
    plt.figure(figsize=(12, 7))
    plt.plot(frequencies, resonance, label='Acoustic Resonance (Q=50)', color='purple', linewidth=2)
    plt.axvline(x=TARGET_FREQ, color='red', linestyle='--', label=f'Target: {TARGET_FREQ:.4f} Hz')
    plt.axvline(x=64.0, color='gray', linestyle=':', label='Naive 64 Hz Estimate')
    plt.axvspan(TARGET_FREQ * (1-HADES_GAP), TARGET_FREQ * (1+HADES_GAP), 
                color='green', alpha=0.15, label='12.37% Hades Gap Tolerance')
    plt.axvspan(freq_min, freq_max, color='orange', alpha=0.1, 
                label=f'Temperature Envelope ({TEMP_RANGE[0]}–{TEMP_RANGE[1]}°C)')
    
    # Highlight √19 convergence point
    plt.axvline(x=separations / sqrt_19, color='blue', linestyle='-.', 
                label=f'√19 Convergence: {separations/sqrt_19:.4f} Hz')
    
    plt.title('Grand Gallery Phonon Bridge: 66.0688 Hz Resonance Simulation (v2.2)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Relative Amplitude')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('gallery_phonon_bridge_simulation_v2.2.png', dpi=300)
    print("\n[SAVE] Resonance plot saved as 'gallery_phonon_bridge_simulation_v2.2.png'")
    
    return {
        "Target Frequency (Hz)": TARGET_FREQ,
        "Required Velocity (m/s)": required_velocity,
        "Temperature-Adjusted Range (m/s)": (v_min, v_max),
        "√19 Convergence Deviation (%)": deviation * 100,
        "Within Hades Gap": deviation < HADES_GAP,
        "Within Temp Range": v_min <= required_velocity <= v_max
    }

if __name__ == "__main__":
    results = simulate_gallery_resonance_v2_2()
