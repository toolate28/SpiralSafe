#!/usr/bin/env bash
# Plugin Initialization Ordering
# Ensures LSP/MCP plugins initialize in correct dependency order
# ATOM: ATOM-LIB-20260103-002-plugin-init-ordering

# Plugin initialization state tracker
declare -A PLUGIN_INITIALIZED

# Define plugin dependency order (LSP must come before MCP)
PLUGIN_ORDER=(
    "environment"
    "lsp_server"
    "mcp_server"
    "workspace"
)

# Initialize plugin with dependency checking
plugin_init() {
    local plugin_name="$1"
    local plugin_init_func="$2"
    
    # Check if already initialized
    if [ "${PLUGIN_INITIALIZED[$plugin_name]:-0}" = "1" ]; then
        echo "[PLUGIN] $plugin_name already initialized, skipping"
        return 0
    fi
    
    # Check dependencies based on ordering
    local found_plugin=false
    for ordered_plugin in "${PLUGIN_ORDER[@]}"; do
        if [ "$ordered_plugin" = "$plugin_name" ]; then
            found_plugin=true
            break
        fi
        # All plugins before this one in order must be initialized
        if [ "${PLUGIN_INITIALIZED[$ordered_plugin]:-0}" != "1" ]; then
            echo "[ERROR] Plugin $plugin_name requires $ordered_plugin to be initialized first"
            return 1
        fi
    done
    
    # Run initialization function
    echo "[PLUGIN] Initializing $plugin_name..."
    if $plugin_init_func; then
        PLUGIN_INITIALIZED[$plugin_name]=1
        echo "[PLUGIN] $plugin_name initialized successfully"
        return 0
    else
        echo "[ERROR] Failed to initialize $plugin_name"
        return 1
    fi
}

# Initialize all plugins in correct order
plugin_init_all() {
    for plugin in "${PLUGIN_ORDER[@]}"; do
        local init_func="init_${plugin}"
        if declare -f "$init_func" >/dev/null; then
            plugin_init "$plugin" "$init_func" || return 1
        fi
    done
}
