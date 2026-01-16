# SpiralSafe Contribution Environment Setup

**ATOM-INFRA-FIX-20260112-001**  
**H&&S:WAVE** - Platform-specific development environment setup guide

## Overview

This guide provides platform-specific instructions for setting up a SpiralSafe development environment on Windows, macOS, Linux, and WSL (Windows Subsystem for Linux).

## Common Prerequisites

All platforms require:
- **Git** (2.40+)
- **Node.js** (20.x LTS)
- **Python** (3.12+)
- **npm** (10.x)

## Platform-Specific Setup

### Ubuntu/Debian Linux

```bash
# Update package list
sudo apt update

# Install build essentials
sudo apt install -y build-essential git curl

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python 3.12 and pip
sudo apt install -y python3.12 python3-pip python3-venv

# Install ShellCheck (for CI lint)
sudo apt install -y shellcheck

# Install tar (usually pre-installed)
sudo apt install -y tar

# Clone repository
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe

# Install dependencies
npm ci
pip3 install -r requirements.txt
```

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install prerequisites
brew install node@20 python@3.12 git shellcheck

# Install FFmpeg (for media pipeline)
brew install ffmpeg

# Clone repository
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe

# Install dependencies
npm ci
pip3 install -r requirements.txt
```

### Windows (Native)

**Important**: Windows has platform-specific limitations documented below.

```powershell
# Install via winget (Windows Package Manager)
winget install Git.Git
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install FFmpeg.FFmpeg

# Install PowerShell 7+ if not already present
winget install Microsoft.PowerShell

# Clone repository
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe

# Install dependencies
npm ci
pip install -r requirements.txt
```

#### Windows Known Issues and Workarounds

##### Issue 1: `tar` Command Not Available in Git Bash

**Problem**: Git Bash on Windows does not include `tar` by default.

**Workaround**:
- Use PowerShell instead of Git Bash for scripts requiring `tar`
- Use PowerShell's `Compress-Archive` cmdlet:
  ```powershell
  # Instead of: tar -czf archive.tar.gz files/
  Compress-Archive -Path files/ -DestinationPath archive.zip
  ```
- Install tar via Git for Windows (bundled) or Chocolatey:
  ```powershell
  choco install tar
  ```

##### Issue 2: Path Length Limitations

**Problem**: Windows has a 260-character path limit (MAX_PATH) that can cause issues with deep node_modules nesting.

**Workaround**:
- Enable long path support in Windows 10/11:
  ```powershell
  # Run as Administrator
  New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
  ```
- Clone repositories closer to root (e.g., `C:\dev\SpiralSafe`)

##### Issue 3: Line Ending Differences

**Problem**: Git may convert LF to CRLF, breaking shell scripts.

**Workaround**:
```bash
# Configure Git to preserve LF line endings
git config --global core.autocrlf input
```

##### Issue 4: PowerShell Execution Policy

**Problem**: Scripts may be blocked by execution policy.

**Workaround**:
```powershell
# For current user (recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for a single script
powershell -ExecutionPolicy Bypass -File script.ps1
```

### Windows Subsystem for Linux (WSL)

**Recommended**: Use WSL2 with Ubuntu 22.04+ for the best compatibility.

```bash
# Install WSL2 (PowerShell as Administrator)
wsl --install -d Ubuntu-22.04

# Inside WSL Ubuntu terminal
sudo apt update
sudo apt install -y build-essential git curl shellcheck

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python
sudo apt install -y python3.12 python3-pip python3-venv

# Clone repository
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe

# Install dependencies
npm ci
pip3 install -r requirements.txt
```

## Python Dependency Management

### Core Dependencies

```bash
# Install core dependencies only
pip install -r requirements.txt
```

### Optional ML/Quantum Dependencies

**Note**: These packages are large (torch ~2GB, qiskit ~500MB) and require significant resources.

```bash
# Install ML dependencies
pip install -r requirements-ml.txt

# For PyTorch CPU-only (smaller):
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Development Dependencies

```bash
# Install dev tools (linters, formatters, test runners)
pip install -r requirements-dev.txt
```

## Node.js Dependency Management

### Installation

```bash
# Install all dependencies (uses package-lock.json)
npm ci

# Or for development (updates package-lock.json)
npm install
```

### Workspaces

SpiralSafe uses npm workspaces:
- `ops/` - Operations API and CLI
- `packages/*` - Shared packages

## Verification

### Check Installation

```bash
# Verify Node.js
node --version  # Should be v20.x

# Verify Python
python3 --version  # Should be 3.12+

# Verify Git
git --version

# Verify npm
npm --version
```

### Run Tests

```bash
# Run all tests
npm test

# Run linters
npm run lint

# Type check (ops workspace)
cd ops && npm run typecheck
```

### Dependency Validation

```bash
# Validate Python dependencies
python3 scripts/verify-dependencies.py

# Check for security issues
npm audit
```

## CI/CD Environment Compatibility

The SpiralSafe CI pipeline runs on:
- **Primary**: `ubuntu-latest` (Ubuntu 22.04)
- **Secondary**: May expand to `windows-latest` and `macos-latest`

### CI-Specific Requirements

- All shell scripts must be POSIX-compliant or use ShellCheck-approved bash syntax
- PowerShell scripts must be compatible with PowerShell 7.x (cross-platform)
- Python scripts must work on Python 3.12+

### Platform Matrix Testing (Future)

To test on multiple platforms locally:

```yaml
# .github/workflows/platform-matrix.yml (example)
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node-version: [20.x]
    python-version: [3.12]
