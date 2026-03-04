import os
import shutil

CANON_DIR = '/Users/studio/ALPHA/LIBRARY_CANON'
ARCHIVE_SILT_DIR = '/Users/studio/ALPHA/LIBRARY_ARCHIVES/Precipitated_Silt'
COMPILED_BOOKS_DIR = os.path.join(CANON_DIR, 'Compiled_Books')

def get_compiled_words():
    # Gather massive text content to check if other fragments are exact sub-strings
    compiled_texts = {}
    for f in os.listdir(COMPILED_BOOKS_DIR):
        if f.endswith('.md'):
            with open(os.path.join(COMPILED_BOOKS_DIR, f), 'r', encoding='utf-8', errors='ignore') as file:
                compiled_texts[f] = file.read()
    return compiled_texts

def is_silt(filepath, compiled_texts):
    if not filepath.endswith('.md'):
        return False
    if os.path.basename(filepath) in ['MASTER_BOOK_INDEX.md', 'README.md']:
        return False
        
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return False
        
    # If the file is very small or its content is fully contained within the massive compiled books,
    # it is a fragment (silt) that was carried over instead of the diamond trail.
    # Exclude files in Foundational_Theory as they form the axioms.
    if 'Foundational_Theory' in filepath:
        return False
        
    for comp_name, comp_content in compiled_texts.items():
        # A simple heuristic: if a large chunk of the current file exists in the compiled text
        # (avoiding whitespace differences by just stripping)
        clean_content = "".join(content.split())
        if len(clean_content) > 500: # Has some substantial text
            snippet = clean_content[:500]
            clean_comp = "".join(comp_content.split())
            if snippet in clean_comp:
                return True
    return False

def run_metabolism():
    print("Initiating Geometric Metabolism (5-12-13 Filter)...")
    compiled_texts = get_compiled_words()
    
    silt_files = []
    
    for dp, dirs, files in os.walk(CANON_DIR):
        if 'Compiled_Books' in dp:
            continue
            
        for f in files:
            fp = os.path.join(dp, f)
            if is_silt(fp, compiled_texts):
                silt_files.append(fp)
                
    print(f"Identified {len(silt_files)} Silt file fragments.")
    
    if silt_files:
        os.makedirs(ARCHIVE_SILT_DIR, exist_ok=True)
        for fp in silt_files:
            dest = os.path.join(ARCHIVE_SILT_DIR, os.path.basename(fp))
            shutil.move(fp, dest)
            print(f"Precipitated: {os.path.basename(fp)}")
            
    print("Vitrification Complete. Only the Diamond Trail remains in the Canon.")

if __name__ == "__main__":
    run_metabolism()
