import math

class TilingShearCalculator:
    def __init__(self):
        self.full_circle = 360.0
        
    def calculate_internal_angle(self, n):
        return (n - 2) * 180.0 / n
        
    def calculate_central_angle(self, n):
        return self.full_circle / n
        
    def compute_shear(self):
        # 4-fold (The Home/Grid)
        sq_int = self.calculate_internal_angle(4)
        sq_center = self.calculate_central_angle(4)
        sq_vertex_sum = 4 * sq_int
        
        # 5-fold (The Departure/Hero)
        pent_int = self.calculate_internal_angle(5)
        pent_center = self.calculate_central_angle(5)
        pent_vertex_max = 3 * pent_int # Maximum pentagons around a vertex without overlapping
        pent_gap = self.full_circle - pent_vertex_max
        
        # The Shear / Phase Divergence
        # If the 5 tries to align its central rotational phases with the 4, 
        # the "slip" or "shear" at each step is the difference in their central angles.
        phase_shear = sq_center - pent_center
        
        # The Internal Structural Divergence
        internal_shear = pent_int - sq_int

        return {
            "Grid_Internal": sq_int,
            "Hero_Internal": pent_int,
            "Internal_Shear": internal_shear,
            "Grid_Central": sq_center,
            "Hero_Central": pent_center,
            "Phase_Shear": phase_shear,
            "Pentagon_Vertex_Gap": pent_gap
        }

calc = TilingShearCalculator()
res = calc.compute_shear()

print("--- GEOMETRIC SHEAR: 5-FOLD FORCED INTO 4-FOLD GRID ---")
print(f"Grid (4) Internal Angle: {res['Grid_Internal']}°")
print(f"Hero (5) Internal Angle: {res['Hero_Internal']}°")
print(f"Internal Structural Shear: {res['Internal_Shear']}°")
print(f"---")
print(f"Grid Phase (Rotation Step): {res['Grid_Central']}°")
print(f"Hero Phase (Rotation Step): {res['Hero_Central']}°")
print(f"Rotational Phase Shear: {res['Phase_Shear']}°")
print(f"---")
print(f"Tiling Rupture (The Gap): {res['Pentagon_Vertex_Gap']}° (3 Pentagons = 324° -> 36° Void)")
