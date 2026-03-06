#!/bin/bash
set -e

echo "🚀 Mathman Lab: GIT SYNC V3 (FORCE MODE)"
echo "============================================"

# 1. Initialize Git if missing
if [ ! -d ".git" ]; then
    echo "⚙️  Initializing repository..."
    git init
    git branch -M main
fi

# 2. Stage and Commit
echo "📦 Staging files..."
git add .

# Check if there are changes to commit
if ! git diff-index --quiet HEAD --; then
    echo "💾 Committing changes..."
    git commit -m "feat: Mathman Lab v2.1 - Complete Project Structure"
else
    echo "ℹ️  No new changes to commit."
fi

# 3. Handle Remote URL
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$CURRENT_REMOTE" ]; then
    echo ""
    echo "⚠️  NO REMOTE LINKED"
    read -p "👉 PASTE YOUR GITHUB URL: " NEW_REMOTE
    
    if [ -z "$NEW_REMOTE" ]; then
        echo "❌ No URL provided. Exiting."
        exit 1
    fi
    
    # Remove