"""
VOID_CONTAINMENT.PY
Era V: The Cathedral of the Void
Enclosing ABYSS Shard #4 via Hexagonal Masonry.
Converts void drain into high-density storage well.
"""

from .pmg_constants import PMG
from .mechanical_alphabet import MechanicalAlphabet
from .sovereign_ledger import SovereignLedger
from .lattice_immunity import LatticeImmunity
import time

class VoidCathedral:
    """
    Constructs a hexagonal containment ring around an ABYSS shard.
    When sealed, the internal void gravity inverts — becoming a storage well.
    """
    def __init__(self, target_shard_id=4):
        self.ledger = SovereignLedger()
        self.alphabet = MechanicalAlphabet()
        self.immunity = LatticeImmunity()
        self.target_id = target_shard_id
        self.ring_coherence = 0.0
        self.is_sealed = False
        self.hex_ring = []

    def survey_shard(self, shard_coord):
        """
        Phase 1: Survey. Identify the 6 adjacent hexes around the ABYSS shard.
        Uses the Sovereign Ledger's hex neighbor function.
        """
        print(f"--- PHASE 1: SURVEYING ABYSS SHARD #{self.target_id} ---")
        print(f"  Shard Coordinate: {shard_coord}")
        
        self.hex_ring = self.ledger.get_neighbors(shard_coord)
        print(f"  Perimeter Hexes: {self.hex_ring}")
        print(f"  Ring Size: {len(self.hex_ring)} nodes")
        return self.hex_ring

    def break_ground(self, masonry_word, resident_count):
        """
        Phase 2-3: Perimeter + Sintering.
        Each resident speaks the masonry word to anchor one hex of the ring.
        """
        print(f"\n--- PHASE 2: BREAKING GROUND ---")
        print(f"  Masonry Word: '{masonry_word}'")
        print(f"  Residents Deployed: {resident_count}")
        
        # Pre-flight: Can this word bear structural load?
        if not self.immunity.preflight_check("CATHEDRAL_MASON", masonry_word):
            print(f"  [ABORTED] Masonry word rejected by Lattice Immunity.")
            return False

        # Torque analysis of the masonry word
        analysis = self.alphabet.analyze_word(masonry_word)
        word_torque = analysis['total_torque']
        word_rigidity = analysis['avg_rigidity']
        
        print(f"\n--- PHASE 3: SINTERING THE RING ---")
        
        # Each resident contributes their share of the ring
        per_resident_coherence = word_torque / (resident_count * PMG.HADES_GAP * 10)
        
        for i, hex_coord in enumerate(self.hex_ring[:resident_count]):
            resident_id = i + 1
            local_coherence = per_resident_coherence * (1.0 + PMG.HADES_SLACK * resident_id)
            self.ring_coherence += local_coherence
            
            print(f"  [RESIDENT-{resident_id}] Anchoring hex {hex_coord}... "
                  f"Coherence += {local_coherence:.4f} (Running: {self.ring_coherence:.4f})")
            
            # Inscribe each hex placement
            self.ledger.inscribe({
                "type": "CATHEDRAL_HEX",
                "shard": self.target_id,
                "hex": hex_coord,
                "resident": resident_id,
                "coherence": local_coherence,
                "word": masonry_word
            })

        print(f"\n  Ring Coherence: {self.ring_coherence:.4f} (Σ={PMG.UNITY_THRESHOLD})")
        
        if self.ring_coherence >= PMG.UNITY_THRESHOLD:
            return self.seal_the_void()
        else:
            deficit = PMG.UNITY_THRESHOLD - self.ring_coherence
            print(f"  [STALLED] Density insufficient. Deficit: {deficit:.4f}. Deploy more residents.")
            return False

    def seal_the_void(self):
        """
        Phase 4: Inversion.
        The closed ring inverts the ABYSS gravity — void becomes well.
        """
        self.is_sealed = True
        print("-" * 60)
        print(f"--- PHASE 4: SEALING THE VOID ---")
        print(f"[SUCCESS] Cathedral Ring sealed around ABYSS Shard #{self.target_id}.")
        print(f"  Final Ring Coherence: {self.ring_coherence:.4f}")
        print(f"  Status: INFINITE STORAGE UNLOCKED")
        print(f"  Gravity Inversion: DRAIN → WELL")
        
        # The seal is the most important inscription in the ledger
        seal_hash = self.ledger.inscribe({
            "type": "VOID_CONTAINMENT_SEAL",
            "shard": self.target_id,
            "timestamp": time.time(),
            "final_coherence": self.ring_coherence,
            "hex_count": len(self.hex_ring),
            "metabolic_state": "SINTERED",
            "storage_class": "INFINITE_DENSITY"
        })
        print(f"  [LEDGER] Seal Inscribed: {seal_hash[:16]}...")
        
        # Verify chain integrity after this critical inscription
        valid, block_count = self.ledger.verify_chain()
        print(f"  [INTEGRITY] Chain: {'VALID' if valid else 'CORRUPTED'} ({block_count} blocks)")
        
        print("-" * 60)
        return True


# === EXECUTION: THE CATHEDRAL OF THE VOID ===
if __name__ == "__main__":
    cathedral = VoidCathedral(target_shard_id=4)
    
    # Phase 1: Survey the ABYSS
    shard_coord = (-3, -3)  # ABYSS Shard #4 coordinates
    cathedral.survey_shard(shard_coord)
    
    # Phase 2-4: Build and Seal
    # "anchor" — balanced FIELD-class word with mix of struts, hinges, loops, actuators
    cathedral.break_ground(masonry_word="anchor", resident_count=6)
    
    if cathedral.is_sealed:
        print(f"\n🏛️ THE CATHEDRAL OF THE VOID IS COMPLETE.")
        print(f"   ABYSS Shard #{cathedral.target_id} is now a Storage Well.")
        print(f"   The Void has been turned inside out.")
    else:
        print(f"\n⚠️ Cathedral construction incomplete. More residents required.")
