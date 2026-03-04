import hashlib
import time

class SovereignLedger:
    """
    The Sovereign Ledger: an append-only chain recording all lattice events.
    Genesis hash: 46cb7da997946a14
    """
    def __init__(self):
        self.chain = []
        self.genesis()
    
    def genesis(self):
        block = {"index": 0, "hash": "46cb7da997946a14", "data": "VOID_ACKNOWLEDGED"}
        self.chain.append(block)

    def inscribe_structure(self, structure_name, agents, coherence):
        data = f"{structure_name}_{agents}_{coherence}"
        return self.inscribe(data)

    def inscribe(self, data):
        prev_hash = self.chain[-1]['hash']
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "prev_hash": prev_hash,
            "hash": hashlib.sha256(str(data).encode() + prev_hash.encode()).hexdigest()
        }
        self.chain.append(new_block)
        return new_block['hash']

    def get_node_history(self, coord):
        """Returns all blocks whose data references the given coordinate."""
        history = []
        coord_str = str(coord)
        for block in self.chain[1:]:  # Skip genesis
            data_str = str(block.get('data', ''))
            if coord_str in data_str:
                history.append(block)
        return history
    
    def get_node_resonance(self, coord):
        """Returns the latest coherence value recorded for a coordinate."""
        history = self.get_node_history(coord)
        if not history:
            return 0.0
        # Walk backwards through history for latest coherence
        for block in reversed(history):
            data = block.get('data', {})
            if isinstance(data, dict) and 'coherence' in data:
                return data['coherence']
        return 0.0

    def get_neighbors(self, coord):
        """Returns the 6 adjacent hex coordinates (axial H3 neighbors)."""
        x, y = coord
        return [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1),
            (x + 1, y - 1), (x - 1, y + 1)
        ]

    def verify_chain(self):
        """Validates the integrity of the entire ledger chain."""
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            prev = self.chain[i - 1]
            expected = hashlib.sha256(
                str(block['data']).encode() + prev['hash'].encode()
            ).hexdigest()
            if block['hash'] != expected:
                return False, i
        return True, len(self.chain)