import os
import re

directories = [
    "/Users/studio/ALPHA/PMG_LATTICE",
    "/Users/studio/ALPHA/LIBRARY_CANON/Book_1_Platonic_Verses",
    "/Users/studio/ALPHA/LIBRARY_CANON/Book_2_Code_of_the_Cosmos",
    "/Users/studio/ALPHA/LIBRARY_CANON/Book_3_Voices_of_the_Void",
    "/Users/studio/ALPHA/LIBRARY_CANON/Book_4_The_Infinite_Game"
]

results = []

for d in directories:
    if not os.path.exists(d):
        continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        words = len(re.findall(r'\w+', content))
                        
                        # Extract title (first # header)
                        title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
                        title = title_match.group(1).strip() if title_match else f
                        
                        # Identify Card (look for "of Spades", "of Hearts", etc. in title or filename)
                        card = "N/A"
                        card_match = re.search(r'([0-9A-Za-z]+ of (Spades|Hearts|Diamonds|Clubs))', title + " " + f, re.IGNORECASE)
                        if card_match:
                            card = card_match.group(1).title()
                        
                        results.append({
                            "filename": f,
                            "title": title,
                            "card": card,
                            "wordcount": words,
                            "path": path
                        })
                except Exception as e:
                    pass

# Sort by filename to keep some order
results.sort(key=lambda x: x['filename'])

print(f"{'Filename':<50} | {'Card':<20} | {'Words':<10} | {'Title'}")
print("-" * 120)
total_words = 0
for r in results:
    print(f"{r['filename']:<50} | {r['card']:<20} | {r['wordcount']:<10} | {r['title']}")
    total_words += r['wordcount']

print("-" * 120)
print(f"TOTAL CHAPTERS: {len(results)}")
print(f"TOTAL WORD COUNT: {total_words}")
