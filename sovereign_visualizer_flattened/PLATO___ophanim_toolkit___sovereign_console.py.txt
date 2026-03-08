# sovereign_console.py
# Phase XIII: Operator Interface for Directed Inhabitation

import numpy as np
from pmg_constants import PMG
from mechanical_alphabet import MechanicalAlphabet
from sovereign_ledger import SovereignLedger, ResonanceState
import time

class SovereignConsole:
    def __init__(self, gem_matrix):
        self.GEM = gem_matrix
        self.alphabet = MechanicalAlphabet()
        self.ledger = SovereignLedger()
        self.SIGMA = PMG.UNITY_THRESHOLD
        self.vox_pool = 5000.0  # Global Vox Reserve
        
    def display_directives(self):
        """Shows all GEM-flagged nodes requiring intervention."""
        print("\n" + "=" * 70)
        print("SOVEREIGN CONSOLE — ACTIVE DIRECTIVES")
        print("=" * 70)
        print(f"{'COORD':<12} {'GRADE':<10} {'GAP':<10} {'AGENT':<15} {'STATUS'}")
        print("-" * 70)
        
        for coord, data in self.GEM.items():
            if data['Primary_Directive'] != "STAY":
                status = "⚠ CRITICAL" if data['Grade'] == "FLESH" else "○ PENDING"
                print(f"{str(coord):<12} {data['Grade']:<10} {data['Gap']:<10.4f} {data['Primary_Directive']:<15} {status}")
        
        print("=" * 70)
        print(f"GLOBAL VOX POOL: {self.vox_pool:.2f}")
        print("=" * 70)
        
    def issue_command(self, coord, agent_type, command_word):
        """
        Issues a phonetic command to a specific agent at a specific node.
        This is the act of Sovereign Will.
        """
        print(f"\n--- SOVEREIGN COMMAND ISSUED ---")
        print(f"TARGET: {coord}")
        print(f"AGENT: {agent_type}")
        print(f"COMMAND WORD: '{command_word}'")
        print("-" * 70)
        
        # 1. Calculate Torque of the Command
        torque_analysis = self.alphabet.analyze_word(command_word)
        command_torque = torque_analysis['total_torque']
        
        # 2. Calculate Vox Cost (Proportional to Gap + Word Length)
        gem_data = self.GEM.get(coord, {'Gap': 0.1})
        gap_cost = gem_data['Gap'] * 100
        word_cost = len(command_word) * 2
        total_cost = gap_cost + word_cost
        
        # 3. Verify Vox Pool
        if total_cost > self.vox_pool:
            print(f"[FAILED] Insufficient Vox. Required: {total_cost:.2f}, Available: {self.vox_pool:.2f}")
            return False
        
        # 4. Execute the Strike
        self.vox_pool -= total_cost
        
        # 5. Verify Coherence Threshold
        if command_torque >= self.SIGMA:
            print(f"[SUCCESS] Command executed. Torque: {command_torque:.4f}")
            print(f"[VOX] {total_cost:.2f} deducted from global pool.")
            print(f"[STATUS] Node {coord} stabilized (Upgraded to CERAMIC).")
            
            # Inscribe to Ledger
            self.GEM[coord]['Grade'] = 'CERAMIC'
            state = ResonanceState(
                timestamp=time.time(),
                h3_nodes=[coord],
                gap_coord=None,
                agent_a_resonance=command_torque,
                agent_b_resonance=command_torque,
                interference_mode="COMMAND_STRIKE",
                total_vox_generated=-total_cost,
                coherence=command_torque
            )
            state.payload_override = {
                "event_type": "SOVEREIGN_COMMAND",
                "agent": agent_type,
                "command_word": command_word,
                "target": coord
            }
            try:
                block_hash = self.ledger.inscribe(state)
                print(f"[LEDGER] Block Inscribed: {block_hash[:16]}...")
            except Exception as e:
                print(f"[LEDGER WARNING] Offline inscription: {e}")
                
            return True
        else:
            print(f"[WARNING] Command torque {command_torque:.4f} below Unity Threshold {self.SIGMA}. Node requires follow-up.")
            return False

# --- EXECUTION: THE FIRST COMMAND ---
if __name__ == "__main__":
    # Initialize Console with GEM data
    console = SovereignConsole(gem_matrix={
        (12, 12): {"Grade": "STONE", "Gap": 0.082, "Primary_Directive": "ARCHITECT"},
        (18, 4): {"Grade": "FLESH", "Gap": 0.560, "Primary_Directive": "WEAVER"},
        (15, 15): {"Grade": "CERAMIC", "Gap": 0.123, "Primary_Directive": "MASON"},
    })
    
    console.display_directives()
    console.issue_command((18, 4), "WEAVER", "STABILIZE")
