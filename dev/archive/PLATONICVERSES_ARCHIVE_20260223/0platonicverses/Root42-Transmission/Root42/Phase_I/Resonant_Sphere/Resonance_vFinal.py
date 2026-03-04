import bpy
import bmesh
import numpy as np

# Clear the stage
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 1. Create the Shell (The Hexagonal Stability)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, radius=1.0)
shell = bpy.context.active_object
shell.name = "Resonant_Shell"

# 2. The Displacement Logic (The Imperfection Signature)
# We apply the sqrt(42) interference as a physical displacement
def apply_resonance_displacement(obj):
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    delta_phi = 0.0801 # The Precession Constant
    
    for v in bm.verts:
        # Get spherical coordinates
        phi = np.arctan2(v.co.y, v.co.x)
        theta = np.arccos(v.co.z / v.co.length)
        
        # Calculate the 6:7 Interference (The Remainder)
        hex_comp = np.sin(6 * phi) * np.sin(6 * theta)
        hep_comp = np.sin(7 * phi + delta_phi) * np.sin(7 * theta)
        
        # The 'Stress' value
        displacement = 0.05 * (hex_comp - hep_comp)
        
        # Move the vertex along its normal
        v.co += v.normal * displacement

    bm.to_mesh(mesh)
    bm.free()

apply_resonance_displacement(shell)

# 3. Add the Core (The Emissive Pulse)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(0, 0, 0))
core = bpy.context.active_object
core.name = "Tidal_Core"

# 4. Material Setup (Gold Dust & Purple Hum)
# Note: Requires manual shader linking in Blender UI for best effect:
# - Shell: Translucent Glass (n=1.31) with the displacement map
# - Core: Emissive Orange (Strength 5.0)
# - Particles: Geometry nodes targeting displacement peaks
