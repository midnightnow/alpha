import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory
os.makedirs('/Users/studio/0platonicverses/Root51/output', exist_ok=True)

def plot_sqrt42_51_interference():
    print("Generating √42 vs √51 Interference Plot...")
    t = np.linspace(0, 100, 5000)
    
    f42 = np.sqrt(42)
    f51 = np.sqrt(51)
    
    wave42 = np.sin(f42 * t)
    wave51 = np.sin(f51 * t)
    
    combined = wave42 + wave51
    beat_freq = abs(f51 - f42)  # ≈ 0.6607
    envelope = 2 * np.cos(beat_freq * t / 2)
    
    plt.figure(figsize=(12, 5), facecolor='#050508')
    plt.plot(t, combined, color='#00f2ff', linewidth=0.8, label='√42 + √51 Superposition', alpha=0.7)
    plt.plot(t, envelope, color='#ff0055', linestyle='--', linewidth=1.5, label=f'Beat Envelope (Δf={beat_freq:.4f})')
    plt.plot(t, -envelope, color='#ff0055', linestyle='--', linewidth=1.5, alpha=0.5)
    
    plt.fill_between(t, combined, 0, where=(np.abs(combined) > 1.8), 
                     color='#ff0055', alpha=0.15, label='High-Energy Zones')
    
    plt.title(r"Interference of $\sqrt{42}$ and $\sqrt{51}$: The Next Resonance Layer", 
              color='white', fontsize=14)
    plt.xlabel("Time (orbital space)", color='gray')
    plt.ylabel("Amplitude (Stress)", color='gray')
    plt.legend(facecolor='#1a1c29', edgecolor='gray', labelcolor='white')
    plt.grid(True, linestyle=':', alpha=0.3)
    plt.savefig('/Users/studio/0platonicverses/Root51/output/sqrt42_51_interference.png', facecolor='#050508')
    plt.close()

def plot_radical_spectrum():
    print("Generating Radical Spectrum Plot...")
    n = np.arange(42, 52, 0.1)
    y = np.sqrt(n)
    
    plt.figure(figsize=(10, 4), facecolor='#050508')
    plt.plot(n, y, color='#00f2ff', linewidth=2)
    
    plt.scatter([42, 51], [np.sqrt(42), np.sqrt(51)], 
                color=['#ff0055', '#00ffaa'], s=100, zorder=5,
                label=['√42 (Europa)', '√51 (Enceladus?)'])
    
    plt.axvspan(42, 51, alpha=0.1, color='#ff0055', label='Δn = 9 = 3²')
    
    plt.title(r"Radical Spectrum: $\sqrt{n}$ from 42 to 51", color='white')
    plt.xlabel("n", color='gray')
    plt.ylabel(r"$\sqrt{n}$", color='gray')
    plt.legend(facecolor='#1a1c29', edgecolor='gray', labelcolor='white')
    plt.grid(True, linestyle=':', alpha=0.3)
    plt.savefig('/Users/studio/0platonicverses/Root51/output/radical_spectrum_42_51.png', facecolor='#050508')
    plt.close()

if __name__ == "__main__":
    plot_sqrt42_51_interference()
    plot_radical_spectrum()
    print("Visuals generated in /Users/studio/0platonicverses/Root51/output")
