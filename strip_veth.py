import re

with open("HERO_93_CANON_v1.1/COMPLETE_VETH_ARCHIVE.md", "r", encoding="utf-8") as f:
    text = f.read()

# Remove the `.VETH HEADER` blocks using regex
stripped_text = re.sub(r'---\n\.VETH HEADER.*?---\n', '', text, flags=re.DOTALL)

with open("HERO_93_CANON_v1.1/CLEAN_CANON_FOR_KDP.md", "w", encoding="utf-8") as f:
    f.write(stripped_text)
