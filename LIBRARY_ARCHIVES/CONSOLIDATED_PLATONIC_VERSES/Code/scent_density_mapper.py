"""
SCENT DENSITY MAPPER
====================
Simulates the Ouroboros Synchronization Engine over a long-form
period (e.g., 1,200 ticks) to generate a Scent Density Map.
Visualizes how the icosahedron's movement creates interference
patterns within the 24-mod wheel.
"""

import math
from ouroboros_sync import OuroborosOrchestrator, OUROBOROS_CYCLE, SPIRAL_MOD

def generate_scent_density_map(total_ticks=1200):
    orchestrator = OuroborosOrchestrator()
    
    # Track Scent accumulation per 24-Mod wheel sector
    sector_scent = {i: 0.0 for i in range(SPIRAL_MOD)}
    sector_hits = {i: 0 for i in range(SPIRAL_MOD)}
    
    phase_locks = 0
    scent_history = []
    
    for _ in range(total_ticks):
        state = orchestrator.pulse()
        
        tick = state.get("tick", 0)
        current_scent = state.get("scent", 0.0)
        
        # Determine current sector on the 24-Mod wheel
        sector = (orchestrator.tick - 1) % SPIRAL_MOD # tick was already incremented in pulse()
        
        if state.get("status") == "PHASE_LOCK":
            phase_locks += 1
            # In phase lock, we record the avg scent from the payload, but for sector mapping we just use 0 or skip
        else:
            sector_scent[sector] += current_scent
            sector_hits[sector] += 1
            scent_history.append((tick, current_scent))
            
    # Generate Map Output
    print("=" * 60)
    print(f"SCENT DENSITY MAP ({total_ticks} TICKS)")
    print("=" * 60)
    print(f"Total Phase-Locks (Ouroboros Returns): {phase_locks}")
    print("\nDensity Distribution across 24-Mod Wheel:")
    print("Sector | Avg Scent | Density Bar")
    print("-" * 60)
    
    for sector in range(SPIRAL_MOD):
        hits = sector_hits[sector]
        avg_scent = sector_scent[sector] / hits if hits > 0 else 0.0
        
        # Visualize density bar (scale factor chosen for terminal display)
        bar_length = int(avg_scent * 100) 
        bar = "█" * (bar_length // 2)
        
        print(f"  {sector:02d}   |  {avg_scent:.5f}  | {bar}")

    print("=" * 60)

if __name__ == "__main__":
    generate_scent_density_map(1200)
