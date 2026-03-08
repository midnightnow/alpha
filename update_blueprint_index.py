import os
import re

def generate_full_technical_index():
    canon_path = "/Users/studio/ALPHA/HERO_93_CANON_v1.1"
    blueprint_path = "/Users/studio/ALPHA/HERO_93_CANON_v1.1/MASTER_BLUEPRINT.md"
    
    # Get all .veth files
    veth_files = [f for f in os.listdir(canon_path) if f.endswith(".veth")]
    veth_files.sort()
    
    # Categorize
    chapters = [f for f in veth_files if "CHAPTER_" in f and "VITRIFIED" in f]
    chapters.sort(key=lambda x: int(re.search(r"CHAPTER_(\d+)", x).group(1)))
    
    master_docs = [f for f in veth_files if "MASTER_" in f or f in ["PADDOCK_THEOREM.veth", "FARMERS_SHADOW.veth", "MAINTENANCE_LOG.veth", "SURVEYORS_MAP_93.veth", "CHAPTER_GRID_MAP.veth", "CHAPTER_1_PRIME_PADDOCK.veth", "CHAPTER_62_FINAL_SEAL.veth"]]
    master_docs = sorted(list(set(master_docs)))

    new_index = "## 3. THE COMPLETE VITRIFIED CANON (62 CHAPTERS)\n"
    for c in chapters:
        num = re.search(r"CHAPTER_(\d+)", c).group(1)
        new_index += f"- [{c}](file:///Users/studio/ALPHA/HERO_93_CANON_v1.1/{c}): Chapter {num} Sealed Record.\n"
    
    new_index += "\n## 4. SYSTEM PROTOCOLS & LOGS\n"
    for d in master_docs:
        new_index += f"- [{d}](file:///Users/studio/ALPHA/HERO_93_CANON_v1.1/{d}): Technical Proof / System Record.\n"

    # read current blueprint
    with open(blueprint_path, "r") as f:
        blueprint = f.read()
    
    # Replace the technical index section
    # Find start of technical index (usually around line 83 based on previous view_file)
    # Actually, I will just append the full index to a new section or replace the old one.
    # Looking at the view_file, section 1 starts at line 91.
    
    start_marker = "## 1. CORE ENGINE ARCHITECTURE"
    if start_marker in blueprint:
        parts = blueprint.split(start_marker)
        header = parts[0]
        # We replace everything after the start marker with the new organized index
        final_blueprint = header + "# 📖 THE COMPLETE TECHNICAL INDEX\n\n" + new_index
        
        with open(blueprint_path, "w") as f:
            f.write(final_blueprint)
        print("Updated MASTER_BLUEPRINT.md with full index.")

generate_full_technical_index()
