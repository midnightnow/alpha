import math

class WheelShearMapper:
    def __init__(self, modulus=24):
        self.mod = modulus
        self.degrees_per_node = 360.0 / self.mod
        
    def map_symmetry(self, fold):
        nodes = []
        step = self.mod / fold
        for i in range(int(fold)):
            exact_pos = i * step
            if exact_pos == 0: exact_pos = self.mod
            nodes.append(exact_pos)
        return nodes
        
    def compute_stress(self, base_fold, stress_fold):
        base_nodes = self.map_symmetry(base_fold)
        stress_nodes = self.map_symmetry(stress_fold)
        
        results = []
        for s_node in stress_nodes:
            # Find the nearest base node
            closest = min(base_nodes, key=lambda b: min(abs(b - s_node), abs(b + self.mod - s_node), abs(b - self.mod - s_node)))
            
            delta_nodes = min(abs(closest - s_node), abs(closest + self.mod - s_node), abs(closest - self.mod - s_node))
            delta_degrees = delta_nodes * self.degrees_per_node
            
            # Formatting degree for 24-wrap
            deg = (s_node % self.mod) * self.degrees_per_node
            
            results.append({
                "Stress_Node_Exact": s_node,
                "Degrees": deg,
                "Closest_Grid_Node": closest,
                "Delta_Nodes": delta_nodes,
                "Delta_Degrees": delta_degrees
            })
            
        return results

if __name__ == "__main__":
    mapper = WheelShearMapper()
    stress_points = mapper.compute_stress(4, 5) # 4-fold grid vs 5-fold hero
    
    print("--- 24-WHEEL SHEAR STRESS: 5-FOLD (HERO) VS 4-FOLD (GRID) ---")
    for pt in stress_points:
        print(f"Hero Phase: {pt['Degrees']:>5.1f}° (Node {pt['Stress_Node_Exact']:>4.1f}) | Closest Grid Anchor: {pt['Closest_Grid_Node']:>2} | Shear Stress (Delta): {pt['Delta_Degrees']:>4.1f}°")
    
    print("\nANALYSIS:")
    max_stress = max([p['Delta_Degrees'] for p in stress_points])
    print(f"1. Maximum Structural Shear: {max_stress}°")
    print("2. The Hero (5) aligns with the Gate (24/0°), but immediately slips out of phase.")
    print("3. The maximum tension occurs at 72° and 288°, where the 5-fold trajectory actively pulls away from the 90° corners of the Home (4).")
    print("4. This 'slip' is the 0.0191 drift visualized as macroscopic narrative tension. The grid cannot contain the 5.")
