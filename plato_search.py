import os
import re

search_dir = '/Volumes/Samsung T9 2/dev/'
output_file = '/Users/studio/ALPHA/PLATO_FILES_AUDIT.md'

target_exts = {'.md', '.docx', '.doc', '.epub'}

records = []
print(f"Scanning {search_dir} for target files containing 'plato'...")

for dp, dirs, files in os.walk(search_dir):
    if '.git' in dp or 'node_modules' in dp:
        continue
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in target_exts:
            fp = os.path.join(dp, f)
            match = False
            
            # Check filename first
            if 'plato' in f.lower():
                match = True
            elif ext == '.md':
                # Check contents for .md quickly
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as txt_f:
                        content = txt_f.read().lower()
                        if 'plato' in content:
                            match = True
                except:
                    pass
            
            # If match, record it
            if match:
                try:
                    size = os.path.getsize(fp)
                    records.append((size, fp))
                except:
                    pass

# Sort by size descending, as larger files are more likely complete books
records.sort(reverse=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('# Plato Documents on External Drive\n\n')
    for s, fp in records:
        f.write(f"- `{fp}` ({s} bytes)\n")

print(f"Audit complete. Found {len(records)} files. Written to {output_file}")
