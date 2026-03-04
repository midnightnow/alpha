import math

class HeroJourneyMapper:
    def __init__(self):
        self.modulus = 24
        self.prime_moduli = {1, 5, 7, 11, 13, 17, 19, 23}
        self.maid_nodes = {3, 6, 9, 12, 15, 18, 21, 24}

    def map_value(self, value: float) -> int:
        node = round(value) % self.modulus
        if node == 0: node = 24
        return node

    def identify_node(self, node: int) -> str:
        if node in self.prime_moduli:
            return "KING'S NODE (Prime Residue Class)"
        elif node in self.maid_nodes:
            return "MAID'S NODE (Multiple of 3 / Digital Root Anchor)"
        else:
            return "STRUCTURAL NODE (Even / Non-Prime)"

    def map_harmonic(self, harmonic_num: int, ratio: tuple) -> dict:
        num, den = ratio
        decimal_ratio = num / den
        
        # 24 elements per octave. log2(ratio) gives the fraction of an octave.
        semitones_24 = 24 * math.log2(decimal_ratio)
        node = self.map_value(semitones_24)
        
        # We start at Node 24 (Tonic / The Home)
        # So we add the semitones to 24 and remap.
        absolute_node = self.map_value(24 + semitones_24)
        identity = self.identify_node(absolute_node)

        return {
            "harmonic": harmonic_num,
            "ratio": f"{num}:{den}",
            "decimal": decimal_ratio,
            "semitones_24": semitones_24,
            "absolute_node": absolute_node,
            "identity": identity,
            "degrees": absolute_node * 15
        }

mapper = HeroJourneyMapper()

# The typical overtone series ratios for harmonics 1 through 7
harmonics = [
    (1, (2, 1)), # Octave
    (2, (3, 2)), # Perfect Fifth
    (3, (4, 3)), # Perfect Fourth
    (4, (5, 4)), # Major Third
    (5, (6, 5)), # Minor Third
    (6, (7, 6)), # Septimal Minor Third
    (7, (8, 7))  # Septimal Major Second
]

print("--- The Harmonic Ladder of the Journey ---")
for h_num, ratio in harmonics:
    res = mapper.map_harmonic(h_num, ratio)
    print(f"H{res['harmonic']} ({res['ratio']}): Node {res['absolute_node']} [{res['degrees']}°] -> {res['identity']}")

