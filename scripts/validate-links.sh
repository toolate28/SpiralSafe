#!/usr/bin/env bash
# Validate internal links in markdown documents
set -euo pipefail

echo "=== Link Validation Report ==="
echo ""

total_links=0
broken_links=0
valid_links=0

# Find all markdown files
while IFS= read -r doc; do
    # Extract markdown links [text](path)
    while IFS= read -r link; do
        ((total_links++))
        
        # Skip external links
        if [[ "$link" =~ ^https?:// ]]; then
            continue
        fi
        
        # Skip anchors
        if [[ "$link" =~ ^# ]]; then
            continue
        fi
        
        # Resolve relative path
        doc_dir=$(dirname "$doc")
        if [[ "$link" == /* ]]; then
            target=".$link"
        else
            target="$doc_dir/$link"
        fi
        
        # Normalize path
        target=$(realpath -m "$target" 2>/dev/null || echo "$target")
        
        # Check if target exists
        if [ -f "$target" ] || [ -d "$target" ]; then
            ((valid_links++))
        else
            ((broken_links++))
            echo "✗ Broken link in $doc"
            echo "  Link: $link"
            echo "  Expected: $target"
            echo ""
        fi
    done < <(grep -oP '\[.*?\]\(\K[^)]+' "$doc" 2>/dev/null || true)
done < <(find . -name "*.md" -type f \
    ! -path "./node_modules/*" \
    ! -path "./archive/*" \
    ! -path "./.git/*")

echo "=== Summary ==="
echo "Total links checked: $total_links"
echo "Valid links: $valid_links"
echo "Broken links: $broken_links"
echo ""

if [ $broken_links -eq 0 ]; then
    echo "✓ All links are valid!"
    exit 0
else
    echo "✗ Found $broken_links broken links"
    exit 1
fi
