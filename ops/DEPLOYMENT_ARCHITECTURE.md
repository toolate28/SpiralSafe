# SpiralSafe Deployment Architecture

> **H&&S:WAVE** | Hope&&Sauced
> Multi-Architecture Pipeline Integration

---

## Architecture Matrix

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                     SPIRALSAFE DEPLOYMENT ARCHITECTURE                           ║
║                                                                                  ║
║  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        ║
║  │    AI        │  │    OS        │  │   SHELL      │  │    IDE       │        ║
║  │  PLATFORMS   │  │  TARGETS     │  │ ENVIRONMENTS │  │ INTEGRATIONS │        ║
║  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘        ║
║        │                 │                 │                 │                  ║
║        └─────────────────┴─────────────────┴─────────────────┘                  ║
║                                    │                                            ║
║                                    ▼                                            ║
║                        ┌─────────────────────┐                                  ║
║                        │  UNIFIED PIPELINE   │                                  ║
║                        │   H&&S:WAVE SIGNED  │                                  ║
║                        └─────────────────────┘                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. AI Platform Integration

| Platform | Integration Method | Status | Notes |
|----------|-------------------|--------|-------|
| **Claude Code** | Native CLI + SDK | ✓ Primary | Direct Opus 4.5 integration |
| **GitHub Copilot** | Extensions + Chat | ✓ Ready | Verification via H&&S markers |
| **OpenAI GPT** | API + Assistants | ○ Planned | Tool calling support |
| **Gemini** | Vertex AI + Extensions | ○ Planned | Google Cloud integration |
| **Grok** | X API (future) | ◐ Research | Real-time context potential |
| **Groq** | High-speed inference | ○ Planned | Low-latency operations |

### AI Context Handoff Protocol

```yaml
# context.yaml - AI Platform Interchange
spiralsafe:
  protocol: "H&&S:WAVE"
  version: "1.0"
  handoff:
    from_platform: "claude-code"
    to_platform: "github-copilot"
    context_hash: "sha256:..."
    verified: true
```

---

## 2. Operating System Targets

### Build Matrix

| OS | Version | Shell | Package Manager | Crypto Backend |
|----|---------|-------|-----------------|----------------|
| **Windows** | 10/11 | PowerShell 7+ | winget/scoop | DPAPI/CNG |
| **macOS** | 12+ | zsh/bash | Homebrew | Keychain/SecureEnclave |
| **Linux (Ubuntu)** | 22.04+ | bash/zsh | apt | GPG/libsodium |
| **Linux (RHEL)** | 8+ | bash | dnf | GPG/OpenSSL |
| **Linux (Alpine)** | 3.18+ | ash/bash | apk | LibreSSL |

### OS-Specific Deployment Scripts

```powershell
# Windows deployment
./ops/scripts/deploy-windows.ps1

# macOS deployment
./ops/scripts/deploy-macos.sh

# Linux deployment
./ops/scripts/deploy-linux.sh

# Container deployment (any OS)
docker compose -f ops/docker-compose.yml up -d
```

---

## 3. Shell Environment Matrix

| Shell | Config File | Activation | Notes |
|-------|------------|------------|-------|
| **PowerShell 7** | `$PROFILE` | `Import-Module SpiralSafe` | Windows primary |
| **PowerShell 5.1** | `$PROFILE` | `Import-Module SpiralSafe` | Windows legacy |
| **Bash** | `.bashrc` / `.bash_profile` | `source spiralsafe.sh` | Linux/macOS |
| **Zsh** | `.zshrc` | `source spiralsafe.zsh` | macOS default |
| **Fish** | `config.fish` | `source spiralsafe.fish` | Alternative |
| **Nushell** | `config.nu` | `use spiralsafe.nu` | Modern shell |

### Shell Detection & Auto-Config

```bash
# Detect shell and configure
case "$SHELL" in
  */bash)  echo 'source ~/spiralsafe/spiralsafe.sh' >> ~/.bashrc ;;
  */zsh)   echo 'source ~/spiralsafe/spiralsafe.zsh' >> ~/.zshrc ;;
  */fish)  echo 'source ~/spiralsafe/spiralsafe.fish' >> ~/.config/fish/config.fish ;;
esac
```

---

## 4. IDE Integrations

| IDE | Extension | Features | Status |
|-----|-----------|----------|--------|
| **VS Code** | `spiralsafe.vscode` | Inline H&&S markers, WAVE status | ✓ Ready |
| **Wave Terminal** | Native | Full SpiralSafe integration | ✓ Primary |
| **Cursor** | Fork-compatible | Claude integration | ✓ Ready |
| **JetBrains** | `spiralsafe-intellij` | Multi-language support | ○ Planned |
| **Neovim** | `spiralsafe.nvim` | Lua plugin | ○ Planned |
| **Emacs** | `spiralsafe.el` | Elisp package | ○ Planned |
| **Zed** | Extension | Rust-native | ◐ Research |

### VS Code Extension Manifest

```json
{
  "name": "spiralsafe",
  "displayName": "SpiralSafe",
  "description": "H&&S:WAVE protocol integration",
  "version": "1.0.0",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["Other"],
  "activationEvents": ["onLanguage:*"],
  "contributes": {
    "commands": [
      { "command": "spiralsafe.bump", "title": "SpiralSafe: Create Bump" },
      { "command": "spiralsafe.wave", "title": "SpiralSafe: Send WAVE" },
      { "command": "spiralsafe.verify", "title": "SpiralSafe: Verify Signature" }
    ],
    "statusBarItems": [
      { "id": "spiralsafe.status", "alignment": "right", "priority": 100 }
    ]
  }
}
```

---

## 5. Verification Registry

### Notebook (.ipynb) Verification Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NOTEBOOK VERIFICATION PIPELINE                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   .ipynb INPUT                                                         │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────────┐                                                     │
│   │  PARSE CELLS │  Extract code, markdown, outputs                    │
│   └──────────────┘                                                     │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────────┐                                                     │
│   │   HASH EACH  │  SHA-256 per cell + metadata                        │
│   │     CELL     │  Merkle tree structure                              │
│   └──────────────┘                                                     │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────────┐                                                     │
│   │  AGGREGATE   │  Root hash of all cells                             │
│   │    HASH      │  Notebook fingerprint                               │
│   └──────────────┘                                                     │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────────┐                                                     │
│   │    SIGN      │  H&&S:WAVE signature                                │
│   │  H&&S:WAVE   │  Timestamp + platform                               │
│   └──────────────┘                                                     │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────────┐                                                     │
│   │   REGISTER   │  Store in verification registry                     │
│   │              │  D1/KV lookup table                                 │
│   └──────────────┘                                                     │
│        │                                                                │
│        ▼                                                                │
│   VERIFIED .ipynb + manifest.json                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Registry Schema

```sql
-- ops/schemas/d1-schema.sql (addition)

CREATE TABLE IF NOT EXISTS notebook_registry (
    id TEXT PRIMARY KEY,
    notebook_path TEXT NOT NULL,
    root_hash TEXT NOT NULL,          -- SHA-256 Merkle root
    cell_count INTEGER NOT NULL,
    cell_hashes TEXT NOT NULL,        -- JSON array of cell hashes
    platform TEXT NOT NULL,           -- windows|macos|linux
    ai_platform TEXT,                 -- claude|copilot|gpt|gemini
    ide TEXT,                         -- vscode|wave|cursor|jetbrains
    shell TEXT,                       -- powershell|bash|zsh|fish
    signature TEXT NOT NULL,          -- H&&S:WAVE
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    verified_at DATETIME,
    verified_by TEXT                  -- agent/user identifier
);

CREATE INDEX idx_notebook_hash ON notebook_registry(root_hash);
CREATE INDEX idx_notebook_platform ON notebook_registry(platform, ai_platform);
```

---

## 6. CI/CD Pipeline Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/spiralsafe-ci.yml

name: SpiralSafe CI

on:
  push:
    branches: [main, ops/*]
  pull_request:
    branches: [main]

jobs:
  verify:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        shell: [bash, pwsh]
        exclude:
          - os: windows-latest
            shell: bash

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Verify H&&S Signatures
        shell: ${{ matrix.shell }}
        run: |
          # Platform-specific verification
          $platform = "${{ matrix.os }}" -replace "-latest", ""
          ./ops/scripts/verify-signatures.ps1 -Platform $platform

      - name: Hash Notebooks
        shell: ${{ matrix.shell }}
        run: |
          ./ops/scripts/hash-notebooks.ps1 -Register

      - name: Update Registry
        shell: ${{ matrix.shell }}
        run: |
          ./ops/scripts/update-registry.ps1 -Sign "H&&S:WAVE"

  deploy:
    needs: verify
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Cloudflare
        run: |
          cd ops && npm ci && npm run deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
```

---

## 7. Unified Command Interface

| Command | PowerShell | Bash | Description |
|---------|-----------|------|-------------|
| Status | `ss-status` | `ss status` | Show connection/registry status |
| Verify | `ss-verify <path>` | `ss verify <path>` | Verify H&&S signature |
| Hash | `ss-hash <path>` | `ss hash <path>` | Generate SHA-256 |
| Register | `ss-register <path>` | `ss register <path>` | Add to verification registry |
| Bump | `ss-bump <agent>` | `ss bump <agent>` | Create context bump |
| Wave | `ss-wave <target>` | `ss wave <target>` | Send WAVE signal |

---

## 8. Architecture Diagram

```
                                    ┌─────────────────┐
                                    │   USER INPUT    │
                                    │  (Any Platform) │
                                    └────────┬────────┘
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                              ▼                              │
              │                    ┌──────────────────┐                    │
              │                    │   AI PLATFORMS   │                    │
              │                    │                  │                    │
              │   ┌────────────────┼────────────────┐ │                    │
              │   │                │                │ │                    │
              │   ▼                ▼                ▼ │                    │
              │ ┌──────┐    ┌──────────┐    ┌──────┐ │                    │
              │ │Claude│    │ Copilot  │    │ GPT  │ │                    │
              │ │ Code │    │          │    │      │ │                    │
              │ └──┬───┘    └────┬─────┘    └──┬───┘ │                    │
              │    │             │             │     │                    │
              │    └─────────────┴─────────────┘     │                    │
              │                  │                   │                    │
              └──────────────────┼───────────────────┘                    │
                                 │                                        │
              ┌──────────────────┼──────────────────────────────┐        │
              │                  ▼                              │        │
              │        ┌──────────────────┐                    │        │
              │        │  SPIRALSAFE API  │                    │        │
              │        │  (Cloudflare)    │                    │        │
              │        └────────┬─────────┘                    │        │
              │                 │                              │        │
              │    ┌────────────┼────────────┐                │        │
              │    ▼            ▼            ▼                │        │
              │ ┌──────┐   ┌──────┐   ┌──────────┐           │        │
              │ │  D1  │   │  KV  │   │    R2    │           │        │
              │ │ (DB) │   │(Cache│   │ (Storage)│           │        │
              │ └──────┘   └──────┘   └──────────┘           │        │
              │                                               │        │
              └───────────────────────────────────────────────┘        │
                                                                       │
              ┌────────────────────────────────────────────────────────┤
              │                     OS LAYER                          │
              │  ┌─────────┐   ┌─────────┐   ┌─────────┐              │
              │  │ Windows │   │  macOS  │   │  Linux  │              │
              │  └────┬────┘   └────┬────┘   └────┬────┘              │
              │       │            │            │                      │
              │       ▼            ▼            ▼                      │
              │  ┌─────────────────────────────────────┐              │
              │  │           SHELL LAYER              │              │
              │  │  PowerShell │ Bash │ Zsh │ Fish    │              │
              │  └─────────────────────────────────────┘              │
              │       │                                                │
              │       ▼                                                │
              │  ┌─────────────────────────────────────┐              │
              │  │           IDE LAYER                │              │
              │  │  VSCode │ Wave │ Cursor │ JetBrains│              │
              │  └─────────────────────────────────────┘              │
              │                                                       │
              └───────────────────────────────────────────────────────┘
```

---

**H&&S:WAVE** | Hope&&Sauced
*Multi-Architecture • Cross-Platform • Verified*
