/**
 * ATOM Logging Integration for SpiralSafe Operations API
 * Provides ATOM trail logging for Cloudflare Workers environment
 * 
 * ATOM: ATOM-INTEGRATION-20260119-001-api-logging
 */

/**
 * ATOMEntry interface for D1 database logging
 * Note: Intentionally duplicated from packages/atom-trail/types.ts
 * because Cloudflare Workers cannot import from workspace packages
 */
export interface ATOMEntry {
  timestamp: string;
  vortexId: string;
  decision: string;
  rationale: string;
  outcome: 'success' | 'failure' | 'pending';
  coherenceScore?: number;
  fibonacciWeight?: number;
  context: Record<string, unknown>;
  signature?: string;
  id?: string;
}

/**
 * Log an ATOM entry to the Cloudflare D1 database
 * This is a lightweight version for the Workers environment
 */
export async function logATOMToD1(
  db: D1Database,
  entry: Omit<ATOMEntry, 'timestamp' | 'id'>
): Promise<ATOMEntry> {
  const fullEntry: ATOMEntry = {
    ...entry,
    timestamp: new Date().toISOString(),
    id: crypto.randomUUID()
  };

  // Store in D1 for permanent audit trail
  await db.prepare(
    `INSERT INTO atom_trail (
      id, timestamp, vortex_id, decision, rationale, outcome, 
      coherence_score, fibonacci_weight, context, signature
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  )
    .bind(
      fullEntry.id,
      fullEntry.timestamp,
      fullEntry.vortexId,
      fullEntry.decision,
      fullEntry.rationale,
      fullEntry.outcome,
      fullEntry.coherenceScore ?? null,
      fullEntry.fibonacciWeight ?? null,
      JSON.stringify(fullEntry.context),
      fullEntry.signature ?? null
    )
    .run();

  return fullEntry;
}

/**
 * Query ATOM entries from D1
 */
export async function queryATOMFromD1(
  db: D1Database,
  filters: {
    vortexId?: string;
    outcome?: 'success' | 'failure' | 'pending';
    limit?: number;
    offset?: number;
  } = {}
): Promise<ATOMEntry[]> {
  let query = 'SELECT * FROM atom_trail';
  const conditions: string[] = [];
  const bindings: unknown[] = [];

  if (filters.vortexId) {
    conditions.push('vortex_id = ?');
    bindings.push(filters.vortexId);
  }

  if (filters.outcome) {
    conditions.push('outcome = ?');
    bindings.push(filters.outcome);
  }

  if (conditions.length > 0) {
    query += ' WHERE ' + conditions.join(' AND ');
  }

  query += ' ORDER BY timestamp DESC';

  if (filters.limit) {
    query += ' LIMIT ?';
    bindings.push(filters.limit);
  }

  if (filters.offset) {
    query += ' OFFSET ?';
    bindings.push(filters.offset);
  }

  const result = await db.prepare(query).bind(...bindings).all();

  return result.results.map((row: unknown) => {
    const r = row as Record<string, unknown>;
    return {
      id: r.id as string,
      timestamp: r.timestamp as string,
      vortexId: r.vortex_id as string,
      decision: r.decision as string,
      rationale: r.rationale as string,
      outcome: r.outcome as 'success' | 'failure' | 'pending',
      coherenceScore: r.coherence_score as number | undefined,
      fibonacciWeight: r.fibonacci_weight as number | undefined,
      context: JSON.parse(r.context as string) as Record<string, unknown>,
      signature: r.signature as string | undefined
    };
  });
}
