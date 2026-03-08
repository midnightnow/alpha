"""
category_mapper.py - Phase V: Category Morphism
Principia Mathematica Geometrica | Book 4: The Infinite Game
Translates abstract relationships into geometric vectors using the 39.4° Shear.
"""

import math
from typing import Dict, List, Tuple, Any
from .e8_hades_validator import PMGConstants

class CategoryMapper:
    """
    Transforms Semantic relationships (A -> B) into Geometric Morphisms.
    Uses the Unified Shear Angle (39.47°) as the mapping constant.
    """
    def __init__(self):
        self.shear_deg = PMGConstants.SHEAR_ANGLE_DEG
        self.shear_rad = math.radians(self.shear_deg)
        self.categories: Dict[str, Tuple[float, float]] = {}

    def define_category(self, name: str, base_coords: Tuple[float, float]):
        """Sets a starting point for a semantic category in the grid."""
        self.categories[name] = base_coords

    def calculate_morphism(self, source_cat: str, target_cat: str, distance: float) -> Tuple[float, float]:
        """
        Calculates the vector between two categories.
        The 'path' always follows the 39.47° shear.
        """
        if source_cat not in self.categories or target_cat not in self.categories:
            return (0.0, 0.0)
            
        # Delta calculation based on the shear angle
        # dx = distance * cos(theta), dy = distance * sin(theta)
        dx = distance * math.cos(self.shear_rad)
        dy = distance * math.sin(self.shear_rad)
        
        return (dx, dy)

    def translate_entropy_to_distance(self, entropy_level: float) -> float:
        """
        In the 'First Translation', Entropy is equated to spatial distance from the Focal Point.
        Distance = 1 / (1 - Entropy) - 1
        """
        if entropy_level >= 1.0: return 99.9 # Absolute void
        return 1.0 / (1.0 - entropy_level) - 1.0

    def get_categorical_path(self, start_label: str, end_label: str, intensity: float) -> Dict[str, Any]:
        """Maps a life-event or data-point into a grid vector."""
        dist = self.translate_entropy_to_distance(intensity)
        vector = self.calculate_morphism(start_label, end_label, dist)
        
        return {
            "morphism": f"{start_label} ➔ {end_label}",
            "shear_angle": self.shear_deg,
            "vector": vector,
            "magnitude": dist,
            "status": "CATEGORIZED"
        }

def test_mapper():
    mapper = CategoryMapper()
    mapper.define_category("Observation", (0.0, 0.0))
    mapper.define_category("Memory", (10.0, 10.0))
    
    # Map a moment of high entropy (0.8 drift) between Observation and Memory
    path = mapper.get_categorical_path("Observation", "Memory", intensity=0.8)
    print(f"Path Map: {path}")
    
    # Verify the vector follows the Shear
    dx, dy = path['vector']
    angle = math.degrees(math.atan2(dy, dx))
    print(f"Observed Angle: {angle:.2f}° (Target: {mapper.shear_deg}°)")

if __name__ == "__main__":
    test_mapper()
