import os
import re
import datetime
from collections import defaultdict

root_dir = '/Users/studio/ALPHA'
output_file = '/Users/studio/ALPHA/COMPREHENSIVE_BOOKS_AUDIT.md'

target_exts = {'.md', '.docx', '.txt', '.pdf', '.epub'}
pattern = re.compile(r'(book|chapter|verse|story|manuscript|platonic|narrative|manic_graphia)', re.IGNORECASE)

records = []

print("Starting audit scan...")

for dp, dirs, files in os.walk(root_dir):
    if '.git' in dp or 'node_modules' in dp or '.gemini' in dp:
        continue
    for f in files:
        if f.startswith('.'):
            continue
        ext = os.path.splitext(f)[1].lower()
        
        # Consider it if it matches our pattern or if it's a markdown file that might be a chapter
        if (pattern.search(f) or pattern.search(dp) or ext == '.md'):
            if ext in target_exts:
                full_path = os.path.join(dp, f)
                try:
                    stats = os.stat(full_path)
                    mtime = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    size = stats.st_size
                    word_count = 0
                    
                    if ext in {'.md', '.txt'}:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as txt_f:
                            content = txt_f.read()
                            word_count = len(content.split())
                    
                    records.append({
                        'path': full_path.replace(root_dir + '/', ''),
                        'filename': f,
                        'mtime': mtime,
                        'size': size,
                        'words': word_count
                    })
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")

print(f"Discovered {len(records)} relevant files. Organizing groups...")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('# Comprehensive Books & Chapters Audit\n\n')
    f.write('This audit captures every version of every book, chapter, and narrative fragment across the entire workspace.\n\n')
    
    groups = defaultdict(list)
    for r in records:
        path = r['path']
        name = r['filename']
        
        # Determine grouping
        book_match = re.search(r'book\_?(\d+)', path, re.IGNORECASE)
        chap_match = re.search(r'chapter\_?(\d+)', name, re.IGNORECASE)
        
        if book_match and chap_match:
            groups[f"Book {book_match.group(1)} - Chapter {chap_match.group(1)}"].append(r)
        elif book_match:
            groups[f"Book {book_match.group(1)} (General/Outlines)"].append(r)
        elif chap_match:
            groups[f"Chapter {chap_match.group(1)} (Unassigned)"].append(r)
        elif 'manic_graphia' in path.lower():
            groups["The Manic Graphia"].append(r)
        elif pattern.search(name):
            groups["Other Narrative Files"].append(r)
        elif 'archive' in path.lower() or 'silt' in path.lower():
            groups["Archives and Silt (Uncategorized)"].append(r)
        else:
            groups["Other Markdown Files"].append(r)

    # Sort groups logically
    def group_sort_key(g):
        import re
        b = re.search(r'Book (\d+)', g)
        c = re.search(r'Chapter (\d+)', g)
        b_num = int(b.group(1)) if b else 999
        c_num = int(c.group(1)) if c else 999
        return (b_num, c_num, g)

    for group, items in sorted(groups.items(), key=lambda x: group_sort_key(x[0])):
        f.write(f'## {group}\n')
        # sort by words descending (often the "most complete" version) then mod time
        items.sort(key=lambda x: (x['words'], x['mtime']), reverse=True)
        for i in items:
            f.write(f"- `{i['path']}` (Words: {i['words']}, Modified: {i['mtime']})\n")
        f.write('\n')

print(f"Audit complete. Written to {output_file}")
