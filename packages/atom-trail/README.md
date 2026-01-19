# ATOM Trail

> **A**uditable **T**rail **O**f **M**odifications

Decision provenance logging system for SpiralSafe. Every decision made by the system is logged with full context, rationale, and outcome, creating an auditable trail for transparency and debugging.

## Features

- 📝 **Decision Logging**: Log every decision with timestamp, vortex ID, rationale, and outcome
- 🔍 **Query Interface**: Filter and search decisions by vortex, outcome, coherence score, and time range
- 📊 **Visualization**: Generate Mermaid diagrams showing decision flows
- 📤 **Export**: Export trail in JSON, CSV, or Markdown formats
- 📈 **Statistics**: Aggregate statistics about decisions and outcomes
- ⚡ **Performance**: Handles 1000+ entries efficiently (<200ms)

## Installation

```bash
npm install @spiralsafe/atom-trail
```

## Usage

### Programmatic API

```typescript
import { logATOM, queryATOM, exportATOM } from '@spiralsafe/atom-trail';

// Log a decision
await logATOM({
  vortexId: 'wave-validator',
  decision: 'Document coherence check passed',
  rationale: 'All metrics within acceptable thresholds',
  outcome: 'success',
  coherenceScore: 0.85,
  fibonacciWeight: 8,
  context: {
    documentPath: './docs/README.md',
    curl: 0.2,
    divergence: 0.3
  }
});

// Query decisions
const entries = await queryATOM({
  vortexId: 'wave-validator',
  outcome: 'success',
  minCoherence: 0.7
});

// Export to markdown
const markdown = await exportATOM('markdown', {
  vortexId: 'wave-validator'
});
```

### CLI

```bash
# Log a decision
atom-trail log "Implemented feature X" \
  --rationale "User requested in issue #42" \
  --outcome success \
  --vortex feature-implementation \
  --coherence 0.95 \
  --priority 8

# Query decisions
atom-trail query --vortex wave-validator --outcome success

# Show statistics
atom-trail stats

# Export to markdown
atom-trail export --format markdown --output decisions.md

# Visualize a vortex
atom-trail viz wave-validator --output graph.mmd
```

## ATOM Entry Structure

```typescript
interface ATOMEntry {
  timestamp: string;          // ISO 8601 timestamp
  vortexId: string;          // Which system component generated this
  decision: string;          // What was decided
  rationale: string;         // Why (AI reasoning, human input, etc.)
  outcome: 'success' | 'failure' | 'pending';
  coherenceScore?: number;   // WAVE score at decision time (0-1)
  fibonacciWeight?: number;  // Priority (1,1,2,3,5,8,13...)
  context: Record<string, unknown>;  // Relevant state
  signature?: string;        // Cryptographic proof (optional)
  id?: string;              // Unique identifier
}
```

## Integration with WAVE

Every WAVE coherence analysis automatically logs to the ATOM trail:

```typescript
// WAVE analysis
const analysis = analyzeCoherence(content);

// Automatically creates ATOM entry
{
  vortexId: 'wave-validator',
  decision: 'Document coherence: COHERENT',
  rationale: 'Curl: 0.12, Divergence: 0.25, Potential: 0.78',
  outcome: 'success',
  coherenceScore: 0.85,
  context: {
    curl: 0.12,
    divergence: 0.25,
    potential: 0.78
  }
}
```

## Storage

- **Default**: JSON Lines file at `.spiralsafe/atom-trail.jsonl`
- **API Mode**: Cloudflare D1 database via `/api/atom/trail` endpoints
- **Cloud**: Optional sync to S3/GitHub Pages for public trails

## API Endpoints

When using the SpiralSafe API:

- `GET /api/atom/trail?vortex=<id>&outcome=<status>` - Query trail
- `POST /api/atom/trail/log` - Log a decision
- `GET /api/atom/trail/stats` - Get statistics

## CLI Commands

| Command | Description |
|---------|-------------|
| `atom-trail log <decision>` | Log a decision manually |
| `atom-trail query [options]` | Query the trail with filters |
| `atom-trail export [options]` | Export trail in various formats |
| `atom-trail viz <vortex>` | Visualize decision graph |
| `atom-trail stats` | Show trail statistics |

## Example Workflow

```bash
# 1. Start implementation
atom-trail log "Starting ATOM implementation" \
  --rationale "Foundation for provenance" \
  --outcome pending \
  --vortex atom-implementation

# 2. Complete phase
atom-trail log "Core logging complete" \
  --rationale "All tests passing" \
  --outcome success \
  --coherence 0.92 \
  --priority 8 \
  --vortex atom-implementation

# 3. View progress
atom-trail query --vortex atom-implementation

# 4. Export for PR
atom-trail export --format markdown \
  --vortex atom-implementation \
  --output ATOM_TRAIL.md
```

## Performance

Tested performance characteristics:

- **1000 entries**: ~174ms total (logging + query)
- **Query speed**: <100ms for 1000 entries
- **File size**: ~1KB per entry in JSON Lines format

## Testing

```bash
npm test
```

21 unit tests covering:
- Logging with various options
- Filtering and queries
- Visualization
- Export formats (JSON, CSV, Markdown)
- Statistics calculation
- Performance with 1000+ entries

## License

MIT - See LICENSE file

---

**H&&S:** Structure-preserving provenance across all operations
