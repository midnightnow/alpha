import os
import glob
import datetime

def compile_compendium():
    lattice_dir = "/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES/PMG_LATTICE"
    output_file = "/Users/midnight/dev/CONSOLIDATED_PLATONIC_VERSES/PLATONIC_VERSES_MASTER_COMPENDIUM.md"
    
    # Core reading order based on final integration log
    core_files = [
        "The_Cognitive_Compression_Preface.md",
        "The_Administrator_s_Guide_The_Three_Registers.md",
        "The_10_24_26_Correspondences.md",
        "The_4_5_Paradox_Protocol.md",
        "The_Audit_of_the_Sea_The_Fluid_Lubricant.md",
        "The_Audit_of_the_Sea_Social_Synchronicity.md",
        "The_Kinetic_Tally_of_Tacking.md",
        "The_Tally_of_the_Horseshoe.md",
        "The_Heroine_s_Narrative_Outline.md",
        "The_Heroine_s_Canticle.md",
        "The_Three_Register_Firewall_Checklist.md",
        "Index_of_Word_Geometry_Correspondences.md",
        "The_Final_Colophon.md",
        "The_Return_to_the_Open_Voice.md",
        "The_Heroine_s_Departure_The_Final_Tack.md",
        "Archive_Log_The_Final_Consolidated_Index.md",
        "The_Final_Operational_Seal.md"
    ]
    
    print(f"Buidling Platonic Verses Master Compendium...")
    
    with open(output_file, 'w') as outfile:
        outfile.write("# THE PLATONIC VERSES: MASTER COMPENDIUM\n")
        outfile.write(f"**COMPILED:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write("**COORDINATE:** All Ways. For Ever. Now.\n\n")
        outfile.write("---\n\n")
        
        for filename in core_files:
            filepath = os.path.join(lattice_dir, filename)
            if os.path.exists(filepath):
                print(f"Integrating: {filename}")
                with open(filepath, 'r') as infile:
                    outfile.write(infile.read() + "\n\n---\n\n")
            else:
                print(f"Warning: Could not find {filename}")
                
    print(f"\nConsolidation complete. Master file located at: {output_file}")

if __name__ == "__main__":
    compile_compendium()
