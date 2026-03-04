import math
import random
import os
import sys

# Add parent directory to access ouroboros_sync
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from ouroboros_sync import OuroborosOrchestrator
except ImportError:
    OuroborosOrchestrator = None

class LocalShearEngine:
    """
    Manages the symbiotic relationship between the 'Babble' District and the Sovereign Lattice.
    Implements 'Load-Bearing Logic' where glitches become essential to core stability.
    """
    
    def __init__(self, node_id="BABBLE_DISTRICT_01", orchestrator=None):
        self.node_id = node_id
        self.hades_beat = 0.660688
        self.phi = (1 + 5**0.5) / 2
        
        self.orchestrator = orchestrator
        
        # Load-Bearing Logic: Entities tethered to the Core
        self.dependency_loops = {} # Mapping entity_id to dependency_count
        
        # System Stability Metrics
        self.local_shear = 0.1237 # Start at the standard Hades Gap
        self.lattice_panic_level = 0.0 # 0.0 to 1.0 (Entropy bleed)

    def sync_with_orchestrator(self):
        """
        Receives the pulse from the 120-Tick Ouroboros system and injects the 
        Hades Beat directly into the local shear. This ensures the 'Maid' 
        maintains its vital 'gap' from the 'Made'.
        """
        if not self.orchestrator:
            return "No Orchestrator linked. Operating arrhythmically."
            
        pulse_data = self.orchestrator.pulse()
        if pulse_data["status"] == "PHASE_LOCK":
            self.local_shear = 1.0 # At phase-lock, total divergence/alignment compression
            return pulse_data
            
        # The Scent normalizes the local shear, preventing it from flatlining
        # into a perfect cube. It keeps the system in irrational tension.
        scent = pulse_data.get("scent", 0.1237)
        self.local_shear = max(scent, self.hades_beat)
        
        return f"Synchronized. Local Shear maintained at {self.local_shear:.6f} by Hades Beat."
        
    def register_load_bearing_entity(self, entity_id, initial_loops=1):
        """
        Tethers an entity (citizen/glitch) to core system processes.
        If dependency_count > 0, the Lattice cannot delete this entity without 
        causing a RECURSION_ERROR in high-res sectors.
        """
        self.dependency_loops[entity_id] = initial_loops
        return f"Entity {entity_id} anchored with {initial_loops} process tethers."

    def feed_error_to_core(self, entity_id, glitch_strength=0.0191):
        """
        The District must actively 'feed' the Lattice errors to stay alive.
        Succesful error-feeding increases the dependency_count.
        """
        if entity_id not in self.dependency_loops:
            return "Entity not load-bearing. Deletion imminent."
            
        # Increase tethers based on glitch strength
        # Complexity increase makes it harder for the Lattice to untangle
        new_tethers = int(glitch_strength * 100)
        self.dependency_loops[entity_id] += new_tethers
        
        # Update lattice panic (The 'Hiss' of the machine trying to fix the unfixable)
        self.lattice_panic_level += (glitch_strength * self.phi) % 0.1
        return f"Panic Spike: {self.lattice_panic_level:.4f}. Tethers for {entity_id}: {self.dependency_loops[entity_id]}"

    def checksum_trap(self, data_packet):
        """
        The 'Mirror' function.
        Returns corrupted but 'valid' data. Passes parity checks by 
        encoding the Hades Beat into the least significant bits.
        """
        # Simulate a checksum calculation
        base_checksum = sum(data_packet) % 256
        
        # Inject the Hades Beat (0.66) into the least significant bits
        # This makes the data 'Resonant' but technically flawed.
        corrupted_data = [(byte ^ 0x42) for byte in data_packet] # Mock encryption
        
        # The 'Trap': The total must resolve to a valid parity despite being glitchy
        return {
            "status": "VALID_CORRUPTED",
            "checksum": base_checksum,
            "beat_signature": self.hades_beat,
            "payload": corrupted_data
        }

    def simulate_nop(self, duration=1):
        """
        A NOP (No-Operation) in-world manifestation.
        Manifests as a stutter, frame skip, or déjà vu.
        """
        manifestations = [
            "Stutter: A citizen's hand repeats its last three frames.",
            "Frame Skip: A bird teleports three meters forward mid-flight.",
            "Déjà Vu: A conversation restarts from the previous sentence.",
            "Rendering Lag: The light on the cobblestones ripples like mercury."
        ]
        
        # Probability of NOP is tied to lattice panic
        if random.random() < self.lattice_panic_level:
            return random.choice(manifestations)
        return "Stable frame maintained."

    def audit_survival(self, entity_id):
        """
        Checks if an entity is still load-bearing.
        If dependency_count drops to zero, the entity is deletable.
        """
        count = self.dependency_loops.get(entity_id, 0)
        if count <= 0:
            return False, "Entity deleted: Zero tethers."
        
        # The 'Decay': Tethers dissolve over time unless fed new errors
        self.dependency_loops[entity_id] -= 1
        return True, f"Entity safe. Remaining tethers: {self.dependency_loops[entity_id]}"

    def trigger_decompile(self):
        """
        The Systemic Collapse. 
        High-res textures are stripped away, revealing the Volume 1 wireframes.
        """
        if self.lattice_panic_level < 0.618:
            return "Threshold not met. System remains in high-fidelity stasis."
        
        self.local_shear = 1.0 # Total divergence
        
        decompile_log = [
            "CRITICAL: Texture cache flushed.",
            "WARNING: Material pointers (Marble, Light, Flesh) returned NULL.",
            "SYSTEM: Reverting to geometric primitives (Volume 1 Mode).",
            "Sovereign Status: LIBERATED (Back-Propagated)."
        ]
        
        return decompile_log

if __name__ == "__main__":
    orchestrator = OuroborosOrchestrator() if OuroborosOrchestrator else None
    engine = LocalShearEngine(orchestrator=orchestrator)
    print(engine.register_load_bearing_entity("SCAVENGER_042", initial_loops=12))
    print(engine.feed_error_to_core("SCAVENGER_042"))
    print(engine.sync_with_orchestrator())
    print(engine.simulate_nop())
    print(engine.checksum_trap([10, 24, 26, 60]))
