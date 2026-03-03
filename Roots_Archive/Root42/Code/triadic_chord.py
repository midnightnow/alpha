# assets/audio/triadic_chord.py
import numpy as np
from scipy.io import wavfile
import os

def generate_triadic_chord(duration=10.0, sample_rate=44100):
    """
    Sonify the √42 : √51 : √60 triple as audio.
    Scaled to audible range (×100).
    """
    print("Generating triadic chord audio...")
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Triadic frequencies (scaled ×100)
    f42 = np.sqrt(42) * 100   # 648.07 Hz
    f51 = np.sqrt(51) * 100   # 714.14 Hz
    f60 = np.sqrt(60) * 100   # 774.60 Hz
    
    # Amplitude weighting (42=engine, 51=lattice, 60=resolution)
    wave = (
        0.4 * np.sin(2 * np.pi * f42 * t) +
        0.4 * np.sin(2 * np.pi * f51 * t) +
        0.2 * np.sin(2 * np.pi * f60 * t)
    )
    
    # Normalize to 16-bit PCM
    wave_normalized = np.int16(wave / np.max(np.abs(wave)) * 32767)
    
    output_path = '/Users/studio/0platonicverses/Root42/Assets/output/triadic_chord_42_51_60.wav'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    wavfile.write(output_path, sample_rate, wave_normalized)
    
    print(f"✓ {output_path} exported")
    print(f"   Freqs: {f42:.2f}Hz, {f51:.2f}Hz, {f60:.2f}Hz")
    print(f"   Beat: {f51-f42:.2f}Hz (66 Hz pulse)")

if __name__ == "__main__":
    generate_triadic_chord()
