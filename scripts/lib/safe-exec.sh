#!/usr/bin/env bash
# Permission Execution-Layer Validation
# Prevents allow-list bypasses by validating at execution layer
# ATOM: ATOM-LIB-20260103-003-safe-exec-wrapper

# Dangerous command patterns that should be blocked
# These patterns are checked in is_dangerous_command() function
# Pattern format: regex patterns for matching dangerous commands
declare -A DANGEROUS_COMMAND_CHECKS=(
    ["rm_root"]='rm[[:space:]]+(((-[rRfF][^[:space:]]*|--recursive|--force)[[:space:]]+)+/([[:space:]]|$)|/([[:space:]]+(-[rRfF][^[:space:]]*|--recursive|--force))+([[:space:]]|$))'
    ["rm_home"]='rm[[:space:]]+(((-[rRfF][^[:space:]]*|--recursive|--force)[[:space:]]+)+~([[:space:]]|$)|~([[:space:]]+(-[rRfF][^[:space:]]*|--recursive|--force))+([[:space:]]|$))'
    ["dd_zero"]='dd[[:space:]]+if=/dev/zero'
    ["mkfs"]='mkfs\.'
    ["fork_bomb"]='([[:alnum:]_:.]+)[[:space:]]*\(\)[[:space:]]*\{[^}]*\1[[:space:]]*\|[[:space:]]*\1[[:space:]]*&[^}]*\}[[:space:]]*;?'
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
        # Canonicalize the path to prevent bypass via symlinks or relative paths
        local canonical_path
        if command -v realpath >/dev/null 2>&1; then
            canonical_path=$(realpath -m "$path" 2>/dev/null) || canonical_path="$path"
        elif command -v readlink >/dev/null 2>&1; then
            canonical_path=$(readlink -f "$path" 2>/dev/null) || canonical_path="$path"
        else
            # Fallback: resolve relative paths and handle non-existent targets safely
            local dir base
            dir=$(dirname -- "$path")
            base=$(basename -- "$path")
            if [ -d "$dir" ]; then
                # Parent exists: resolve against its absolute path
                canonical_path="$(cd "$dir" 2>/dev/null && pwd)/$base"
            else
                # Parent does not exist: anchor relative paths to CWD, keep absolute as-is
                if [[ "$path" == /* ]]; then
                    canonical_path="$path"
                else
                    canonical_path="$(pwd)/$path"
                fi
            fi
        fi
        
        # Check against allow-list with canonicalized path
        for safe_dir in "${SAFE_DIRECTORIES[@]}"; do
            local canonical_safe
            if [[ "$safe_dir" == ./* ]]; then
                canonical_safe="$(pwd)/${safe_dir#./}"
            else
                canonical_safe="$safe_dir"
            fi
            
            # Canonicalize safe directory too
            if command -v realpath >/dev/null 2>&1; then
                local canonical_safe_tmp
                canonical_safe_tmp=$(realpath -m "$canonical_safe" 2>/dev/null) && canonical_safe="$canonical_safe_tmp"
            fi
            
            # Normalize safe directory (strip trailing slash) to avoid false matches like /tmp_backup for /tmp
            local safe_root="${canonical_safe%/}"
            if [[ "$canonical_path" == "$safe_root" ]] || [[ "$canonical_path" == "$safe_root/"* ]]; then
                return 0
            fi
        done
        echo "[SECURITY] Path not in allow-list for destructive operations: $path (canonical: $canonical_path)"
        return 1
    fi
    
    return 0
}

# Safe execution wrapper with permission validation
# NOTE: This wrapper does not support quoted paths with spaces (e.g., '/path/my file')
# Use paths without spaces or handle quoting at the caller level
safe_exec() {
    local cmd="$*"
    
    # Step 1: Check for dangerous patterns
    if is_dangerous_command "$cmd"; then
        echo "[SECURITY] Command blocked by pattern filter"
        return 1
    fi
    
    # Step 2: Extract paths and validate for destructive operations
    # Validate ALL non-flag paths, not just the last one
    # WARNING: Quoted arguments with spaces are not properly handled by read -ra
    # Callers should avoid passing paths with spaces to safe_exec
    # NOTE: Currently only 'rm' commands have path validation implemented.
    # Other destructive operations (chmod, chown, truncate, etc.) rely on pattern matching only.
    if [[ "$cmd" =~ rm[[:space:]] ]]; then
        # Parse arguments and validate all non-flag paths
        local -a args
        read -ra args <<< "$cmd"
        
        # Track if we found any paths to validate
        local found_path=false
        
        # Iterate over all arguments except the command name ("rm")
        for arg in "${args[@]:1}"; do
            # Skip flags (options) and '--' separator
            if [[ "$arg" =~ ^- ]] || [[ "$arg" == "--" ]]; then
                continue
            fi
            
            # Validate each non-flag argument as a potential target path
            found_path=true
            if ! is_path_allowed "$arg" "destructive"; then
                echo "[SECURITY] Command blocked by path validation"
                return 1
            fi
        done
        
        # If no paths found, the command is likely incomplete or invalid
        if [[ "$found_path" == false ]]; then
            echo "[SECURITY] No valid target paths found in rm command"
            return 1
        fi
    fi
    
    # Step 3: Log execution (for audit trail)
    echo "[EXEC] $(TZ=UTC date +%Y-%m-%dT%H:%M:%SZ) - Executing: $cmd"
    
    # Step 4: Execute with timeout protection (configurable via SAFE_EXEC_TIMEOUT)
    local timeout_seconds="${SAFE_EXEC_TIMEOUT:-600}"
    # Validate that timeout_seconds is a positive integer
    if ! [[ "$timeout_seconds" =~ ^[0-9]+$ ]] || [ "$timeout_seconds" -le 0 ]; then
        timeout_seconds=600
    fi
    
    # Execute without intermediate shell to prevent command injection
    # Parse command into array for safe execution
    local -a exec_args
    read -ra exec_args <<< "$cmd"
    
    if [ ${#exec_args[@]} -eq 0 ]; then
        echo "[SECURITY] Empty command, nothing to execute"
        return 1
    fi
    
    timeout "$timeout_seconds" "${exec_args[@]}"
    local exit_code=$?
    
    if [ $exit_code -eq 124 ]; then
        echo "[SECURITY] Command timed out after ${timeout_seconds} seconds"
        return 1
    fi
    
    return $exit_code
}
