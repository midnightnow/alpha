import math

class BeeDiagonalBrace:
    def __init__(self, mod=24):
        self.mod = mod
        self.deg_per_node = 360.0 / self.mod
        
    def calculate_bracing(self):
        """
        Calculates how the 5-fold 'Bee' diagonal provides structural stability 
        between the 4-fold 'Bread' grid and the 6-fold 'Honey' efficiency.
        """
        # Symmetry Nodes
        bread = [i * (self.mod // 4) for i in range(4)]  # [0, 6, 12, 18]
        honey = [i * (self.mod // 6) for i in range(6)]  # [0, 4, 8, 12, 16, 20]
        bee = [i * (self.mod / 5.0) for i in range(5)]   # [0, 4.8, 9.6, 14.4, 19.2]
        
        print(f"--- THE BEE'S DIAGONAL: 5-FOLD BRACING ANALYSIS ---")
        print(f"4-Fold (Bread): {bread}")
        print(f"6-Fold (Honey): {honey}")
        print(f"5-Fold (Bee):   {[round(n, 2) for n in bee]}\n")
        
        print(f"{'Bee Node':>10} | {'Dist to Bread':>15} | {'Dist to Honey':>15}")
        print("-" * 45)
        
        for b_node in bee:
            # Find closest bread node
            dist_bread = min([abs(b_node - br) for br in bread])
            # Find closest honey node
            dist_honey = min([abs(b_node - h) for h in honey])
            
            print(f"{b_node:>10.1f} | {dist_bread:>15.2f} | {dist_honey:>15.2f}")
            
        print("\nCONCLUSION: THE 18-DEGREE SHEAR")
        print("The Bee Node at 4.8 (the 1st step) is exactly 1.2 units from the Bread Node at 6.")
        print(f"1.2 units * {self.deg_per_node} deg/unit = {1.2 * self.deg_per_node:.1f} degrees.")
        print("This is the 'Grid-Break' angle. The Bee is the physical brace that stops ")
        print("the 4-fold Bread from collapsing under the 6-fold Honey pressure.")

if __name__ == "__main__":
    brace = BeeDiagonalBrace()
    brace.calculate_bracing()
