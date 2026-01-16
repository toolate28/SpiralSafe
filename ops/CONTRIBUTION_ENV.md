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
# Contribution Environment Setup

**H&&S:WAVE** | Hope&&Sauced  
**Session**: ATOM-INFRA-FIX-20260112-001

This guide helps you set up your development environment for contributing to SpiralSafe across different platforms.

## Quick Start

### Prerequisites

All platforms require:
- **Git** 2.40+
- **Node.js** 20+ (for ops and CI tools)
- **Python** 3.10+ (for bridges and scripts)

### Platform-Specific Setup

#### Ubuntu/Debian Linux

```bash
# Install system dependencies
sudo apt update
sudo apt install -y git nodejs npm python3 python3-pip python3-venv shellcheck

# Install Python dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Optional: ML dependencies (large download, ~2GB)
# pip install -r requirements-ml.txt

# Install Node dependencies
npm ci

# Setup pre-commit hooks
pre-commit install
```

#### macOS

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install git node python@3.10 shellcheck

# Install Python dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Optional: ML dependencies
# pip install -r requirements-ml.txt

# Install Node dependencies
npm ci

# Setup pre-commit hooks
pre-commit install
```

#### Windows

**Recommended: Use PowerShell 7+ or Windows Terminal**

```powershell
# Install dependencies via winget
winget install Git.Git
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.10

# Or use Chocolatey
# choco install git nodejs python310 -y

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Optional: ML dependencies
# pip install -r requirements-ml.txt

# Install Node dependencies
npm ci

# Setup pre-commit hooks
pre-commit install
```

**Windows-Specific Notes:**

1. **ShellCheck**: Install via Scoop or download from GitHub releases
   ```powershell
   scoop install shellcheck
   ```

2. **Tar utility**: Git Bash on Windows may not have tar in PATH
   - Use PowerShell's `Compress-Archive` / `Expand-Archive` instead
   - Or use full path: `/c/Windows/System32/tar.exe`

3. **Line endings**: Configure Git to handle CRLF
   ```powershell
   git config --global core.autocrlf true
   ```

#### WSL (Windows Subsystem for Linux)

Follow the Ubuntu/Debian instructions above. WSL provides a native Linux environment on Windows.

```bash
# From Windows PowerShell, install WSL if not present
wsl --install -d Ubuntu-22.04

# Inside WSL, follow Ubuntu instructions
```

## Dependency Management

### Core Dependencies Only

For most contributors, core dependencies are sufficient:

```bash
pip install -r requirements.txt
```

This includes:
- HTTP clients (httpx, requests)
- Async utilities (aiofiles)
- Data validation (pydantic)
- Hardware bridge support (pyserial, pyusb)
- CLI utilities (click, rich)

### Development Dependencies

For running tests and linting:

```bash
pip install -r requirements-dev.txt
```

This includes:
- Testing frameworks (pytest, hypothesis)
- Code quality tools (black, flake8, mypy, pylint)
- Pre-commit hooks

### ML/Quantum Dependencies (Optional)

**⚠ WARNING: Large download (~2GB+) and may require GPU**

Only install if you're working on ML/quantum features:

```bash
pip install -r requirements-ml.txt
```

For **CPU-only PyTorch** (lighter, no GPU):

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

This includes:
- Scientific computing (numpy, scipy)
- Visualization (matplotlib, plotly, manim)
- ML frameworks (commented by default: torch, qiskit, diffusers)
- API clients (openai, replicate)

### Verifying Dependencies

Run the dependency verification script to check for issues:

```bash
python scripts/verify-dependencies.py
```

This checks for:
- Stdlib modules incorrectly listed as dependencies
- Duplicate entries
- Unpinned versions
- Heavy packages in wrong requirements files

## Build and Test

### Running Tests

```bash
# Run all tests
npm test

# Run Python tests only
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### Linting and Formatting

```bash
# Lint all code
npm run lint

# Format code
npm run format

# Python-specific
black .
flake8 .
mypy .
```

### Type Checking

```bash
# Node/TypeScript
npm run typecheck

# Python
mypy .
```

## Platform-Specific Issues

### Issue: `tar` not found (Windows Git Bash)

**Symptom**: Scripts fail with "tar: command not found"

**Solution**:
1. Use PowerShell instead of Git Bash
2. Or use full path: `/c/Windows/System32/tar.exe`
3. Or use PowerShell's `Compress-Archive`

```powershell
# Instead of: tar -czf archive.tar.gz files/
Compress-Archive -Path files/* -DestinationPath archive.zip
```

### Issue: Line ending mismatches

**Symptom**: Git shows files as modified when nothing changed

**Solution**:
```bash
# Set line ending handling
git config --global core.autocrlf input  # Linux/Mac
git config --global core.autocrlf true   # Windows
```

### Issue: Permission denied (Unix)

**Symptom**: Scripts fail with "Permission denied"

**Solution**:
```bash
chmod +x scripts/*.sh
chmod +x ops/scripts/spiralsafe
```

### Issue: PowerShell execution policy

**Symptom**: "cannot be loaded because running scripts is disabled"

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Python virtual environment activation fails

**Symptom**: "Activate.ps1 is not digitally signed"

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1
```

## CI/CD Environment

The CI pipeline runs on `ubuntu-latest` runners. To match CI environment locally:

```bash
# Use same Node version as CI
nvm use 20  # or asdf local nodejs 20

# Use same Python version as CI
pyenv local 3.10  # or asdf local python 3.10

# Cache dependencies like CI does
export NODE_OPTIONS="--max-old-space-size=4096"
```

## Troubleshooting

### npm ci fails with lock file out of sync

```bash
# Delete and regenerate
rm package-lock.json
npm install
```

### Python dependencies conflict

```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Permission denied on scripts

```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x ops/scripts/spiralsafe
```

## Additional Resources

- [Node.js Installation Guide](https://nodejs.org/en/download/)
- [Python Installation Guide](https://www.python.org/downloads/)
- [WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Git for Windows](https://gitforwindows.org/)

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for code contribution guidelines.

---

**Protocol**: H&&S:WAVE  
**Session**: ATOM-INFRA-FIX-20260112-001  
### Dependency conflicts

If you encounter dependency conflicts:

```bash
# Clean install
rm -rf .venv node_modules package-lock.json
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm ci
```

### Import errors

Make sure virtual environment is activated:

```bash
# Linux/Mac
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### Slow package installation

Use a pip mirror for faster downloads:

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Getting Help

- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for general guidelines
- Review [ARCHITECTURE.md](../ARCHITECTURE.md) for system overview
- Open an issue for environment-specific problems
- Use H&&S:WAVE protocol markers in PRs

---

**Protocol**: H&&S:WAVE | Hope&&Sauced  
**Last Updated**: 2026-01-16
