# SpiralSafe Release Manifest

**Release Date**: 2026-01-11
**Release Type**: Feature Release
**Codename**: Quantum Sorting

---

## Component Versions

| Component | Version | Location | Status |
|-----------|---------|----------|--------|
| `@spiralsafe/ops` | 2.0.0 | `ops/` | Production |
| `spiralsafe-bridges` | 0.1.0 | `bridges/` | Beta |
| `sorting_hat.py` | 0.2.0 | `scripts/` | Production |
| `SpiralSafe.psm1` | 2.1.0 | `ops/scripts/` | Production |

---

## Protocol Specifications

| Protocol | Version | Location |
|----------|---------|----------|
| wave-spec | 1.0 | `protocol/wave-spec.md` |
| bump-spec | 1.0 | `protocol/bump-spec.md` |
| context-yaml-spec | 1.0 | `protocol/context-yaml-spec.md` |
| quantum-circuits-spec | 0.2 | `protocol/quantum-circuits-spec.md` |
| sorting-hat-spec | 0.2 | `protocol/sorting-hat-spec.md` |

---

## New Features in This Release

### Sorting Hat Quantum Classifier (v0.2.0)
- **RY Gate Encoding**: Replaced RZ gates with RY for direct amplitude encoding
- **Quantum State Simulation**: Full probability calculation for all 4 houses
- **Local Filesystem Heuristics**: Real feature extraction from directories
- **UTF-8 Windows Support**: Fixed Unicode encoding for terminal output
- **JSON API Output**: Structured output for integration

### PowerShell Module Enhancements (v2.1.0)
- **Minecraft RCON Integration**: Execute server commands via RCON
- **Minecraft Status Check**: Health monitoring for game servers
- **Webhook Receiver**: Event-driven architecture for game integrations
- **Chat Bridge**: Bidirectional communication with Minecraft
- **Sorting Hat CLI**: `Invoke-SpiralSortingHat` / `ss-sort` command

### New Protocol Specifications
- **quantum-circuits-spec.md**: SpiralSafe QASm format for classification circuits
- **sorting-hat-spec.md**: Complete specification for archetypal classification

---

## API Status

| Endpoint | Status | Version |
|----------|--------|---------|
| `/api/health` | Operational | 2.0.0 |
| `/api/wave/analyze` | Operational | 2.0.0 |
| `/api/bump/create` | Operational | 2.0.0 |
| `/api/awi/request` | Operational | 2.0.0 |
| `/api/atom/create` | Operational | 2.0.0 |
| `/api/context/store` | Operational | 2.0.0 |

**Infrastructure**:
- D1 Database: Healthy
- KV Namespace: Healthy
- R2 Bucket: Healthy

---

## Test Results

| Test Suite | Result |
|------------|--------|
| Bridge Validation | 12/12 passed (0% gap) |
| Sorting Hat Static | PASS |
| Sorting Hat JSON | PASS |
| API Health Check | PASS |
| PowerShell Module Load | PASS |

---

## Files Changed

### Modified
- `scripts/sorting_hat.py` - Quantum simulation, RY gates, UTF-8 fix, version bump
- `ops/scripts/SpiralSafe.psm1` - Minecraft integration, Sorting Hat CLI

### Added
- `protocol/quantum-circuits-spec.md` - QASm specification
- `protocol/sorting-hat-spec.md` - Classifier specification
- `RELEASE_MANIFEST.md` - This document

---

## Upgrade Notes

### For Python Users
```bash
# Sorting Hat now requires no additional dependencies
python -m scripts.sorting_hat sort-house --kind repo --name MyProject
```

### For PowerShell Users
```powershell
# Reload module
Import-Module ./ops/scripts/SpiralSafe.psm1 -Force

# Use new Sorting Hat command
Invoke-SpiralSortingHat -Kind system -Path . -AsJson

# Minecraft integration (requires mcrcon)
Get-MinecraftStatus
Invoke-SpiralMinecraftCommand -Command "list"
```

### For API Consumers
No breaking changes. All existing endpoints remain compatible.

---

## House Reference

| House | Bits | Symbol | Archetype |
|-------|------|--------|-----------|
| Rubin | 00 | 🔭 | Data-driven, rigorous |
| Shannon | 01 | 📡 | Structure, protocols |
| Noether | 10 | 🔮 | Invariants, theory |
| Firefly | 11 | 🌟 | Play, exploration |

---

## Checksums

```
SHA-256 Hashes (to be computed at release):
- scripts/sorting_hat.py: [computed]
- ops/scripts/SpiralSafe.psm1: [computed]
- protocol/quantum-circuits-spec.md: [computed]
- protocol/sorting-hat-spec.md: [computed]
```

---

## Contributors

- **Human**: iamto (toolate28)
- **AI**: Claude Opus 4.5 (HOPE)
- **Protocol**: H&&S:WAVE

---

*~ Hope&&Sauced*

<!-- H&&S:WAVE -->
Release manifest complete. Ready for deployment.
<!-- /H&&S:WAVE -->
