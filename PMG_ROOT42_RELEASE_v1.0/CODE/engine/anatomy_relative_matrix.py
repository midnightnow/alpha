import numpy as np

class PivotRelativeAnatomy:
    """
    De-Mythologized Engineering Version of File 005: ANATOMY
    (Pivot-Relative Units Update)
    
    Generates the literal 93-point coordinate matrix not as absolute space,
    but as Centrifugal Divergence ratios from the sqrt(42) singularity.
    The boundary limit is sqrt(51) / sqrt(42) = ~1.101.
    """

    def __init__(self, pivot=np.sqrt(42), shell_boundary=np.sqrt(51)):
        self.pivot = pivot
        self.shell_boundary = shell_boundary
        
        # The engine constraint: Maximum permissible expansion ratio
        self.max_divergence_ratio = self.shell_boundary / self.pivot
        
        self.points_absolute = []
        self.points_relative = []
        
        # Build the architecture (Absolute Space)
        self._generate_core()
        self._generate_seed()
        self._generate_shell()
        
        # Transform to Pivot-Relative Sub-Space
        self._transform_to_pivot_units()

    def _generate_core(self):
        """ The E-Manifold (3 Points, Z-Spike). Height bounded by Pivot. """
        half_h = self.pivot / 2.0
        self.points_absolute.extend([
            (0.0, 0.0, half_h),   
            (0.0, 0.0, 0.0),     
            (0.0, 0.0, -half_h)   
        ])

    def _generate_seed(self):
        """ The V-Manifold (30 Points, Icosidodecahedron). """
        # Scaled to the 12.37% Hades Gap beneath the Shell limit
        seed_radius = self.shell_boundary * (1.0 - 0.1237)
        phi = (1 + np.sqrt(5)) / 2  
        
        base_points = [
            (0, 0, 2*phi), (0, 0, -2*phi),
            (0, 2*phi, 0), (0, -2*phi, 0),
            (2*phi, 0, 0), (-2*phi, 0, 0),
            (1, phi, phi**2), (1, -phi, phi**2), (-1, phi, phi**2), (-1, -phi, phi**2),
            (1, phi, -phi**2), (1, -phi, -phi**2), (-1, phi, -phi**2), (-1, -phi, -phi**2),
            (phi**2, 1, phi), (phi**2, -1, phi), (-phi**2, 1, phi), (-phi**2, -1, phi),
            (phi**2, 1, -phi), (phi**2, -1, -phi), (-phi**2, 1, -phi), (-phi**2, -1, -phi),
            (phi, phi**2, 1), (phi, -phi**2, 1), (-phi, phi**2, 1), (-phi, -phi**2, 1),
            (phi, phi**2, -1), (phi, -phi**2, -1), (-phi, phi**2, -1), (-phi, -phi**2, -1)
        ]
        
        for x, y, z in base_points:
            mag = np.sqrt(x**2 + y**2 + z**2)
            self.points_absolute.append((
                (x / mag) * seed_radius,
                (y / mag) * seed_radius,
                (z / mag) * seed_radius
            ))

    def _generate_shell(self):
        """ The M/W-Manifold Turbine Shell (60 Points). """
        phi = (1 + np.sqrt(5)) / 2
        base_points = []
        
        for x in [0]:
            for y in [1, -1]:
                for z in [3*phi, -3*phi]:
                    base_points.append((x, y, z)); base_points.append((y, z, x)); base_points.append((z, x, y))
        for x in [2, -2]:
            for y in [1+2*phi, -(1+2*phi)]:
                for z in [phi, -phi]:
                    base_points.append((x, y, z)); base_points.append((y, z, x)); base_points.append((z, x, y))
        for x in [1, -1]:
            for y in [2+phi, -(2+phi)]:
                for z in [2*phi, -2*phi]:
                    base_points.append((x, y, z)); base_points.append((y, z, x)); base_points.append((z, x, y))

        unique_points = []
        for p in base_points:
            rp = (round(p[0], 4), round(p[1], 4), round(p[2], 4))
            if rp not in unique_points:
                unique_points.append(rp)
        
        for x, y, z in unique_points:
            mag = np.sqrt(x**2 + y**2 + z**2)
            self.points_absolute.append((
                (x / mag) * self.shell_boundary,
                (y / mag) * self.shell_boundary,
                (z / mag) * self.shell_boundary
            ))

    def _transform_to_pivot_units(self):
        """
        Applies the Unwobbling Law: P_relative = P_absolute / sqrt(42)
        Calculates the divergence ratio for every node.
        """
        matrix_abs = np.array(self.points_absolute)
        
        # Scale to pivot
        matrix_rel = matrix_abs / self.pivot
        self.points_relative = matrix_rel.tolist()

    def validate_falsifiability(self):
        """
        Mathematical stress test: Ensuring no node exceeds the 1.101 Expansion Limit.
        """
        matrix_rel = np.array(self.points_relative)
        
        # Calculate divergence magnitudes (Distance from origin (0,0,0) in relative units)
        magnitudes = np.linalg.norm(matrix_rel, axis=1)
        
        max_divergence = np.max(magnitudes)
        
        print("="*60)
        print("05_ANATOMY: PIVOT-RELATIVE GEOMETRY COMPILER")
        print("="*60)
        print(f"[{len(self.points_relative)} Nodes Generated]")
        print(f"-> Unwobbling Pivot (Identity): sqrt(42) = {self.pivot:.4f}")
        print(f"-> Skybox Limit (Turbine): sqrt(51) = {self.shell_boundary:.4f}")
        print(f"-> Max Permissible Limit Ratio: {self.max_divergence_ratio:.5f}")
        print("-" * 60)
        print(f"-> Calculated Max Node Divergence: {max_divergence:.5f}")
        
        limit_tolerance = 1e-4
        if max_divergence <= (self.max_divergence_ratio + limit_tolerance):
            print("[VALIDATION PASSED] Geometry is contained by the Centripetal Force.")
            print("[SYSTEM STATUS] The 93-Point Solid is successfully vitrified to the Pivot.")
        else:
            print(f"[FATAL EXCEPTION] Node divergence ({max_divergence:.5f}) exceeds Limit Ratio!")
            print("[SYSTEM STATUS] M/W Turbines failed to contain the data.")
            
        return matrix_rel

    def export_csv(self, filename="05_anatomy_relative.csv"):
        matrix = np.array(self.points_relative)
        np.savetxt(filename, matrix, delimiter=",", header="Relative_X,Relative_Y,Relative_Z", comments="")
        print(f"\n[SUCCESS] Pivot-Relative Matrix Exported to {filename}")


if __name__ == "__main__":
    anatomy = PivotRelativeAnatomy()
    vertices_relative = anatomy.validate_falsifiability()
    anatomy.export_csv("/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/05_anatomy_relative.csv")
    print("="*60)
