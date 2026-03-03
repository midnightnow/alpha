import os
import shutil
import glob

print("Starting consolidation script...")

BASE = "/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES"
OLD = os.path.join(BASE, "0platonicverses")
CHAP_TOP = os.path.join(BASE, "PlatonicVerses Chapters")
CHAP_NEST = os.path.join(OLD, "PlatonicVerses Chapters")
BOOKS_DIR = os.path.join(BASE, "Books")
CODE_DIR = os.path.join(BASE, "Code")
DOCS_DIR = os.path.join(BASE, "Docs")
ARCHIVE_DIR = os.path.join(BASE, "_ARCHIVE")

# Directories to create
dirs_to_create = [
    os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses"),
    os.path.join(BOOKS_DIR, "Book_2_Babble"),
    os.path.join(BOOKS_DIR, "Book_3_Sexagesimal"),
    os.path.join(BOOKS_DIR, "Book_4_The_Sovereign_Lattice"),
    os.path.join(BOOKS_DIR, "Book_5_Sonnets"),
    CODE_DIR,
    DOCS_DIR,
    ARCHIVE_DIR,
]

for d in dirs_to_create:
    os.makedirs(d, exist_ok=True)

def safe_move(src, dst):
    if os.path.exists(src):
        try:
            if os.path.isdir(src):
                # if destination already exists and is a dir, move contents
                if os.path.exists(dst) and os.path.isdir(dst):
                    for item in os.listdir(src):
                        s = os.path.join(src, item)
                        d = os.path.join(dst, item)
                        safe_move(s, d)
                else:
                    shutil.move(src, dst)
            else:
                shutil.move(src, dst)
            print(f"Moved: {src} -> {dst}")
        except Exception as e:
            print(f"Error moving {src} to {dst}: {e}")

# --- BOOK 1 ---
safe_move(os.path.join(CHAP_TOP, "PlatonicVerses_Complete_Book1.md"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses"))
safe_move(os.path.join(CHAP_TOP, "PlatonicVerses_Complete_Book1.epub"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses"))
safe_move(os.path.join(CHAP_TOP, "Chapter_0_Foreword_The_Leak.md"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses"))
safe_move(os.path.join(CHAP_TOP, "Chapter_0_The_Void"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses", "Chapter_0_The_Void"))
safe_move(os.path.join(CHAP_TOP, "Chapter_1_The_Line"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses", "Chapter_1_The_Line"))
safe_move(os.path.join(CHAP_TOP, "Chapter_2_The_Angle"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses", "Chapter_2_The_Angle"))
safe_move(os.path.join(CHAP_TOP, "Chapter_3_The_Plane"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses", "Chapter_3_The_Plane"))
safe_move(os.path.join(CHAP_TOP, "Chapter_4_The_Solid"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses", "Chapter_4_The_Solid"))
safe_move(os.path.join(CHAP_TOP, "Appendix_A_Introductory_Manual.md"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses"))
safe_move(os.path.join(CHAP_TOP, "Appendix_The_Agrafa_Dogmata.md"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses"))
safe_move(os.path.join(CHAP_TOP, "Epilogue_The_Man_Who_Ate_at_Noon.md"), os.path.join(BOOKS_DIR, "Book_1_The_Platonic_Verses"))

# --- BOOK 2 ---
safe_move(os.path.join(CHAP_TOP, "Book_2_Babble"), os.path.join(BOOKS_DIR, "Book_2_Babble"))
# Archive the alt Volume 2
safe_move(os.path.join(CHAP_TOP, "Volume_2_Babble"), os.path.join(ARCHIVE_DIR, "Book_2_Volume_2_Babble_Drafts"))
# Move Code of the Cosmos to an Appendix of Book 2
safe_move(os.path.join(CHAP_NEST, "Book_2_Code_of_the_Cosmos"), os.path.join(BOOKS_DIR, "Book_2_Babble", "Appendix_Code_of_the_Cosmos"))

# --- BOOK 3 ---
# Move from top level
safe_move(os.path.join(CHAP_TOP, "Book_3_Sexagesimal"), os.path.join(BOOKS_DIR, "Book_3_Sexagesimal"))
# Move from nested level
safe_move(os.path.join(CHAP_NEST, "Book_3_Voices_of_the_Void"), os.path.join(BOOKS_DIR, "Book_3_Sexagesimal", "Appendix_Voices_of_the_Void"))

# --- BOOK 4 ---
# Keep Sovereign Lattice as the canonical Book 4 name, per latest notes
safe_move(os.path.join(CHAP_NEST, "Book_4_The_Sovereign_Lattice"), os.path.join(BOOKS_DIR, "Book_4_The_Sovereign_Lattice"))
# Archive the other Book 4 drafts
safe_move(os.path.join(CHAP_NEST, "Book_4_The_Infinite_Game"), os.path.join(ARCHIVE_DIR, "Book_4_The_Infinite_Game_Draft"))
safe_move(os.path.join(CHAP_NEST, "Book_4_The_Architects_Exile"), os.path.join(ARCHIVE_DIR, "Book_4_The_Architects_Exile_Draft"))
safe_move(os.path.join(CHAP_NEST, "Book_4_The_Players"), os.path.join(ARCHIVE_DIR, "Book_4_The_Players_Draft"))

# --- BOOK 5 SONNETS ---
for f in glob.glob(os.path.join(CHAP_NEST, "*Octave*.md")):
    safe_move(f, os.path.join(BOOKS_DIR, "Book_5_Sonnets"))
for f in glob.glob(os.path.join(CHAP_NEST, "The_Dark_Lady_Sequence*.md")):
    safe_move(f, os.path.join(BOOKS_DIR, "Book_5_Sonnets"))
for f in glob.glob(os.path.join(CHAP_NEST, "The_Fair_Youth_Conclusion*.md")):
    safe_move(f, os.path.join(BOOKS_DIR, "Book_5_Sonnets"))
for f in glob.glob(os.path.join(CHAP_NEST, "The_Final_Coda*.md")):
    safe_move(f, os.path.join(BOOKS_DIR, "Book_5_Sonnets"))

# --- CODE ---
safe_move(os.path.join(OLD, "lib"), os.path.join(CODE_DIR, "lib"))
safe_move(os.path.join(OLD, "ophanim_toolkit"), os.path.join(CODE_DIR, "ophanim_toolkit"))
safe_move(os.path.join(OLD, "PMG_LATTICE"), os.path.join(CODE_DIR, "PMG_LATTICE"))
# Canonical app
safe_move(os.path.join(OLD, "radical-resonance_-root-42"), os.path.join(CODE_DIR, "radical-resonance_-root-42"))
safe_move(os.path.join(OLD, "radical-resonance_-root-51"), os.path.join(CODE_DIR, "radical-resonance_-root-51"))
# Archive "with music" and "transmission"
safe_move(os.path.join(OLD, "radical-resonance_-root-42 with music"), os.path.join(ARCHIVE_DIR, "radical-resonance_-root-42_music"))
safe_move(os.path.join(OLD, "Root42-Transmission"), os.path.join(ARCHIVE_DIR, "Root42-Transmission"))
safe_move(os.path.join(OLD, "Root42"), os.path.join(ARCHIVE_DIR, "Legacy_Root42_Archive"))

# Move .py and .ts standalone scripts
for script in glob.glob(os.path.join(OLD, "*.py")):
    safe_move(script, os.path.join(CODE_DIR, os.path.basename(script)))
for script in glob.glob(os.path.join(OLD, "*.ts")):
    safe_move(script, os.path.join(CODE_DIR, os.path.basename(script)))

# --- DOCS ---
safe_move(os.path.join(OLD, "CONSTANTS_CANON.md"), DOCS_DIR)
safe_move(os.path.join(OLD, "COMPLETE_SYSTEM_SUMMARY.md"), DOCS_DIR)
safe_move(os.path.join(OLD, "NARRATIVE_AND_WORLDBUILDING_PLAN.md"), DOCS_DIR)
safe_move(os.path.join(OLD, "2026_MOONSHOT_ROADMAP.md"), DOCS_DIR)
safe_move(os.path.join(OLD, "BOOKS_INVENTORY.md"), DOCS_DIR)
safe_move(os.path.join(OLD, "SOVEREIGN_LEDGER.md"), DOCS_DIR)
# Move the main README to ROOT
safe_move(os.path.join(OLD, "README_PRINCIPIA_MATHEMATICA_GEOMETRICA.md"), os.path.join(BASE, "README.md"))

# --- CLEANUP (Archive the rest) ---
safe_move(os.path.join(OLD, "Sequel_Terrible_To_Behold"), os.path.join(BOOKS_DIR, "Sequel_Terrible_To_Behold"))

# Everything remaining in 0platonicverses and PlatonicVerses Chapters moves to Archive
if os.path.exists(OLD):
    for item in os.listdir(OLD):
        safe_move(os.path.join(OLD, item), os.path.join(ARCHIVE_DIR, f"legacy_{item}"))
    try:
        os.rmdir(OLD)
    except:
        pass

if os.path.exists(CHAP_TOP):
    for item in os.listdir(CHAP_TOP):
        safe_move(os.path.join(CHAP_TOP, item), os.path.join(ARCHIVE_DIR, f"legacy_{item}"))
    try:
        os.rmdir(CHAP_TOP)
    except:
        pass

# INDEX ARCHIVE
archive_index = ["# ARCHIVE INDEX\n"]
for root, dirs, files in os.walk(ARCHIVE_DIR):
    rel = os.path.relpath(root, ARCHIVE_DIR)
    if rel == ".":
        for d in dirs: archive_index.append(f"- **{d}/**\n")
        for f in files: archive_index.append(f"- {f}\n")

with open(os.path.join(ARCHIVE_DIR, "INDEX.md"), "w") as f:
    f.writelines(archive_index)

print("Consolidation finished.")
