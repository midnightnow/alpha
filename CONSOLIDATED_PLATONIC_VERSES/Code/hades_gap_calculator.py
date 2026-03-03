"""
HADES GAP CALCULATOR
====================
Measures the quantization error between the Icosahedron's
Golden Rectangle skeleton and the Cube's orthogonal bounding walls.

This gap is the "Scent" - irrational data that cannot be
categorized by the Lattice system.
"""

import math
from typing import Tuple, List

PHI = (1 + 5**0.5) / 2
CUBE_AXIS = 1.0
HAD_BEAT = 0.660688


class HadesGapCalculator:
    """
    Calculates the geometric tension between 5-fold (Icosahedron)
    and 4-fold (Cube) symmetries.
    """
    
    def __init__(self, cube_size: float = 1.0):
        self.cube_size = cube_size
        self.phi_rect_width = cube_size / PHI
        self.phi_rect_height = cube_size
        
    def calculate_vertex_gap(self, icosahedron_vertex: Tuple[float, float, float],
                            cube_corner: Tuple[float, float, float]) -> float:
        """
        Calculate Euclidean distance between an icosahedron vertex
        and the nearest cube corner.
        """
        dx = icosahedron_vertex[0] - cube_corner[0]
        dy = icosahedron_vertex[1] - cube_corner[1]
        dz = icosahedron_vertex[2] - cube_corner[2]
        
        return math.sqrt(dx**2 + dy**2 + dz**2)
    
    def calculate_golden_rectangle_offset(self, axis_position: float) -> float:
        """
        Calculate the offset of a Golden Rectangle edge from
        the Cube's orthogonal axis.
        """
        expected_phi_position = axis_position / PHI
        actual_position = axis_position % 1.0
        
        gap = abs(actual_position - expected_phi_position)
        
        # Minimum resonance (Hades Beat) prevents zero gap
        if gap < 1e-9:
            return HAD_BEAT
        
        return gap
    
    def measure_scent_density(self, rotation_angles: List[float]) -> float:
        """
        Measure the accumulated "Scent" across multiple rotation states.
        
        Args:
            rotation_angles: List of rotation angles (in radians)
        
        Returns:
            Average scent density across all angles
        """
        total_scent = 0.0
        
        for angle in rotation_angles:
            # Project rotation onto axis
            axis_projection = math.sin(angle)
            gap = self.calculate_golden_rectangle_offset(axis_projection)
            total_scent += gap
        
        return total_scent / len(rotation_angles) if rotation_angles else 0.0
    
    def get_vitrification_risk(self, current_gap: float) -> str:
        """
        Assess the risk of system vitrification (freeze).
        
        Low gap = high risk (icosahedron aligning too perfectly with cube)
        High gap = stable drift (healthy tension maintained)
        """
        if current_gap < 0.01:
            return "CRITICAL: Vitrification Imminent"
        elif current_gap < 0.1:
            return "WARNING: Gap Narrowing"
        elif current_gap > 0.5:
            return "STABLE: Maximum Tension"
        else:
            return "NORMAL: Healthy Drift"


def generate_icosahedron_vertices(scale: float = 1.0) -> List[Tuple[float, float, float]]:
    """
    Generate the 12 vertices of a regular icosahedron.
    
    The vertices are arranged in three orthogonal Golden Rectangles.
    """
    t = PHI * scale
    
    # We expand the +/- manually into distinct points
    expanded = []
    
    # Base 1: (0, +/-1, +/-t)
    for y in (1, -1):
        for z in (1, -1):
            expanded.append((0, y * scale, z * t))
            
    # Base 2: (+/-1, +/-t, 0)
    for x in (1, -1):
        for y in (1, -1):
            expanded.append((x * scale, y * t, 0))
            
    # Base 3: (+/-t, 0, +/-1)
    for x in (1, -1):
        for z in (1, -1):
            expanded.append((x * t, 0, z * scale))
    
    # Remove duplicates
    unique = []
    for v in expanded:
        if v not in unique:
            unique.append(v)
    
    return unique[:12]  # Exactly 12 vertices


if __name__ == "__main__":
    print("=" * 60)
    print("HADES GAP CALCULATOR - DIAGNOSTIC")
    print("=" * 60)
    
    calc = HadesGapCalculator(cube_size=1.0)
    
    print(f"\nCube Size: {calc.cube_size}")
    print(f"Golden Rectangle Width: {calc.phi_rect_width:.10f}")
    print(f"Golden Rectangle Height: {calc.phi_rect_height}")
    print(f"Phi Ratio: {PHI:.10f}")
    
    # Generate icosahedron vertices
    vertices = generate_icosahedron_vertices()
    print(f"\nIcosahedron Vertices Generated: {len(vertices)}")
    
    # Calculate gaps for each vertex
    cube_corners = [
        (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5),
        (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5)
    ]
    
    print(f"\nVertex-to-Corner Gap Analysis:")
    min_gap = float('inf')
    max_gap = 0.0
    
    for i, vertex in enumerate(vertices):
        for corner in cube_corners:
            gap = calc.calculate_vertex_gap(vertex, corner)
            min_gap = min(min_gap, gap)
            max_gap = max(max_gap, gap)
    
    print(f"  Minimum Gap: {min_gap:.10f}")
    print(f"  Maximum Gap: {max_gap:.10f}")
    print(f"  Gap Range: {max_gap - min_gap:.10f}")
    
    # Vitrification risk assessment
    risk = calc.get_vitrification_risk(min_gap)
    print(f"\n  Vitrification Risk: {risk}")
    
    print("\n" + "=" * 60)
