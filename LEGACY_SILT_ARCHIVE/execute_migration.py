import os
import shutil

ROOT = '/Users/studio/ALPHA'
ARCHIVES = os.path.join(ROOT, 'LIBRARY_ARCHIVES')
CANON = os.path.join(ROOT, 'LIBRARY_CANON')

# 1. Move CONSOLIDATED_PLATONIC_VERSES/Books to Archives
src_cpv_books = os.path.join(ROOT, 'CONSOLIDATED_PLATONIC_VERSES', 'Books')
if os.path.exists(src_cpv_books):
    shutil.move(src_cpv_books, os.path.join(ARCHIVES, 'CONSOLIDATED_PLATONIC_VERSES_Books'))
    print(f"Moved {src_cpv_books} to Archives.")

# 2. Let's look at PlatonicVerses Chapters folder
pvc_dir = os.path.join(ROOT, 'PlatonicVerses Chapters')

# Canon paths according to BOOKS_INVENTORY.md:
# Book 1: /PlatonicVerses Chapters/ (Root files in this dir, e.g. Chapter_1_The_Line to 154 sonnets etc.)
# Book 2: /PlatonicVerses Chapters/Book_2_Code_of_the_Cosmos/
# Book 3: /PlatonicVerses Chapters/Book_3_Voices_of_the_Void/
# Book 4: /PlatonicVerses Chapters/Book_4_The_Infinite_Game/
# Roots: /Root42/ and /Root51/ - wait, is Root42 actually at /Users/studio/ALPHA/Root42 or inside PMG_ROOT42_RELEASE?
# The script audit_books.py would tell us.
# Let's write the canon structure properly.
    
print("Migration script initialized. Folders prepped.")
