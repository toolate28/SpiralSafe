#!/usr/bin/env bash
# Permission Execution-Layer Validation
# Prevents allow-list bypasses by validating at execution layer
# ATOM: ATOM-LIB-20260103-003-safe-exec-wrapper

# Dangerous command patterns that should be blocked
DANGEROUS_PATTERNS=(
    "rm -rf / "
    "rm -rf /"$
    " rm -rf ~"
    "rm -rf ~ "
    "rm -rf ~"$
    "rm[[:space:]]+-rf[[:space:]]+/[[:space:]]"
    "dd if=/dev/zero"
    "mkfs\."
    ":(){ :|:& };:"  # fork bomb
    "chmod -R 777 /"
    "chown -R"
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
    
    # Check for exact dangerous patterns
    if [[ "$cmd" =~ rm[[:space:]]+-rf[[:space:]]+/[[:space:]] ]] || \
       [[ "$cmd" =~ rm[[:space:]]+-rf[[:space:]]+/$ ]] || \
       [[ "$cmd" =~ rm[[:space:]]+-rf[[:space:]]+~[[:space:]] ]] || \
       [[ "$cmd" =~ rm[[:space:]]+-rf[[:space:]]+~$ ]] || \
       [[ "$cmd" == *"dd if=/dev/zero"* ]] || \
       [[ "$cmd" == *"mkfs."* ]] || \
       [[ "$cmd" == *":(){ :|:& };:"* ]] || \
       [[ "$cmd" == *"chmod -R 777 /"* ]]; then
        echo "[SECURITY] Dangerous pattern detected in: $cmd"
        return 0
    fi
    
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
                local abs_safe="$(pwd)/${safe_dir#./}"
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
    if [[ "$cmd" == *"rm "* ]] || [[ "$cmd" == *"dd "* ]]; then
        # Extract target path (simplified - real implementation would be more robust)
        local target_path
        if [[ "$cmd" =~ rm[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*(.+) ]]; then
            target_path="${BASH_REMATCH[2]}"
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
