#!/usr/bin/env bash
# Permission Execution-Layer Validation
# Prevents allow-list bypasses by validating at execution layer
# ATOM: ATOM-LIB-20260103-003-safe-exec-wrapper

# Dangerous command patterns that should be blocked
# These patterns are checked in is_dangerous_command() function
# Pattern format: regex patterns for matching dangerous commands
declare -A DANGEROUS_COMMAND_CHECKS=(
    ["rm_root"]='rm[[:space:]]+-+[rf]+[[:space:]]+/[[:space:]]|rm[[:space:]]+-+[rf]+[[:space:]]+/$'
    ["rm_home"]='rm[[:space:]]+-+[rf]+[[:space:]]+~[[:space:]]|rm[[:space:]]+-+[rf]+[[:space:]]+~$'
    ["dd_zero"]='dd[[:space:]]+if=/dev/zero'
    ["mkfs"]='mkfs\.'
    ["fork_bomb"]=':\(\)\{[[:space:]]*:|:\|:[[:space:]]*&[[:space:]]*\};:'
    ["chmod_root"]='chmod[[:space:]]+-R[[:space:]]+777[[:space:]]+/'
)

# Allow-list of safe directories for destructive operations
SAFE_DIRECTORIES=(
    "/tmp"
    "/var/tmp"
    "./build"
    "./dist"
    "./target"
)

# Check if command contains dangerous patterns
is_dangerous_command() {
    local cmd="$1"
    
    # Check against all defined dangerous command patterns
    for pattern_name in "${!DANGEROUS_COMMAND_CHECKS[@]}"; do
        local pattern="${DANGEROUS_COMMAND_CHECKS[$pattern_name]}"
        if [[ "$cmd" =~ $pattern ]]; then
            echo "[SECURITY] Dangerous pattern detected ($pattern_name): $cmd"
            return 0
        fi
    done
    
    return 1
}

# Check if path is in allow-list for destructive operations
is_path_allowed() {
    local path="$1"
    local operation="$2"
    
    # For destructive operations, check against allow-list
    if [[ "$operation" == "destructive" ]]; then
        # Expand path to absolute if it starts with /tmp
        if [[ "$path" == /tmp/* ]] || [[ "$path" == /var/tmp/* ]]; then
            return 0
        fi
        
        for safe_dir in "${SAFE_DIRECTORIES[@]}"; do
            # Handle relative paths in current directory
            if [[ "$safe_dir" == ./* ]]; then
                local abs_safe
                abs_safe="$(pwd)/${safe_dir#./}"
                if [[ "$path" == "$abs_safe"* ]]; then
                    return 0
                fi
            elif [[ "$path" == "$safe_dir"* ]]; then
                return 0
            fi
        done
        echo "[SECURITY] Path not in allow-list for destructive operations: $path"
        return 1
    fi
    
    return 0
}

# Safe execution wrapper with permission validation
safe_exec() {
    local cmd="$*"
    
    # Step 1: Check for dangerous patterns
    if is_dangerous_command "$cmd"; then
        echo "[SECURITY] Command blocked by pattern filter"
        return 1
    fi
    
    # Step 2: Extract paths and validate for destructive operations
    # More robust parsing that handles various rm flag combinations
    if [[ "$cmd" =~ rm[[:space:]] ]]; then
        # Extract the last argument which is typically the target path
        # This handles: rm -rf path, rm --recursive --force path, rm -r -f path
        local -a args
        read -ra args <<< "$cmd"
        local target_path="${args[-1]}"
        
        # Skip if target looks like a flag
        if [[ ! "$target_path" =~ ^- ]]; then
            if ! is_path_allowed "$target_path" "destructive"; then
                echo "[SECURITY] Command blocked by path validation"
                return 1
            fi
        fi
    fi
    
    # Step 3: Log execution (for audit trail)
    echo "[EXEC] $(date -u +%Y-%m-%dT%H:%M:%SZ) - Executing: $cmd"
    
    # Step 4: Execute with timeout protection (10 minutes default)
    timeout 600 bash -c "$cmd"
    local exit_code=$?
    
    if [ $exit_code -eq 124 ]; then
        echo "[SECURITY] Command timed out after 10 minutes"
        return 1
    fi
    
    return $exit_code
}
