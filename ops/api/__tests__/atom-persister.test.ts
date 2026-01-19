/**
 * ATOM Persister Tests
 * Tests for Auditable Trail of Metadata persistence layer
 * 
 * ATOM: ATOM-TEST-20260119-001-atom-persister-tests
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { ATOMPersister } from '../atom-persister';

// Mock D1Database and KVNamespace
interface MockD1Result {
  results: Record<string, unknown>[];
  success: boolean;
  meta: Record<string, unknown>;
}

interface MockD1PreparedStatement {
  bind(...values: unknown[]): MockD1PreparedStatement;
  first(): Promise<Record<string, unknown> | null>;
  run(): Promise<MockD1Result>;
  all(): Promise<MockD1Result>;
}

class MockD1Database {
  private data: Map<string, Record<string, unknown>[]> = new Map();

  private extractTable(sql: string): string {
    const match = sql.match(/(?:FROM|INTO)\s+(\w+)/i);
    return match ? match[1] : 'atom_entries';
  }

  prepare(query: string): MockD1PreparedStatement {
    const bindings: unknown[] = [];
    const self = this;

    return {
      bind(...values: unknown[]) {
        bindings.push(...values);
        return this;
      },
      async first() {
        // Simplified mock - would need full SQL parser for production
        if (query.includes('SELECT')) {
          const table = self.extractTable(query);
          const rows = self.data.get(table) || [];
          return rows[0] || null;
        }
        return null;
      },
      async run() {
        if (query.includes('INSERT INTO atom_entries')) {
          const table = 'atom_entries';
          if (!self.data.has(table)) {
            self.data.set(table, []);
          }
          const rows = self.data.get(table)!;
          const row: Record<string, unknown> = {
            id: bindings[0],
            timestamp: bindings[1],
            actor: bindings[2],
            decision: bindings[3],
            rationale: bindings[4],
            outcome: bindings[5],
            coherence_score: bindings[6],
            context: bindings[7],
            parent_entry: bindings[8],
            vortex_state: bindings[9],
            hash: bindings[10],
            previous_hash: bindings[11],
            signature: bindings[12],
          };
          rows.push(row);
        }
        return { results: [], success: true, meta: {} };
      },
      async all() {
        const table = self.extractTable(query);
        const rows = self.data.get(table) || [];
        return { results: rows, success: true, meta: {} };
      },
    };
  }

  getData(table: string): Record<string, unknown>[] {
    return this.data.get(table) || [];
  }

  clearData(): void {
    this.data.clear();
  }
}

class MockKVNamespace {
  private data: Map<string, string> = new Map();

  async get(key: string): Promise<string | null> {
    return this.data.get(key) || null;
  }

  async put(key: string, value: string, _options?: { expirationTtl?: number }): Promise<void> {
    this.data.set(key, value);
  }

  async list(options?: { prefix?: string }): Promise<{ keys: { name: string }[] }> {
    const prefix = options?.prefix || '';
    const keys = Array.from(this.data.keys())
      .filter(key => key.startsWith(prefix))
      .map(name => ({ name }));
    return { keys };
  }

  clearData(): void {
    this.data.clear();
  }
}

describe('ATOMPersister', () => {
  let mockDb: MockD1Database;
  let mockKv: MockKVNamespace;
  let persister: ATOMPersister;

  beforeEach(() => {
    mockDb = new MockD1Database();
    mockKv = new MockKVNamespace();
    persister = new ATOMPersister('sqlite', mockDb as unknown as D1Database, mockKv as unknown as KVNamespace);
  });

  describe('log', () => {
    it('should log a decision with all required fields', async () => {
      const entryId = await persister.log({
        actor: 'test-actor',
        decision: 'Test decision',
        rationale: 'Test rationale',
        outcome: 'SUCCESS',
        context: { test: true },
      });

      expect(entryId).toBeDefined();
      expect(typeof entryId).toBe('string');

      const entries = mockDb.getData('atom_entries');
      expect(entries).toHaveLength(1);
      expect(entries[0].actor).toBe('test-actor');
      expect(entries[0].decision).toBe('Test decision');
      expect(entries[0].outcome).toBe('SUCCESS');
    });

    it('should generate unique IDs for each entry', async () => {
      const id1 = await persister.log({
        actor: 'actor1',
        decision: 'Decision 1',
        rationale: 'Rationale 1',
        outcome: 'PASS',
        context: {},
      });

      const id2 = await persister.log({
        actor: 'actor2',
        decision: 'Decision 2',
        rationale: 'Rationale 2',
        outcome: 'FAIL',
        context: {},
      });

      expect(id1).not.toBe(id2);
    });

    it('should include coherence score when provided', async () => {
      await persister.log({
        actor: 'wave-validator',
        decision: 'Coherence check',
        rationale: 'Threshold validation',
        outcome: 'PASS',
        coherenceScore: 0.85,
        context: {},
      });

      const entries = mockDb.getData('atom_entries');
      expect(entries[0].coherence_score).toBe(0.85);
    });

    it('should link to parent entry when provided', async () => {
      const parentId = await persister.log({
        actor: 'actor1',
        decision: 'Parent decision',
        rationale: 'Initial decision',
        outcome: 'PASS',
        context: {},
      });

      await persister.log({
        actor: 'actor2',
        decision: 'Child decision',
        rationale: 'Follow-up decision',
        outcome: 'PASS',
        context: {},
        parentEntry: parentId,
      });

      const entries = mockDb.getData('atom_entries');
      expect(entries).toHaveLength(2);
      expect(entries[1].parent_entry).toBe(parentId);
    });

    it('should calculate hash for integrity', async () => {
      await persister.log({
        actor: 'test-actor',
        decision: 'Test decision',
        rationale: 'Test rationale',
        outcome: 'SUCCESS',
        context: {},
      });

      const entries = mockDb.getData('atom_entries');
      expect(entries[0].hash).toBeDefined();
      expect(typeof entries[0].hash).toBe('string');
      expect((entries[0].hash as string).length).toBe(64); // SHA-256 hex length
    });

    it('should chain previous hash', async () => {
      await persister.log({
        actor: 'actor1',
        decision: 'First decision',
        rationale: 'First',
        outcome: 'PASS',
        context: {},
      });

      await persister.log({
        actor: 'actor2',
        decision: 'Second decision',
        rationale: 'Second',
        outcome: 'PASS',
        context: {},
      });

      const entries = mockDb.getData('atom_entries');
      expect(entries).toHaveLength(2);
      expect(entries[1].previous_hash).toBe(entries[0].hash);
    });
  });

  describe('query', () => {
    beforeEach(async () => {
      // Populate test data
      await persister.log({
        actor: 'claude',
        decision: 'Architecture design',
        rationale: 'Initial design',
        outcome: 'COMPLETE',
        coherenceScore: 0.9,
        context: { phase: 'planning' },
      });

      await persister.log({
        actor: 'copilot',
        decision: 'Code formatting',
        rationale: 'Style consistency',
        outcome: 'COMPLETE',
        coherenceScore: 0.95,
        context: { phase: 'implementation' },
      });

      await persister.log({
        actor: 'claude',
        decision: 'Documentation update',
        rationale: 'Reflect changes',
        outcome: 'COMPLETE',
        coherenceScore: 0.85,
        context: { phase: 'documentation' },
      });
    });

    it('should query all entries when no filter provided', async () => {
      const entries = await persister.query({});
      expect(entries.length).toBeGreaterThan(0);
    });

    it('should filter by actor', async () => {
      const entries = await persister.query({ actor: 'claude' });
      expect(entries.length).toBeGreaterThanOrEqual(2);
      entries.forEach(entry => {
        expect(entry.actor).toBe('claude');
      });
    });

    it('should respect limit parameter', async () => {
      const entries = await persister.query({ limit: 2 });
      expect(entries.length).toBeLessThanOrEqual(2);
    });
  });

  describe('getChain', () => {
    it('should retrieve full decision chain', async () => {
      const id1 = await persister.log({
        actor: 'actor1',
        decision: 'Root decision',
        rationale: 'Starting point',
        outcome: 'PASS',
        context: {},
      });

      const id2 = await persister.log({
        actor: 'actor2',
        decision: 'Second decision',
        rationale: 'Building on root',
        outcome: 'PASS',
        context: {},
        parentEntry: id1,
      });

      const id3 = await persister.log({
        actor: 'actor3',
        decision: 'Third decision',
        rationale: 'Final step',
        outcome: 'PASS',
        context: {},
        parentEntry: id2,
      });

      const chain = await persister.getChain(id3);

      expect(chain.entries).toHaveLength(3);
      expect(chain.depth).toBe(3);
      expect(chain.root.id).toBe(id1);
      expect(chain.entries[0].id).toBe(id1);
      expect(chain.entries[1].id).toBe(id2);
      expect(chain.entries[2].id).toBe(id3);
    });

    it('should validate chain integrity', async () => {
      const id1 = await persister.log({
        actor: 'actor1',
        decision: 'First',
        rationale: 'First',
        outcome: 'PASS',
        context: {},
      });

      const id2 = await persister.log({
        actor: 'actor2',
        decision: 'Second',
        rationale: 'Second',
        outcome: 'PASS',
        context: {},
        parentEntry: id1,
      });

      const chain = await persister.getChain(id2);
      expect(chain.integrityValid).toBe(true);
    });
  });

  describe('verify', () => {
    it('should verify intact trail', async () => {
      await persister.log({
        actor: 'actor1',
        decision: 'Test 1',
        rationale: 'Test',
        outcome: 'PASS',
        context: {},
      });

      await persister.log({
        actor: 'actor2',
        decision: 'Test 2',
        rationale: 'Test',
        outcome: 'PASS',
        context: {},
      });

      const verification = await persister.verify();
      expect(verification.valid).toBe(true);
      expect(verification.totalEntries).toBe(2);
      expect(verification.brokenChains).toBe(0);
      expect(verification.tamperedEntries).toHaveLength(0);
    });
  });

  describe('export', () => {
    beforeEach(async () => {
      await persister.log({
        actor: 'test-actor',
        decision: 'Test decision',
        rationale: 'Test rationale',
        outcome: 'SUCCESS',
        context: { key: 'value' },
      });
    });

    it('should export to markdown format', async () => {
      const entries = await persister.query({});
      const markdown = persister.export(entries, 'markdown');

      expect(markdown).toContain('# ATOM Trail Timeline');
      expect(markdown).toContain('Test decision');
      expect(markdown).toContain('test-actor');
      expect(markdown).toContain('SUCCESS');
    });

    it('should export to JSON format', async () => {
      const entries = await persister.query({});
      const json = persister.export(entries, 'json');

      expect(() => JSON.parse(json)).not.toThrow();
      const parsed = JSON.parse(json);
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed[0].decision).toBe('Test decision');
    });

    it('should export to CSV format', async () => {
      const entries = await persister.query({});
      const csv = persister.export(entries, 'csv');

      expect(csv).toContain('id,timestamp,actor,decision');
      expect(csv).toContain('test-actor');
      expect(csv).toContain('Test decision');
    });

    it('should escape CSV values with commas', async () => {
      await persister.log({
        actor: 'actor',
        decision: 'Decision with, comma',
        rationale: 'Rationale',
        outcome: 'SUCCESS',
        context: {},
      });

      const entries = await persister.query({});
      const csv = persister.export(entries, 'csv');

      expect(csv).toContain('"Decision with, comma"');
    });
  });

  describe('integration scenarios', () => {
    it('should track WAVE validation workflow', async () => {
      await persister.log({
        actor: 'wave-validator',
        decision: 'Analyzed content coherence',
        rationale: 'Threshold check: curl=0.2, divergence=0.1',
        outcome: 'PASS',
        coherenceScore: 0.3,
        context: {
          curl: 0.2,
          divergence: 0.1,
          potential: 0.5,
        },
      });

      const entries = await persister.query({ actor: 'wave-validator' });
      expect(entries).toHaveLength(1);
      expect(entries[0].coherenceScore).toBe(0.3);
      expect(entries[0].context).toHaveProperty('curl');
    });

    it('should track H&&S handoff workflow', async () => {
      await persister.log({
        actor: 'claude',
        decision: 'H&&S:PASS to copilot',
        rationale: 'Architecture complete',
        outcome: 'Context transferred',
        context: {
          handoffType: 'PASS',
          nextAgent: 'copilot',
          bumpId: 'test-bump-123',
        },
      });

      const entries = await persister.query({ actor: 'claude' });
      expect(entries).toHaveLength(1);
      expect(entries[0].decision).toContain('H&&S:PASS');
      expect(entries[0].context).toHaveProperty('nextAgent', 'copilot');
    });

    it('should track multi-agent collaboration chain', async () => {
      const id1 = await persister.log({
        actor: 'claude',
        decision: 'Design architecture',
        rationale: 'Initial planning',
        outcome: 'COMPLETE',
        context: {},
      });

      const id2 = await persister.log({
        actor: 'copilot',
        decision: 'Implement features',
        rationale: 'Following design',
        outcome: 'COMPLETE',
        context: {},
        parentEntry: id1,
      });

      const id3 = await persister.log({
        actor: 'human',
        decision: 'Review and approve',
        rationale: 'Quality check',
        outcome: 'APPROVED',
        context: {},
        parentEntry: id2,
      });

      const chain = await persister.getChain(id3);
      expect(chain.entries).toHaveLength(3);
      expect(chain.entries.map(e => e.actor)).toEqual(['claude', 'copilot', 'human']);
    });
  });
});
