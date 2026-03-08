import os

def generate_master_blueprint(output_path):
    print("Generating Master Blueprint...")
    
    # Priority Files
    priority = [
        "/Users/studio/ALPHA/PMG_LATTICE/TECHNICAL_INDEX.md",
        "/Users/studio/ALPHA/PMG_LATTICE/RESONANCE_LOCK_THEOREM.md",
        "/Users/studio/ALPHA/PMG_LATTICE/GEOMETRIC_93_MAP.md",
        "/Users/studio/ALPHA/PMG_LATTICE/GEOMETRIC_INSIGHTS_REFERENCE.md",
        "/Users/studio/ALPHA/PMG_LATTICE/The_Vitrified_Index_Platonic_Verses.md",
        "/Users/studio/ALPHA/PMG_LATTICE/The_Platonic_Verses_Book_1.md",
        "/Users/studio/ALPHA/PMG_LATTICE/Chapter_61_The_Join.md"
    ]
    
    with open(output_path, 'w', encoding='utf-8') as blueprint:
        blueprint.write("# 🏛️ THE MASTER BLUEPRINT: THE PLATONIC VERSES & SOVEREIGN ENGINE\n\n")
        blueprint.write("**Status:** FINAL VITRIFICATION | **Date:** 2026-03-07\n\n")
        blueprint.write("---\n\n")
        
        for p in priority:
            if os.path.exists(p):
                with open(p, 'r') as f:
                    blueprint.write(f"\n\n## SOURCE: {os.path.basename(p)}\n")
                    blueprint.write("---\n")
                    blueprint.write(f.read())
                    blueprint.write("\n\n---\n")
    
    print(f"Master Blueprint generated at: {output_path}")

if __name__ == "__main__":
    generate_master_blueprint("/Users/studio/ALPHA/Master_Blueprint.md")
