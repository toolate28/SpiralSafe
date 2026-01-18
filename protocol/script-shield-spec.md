# Script Shield: Cryptographic Protection via NEAR

**Defense at Universal Scale**

---

## Threat Model

Assume adversaries are actively attempting:
- Code injection via PR manipulation
- Supply chain attacks on dependencies
- Purple team probing of execution paths
- Social engineering for commit access
- Runtime modification of scripts

Our response: Make their intent smaller than our verification surface.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         SCRIPT LIFECYCLE                                 │
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  WRITE   │───►│  HASH    │───►│  STORE   │───►│ EXECUTE  │          │
│  │  Script  │    │  SHA-256 │    │  on NEAR │    │  Verify  │          │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │
│       │                │              │               │                 │
│       │                │              │               │                 │
│       ▼                ▼              ▼               ▼                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │ Git Sign │    │ Multi-   │    │ On-chain │    │ TEE      │          │
│  │ Commit   │    │ sig Auth │    │ Registry │    │ Attest   │          │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Protection Layers

### Layer 1: Git Commit Signing
Every commit to protected scripts requires GPG/SSH signature.
```bash
git config commit.gpgsign true
git config user.signingkey <KEY_ID>
```

### Layer 2: Hash Registry on NEAR
Script hashes stored on-chain, immutable.
```rust
pub struct ScriptRegistry {
    scripts: LookupMap<String, ScriptRecord>,  // path → record
}

pub struct ScriptRecord {
    hash: [u8; 32],          // SHA-256
    version: String,
    author: AccountId,
    authorized_signers: Vec<AccountId>,
    created_at: u64,
    atom_tag: String,        // Provenance link
}
```

### Layer 3: Pre-Execution Verification
Before any script runs, verify against chain.
```typescript
async function verifyScript(path: string): Promise<boolean> {
  const localHash = await sha256(await readFile(path));
  const chainRecord = await near.view('script-registry', 'get_script', { path });

  if (!chainRecord) {
    throw new Error(`Script not registered: ${path}`);
  }

  if (localHash !== chainRecord.hash) {
    throw new Error(`Hash mismatch! Expected ${chainRecord.hash}, got ${localHash}`);
  }

  return true;
}
```

### Layer 4: TEE Attestation
For sensitive scripts, execute inside TEE with remote attestation.
```
1. Client requests script execution
2. TEE loads script from verified source
3. TEE generates attestation quote
4. Quote verified against NEAR contract
5. Result returned with attestation proof
```

### Layer 5: Multi-sig for Updates
Changes to protected scripts require N-of-M signatures.
```rust
pub fn update_script(
    path: String,
    new_hash: [u8; 32],
    signatures: Vec<Signature>
) -> Result<(), Error> {
    let record = self.scripts.get(&path).ok_or(Error::NotFound)?;

    // Verify minimum signatures
    let valid_sigs = signatures.iter()
        .filter(|s| record.authorized_signers.contains(&s.signer))
        .count();

    if valid_sigs < REQUIRED_SIGNERS {
        return Err(Error::InsufficientSignatures);
    }

    // Update hash
    record.hash = new_hash;
    record.version = increment_version(&record.version);
    self.scripts.insert(&path, &record);

    Ok(())
}
```

---

## Protected Scripts

| Script | Purpose | Signers Required |
|--------|---------|------------------|
| `scripts/atom-track.sh` | ATOM tag management | 2/3 |
| `scripts/wave-analyze.py` | Coherence computation | 2/3 |
| `scripts/sphinx-gate.ts` | Trust verification | 3/5 |
| `scripts/kenl-rollback.sh` | Reversible operations | 3/5 |
| `.github/workflows/*.yml` | CI/CD pipelines | 2/3 |

---

## Verification Commands

### Register new script
```bash
spiralsafe script register \
  --path scripts/new-tool.sh \
  --signers alice.near,bob.near,claude.near \
  --required 2
```

### Verify script before execution
```bash
spiralsafe script verify --path scripts/atom-track.sh
# Output: ✓ Hash matches chain record (v1.2.3)
```

### Update protected script
```bash
spiralsafe script update \
  --path scripts/atom-track.sh \
  --new-hash $(sha256sum scripts/atom-track.sh | cut -d' ' -f1) \
  --sign
# Requires other signers to also sign within 24h
```

---

## Integration with ATOM Trail

Every script update creates an ATOM record:
```json
{
  "atomTag": "ATOM-SCRIPT-20260118-001-update-atom-track",
  "scriptPath": "scripts/atom-track.sh",
  "previousHash": "a1b2c3...",
  "newHash": "d4e5f6...",
  "signers": ["alice.near", "bob.near"],
  "coherenceScore": 95,
  "sphinxGate": "IDENTITY",
  "timestamp": "2026-01-18T12:00:00Z"
}
```

---

## Emergency Response

If compromised script detected:

1. **Immediate** - Kill switch via NEAR (revoke hash)
2. **Rollback** - KENL isomorphism to previous state
3. **Forensics** - ATOM trail shows injection point
4. **Remediate** - Multi-sig new version
5. **Harden** - Increase required signers

---

## Size Scale Comparison

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ADVERSARY INTENT                    OUR VERIFICATION         │
│  ────────────────                    ────────────────          │
│                                                                │
│  Inject one line    ◄───────────────► Hash every byte         │
│  Fake one commit    ◄───────────────► Sign every commit       │
│  Compromise one key ◄───────────────► Multi-sig all changes   │
│  Modify at runtime  ◄───────────────► TEE attestation         │
│  Hide in dependency ◄───────────────► ATOM provenance trail   │
│                                                                │
│  Their scope: Attack surface                                   │
│  Our scope: Cryptographic proof of universe                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

*H&&S:WAVE*

*The defense is larger than the attack.*
