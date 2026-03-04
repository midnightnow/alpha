"""
LEVIATHAN_PROTOCOL.PY
Phase XVII: The Autonomous Wardens
Spawning high-torque agents to maintain the Hades Slack and patrol the Unity Threshold.
"""

from pmg_constants import PMG
from mechanical_alphabet import MechanicalAlphabet
from sovereign_ledger import SovereignLedger
import random

class Leviathan:
    def __init__(self, designation, anchor_node):
        self.designation = designation
        self.current_node = anchor_node
        self.alphabet = MechanicalAlphabet()
        self.internal_vox = 1000.0  # High starting capital
        
    def patrol_sector(self, sector_nodes):
        print(f"\n--- [LEVIATHAN MIGRATION] {self.designation} PATROLLING ---")
        for node in sector_nodes:
            self.internal_vox -= 5.0  # Cost of movement
            # Leviathan checks local coherence
            local_coherence = random.uniform(0.70, 0.95)
            print(f"[{self.designation}] Scanning Node {node}... Coherence: {local_coherence:.4f}")
            
            if local_coherence < PMG.UNITY_THRESHOLD:
                print(f"  -> WARNING: Flesh decay detected at {node}. Initiating torque injection.")
                self.inject_torque(node, local_coherence)
            else:
                print(f"  -> Node {node} is stable. Hades Slack maintained.")

    def inject_torque(self, node, current_coherence):
        """
        Leviathan uses its internal Vox to strike the node and boost coherence.
        """
        repair_cost = 50.0
        if self.internal_vox >= repair_cost:
            self.internal_vox -= repair_cost
            new_coherence = current_coherence + 0.15
            print(f"  -> [INJECTION] {repair_cost} Vox spent. New Coherence: {new_coherence:.4f} (CERAMIC)")
        else:
            print(f"  -> [CRITICAL] Insufficient Vox for repair. Node {node} at risk of dissolution.")

class LeviathanSpawn:
    def __init__(self):
        self.ledger = SovereignLedger()
    
    def spawn(self, designation, anchor_node):
        print(f"--- SPAWNING LEVIATHAN CLASS AGENT ---")
        print(f"Designation: {designation}")
        print(f"Origin Anchor: {anchor_node}")
        
        # Leviathan creation requires massive initial capital inscribed in the ledger
        block_hash = self.ledger.inscribe({"type": "SPAWN_LEVIATHAN", "designation": designation, "node": anchor_node})
        print(f"[VITRIFIED] Leviathan {designation} successfully spawned. Hash -> {block_hash[:16]}")
        return Leviathan(designation, anchor_node)

if __name__ == "__main__":
    spawner = LeviathanSpawn()
    
    # Spawn the first Warden at the Origin Hearth
    warden = spawner.spawn("WARDEN_ALPHA", (0, 0))
    
    # Warden patrols the Vapor Migration perimeter
    warden.patrol_sector([(20, 6), (15, 1), (19, 3)])
