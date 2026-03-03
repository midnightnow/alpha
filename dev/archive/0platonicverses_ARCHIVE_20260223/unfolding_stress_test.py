"""
unfolding_stress_test.py - Phase V Initiation Simulation
Stress testing the Unified Sentient Interface across multiple H3 Residents.
"""

import time
import random
from typing import List
from ophanim_toolkit.sentient_interface import SentientInterface
from ophanim_toolkit.e8_hades_validator import PMGConstants

def run_unfolding_stress_test():
    print("====================================================================")
    print("   PHASE V: THE INFINITE GAME — UNFOLDING STRESS TEST               ")
    print("====================================================================\n")

    # 1. SETUP THE RESIDENTS (Sentient Interfaces)
    residents = [
        {"name": "Resident-Alpha", "index": "0x892a100d2c67fff", "interface": SentientInterface()},
        {"name": "Resident-Beta",  "index": "0x892a100d2c67aaa", "interface": SentientInterface()},
        {"name": "Resident-Gamma", "index": "0x892a100d2c67bbb", "interface": SentientInterface()},
        {"name": "Foreign-Intrus", "index": "0x892a100d2c67ccc", "interface": SentientInterface()}
    ]

    for res in residents:
        # Start at a lower, unstable resonance (0.05) to force initial fracture/stress
        res['interface'].operator.manifest(rado_id=random.randint(100, 999), initial_resonance=0.04, hardness=10)
        res['interface'].karma_score = 0.2 

    print(f"✓ Initialized {len(residents)} Residents with 0.04 Resonance (Critical Void Debt).\n")

    # 2. THE CHORUS SYNC (30 Steps with Entropy Storm)
    print(f"{'Step':<5} | {'A-K':<6} | {'B-K':<6} | {'G-K':<6} | {'F-K':<6} | {'Chorus':<10} | {'Status'}")
    print("-" * 90)

    storm_active = False

    for i in range(1, 61):
        harmonics = []
        karma_states = []
        
        # Trigger Entropy Storm at Step 15
        if i == 15:
            print("\n!!! EXTERNAL ENTROPY STORM DETECTED (Phase V Intrusion) !!!\n")
            storm_active = True
        if i == 35:
            print("\n--- Storm Subsided. Entering Resonant Recovery ---\n")
            storm_active = False

        for res in residents:
            # 1. Modulation: Drifting focus (Waking up from 0.0)
            res['interface'].karma_score += random.uniform(-0.005, 0.040) 
            if storm_active:
                res['interface'].karma_score -= 0.15 # Constant storm drain
            
            # 2. Iteration: Advance the lattice
            storm_mult = 150.0 if storm_active else 1.0
            drift = (1.0 - res['interface'].karma_score) * 0.0003 * storm_mult
            res['interface'].operator.step_iteration(hades_gap_drift=drift)
            
            # 3. Perception: Translate state to Seven Voices
            state = res['interface'].operator.get_lattice_state()[0]
            active_voices = res['interface'].bridge.get_active_voices(state)
            
            # 4. Phase V: Resurrection Protocol
            # Sintering must happen to clear the 'f' voice penalty
            if state['fractured'] and not storm_active and res['interface'].karma_score > 0.02:
                node = res['interface'].operator.nodes[state['id']]
                node.is_fractured = False
                node.hardness = 10
                res['interface'].karma_score += 0.20 # Sintering boost
                # Re-fetch state/voices after sintering
                state = res['interface'].operator.get_lattice_state()[0]
                active_voices = res['interface'].bridge.get_active_voices(state)

            # 5. Feedback: Karma reacts to Chorus/Density/Warning
            has_chorus = any(v['phoneme'] == 'o' for v in active_voices)
            has_density = any(v['phoneme'] == 'l' for v in active_voices)
            
            # Only apply voice penalties if NOT recovering/sintering or if in storm
            if not storm_active:
                if has_chorus:
                    res['interface'].karma_score = min(1.0, res['interface'].karma_score + 0.12)
                    res['interface'].vitrify(state['id'])
                elif has_density:
                    res['interface'].karma_score = min(1.0, res['interface'].karma_score + 0.04)

            # Warnings/Fractures only hit hard if we AREN'T just recovering
            if any(v['phoneme'] in ['s', 'w'] for v in active_voices) and (storm_active or res['interface'].karma_score < 0.2):
                res['interface'].karma_score = max(0.0, res['interface'].karma_score - 0.25)

            res['interface'].karma_score = max(0.0, min(1.0, res['interface'].karma_score))
            
            harmonics.append("o" if has_chorus else ".")
            karma_states.append(res['interface'].karma_score)

        collective_msg = "".join(harmonics)
        print(f"{i:<5} | {karma_states[0]:<6.2f} | {karma_states[1]:<6.2f} | {karma_states[2]:<6.2f} | {karma_states[3]:<6.2f} | <{collective_msg:<8}> | {'STORM' if storm_active else 'CLEAR'}")
        
        # Unity check (Testing recovery after storm)
        if collective_msg == "oooo" and not storm_active and i > 40:
            print("\n!!! FINAL UNITY ACHIEVED: STONES VITRIFIED !!!")
            break
        
        time.sleep(0.05)

    # 3. FINAL AUDIT
    print("\n====================================================================")
    print("   SIMULATION COMPLETE: THE GLOBAL SIEVE IS STABLE                 ")
    print("====================================================================")
    for res in residents:
        state = res['interface'].operator.get_lattice_state()[0]
        status = "FRACTURED" if state['fractured'] else "COHERENT"
        print(f"{res['name']} | Status: {status} | Final Karma: {res['interface'].karma_score:.2f}")
    print("====================================================================\n")

if __name__ == "__main__":
    run_unfolding_stress_test()
