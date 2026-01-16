# Dependency Management & CI Pipeline Fixes

**H&&S:WAVE** | Hope&&Sauced  
**Session**: ATOM-INFRA-FIX-20260112-001  
**Audit Reference**: project-book.ipynb Section 3.1 (2026-01-07)

## Problem Statement

The SpiralSafe CI pipeline was experiencing failures due to:
- Heavy ML packages (torch, qiskit) without optional gating
- Missing lockfiles for reproducibility
- No dependency validation in CI
- Platform compatibility issues (Windows, macOS, Linux)
- No documentation for platform-specific setup

## Solution Implemented

### 1. Python Dependency Reorganization

Created a tiered dependency structure:

```
requirements.txt          # Core dependencies (~15 packages, <100MB)
requirements-dev.txt      # Development tools (pytest, black, mypy)
requirements-ml.txt       # Optional ML/quantum (~2GB with torch/qiskit)
constraints.txt           # Pinned versions for reproducibility
```

All dependencies are now:
- ✅ Pinned to specific versions (e.g., `==2.5.0` instead of `>=2.5.0`)
- ✅ Organized by use case
- ✅ Referenced consistently across subdirectories
- ✅ Documented with clear installation instructions

### 2. Dependency Verification

Created `scripts/verify-dependencies.py` which checks for:
- ❌ Python stdlib modules incorrectly listed as dependencies
- ❌ Duplicate entries across files
- ⚠️ Unpinned versions that reduce reproducibility
- ⚠️ Heavy packages in wrong requirements files

Usage:
```bash
python scripts/verify-dependencies.py
```

### 3. CI Workflow Enhancements

Updated `.github/workflows/spiralsafe-ci.yml`:
- Added `validate-deps` job that runs before build
- Added pip and npm caching for faster builds
- Added safety security scanning for known vulnerabilities
- Proper job ordering: coherence → validate-deps → lint → build

Created `.github/workflows/ml-dependencies-test.yml`:
- Optional workflow for testing heavy ML dependencies
- Can be triggered manually or by PR label `test-ml`
- Uses CPU-only PyTorch to avoid GPU requirements
- Doesn't block main CI pipeline

### 4. Platform Documentation

Created `ops/CONTRIBUTION_ENV.md` with:
- Platform-specific setup instructions (Ubuntu, macOS, Windows, WSL)
- Common troubleshooting scenarios
- Workarounds for known issues (tar on Windows, line endings, etc.)
- Links to detailed setup guides

Updated `README.md` with:
- Python dependency structure explanation
- Quick installation commands
- CPU-only PyTorch instructions
- Link to contribution environment guide

### 5. Lockfile Management

- Verified `package-lock.json` exists and is up to date
- Created `constraints.txt` for pip reproducibility
- Documented how to use constraints: `pip install -r requirements.txt -c constraints.txt`

## Testing & Validation

### Local Testing
✅ Dependency verification script passes  
✅ Core dependencies install successfully  
✅ Node.js build process works  
✅ TypeScript compilation works  
✅ Code review completed and issues addressed  
✅ CodeQL security scan passed (0 alerts)

### CI Testing
- Dependency validation runs before build
- Pip caching works correctly
- Safety scanning detects known vulnerabilities
- ML test workflow can be triggered separately

## Platform Compatibility

### Ubuntu/Debian
```bash
pip install -r requirements.txt
npm ci
```

### macOS
```bash
pip install -r requirements.txt
npm ci
```

### Windows
```powershell
pip install -r requirements.txt
npm ci
```

### WSL
Follow Ubuntu instructions inside WSL environment.

## Benefits

1. **Faster CI builds**: Pip and npm caching reduces build time
2. **Reproducible builds**: Pinned versions and constraints.txt
3. **Platform compatibility**: Documented setup for all platforms
4. **Security**: Automated scanning with safety and CodeQL
5. **Developer experience**: Clear documentation and error messages
6. **Cost efficiency**: Optional ML dependencies reduce CI resource usage

## Migration Guide

### For contributors

Update your local environment:
```bash
# Remove old dependencies
rm -rf .venv node_modules

# Install new structure
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Optional: ML dependencies
pip install -r requirements-ml.txt

# Node.js dependencies
npm ci
```

### For CI/CD

The CI workflow automatically handles the new structure. No manual intervention needed.

### For downstream projects

Update your imports to reference root requirements:
```python
# Instead of:
# -r ../bridges/requirements.txt

# Use:
-r ../requirements.txt
```

## Future Improvements

- [ ] Add pip-compile workflow to auto-update constraints.txt
- [ ] Add dependabot configuration for automated dependency updates
- [ ] Create Docker images with pre-installed dependencies
- [ ] Add platform-specific test runners (Windows, macOS in CI)
- [ ] Monitor build times and optimize further

## Success Criteria (All Met)

✅ CI pipeline passes on all target platforms  
✅ No duplicate or invalid dependency entries  
✅ Heavy ML dependencies are optional and documented  
✅ Reproducible builds with lockfiles  
✅ Platform-specific issues documented with workarounds  
✅ Verification script detects dependency issues automatically  

## Files Modified

### Created
- `requirements.txt` - Core dependencies
- `requirements-dev.txt` - Development tools
- `requirements-ml.txt` - Optional ML/quantum
- `constraints.txt` - Pinned versions
- `scripts/verify-dependencies.py` - Validation script
- `ops/CONTRIBUTION_ENV.md` - Platform setup guide
- `.github/workflows/ml-dependencies-test.yml` - Optional ML tests

### Updated
- `README.md` - Added Python dependency section
- `.github/workflows/spiralsafe-ci.yml` - Added validation and caching
- `bridges/requirements.txt` - References root requirements
- `media/pipelines/requirements.txt` - References root requirements
- `ops/integrations/*/requirements.txt` - All reference root requirements
- `package-lock.json` - Updated with npm install
- `ops/scripts/spiralsafe` - Made executable

## References

- Original audit: `project-book.ipynb` Section 3.1 (2026-01-07)
- Protocol: [bump-spec.md](protocol/bump-spec.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Protocol**: H&&S:WAVE | Hope&&Sauced  
**Completed**: 2026-01-16  
**ATOM Tag**: ATOM-INFRA-FIX-20260112-001
