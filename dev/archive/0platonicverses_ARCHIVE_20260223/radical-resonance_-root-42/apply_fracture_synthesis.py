import bpy
import bmesh
import numpy as np
import random

def apply_fracture_synthesis():
    # 1. Target the Artifact
    obj = bpy.data.objects.get("93_Faced_Solid")
    if not obj:
        print("Error: 93_Faced_Solid not found. Please select your mesh.")
        return

    # Ensure we are in Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # 2. Prepare the Mesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Subdivide edges to create geometry for the cracks
    # We do this selectively to keep poly count manageable
    # (Increase 'cuts' for higher resolution cracks)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2)
    
    # 3. The Physics of the Break
    # The Shear Angle: arctan(14/17)
    shear_angle = np.arctan(14/17) # approx 0.688 rad or 39.4 degrees
    
    # The "Overpack Delta" Threshold (The Breaking Point)
    # We normalize this for the mesh scale
    break_threshold = 0.82 
    
    fracture_count = 0
    
    print(f"Applying Shear Stress at {np.degrees(shear_angle):.2f} degrees...")

    for v in bm.verts:
        # Get spherical coordinates of the vertex
        x, y, z = v.co
        theta = np.arctan2(y, x)
        phi = np.arccos(z / v.co.length)
        
        # 4. The Stress Function (The "Grind")
        # We combine the 17-fold symmetry with the shear offset
        # The 'noise' adds the organic irregularity of ice
        noise = random.uniform(0.95, 1.05)
        
        # Primary Stress Vector
        stress_val = abs(np.sin(17 * theta + shear_angle) * np.sin(phi))
        
        # 5. Apply the Fracture
        if stress_val * noise > break_threshold:
            # Calculate displacement vector (Pushing OUT or IN)
            # Chaos terrain pushes out; cracks pull in.
            # We alternate based on the phase to create "Ridges" and "Troughs"
            direction = v.normal
            if random.random() > 0.5:
                 displacement = -0.04 * stress_val # Crack (In)
            else:
                 displacement = 0.02 * stress_val # Ridge (Out)
            
            v.co += direction * displacement
            fracture_count += 1

    # 6. Finalize
    bm.to_mesh(obj.data)
    bm.free()
    
    # Recalculate normals to show the sharp edges of the breaks
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_flat()
    
    print(f"Fracture Complete. {fracture_count} vertices displaced.")
    print("The Overpack Delta has been released.")

if __name__ == "__main__":
    apply_fracture_synthesis()