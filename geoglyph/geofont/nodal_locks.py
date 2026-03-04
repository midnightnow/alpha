import numpy as np
import math

def calculate_overlaps():
    # Node counts
    systems = {
        "Hebrew (Foundation)": 11,
        "Greek (Measure)": 12,
        "Latin (Vortex)": 13
    }
    
    # We look for "Nodal Locks" - angles where nodes from different systems converge
    # Tolerance for a "Lock" in degrees
    TOLERANCE = 5.0
    
    locks = []
    
    # Get all angles
    angles = {}
    for name, n in systems.items():
        angles[name] = [round(i * (360/n), 2) for i in range(n)]
        
    print("--- NODAL LOCK ANALYSIS (Refractive Overlap) ---")
    print(f"Tolerance: {TOLERANCE}°\n")
    
    # Compare systems
    system_names = list(systems.keys())
    for i in range(len(system_names)):
        for j in range(i + 1, len(system_names)):
            s1_name = system_names[i]
            s2_name = system_names[j]
            
            for idx1, a1 in enumerate(angles[s1_name]):
                for idx2, a2 in enumerate(angles[s2_name]):
                    diff = abs(a1 - a2)
                    # Handle 360 wrap
                    if diff > 180: diff = 360 - diff
                    
                    if diff <= TOLERANCE:
                        locks.append({
                            "systems": (s1_name, s2_name),
                            "indices": (idx1, idx2),
                            "angle": round((a1 + a2) / 2, 2),
                            "error": round(diff, 2)
                        })

    # Sort locks by angle
    locks.sort(key=lambda x: x["angle"])
    
    print(f"{'Systems':<40} | {'Nodes':<10} | {'Angle':<8} | {'Error'}")
    print("-" * 75)
    for l in locks:
        # Filter out Node 0 as it always locks at 0 degrees
        if l["angle"] < 1.0: continue
        
        sys_str = f"{l['systems'][0]} / {l['systems'][1]}"
        node_str = f"N{l['indices'][0]} / N{l['indices'][1]}"
        print(f"{sys_str:<40} | {node_str:<10} | {l['angle']:<8}° | {l['error']}°")

    # Triple Locks (All three systems converge)
    print("\n--- TRIPLE LOCKS (Universal Resonance) ---")
    for idx1, a1 in enumerate(angles["Hebrew (Foundation)"]):
        for idx2, a2 in enumerate(angles["Greek (Measure)"]):
            for idx3, a3 in enumerate(angles["Latin (Vortex)"]):
                # Pairwise checks
                d12 = abs(a1 - a2)
                if d12 > 180: d12 = 360 - d12
                d23 = abs(a2 - a3)
                if d23 > 180: d23 = 360 - d23
                d13 = abs(a1 - a3)
                if d13 > 180: d13 = 360 - d13
                
                # We show "Near Misses" as well
                if d12 <= 10.0 and d23 <= 10.0 and d13 <= 10.0:
                    if a1 < 1.0: continue # Skip origin
                    avg_a = round((a1 + a2 + a3) / 3, 2)
                    max_err = max(d12, d23, d13)
                    print(f"Angle: {avg_a:>6}° | Max Err: {max_err:.2f}° (H:N{idx1}, G:N{idx2}, L:N{idx3})")

if __name__ == "__main__":
    calculate_overlaps()
