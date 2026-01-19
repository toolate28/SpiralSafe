/**
 * ATOM Trail Persister Tests
 * Unit tests for the ATOM logging system
 * 
 * ATOM: ATOM-TEST-20260119-001-trail-persister-tests
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import {
  logATOM,
  queryATOM,
  visualizeATOM,
  exportATOM,
  getATOMStats,
  generateMermaidDiagram
} from '../trail-persister.js';
import { ATOMEntry } from '../types.js';

const TEST_TRAIL_PATH = '/tmp/test-atom-trail.jsonl';

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
    it('should log an ATOM entry with timestamp and ID', async () => {
      const entry = {
        vortexId: 'test-vortex',
        decision: 'Test decision',
        rationale: 'Testing the ATOM logger',
        outcome: 'success' as const,
        context: { test: true }
      };

      const logged = await logATOM(entry, TEST_TRAIL_PATH);

      expect(logged.timestamp).toBeDefined();
      expect(logged.id).toBeDefined();
      expect(logged.vortexId).toBe('test-vortex');
      expect(logged.decision).toBe('Test decision');
      expect(logged.outcome).toBe('success');
    });

    it('should append multiple entries to the trail', async () => {
      await logATOM({
        vortexId: 'vortex-1',
        decision: 'First decision',
        rationale: 'First rationale',
        outcome: 'success',
        context: {}
      }, TEST_TRAIL_PATH);

      await logATOM({
        vortexId: 'vortex-2',
        decision: 'Second decision',
        rationale: 'Second rationale',
        outcome: 'failure',
        context: {}
      }, TEST_TRAIL_PATH);

      const entries = await queryATOM({}, TEST_TRAIL_PATH);
      expect(entries.length).toBe(2);
    });

    it('should include coherence score when provided', async () => {
      const entry = {
        vortexId: 'wave-validator',
        decision: 'Document coherence check',
        rationale: 'Validating documentation',
        outcome: 'success' as const,
        coherenceScore: 0.85,
        context: { documentPath: '/test/doc.md' }
      };

      const logged = await logATOM(entry, TEST_TRAIL_PATH);
      expect(logged.coherenceScore).toBe(0.85);
    });

    it('should include fibonacci weight when provided', async () => {
      const entry = {
        vortexId: 'task-manager',
        decision: 'Prioritize task',
        rationale: 'High priority task',
        outcome: 'pending' as const,
        fibonacciWeight: 8,
        context: { taskId: 'task-123' }
      };

      const logged = await logATOM(entry, TEST_TRAIL_PATH);
      expect(logged.fibonacciWeight).toBe(8);
    });
  });

  describe('queryATOM', () => {
    beforeEach(async () => {
      // Set up test data
      await logATOM({
        vortexId: 'vortex-1',
        decision: 'Decision 1',
        rationale: 'Rationale 1',
        outcome: 'success',
        coherenceScore: 0.9,
        context: {}
      }, TEST_TRAIL_PATH);

      await logATOM({
        vortexId: 'vortex-1',
        decision: 'Decision 2',
        rationale: 'Rationale 2',
        outcome: 'failure',
        coherenceScore: 0.4,
        context: {}
      }, TEST_TRAIL_PATH);

      await logATOM({
        vortexId: 'vortex-2',
        decision: 'Decision 3',
        rationale: 'Rationale 3',
        outcome: 'success',
        coherenceScore: 0.7,
        context: {}
      }, TEST_TRAIL_PATH);
    });

    it('should query all entries when no filters provided', async () => {
      const entries = await queryATOM({}, TEST_TRAIL_PATH);
      expect(entries.length).toBe(3);
    });

    it('should filter by vortexId', async () => {
      const entries = await queryATOM({ vortexId: 'vortex-1' }, TEST_TRAIL_PATH);
      expect(entries.length).toBe(2);
      expect(entries.every(e => e.vortexId === 'vortex-1')).toBe(true);
    });

    it('should filter by outcome', async () => {
      const entries = await queryATOM({ outcome: 'success' }, TEST_TRAIL_PATH);
      expect(entries.length).toBe(2);
      expect(entries.every(e => e.outcome === 'success')).toBe(true);
    });

    it('should filter by minimum coherence score', async () => {
      const entries = await queryATOM({ minCoherence: 0.7 }, TEST_TRAIL_PATH);
      expect(entries.length).toBe(2);
      expect(entries.every(e => e.coherenceScore && e.coherenceScore >= 0.7)).toBe(true);
    });

    it('should filter by maximum coherence score', async () => {
      const entries = await queryATOM({ maxCoherence: 0.5 }, TEST_TRAIL_PATH);
      expect(entries.length).toBe(1);
      expect(entries[0].coherenceScore).toBe(0.4);
    });

    it('should support pagination with limit and offset', async () => {
      const page1 = await queryATOM({ limit: 2, offset: 0 }, TEST_TRAIL_PATH);
      expect(page1.length).toBe(2);

      const page2 = await queryATOM({ limit: 2, offset: 2 }, TEST_TRAIL_PATH);
      expect(page2.length).toBe(1);
    });

    it('should return empty array for non-existent trail', async () => {
      const entries = await queryATOM({}, '/tmp/nonexistent-trail.jsonl');
      expect(entries).toEqual([]);
    });
  });

  describe('visualizeATOM', () => {
    it('should create a graph structure for a vortex', async () => {
      await logATOM({
        vortexId: 'test-vortex',
        decision: 'Root decision',
        rationale: 'Starting point',
        outcome: 'success',
        context: {}
      }, TEST_TRAIL_PATH);

      const graph = await visualizeATOM('test-vortex', TEST_TRAIL_PATH);
      expect(graph.vortexId).toBe('test-vortex');
      expect(graph.nodes.size).toBe(1);
      expect(graph.roots.length).toBe(1);
    });

    it('should link parent-child relationships', async () => {
      const parent = await logATOM({
        vortexId: 'test-vortex',
        decision: 'Parent decision',
        rationale: 'Parent rationale',
        outcome: 'success',
        context: {}
      }, TEST_TRAIL_PATH);

      await logATOM({
        vortexId: 'test-vortex',
        decision: 'Child decision',
        rationale: 'Child rationale',
        outcome: 'success',
        context: { parentId: parent.id }
      }, TEST_TRAIL_PATH);

      const graph = await visualizeATOM('test-vortex', TEST_TRAIL_PATH);
      expect(graph.nodes.size).toBe(2);
      
      const parentNode = Array.from(graph.nodes.values()).find(
        n => n.entry.decision === 'Parent decision'
      );
      expect(parentNode?.children.length).toBe(1);
    });
  });

  describe('exportATOM', () => {
    beforeEach(async () => {
      await logATOM({
        vortexId: 'test',
        decision: 'Test decision',
        rationale: 'Test rationale',
        outcome: 'success',
        coherenceScore: 0.85,
        fibonacciWeight: 5,
        context: { key: 'value' }
      }, TEST_TRAIL_PATH);
    });

    it('should export as JSON', async () => {
      const json = await exportATOM('json', {}, TEST_TRAIL_PATH);
      const parsed = JSON.parse(json);
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed.length).toBe(1);
      expect(parsed[0].decision).toBe('Test decision');
    });

    it('should export as CSV', async () => {
      const csv = await exportATOM('csv', {}, TEST_TRAIL_PATH);
      expect(csv).toContain('timestamp,vortexId,decision,outcome');
      expect(csv).toContain('Test decision');
      expect(csv).toContain('success');
    });

    it('should export as Markdown', async () => {
      const md = await exportATOM('markdown', {}, TEST_TRAIL_PATH);
      expect(md).toContain('# ATOM Trail Export');
      expect(md).toContain('Test decision');
      expect(md).toContain('Test rationale');
      expect(md).toContain('85.0%');
    });

    it('should apply filters when exporting', async () => {
      await logATOM({
        vortexId: 'other',
        decision: 'Other decision',
        rationale: 'Other rationale',
        outcome: 'failure',
        context: {}
      }, TEST_TRAIL_PATH);

      const json = await exportATOM('json', { outcome: 'success' }, TEST_TRAIL_PATH);
      const parsed = JSON.parse(json);
      expect(parsed.length).toBe(1);
      expect(parsed[0].outcome).toBe('success');
    });
  });

  describe('getATOMStats', () => {
    beforeEach(async () => {
      await logATOM({
        vortexId: 'vortex-1',
        decision: 'Decision 1',
        rationale: 'Rationale 1',
        outcome: 'success',
        coherenceScore: 0.9,
        context: {}
      }, TEST_TRAIL_PATH);

      await logATOM({
        vortexId: 'vortex-1',
        decision: 'Decision 2',
        rationale: 'Rationale 2',
        outcome: 'failure',
        coherenceScore: 0.4,
        context: {}
      }, TEST_TRAIL_PATH);

      await logATOM({
        vortexId: 'vortex-2',
        decision: 'Decision 3',
        rationale: 'Rationale 3',
        outcome: 'pending',
        coherenceScore: 0.7,
        context: {}
      }, TEST_TRAIL_PATH);
    });

    it('should calculate statistics correctly', async () => {
      const stats = await getATOMStats(TEST_TRAIL_PATH);
      
      expect(stats.totalEntries).toBe(3);
      expect(stats.successCount).toBe(1);
      expect(stats.failureCount).toBe(1);
      expect(stats.pendingCount).toBe(1);
      expect(stats.avgCoherenceScore).toBeCloseTo(0.6667, 2);
      expect(stats.vortexBreakdown).toEqual({
        'vortex-1': 2,
        'vortex-2': 1
      });
      expect(stats.timeRange.earliest).toBeDefined();
      expect(stats.timeRange.latest).toBeDefined();
    });

    it('should handle empty trail', async () => {
      const stats = await getATOMStats('/tmp/empty-trail.jsonl');
      expect(stats.totalEntries).toBe(0);
      expect(stats.avgCoherenceScore).toBe(0);
    });
  });

  describe('generateMermaidDiagram', () => {
    it('should generate Mermaid syntax for a graph', async () => {
      const parent = await logATOM({
        vortexId: 'test',
        decision: 'Parent decision with a very long name',
        rationale: 'Parent',
        outcome: 'success',
        coherenceScore: 0.85,
        context: {}
      }, TEST_TRAIL_PATH);

      await logATOM({
        vortexId: 'test',
        decision: 'Child decision',
        rationale: 'Child',
        outcome: 'failure',
        coherenceScore: 0.4,
        context: { parentId: parent.id }
      }, TEST_TRAIL_PATH);

      const graph = await visualizeATOM('test', TEST_TRAIL_PATH);
      const mermaid = generateMermaidDiagram(graph);

      expect(mermaid).toContain('graph TD');
      expect(mermaid).toContain('✓');
      expect(mermaid).toContain('✗');
      expect(mermaid).toContain('85%');
      expect(mermaid).toContain('40%');
      expect(mermaid).toContain('-->');
    });
  });

  describe('Performance', () => {
    it('should handle 1000+ entries efficiently', async () => {
      const startTime = Date.now();
      
      // Log 1000 entries
      for (let i = 0; i < 1000; i++) {
        await logATOM({
          vortexId: `vortex-${i % 10}`,
          decision: `Decision ${i}`,
          rationale: `Rationale ${i}`,
          outcome: i % 3 === 0 ? 'success' : i % 3 === 1 ? 'failure' : 'pending',
          coherenceScore: Math.random(),
          context: { index: i }
        }, TEST_TRAIL_PATH);
      }
      
      // Query should be fast
      const queryStart = Date.now();
      const entries = await queryATOM({ vortexId: 'vortex-5' }, TEST_TRAIL_PATH);
      const queryTime = Date.now() - queryStart;
      
      expect(entries.length).toBe(100);
      expect(queryTime).toBeLessThan(100); // Should be less than 100ms
      
      const totalTime = Date.now() - startTime;
      console.log(`Performance test: ${totalTime}ms for 1000 entries`);
    });
  });
});
