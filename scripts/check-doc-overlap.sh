#!/usr/bin/env bash
# Check for overlapping or duplicate content across documentation
set -euo pipefail

echo "=== Documentation Overlap Analysis ==="
echo ""

# Create temporary directory
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Extract key phrases from each doc (5+ word sequences)
find . -name "*.md" -type f \
    ! -path "./node_modules/*" \
    ! -path "./archive/*" \
    ! -path "./.git/*" | while read -r doc; do
    
    # Extract content (skip YAML frontmatter and code blocks)
    awk '
        BEGIN { in_code=0; in_yaml=0; yaml_count=0 }
        /^---$/ { 
            if (NR <= 3 || yaml_count == 1) { 
                in_yaml = !in_yaml; 
                yaml_count++; 
                next 
            } 
        }
        /^```/ { in_code = !in_code; next }
        !in_code && !in_yaml && NF >= 5 { print }
    ' "$doc" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' > "$TMPDIR/$(basename "$doc").txt"
done

# Find duplicate phrases
echo "Checking for significant content duplication..."
echo ""

duplicates_found=0

# Compare each pair of documents
for doc1 in "$TMPDIR"/*.txt; do
    for doc2 in "$TMPDIR"/*.txt; do
        if [ "$doc1" \< "$doc2" ]; then
            # Find common 10-word sequences
            comm -12 \
                <(sed 's/ /\n/g' "$doc1" | grep -v '^$' | sort -u) \
                <(sed 's/ /\n/g' "$doc2" | grep -v '^$' | sort -u) | wc -l | {
                read -r overlap
                
                # Calculate sizes
                size1=$(wc -w < "$doc1")
                size2=$(wc -w < "$doc2")
                
                # If overlap > 20% of smaller doc, flag it
                smaller=$((size1 < size2 ? size1 : size2))
                
                if [ $smaller -gt 0 ]; then
                    overlap_pct=$((overlap * 100 / smaller))
                    
                    if [ $overlap_pct -gt 20 ]; then
                        echo "⚠ Significant overlap detected:"
                        echo "  $(basename "$doc1" .txt) ←→ $(basename "$doc2" .txt)"
                        echo "  Overlap: $overlap_pct% of smaller document"
                        echo ""
                        duplicates_found=$((duplicates_found + 1))
                    fi
                fi
            }
        fi
    done
done

if [ $duplicates_found -eq 0 ]; then
    echo "✓ No significant content duplication found"
else
    echo "Found $duplicates_found cases of significant overlap"
    echo ""
    echo "Note: Some overlap is expected (e.g., shared terminology, examples)"
    echo "Review flagged pairs to determine if consolidation is needed"
fi

echo ""
echo "=== Document Purpose Check ==="
echo ""

# Check that each doc has unique purpose stated
find . -name "*.md" -type f \
    ! -path "./node_modules/*" \
    ! -path "./archive/*" \
    ! -path "./.git/*" | while read -r doc; do
    
    # Check for YAML intent or first paragraph
    if grep -q "^intent:" "$doc" 2>/dev/null; then
        echo "✓ $(basename "$doc") - Has explicit intent"
    elif head -20 "$doc" | grep -q "^#.*Purpose\|^#.*Overview\|^#.*What"; then
        echo "✓ $(basename "$doc") - Has purpose section"
    else
        echo "⚠ $(basename "$doc") - No clear purpose stated"
    fi
done

echo ""
echo "=== Analysis Complete ==="
