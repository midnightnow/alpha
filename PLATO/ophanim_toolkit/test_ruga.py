
import sys
import os

# Add current directory to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rado_extension import RadoExtension, VertexState, HADES_GAP

def test_ruga_v2():
    print("=== TESTING RUGA v2.0 ===")
    
    rado = RadoExtension(seed=42)
    
    # Setup initial state
    print("[1] Initializing Substrate...")
    for i in range(3):
        rado.vertices.append(rado._create_extension_vertex(set(), set()))
    rado.vertex_counter = 3
    
    print(f"Initial Vertices: {len(rado.vertices)}")
    print(f"Initial Hammer Xi: {rado.hammer_xi}")
    print(f"Initial Clock: {rado.clock}")
    
    # Test 1: Normal RUGA Step
    print("\n[2] Testing Normal Step...")
    U = {0}
    V = {1}
    # Force entropy to be valid for the sake of test if possible, 
    # but ruga_step handles search.
    
    # We cheat slightly to ensure _hades_gate_check passes or we loop until it does
    # Actually, let's just run it and see.
    result = rado.ruga_step(U, V)
    
    if result:
        print(f"SUCCESS: Created Vertex {result.id}")
    else:
        print("Blocked/Reset triggered (Expected if simulation heavy)")
        
    print(f"Clock after step: {rado.clock}")
    
    # Test 2: Hammer Protocol (Simulate Drift)
    print("\n[3] Testing Hammer Protocol (Xi Threshold)...")
    
    # Artificially pump Xi
    rado.hammer_xi = 0.00013 # Just below 0.00014
    print(f"Pumped Xi to: {rado.hammer_xi}")
    
    # This step should push it over
    # We need to find a way to guarantee a match or force drift.
    # The existing logic calculates drift based on candidate entropy.
    
    res2 = rado.ruga_step({0}, {2})
    
    if res2:
        print(f"Step Result ID: {res2.id}")
        # Check if Hammer reset Xi
        if rado.hammer_xi < 0.0001:
            print("SUCCESS: Hammer Xi reset to 0 (Fracture occurred)")
        else:
            print(f"FAILURE: Hammer Xi not reset: {rado.hammer_xi}")
            
    # Test 3: 60-Fold Clock Reset
    print("\n[4] Testing 60-Fold Clock Reset...")
    rado.clock = 59
    print(f"Clock set to: {rado.clock}")
    
    res3 = rado.ruga_step(U, V)
    
    if res3 is None and rado.logic_lock_prevented:
        print("SUCCESS: Reset Triggered at Clock 60")
    else:
        print(f"FAILURE: Reset not triggered (Res={res3}, Lock={rado.logic_lock_prevented})")

if __name__ == "__main__":
    test_ruga_v2()
