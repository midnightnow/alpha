# great_migration.py
# Phase XIV: The Great Migration
# Autonomous expansion into unmapped H3 clusters

import time
import numpy as np
from pmg_constants import PMG
from mechanical_alphabet import MechanicalAlphabet
from sovereign_ledger import SovereignLedger, ResonanceState

class GreatMigration:
    def __init__(self, vox_pool=4815.0):
        self.ledger = SovereignLedger()
        self.alphabet = MechanicalAlphabet()
        self.SIGMA = PMG.UNITY_THRESHOLD
        self.HADES_SLACK = PMG.HADES_SLACK
        self.vox_pool = vox_pool
        self.frontier_nodes = set()

    def discover_frontier(self, current_cluster_radius: int, expansion_depth: int):
        """Scans the void beyond the known H3 grid to identify new anchor points."""
        print("\n" + "=" * 70)
        print("PHASE XIV: THE GREAT MIGRATION — FRONTIER SCAN")
        print("=" * 70)
        
        # Calculate new nodes in the expanded radius
        new_radius = current_cluster_radius + expansion_depth
        for r in range(current_cluster_radius + 1, new_radius + 1):
            # Generating a ring of potential nodes
            num_nodes = r * 6
            for i in range(num_nodes):
                # Simulated mapping to a 2D coordinate for the unmapped void
                angle = (i / num_nodes) * 2 * np.pi
                x = int(np.round(r * np.cos(angle)))
                y = int(np.round(r * np.sin(angle)))
                self.frontier_nodes.add((x, y))
                
        print(f"Discovered {len(self.frontier_nodes)} unmapped nodes in the Abyss.")
        return list(self.frontier_nodes)

    def launch_expedition(self, agents, target_nodes):
        """Sends the Triad to colonize unmapped nodes."""
        print("\n--- LAUNCHING COLONIZATION EXPEDITION ---")
        successful_claims = 0
        
        for coord in target_nodes[:5]:  # Attempt first 5 nodes to conserve Vox
            print(f"\n[EXPEDITION] Targeting Unmapped Node: {coord}")
            
            combined_torque = 0.0
            total_cost = 0.0
            
            for agent in agents:
                # The word to claim new territory
                if agent.role == "MASON":
                    word = "claim"
                elif agent.role == "WEAVER":
                    word = "reach"
                elif agent.role == "ARCHITECT":
                    word = "expand"
                else:
                    word = "move"
                    
                analysis = self.alphabet.analyze_word(word)
                combined_torque += analysis['total_torque']
                
                # Vox cost is higher in unmapped territory (Distance * Slack Multiplier)
                distance = np.sqrt(coord[0]**2 + coord[1]**2)
                cost = (distance * 10) * (1.0 + self.HADES_SLACK)
                total_cost += cost
                
            coherence = combined_torque / (len(agents) * 1.5) # Unmapped resistance
            
            if self.vox_pool < total_cost:
                print(f"[FAILED] Insufficient Vox for expedition. Required: {total_cost:.2f}, Pool: {self.vox_pool:.2f}")
                break
                
            self.vox_pool -= total_cost
            
            if coherence >= self.SIGMA:
                print(f"[SUCCESS] Node {coord} claimed. Coherence: {coherence:.4f}, Cost: {total_cost:.2f} Vox")
                successful_claims += 1
                
                # Ledger Inscription
                state = ResonanceState(
                    timestamp=time.time(),
                    h3_nodes=[coord],
                    gap_coord=None,
                    agent_a_resonance=coherence,
                    agent_b_resonance=coherence,
                    interference_mode="FRONTIER_CLAIM",
                    total_vox_generated=-total_cost,
                    coherence=coherence
                )
                state.payload_override = {
                    "event_type": "GREAT_MIGRATION",
                    "agents": [a.role for a in agents],
                    "target": coord
                }
                try:
                    block_hash = self.ledger.inscribe(state)
                    print(f"[LEDGER] Migration Inscribed: {block_hash[:16]}...")
                except:
                    pass
            else:
                print(f"[ALERT] Coherence {coherence:.4f} below threshold at {coord}. Void rejected claim.")
                
        print("\n" + "=" * 70)
        print(f"EXPEDITION COMPLETE. {successful_claims} new nodes added to the Sovereign Lattice.")
        print(f"Remaining Vox Pool: {self.vox_pool:.2f}")
        print("=" * 70)
        return successful_claims

# --- EXECUTION: THE GREAT MIGRATION ---
if __name__ == "__main__":
    from immune_move import IntegratedAgent
    
    # Initialize the swarm for the frontier
    mason = IntegratedAgent("MASON", base_vox=100.0, rigidity=0.82)
    weaver = IntegratedAgent("WEAVER", base_vox=100.0, rigidity=0.45)
    architect = IntegratedAgent("ARCHITECT", base_vox=100.0, rigidity=0.65)
    
    migration = GreatMigration(vox_pool=4815.0)
    
    # Map the next 2 rings of the H3 cluster
    frontier = migration.discover_frontier(current_cluster_radius=3, expansion_depth=2)
    
    # Launch expedition to claim the void
    migration.launch_expedition([mason, weaver, architect], frontier)
