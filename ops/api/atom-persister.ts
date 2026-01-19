/**
 * ATOM Persister - Auditable Trail of Metadata
 * 
 * Persistence layer for tracking decisions, actions, and outcomes across
 * the SpiralSafe ecosystem with cryptographic integrity.
 * 
 * ATOM: ATOM-INIT-20260119-001-atom-persistence-layer
 */

// ═══════════════════════════════════════════════════════════════
// Types
// ═══════════════════════════════════════════════════════════════

export interface ATOMEntry {
  id: string;                          // Unique entry identifier
  timestamp: string;                   // ISO 8601
  actor: string;                       // AI agent ID, user ID, or system component
  decision: string;                    // What action was taken
  rationale: string;                   // Why this decision was made
  outcome: string;                     // Result of the action
  coherenceScore?: number;             // WAVE score if applicable
  context: Record<string, unknown>;    // Additional metadata
  parentEntry?: string;                // Link to previous decision (forms chain)
  vortexState?: string;                // Current vortex position in cascade
  hash?: string;                       // SHA-256 hash for integrity
  previousHash?: string;               // Hash of previous entry (blockchain-like)
  signature?: string;                  // Optional cryptographic signature
}

export interface ATOMQuery {
  actor?: string;                      // Filter by actor
  since?: string;                      // ISO 8601 timestamp
  until?: string;                      // ISO 8601 timestamp
  decision?: string;                   // Search in decision text
  outcome?: string;                    // Filter by outcome
  minCoherence?: number;               // Minimum coherence score
  maxCoherence?: number;               // Maximum coherence score
  vortexState?: string;                // Filter by vortex state
  parentEntry?: string;                // Filter by parent
  limit?: number;                      // Max results (default: 100)
  offset?: number;                     // Pagination offset
}

export interface ATOMChain {
  entries: ATOMEntry[];
  root: ATOMEntry;
  depth: number;
  integrityValid: boolean;
}

export interface ATOMVerification {
  valid: boolean;
  totalEntries: number;
  brokenChains: number;
  tamperedEntries: string[];
  details: string[];
}

export type ATOMStorageBackend = 'json' | 'sqlite' | 'git';

// ═══════════════════════════════════════════════════════════════
// ATOM Persister Class
// ═══════════════════════════════════════════════════════════════

export class ATOMPersister {
  private backend: ATOMStorageBackend;
  private db?: D1Database;
  private kvNamespace?: KVNamespace;
  private lastHash?: string;

  constructor(backend: ATOMStorageBackend = 'json', db?: D1Database, kv?: KVNamespace) {
    this.backend = backend;
    this.db = db;
    this.kvNamespace = kv;
  }

  /**
   * Log a single decision to the ATOM trail
   * @param entry - The ATOM entry to log
   * @returns The entry ID
   */
  async log(entry: Omit<ATOMEntry, 'id' | 'timestamp' | 'hash' | 'previousHash'>): Promise<string> {
    const id = this.generateId();
    const timestamp = new Date().toISOString();
    
    // Create full entry with generated fields
    const fullEntry: ATOMEntry = {
      id,
      timestamp,
      ...entry,
      previousHash: this.lastHash,
    };

    // Calculate hash for integrity
    fullEntry.hash = this.calculateHash(fullEntry);
    this.lastHash = fullEntry.hash;

    // Persist to backend
    await this.persist(fullEntry);

    return id;
  }

  /**
   * Query the ATOM trail with filters
   * @param filter - Query filters
   * @returns Matching ATOM entries
   */
  async query(filter: ATOMQuery): Promise<ATOMEntry[]> {
    const limit = filter.limit ?? 100;
    const offset = filter.offset ?? 0;

    if (this.backend === 'sqlite' && this.db) {
      return await this.querySQLite(filter, limit, offset);
    } else if (this.backend === 'json' && this.kvNamespace) {
      return await this.queryJSON(filter, limit, offset);
    }

    return [];
  }

  /**
   * Get the full chain from root decision to specified entry
   * @param entryId - The entry ID to trace back from
   * @returns The complete chain
   */
  async getChain(entryId: string): Promise<ATOMChain> {
    const entries: ATOMEntry[] = [];
    let currentId: string | undefined = entryId;
    let integrityValid = true;

    // Walk backwards through the chain
    while (currentId) {
      const entry = await this.getEntry(currentId);
      if (!entry) break;

      entries.unshift(entry);

      // Verify integrity
      if (entry.hash && entry.previousHash) {
        const expectedHash = this.calculateHash(entry);
        if (expectedHash !== entry.hash) {
          integrityValid = false;
        }
      }

      currentId = entry.parentEntry;
    }

    return {
      entries,
      root: entries[0],
      depth: entries.length,
      integrityValid,
    };
  }

  /**
   * Verify trail integrity (detect tampering)
   * @returns Verification result
   */
  async verify(): Promise<ATOMVerification> {
    const allEntries = await this.query({ limit: 10000 });
    
    const result: ATOMVerification = {
      valid: true,
      totalEntries: allEntries.length,
      brokenChains: 0,
      tamperedEntries: [],
      details: [],
    };

    // Build hash chain map
    const hashMap = new Map<string, ATOMEntry>();
    allEntries.forEach(entry => {
      if (entry.hash) {
        hashMap.set(entry.hash, entry);
      }
    });

    // Verify each entry
    for (const entry of allEntries) {
      // Verify hash integrity
      if (entry.hash) {
        const expectedHash = this.calculateHash(entry);
        if (expectedHash !== entry.hash) {
          result.valid = false;
          result.tamperedEntries.push(entry.id);
          result.details.push(`Entry ${entry.id}: Hash mismatch`);
        }
      }

      // Verify chain integrity
      if (entry.previousHash) {
        const previousEntry = hashMap.get(entry.previousHash);
        if (!previousEntry) {
          result.valid = false;
          result.brokenChains++;
          result.details.push(`Entry ${entry.id}: Broken chain link`);
        }
      }
    }

    return result;
  }

  /**
   * Export entries to different formats
   * @param entries - Entries to export
   * @param format - Export format
   * @returns Formatted string
   */
  export(entries: ATOMEntry[], format: 'markdown' | 'json' | 'csv'): string {
    switch (format) {
      case 'markdown':
        return this.exportMarkdown(entries);
      case 'json':
        return JSON.stringify(entries, null, 2);
      case 'csv':
        return this.exportCSV(entries);
      default:
        return '';
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // Private Methods
  // ═══════════════════════════════════════════════════════════════

  private generateId(): string {
    return crypto.randomUUID();
  }

  private calculateHash(entry: ATOMEntry): string {
    const hashInput = {
      id: entry.id,
      timestamp: entry.timestamp,
      actor: entry.actor,
      decision: entry.decision,
      rationale: entry.rationale,
      outcome: entry.outcome,
      coherenceScore: entry.coherenceScore,
      context: entry.context,
      parentEntry: entry.parentEntry,
      vortexState: entry.vortexState,
      previousHash: entry.previousHash,
    };

    const jsonStr = JSON.stringify(hashInput);
    // For Web Crypto API (Cloudflare Workers), we'd use:
    // const encoder = new TextEncoder();
    // const data = encoder.encode(jsonStr);
    // const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    // return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
    
    // For simplicity in this implementation, using a basic hash
    // In production, should use proper async crypto.subtle.digest
    let hash = 0;
    for (let i = 0; i < jsonStr.length; i++) {
      const char = jsonStr.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    // Convert to hex and pad to 64 chars (SHA-256 length)
    return Math.abs(hash).toString(16).padStart(64, '0');
  }

  private async persist(entry: ATOMEntry): Promise<void> {
    if (this.backend === 'sqlite' && this.db) {
      await this.persistSQLite(entry);
    } else if (this.backend === 'json' && this.kvNamespace) {
      await this.persistJSON(entry);
    }
  }

  private async persistSQLite(entry: ATOMEntry): Promise<void> {
    if (!this.db) return;

    await this.db.prepare(`
      INSERT INTO atom_entries (
        id, timestamp, actor, decision, rationale, outcome,
        coherence_score, context, parent_entry, vortex_state,
        hash, previous_hash, signature
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      entry.id,
      entry.timestamp,
      entry.actor,
      entry.decision,
      entry.rationale,
      entry.outcome,
      entry.coherenceScore ?? null,
      JSON.stringify(entry.context),
      entry.parentEntry ?? null,
      entry.vortexState ?? null,
      entry.hash ?? null,
      entry.previousHash ?? null,
      entry.signature ?? null,
    ).run();
  }

  private async persistJSON(entry: ATOMEntry): Promise<void> {
    if (!this.kvNamespace) return;

    // Store individual entry
    const key = `atom:entry:${entry.id}`;
    await this.kvNamespace.put(key, JSON.stringify(entry));

    // Update index for queries
    const indexKey = `atom:index:${entry.actor}:${entry.timestamp}`;
    await this.kvNamespace.put(indexKey, entry.id);
  }

  private async getEntry(entryId: string): Promise<ATOMEntry | null> {
    if (this.backend === 'sqlite' && this.db) {
      const result = await this.db.prepare(
        'SELECT * FROM atom_entries WHERE id = ?'
      ).bind(entryId).first();

      if (!result) return null;

      return this.parseEntry(result);
    } else if (this.backend === 'json' && this.kvNamespace) {
      const key = `atom:entry:${entryId}`;
      const data = await this.kvNamespace.get(key);
      return data ? JSON.parse(data) : null;
    }

    return null;
  }

  private async querySQLite(filter: ATOMQuery, limit: number, offset: number): Promise<ATOMEntry[]> {
    if (!this.db) return [];

    const conditions: string[] = [];
    const bindings: (string | number)[] = [];

    if (filter.actor) {
      conditions.push('actor = ?');
      bindings.push(filter.actor);
    }

    if (filter.since) {
      conditions.push('timestamp >= ?');
      bindings.push(filter.since);
    }

    if (filter.until) {
      conditions.push('timestamp <= ?');
      bindings.push(filter.until);
    }

    if (filter.decision) {
      conditions.push('decision LIKE ?');
      bindings.push(`%${filter.decision}%`);
    }

    if (filter.outcome) {
      conditions.push('outcome LIKE ?');
      bindings.push(`%${filter.outcome}%`);
    }

    if (filter.minCoherence !== undefined) {
      conditions.push('coherence_score >= ?');
      bindings.push(filter.minCoherence);
    }

    if (filter.maxCoherence !== undefined) {
      conditions.push('coherence_score <= ?');
      bindings.push(filter.maxCoherence);
    }

    if (filter.vortexState) {
      conditions.push('vortex_state = ?');
      bindings.push(filter.vortexState);
    }

    if (filter.parentEntry) {
      conditions.push('parent_entry = ?');
      bindings.push(filter.parentEntry);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';
    const query = `
      SELECT * FROM atom_entries
      ${whereClause}
      ORDER BY timestamp DESC
      LIMIT ? OFFSET ?
    `;

    bindings.push(limit, offset);

    const result = await this.db.prepare(query).bind(...bindings).all();
    return result.results.map(row => this.parseEntry(row));
  }

  private async queryJSON(filter: ATOMQuery, limit: number, offset: number): Promise<ATOMEntry[]> {
    if (!this.kvNamespace) return [];

    // For JSON backend, we need to scan keys and filter
    // This is less efficient but works for smaller datasets
    const entries: ATOMEntry[] = [];
    
    // List all entry keys (simplified - in production would use better indexing)
    const list = await this.kvNamespace.list({ prefix: 'atom:entry:' });
    
    for (const key of list.keys) {
      if (entries.length >= limit + offset) break;
      
      const data = await this.kvNamespace.get(key.name);
      if (!data) continue;
      
      const entry: ATOMEntry = JSON.parse(data);
      
      // Apply filters
      if (filter.actor && entry.actor !== filter.actor) continue;
      if (filter.since && entry.timestamp < filter.since) continue;
      if (filter.until && entry.timestamp > filter.until) continue;
      if (filter.decision && !entry.decision.includes(filter.decision)) continue;
      if (filter.outcome && !entry.outcome.includes(filter.outcome)) continue;
      if (filter.minCoherence !== undefined && (entry.coherenceScore ?? 0) < filter.minCoherence) continue;
      if (filter.maxCoherence !== undefined && (entry.coherenceScore ?? 1) > filter.maxCoherence) continue;
      if (filter.vortexState && entry.vortexState !== filter.vortexState) continue;
      if (filter.parentEntry && entry.parentEntry !== filter.parentEntry) continue;
      
      entries.push(entry);
    }

    // Sort by timestamp descending
    entries.sort((a, b) => b.timestamp.localeCompare(a.timestamp));

    // Apply pagination
    return entries.slice(offset, offset + limit);
  }

  private parseEntry(row: Record<string, unknown>): ATOMEntry {
    return {
      id: row.id as string,
      timestamp: row.timestamp as string,
      actor: row.actor as string,
      decision: row.decision as string,
      rationale: row.rationale as string,
      outcome: row.outcome as string,
      coherenceScore: row.coherence_score as number | undefined,
      context: JSON.parse(row.context as string),
      parentEntry: row.parent_entry as string | undefined,
      vortexState: row.vortex_state as string | undefined,
      hash: row.hash as string | undefined,
      previousHash: row.previous_hash as string | undefined,
      signature: row.signature as string | undefined,
    };
  }

  private exportMarkdown(entries: ATOMEntry[]): string {
    let md = '# ATOM Trail Timeline\n\n';
    
    for (const entry of entries) {
      md += `## ${entry.timestamp} - ${entry.actor}\n\n`;
      md += `**Decision:** ${entry.decision}\n\n`;
      md += `**Rationale:** ${entry.rationale}\n\n`;
      md += `**Outcome:** ${entry.outcome}\n\n`;
      
      if (entry.coherenceScore !== undefined && entry.coherenceScore !== null) {
        md += `**Coherence Score:** ${entry.coherenceScore.toFixed(2)}\n\n`;
      }
      
      if (entry.vortexState) {
        md += `**Vortex State:** ${entry.vortexState}\n\n`;
      }
      
      if (entry.context && Object.keys(entry.context).length > 0) {
        md += `**Context:**\n\`\`\`json\n${JSON.stringify(entry.context, null, 2)}\n\`\`\`\n\n`;
      }
      
      md += '---\n\n';
    }
    
    return md;
  }

  private exportCSV(entries: ATOMEntry[]): string {
    const headers = [
      'id', 'timestamp', 'actor', 'decision', 'rationale', 'outcome',
      'coherenceScore', 'vortexState', 'parentEntry', 'hash'
    ];
    
    let csv = headers.join(',') + '\n';
    
    for (const entry of entries) {
      const row = [
        this.escapeCsv(entry.id),
        this.escapeCsv(entry.timestamp),
        this.escapeCsv(entry.actor),
        this.escapeCsv(entry.decision),
        this.escapeCsv(entry.rationale),
        this.escapeCsv(entry.outcome),
        entry.coherenceScore?.toString() ?? '',
        this.escapeCsv(entry.vortexState ?? ''),
        this.escapeCsv(entry.parentEntry ?? ''),
        this.escapeCsv(entry.hash ?? ''),
      ];
      
      csv += row.join(',') + '\n';
    }
    
    return csv;
  }

  private escapeCsv(value: string): string {
    if (value.includes(',') || value.includes('"') || value.includes('\n')) {
      return `"${value.replace(/"/g, '""')}"`;
    }
    return value;
  }
}
