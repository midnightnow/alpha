"""
simulate_breach.py - Global Stress Test: √42 ↔ √51 Transition
Simulating the Physical Shattering of the Interference Solid.
Part of Phase II: The Sibling Resonance.
"""

import math
import sys
import os

# Add toolkit to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ophanim_toolkit'))

from bridge_operator import BridgeOperator
from mineral_operator import MineralOperator
from aion_interface import AionInterface, CONST_RHO, CONST_DELTA

def run_breach_simulation():
    print("====================================================================")
    print("   GLOBAL STRESS TEST: THE √42 ↔ √51 BREACH SIMULATION             ")
    print("====================================================================\n")

    # 1. INITIALIZATION
    bridge = BridgeOperator()
    min_op = MineralOperator()
    aion = AionInterface("Breach-Monitor")
    aion.calibrate_system()
    
    # Manifest 3 nodes representing the Triadic Chord of the Solid
    # Frequencies: √42, √51, √60 (Projected to audible range by generator)
    # Here we manifest them at their base resonance
    chord_nodes = [
        min_op.manifest(rado_id=42, initial_resonance=math.sqrt(42)/100, hardness=10), # Root
        min_op.manifest(rado_id=51, initial_resonance=math.sqrt(51)/100, hardness=10), # Third (17-gon)
        min_op.manifest(rado_id=60, initial_resonance=math.sqrt(60)/100, hardness=10)  # Fifth
    ]
    
    print(f"✓ Triadic Solid Manifested (3 Nodes, Mohs-10)")
    print(f"✓ Bridge Ratio: {bridge.calculate_bridge_ratio():.4f}")
    print(f"✓ Resonant Whisper: {bridge.get_resonant_whisper():.4f} Hz\n")

    # 2. TRANSITION LOOP (One Pisano-60 Period)
    print(f"{'Tick':<5} | {'Density':<8} | {'Morph %':<8} | {'Alignment':<10} | {'Status':<15}")
    print("-" * 65)

    for tick in range(1, 61):
        # Gradual density increase to induce the breach
        # Starting at 0.900, ramping past RHO (0.907485)
        grid_density = 0.900 + (tick * 0.00025)
        
        # Calculate Tension and Drift
        aion.apply_overpack_tension(grid_density)
        tension = aion.visual_tension
        
        # Drift increases as we approach the shear angle limit
        drift = tension * 0.0001
        
        # Step the Mineral Operator
        min_op.step_iteration(hades_gap_drift=drift)
        
        # Evaluate Alignment via Bridge
        # We simulate the frequencies shifting as the solid deforms
        f42 = 66.0 # Reference
        f51 = 66.0 * (1.1019 + (tension * 0.001)) # Drifted relative to ideal ratio
        alignment = bridge.evaluate_sibling_alignment(f42, f51)
        
        # Morph Percentage: How much of √51 is "shining through"
        # At Tension > 0, the Morph Shape Key starts to activate
        morph_pct = min(1.0, tension * 0.5) if tension > 0 else 0.0
        
        status = alignment["status"]
        if any(n.is_fractured for n in chord_nodes):
            status = "FRACTURE_EVENT"
            
        # Display Every 5th Tick or Status Change
        if tick % 5 == 0 or status != "STABLE_BRIDGE":
            print(f"{tick:<5} | {grid_density:<8.4f} | {morph_pct:<8.1%} | {alignment['alignment_score']:<10.3f} | {status}")
            
        if status == "THE_BREACH":
            print("\n!!! CRITICAL BREACH DETECTED !!!")
            print("The 9-Gap Bridge has collapsed.")
            print(f"Visual Tension: {tension:.4f}")
            print(f"Morph State: √51 Dominant ({morph_pct:.1%})")
            break

    print("\n====================================================================")
    print("   STRESS TEST COMPLETE: SYSTEM STABILITY AUDIT                    ")
    print("====================================================================")
    for i, node in enumerate(chord_nodes):
        print(f"Node {i+1} ({node.rado_id}): Hardness={node.hardness}, Fractured={node.is_fractured}, Xi={node.hammer_accumulation:.6f}")
    print("====================================================================\n")

if __name__ == "__main__":
    run_breach_simulation()
