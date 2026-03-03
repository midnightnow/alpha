import math

class SquareShearSimulator:
    def __init__(self, side_length=4.0):
        # The base Enclosure (The 4)
        self.L = side_length
        # The initial diagonal (The 5)
        self.d_initial = math.sqrt(2 * (self.L**2)) # If it's a perfect square 4x4, diagonal is 5.65.
                                                    # Wait, we are talking about a 3-4-5 triangle.
                                                    # Let's model a 3x4 rectangle.
        self.w = 4.0
        self.h = 3.0
        self.d_ideal = 5.0 # The perfect Pythagorean brace
        
    def apply_shear(self, shear_angle_degrees):
        """
        Applies a shear force to the 3x4 rectangle, turning it into a parallelogram.
        We calculate the new length of the diagonal to show how much the '5' must stretch/compress.
        """
        shear_rad = math.radians(shear_angle_degrees)
        
        # When sheared, the top shifts by dx = h * tan(theta)
        # Assuming the base stays flat on the x-axis from (0,0) to (4,0)
        # The top left corner moves from (0,3) to (dx, 3)
        # The top right corner moves from (4,3) to (4+dx, 3)
        
        dx = self.h * math.tan(shear_rad)
        
        # The Main Diagonal goes from (0,0) to (4+dx, 3)
        d_main = math.sqrt((self.w + dx)**2 + self.h**2)
        
        # The Cross Diagonal goes from (4,0) to (dx, 3)
        d_cross = math.sqrt((dx - self.w)**2 + self.h**2)
        
        return {
            "Shear_Angle": shear_angle_degrees,
            "Top_Displacement": dx,
            "Main_Diagonal": d_main,
            "Main_Delta": d_main - self.d_ideal,
            "Cross_Diagonal": d_cross,
            "Cross_Delta": d_cross - self.d_ideal
        }

if __name__ == "__main__":
    sim = SquareShearSimulator()
    print("--- THE PHYSICS OF SHEAR: THE 5-BRACE ---")
    print(f"Initial State: Base=4, Height=3. Ideal Diagonal Brace = {sim.d_ideal}")
    print("Applying structural entropy (Shear Force)...\n")
    
    angles = [1, 5, 10, 15]
    for angle in angles:
        res = sim.apply_shear(angle)
        print(f"Shear Angle: {res['Shear_Angle']}°")
        print(f"  Frame Displacement: {res['Top_Displacement']:.3f} units")
        print(f"  Tension on the Hero (Main Brace): {res['Main_Diagonal']:.3f} (Delta: {res['Main_Delta']:+.3f})")
        print(f"  Compression on the Shadow (Cross Brace): {res['Cross_Diagonal']:.3f} (Delta: {res['Cross_Delta']:+.3f})\n")
    
    print("CONCLUSION:")
    print("Without the 5-Brace, the 3x4 grid offers ZERO resistance to shear.")
    print("The 4-Enclosure is a socially repeating pattern, but geometrically fluid.")
    print("The Hero (5) is the rigid verification metric that locks the narrative into structural reality.")
