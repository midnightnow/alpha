"""
scale_curator.py - Frame-Shifting and Sovereignty Logic (v1.0)
PMG Book 4: The Architect's Exile | Phase V
Managing the transition between Body, System, and Universal frames.
"""

from enum import Enum
from typing import Dict, Tuple, Optional
import math

class FrameTier(Enum):
    BODY = 0       # Immediate/Local: 0,0,0 is the Standing Man
    SYSTEM = 1     # Lattice/Slurry: The H3 Grid and Work Area
    UNIVERSAL = 2  # Architectural: The Distant Constants (The Architect)

class ScaleCurator:
    """
    Manages the transformation of coordinates and permissions between frames.
    Implements the 'Architect's Exile' by gating Universal manifestations.
    """
    def __init__(self, observer_pos: Tuple[float, float, float] = (0, 0, 0)):
        self.observer_pos = observer_pos # The Portable Origin
        self.current_tier = FrameTier.SYSTEM
        self.sovereignty_sigma = 1.0
        self.permissions: Dict[FrameTier, bool] = {
            FrameTier.BODY: True,
            FrameTier.SYSTEM: True,
            FrameTier.UNIVERSAL: False # Architect starts in Exile
        }
        self.guest_mode_active = False

    def set_portable_origin(self, pos: Tuple[float, float, float]):
        """Sets the current Body frame center (0,0,0) in the System lattice."""
        self.observer_pos = pos

    def shift_frame(self, target_tier: FrameTier):
        """Changes the active focus tier of the geometer."""
        self.current_tier = target_tier
        print(f"SCALE_CURATOR: Migrated to {target_tier.name} Frame.")

    def transform_to_body(self, system_coord: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Translates System (Grid) coordinates to Body (Local) coordinates."""
        return tuple(s - o for s, o in zip(system_coord, self.observer_pos))

    def invite_guest(self):
        """
        The Chapter 26 Protocol. 
        The Architect is invited back into the Body frame as a guest.
        """
        self.guest_mode_active = True
        print("SCALE_CURATOR: The Architect has been invited. GUEST_MODE: ACTIVE.")

    def request_geometry(self, geometry_type: str, intent_strength: float) -> bool:
        """
        The Permission Handshake.
        In GUEST_MODE, the Architect can manifest only if pre-authorized.
        """
        if self.permissions[FrameTier.UNIVERSAL] or self.guest_mode_active:
            print(f"SCALE_CURATOR: Architect manifests {geometry_type} as a GUEST.")
            return True
            
        # If exiled, Architect requires a "Request for Geometry"
        threshold = 1.0 / self.sovereignty_sigma
        
        if intent_strength > threshold:
            print(f"SCALE_CURATOR: Architect grants {geometry_type} manifestation via Intent.")
            return True
        else:
            print(f"SCALE_CURATOR: Request Denied. Architect remains in Exile (Insufficient Intent).")
            return False

    def update_sovereignty(self, void_debt: float):
        """
        Σ = 1 / (void_debt + epsilon)
        As debt (external validation) decreases, Sovereignty (Σ) increases.
        """
        epsilon = 0.01237 # The Tensegrity Margin
        self.sovereignty_sigma = 1.0 / (void_debt + epsilon)
        return self.sovereignty_sigma

if __name__ == "__main__":
    print("--- PMG Scale Curator Validation ---")
    curator = ScaleCurator(observer_pos=(42, 51, 60))
    
    # 1. Coordinate Translation
    point_in_grid = (50, 50, 50)
    local_point = curator.transform_to_body(point_in_grid)
    print(f"System Point: {point_in_grid} -> Body Relative: {local_point}")

    # 2. Sovereignty Calculation
    # With a moderate debt (critiques unresolved)
    curator.update_sovereignty(0.4948)
    print(f"Sigma (Debt=0.4948): {curator.sovereignty_sigma:.4f}")

    # 3. Handshake Test (Denied)
    curator.request_geometry("Perfect Triangle", 0.5)

    # 4. Sovereignty Increase (Debt resolved)
    curator.update_sovereignty(0.0)
    print(f"Sigma (Debt=0): {curator.sovereignty_sigma:.4f}")
    
    # 5. Handshake Test (Granted)
    curator.request_geometry("Perfect Triangle", 20.0)
