import math

class HeroicHarmonicsMapper:
    def __init__(self):
        self.modulus = 24
        self.prime_moduli = {1, 5, 7, 11, 13, 17, 19, 23}
        
    def map_value(self, value):
        node = round(value) % self.modulus
        if node == 0: node = 24
        return node
        
    def map_harmonic(self, n, ratio):
        # We can map the harmonic index itself (n) and the ratio in cents or semitones onto the 24-key system.
        # 1 Octave = 1200 cents. 24 wheel = 24 "keys" / quarter tones? 
        # If 24 is the full circle (1 octave), then position = 24 * log2(ratio)
        semitones_24 = 24 * math.log2(ratio)
        node = self.map_value(semitones_24)
        is_prime = node in self.prime_moduli
        
        return {
            "Harmonic": n,
            "Ratio": ratio,
            "Node_24": node,
            "Is_Prime_Lane": is_prime
        }

mapper = HeroicHarmonicsMapper()
harmonics = [
    (1, 2/1),
    (2, 3/2),
    (3, 4/3),
    (4, 5/4),
    (5, 6/5),
    (6, 7/6),
    (7, 8/7)
]

print("--- Heroic Harmonics mapped to 24-Wheel ---")
for n, ratio in harmonics:
    res = mapper.map_harmonic(n, ratio)
    status = "BLACKBIRD (Prime)" if res["Is_Prime_Lane"] else "STRUCTURAL/MAID"
    print(f"Harmonic {n} ({ratio:.2f}): Node {res['Node_24']} -> {status}")

