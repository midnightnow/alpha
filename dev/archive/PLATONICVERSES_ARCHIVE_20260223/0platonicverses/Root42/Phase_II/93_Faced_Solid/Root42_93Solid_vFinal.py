"""
Root42_93Solid_vFinal.py
The Second Talisman: 93-Faced Interference Solid
Blender 3.6+ | Python API | Root42 Archive

"The 0.000585 gap is where the ocean breathes."
"""
import bpy
import bmesh
import numpy as np
from mathutils import Vector
try:
    from scipy.spatial import ConvexHull
except ImportError:
    # If scipy is not available in Blender's python, we'll need a fallback or notify
    ConvexHull = None

# ═══════════════════════════════════════════════════════════
# ROOT42 CONSTANTS — The Biquadratic Field
# ═══════════════════════════════════════════════════════════
CONST = {
    "r42": np.sqrt(42),                    # 6.480740698 — The Engine
    "r51": np.sqrt(51),                    # 7.141428429 — The Lattice
    "r60": np.sqrt(60),                    # 7.745966692 — The Resolution
    "delta_9": 3.0,                        # The "9 Gap" (3²)
    "rho": np.sqrt(42/51),                 # 0.907485 — Packing Constant
    "eta_hex": np.pi / (2 * np.sqrt(3)),   # 0.906899 — Hex Limit
    "overpack_delta": 0.0005855308,        # The Vitality Constant ✨
    "phi": (1 + np.sqrt(5)) / 2,           # 1.618033 — Pressure Valve
    "shear_angle": np.arctan(14/17),       # 39.4° — Lineae Orientation
    "beat_freq": 0.6607,                   # Hz — Triadic Pulse
    "vertex_count": 93,                    # 42 + 51 — Interference Nodes
    "triadic_clusters": 31,                # 93 / 3 — Harmonic Groups
}

# Minimal Polynomial: x⁴ − 186x² + 81 = 0
# Roots define inner/outer breathing limits
POLY_ROOTS = [
    np.sqrt(93 - 2*np.sqrt(2142)),  # ≈ 0.658
    np.sqrt(93 + 2*np.sqrt(2142)),  # ≈ 13.638
]

def clear_scene():
    """Clean slate for artifact generation."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 250
    bpy.context.scene.frame_current = 1

def generate_93_vertices():
    """
    Generate 93 vertices at interference peaks of √42 and √51 fields.
    Applies Phi-distortion and 14/17 shear mapping.
    """
    np.random.seed(42)  # Reproducible "chaos"
    
    # High-resolution sphere grid for peak detection
    u = np.linspace(0, 2 * np.pi, 400)
    v = np.linspace(0, np.pi, 400)
    U, V = np.meshgrid(u, v)
    
    # Interference field: √42 vs √51
    field = np.abs(
        np.sin(CONST["r42"] * U) * np.sin(CONST["r51"] * V) +
        np.sin(CONST["r51"] * U) * np.sin(CONST["r42"] * V)
    )
    
    # Extract 93 highest peaks
    flat_field = field.flatten()
    indices = np.argpartition(flat_field, -CONST["vertex_count"])[-CONST["vertex_count"]:]
    peak_indices = np.unravel_index(indices, field.shape)
    
    vertices = []
    
    for i, j in zip(peak_indices[0], peak_indices[1]):
        theta = U[i, j]
        phi = V[i, j]
        
        # Base spherical coordinates
        x_base = np.sin(phi) * np.cos(theta)
        y_base = np.sin(phi) * np.sin(theta)
        z_base = np.cos(phi)
        
        # Radial displacement from Triadic Chord (√42, √51, √60)
        triadic_mod = (
            np.sin(CONST["r42"] * theta) +
            np.sin(CONST["r51"] * theta) +
            np.sin(CONST["r60"] * theta)
        ) / 3
        
        # Phi-distortion (the "pressure valve" buckling)
        phi_buckle = CONST["overpack_delta"] * np.sin(5 * theta) * np.cos(5 * phi)
        
        # 14/17 shear angle rotation (Lineae orientation)
        shear_rot = np.array([
            [np.cos(CONST["shear_angle"]), -np.sin(CONST["shear_angle"]), 0],
            [np.sin(CONST["shear_angle"]),  np.cos(CONST["shear_angle"]), 0],
            [0,                             0,                            1]
        ])
        
        # Final radius with breathing limits from minimal polynomial
        base_radius = 1.0 + 0.3 * triadic_mod + phi_buckle
        radius = np.clip(base_radius, POLY_ROOTS[0]/10, POLY_ROOTS[1]/10)
        
        # Apply shear and scale
        vec = np.array([x_base, y_base, z_base]) * radius
        vec = shear_rot @ vec
        
        vertices.append(vec)
    
    return np.array(vertices)

def create_93_solid_mesh(vertices):
    """Generate convex hull mesh from vertex cloud."""
    if ConvexHull is None:
        print("Scipy.spatial.ConvexHull not found. Creating vertices only.")
        mesh = bpy.data.meshes.new("93Solid_Vertices")
        obj = bpy.data.objects.new("93_Faced_Talisman", mesh)
        bpy.context.collection.objects.link(obj)
        mesh.from_pydata(vertices.tolist(), [], [])
        return obj

    hull = ConvexHull(vertices)
    
    # Create Blender mesh
    mesh = bpy.data.meshes.new("93Solid_Interference")
    obj = bpy.data.objects.new("93_Faced_Talisman", mesh)
    bpy.context.collection.objects.link(obj)
    
    # Extract hull faces
    faces = []
    for simplex in hull.simplices:
        faces.append(simplex.tolist())
    
    mesh.from_pydata(vertices.tolist(), [], faces)
    mesh.update()
    
    return obj

def apply_crystalline_material(obj):
    """
    Material: Crystalline Interference
    Reflects light according to 14/17 ratio.
    """
    mat = bpy.data.materials.new("Radical_Crystal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create shader nodes
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (400, 0)
    
    # Principled BSDF (crystalline base)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (0.95, 0.98, 1.0, 1.0)
    # Note: Using blender 3.6+ principled BSDF inputs
    if "Subsurface Weight" in bsdf.inputs:
        bsdf.inputs["Subsurface Weight"].default_value = 0.6
    elif "Subsurface" in bsdf.inputs:
        bsdf.inputs["Subsurface"].default_value = 0.6
    bsdf.inputs["Roughness"].default_value = 0.05
    bsdf.inputs["IOR"].default_value = 1.31  # Hexagonal ice
    
    # Emission for "66 Hz pulse" glow
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (0, -300)
    emission.inputs["Color"].default_value = (0.6, 0.2, 1.0, 1.0)  # Purple hum
    emission.inputs["Strength"].default_value = 2.0
    
    # Mix shader (crystal + glow)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (200, 0)
    mix.inputs["Fac"].default_value = 0.3
    
    # Link nodes
    links.new(bsdf.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    
    obj.data.materials.append(mat)
    return mat

def animate_triadic_wobble(obj):
    """
    Animate the 66 Hz sub-pulse as deterministic chaos.
    Rotation migrates ergodically over 250 frames.
    """
    obj.rotation_euler = (0, 0, 0)
    
    # Create animation data
    if not obj.animation_data:
        obj.animation_data_create()
    
    # Animate rotation with beat frequency modulation
    for frame in range(1, 251):
        t = frame / 24.0  # Time in seconds (24 fps)
        
        # Base rotation
        rot_z = frame * 0.02
        
        # 66 Hz wobble (scaled for visibility)
        wobble = 0.05 * np.sin(2 * np.pi * CONST["beat_freq"] * t)
        
        # Phi-based precession (slow migration)
        precession = 0.01 * np.sin(2 * np.pi * t / CONST["phi"])
        
        # Set keyframes
        obj.rotation_euler = (wobble, precession, rot_z)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)

def add_fracture_lines(obj):
    """
    Map the 14/17 shear angle as surface fracture lines (Lineae).
    These represent the "Overpack Delta" stress relief.
    """
    # Create curve for fractures
    bpy.ops.curve.primitive_bezier_curve_add()
    fractures = bpy.context.active_object
    fractures.name = "Lineae_Fractures"
    
    # Generate fracture paths along shear angle
    spline = fractures.data.splines[0]
    points = []
    
    for i in range(17):  # 17-fold symmetry
        angle = (2 * np.pi * i / 17) + CONST["shear_angle"]
        x = 1.2 * np.cos(angle)
        y = 1.2 * np.sin(angle)
        z = 0.3 * np.sin(7 * angle)  # 7-fold disruption
        points.append((x, y, z))
    
    # Add points to spline
    spline.bezier_points.add(len(points) - 1)
    for i, pt in enumerate(points):
        spline.bezier_points[i].co = Vector(pt)
    
    # Material for fractures (glowing stress lines)
    mat = bpy.data.materials.new("Stress_Lineae")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    # Ensure Emission node exists or create it
    if "Emission" in nodes:
        emission = nodes["Emission"]
    else:
        emission = nodes.new("ShaderNodeEmission")
        output = nodes.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])

    emission.inputs["Color"].default_value = (1.0, 0.3, 0.1, 1.0)  # Red-orange
    emission.inputs["Strength"].default_value = 5.0
    fractures.data.materials.append(mat)
    
    return fractures

def setup_render():
    """Cycles render settings for final artifact portrait."""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.render.resolution_x = 2048
    scene.render.resolution_y = 2048
    # Lower samples for quick preview/test unless explicitly high
    scene.cycles.samples = 128
    scene.render.film_transparent = True
    
    # Camera
    bpy.ops.object.camera_add(location=(0, -3, 1.5))
    cam = bpy.context.active_object
    cam.rotation_euler = (np.radians(75), 0, 0)
    scene.camera = cam
    
    # Lighting (three-point: cold key, warm fill, rim)
    bpy.ops.object.light_add(type='POINT', location=(2, 2, 2))
    bpy.context.active_object.data.energy = 300
    bpy.context.active_object.data.color = (0.8, 0.9, 1.0)
    
    bpy.ops.object.light_add(type='POINT', location=(-2, -1, 1))
    bpy.context.active_object.data.energy = 150
    bpy.context.active_object.data.color = (1.0, 0.7, 0.5)
    
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 3))
    bpy.context.active_object.data.energy = 100
    bpy.context.active_object.data.color = (0.6, 0.2, 1.0)  # Purple rim

def main():
    """Execute the full 93-Solid generation pipeline."""
    print("🌀 Initializing 93-Faced Interference Solid")
    
    clear_scene()
    
    vertices = generate_93_vertices()
    solid = create_93_solid_mesh(vertices)
    apply_crystalline_material(solid)
    animate_triadic_wobble(solid)
    fractures = add_fracture_lines(solid)
    setup_render()
    
    output_path = "//Assets/output/93Solid_Talisman_Final.png"
    bpy.context.scene.render.filepath = output_path
    
    print(f"✨ 93-Faced Solid ready. Minimal Polynomial: x⁴ − 186x² + 81 = 0")
    
if __name__ == "__main__":
    main()
