# SpiralSafe Python Dependencies

**ATOM-INFRA-FIX-20260112-001**

This document describes the Python dependency structure for SpiralSafe.

## Overview

SpiralSafe uses a layered dependency structure to keep installations lean and support multiple use cases:

```
requirements.txt          # Core dependencies (always required)
├── requirements-ml.txt   # Optional: Heavy ML/quantum packages
└── requirements-dev.txt  # Optional: Development tools
```

## Installation Patterns

### For End Users (Core Functionality)

```bash
pip install -r requirements.txt
```

This installs only the essential dependencies needed for:
- ATOM trail streaming
- Hardware bridges (hologram, Tartarus)
- Configuration and environment management
- Basic documentation tools

**Size**: ~50-100MB

### For ML/Quantum Work (Optional)

```bash
pip install -r requirements.txt -r requirements-ml.txt
```

Adds support for:
- Image processing (Pillow, OpenCV)
- Scientific computing (NumPy, SciPy, Matplotlib)
- Network visualization (NetworkX)
- Mathematical animations (Manim)
- Machine learning (PyTorch - commented, see below)
- Quantum computing (Qiskit - commented)

**Size**: ~500MB-2GB depending on options

#### PyTorch CPU-Only Installation

For reduced size, install PyTorch CPU-only:

```bash
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

This avoids downloading CUDA libraries (~2GB reduction).

### For Developers (Testing & Code Quality)

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Adds development tools:
- pytest, pytest-asyncio, pytest-cov
- black, flake8, mypy, pylint
- Type stubs for common packages

**Size**: ~100-150MB

### For Complete Setup

```bash
pip install -r requirements.txt \
            -r requirements-ml.txt \
            -r requirements-dev.txt
```

## Module-Specific Requirements

Some modules have their own requirements that extend the core:

### Bridges (`bridges/`)

```bash
pip install -r requirements.txt -r bridges/requirements.txt
```

### Media Pipeline (`media/pipelines/`)

```bash
pip install -r requirements.txt -r media/pipelines/requirements.txt
```

### Integrations (`ops/integrations/*/`)

```bash
pip install -r requirements.txt \
            -r ops/integrations/openai-gpt/requirements.txt
```

## Version Pinning Strategy

All dependencies use exact version pinning (e.g., `==1.2.3`) for reproducibility:

- **Core dependencies**: Pinned to stable, tested versions
- **ML dependencies**: Pinned to latest stable at time of release
- **Dev dependencies**: Updated regularly for latest tools

### Updating Versions

To update all dependencies to latest compatible versions:

```bash
# Install pip-tools
pip install pip-tools

# Compile new pins (example)
pip-compile --upgrade requirements.in -o requirements.txt
```

## Validation

A validation script checks for common issues:

```bash
python3 scripts/verify-dependencies.py
```

This checks for:
- Duplicate package entries
- Standard library modules incorrectly listed
- Heavy packages in wrong files
- Unpinned versions (warnings)

## Platform-Specific Notes

### Windows

- Some packages may require Visual C++ Build Tools
- Install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Linux

- Some packages require system libraries:
  ```bash
  sudo apt install python3-dev libffi-dev libssl-dev
  ```

### macOS

- Usually works out-of-box with system Python or Homebrew Python

## CI/CD Integration

The CI pipeline (`spiralsafe-ci.yml`) validates dependencies:

1. **Lint job**: Runs `verify-dependencies.py` to catch issues early
2. **Build job**: Installs core dependencies with graceful fallback
3. **Python caching**: Uses `actions/setup-python@v5` with pip cache

## Lockfiles

**Status**: Python uses pinned versions in requirements.txt files.

**Future**: Consider adding `requirements.lock` or using `pip-tools` for dependency resolution tracking.

## Heavy Packages Reference

The following packages are considered "heavy" and should remain in `requirements-ml.txt`:

- **torch**: ~2GB (GPU), ~200MB (CPU-only)
- **tensorflow**: ~500MB-2GB
- **qiskit**: ~300-500MB
- **manim**: ~500MB (includes Cairo, LaTeX dependencies)
- **diffusers**: ~100-200MB

## FAQ

### Q: Why not use `poetry` or `pipenv`?

**A**: SpiralSafe prioritizes compatibility with standard pip workflows. Future versions may add optional Poetry support.

### Q: Can I use `pip install -e .` for development?

**A**: Yes! The repository includes a `setup.py` for bridges and ops packages.

### Q: What about conda?

**A**: Conda is not officially supported but should work. Use the requirements files as a guide.

### Q: Are there any dependencies that conflict?

**A**: All pinned versions are tested together. If you encounter conflicts, file an issue.

## Related Documentation

- [ops/CONTRIBUTION_ENV.md](ops/CONTRIBUTION_ENV.md) - Platform setup guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [ops/README.md](ops/README.md) - Operations API documentation

---

**Protocol**: H&&S:WAVE  
**Session**: ATOM-INFRA-FIX-20260112-001  
**Last Updated**: 2026-01-16
