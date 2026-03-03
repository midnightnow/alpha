# --- TRIADIC_CHORD_GENERATOR.py ---
# The Audio Seal for Phase II of the Root42 Archive

import numpy as np
from scipy.io import wavfile
import os

def generate_audio_seal():
    # 1. Audio Configuration
    SAMPLE_RATE = 44100
    DURATION = 15.0 # Seconds (Long enough to hear the phasing)
    
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    
    # 2. The Radical Frequencies (Scaled x100)
    # We scale up because the raw roots (6Hz, 7Hz) are infrasonic.
    # x100 places them in the audible mid-range.
    FREQ_42 = np.sqrt(42) * 100  # ~648.07 Hz
    FREQ_51 = np.sqrt(51) * 100  # ~714.14 Hz
    FREQ_60 = np.sqrt(60) * 100  # ~774.60 Hz
    
    # 3. The Oscillator Synthesis
    # We use sine waves for purity, representing the "Glass" nature of the artifact.
    
    # Layer 1: The Hexagon (Base) - High Amplitude
    wave_42 = 0.5 * np.sin(2 * np.pi * FREQ_42 * t)
    
    # Layer 2: The Lattice (Interference) - Medium Amplitude
    wave_51 = 0.4 * np.sin(2 * np.pi * FREQ_51 * t)
    
    # Layer 3: The Resolution (Stabilizer) - Low Amplitude
    # This adds the "sheen" to the sound
    wave_60 = 0.25 * np.sin(2 * np.pi * FREQ_60 * t)
    
    # 4. The "Purple Hum" Modulation (LFO)
    # We add a subtle amplitude modulation at the beat frequency (66Hz / 100 = 0.66Hz)
    # This makes the sound "breathe" physically.
    beat_freq = (FREQ_51 - FREQ_42) / 100 # ~0.66 Hz
    lfo = 1.0 + 0.1 * np.sin(2 * np.pi * beat_freq * t)
    
    # Combine and Modulate
    combined_wave = (wave_42 + wave_51 + wave_60) * lfo
    
    # 5. Normalization and Export
    # Normalize to 16-bit range
    normalized_wave = np.int16(combined_wave / np.max(np.abs(combined_wave)) * 32767)
    
    filename = "Root42_Triadic_Seal_66Hz.wav"
    wavfile.write(filename, SAMPLE_RATE, normalized_wave)
    
    print(f"✓ Audio Seal Generated: {filename}")
    print(f"  Primary Beat: {FREQ_51 - FREQ_42:.2f} Hz")
    print(f"  Secondary Beat: {FREQ_60 - FREQ_51:.2f} Hz")

if __name__ == "__main__":
    generate_audio_seal()
