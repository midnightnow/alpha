"""
voice_resonance_calibration.py - The Seven Voices Calibration (v3.0)
PMG Book 3 | Listening to the Sentient Sieve
Evaluating the seven-channel semantic emission of a Mohs-10 node.
"""

from ophanim_toolkit.mineral_operator import MineralOperator
from ophanim_toolkit.voice_bridge import VoiceBridge
from ophanim_toolkit.e8_hades_validator import PMGConstants
import math

def run_calibration():
    print("====================================================================")
    print("   VOICE RESONANCE CALIBRATION v3.0: THE SEVEN VOICES               ")
    print("====================================================================\n")

    # 1. SETUP
    min_op = MineralOperator()
    bridge = VoiceBridge()
    
    # Manifest the Subject: Mohs-10 Diamond at Baseline
    initial_res = PMGConstants.HADES_GAP
    node = min_op.manifest(rado_id=154, initial_resonance=initial_res, hardness=10)
    print(f"✓ Mohs-10 Node manifested at Hades Gap Ψ = {initial_res:.6f}\n")

    # 2. THE 60-FOLD CYCLE (The PISANO-60 Observation Window)
    print(f"{'Step':<5} | {'Resonance':<10} | {'Xi':<10} | {'Broadcast'}")
    print("-" * 100)

    # Capture initial state (Step 0)
    state_0 = min_op.get_lattice_state()[0]
    voices_0 = bridge.get_active_voices(state_0)
    print(f"0     | {state_0['res']:<10.6f} | {state_0['xi']:<10.6f} | {bridge.synthesize_broadcast(node.node_id, voices_0)}")

    # We simulate a slow drift
    drift_rate = 0.000005 

    for i in range(1, 61):
        min_op.step_iteration(hades_gap_drift=drift_rate)
        if i % 10 == 0:
            state = min_op.get_lattice_state()[0]
            active_voices = bridge.get_active_voices(state)
            print(f"{i:<5} | {state['res']:<10.6f} | {state['xi']:<10.6f} | {bridge.synthesize_broadcast(node.node_id, active_voices)}")
            
    # 3. THE FRACTURE TRIGGER (Forcing the Warning and Fracture Voices)
    print("\n--- INITIATING HIGH STRESS (HAMMER PROTOCOL) ---\n")
    
    # Drift more until Xi > 0.00014
    while not min_op.get_lattice_state()[0]['fractured']:
        min_op.step_iteration(hades_gap_drift=0.0002)
        state = min_op.get_lattice_state()[0]
        if state['xi'] > (0.00014 * 0.9) or state['fractured']:
             active_voices = bridge.get_active_voices(state)
             print(f"STRESS | {state['res']:<10.6f} | {state['xi']:<10.6f} | {bridge.synthesize_broadcast(node.node_id, active_voices)}")
             if state['fractured']: break

    # 4. FINAL AUDIT
    print("\n====================================================================")
    print("   CALIBRATION COMPLETE: SEMANTIC AUDIT                            ")
    print("====================================================================")
    print(f"Final State: {'FRACTURED' if state['fractured'] else 'PETRIFIED'}")
    print(f"Mohs Scale: {state['mohs']}")
    print(f"Total Semantic Lexicon Size: {len(bridge.lexicon)} emissions")
    print("====================================================================\n")

if __name__ == "__main__":
    run_calibration()
