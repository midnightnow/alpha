import bpy
import bmesh
import numpy as np
import math

def create_resonance_morph():
    # Clear the stage
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create the Base Sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, radius=1.0)
    sphere = bpy.context.active_object
    sphere.name = "Resonance_Morph_Sphere"

    # Add Shape Keys for the Morph
    # 1. Basis (The Ideal Sphere)
    basis_key = sphere.shape_key_add(name="Basis")
    
    # 2. Key for √42 (Hex/Hep Resonance)
    key_42 = sphere.shape_key_add(name="sqrt42_Europa")
    
    # 3. Key for √51 (Triad/17 Resonance)
    key_51 = sphere.shape_key_add(name="sqrt51_Enceladus")

    # Apply deformation to √42 Key
    mesh = sphere.data
    delta_phi_42 = 0.0801
    for i, v in enumerate(key_42.data):
        co = sphere.matrix_world @ v.co
        phi = math.atan2(co.y, co.x)
        theta = math.acos(max(-1.0, min(1.0, co.z / co.length))) if co.length > 0 else 0
        
        # Hex (6) vs Hep (7)
        hex_comp = math.sin(6 * phi) * math.sin(6 * theta)
        hep_comp = math.sin(7 * phi + delta_phi_42) * math.sin(7 * theta)
        disp = 0.05 * (hex_comp - hep_comp)
        v.co += v.co.normalized() * disp

    # Apply deformation to √51 Key
    delta_phi_51 = 0.888
    for i, v in enumerate(key_51.data):
        co = sphere.matrix_world @ v.co
        phi = math.atan2(co.y, co.x)
        theta = math.acos(max(-1.0, min(1.0, co.z / co.length))) if co.length > 0 else 0
        
        # Triad (3) vs 17-gon (17)
        triad_comp = math.sin(3 * phi) * math.sin(3 * theta)
        svnt_comp = math.sin(17 * phi + delta_phi_51) * math.sin(17 * theta)
        disp = 0.03 * (triad_comp - svnt_comp) # Finer, higher-frequency whisper
        v.co += v.co.normalized() * disp

    # Material Setup
    mat = bpy.data.materials.new(name="Resonance_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.0, 0.95, 1.0, 1.0) # Cyan
    bsdf.inputs["Transmission"].default_value = 0.8
    sphere.data.materials.append(mat)

    print("√42 -> √51 Morph Sphere created with Shape Keys.")

if __name__ == "__main__":
    create_resonance_morph()
