import os
import re

# Define paths
BOOK_1_PATH = "/Users/studio/ALPHA/PMG_LATTICE/The_Platonic_Verses_Book_1.md"
CANON_DIR = "/Users/studio/ALPHA/LIBRARY_CANON"

results = {
    "Prologues": [],
    "Weeks": [],
    "Completion": [],
    "Supplements": []
}

# 1. Audit Book 1 for Prologues (Chapters 0-4)
if os.path.exists(BOOK_1_PATH):
    with open(BOOK_1_PATH, 'r') as f:
        content = f.read()
        # Split by Chapter headers to get word counts for sub-chapters
        chapters = re.split(r'(?m)^# (Chapter \d.*)', content)
        # The first element is the book intro
        header_text = chapters[0]
        results["Prologues"].append({
            "title": "Book 1 Introduction",
            "words": len(re.findall(r'\w+', header_text)),
            "card": "N/A"
        })
        for i in range(1, len(chapters), 2):
            title = chapters[i]
            body = chapters[i+1]
            words = len(re.findall(r'\w+', body))
            results["Prologues"].append({
                "title": title,
                "words": words,
                "card": "N/A"
            })

# 2. Audit Library Canon for Weeks and Completion
for root, dirs, files in os.walk(CANON_DIR):
    for f in files:
        if f.endswith(".md"):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
                words = len(re.findall(r'\w+', content))
                title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else f
                
                card = "N/A"
                card_match = re.search(r'([0-9A-Za-z]+ of (Spades|Hearts|Diamonds|Clubs))', title + " " + f, re.IGNORECASE)
                if card_match:
                    card = card_match.group(1).title()

                # Categorize based on Chapter number
                chapter_num_match = re.search(r'Chapter_(\d+)', f)
                if chapter_num_match:
                    num = int(chapter_num_match.group(1))
                    if 1 <= num <= 52:
                        results["Weeks"].append({"title": title, "card": card, "words": words, "num": num})
                    elif num > 52:
                        results["Completion"].append({"title": title, "card": card, "words": words, "num": num})
                else:
                    results["Supplements"].append({"title": title, "card": card, "words": words})

# Sort Results
results["Weeks"].sort(key=lambda x: x['num'])
results["Completion"].sort(key=lambda x: x['num'])

# Final Table Printing
def print_section(name, items):
    print(f"\n### {name}")
    print(f"{'Title':<60} | {'Card':<20} | {'Words':<10}")
    print("-" * 95)
    total = 0
    for item in items:
        print(f"{item['title'][:60]:<60} | {item.get('card', 'N/A'):<20} | {item['words']:<10}")
        total += item['words']
    print(f"{'TOTAL':<60} | {'':<20} | {total:<10}")
    return total

grand_total = 0
grand_total += print_section("I. THE PROLOGUES (Book 1)", results["Prologues"])
grand_total += print_section("II. THE 52 WEEKLY CHAPTERS (Canon)", results["Weeks"])
grand_total += print_section("III. COMPLETION & LEAP CHAPTERS", results["Completion"])
grand_total += print_section("IV. VITRIFIED TECHNICAL SUPPLEMENTS", results["Supplements"])

print(f"\n{'='*95}")
print(f"{'GRAND TOTAL WORD COUNT':<80} | {grand_total:<10}")
print(f"{'='*95}")
