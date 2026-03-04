import os
import datetime

TARGET_DIR = '/Users/studio/ALPHA'
OUTPUT_FILE = '/Users/studio/ALPHA/HORIZON_MAP.md'

def scan_horizon(directory):
    records = []
    
    for dp, dirs, files in os.walk(directory):
        if '.git' in dp or 'node_modules' in dp or '.gemini' in dp:
            continue
            
        for f in files:
            if f.endswith('.md') or f.endswith('.epub') or f.endswith('.docx'):
                fp = os.path.join(dp, f)
                try:
                    size = os.path.getsize(fp)
                    mtime = os.path.getmtime(fp)
                    dt = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                    records.append((size, dt, fp))
                except Exception as e:
                    pass
                    
    # Sort by "height/weight" (size descending)
    records.sort(reverse=True)
    return records

def build_map():
    print("Initiating Horizon Scan across the Paddock...")
    records = scan_horizon(TARGET_DIR)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('# THE HORIZON MAP\n')
        f.write('*A geometric survey of file mass (Z-Axis height) to isolate primitives vs compound structures.*\n\n')
        
        f.write('## I. THE PEAKS (Compound Documents / Solids)\n')
        f.write('*Files > 50,000 bytes. These are the completed "posts".*\n')
        
        for size, dt, fp in records:
            if size > 50000:
                rel = os.path.relpath(fp, TARGET_DIR)
                f.write(f"- `{rel}` (Mass: {size} bytes | Folded: {dt})\n")
                
        f.write('\n## II. THE MIDLANDS (Polygons / Chapters)\n')
        f.write('*Files between 5,000 and 50,000 bytes. Structural components.*\n')
        
        count_midlands = 0
        for size, dt, fp in records:
            if 5000 <= size <= 50000:
                count_midlands += 1
                if count_midlands <= 100: # Only show top 100 to avoid clutter
                    rel = os.path.relpath(fp, TARGET_DIR)
                    f.write(f"- `{rel}` (Mass: {size} bytes | Folded: {dt})\n")
        
        if count_midlands > 100:
            f.write(f"- ... and {count_midlands - 100} more structural polygons.\n")
                
        f.write('\n## III. THE SILT & DUNG (Fragments / Noise)\n')
        f.write('*Files < 5,000 bytes. Primed for deep archival composting.*\n')
        
        count_silt = sum(1 for size, dt, fp in records if size < 5000)
        f.write(f"- Absolute Count: {count_silt} fragmented primitives located in the soil.\n")

    print(f"Horizon Map complete. Found {len(records)} structures traversing the Z-axis. Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_map()
