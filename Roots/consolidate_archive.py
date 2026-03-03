import os
import shutil

source_dir = "/Users/studio/ALPHA/Roots"
dest_dir = "/Users/studio/ALPHA/Roots_Archive"

directories_to_create = [
    "Apps/radical-resonance-root-42",
    "Apps/radical-resonance-root-51",
    "Apps/radical-resonance-root-42-music",
    "Apps/root_42_mathman-genesis",
    "Story_and_Lore",
    "Scripts",
    "Assets"
]

for d in directories_to_create:
    os.makedirs(os.path.join(dest_dir, d), exist_ok=True)

def copy_file(src, dst_folder):
    if not os.path.exists(src): return
    dst = os.path.join(dst_folder, os.path.basename(src))
    if not os.path.exists(dst):
        shutil.copy2(src, dst)

apps_mapping = {
    "radical-resonance_-root-42": "Apps/radical-resonance-root-42",
    "radical-resonance_-root-51": "Apps/radical-resonance-root-51",
    "radical-resonance_-root-42 with music": "Apps/radical-resonance-root-42-music",
    "root_42_mathman-genesis": "Apps/root_42_mathman-genesis"
}

for src_app, dest_app in apps_mapping.items():
    src_path = os.path.join(source_dir, src_app)
    dest_path = os.path.join(dest_dir, dest_app)
    if os.path.exists(src_path):
        os.system(f"cp -R '{src_path}/'* '{dest_path}/' 2>/dev/null")

lore_files = [
    "Root51/Resonance_Manuscript_v51.md",
    "Root42 1?/PRIME_DIMENSION_ROOTS.md",
    "Root42 1?/DIGITAL_ROOT_TRIPLET_VERIFICATION.md",
    "Root42 1?/ROOT42_RESONANCE_ARCHIVE_PHASE_II.md",
    "radical-resonance_-root-42/Chapter_4_The_Teeth_of_Stones_Narrative.md",
    "radical-resonance_-root-42/The_Amortization_of_Akademos.md",
    "radical-resonance_-root-42/Chapter_4_The_Teeth_of_Stones.md",
    "radical-resonance_-root-42/Seven_Constants.md",
    "roots2/diagonal_rupture.md",
    "roots2/reiman_bridge.md",
    "Root42 1?/The PMG Camera Obscura_ A Geometric Manual for Constructing Reality from the Root-42 Axiom and the 93-Faced Solid.pdf"
]

for f in lore_files:
    copy_file(os.path.join(source_dir, f), os.path.join(dest_dir, "Story_and_Lore"))

script_files = [
    "Root51/Resonance_v51_Morph.py",
    "radical-resonance_-root-42/apply_fracture_synthesis.py",
    "roots2/spiral_theodorus.py",
    "roots2/root42_root51_audit.py",
    "roots2/root_two_propulsion.py",
    "roots2/root_fields.py"
]

for f in script_files:
    copy_file(os.path.join(source_dir, f), os.path.join(dest_dir, "Scripts"))

asset_files = [
    "roots2/spiral_theodorus.png",
    "roots2/root_fields.png",
    "roots2/vector_equilibrium.json"
]

for f in asset_files:
    copy_file(os.path.join(source_dir, f), os.path.join(dest_dir, "Assets"))

print("Consolidation mapping complete.")
