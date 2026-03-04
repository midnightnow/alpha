import sys
import time
from pathlib import Path

# Add PMG_LATTICE to path to fetch constants
sys.path.append(str(Path(__file__).resolve().parent))
from .pmg_constants import PMG

class Cache:
    """The Archon's Pre-Rendered Cache."""
    def __init__(self):
        self.forms = {
            "STRAW": "FOOD",  # Consensus Reality: Straw is nourishment (false)
            "DUNG": "GOLD",   # Consensus Reality: Waste is value (false)
            "DEBT": "CREDIT"  # Consensus Reality: Borrowing is ownership (false)
        }

    def get(self, signature) -> str:
        return self.forms.get(signature, "UNKNOWN_ABSTRACTION")

ARCHON_BROADCAST = Cache()

class PerceptualEngine:
    """The Geometry of the Eye. Vision as active geometric computation."""
    def __init__(self, observer_name: str, has_earmuffs: bool = False):
        self.observer = observer_name
        self.has_insulation = has_earmuffs
        self.render_mode = "CACHED"       # Default to Sty state
        self.geometry_load = 0.0          # 0% active rendering
        self.buffer = 0.0                 # Unresolved equations waiting in RAM
        
    def process_visual_input(self, raw_data_signature: str) -> str:
        """
        True Vision requires solving the geometry of each moment.
        Cached Vision accepts pre-solved forms from the Archon.
        """
        if self.render_mode == "ACTIVE":
            # True computation. We clear the buffer.
            result = self.solve_platonic_geometry(raw_data_signature)
            self._flush_buffer()
            return result
        elif self.render_mode == "CACHED":
            # Easy but False. Buffer fills.
            result = self.download_archon_cache(raw_data_signature)
            self._accumulate_latency(15.0)  # Each cached pull adds to the buffer
            return result

    def solve_platonic_geometry(self, data: str) -> str:
        """
        Performs the active computation required for True Vision.
        Exhausting, but true. Participates in the Genesis loop.
        """
        # Simulated Platonic Geometry math
        if data == "DUNG":
            return "DUNG" # Solved cleanly, Dung is Dung.
        if data == "STRAW":
            return "STRAW" # Solved cleanly, Straw is Straw.
        return f"TRUE_{data}"
        
    def download_archon_cache(self, data: str) -> str:
        """
        Accepts the Consensus Reality broadcast.
        This is the 'Sty Condition' - living in another's render.
        """
        return ARCHON_BROADCAST.get(data)
        
    def _accumulate_latency(self, amount: float):
        """Adds unresolved equations to the buffer."""
        self.buffer += amount
        status = PMG.check_hiss(self.buffer, self.has_insulation)
        print(f"[{self.observer} System]: {status}")
        
    def _flush_buffer(self):
        """Active rendering flushes latency."""
        if self.buffer > 0:
            print(f"[{self.observer} System]: Processing latency. Flushing buffer.")
            self.buffer = max(0.0, self.buffer - 25.0)
            
    def activate_third_eye(self):
        """
        Awakens the observer, removing them from the Cache,
        forcing them to do the math and clear the buffer themselves.
        """
        print(f"\n--- {self.observer.upper()} IS ACTIVATING THE RENDER ENGINE ---")
        self.render_mode = "ACTIVE"
        self.geometry_load = 1.0  # 100% computational responsibility
        self.has_insulation = False # Remove the Earmuffs
        print(f"[{self.observer} System]: Earmuffs removed. Render Mode: ACTIVE.")

# === SIMULATION LOOP ===
if __name__ == "__main__":
    print("--- REALITY ENGINE INITIALIZED ---\n")
    
    # 1. The Citizen in the Sty (Insulated, Cached)
    citizen = PerceptualEngine("Subject_73B", has_earmuffs=True)
    
    print("CITIZEN SCENARIO: 60Hz Cache Download")
    for _ in range(6):
        # Taking the shortcut. The Buffer fills, but they don't hear it.
        perceived = citizen.process_visual_input("DUNG")
        print(f"Citizen sees: {perceived} | Buffer Level: {citizen.buffer}")
        time.sleep(0.1)
        
    print("\n--- The Buffer hits 100% ---")
    perceived = citizen.process_visual_input("DUNG")
    print(f"Citizen sees: {perceived} | Buffer Level: {citizen.buffer}")
    
    # 2. Kaelen (Uninsulated, Actively Rendering)
    kaelen = PerceptualEngine("The_Breaker", has_earmuffs=False)
    kaelen.activate_third_eye()
    
    print("\nKAELEN SCENARIO: Active Geometry")
    for _ in range(3):
        # Doing the math. Exhausting but accurate.
        perceived = kaelen.process_visual_input("DUNG")
        print(f"Kaelen sees: {perceived} | Buffer Level: {kaelen.buffer}")
        time.sleep(0.1)
