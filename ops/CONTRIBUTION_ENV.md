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
