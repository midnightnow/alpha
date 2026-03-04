import math

class StorySpectra:
    def __init__(self, points=1000):
        self.points = points
        self.omega = 2 * math.pi
        self.t_values = [i / self.points for i in range(self.points)]
        
    def generate_harmonic(self, n: int, amplitude: float):
        wave = []
        for t in self.t_values:
            wave.append(amplitude * math.sin(n * self.omega * t))
        return wave
        
    def calculate_envelope(self, wave):
        # A simple envelope calculation: RMS over a small moving window
        window_size = 50
        envelope = []
        for i in range(len(wave)):
            start = max(0, i - window_size//2)
            end = min(len(wave), i + window_size//2)
            window = wave[start:end]
            rms = math.sqrt(sum([x**2 for x in window]) / len(window))
            envelope.append(rms)
        return envelope

    def compute_narrative_intensity(self):
        # Amplitudes roughly following 1/n 
        h1 = self.generate_harmonic(1, 1.0)
        h2 = self.generate_harmonic(2, 0.5)
        h3 = self.generate_harmonic(3, 0.33)
        h4 = self.generate_harmonic(4, 0.25)
        h5 = self.generate_harmonic(5, 0.2)
        h6 = self.generate_harmonic(6, 0.16)
        
        # The 7th harmonic creates the crucial beating/tension
        h7 = self.generate_harmonic(7, 0.14)
        
        # Superposition 1-6 (The Established System)
        sys6 = [sum(x) for x in zip(h1, h2, h3, h4, h5, h6)]
        env6 = self.calculate_envelope(sys6)
        
        # Superposition 1-7 (The Rupture / Meaning)
        sys7 = [sum(x) for x in zip(h1, h2, h3, h4, h5, h6, h7)]
        env7 = self.calculate_envelope(sys7)
        
        # Calculate divergence in the envelope (Psychoacoustic Tension)
        tension = []
        for i in range(self.points):
            tension.append(abs(env7[i] - env6[i]))
            
        max_tension = max(tension)
        max_t_index = tension.index(max_tension)
        phase_angle = (max_t_index / self.points) * 360
        
        return {
            "max_tension": max_tension,
            "phase_angle": phase_angle,
            "mean_energy_6": sum(env6) / len(env6),
            "mean_energy_7": sum(env7) / len(env7)
        }

spectra = StorySpectra()
results = spectra.compute_narrative_intensity()

print("\n--- SPECTRAL DENSITY ANALYSIS OF NARRATIVE TENSION ---")
print(f"Max Perceptual Tension (Envelope Divergence): {results['max_tension']:.4f}")
print(f"Phase Angle of Maximum Tension: {results['phase_angle']:.1f}°")
print(f"Mean Energy (System 1-6): {results['mean_energy_6']:.4f}")
print(f"Mean Energy (System 1-7): {results['mean_energy_7']:.4f}")
