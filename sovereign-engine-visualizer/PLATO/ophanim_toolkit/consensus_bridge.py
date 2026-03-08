"""
consensus_bridge.py - Multi-Agent Handshake & Negotiation (v1.0)
PMG Book 4: The Architect's Exile | Phase V
Negotiating shared reality between multiple Sovereigns.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class SovereignState:
    id: str
    sigma: float
    origin: Tuple[float, float, float]
    intent_vector: Tuple[float, float, float]

class ConsensusBridge:
    """
    Manages the 'Reciprocal Paddock'. 
    Handles how two sovereigns agree on the state of a shard in the Slurry.
    """
    def __init__(self):
        self.players: Dict[str, SovereignState] = {}
        self.shared_shards: Dict[int, str] = {} # shard_id -> consensus_name

    def register_player(self, player: SovereignState):
        self.players[player.id] = player
        print(f"CONSENSUS: {player.id} has entered the Paddock (Σ={player.sigma:.2f}).")

    def negotiate_naming(self, shard_id: int, p1_id: str, p1_name: str, p2_id: str, p2_name: str) -> str:
        """
        Two sovereigns propose names for the same shard.
        The name is weighted by their Sovereignty (Sigma).
        """
        s1 = self.players.get(p1_id)
        s2 = self.players.get(p2_id)
        
        if not s1 or not s2:
            return "Consensus Failed: Unknown Player"
            
        total_sigma = s1.sigma + s2.sigma
        w1 = s1.sigma / total_sigma
        w2 = s2.sigma / total_sigma
        
        # A simple phonetic blend or win-loss based on weight
        # For PMG, we use the "Morphism of Consensus": a hybrid name.
        # e.g., "Stone" + "Bone" = "Stone-Bone" or "Stone" (if s1 >> s2)
        
        if w1 > 0.66:
            consensus = p1_name
        elif w2 > 0.66:
            consensus = p2_name
        else:
            consensus = f"{p1_name}-{p2_name}"
            
        self.shared_shards[shard_id] = consensus
        print(f"CONSENSUS: Shard {shard_id} is now named '{consensus}' by mutual audit.")
        return consensus

    def get_paddock_status(self):
        print(f"--- Reciprocal Paddock Status ---")
        print(f"  Players in Field: {len(self.players)}")
        print(f"  Consensus Objects: {len(self.shared_shards)}")
        for shard_id, name in self.shared_shards.items():
            print(f"    [Shard {shard_id}] -> {name}")

if __name__ == "__main__":
    bridge = ConsensusBridge()
    
    # Player 1: The Standing Man (High Sigma)
    p1 = SovereignState(id="StandingMan_01", sigma=80.84, origin=(42, 51, 60), intent_vector=(1, 0, 0))
    
    # Player 2: The Stranger (Emergent Sigma)
    p2 = SovereignState(id="Stranger_007", sigma=12.37, origin=(100, 100, 100), intent_vector=(0, 1, 0))
    
    bridge.register_player(p1)
    bridge.register_player(p2)
    
    # Negotiate naming of a shard
    bridge.negotiate_naming(93, "StandingMan_01", "The Altar", "Stranger_007", "The Bench")
    bridge.get_paddock_status()
