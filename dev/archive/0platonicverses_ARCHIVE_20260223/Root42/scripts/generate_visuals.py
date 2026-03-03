import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Create output directory
os.makedirs('/Users/studio/0platonicverses/Root42/output', exist_ok=True)

def generate_spherical_map():
    print("Generating Spherical Stress Map...")
    fig = plt.figure(figsize=(10, 10), facecolor='#050508')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#050508')

    u = np.linspace(0, 2 * np.pi, 200)
    v = np.linspace(0, np.pi, 200)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    phi, theta = np.meshgrid(v, u)
    intensity = np.abs(np.sin(6 * theta) * np.sin(6 * phi) + np.sin(7 * theta) * np.sin(7 * phi))
    
    colors = plt.cm.magma(intensity)
    surf = ax.plot_surface(x, y, z, facecolors=colors, rstride=1, cstride=1, antialiased=False, shade=False)

    ax.set_axis_off()
    plt.title("The Resonant Sphere: Spherical Map of √42", color='white', y=0.95, fontsize=15)
    
    plt.savefig('/Users/studio/0platonicverses/Root42/output/sqrt42_sphere.png', facecolor='#050508')
    plt.close()

def generate_audio_waveform():
    print("Generating Acoustic Remainder Waveform...")
    duration = 5.0
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    freq_hex = 60.0 
    freq_hep = 70.0
    
    wave = np.sin(2 * np.pi * freq_hex * t) + np.sin(2 * np.pi * freq_hep * t)
    
    plt.figure(figsize=(10, 4), facecolor='#050508')
    plt.plot(t[:2000], wave[:2000], color='#ff0055', linewidth=1)
    plt.title("Acoustic Remainder Waveform (6:7 Beat)", color='white')
    plt.axis('off')
    plt.savefig('/Users/studio/0platonicverses/Root42/output/acoustic_hum.png', facecolor='#050508')
    plt.close()

def generate_stress_heatmap():
    print("Generating Europa Stress Map Heatmap...")
    lon = np.linspace(-np.pi, np.pi, 500)
    lat = np.linspace(-np.pi/2, np.pi/2, 250)
    LON, LAT = np.meshgrid(lon, lat)

    shell_stress = np.cos(6 * LON) * np.cos(LAT)
    delta_phi = 0.0801 
    tide_stress = np.cos(7 * LON + delta_phi) * np.cos(LAT)
    interference = np.abs(shell_stress - tide_stress)

    plt.figure(figsize=(12, 6), facecolor='#050508')
    plt.imshow(interference, extent=[-180, 180, -90, 90], cmap='magma', aspect='auto')
    
    for i in range(-2, 3):
        x = np.linspace(-180, 180, 100)
        y = 30 * np.sin(np.deg2rad(x) * (np.sqrt(42)/2) + i) 
        plt.plot(x, y, color='#00f2ff', alpha=0.3, linewidth=1, linestyle='--')

    plt.title(r"Empirical Stress Map: $\sqrt{42}$ Resonance vs. Europa Lineae", color='white', fontsize=15)
    plt.xlabel("Longitude", color='gray')
    plt.ylabel("Latitude", color='gray')
    plt.colorbar(label="Energy Density (Tidal Heating)")
    plt.tick_params(colors='gray')
    
    plt.savefig('/Users/studio/0platonicverses/Root42/output/europa_stress_map.png', facecolor='#050508')
    plt.close()

if __name__ == "__main__":
    generate_spherical_map()
    generate_audio_waveform()
    generate_stress_heatmap()
    print("All visuals generated in /Users/studio/0platonicverses/Root42/output")
