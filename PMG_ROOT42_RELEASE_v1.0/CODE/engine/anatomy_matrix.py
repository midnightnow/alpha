import numpy as np

class AnatomyManifold:
    """
    De-Mythologized Engineering Version of File 005: ANATOMY
    Generates the literal 93-point (x, y, z) coordinate vertex matrix.
    
    Structure:
    - 3 Core Points (Z-Spike)  -> Identity / Energy
    - 30 Seed Points (Matrix)  -> Time / Light
    - 60 Shell Points (Geodesic)-> Space / Mass
    """

    def __init__(self, core_height=6.4807, shell_radius=7.1414): # sqrt(42) and sqrt(51)
        self.core_height = core_height
        self.shell_radius = shell_radius
        self.points = []
        
        # Build the architecture
        self._generate_core()
        self._generate_seed()
        self._generate_shell()

    def _generate_core(self):
        """
        The E-Manifold (3 Points).
        Aligned exactly on the Z-axis, defining the computational height.
        """
        half_h = self.core_height / 2.0
        self.points.extend([
            (0.0, 0.0, half_h),   # P1: Top
            (0.0, 0.0, 0.0),      # P2: Origin (Absolute Center)
            (0.0, 0.0, -half_h)   # P3: Bottom
        ])
        print(f"Generated 3 Core Points (Z-Spike). Height: {self.core_height:.4f}")

    def _generate_seed(self):
        """
        The V-Manifold (30 Points).
        Distributed as an Icosidodecahedron (30 vertices) to map the 5-12-13 matrix.
        Radius is scaled to the 12.37% Hades Gap beneath the Shell.
        """
        seed_radius = self.shell_radius * (1.0 - 0.1237)
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        # Vertices of an icosidodecahedron (all permutations of even sign changes)
        # Scaled to the seed_radius
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
        
        # Normalize and scale
        for x, y, z in base_points:
            mag = np.sqrt(x**2 + y**2 + z**2)
            self.points.append((
                (x / mag) * seed_radius,
                (y / mag) * seed_radius,
                (z / mag) * seed_radius
            ))
            
        print(f"Generated 30 Seed Points. Inner Radius: {seed_radius:.4f}")

    def _generate_shell(self):
        """
        The M/W-Manifold Turbine (60 Points).
        Distributed as a Truncated Icosahedron (Buckminsterfullerene) structure,
        forming the Root 51 Skybox boundary.
        """
        phi = (1 + np.sqrt(5)) / 2
        
        # Buckyball vertices (60 points total)
        # We will approximate this by generating structural permutations
        # For actual physics solvers, precise coordinates matter.
        base_points = []
        for x in [0]:
            for y in [1, -1]:
                for z in [3*phi, -3*phi]:
                    base_points.append((x, y, z))
                    base_points.append((y, z, x)) # Cyclic permutation
                    base_points.append((z, x, y))
                    
        for x in [2, -2]:
            for y in [1+2*phi, -(1+2*phi)]:
                for z in [phi, -phi]:
                    base_points.append((x, y, z))
                    base_points.append((y, z, x)) 
                    base_points.append((z, x, y))
                    
        for x in [1, -1]:
            for y in [2+phi, -(2+phi)]:
                for z in [2*phi, -2*phi]:
                    base_points.append((x, y, z))
                    base_points.append((y, z, x))
                    base_points.append((z, x, y))

        # We need exactly 60 unique coordinates
        unique_points = []
        for p in base_points:
            # Rounding to prevent floating point duplication
            rp = (round(p[0], 4), round(p[1], 4), round(p[2], 4))
            if rp not in unique_points:
                unique_points.append(rp)
        
        # Normalize to Root 51 boundary
        for x, y, z in unique_points:
            mag = np.sqrt(x**2 + y**2 + z**2)
            self.points.append((
                (x / mag) * self.shell_radius,
                (y / mag) * self.shell_radius,
                (z / mag) * self.shell_radius
            ))
            
        print(f"Generated 60 Shell Points (Skybox Turbine). Outer Radius: {self.shell_radius:.4f}")

    def get_vertex_matrix(self):
        """
        Returns the full 93-point numpy array for ingestion by solvers.
        """
        matrix = np.array(self.points)
        assert len(matrix) == 93, f"CRITICAL: System constructed {len(matrix)} points instead of 93."
        return matrix
        
    def export_csv(self, filename="05_anatomy_vertices.csv"):
        matrix = self.get_vertex_matrix()
        np.savetxt(filename, matrix, delimiter=",", header="X,Y,Z", comments="")
        print(f"\n[SUCCESS] 93-Point Matrix Exported to {filename}")


if __name__ == "__main__":
    print("="*60)
    print("05_ANATOMY: 93-POINT VECTOR MATRIX COMPILER")
    print("="*60)
    
    anatomy = AnatomyManifold()
    vertices = anatomy.get_vertex_matrix()
    
    # Boundary Check (Falsifiability)
    max_radius = np.max(np.linalg.norm(vertices, axis=1))
    print(f"\n[VALIDATION] Maximum Entity Radius: {max_radius:.4f}")
    if max_radius <= 7.1415:  # Tolerance for float rounding of sqrt(51)
        print("[VALIDATION] Geometry is geometrically contained within Root 51 Boundary.")
    else:
        print("[WARNING] Entity exceeds spatial boundaries!")
        
    anatomy.export_csv("/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/05_anatomy_vertices.csv")
    print("="*60)
