import os
import re

CANON_DIR = "/Users/studio/ALPHA/HERO_93_CANON_v1.1"
EXPECTED_COUNT = 24

def final_audit():
    print("="*60)
    print("FINAL CANON AUDIT: HERO 93 v1.1")
    print("="*60)
    
    files = os.listdir(CANON_DIR)
    print(f"Total Files Found: {len(files)}")
    
    veth_files = [f for f in files if f.endswith(".veth")]
    md_files = [f for f in files if f.endswith(".md")]
    
    print(f"VETH Records: {len(veth_files)}")
    print(f"MD Records  : {len(md_files)}")
    
    # Check for VETH Headers
    sealed_count = 0
    for f in veth_files:
        path = os.path.join(CANON_DIR, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(500)
            if ".VETH HEADER" in content and "VITRIFICATION_STATUS: ABSOLUTE" in content:
                sealed_count += 1
            elif "VITRIFICATION_STATUS: Linguistic Emergence Verified" in content:
                sealed_count += 1
                
    print(f"Sealed & Vitrified: {sealed_count}/{len(veth_files)}")
    
    if len(files) >= EXPECTED_COUNT and sealed_count == len(veth_files):
        print("\n>>> AUDIT VERDICT: ZERO HYSTERESIS ACHIEVED.")
        print(">>> CANON IS LOCKED AT NOTE 0.")
    else:
        print("\n>>> WARNING: AUDIT INCOMPLETE OR INCONSISTENT.")

if __name__ == "__main__":
    final_audit()
