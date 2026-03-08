import math

class QuasiPeriodicGarden:
    def __init__(self, n_sides=5, grid_size=24):
        self.n = n_sides
        self.grid = grid_size
        self.exterior_angle = 360.0 / self.n
        
    def analyze_tiling_gap(self):
        """
        Calculates the angular deficit when trying to tile a 360-degree point
        using n-sided regular polygons.
        """
        interior_angle = (self.n - 2) * 180.0 / self.n
        
        # How many fit into 360?
        count = 360.0 / interior_angle
        remainder = 360.0 % interior_angle
        
        print(f"--- QUASI-PERIODIC GARDEN ANALYSIS (n={self.n}) ---")
        print(f"Interior Angle of a {self.n}-gon: {interior_angle} degrees.")
        print(f"Number of units around a vertex: {count:.2f}")
        print(f"Angular Deficit (The Gap): {360.0 - (math.floor(count) * interior_angle):.2f} degrees.\n")
        
        print("OBSERVATION:")
        if remainder == 0:
            print(f"The {self.n}-gon tiles the plane PERFECTLY (Periodic).")
        else:
            print(f"The {self.n}-gon leaves a GHOST REMAINDER (Aperiodic/Quasi-Periodic).")
            print("To fill this gap, the structure must buckle or introduce a second shape.")
            print(f"On the {self.grid}-wheel, this is the 18-degree shear point.")

if __name__ == "__main__":
    # The House (4-fold)
    house = QuasiPeriodicGarden(4)
    house.analyze_tiling_gap()
    print("\n" + "="*40 + "\n")
    # The Hive (6-fold)
    hive = QuasiPeriodicGarden(6)
    hive.analyze_tiling_gap()
    print("\n" + "="*40 + "\n")
    # The Garden (5-fold)
    garden = QuasiPeriodicGarden(5)
    garden.analyze_tiling_gap()
