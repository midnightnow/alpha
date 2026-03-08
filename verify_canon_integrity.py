import os

CANON_DIR = "/Users/studio/ALPHA/HERO_93_CANON_v1.1"

def verify():
    files = os.listdir(CANON_DIR)
    print(f"Total files in Canon: {len(files)}")
    veth_count = len([f for f in files if f.endswith(".veth")])
    md_count = len([f for f in files if f.endswith(".md")])
    
    print(f"VETH: {veth_count}, MD: {md_count}")
    
    for f in sorted(files):
        print(f"- [x] {f}")

if __name__ == "__main__":
    verify()
