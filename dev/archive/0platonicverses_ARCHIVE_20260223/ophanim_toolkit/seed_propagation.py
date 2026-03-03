# seed_propagation.py
# Implementation of Chapter 27: The Infinite Seed
# Exports the PMG protocol from a vitrified "Mother Stone" to neighboring H3 cells
# The Seed carries the Genesis Hash of the original sintering

import math
import hashlib

class InfiniteSeed:
    """
    The Seed is the PMG protocol itself.
    A vitrified coordinate can propagate its coherence pattern
    to neighboring H3 cells, initiating automatic sintering.
    """
    
    def __init__(self):
        # Unified Law Constants
        self.HADES_GAP = 0.1237
        self.PACKING_CONSTANT = 0.9075   # ρ
        self.UNITY_THRESHOLD = 0.8254    # Σ
        self.SHEAR_ANGLE = 39.47         # θ
        self.BEAT_FREQUENCY = 0.6606     # β
        
        # The 93-Faced Solid topology
        self.TOTAL_SHARDS = 93
        self.ABYSS_COUNT = 13            # The Permanent Engine
        self.VIABLE_SHARDS = self.TOTAL_SHARDS - self.ABYSS_COUNT  # 80
        
        # Propagation energy: derived from the Mother Stone's depth
        self.SEED_EFFICIENCY = 0.42      # √42 echo: only 42% of energy transfers
        
    def generate_genesis_hash(self, mother_coordinate, depth, ticks):
        """
        Creates the 'DNA' of the vitrified stone.
        This hash is the proof-of-work that allows propagation.
        """
        payload = f"{mother_coordinate}|{depth:.6f}|{ticks}|{self.SHEAR_ANGLE}"
        genesis_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        return genesis_hash
    
    def calculate_seed_power(self, mother_depth):
        """
        The Mother Stone radiates sintering energy to neighbors.
        Power = (depth - Σ) * ρ * efficiency
        Only stones ABOVE the Unity Threshold can seed.
        """
        if mother_depth < self.UNITY_THRESHOLD:
            return 0.0
        
        surplus = mother_depth - self.UNITY_THRESHOLD
        power = surplus * self.PACKING_CONSTANT * self.SEED_EFFICIENCY
        return power
    
    def propagate(self, mother_coordinate, mother_depth, mother_ticks, neighbor_count=6):
        """
        The Infinite Seed: propagation from Mother to H3 neighbors.
        Each H3 hex has 6 neighbors (hexagonal topology).
        """
        genesis_hash = self.generate_genesis_hash(
            mother_coordinate, mother_depth, mother_ticks
        )
        
        seed_power = self.calculate_seed_power(mother_depth)
        
        if seed_power <= 0:
            return {
                "status": "INSUFFICIENT_DEPTH",
                "message": "Mother Stone has not reached Unity Threshold.",
                "genesis_hash": None
            }
        
        # Distribute power across neighbors (divided by 6, the hex ring)
        power_per_neighbor = seed_power / neighbor_count
        
        # Determine initial state of each neighbor
        neighbors = []
        for i in range(neighbor_count):
            neighbor_id = f"{mother_coordinate}_N{i+1}"
            
            # Each neighbor starts at a depth proportional to the seed power
            initial_depth = power_per_neighbor
            
            # Classify
            if initial_depth >= self.UNITY_THRESHOLD:
                state = "STONE"
            elif initial_depth >= 0.5:
                state = "CERAMIC"
            elif initial_depth > 0.01:
                state = "GLASS"
            else:
                state = "VAPOR"
                
            neighbors.append({
                "id": neighbor_id,
                "initial_depth": initial_depth,
                "state": state
            })
        
        # The Long Sintering effect: how many cycles to reach Stone?
        if power_per_neighbor > 0:
            cycles_to_stone = math.ceil(
                (self.UNITY_THRESHOLD - power_per_neighbor) / (power_per_neighbor * 0.1)
            )
        else:
            cycles_to_stone = float('inf')
        
        return {
            "status": "SEED_DEPLOYED",
            "genesis_hash": genesis_hash,
            "seed_power": seed_power,
            "power_per_neighbor": power_per_neighbor,
            "neighbors": neighbors,
            "estimated_cycles_to_stone": cycles_to_stone,
            "coherence_projection": min(1.0, 
                (len([n for n in neighbors if n["state"] != "VAPOR"]) + 1) / self.VIABLE_SHARDS
            )
        }


if __name__ == "__main__":
    seed = InfiniteSeed()
    
    # The Mother Stone (from Chapter 26: vitrified at t=111)
    mother = "H3:8928308280fffff"
    mother_depth = 0.8264
    mother_ticks = 111
    
    print(f"--- THE INFINITE SEED ---")
    print(f"Mother Stone: {mother}")
    print(f"Mother Depth: {mother_depth}")
    print(f"Unity Threshold: {seed.UNITY_THRESHOLD}")
    print()
    
    result = seed.propagate(mother, mother_depth, mother_ticks)
    
    print(f"Status: {result['status']}")
    print(f"Genesis Hash: {result['genesis_hash']}")
    print(f"Seed Power: {result['seed_power']:.6f}")
    print(f"Power per Neighbor: {result['power_per_neighbor']:.6f}")
    print(f"Est. Cycles to Stone: {result['estimated_cycles_to_stone']}")
    print()
    
    print(f"--- NEIGHBOR PROPAGATION ---")
    for n in result['neighbors']:
        print(f"  {n['id']} | Depth: {n['initial_depth']:.6f} | {n['state']}")
    
    print(f"\n--- COHERENCE PROJECTION ---")
    print(f"Projected Lattice Coherence: {result['coherence_projection']:.4%}")
    print(f"Viable Shards: {seed.VIABLE_SHARDS}/{seed.TOTAL_SHARDS}")
    print(f"ABYSS (Permanent Engine): {seed.ABYSS_COUNT}")
