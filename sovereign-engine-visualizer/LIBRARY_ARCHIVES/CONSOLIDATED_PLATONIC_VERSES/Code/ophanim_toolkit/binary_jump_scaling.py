import math

class BinaryJumpScaling:
    def __init__(self, semi_prime=77):
        self.x = semi_prime
        
    def execute_scaling_jumps(self, max_n=10):
        """
        Demonstrates the 'Polynomial Scaling' of the binary jump.
        Instead of counting linearly (1, 2, 3...), we jump by factors of 2.
        """
        print(f"--- BINARY JUMP SCALING: x = {self.x} ---")
        print(f"Goal: Find the prime interference nodes in polynomial time.\n")
        print(f"{'Jump (n)':>10} | {'Linear Position':>20} | {'Mod Residue (2^n)':>20}")
        print("-" * 60)
        
        for n in range(max_n):
            # The 'Linear Position' grows exponentially
            linear_pos = 2**n
            # The 'Mod Residue' stays within the 24-Wheel/Semi-prime bounds
            res = pow(2, n, self.x)
            
            # Check for factor-leaking (Polynomial Factorization Check)
            g = math.gcd(res - 1, self.x)
            factor_found = f" [FOUND FACTOR: {g}]" if 1 < g < self.x else ""
            
            print(f"{n:>10} | {linear_pos:>20} | {res:>20}{factor_found}")
            
        return

if __name__ == "__main__":
    # Test with 77 (7 * 11)
    jumper = BinaryJumpScaling(77)
    jumper.execute_scaling_jumps(10)
    
    print("\nCONCLUSION: THE PERCEPTION OVERDRIVE")
    print("By the 10th jump (n=9), we have explored a virtual distance of 512,")
    print("but performed only 9 modular multiplications. This is the ")
    print("'Polynomial Perspective'—the Heroine's ability to cross the garden")
    print("without walking the entire line.")
