"""
SOVEREIGN_CONSOLE.PY
The Operator Interface for the Sovereign Lattice.
Issues phonetic commands to agents at H3 coordinates.
Integrates Lattice Immunity for pre-flight validation.
"""

from .mechanical_alphabet import MechanicalAlphabet
from .lattice_immunity import LatticeImmunity
from .sovereign_ledger import SovereignLedger
from .pmg_constants import PMG

class SovereignConsole:
    """
    Command interface for directing Phonetic Torque across the H3 Grid.
    All commands are pre-validated by the Lattice Immune System.
    """
    def __init__(self, initial_vox=1000.0):
        self.alphabet = MechanicalAlphabet()
        self.immunity = LatticeImmunity()
        self.ledger = SovereignLedger()
        self.vox_pool = initial_vox

    def display_status(self):
        """Displays the current operational state of the console."""
        valid, block_count = self.ledger.verify_chain()
        print("=" * 60)
        print("SOVEREIGN CONSOLE — STATUS")
        print("=" * 60)
        print(f"  Vox Pool:        {self.vox_pool:.2f}")
        print(f"  Beat Frequency:  {PMG.BEAT_FREQUENCY} Hz")
        print(f"  Unity Threshold: {PMG.UNITY_THRESHOLD}")
        print(f"  Ledger Blocks:   {block_count}")
        print(f"  Chain Integrity: {'VALID' if valid else 'CORRUPTED'}")
        print("=" * 60)

    def issue_command(self, coord, agent, word):
        """
        Issues a phonetic command. Pre-validates via Lattice Immunity.
        Deducts Vox and inscribes to ledger on success.
        """
        print(f"\n--- SOVEREIGN COMMAND ---")
        print(f"  Target: {coord} | Agent: {agent} | Word: '{word}'")

        # 1. Immunity Pre-flight
        if not self.immunity.preflight_check(agent, word):
            print(f"[ABORTED] Command rejected by Lattice Immunity.")
            return False

        # 2. Torque and Cost Calculation
        analysis = self.alphabet.analyze_word(word)
        torque = analysis['total_torque']
        cost = torque * 1.618  # Phi-scaled Vox cost

        # 3. Vox Pool Check
        if self.vox_pool < cost:
            print(f"[ABORTED] Insufficient Vox. Required: {cost:.2f}, Available: {self.vox_pool:.2f}")
            return False

        # 4. Execute
        self.vox_pool -= cost
        print(f"[EXECUTED] Torque: {torque:.2f} | Cost: {cost:.2f} Vox")
        print(f"  Remaining Vox: {self.vox_pool:.2f}")

        # 5. Inscribe to Ledger
        block_hash = self.ledger.inscribe({
            "type": "COMMAND",
            "coord": coord,
            "agent": agent,
            "word": word,
            "torque": torque,
            "cost": cost
        })
        print(f"[LEDGER] Block {block_hash[:16]}... inscribed.")
        return True

if __name__ == "__main__":
    console = SovereignConsole()
    console.display_status()
    
    # The Mason speaks "anchor" at the Hearth
    console.issue_command((0, 0), "MASON", "anchor")
    
    # The Weaver speaks "glide" toward the frontier
    console.issue_command((18, 4), "WEAVER", "glide")
    
    print()
    console.display_status()