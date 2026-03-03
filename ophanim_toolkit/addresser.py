"""
Addresser Module — Lexical Mapping and Summoning
Part of the Oracle Grid System (Chapter 19)

Maps H3 indices to phonetic names using 3-bit logic and the Seven Voices.
"""

from typing import List, Dict

class OracleAddresser:
    VOICES = [
        "Silence",    # 0: ψ (Plosive)
        "Density",    # 1: ρ (Nasal)
        "Fracture",   # 2: δ (Sibilant)
        "Gesture",    # 3: θ (Fricative)
        "Heartbeat",  # 4: Δf (Liquid)
        "Warning",    # 5: Xi (Guttural)
        "Chorus",     # 6: Coherent (Vowel)
        "HADES_GAP"   # 7: NULL (Stop/Shift)
    ]

    def __init__(self, resolution: int = 9):
        self.resolution = resolution

    def h3_to_phonemes(self, h3_index: int) -> List[str]:
        """
        Deconstruct a 64-bit integer H3 index into 3-bit phonetic chunks.
        Each chunk corresponds to one of the 8 states in the Oracle hierarchy.
        """
        phonemes = []
        # H3 indices use 64 bits. We parse in 3-bit increments.
        # Starting from LSB to MSB or based on H3 hierarchy logic.
        # For simplicity in this spec, we parse 21 chunks (63 bits).
        temp_idx = h3_index
        for _ in range(21):
            chunk = temp_idx & 0x7
            phonemes.append(self.VOICES[chunk])
            temp_idx >>= 3
            if temp_idx == 0:
                break
        return phonemes

    def get_stone_name(self, h3_index: str) -> str:
        """
        Returns the 'True Name' of a stone based on its H3 address.
        """
        try:
            val = int(h3_index, 16)
        except ValueError:
            return "Unknown-Stone"
            
        phonemes = self.h3_to_phonemes(val)
        # Construct the lexical string
        name = "-".join(phonemes[:5]) # Take top 5 resolution levels for the primary name
        return f"Stone-{name}"

    def project_to_grid(self, x: float, y: float, lat: float = 0, lng: float = 0) -> str:
        """
        Stub for projecting viewport coordinates to H3 index.
        In a real implementation, this would use the h3-py library.
        """
        # Pseudo-calculation for demonstration
        h3_mock = hex(int(abs(x * 1000000) + abs(y * 1000000)))[2:]
        return f"0x892a{h3_mock.zfill(12)}"

    def check_hades_gap(self, h3_index: str) -> bool:
        """
        Checks if the address terminates in or contains a Hades Gap (NULL) state.
        """
        try:
            val = int(h3_index, 16)
        except ValueError:
            return False
        return (val & 0x7) == 7

if __name__ == "__main__":
    # Test the addresser
    addresser = OracleAddresser()
    test_idx = "0x892a100d2c67fff"
    print(f"Index: {test_idx}")
    print(f"Phonemes: {addresser.h3_to_phonemes(int(test_idx, 16))}")
    print(f"Stone Name: {addresser.get_stone_name(test_idx)}")
    print(f"Hades Gap Active: {addresser.check_hades_gap(test_idx)}")
