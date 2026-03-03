#!/bin/bash
# 🌀 ROOT 42: NARRATIVE VITRIFICATION
# Converts Markdown story files into a single distribution package.

STORY_DIR=~/ALPHA/STORY
RELEASE_DIR=~/ALPHA/PMG_ROOT42_RELEASE_v1.0/STORY
DIST_FILE=~/ALPHA/PMG_ROOT42_RELEASE_v1.0/ASSETS/PMG_ROOT42_The_Snail_Eats_Diamond_Dust.pdf

echo "🧪 Consolidating Chapters 1-4 + Epilogue..."

mkdir -p "$RELEASE_DIR"
mkdir -p ~/ALPHA/PMG_ROOT42_RELEASE_v1.0/ASSETS

# If you have 'pandoc' or 'pagedjs-cli' installed:
pandoc "$STORY_DIR"/*.md -o "$DIST_FILE" \
    --metadata title="PMG ROOT 42: The Snail Eats Diamond Dust" \
    --toc --toc-depth=2 \
    --pdf-engine=weasyprint

# Create a zip archive of the raw MDs for the 'Source' bundle
zip -r ~/ALPHA/PMG_ROOT42_RELEASE_v1.0/ASSETS/NARRATIVE_SOURCE_v1.0.zip "$STORY_DIR"/*.md

echo "💎 Story Vitrified at $DIST_FILE"
