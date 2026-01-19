# ATOM Trail Persister

**Foundational provenance logging system for all SpiralSafe/QDI decisions**

ATOM: ATOM-FEATURE-20260119-001-atom-trail-persister

---

## Overview

The ATOM Trail Persister provides a comprehensive decision logging and audit system that captures every decision made within the SpiralSafe ecosystem. It implements JSON Lines storage for efficient append-only logging and provides powerful querying, export, and visualization capabilities.

## Core Concepts

### ATOM Entry

An ATOM entry represents a single decision point with full provenance:

```typescript
interface ATOMEntry {
  timestamp: string;           // ISO 8601 timestamp
  vortexId: string;           // Identifies the decision context/vortex
  decision: string;           // The decision made
  rationale: string;          // Why this decision was made
  outcome: 'success' | 'failure' | 'pending';
  coherenceScore?: number;    // 0-1 score from WAVE analysis
  fibonacciWeight?: number;   // For 42-cycle tracking
  context: Record<string, unknown>;  // Additional metadata
  signature?: string;         // Cryptographic signature
}
```

### Vortexes

A vortex represents a logical grouping of related decisions, such as:
- A specific PR or issue
- A feature implementation
- A debugging session
- An architectural discussion

### 42-Cycle Iterations

The system detects and tracks Fibonacci-weighted 42-cycle patterns, which represent complete iteration cycles in the SpiralSafe methodology.

---

## API Endpoints

### POST `/api/atom/log`

Log a new ATOM decision.

**Request:**
```json
{
  "vortexId": "pr-123",
  "decision": "Implement ATOM trail persister",
  "rationale": "Need provenance logging for decisions",
  "outcome": "success",
  "coherenceScore": 0.85,
  "context": {
    "component": "ops/api",
    "author": "copilot"
  }
}
```

**Response:**
```json
{
  "timestamp": "2026-01-19T13:30:00Z",
  "vortexId": "pr-123",
  "decision": "Implement ATOM trail persister",
  "rationale": "Need provenance logging for decisions",
  "outcome": "success",
  "coherenceScore": 0.85,
  "context": {
    "component": "ops/api",
    "author": "copilot"
  }
}
```

### GET `/api/atom/query`

Query ATOM trail entries with filters.

**Parameters:**
- `vortexId` - Filter by vortex ID
- `outcome` - Filter by outcome (success/failure/pending)
- `startTime` - ISO timestamp for start of range
- `endTime` - ISO timestamp for end of range
- `minCoherence` - Minimum coherence score (0-1)
- `limit` - Maximum number of results (default: 100)

**Example:**
```
GET /api/atom/query?vortexId=pr-123&outcome=success&limit=10
```

### GET `/api/atom/export`

Export ATOM trail data in various formats.

**Parameters:**
- `format` - Export format: `json`, `csv`, or `markdown`
- `vortexId` - Optional filter by vortex
- `outcome` - Optional filter by outcome

**Example:**
```
GET /api/atom/export?format=csv&vortexId=pr-123
```

### GET `/api/atom/visualize`

Generate visualization data for ATOM trail graph.

**Parameters:**
- `vortexId` - Optional filter by vortex
- `limit` - Maximum number of entries (default: 50)

**Response:**
```json
{
  "mermaid": "graph TD\n  V_pr-123[Vortex pr-123]\n  ...",
  "nodes": 15
}
```

### GET `/api/atom/stats`

Get aggregate statistics about the ATOM trail.

**Response:**
```json
{
  "total_entries": 1247,
  "success_count": 1089,
  "failure_count": 42,
  "pending_count": 116,
  "avg_coherence": 0.82,
  "vortex_count": 23,
  "oldest_entry": "2026-01-01T00:00:00Z",
  "newest_entry": "2026-01-19T13:30:00Z"
}
```

---

## CLI Usage

The ATOM trail persister can be accessed via the `spiralsafe` CLI:

### Log a Decision

```bash
spiralsafe atom log \
  --vortex "pr-123" \
  --decision "Add validation" \
  --rationale "Prevent invalid input" \
  --outcome "success" \
  --coherence 0.9
```

### Query Entries

```bash
# Query all entries for a vortex
spiralsafe atom query --vortex "pr-123"

# Query successful decisions with high coherence
spiralsafe atom query --outcome success --min-coherence 0.8 --limit 20
```

### Export Data

```bash
# Export as JSON
spiralsafe atom export --format json > trail.json

# Export as CSV for a specific vortex
spiralsafe atom export --format csv --vortex "pr-123" > pr-123-trail.csv

# Export as Markdown
spiralsafe atom export --format markdown > TRAIL_REPORT.md
```

### Visualize Trail

```bash
# Generate Mermaid diagram
spiralsafe atom viz --vortex "pr-123"

# Visualize recent decisions
spiralsafe atom viz --limit 30
```

### View Statistics

```bash
spiralsafe atom stats
```

---

## Integration with WAVE Analysis

WAVE coherence analysis automatically logs to the ATOM trail when a `vortexId` is provided:

```bash
# Analyze content and log to ATOM trail
curl -X POST https://api.spiralsafe.org/api/wave/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "document content...",
    "vortexId": "pr-123"
  }'
```

This creates an ATOM entry with:
- Decision: "WAVE analysis completed"
- Outcome: Based on coherence (pass/fail)
- Coherence Score: Calculated from curl and divergence
- Context: WAVE metrics (curl, divergence, potential)

---

## Performance

The ATOM trail persister is designed for high performance:

- **Query Performance**: <100ms for 1,000 entries
- **Write Performance**: Append-only writes are O(1)
- **Storage Format**: JSON Lines for efficient streaming
- **Indexes**: Optimized for vortex, outcome, timestamp, and coherence queries

---

## File-Based Storage

For local development and testing, the trail-persister module supports file-based storage:

```typescript
import { logATOM, queryATOM } from './trail-persister';

// Log to custom file
await logATOM(entry, '/path/to/trail.jsonl');

// Query from custom file
const results = await queryATOM({ vortexId: 'test' }, '/path/to/trail.jsonl');
```

Default storage location: `.spiralsafe/atom-trail.jsonl`

---

## Database Schema

The `atom_trail` table in D1:

```sql
CREATE TABLE atom_trail (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    vortex_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN ('success', 'failure', 'pending')),
    coherence_score REAL,
    fibonacci_weight INTEGER,
    context TEXT, -- JSON
    signature TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_atom_trail_vortex ON atom_trail(vortex_id);
CREATE INDEX idx_atom_trail_outcome ON atom_trail(outcome);
CREATE INDEX idx_atom_trail_timestamp ON atom_trail(timestamp);
CREATE INDEX idx_atom_trail_coherence ON atom_trail(coherence_score);
```

---

## Security & Authentication

Write operations (POST) require API key authentication:

```bash
curl -X POST https://api.spiralsafe.org/api/atom/log \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"vortexId": "...", ...}'
```

Read operations (GET) are rate-limited but do not require authentication.

---

## Examples

### Track PR Review Decisions

```typescript
// Log initial review
await logATOM({
  timestamp: new Date().toISOString(),
  vortexId: 'pr-456',
  decision: 'Request changes on PR',
  rationale: 'Missing test coverage',
  outcome: 'pending',
  context: { reviewer: 'claude', files_changed: 5 }
});

// Log follow-up
await logATOM({
  timestamp: new Date().toISOString(),
  vortexId: 'pr-456',
  decision: 'Approve PR',
  rationale: 'Tests added, coherence verified',
  outcome: 'success',
  coherenceScore: 0.92,
  context: { reviewer: 'claude', test_coverage: 0.89 }
});

// Query all PR decisions
const prDecisions = await queryATOM({ vortexId: 'pr-456' });
```

### Track Feature Implementation

```typescript
// Track each implementation decision
for (const decision of implementationSteps) {
  await logATOM({
    timestamp: new Date().toISOString(),
    vortexId: 'feature-atom-trail',
    decision: decision.name,
    rationale: decision.rationale,
    outcome: decision.success ? 'success' : 'failure',
    fibonacciWeight: decision.complexity,
    context: decision.metadata
  });
}

// Visualize implementation flow
const viz = await visualizeATOM('mermaid', { vortexId: 'feature-atom-trail' });
```

---

## See Also

- [WAVE Protocol](../../protocol/wave-spec.md) - Coherence analysis
- [BUMP Protocol](../../protocol/bump-spec.md) - Handoff markers
- [ATOM Methodology](../../methodology/atom.md) - Task orchestration
- [AWI Protocol](../../ARCHITECTURE.md) - Authorization-with-intent

---

*H&&S: Every decision leaves a trace. Make them count.*
