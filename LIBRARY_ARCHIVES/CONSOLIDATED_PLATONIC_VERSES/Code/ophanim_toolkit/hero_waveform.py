import math

class HeroWaveformMapper:
    def __init__(self):
        # We model the story as the sum of a_n * sin(n * omega * t)
        # Using a normalized period 0 to 2*pi
        self.points = 100
        self.step = (2 * math.pi) / self.points
        
    def generate_harmonic(self, n: int, amplitude: float = 1.0):
        # Generates the sine wave for a given harmonic n
        wave = []
        for i in range(self.points):
            t = i * self.step
            val = amplitude * math.sin(n * t)
            wave.append(val)
        return wave
        
    def superposition(self, harmonics: list):
        # Sums the provided harmonic waveforms
        super_wave = [0.0] * self.points
        for wave in harmonics:
            for i in range(self.points):
                super_wave[i] += wave[i]
        return super_wave
        
    def compute_journey_stages(self):
        h1 = self.generate_harmonic(1, 1.0) # Identity
        h2 = self.generate_harmonic(2, 0.5) # Duality
        h3 = self.generate_harmonic(3, 0.33) # Structural Base
        h4 = self.generate_harmonic(4, 0.25) # Expansion
        h5 = self.generate_harmonic(5, 0.2) # Emotional Color
        h6 = self.generate_harmonic(6, 0.16) # Full Richness
        
        # The 7th harmonic is the non-equal tempered septimal tone. 
        # It creates narrative beat patterns and asymmetry.
        h7 = self.generate_harmonic(7, 0.14) 
        
        system_1_to_6 = self.superposition([h1, h2, h3, h4, h5, h6])
        system_with_7 = self.superposition([h1, h2, h3, h4, h5, h6, h7])
        
        return system_1_to_6, system_with_7

mapper = HeroWaveformMapper()
sys6, sys7 = mapper.compute_journey_stages()

# Analyzing the peak energy (Climax) and the asymmetry introduced by H7
peak_6 = max(sys6)
peak_7 = max(sys7)

# Finding where the max divergence happens
max_diff = 0
diff_index = 0
for i in range(len(sys6)):
    diff = abs(sys7[i] - sys6[i])
    if diff > max_diff:
        max_diff = diff
        diff_index = i

phase_angle = (diff_index / len(sys6)) * 360

print(f"--- Waveform Physics of the Hero's Journey ---")
print(f"Peak Constructive Interference (Harmonics 1-6): {peak_6:.2f}")
print(f"Asymmetric Peak with 7th Harmonic (Meaning): {peak_7:.2f}")
print(f"Maximum Semantic Tension (H7 Divergence) occurs at Phase Angle: {phase_angle:.1f}°")
print(f"This is the precise moment the story ruptures the closed system and generates 'Meaning'.")
