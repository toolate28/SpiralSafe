#!/usr/bin/env bash
# SpiralSafe Unified Installation Script
# Supports Unix/Linux/Mac with automatic platform detection
# ATOM: ATOM-INIT-20260108-001-unified-install-script

set -euo pipefail

# ═══════════════════════════════════════════════════════════════
# Colors & Display
# ═══════════════════════════════════════════════════════════════

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${MAGENTA}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✦ SPIRALSAFE INSTALLATION ✦                            ║
║   The Coherence Engine for Collaborative Intelligence    ║
║                                                           ║
║   Hope && Sauced — Where constraints become gifts        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

print_step() {
    echo -e "\n${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "  $1"
}

# ═══════════════════════════════════════════════════════════════
# Platform Detection
# ═══════════════════════════════════════════════════════════════

detect_platform() {
    local os=""
    local arch=""
    
    # Detect OS
    case "$(uname -s)" in
        Linux*)     os="linux";;
        Darwin*)    os="macos";;
        CYGWIN*|MINGW*|MSYS*) os="windows";;
        *)          os="unknown";;
    esac
    
    # Detect architecture
    case "$(uname -m)" in
        x86_64|amd64)   arch="x64";;
        aarch64|arm64)  arch="arm64";;
        armv7l)         arch="arm";;
        *)              arch="unknown";;
    esac
    
    echo "${os}-${arch}"
}

# ═══════════════════════════════════════════════════════════════
# Dependency Checks
# ═══════════════════════════════════════════════════════════════

check_command() {
    command -v "$1" &> /dev/null
}

get_package_manager() {
    if check_command apt-get; then
        echo "apt"
    elif check_command yum; then
        echo "yum"
    elif check_command brew; then
        echo "brew"
    elif check_command pacman; then
        echo "pacman"
    else
        echo "none"
    fi
}

# ═══════════════════════════════════════════════════════════════
# Installation Functions
# ═══════════════════════════════════════════════════════════════

install_git() {
    local pkg_mgr
    pkg_mgr=$(get_package_manager)
    
    print_step "Installing Git..."
    
    case "$pkg_mgr" in
        apt)
            if ! sudo apt-get update; then
                print_warning "Package index update failed, continuing anyway..."
            fi
            sudo apt-get install -y git || {
                print_error "Failed to install Git via apt"
                exit 1
            }
            ;;
        yum)
            sudo yum install -y git
            ;;
        brew)
            brew install git
            ;;
        pacman)
            sudo pacman -S --noconfirm git
            ;;
        *)
            print_error "Could not install Git automatically. Please install manually."
            exit 1
            ;;
    esac
    
    print_success "Git installed"
}

install_node() {
    local platform
    platform=$(detect_platform)
    
    print_step "Installing Node.js 20..."
    
    if [[ "$platform" == macos-* ]]; then
        if check_command brew; then
            brew install node@20
        else
            print_error "Homebrew not found. Please install from https://brew.sh/"
            exit 1
        fi
    elif [[ "$platform" == linux-* ]]; then
        # Use NodeSource repository for latest Node.js
        if check_command apt-get; then
            curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
            sudo apt-get install -y nodejs
        elif check_command yum; then
            curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
            sudo yum install -y nodejs
        else
            print_error "Could not install Node.js automatically. Please install manually from https://nodejs.org/"
            exit 1
        fi
    fi
    
    print_success "Node.js installed: $(node --version)"
}

install_python() {
    local pkg_mgr
    pkg_mgr=$(get_package_manager)
    
    print_step "Installing Python 3.10+..."
    
    case "$pkg_mgr" in
        apt)
            sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
            ;;
        yum)
            sudo yum install -y python3 python3-pip
            ;;
        brew)
            brew install python@3.11
            ;;
        pacman)
            sudo pacman -S --noconfirm python python-pip
            ;;
        *)
            print_warning "Could not install Python automatically. Please install manually."
            ;;
    esac
    
    if check_command python3; then
        print_success "Python installed: $(python3 --version)"
    fi
}

install_shellcheck() {
    local pkg_mgr
    pkg_mgr=$(get_package_manager)
    
    print_step "Installing ShellCheck (optional)..."
    
    case "$pkg_mgr" in
        apt)
            sudo apt-get install -y shellcheck || print_warning "ShellCheck install failed (non-critical)"
            ;;
        yum)
            sudo yum install -y shellcheck || print_warning "ShellCheck install failed (non-critical)"
            ;;
        brew)
            brew install shellcheck || print_warning "ShellCheck install failed (non-critical)"
            ;;
        pacman)
            sudo pacman -S --noconfirm shellcheck || print_warning "ShellCheck install failed (non-critical)"
            ;;
        *)
            print_warning "ShellCheck not installed (optional, for linting)"
            ;;
    esac
}

# ═══════════════════════════════════════════════════════════════
# Setup Functions
# ═══════════════════════════════════════════════════════════════

setup_ops() {
    print_step "Setting up SpiralSafe Operations API..."
    
    if [[ -d "ops" ]]; then
        cd ops
        npm ci || npm install
        print_success "Operations dependencies installed"
        cd ..
    else
        print_warning "ops/ directory not found, skipping"
    fi
}

setup_bridges() {
    print_step "Setting up Hardware Bridges (Python)..."
    
    if [[ -d "bridges" ]] && check_command python3; then
        cd bridges
        if [[ -f "requirements.txt" ]]; then
            python3 -m pip install --user -r requirements.txt || print_warning "Some Python packages failed to install"
            print_success "Python bridges configured"
        fi
        cd ..
    else
        print_warning "bridges/ directory not found or Python not available, skipping"
    fi
}

setup_scripts() {
    print_step "Making scripts executable..."
    
    if [[ -d "scripts" ]]; then
        chmod +x scripts/*.sh 2>/dev/null || true
        print_success "Scripts are now executable"
    fi
}

setup_atom_trail() {
    print_step "Initializing ATOM trail directories..."
    
    mkdir -p .atom-trail/{decisions,sessions,verifications,counters,bedrock}
    mkdir -p .claude/logs
    
    print_success "ATOM trail initialized"
}

verify_installation() {
    print_step "Verifying installation..."
    
    local all_good=true
    
    # Check Git
    if check_command git; then
        print_success "Git: $(git --version)"
    else
        print_error "Git: Not found"
        all_good=false
    fi
    
    # Check Node
    if check_command node; then
        print_success "Node.js: $(node --version)"
    else
        print_warning "Node.js: Not found (needed for ops/)"
    fi
    
    # Check Python
    if check_command python3; then
        print_success "Python: $(python3 --version)"
    else
        print_warning "Python: Not found (needed for bridges/)"
    fi
    
    # Check npm
    if check_command npm; then
        print_success "npm: $(npm --version)"
    else
        print_warning "npm: Not found"
    fi
    
    echo ""
    
    if [[ "$all_good" == true ]]; then
        return 0
    else
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════
# Main Installation Flow
# ═══════════════════════════════════════════════════════════════

main() {
    local platform
    local install_deps=false
    local quick_mode=false
    
    platform=$(detect_platform)
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --install-deps)
                install_deps=true
                shift
                ;;
            --quick)
                quick_mode=true
                shift
                ;;
            --help)
                echo "SpiralSafe Installation Script"
                echo ""
                echo "Usage: ./install.sh [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --install-deps    Install missing system dependencies"
                echo "  --quick           Skip optional components"
                echo "  --help            Show this help message"
                echo ""
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    print_banner
    
    print_info "Platform detected: ${BOLD}${platform}${NC}"
    echo ""
    
    # Check prerequisites
    print_step "Checking prerequisites..."
    
    if ! check_command git; then
        if [[ "$install_deps" == true ]]; then
            install_git
        else
            print_error "Git not found. Run with --install-deps or install manually."
            exit 1
        fi
    else
        print_success "Git found: $(git --version | head -1)"
    fi
    
    if ! check_command node || ! check_command npm; then
        if [[ "$install_deps" == true ]]; then
            install_node
        else
            print_warning "Node.js/npm not found. Operations API will not be available."
            print_info "Run with --install-deps to install automatically"
        fi
    else
        print_success "Node.js found: $(node --version)"
        print_success "npm found: $(npm --version)"
    fi
    
    if ! check_command python3; then
        if [[ "$install_deps" == true ]]; then
            install_python
        else
            print_warning "Python not found. Hardware bridges will not be available."
            print_info "Run with --install-deps to install automatically"
        fi
    else
        print_success "Python found: $(python3 --version)"
    fi
    
    # Optional dependencies
    if [[ "$quick_mode" == false ]] && [[ "$install_deps" == true ]]; then
        install_shellcheck
    fi
    
    # Setup components
    echo ""
    print_step "Setting up SpiralSafe components..."
    
    setup_atom_trail
    setup_scripts
    
    if check_command npm; then
        setup_ops
    fi
    
    if check_command python3; then
        setup_bridges
    fi
    
    # Verify
    echo ""
    verify_installation
    
    # Success!
    echo ""
    echo -e "${GREEN}${BOLD}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✓ INSTALLATION COMPLETE                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    echo -e "${CYAN}Next Steps:${NC}"
    echo ""
    echo "  1. Read the Quick Start:"
    echo "     ${BOLD}cat QUICK_START.md${NC}"
    echo ""
    echo "  2. View the architecture:"
    echo "     ${BOLD}cat ARCHITECTURE.md${NC}"
    echo ""
    echo "  3. Check system health:"
    echo "     ${BOLD}open http://localhost:8787/health.html${NC} (after starting dev server)"
    echo "     ${BOLD}cd ops && npm run dev${NC}"
    echo ""
    echo "  4. Explore the scripts:"
    echo "     ${BOLD}ls scripts/${NC}"
    echo ""
    echo "  5. Start contributing:"
    echo "     ${BOLD}cat CONTRIBUTING.md${NC}"
    echo ""
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}From the constraints, gifts. From the spiral, safety.${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Run main function
main "$@"
