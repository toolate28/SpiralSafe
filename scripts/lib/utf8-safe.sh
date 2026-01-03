#!/usr/bin/env bash
# UTF-8 Safe String Operations
# Prevents fatal crashes with CJK characters and other multi-byte encodings
# ATOM: ATOM-LIB-20260103-001-utf8-safe-strings

# Ensure UTF-8 locale for all string operations
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Safe string length - handles multi-byte characters correctly
utf8_length() {
    local str="$1"
    # Use wc with -m for character count (not byte count)
    echo -n "$str" | wc -m | tr -d ' '
}

# Safe substring extraction - prevents splitting multi-byte characters
utf8_substring() {
    local str="$1"
    local start="$2"
    local length="${3:-}"
    
    # Validate that start is at least 1 (1-based indexing)
    if [ "$start" -lt 1 ]; then
        echo "[ERROR] utf8_substring: start position must be >= 1, got: $start" >&2
        return 1
    fi
    
    # Use Python for proper UTF-8 substring handling
    if command -v python3 >/dev/null 2>&1; then
        if [ -z "$length" ]; then
            python3 -c "import sys; s=sys.argv[1]; start=max(int(sys.argv[2])-1, 0); print(s[start:])" "$str" "$start"
        else
            python3 -c "import sys; s=sys.argv[1]; start=max(int(sys.argv[2])-1, 0); length=max(int(sys.argv[3]), 0); print(s[start:start+length])" "$str" "$start" "$length"
        fi
    else
        # Fallback to cut (may not handle UTF-8 properly)
        if [ -z "$length" ]; then
            echo -n "$str" | cut -c"${start}-"
        else
            echo -n "$str" | cut -c"${start}-$((start + length - 1))"
        fi
    fi
}

# Validate UTF-8 encoding - returns 0 if valid, 1 if invalid
utf8_validate() {
    local str="$1"
    echo -n "$str" | iconv -f UTF-8 -t UTF-8 >/dev/null 2>&1
    return $?
}

# Safe echo - ensures output doesn't corrupt terminal with invalid UTF-8
utf8_echo() {
    local str="$1"
    if utf8_validate "$str"; then
        echo "$str"
    else
        # Strip invalid sequences and output
        echo -n "$str" | iconv -f UTF-8 -t UTF-8 -c
        echo " [!UTF-8 cleaned]"
    fi
}
