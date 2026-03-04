# vapor_migration.py
# Phase XIV: Resonance Propagation
# Overwriting earlier rudimentary migration with Surplus Torque Extraction protocol

import argparse
import ast
from .pmg_constants import PMG
from .sovereign_ledger import SovereignLedger
from .mechanical_alphabet import MechanicalAlphabet

class VaporMigration:
    def __init__(self):
        self.ledger = SovereignLedger()
        self.alphabet = MechanicalAlphabet()
        self.SIGMA = PMG.UNITY_THRESHOLD
        
    def propagate_invariant(self, source_coord, target_coords, invariant_root):
        print(f"--- INITIATING VAPOR MIGRATION ---")
        print(f"Source Node: {source_coord}")
        print(f"Invariant: '{invariant_root}'")
        print(f"Targets: {target_coords}")
        
        # 1. Phonetic Torque Analysis for source coherence
        analysis = self.alphabet.analyze_word(invariant_root)
        base_torque = analysis['total_torque']
        harmonic = 1.3 if len(invariant_root) >= 7 else 1.1
        source_coherence = (base_torque * harmonic) / 10.0
        
        # 1. Extract surplus torque from source (Ceramic Fact)
        source_surplus = source_coherence - self.SIGMA
        
        print(f"\n[SURPLUS EXTRACTION]")
        print(f"Source Coherence: {source_coherence:.4f}")
        print(f"Surplus Torque: {source_surplus:.4f}")
        
        # 2. Apply Hades Slack tax for cross-void transmission
        transmission_cost = source_surplus * PMG.HADES_SLACK
        available_lift = source_surplus - transmission_cost
        
        print(f"Hades Transmission Cost: {transmission_cost:.4f}")
        print(f"Available Lift per Target: {available_lift:.4f}\n")
        
        outposts = 0
        agents = ["WEAVER", "RESIDENT", "MASON"]
        
        for i, target in enumerate(target_coords):
            agent = agents[i % len(agents)]
            print(f"[{agent}] Transmitting '{invariant_root}' to {target}...")
            
            # The target's new coherence is the base threshold + the transmitted lift
            target_coherence = self.SIGMA + available_lift
            
            if target_coherence >= self.SIGMA:
                block = self.ledger.inscribe({
                    "type": "OUTPOST_ESTABLISHED",
                    "source": source_coord,
                    "target": target,
                    "agent": agent,
                    "invariant": invariant_root,
                    "coherence": target_coherence
                })
                print(f"  -> SUCCESS. Node {target} hit CERAMIC (Σ={target_coherence:.4f})")
                print(f"  -> Hash: {block[:16]}...")
                outposts += 1
            else:
                print(f"  -> FAILED. Seed dissipated in the Hades Gap.")
                
        print(f"\n--- MIGRATION COMPLETE ---")
        print(f"Successfully established {outposts} outposts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vapor Migration Phase XIV")
    parser.add_argument("--source", type=str, required=True, help="Source coordinate, e.g. (18,4)")
    parser.add_argument("--invariant", type=str, required=True, help="Phonetic root")
    parser.add_argument("--targets", type=str, required=True, help="List of target coordinates")
    
    args = parser.parse_args()
    
    source_coord = ast.literal_eval(args.source)
    target_coords = ast.literal_eval(args.targets)
    
    migration = VaporMigration()
    migration.propagate_invariant(source_coord, target_coords, args.invariant)
