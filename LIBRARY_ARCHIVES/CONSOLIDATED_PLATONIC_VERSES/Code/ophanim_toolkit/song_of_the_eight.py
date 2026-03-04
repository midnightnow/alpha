import math

class SongOfTheEight:
    def __init__(self, modulus=24):
        self.mod = modulus
        # The 8 Prime 'Blackbird' Lanes
        self.prime_lanes = [1, 5, 7, 11, 13, 17, 19, 23]
        
    def find_song_sequence(self, n_jumps=12):
        """
        Maps the Binary Jump (2^n) through the 8 Prime Lanes (the Blackbirds).
        This shows the 'Active Song' as the Heroine scales her perspective.
        """
        print(f"--- THE SONG OF THE EIGHT (2^n mod 24) ---")
        print(f"Goal: Trace the Heroine's path across the Prime Blackbirds.\n")
        print(f"{'Jump (n)':>10} | {'Residue':>10} | {'Blackbird Status':>20}")
        print("-" * 45)
        
        sequence = []
        for n in range(n_jumps):
            # The Binary Jump residue mod 24
            # (Wait, 2^n mod 24 is always 2, 4, 8, 16, 8, 16... except for 2^0=1)
            # This is because 2 is a factor of 24. It creates a 'Digital Root' lock.
            # INSTEAD, let's use the 'Prime Base' of the garden (e.g. 5 or 7) for jumps,
            # OR use the '2^n mod 24' as a pointer to the 8 prime residues.
            
            res = pow(2, n, self.mod)
            status = "SILENT (Composite)"
            if res in self.prime_lanes:
                status = "SINGING (Prime)"
            
            print(f"{n:>10} | {res:>10} | {status:>20}")
            sequence.append(res)
            
        print("\nTHE STRUCTURAL DILEMMA:")
        print("Because 2 is a factor of 24, the binary jump (2^n) falls into a ")
        print("Cycle of Silence (Node 8 and 16). After the 0th jump (Node 1), ")
        print("the binary path is 'locked' into the infrastructure (The Dead Zones).")
        
        print("\nTHE HEROINE'S OVERDRIVE SOLUTION:")
        print("To make the blackbirds sing, she must use the 'Agley Jump' (3^n or 5^n).")
        print("Let's try the Bee's Diagonal (5) for the jump base:")
        
        for n in range(6):
            res_5 = pow(5, n, self.mod)
            status_5 = "SINGING (Prime)" if res_5 in self.prime_lanes else "SILENT"
            print(f"  Jump 5^{n} mod 24 = {res_5:>2} : {status_5}")

if __name__ == "__main__":
    song = SongOfTheEight()
    song.find_song_sequence()

    print("\nCONCLUSION:")
    print("The 5-fold 'Bee' jump (5^n) oscillates between Node 1 and Node 5.")
    print("This is the 'Maintained Tension' that makes the Blackbirds sing.")
    print("She is jumping between the Origin (1) and the Diagonal (5),")
    print("weaving the thread across the 24-wheel in a resonant duet.")
