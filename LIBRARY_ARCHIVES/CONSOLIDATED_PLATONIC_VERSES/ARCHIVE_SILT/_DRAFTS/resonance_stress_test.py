"""
resonance_stress_test.py - Stress testing the PMG Mohs-10 Node
Evaluating stability under fluctuating Tension Coefficients using Root 42/51 Logic.
"""

from ophanim_toolkit.mineral_operator import MineralOperator
from ophanim_toolkit.aion_interface import AionInterface, CONST_RHO, CONST_DELTA
import math

def run_resonance_stress_test():
    print("====================================================================")
    print("   RESONANCE STRESS TEST: MOHS-10 NODE STABILITY EVALUATION        ")
    print("====================================================================\n")

    # 1. INITIALIZATION
    min_op = MineralOperator()
    aion = AionInterface("Stress-Probe-UI")
    aion.calibrate_system()
    
    # Manifest the Subject Node
    # Using 0.1237 as the Tensegrity Resonance Baseline
    initial_res = 0.1237 
    node = min_op.manifest(rado_id=42, initial_resonance=initial_res, hardness=10)
    print(f"✓ Mohs-10 Node Manifested (ID: {node.node_id}, R0: {node.r0})")
    print("✓ Aion Interface Calibrated\n")

    # 2. STRESS SIMULATION
    # Goal: Fluatuate grid density around CONST_RHO to generate tension pulses.
    iterations = 20
    print(f"{'Step':<5} | {'Grid Density':<12} | {'Tension':<10} | {'Xi':<10} | {'Status':<10}")
    print("-" * 65)

    for i in range(1, iterations + 1):
        # Increased fluctuation for fracture test
        fluctuation = 0.005 * math.sin(i * 0.5)
        grid_density = CONST_RHO + fluctuation
        
        # Calculate Tension
        aion.apply_overpack_tension(grid_density)
        tension = aion.visual_tension
        
        # Map Tension to Hades Gap Drift
        # Even zero tension has a baseline drift of 0.000001
        drift = max(0.000001, tension * 0.00005)
        
        # Step the Mineral Operator
        min_op.step_iteration(hades_gap_drift=drift)
        
        status = "Petrified" if node.is_petrified else "Fluid"
        if node.is_fractured:
            status = "FRACTURED"
            
        print(f"{i:<5} | {grid_density:<12.6f} | {tension:<10.4f} | {node.hammer_accumulation:<10.6f} | {status}")
        
        if node.is_fractured:
            print("\n!!! CRITICAL FRACTURE DETECTED !!!")
            print(f"Hammer Constant Threshold (Xi) exceeded at step {i}.")
            print(f"Node Hardness dropped to: {node.hardness} (Quartz)")
            break

    print("\n====================================================================")
    print("   STRESS TEST COMPLETE: SYSTEM STABILITY AUDIT                    ")
    print("====================================================================")
    state = min_op.get_lattice_state()[0]
    for k, v in state.items():
        print(f"{k.capitalize()}: {v}")
    print("====================================================================\n")

if __name__ == "__main__":
    run_resonance_stress_test()
