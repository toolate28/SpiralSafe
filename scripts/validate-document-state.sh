#!/usr/bin/env bash
# Validate all markdown documents have proper state markers
set -euo pipefail

REQUIRED_FIELDS=("status" "last_verified" "atom_tags")
VALID_STATUSES=("active" "aspirational" "historical" "archived")

validate_document() {
    local doc="$1"
    local errors=()
    
    # Check for YAML frontmatter
    if ! head -1 "$doc" | grep -q '^---$'; then
        errors+=("Missing YAML frontmatter")
    else
        # Check required fields
        for field in "${REQUIRED_FIELDS[@]}"; do
            if ! grep -q "^${field}:" "$doc"; then
                errors+=("Missing required field: $field")
            fi
        done
        
        # Validate status value
        if grep -q '^status:' "$doc"; then
            local status
            status=$(
                awk -F':' '
                    /^status:[[:space:]]*/ {
                        # Take the part after the first colon as the value
                        val = $2
                        # Trim leading whitespace
                        sub(/^[[:space:]]+/, "", val)
                        # Trim trailing whitespace
                        sub(/[[:space:]]+$/, "", val)
                        print val
                        exit
        # Ensure there is a closing YAML frontmatter delimiter
        if ! tail -n +2 "$doc" | grep -q '^---$'; then
            errors+=("Missing closing YAML frontmatter delimiter")
        else
            # Check required fields
            for field in "${REQUIRED_FIELDS[@]}"; do
                if ! grep -q "^${field}:" "$doc"; then
                    errors+=("Missing required field: $field")
                fi
            done
            
            # Validate status value
            if grep -q '^status:' "$doc"; then
                local status
                status=$(grep '^status:' "$doc" | head -1 | sed 's/status:[[:space:]]*//' | tr -d '"' | tr -d "'")
                local valid=false
                for vs in "${VALID_STATUSES[@]}"; do
                    if [ "$status" = "$vs" ]; then
                        valid=true
                        break
                    fi
                done
                if [ "$valid" = false ]; then
                    errors+=("Invalid status: $status (must be one of: ${VALID_STATUSES[*]})")
                fi
            fi
        fi
    fi
    
    if [ ${#errors[@]} -gt 0 ]; then
        echo "✗ $doc"
        for err in "${errors[@]}"; do
            echo "    - $err"
        done
        return 1
    else
        echo "✓ $doc"
        return 0
    fi
}

main() {
    local exit_code=0
    
    echo "Validating document state markers..."
    echo ""
    
    # Find all markdown files (excluding node_modules, archive)
    while IFS= read -r doc; do
        if ! validate_document "$doc"; then
            exit_code=1
        fi
    done < <(find . -name "*.md" -type f \
        ! -path "./node_modules/*" \
        ! -path "./archive/*" \
        ! -path "./.git/*" \
        ! -name "LICENSE" \
        | sort)
    
    echo ""
    if [ $exit_code -eq 0 ]; then
        echo "All documents have valid state markers ✓"
    else
        echo "Some documents are missing state markers ✗"
    fi
    
    return $exit_code
}

main "$@"
