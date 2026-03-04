import os
import shutil

ROOT = '/Users/studio/ALPHA'
ARCHIVES = os.path.join(ROOT, 'LIBRARY_ARCHIVES')
CANON = os.path.join(ROOT, 'LIBRARY_CANON')

def safe_move(src, dest_dir):
    if not os.path.exists(src):
        return
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(src))
    if not os.path.exists(dest_path):
        shutil.move(src, dest_path)
        print(f"Moved {src} to {dest_dir}")

# Canon directories
canon_b1 = os.path.join(CANON, 'Book_1_Platonic_Verses')
canon_b2 = os.path.join(CANON, 'Book_2_Code_of_the_Cosmos')
canon_b3 = os.path.join(CANON, 'Book_3_Voices_of_the_Void')
canon_b4 = os.path.join(CANON, 'Book_4_The_Infinite_Game')
canon_foundational = os.path.join(CANON, 'Foundational_Theory')
canon_standalone = os.path.join(CANON, 'Standalone_Vocational')

# 1. Book 2
b2_src = os.path.join(ROOT, 'PlatonicVerses Chapters', 'Book_2_Code_of_the_Cosmos')
safe_move(b2_src, CANON)

# 2. Book 3
b3_src = os.path.join(ROOT, 'PlatonicVerses Chapters', 'Book_3_Voices_of_the_Void')
safe_move(b3_src, CANON)

# 3. Book 4
b4_src = os.path.join(ROOT, 'PlatonicVerses Chapters', 'Book_4_The_Infinite_Game')
safe_move(b4_src, CANON)

# 4. Standalone
pvc_dir = os.path.join(ROOT, 'PlatonicVerses Chapters')
if os.path.exists(pvc_dir):
    safe_move(os.path.join(pvc_dir, 'Chapter_7_The_Pavers_Grid.md'), canon_standalone)
    safe_move(os.path.join(pvc_dir, 'Chapter_8_The_Gaugers_Tide.md'), canon_standalone)
    safe_move(os.path.join(ROOT, 'Example_Chapter_The_Weavers_Tensegrity.md'), canon_standalone)

# 5. Foundational Theory
theory_files = [
    'README_PRINCIPIA_MATHEMATICA_GEOMETRICA.md',
    'The_60Fold_Vector_Field.md',
    'The_Hired_Mans_Field_Guide_2026.md',
    'PLATO_The_Fractal_Name_Analysis.md',
    'Deep_Onomatopoeia_Dictionary_Implementation.md',
    'Sandbox_World_Architecture.md',
    'Platonic_Verses_Staging_Protocol.md',
    'System_Architecture_Olympian_Standard_v2.3.md',
    'COMPLETE_SYSTEM_SUMMARY.md'
]
for tf in theory_files:
    # They could be in ROOT or CONSOLIDATED_PLATONIC_VERSES
    tf_path = os.path.join(ROOT, tf)
    if os.path.exists(tf_path):
        safe_move(tf_path, canon_foundational)
        
# 6. Book 1 (Sonnets and analyses in pvc_dir)
# These are files like Complete_Platonic_Verses_Master_Index.md and Octaves
if os.path.exists(pvc_dir):
    for f in os.listdir(pvc_dir):
        fp = os.path.join(pvc_dir, f)
        if os.path.isfile(fp):
            # Move all remaining naked files in pvc_dir to Book 1 as they are mostly the octave docs
            safe_move(fp, canon_b1)

# 7. Roots Archive Canon
# The inventory says /Root42/ and /Root51/
root42_src = os.path.join(ROOT, 'Roots_Archive', 'Root42') # Guessing path
if not os.path.exists(root42_src):
     root42_src = os.path.join(ROOT, 'M=42') # or similar
root51_src = os.path.join(ROOT, 'Roots_Archive', 'Root51')

# 8. Now move the REST of legacy PlatonicVerses Chapters to Archives
if os.path.exists(pvc_dir):
    arch_pvc = os.path.join(ARCHIVES, 'PlatonicVerses_Chapters_Legacy')
    os.makedirs(arch_pvc, exist_ok=True)
    for f in os.listdir(pvc_dir):
        fp = os.path.join(pvc_dir, f)
        shutil.move(fp, arch_pvc)
    print("Moved remaining PlatonicVerses Chapters to Archives.")

# 9. Also move CONSOLIDATED_PLATONIC_VERSES entirely to Archives since it's redundant / mostly old papers
cpv_dir = os.path.join(ROOT, 'CONSOLIDATED_PLATONIC_VERSES')
if os.path.exists(cpv_dir):
    safe_move(cpv_dir, ARCHIVES)

print("Migration step 2 complete.")
