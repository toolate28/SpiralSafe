# ATOM Persistence API Documentation

**Auditable Trail of Metadata - Complete API Reference**

> ATOM: ATOM-DOC-20260119-001-atom-api-documentation

---

## Overview

The ATOM persistence layer provides tamper-evident logging of decisions, actions, and outcomes across the SpiralSafe ecosystem. Each entry is cryptographically hashed and chained to form an immutable audit trail.

---

## Core Concepts

### ATOMEntry Structure

```typescript
interface ATOMEntry {
  id: string;                          // Unique entry identifier (UUID)
  timestamp: string;                   // ISO 8601 timestamp
  actor: string;                       // AI agent ID, user ID, or system component
  decision: string;                    // What action was taken
  rationale: string;                   // Why this decision was made
  outcome: string;                     // Result of the action
  coherenceScore?: number;             // WAVE score if applicable (0-1)
  context: Record<string, unknown>;    // Additional metadata
  parentEntry?: string;                // Link to previous decision (forms chain)
  vortexState?: string;                // Current vortex position in cascade
  hash?: string;                       // SHA-256 hash for integrity
  previousHash?: string;               // Hash of previous entry (blockchain-like)
  signature?: string;                  // Optional cryptographic signature
}
```

### Blockchain-like Integrity

Each entry includes:
- **hash**: SHA-256 of the entry's content
- **previousHash**: Hash of the chronologically previous entry

This creates a tamper-evident chain where any modification to past entries breaks the chain integrity.

---

## REST API Endpoints

### Log Decision

**Endpoint:** `POST /api/atom/trail/log`

**Description:** Log a new decision to the ATOM trail.

**Request Body:**
```json
{
  "actor": "claude",
  "decision": "Design architecture for feature X",
  "rationale": "Initial planning phase requires clear structure",
  "outcome": "COMPLETE",
  "coherenceScore": 0.85,
  "context": {
    "feature": "user-authentication",
    "phase": "planning"
  },
  "parentEntry": "uuid-of-parent-entry",
  "vortexState": "planning"
}
```

**Response:**
```json
{
  "id": "generated-uuid",
  "success": true
}
```

**Example:**
```bash
curl -X POST https://api.spiralsafe.org/api/atom/trail/log \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "actor": "claude",
    "decision": "Create documentation",
    "rationale": "Required for API reference",
    "outcome": "SUCCESS",
    "context": {}
  }'
```

---

### Query Trail

**Endpoint:** `POST /api/atom/trail/query`

**Description:** Query the ATOM trail with filters.

**Request Body:**
```json
{
  "actor": "claude",
  "since": "2026-01-19T00:00:00Z",
  "until": "2026-01-20T00:00:00Z",
  "decision": "architecture",
  "outcome": "COMPLETE",
  "minCoherence": 0.7,
  "maxCoherence": 1.0,
  "vortexState": "planning",
  "parentEntry": "uuid",
  "limit": 50,
  "offset": 0
}
```

**Response:**
```json
{
  "entries": [
    {
      "id": "uuid",
      "timestamp": "2026-01-19T12:00:00Z",
      "actor": "claude",
      "decision": "Design architecture",
      "rationale": "Initial planning",
      "outcome": "COMPLETE",
      "coherenceScore": 0.85,
      "context": {},
      "hash": "sha256-hash",
      "previousHash": "previous-sha256-hash"
    }
  ],
  "count": 1
}
```

**Example:**
```bash
curl -X POST https://api.spiralsafe.org/api/atom/trail/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"actor": "claude", "limit": 10}'
```

---

### Get Decision Chain

**Endpoint:** `GET /api/atom/trail/chain/:entryId`

**Description:** Retrieve the complete decision chain from root to specified entry.

**Response:**
```json
{
  "entries": [
    {
      "id": "root-uuid",
      "timestamp": "2026-01-19T10:00:00Z",
      "actor": "claude",
      "decision": "Root decision",
      "rationale": "Starting point",
      "outcome": "PASS",
      "context": {}
    },
    {
      "id": "child-uuid",
      "timestamp": "2026-01-19T11:00:00Z",
      "actor": "copilot",
      "decision": "Follow-up decision",
      "rationale": "Building on root",
      "outcome": "PASS",
      "context": {},
      "parentEntry": "root-uuid"
    }
  ],
  "root": {
    "id": "root-uuid",
    ...
  },
  "depth": 2,
  "integrityValid": true
}
```

**Example:**
```bash
curl -X GET https://api.spiralsafe.org/api/atom/trail/chain/some-uuid \
  -H "X-API-Key: your-api-key"
```

---

### Verify Trail Integrity

**Endpoint:** `GET /api/atom/trail/verify`

**Description:** Verify the integrity of the entire ATOM trail (detect tampering).

**Response:**
```json
{
  "valid": true,
  "totalEntries": 150,
  "brokenChains": 0,
  "tamperedEntries": [],
  "details": []
}
```

**Example (with issues):**
```json
{
  "valid": false,
  "totalEntries": 150,
  "brokenChains": 2,
  "tamperedEntries": ["uuid-1", "uuid-2"],
  "details": [
    "Entry uuid-1: Hash mismatch",
    "Entry uuid-2: Broken chain link"
  ]
}
```

**Example:**
```bash
curl -X GET https://api.spiralsafe.org/api/atom/trail/verify \
  -H "X-API-Key: your-api-key"
```

---

### Export Trail

**Endpoint:** `POST /api/atom/trail/export`

**Description:** Export trail entries in different formats.

**Request Body:**
```json
{
  "format": "markdown",
  "filter": {
    "actor": "claude",
    "since": "2026-01-19T00:00:00Z",
    "limit": 100
  }
}
```

**Supported Formats:**
- `markdown` - Human-readable timeline
- `json` - Machine-readable for analysis
- `csv` - Spreadsheet format

**Response:** The exported content in the requested format.

**Example:**
```bash
curl -X POST https://api.spiralsafe.org/api/atom/trail/export \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"format": "markdown", "filter": {"limit": 50}}' \
  > atom-trail.md
```

---

## CLI Commands

### Prerequisites

```bash
# Set API base URL (optional, defaults to https://api.spiralsafe.org)
export SPIRALSAFE_API_BASE="https://api.spiralsafe.org"
```

### Log a Decision

```bash
spiralsafe atom log "Deploy to production" "All tests passed" "SUCCESS" \
  --actor "human-operator" \
  --coherence 0.95
```

**Options:**
- `--actor <actor>` - Actor making the decision (default: cli)
- `--coherence <score>` - Coherence score 0-1
- `--parent <entry-id>` - Parent entry ID to link to
- `--vortex <state>` - Vortex state

### Query the Trail

```bash
# Query by actor
spiralsafe atom query --actor claude --limit 10

# Query by date range
spiralsafe atom query --since 2026-01-19 --until 2026-01-20

# Search in decisions
spiralsafe atom query --decision "architecture" --limit 5

# Filter by outcome
spiralsafe atom query --outcome "SUCCESS"
```

**Options:**
- `--actor <actor>` - Filter by actor
- `--since <date>` - ISO 8601 timestamp (e.g., 2026-01-19)
- `--until <date>` - ISO 8601 timestamp
- `--decision <text>` - Search in decision text
- `--outcome <text>` - Filter by outcome
- `--limit <n>` - Max results (default: 50)

### Show Decision Chain

```bash
spiralsafe atom chain <entry-id>
```

**Output:**
```
Decision Chain (depth: 3):
✓ Chain integrity: VALID

  [2026-01-19T10:00:00Z] claude
    Decision: Root decision
    Outcome: PASS
    ID: root-uuid

  [2026-01-19T11:00:00Z] copilot
    Decision: Follow-up decision
    Outcome: PASS
    ID: child-uuid
```

### Verify Trail Integrity

```bash
spiralsafe atom verify
```

**Output:**
```
✓ Trail integrity: VALID

  Total entries: 150
  Broken chains: 0
  Tampered entries: 0
```

### Export Trail

```bash
# Export to Markdown
spiralsafe atom export --format markdown --output trail.md

# Export to JSON
spiralsafe atom export --format json --since 2026-01-19 > trail.json

# Export to CSV
spiralsafe atom export --format csv --actor claude > claude-trail.csv
```

**Options:**
- `--format <format>` - Export format: markdown, json, csv (default: markdown)
- `--since <date>` - Filter by start date
- `--actor <actor>` - Filter by actor
- `--limit <n>` - Max entries (default: 1000)
- `--output <file>` - Output file path (default: stdout)

---

## Integration Examples

### WAVE Validator Integration

```typescript
import { ATOMPersister } from './atom-persister';

// After WAVE analysis
const atomPersister = new ATOMPersister('sqlite', env.SPIRALSAFE_DB, env.SPIRALSAFE_KV);
await atomPersister.log({
  actor: 'wave-validator',
  decision: `Analyzed content coherence`,
  rationale: `Threshold check: curl=0.2, divergence=0.1`,
  outcome: analysis.coherent ? 'PASS' : 'FAIL',
  coherenceScore: analysis.curl + Math.abs(analysis.divergence),
  context: {
    curl: analysis.curl,
    divergence: analysis.divergence,
    potential: analysis.potential,
    regions: analysis.regions.length,
  },
});
```

### H&&S Protocol Integration

```typescript
// After creating bump marker
await atomPersister.log({
  actor: bump.from,
  decision: `H&&S:${bump.type} to ${bump.to}`,
  rationale: `Agent handoff: ${bump.state}`,
  outcome: 'Context transferred',
  context: {
    handoffType: bump.type,
    nextAgent: bump.to,
    bumpId: bump.id,
    ...bump.context,
  },
});
```

### Multi-Agent Collaboration

```typescript
// Claude's initial decision
const id1 = await atomPersister.log({
  actor: 'claude',
  decision: 'Design system architecture',
  rationale: 'Initial planning phase',
  outcome: 'COMPLETE',
  context: { feature: 'auth-system' },
});

// Copilot builds on Claude's work
const id2 = await atomPersister.log({
  actor: 'copilot',
  decision: 'Implement authentication handlers',
  rationale: 'Following approved architecture',
  outcome: 'COMPLETE',
  context: { feature: 'auth-system' },
  parentEntry: id1,
});

// Human reviews
await atomPersister.log({
  actor: 'human-reviewer',
  decision: 'Code review and approval',
  rationale: 'Quality check passed',
  outcome: 'APPROVED',
  context: { feature: 'auth-system' },
  parentEntry: id2,
});

// Retrieve full chain
const chain = await atomPersister.getChain(id2);
console.log(`Chain depth: ${chain.depth}, integrity: ${chain.integrityValid}`);
```

---

## Export Format Examples

### Markdown Timeline

```markdown
# ATOM Trail Timeline

## 2026-01-19T12:00:00Z - claude

**Decision:** Design system architecture

**Rationale:** Initial planning phase

**Outcome:** COMPLETE

**Coherence Score:** 0.85

**Context:**
\`\`\`json
{
  "feature": "auth-system",
  "phase": "planning"
}
\`\`\`

---
```

### JSON Format

```json
[
  {
    "id": "uuid",
    "timestamp": "2026-01-19T12:00:00Z",
    "actor": "claude",
    "decision": "Design system architecture",
    "rationale": "Initial planning phase",
    "outcome": "COMPLETE",
    "coherenceScore": 0.85,
    "context": {
      "feature": "auth-system"
    },
    "hash": "sha256-hash"
  }
]
```

### CSV Format

```csv
id,timestamp,actor,decision,rationale,outcome,coherenceScore,vortexState,parentEntry,hash
uuid,2026-01-19T12:00:00Z,claude,"Design system architecture","Initial planning phase",COMPLETE,0.85,,,sha256-hash
```

---

## Best Practices

### 1. Actor Naming

Use consistent actor identifiers:
- AI agents: `claude`, `copilot`, `grok`
- Humans: `human-<name>` or `user-<id>`
- System components: `wave-validator`, `bump-creator`, `awi-verifier`

### 2. Decision Granularity

- **Good:** "Implemented authentication middleware"
- **Too vague:** "Made changes"
- **Too detailed:** "Added 47 lines to auth.ts including imports, types, and middleware function with error handling"

### 3. Context Structure

Include relevant but concise metadata:
```typescript
{
  feature: 'auth',
  phase: 'implementation',
  files: ['auth.ts', 'middleware.ts'],
  tests_added: 12
}
```

### 4. Chain Usage

Link related decisions:
- Use `parentEntry` for direct dependencies
- Query by actor/time for related work
- Use chains to trace decision evolution

### 5. Coherence Scores

Include WAVE scores when applicable:
- Documentation changes: Log analysis coherence
- Code reviews: Log maintainability score
- Architecture decisions: Log design coherence

---

## Security Considerations

### Hash Verification

**Note on Current Implementation:** The current hash function uses a simplified 32-bit hash for demonstration purposes. For production environments requiring cryptographic integrity, the implementation should be upgraded to use Web Crypto API's SHA-256:

```typescript
async calculateHash(entry: ATOMEntry): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(JSON.stringify(hashInput));
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}
```

This would require making the `log()` method async, but provides proper tamper detection.

Always verify trail integrity before critical operations:
```typescript
const verification = await atomPersister.verify();
if (!verification.valid) {
  throw new Error(`Trail integrity compromised: ${verification.tamperedEntries}`);
}
```

### Rate Limiting

API endpoints are rate-limited:
- Default: 100 requests per 60 seconds
- Authenticated: Higher limits available
- Batch operations recommended for bulk logging

### Data Privacy

- Do not log sensitive data (passwords, tokens, PII)
- Use context field for metadata, not raw content
- Audit trail is append-only and permanent

---

## Troubleshooting

### "Trail integrity: INVALID"

**Cause:** Hash chain broken or entries tampered with

**Solution:**
```bash
spiralsafe atom verify
# Review details
# Restore from backup if necessary
```

### "Rate limit exceeded"

**Cause:** Too many requests in short time

**Solution:**
- Batch multiple decisions into single log call with context
- Implement exponential backoff
- Request higher rate limits for production use

### Query returns no results

**Checklist:**
- Verify actor name matches exactly (case-sensitive)
- Check date format (ISO 8601 required)
- Confirm entries exist with `spiralsafe atom query --limit 10`
- Review filter combinations

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS atom_entries (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    actor TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT NOT NULL,
    outcome TEXT NOT NULL,
    coherence_score REAL,
    context TEXT NOT NULL, -- JSON
    parent_entry TEXT,
    vortex_state TEXT,
    hash TEXT,
    previous_hash TEXT,
    signature TEXT,
    FOREIGN KEY (parent_entry) REFERENCES atom_entries(id)
);

CREATE INDEX idx_atom_timestamp ON atom_entries(timestamp);
CREATE INDEX idx_atom_actor ON atom_entries(actor);
CREATE INDEX idx_atom_parent ON atom_entries(parent_entry);
```

---

## Additional Resources

- [ATOM Methodology](../../methodology/atom.md) - Task orchestration principles
- [Wave Protocol](../../protocol/wave-spec.md) - Coherence analysis integration
- [Bump Protocol](../../protocol/bump-spec.md) - Agent handoff integration
- [SpiralSafe API](../README.md) - General API documentation

---

_~ Hope&&Sauced - Making decisions auditable, one ATOM at a time_
