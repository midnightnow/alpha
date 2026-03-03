#!/bin/bash
# DEPLOY STORY: Converts Markdown files into a unified, consolidated publication ready format.

RELEASE_DIR=/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0
STORY_DIR=$RELEASE_DIR/STORY
BUNDLE_FILE=$RELEASE_DIR/ASSETS/PMG_ROOT42_Story_Bundle.md

echo "🌀 Generating Story Bundle..."

mkdir -p $RELEASE_DIR/ASSETS

# Initialize the bundle file
cat > "$BUNDLE_FILE" <<EOF
# PMG ROOT 42: THE SOVEREIGN LATTICE (STORY BUNDLE)
**Version:** 1.0.0
**Target Volume:** 42.0

---
EOF

# Find all markdown files, sort them to ensure proper ordering, and append to the bundle
# Ordering could be specific context-wise, using sort ensures Book chapters align
find "$STORY_DIR" -type f -name "*.md" | sort | while read -r file; do
    echo "Appending: $(basename "$file")"
    
    # Adding a separator and the file contents to the master unified bundle
    echo -e "\n\n<!-- PAGE BREAK: $(basename "$file") -->\n" >> "$BUNDLE_FILE"
    cat "$file" >> "$BUNDLE_FILE"
done

echo "💎 Story Bundle generation complete: $BUNDLE_FILE"
echo "You can now use tools like Calibre or Pandoc to convert this file into a PDF or ePub:"
echo "    pandoc \"$BUNDLE_FILE\" -o \"$RELEASE_DIR/ASSETS/PMG_ROOT42_Story_Bundle.pdf\""
