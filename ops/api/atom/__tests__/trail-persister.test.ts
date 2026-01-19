/**
 * ATOM Trail Persister Tests
 * Tests for foundational provenance logging system
 * 
 * ATOM: ATOM-TEST-20260119-001-atom-trail-persister-tests
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import {
  logATOM,
  queryATOM,
  exportATOM,
  visualizeATOM,
  getTrailStats,
  type ATOMEntry
} from '../trail-persister';

const TEST_TRAIL_PATH = path.join(process.cwd(), '.test-atom-trail.jsonl');

describe('ATOM Trail Persister', () => {
  beforeEach(() => {
    // Clean up test file before each test
    if (fs.existsSync(TEST_TRAIL_PATH)) {
      fs.unlinkSync(TEST_TRAIL_PATH);
    }
  });

  afterEach(() => {
    // Clean up test file after each test
    if (fs.existsSync(TEST_TRAIL_PATH)) {
      fs.unlinkSync(TEST_TRAIL_PATH);
    }
  });

  describe('logATOM', () => {
    it('should log a valid ATOM entry', async () => {
      const entry: ATOMEntry = {
        timestamp: new Date().toISOString(),
        vortexId: 'vortex-001',
        decision: 'Implement ATOM trail persister',
        rationale: 'Need provenance logging for all decisions',
        outcome: 'success',
        coherenceScore: 0.85,
        context: { pr: '123' }
      };

      await logATOM(entry, TEST_TRAIL_PATH);

      expect(fs.existsSync(TEST_TRAIL_PATH)).toBe(true);
      const content = fs.readFileSync(TEST_TRAIL_PATH, 'utf8');
      expect(content).toContain(entry.vortexId);
      expect(content).toContain(entry.decision);
    });

    it('should append multiple entries to the same file', async () => {
      const entries: ATOMEntry[] = [
        {
          timestamp: new Date().toISOString(),
          vortexId: 'vortex-001',
          decision: 'First decision',
          rationale: 'First rationale',
          outcome: 'success',
          context: {}
        },
        {
          timestamp: new Date().toISOString(),
          vortexId: 'vortex-001',
          decision: 'Second decision',
          rationale: 'Second rationale',
          outcome: 'pending',
          context: {}
        }
      ];

      for (const entry of entries) {
        await logATOM(entry, TEST_TRAIL_PATH);
      }

      const content = fs.readFileSync(TEST_TRAIL_PATH, 'utf8');
      const lines = content.trim().split('\n');
      expect(lines).toHaveLength(2);
    });
  });

  describe('queryATOM', () => {
    beforeEach(async () => {
      const entries: ATOMEntry[] = [
        {
          timestamp: '2026-01-19T10:00:00Z',
          vortexId: 'vortex-001',
          decision: 'Decision 1',
          rationale: 'Rationale 1',
          outcome: 'success',
          coherenceScore: 0.9,
          context: {}
        },
        {
          timestamp: '2026-01-19T11:00:00Z',
          vortexId: 'vortex-001',
          decision: 'Decision 2',
          rationale: 'Rationale 2',
          outcome: 'failure',
          coherenceScore: 0.5,
          context: {}
        },
        {
          timestamp: '2026-01-19T12:00:00Z',
          vortexId: 'vortex-002',
          decision: 'Decision 3',
          rationale: 'Rationale 3',
          outcome: 'pending',
          coherenceScore: 0.7,
          context: {}
        }
      ];

      for (const entry of entries) {
        await logATOM(entry, TEST_TRAIL_PATH);
      }
    });

    it('should return all entries when no filter is provided', async () => {
      const results = await queryATOM({}, TEST_TRAIL_PATH);
      expect(results).toHaveLength(3);
    });

    it('should filter by vortexId', async () => {
      const results = await queryATOM({ vortexId: 'vortex-001' }, TEST_TRAIL_PATH);
      expect(results).toHaveLength(2);
      expect(results.every(r => r.vortexId === 'vortex-001')).toBe(true);
    });

    it('should filter by outcome', async () => {
      const results = await queryATOM({ outcome: 'success' }, TEST_TRAIL_PATH);
      expect(results).toHaveLength(1);
      expect(results[0].outcome).toBe('success');
    });
  });

  describe('exportATOM', () => {
    beforeEach(async () => {
      const entry: ATOMEntry = {
        timestamp: '2026-01-19T10:00:00Z',
        vortexId: 'vortex-001',
        decision: 'Test decision',
        rationale: 'Test rationale',
        outcome: 'success',
        coherenceScore: 0.85,
        context: {}
      };
      await logATOM(entry, TEST_TRAIL_PATH);
    });

    it('should export as JSON', async () => {
      const exported = await exportATOM({ format: 'json' }, TEST_TRAIL_PATH);
      const parsed = JSON.parse(exported);
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed).toHaveLength(1);
    });
  });

  describe('visualizeATOM', () => {
    beforeEach(async () => {
      const entries: ATOMEntry[] = [
        {
          timestamp: '2026-01-19T10:00:00Z',
          vortexId: 'vortex-001',
          decision: 'Decision 1',
          rationale: 'Rationale 1',
          outcome: 'success',
          context: {}
        },
        {
          timestamp: '2026-01-19T11:00:00Z',
          vortexId: 'vortex-001',
          decision: 'Decision 2',
          rationale: 'Rationale 2',
          outcome: 'failure',
          context: {}
        }
      ];

      for (const entry of entries) {
        await logATOM(entry, TEST_TRAIL_PATH);
      }
    });

    it('should generate visualization data', async () => {
      const viz = await visualizeATOM('mermaid', {}, TEST_TRAIL_PATH);
      expect(viz.nodes.length).toBeGreaterThan(0);
      expect(viz.edges.length).toBeGreaterThan(0);
    });
  });

  describe('getTrailStats', () => {
    it('should return zero stats for empty trail', async () => {
      const stats = await getTrailStats(TEST_TRAIL_PATH);
      expect(stats.totalEntries).toBe(0);
      expect(stats.successCount).toBe(0);
    });
  });
});
