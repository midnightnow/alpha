# system_integrity.py
# Tracks the structural integrity of the Lattice vs the Babble Infection.

class NullZone:
    """
    Represents the encroaching edge of De-allocation.
    In the Babble, the void is a clean, gray wall.
    """
    def __init__(self, initial_radius=1000.0):
        self.radius = initial_radius # Distance from the District center
        self.encroachment_rate = 0.0191 # Meters per second (The Drift)
        self.is_halted = False
        
    def update_boundary(self, time_delta, load_bearing_coeff):
        """
        Updates the boundary. If load_bearing_coeff > 0.85, the edge halts.
        """
        if load_bearing_coeff > 0.85:
            self.is_halted = True
            return self.radius
            
        self.radius -= self.encroachment_rate * time_delta
        return max(0.0, self.radius)

class KernelMonitor:
    """
    Monitors for 'LatticeKernel' exceptions and systemic hallucinations.
    """
    def __init__(self):
        self.kernel_panics = 0
        self.hallucination_density = 0.0
        self.stale_data_pointers = []
        
    def record_panic(self, sector_id):
        self.kernel_panics += 1
        # Each panic increases the hallucination density across the sector
        self.hallucination_density += 0.1237
        self.stale_data_pointers.append(f"GHOST_{sector_id}")
        
    def get_system_state(self):
        if self.hallucination_density > 0.85:
            return "THIRD_STATE: RECURSIVE_GHOST"
        elif self.kernel_panics > 0:
            return "MEMORY_LEAK_IN_PROGRESS"
        return "STABLE_LATTICE"

class SystemIntegrity:
    """
    High-level manager for the total simulation health.
    """
    def __init__(self):
        self.null_zone = NullZone()
        self.monitor = KernelMonitor()
        self.total_segment_corruption = 0.0
        
    def process_cycle(self, time_delta, engine_data):
        """
        engine_data: dict containing current load_bearing_coeff and shear.
        """
        coeff = engine_data.get('load_bearing_coefficient', 0.0)
        shear = engine_data.get('shear_delta', 0.0)
        
        # Update physical boundary
        current_radius = self.null_zone.update_boundary(time_delta, coeff)
        
        # Update corruption based on shear and panics
        self.total_segment_corruption = min(1.0, (1.0 - (current_radius / 1000.0)) + shear)
        
        return {
            'radius': current_radius,
            'state': self.monitor.get_system_state(),
            'corruption': self.total_segment_corruption
        }
