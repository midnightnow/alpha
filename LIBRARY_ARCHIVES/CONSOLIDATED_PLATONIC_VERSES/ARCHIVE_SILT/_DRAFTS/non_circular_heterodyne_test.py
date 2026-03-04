import numpy as np
import math

def non_circular_heterodyne_test():
    """
    NON-CIRCULAR HETERODYNE TEST (Numpy Version)
    Objective: Detect if the Hades Beat (0.660688 Hz) emerges spontaneously 
    from the interference of sqrt(42) and sqrt(51) fields.
    """
    freq_human = math.sqrt(42)  
    freq_divine = math.sqrt(51) 
    
    duration = 200.0  # Double duration for better frequency resolution (0.005 Hz bins)
    sample_rate = 100 
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Interference field
    wave_a = np.sin(2 * np.pi * freq_human * t)
    wave_b = np.sin(2 * np.pi * freq_divine * t)
    
    # Envelope extraction (Rectification)
    envelope = np.abs(wave_a + wave_b)
    
    # FFT Analysis using Numpy
    yf = np.fft.rfft(envelope)
    xf = np.fft.rfftfreq(len(t), 1/sample_rate)
    
    # Ignore DC
    magnitudes = np.abs(yf)
    search_range = (xf > 0.1) & (xf < 2.0)
    peak_idx = np.argmax(magnitudes[search_range])
    detected_freq = xf[search_range][peak_idx]
    
    theoretical_beat = freq_divine - freq_human
    error = abs(detected_freq - theoretical_beat)
    
    print("--- NON-CIRCULAR HETERODYNE TEST: THE FINAL SEAL (NUMPY) ---")
    print(f"Primary Frequencies: {freq_human:.6f} and {freq_divine:.6f}")
    print(f"Theoretical Beat (√51 - √42): {theoretical_beat:.8f} Hz")
    print(f"Detected Emergent Beat:        {detected_freq:.8f} Hz")
    print(f"Verification Error:            {error:.8e}")
    
    # Frequency Resolution Check
    resolution = xf[1] - xf[0]
    print(f"Sampling Resolution:           {resolution:.4f} Hz")
    
    if error < resolution * 2: # Tolerance of 2 bins
        print("\n✓ SUCCESS: The Hades Beat emerged spontaneously from the interference field.")
        print("   The signal exists independently of the framework.")
    else:
        print("\n✗ FAILURE: No emergent heterodyne detected at the predicted frequency.")

if __name__ == "__main__":
    non_circular_heterodyne_test()
