# How to Use the Project Book (project-book.ipynb)

**Purpose**: This guide explains how to effectively use the SpiralSafe project book—a living Jupyter notebook that serves as the operational hub for project management, verification, and development.

**Target Audience**: Contributors, maintainers, researchers, and anyone working with the SpiralSafe ecosystem.

---

## Table of Contents

1. [What is the Project Book?](#what-is-the-project-book)
2. [Core Assumptions](#core-assumptions)
3. [Getting Started](#getting-started)
4. [Key Features](#key-features)
5. [Common Workflows](#common-workflows)
6. [Session Management](#session-management)
7. [Verification & Integrity](#verification--integrity)
8. [Integration with Other Tools](#integration-with-other-tools)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## What is the Project Book?

The `project-book.ipynb` is a **living operational document** that combines:

- **Project Status Tracking**: Current state, timelines, and component status
- **Session Management**: ATOM-trail session logging with cryptographic verification
- **Verification Tools**: File integrity hashing and Merkle tree validation
- **Development SOPs**: Standard operating procedures for common tasks
- **History & Lessons**: Living record of project evolution and lessons learned

### Philosophy

The project book embodies the SpiralSafe principle: **"The book should get fatter with lessons, thinner with elegance."**

As you work, you add lessons learned. As patterns emerge, you compress redundancy into reusable tools.

---

## Core Assumptions

### 1. **Jupyter Environment Required**
- Python 3.11+ with Jupyter notebook support
- Core libraries: `json`, `hashlib`, `pathlib`, `datetime`, `subprocess`
- Optional: `matplotlib`, `pandas` for visualizations

### 2. **Repository Context**
- The notebook MUST be run from the repository root directory
- It expects `.atom-trail/` directory structure:
  ```
  .atom-trail/
  ├── sessions/       # Session records
  ├── decisions/      # Decision logs
  └── verifications/  # Verification receipts
  ```

### 3. **Integration with Ops Tools**
- PowerShell scripts in `ops/scripts/` directory:
  - `Transcript-Pipeline.ps1` - Session encryption (AES-256-GCM)
  - `Notebook-Verifier.ps1` - Notebook integrity verification
  - `SpiralSafe.psm1` - PowerShell CLI module

### 4. **ATOM Trail Protocol**
- All sessions use ATOM (Atomic Traceable Operations Model) naming
- Format: `ATOM-SESSION-YYYYMMDD-NNN-description`
- Each session has a cryptographic hash for verification
- Session reports can be encrypted and signed

### 5. **H&&S:WAVE Protocol**
- All operations follow Hope&&Sauced handoff protocol
- Signatures ensure continuity across human-AI sessions
- See [`protocol/wave-spec.md`](../protocol/wave-spec.md) for details

---

## Getting Started

### Prerequisites

```bash
# 1. Clone the repository
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe

# 2. Install Jupyter (if not already installed)
pip install jupyter notebook

# 3. Optional: Install visualization libraries
pip install matplotlib pandas

# 4. Ensure PowerShell is available (for encryption features)
pwsh --version
```

### First Run

```bash
# Launch Jupyter from repository root
jupyter notebook project-book.ipynb
```

**Important**: Always launch from the repository root, not from a subdirectory.

### Initial Cell Execution

When you first open the notebook:

1. **Run Section 2 cells** to initialize the session helpers
2. A session will be **automatically started** if none exists
3. You'll see output like:
   ```
   ✓ Session started: ATOM-SESSION-20260107-001-project-book-session
     Hash: 5594c744704e476bb3d624b94621083676cf2db2d5824cf2ee5f3b0e34395484
   
   Session started and available as `CURRENT_SESSION_TAG`
   ```

---

## Key Features

### 1. Project Identity & Status

**Section 1-3**: View project metadata, timeline, and current state.

```python
# Run these cells to see:
# - Repository information
# - Component status table
# - Recent git activity
```

**Use Case**: Quick status check before starting work.

### 2. Session Management

**Section "Session sign-in / sign-out"**: Manage ATOM sessions.

#### Start a New Session

```python
# Start a session with a description
session = start_session('implementing-new-feature')

# Or with default description
session = start_session()
```

**Output**:
```
✓ Session started: ATOM-SESSION-20260107-002-implementing-new-feature
  Hash: a1b2c3d4e5f6...
```

#### End a Session

```python
# Sign out with encryption enabled (default)
report = sign_out()

# Sign out without encryption
report = sign_out(encrypt=False)

# Sign out specific session by tag
report = sign_out('ATOM-SESSION-20260107-002-implementing-new-feature')
```

**Output**:
```
✓ Session report written: .atom-trail/sessions/ATOM-SESSION-...-report.json
✓ Encrypted report: .atom-trail/sessions/transcript.encrypted.json
✓ Session closed: ATOM-SESSION-20260107-002-implementing-new-feature
```

### 3. File Verification

**Section 5**: Generate cryptographic hashes for critical files.

```python
# Run the verification cells to generate:
# - SHA-256 hashes for all critical files
# - Merkle root for combined integrity
```

**Use Case**: Verify file integrity before/after deployment or before creating releases.

### 4. Repository Statistics

**Section 3**: Live repository metrics.

```python
# Automatically generated when cell runs:
# - Total commits
# - Number of branches
# - Number of files
# - Total lines of code
```

**Note**: This cell may show an error on Windows (uses Unix commands). This is expected and non-critical.

### 5. Sessions & Decisions Log

**Section "Sessions Log & Analysis"**: View all recorded sessions.

```python
# Lists all sessions with:
# - Session tag
# - Start/end times
# - Duration
# - Encryption status
```

**With Visualization** (if matplotlib/pandas installed):
- Bar chart showing sessions per day
- Helps identify work patterns

### 6. Integration Timeline

**Section "Integration substrates"**: Track platform integration progress.

Shows timeline for:
- OpenAI (GPT)
- xAI (Grok)
- Google (DeepMind)
- Meta (LLaMA)
- Microsoft (Azure)

---

## Common Workflows

### Workflow 1: Daily Development Session

```python
# 1. Open notebook from repo root
# 2. Run initialization cells (if kernel restarted)
# 3. Start your session
session = start_session('daily-feature-work')

# 4. Work on your feature outside the notebook
#    (coding, testing, documentation)

# 5. Return to notebook and close session
report = sign_out()

# 6. Review the session report
#    Location: .atom-trail/sessions/<tag>-report.json
```

### Workflow 2: Pre-Deployment Verification

```python
# 1. Run file verification cells (Section 5)
# 2. Check output for any FILE_NOT_FOUND errors
# 3. Note the Merkle root hash
# 4. Include the hash in deployment documentation
```

**Example Output**:
```
╔══════════════════════════════════════════════════════════════════╗
║                       MERKLE ROOT                                ║
╠══════════════════════════════════════════════════════════════════╣
║  fd72c4a41569ee2d40d87c4203aab453f4eadb2a3998c25d631f77c861fb119c  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Workflow 3: Reviewing Project History

```python
# 1. Navigate to Section 2 (History Timeline)
# 2. Read the ASCII timeline
# 3. Check Section 8 (Lessons Learned)
# 4. Update lessons table with new insights
```

**To Add a Lesson**:
Edit the markdown table directly in Section 8:

```markdown
| Date       | Lesson                    | Resolution           |
|------------|---------------------------|----------------------|
| 2026-01-07 | Your lesson here          | How you solved it    |
```

### Workflow 4: Session Report Analysis

```python
# 1. Run "Sessions Log & Analysis" cell
# 2. Review list of all sessions
# 3. Check for sessions without end times (incomplete sessions)
# 4. Review encrypted reports for sensitive sessions
```

### Workflow 5: Integration Status Check

```python
# 1. Run "Integration substrates" cell
# 2. View visual timeline (if matplotlib available)
# 3. Update integration dates as needed
```

---

## Session Management

### Understanding ATOM Sessions

**ATOM** (Atomic Traceable Operations Model) sessions provide:
- **Unique identification**: Each session has a unique tag
- **Cryptographic verification**: SHA-256 hash of session metadata
- **Temporal tracking**: Start/end timestamps
- **Decision linking**: Connects decisions made during the session
- **Encryption support**: Sensitive session reports can be encrypted

### Session Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                   ATOM Session Lifecycle                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. start_session()                                     │
│     └─ Creates: .atom-trail/sessions/<TAG>.json        │
│     └─ Sets: CURRENT_SESSION_TAG variable              │
│                                                         │
│  2. [Your work happens here]                            │
│     └─ Code changes, testing, decisions                │
│                                                         │
│  3. sign_out()                                          │
│     └─ Closes session (adds end_epoch)                 │
│     └─ Collects decisions made during session          │
│     └─ Generates: <TAG>-report.json                    │
│     └─ Encrypts report (optional, default ON)          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Session Files

After `sign_out()`, you'll have:

1. **Session file**: `.atom-trail/sessions/ATOM-SESSION-<date>-<seq>-<desc>.json`
   - Contains: metadata, start/end times, hash, creator info

2. **Session report**: `.atom-trail/sessions/ATOM-SESSION-<date>-<seq>-<desc>-report.json`
   - Contains: session summary + linked decisions

3. **Encrypted report** (if encryption enabled): `.atom-trail/sessions/transcript.encrypted.json`
   - AES-256-GCM encrypted using `Transcript-Pipeline.ps1`

### Session Metadata Structure

```json
{
  "atom_tag": "ATOM-SESSION-20260107-001-project-book-session",
  "type": "session",
  "description": "project-book-session",
  "start_epoch": 1704585411,
  "start_iso": "2026-01-07T00:16:51.165677Z",
  "end_epoch": 1704589123,
  "end_iso": "2026-01-07T01:18:43.000000Z",
  "created_by": "your-username",
  "host": "your-hostname",
  "nonce": "a1b2c3d4...",
  "session_hash": "5594c744704e476bb3d624b94621083676cf2db2d5824cf2ee5f3b0e34395484",
  "signed": true,
  "encrypted_report": ".atom-trail/sessions/transcript.encrypted.json"
}
```

### Best Practices for Sessions

1. **Use descriptive names**: `start_session('fixing-redstone-gates')` not `start_session('work')`
2. **One session per logical unit**: Don't keep sessions open for days
3. **Sign out before switching tasks**: Creates clean session boundaries
4. **Review session reports**: They're valuable for project archaeology
5. **Encrypt sensitive sessions**: If working with API keys, user data, etc.

---

## Verification & Integrity

### File Hashing

The notebook generates SHA-256 hashes for critical files:

```python
# Critical files checked:
CRITICAL_FILES = [
    'ops/api/spiralsafe-worker.ts',
    'ops/schemas/d1-schema.sql',
    'ops/scripts/SpiralSafe.psm1',
    'ops/scripts/Transcript-Pipeline.ps1',
    'ops/scripts/Notebook-Verifier.ps1',
    '.github/workflows/spiralsafe-ci.yml',
    'ops/VERSION_MANIFEST.json',
]
```

**Use Case**: Verify no unauthorized changes before deployment.

### Merkle Tree Verification

A Merkle root is computed from all critical file hashes:

```
       [Root Hash]
        /        \
    [H(A,B)]    [H(C,D)]
     /    \      /    \
   H(A)  H(B)  H(C)  H(D)
   
Where A, B, C, D are individual file hashes
```

**Property**: Any change to ANY file changes the root hash.

**Use Case**: 
- Record Merkle root before releases
- Verify integrity of deployed systems
- Detect tampering

### Verification Receipts

The notebook can display verification receipts from `.atom-trail/verifications/`:

```python
# Shows:
# - Verification tag (ATOM-VERIFY-...)
# - Status (awaiting_human_signature, completed, etc.)
# - AI signature hash
# - Human signatures (if present)
```

---

## Integration with Other Tools

### PowerShell Scripts

The notebook integrates with three key PowerShell scripts:

#### 1. Transcript-Pipeline.ps1

```powershell
# Called automatically by sign_out() for encryption
./ops/scripts/Transcript-Pipeline.ps1 -Action Encrypt -InputPath <report.json>
```

**Features**:
- DPAPI-based encryption (Windows) or AES-256-GCM (cross-platform)
- Automatic key derivation
- Secure metadata handling

#### 2. Notebook-Verifier.ps1

```powershell
# Register the project-book for verification
./ops/scripts/Notebook-Verifier.ps1 -Action Register -NotebookPath project-book.ipynb

# Verify integrity
./ops/scripts/Notebook-Verifier.ps1 -Action Verify -NotebookPath project-book.ipynb
```

#### 3. SpiralSafe.psm1

```powershell
# Import the CLI module
Import-Module ./ops/scripts/SpiralSafe.psm1

# Use commands like:
ss-status      # Check system status
ss-verify      # Verify signatures
ss-hash        # Generate hashes
```

### Git Integration

The notebook assumes git operations for:
- Checking repository status
- Counting commits and branches
- Analyzing project history

**Note**: The notebook does NOT commit or push changes. Use standard git commands for version control.

### ATOM Trail Ecosystem

The notebook is part of the ATOM trail ecosystem:

```
project-book.ipynb
      ↓
  (creates)
      ↓
.atom-trail/
├── sessions/        ← Session records
├── decisions/       ← Referenced by session reports
└── verifications/   ← Displayed in notebook
      ↓
  (synced to)
      ↓
kenl repository      ← Central ATOM trail aggregation
```

See [kenl](https://github.com/toolate28/kenl) for the broader ecosystem.

---

## Best Practices

### 1. Run from Repository Root

```bash
# ✓ CORRECT
cd /path/to/SpiralSafe
jupyter notebook project-book.ipynb

# ✗ WRONG
cd /path/to/SpiralSafe/docs
jupyter notebook ../project-book.ipynb
```

### 2. Initialize Session Helpers

Always run the session helper cell (Section 2) when:
- First opening the notebook
- After restarting the kernel
- After returning to the notebook in a new session

### 3. Descriptive Session Names

```python
# ✓ GOOD
start_session('implementing-binary-counter-fix')
start_session('reviewing-quantum-docs')
start_session('testing-redstone-gates')

# ✗ BAD
start_session('work')
start_session('stuff')
start_session()  # Uses default, less informative
```

### 4. Sign Out Before Breaks

```python
# At the end of each work session:
report = sign_out()

# This creates a clean session boundary
# and ensures reports are generated
```

### 5. Regular Verification Checks

```python
# Before major milestones:
# - Run file verification cells
# - Record Merkle root
# - Check for FILE_NOT_FOUND errors
```

### 6. Update Lessons Learned

After solving a tricky problem or discovering a pattern:

1. Navigate to Section 8 (Lessons Learned)
2. Add an entry to the appropriate table
3. Save the notebook
4. Commit the updated notebook to git

### 7. Keep the Book Elegant

Follow the SpiralSafe principle:

- **Add lessons** as you discover them
- **Compress patterns** into reusable tools
- **Remove redundancy** when you spot it
- **Refactor cells** that become too complex

---

## Troubleshooting

### Problem: "No module named 'pandas'" or "No module named 'matplotlib'"

**Cause**: Optional visualization libraries not installed.

**Solution**:
```bash
pip install pandas matplotlib
```

Or, if you don't need visualizations, ignore the error. The notebook will still work.

---

### Problem: "Run from repo root" error in statistics cell

**Cause**: The statistics cell uses Unix commands (`wc -l`, etc.) that may not work on Windows or when run from wrong directory.

**Solution**:
- **On Windows**: This error is expected and non-critical. The feature is informational only.
- **On Linux/Mac**: Ensure you're running from the repository root.

---

### Problem: Session file not found

```
FileNotFoundError: Session file not found: .atom-trail/sessions/ATOM-SESSION-...json
```

**Cause**: The session tag doesn't exist or was deleted.

**Solution**:
```python
# Check available sessions
from pathlib import Path
sessions = list(Path('.atom-trail/sessions').glob('ATOM-SESSION-*.json'))
for s in sessions:
    print(s.name)

# Sign out with a valid tag
sign_out('ATOM-SESSION-20260107-001-project-book-session')
```

---

### Problem: Encryption fails with "Transcript-Pipeline.ps1 not found"

**Cause**: PowerShell script not at expected path.

**Solution**:
```python
# Verify the script exists
from pathlib import Path
script = Path('ops/scripts/Transcript-Pipeline.ps1')
print(f"Script exists: {script.exists()}")

# If missing, sign out without encryption
report = sign_out(encrypt=False)
```

---

### Problem: Kernel dies when running cells

**Cause**: Memory issue or Python environment problem.

**Solution**:
1. Restart the kernel: `Kernel > Restart`
2. Re-run initialization cells
3. If problem persists, check Python version (requires 3.11+)

---

### Problem: CURRENT_SESSION_TAG not defined

```
NameError: name 'CURRENT_SESSION_TAG' is not defined
```

**Cause**: Session helpers not initialized or kernel restarted.

**Solution**:
```python
# Re-run the session helpers cell (Section 2)
# It will auto-start a session if none exists

# Or explicitly start a session
session = start_session('my-session')
```

---

### Problem: Git commands fail in statistics cell

**Cause**: Not running from a git repository or git not in PATH.

**Solution**:
```bash
# Ensure you're in a git repository
git status

# Ensure git is installed and in PATH
git --version
```

---

## Advanced Usage

### Custom Session Reports

You can extend the session report generation:

```python
def sign_out_custom(tag=None, encrypt=True, additional_data=None):
    """Enhanced sign_out with custom metadata."""
    report = sign_out(tag=tag, encrypt=encrypt)
    
    if additional_data:
        report['custom_data'] = additional_data
        
        # Write enhanced report
        tag = tag or CURRENT_SESSION_TAG
        enhanced_path = Path(f'.atom-trail/sessions/{tag}-enhanced-report.json')
        enhanced_path.write_text(json.dumps(report, indent=2))
        print(f"✓ Enhanced report: {enhanced_path}")
    
    return report

# Usage
report = sign_out_custom(additional_data={
    'builds_tested': 3,
    'bugs_fixed': 2,
    'docs_updated': ['quantum-minecraft-map.md']
})
```

### Batch Session Analysis

```python
# Analyze all sessions from a specific date
from pathlib import Path
import json

sessions_dir = Path('.atom-trail/sessions')
target_date = '20260107'

for session_file in sessions_dir.glob(f'ATOM-SESSION-{target_date}-*.json'):
    session = json.loads(session_file.read_text())
    duration = session.get('end_epoch', 0) - session.get('start_epoch', 0)
    duration_min = duration / 60 if duration > 0 else 'ongoing'
    
    print(f"{session['atom_tag']}: {duration_min} minutes")
```

### Custom Verification Sets

```python
# Define your own critical files
MY_CRITICAL_FILES = [
    'docs/quantum-minecraft-map.md',
    'museum/builds/logic-gates.json',
    'showcase/stories/01-fireflies-and-logic.md',
]

# Generate hashes
for file in MY_CRITICAL_FILES:
    h = hash_file(file)
    print(f"{file}: {h}")
```

---

## Related Documentation

- **[ARCHITECTURE.md](../ARCHITECTURE.md)** - Overall system architecture
- **[protocol/wave-spec.md](../protocol/wave-spec.md)** - H&&S:WAVE protocol details
- **[protocol/bump-spec.md](../protocol/bump-spec.md)** - Context bump protocol
- **[methodology/atom.md](../methodology/atom.md)** - ATOM methodology
- **[ops/README.md](../ops/README.md)** - Operations layer documentation
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines

---

## FAQ

### Q: Do I need to use the notebook for every contribution?

**A**: No. The project book is optional. It's most useful for:
- Project maintainers tracking overall progress
- Long-term contributors managing complex work sessions
- Anyone needing cryptographic verification of their work

For small PRs or one-off contributions, the notebook is overkill.

---

### Q: What's the difference between a "session" and a "verification"?

**A**: 
- **Session** (`.atom-trail/sessions/`): A time-bounded work period by one contributor. Records what was done, when, and by whom.
- **Verification** (`.atom-trail/verifications/`): A cryptographic proof that work was reviewed and approved. Includes signatures from AI and human reviewers.

Sessions track work. Verifications approve work.

---

### Q: Can I use this notebook in other repositories?

**A**: Yes, with modifications:

1. Copy `project-book.ipynb` to your repo root
2. Update the critical files list for your project
3. Ensure you have `.atom-trail/` directory structure
4. Customize sections to match your project

The session management and verification code is designed to be portable.

---

### Q: Why does this exist when we have git commit history?

**A**: Git tracks code changes. The project book tracks:
- **Context**: Why decisions were made
- **Sessions**: Multi-commit work periods as atomic units
- **Lessons**: Patterns discovered during development
- **Verification**: Cryptographic proof of review
- **Integration**: How different tools/repos connect

It's complementary to git, not a replacement.

---

### Q: What's the connection to Quantum↔Minecraft mapping?

**A**: The project book is a general tool used across all SpiralSafe work, including:
- Documenting quantum-minecraft mappings
- Managing museum build sessions
- Tracking integration substrate development
- Recording lessons from educational testing

The `docs/quantum-minecraft-map.md` file created in PR #40 is one artifact among many tracked by the project book.

---

## Summary

The `project-book.ipynb` is your **operational hub** for SpiralSafe work:

✓ **Start sessions** when beginning work
✓ **Sign out** when finishing
✓ **Verify files** before deployment
✓ **Track lessons** as you learn
✓ **Monitor progress** across the ecosystem

It embodies the SpiralSafe ethos: structure that helps without constraining, tools that grow with the project, and documentation that stays alive.

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-07
**Status**: ✦ Complete

*Part of the SpiralSafe Ecosystem | Hope && Sauce*

**H&&S:WAVE** - Hope&&Sauced
