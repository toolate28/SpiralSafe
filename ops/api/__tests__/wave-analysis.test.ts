/**
 * Wave Analysis Tests
 * Tests for coherence analysis including positive and negative divergence detection
 * 
 * ATOM: ATOM-TEST-20260117-002-wave-analysis-negative-divergence
 */

import { describe, it, expect } from 'vitest';
import { analyzeCoherence } from '../spiralsafe-worker';

describe('Wave Analysis - Divergence Detection', () => {
  describe('Positive Divergence (Unresolved Expansion)', () => {
    it('should detect positive divergence when content has many questions without conclusions', () => {
      const content = `What is the solution to this problem?

How should we implement this feature?

What are the alternatives?

What should we consider?`;

      const analysis = analyzeCoherence(content);
      
      expect(analysis.divergence).toBeGreaterThan(0);
      expect(analysis.regions.some(r => r.type === 'positive_divergence')).toBe(true);
      
      const positiveDivRegion = analysis.regions.find(r => r.type === 'positive_divergence');
      expect(positiveDivRegion).toBeDefined();
      expect(positiveDivRegion?.description).toContain('expanding without resolution');
    });

    it('should have low positive divergence when content has proper conclusions', () => {
      const content = `What is the solution to this problem?

After careful analysis, we determined the best approach.

Therefore, we recommend implementing feature X with the following strategy.

In conclusion, this solution addresses all requirements.`;

      const analysis = analyzeCoherence(content);
      
      expect(analysis.divergence).toBeLessThanOrEqual(0.3);
      expect(analysis.regions.some(r => r.type === 'positive_divergence')).toBe(false);
    });
  });

  describe('Negative Divergence (Premature Closure/Over-Compression)', () => {
    it('should detect negative divergence when content has excessive conclusions in short text', () => {
      const content = `Brief intro. Therefore, we conclude. Thus, the summary. In conclusion, done.`;

      const analysis = analyzeCoherence(content);
      
      expect(analysis.divergence).toBeLessThan(0);
      expect(analysis.regions.some(r => r.type === 'negative_divergence')).toBe(true);
      
      const negativeDivRegion = analysis.regions.find(r => r.type === 'negative_divergence');
      expect(negativeDivRegion).toBeDefined();
      expect(negativeDivRegion?.description).toContain('Premature closure or over-compression');
    });

    it('should detect critical negative divergence for heavily over-compressed content', () => {
      const content = `Start. Therefore A. Thus B. In conclusion C. Finally D. To summarize E.`;

      const analysis = analyzeCoherence(content);
      
      expect(analysis.divergence).toBeLessThan(-0.4);
      expect(analysis.regions.some(r => r.type === 'negative_divergence' && r.severity === 'critical')).toBe(true);
    });

    it('should not detect negative divergence for properly balanced content', () => {
      const content = `This is the introduction explaining the problem in detail.

We explored several approaches and considered multiple factors.

The analysis revealed important insights about the system behavior.

After thorough evaluation, we recommend the following approach.

Therefore, this solution provides the best balance of all requirements.`;

      const analysis = analyzeCoherence(content);
      
      expect(analysis.divergence).toBeGreaterThanOrEqual(-0.4);
      expect(analysis.regions.some(r => r.type === 'negative_divergence')).toBe(false);
    });
  });

  describe('Balanced Content (No Divergence Issues)', () => {
    it('should not flag divergence for well-structured content', () => {
      const content = `This document explains the wave protocol coherence analysis.

The protocol measures curl, divergence, and potential in text.

Curl represents circular reasoning patterns in the content.

Divergence shows expansion or compression of ideas.

Potential indicates areas for future development.

In summary, these metrics help maintain document quality.`;

      const analysis = analyzeCoherence(content);
      
      expect(Math.abs(analysis.divergence)).toBeLessThanOrEqual(0.4);
      expect(analysis.regions.filter(r => r.type.includes('divergence'))).toHaveLength(0);
      expect(analysis.coherent).toBe(true);
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty content gracefully', () => {
      const analysis = analyzeCoherence('');
      
      expect(analysis.divergence).toBeDefined();
      expect(analysis.regions).toEqual([]);
    });

    it('should handle single sentence content', () => {
      const analysis = analyzeCoherence('This is a single sentence.');
      
      expect(analysis.divergence).toBeDefined();
      expect(analysis.coherent).toBe(true);
    });

    it('should handle content with only questions', () => {
      const content = 'Why? How? What? When? Where?';
      
      const analysis = analyzeCoherence(content);
      
      expect(analysis.divergence).toBeGreaterThan(0);
    });
  });

  describe('High Curl Detection (Existing Functionality)', () => {
    it('should detect high curl for repetitive content', () => {
      const content = `This is a repeated concept that appears multiple times.

This is a repeated concept that appears multiple times.

This is a repeated concept that appears multiple times.`;

      const analysis = analyzeCoherence(content);
      
      expect(analysis.curl).toBeGreaterThan(0.3);
      expect(analysis.regions.some(r => r.type === 'high_curl')).toBe(true);
    });
  });
});
