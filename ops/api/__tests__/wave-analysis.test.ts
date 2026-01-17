/**
 * Wave Analysis Tests
 * Tests for coherence analysis including positive and negative divergence detection
 * 
 * ATOM: ATOM-TEST-20260117-002-wave-analysis-negative-divergence
 */

import { describe, it, expect } from 'vitest';

// Mock the types from spiralsafe-worker.ts
interface WaveRegion {
  start: number;
  end: number;
  type: 'high_curl' | 'positive_divergence' | 'negative_divergence' | 'high_potential';
  severity: 'warning' | 'critical';
  description: string;
}

interface WaveAnalysis {
  curl: number;
  divergence: number;
  potential: number;
  regions: WaveRegion[];
  coherent: boolean;
}

// Helper functions copied from spiralsafe-worker.ts for testing
function detectRepetition(paragraphs: string[]): number {
  const phrases = paragraphs.flatMap(p => p.toLowerCase().split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 20));
  const unique = new Set(phrases);
  return phrases.length > 0 ? 1 - (unique.size / phrases.length) : 0;
}

function detectExpansion(paragraphs: string[]): number {
  // Returns positive values for unresolved expansion, negative for over-compression
  const text = paragraphs.join(' ');
  
  // Positive divergence indicators: content expands without concluding
  const hasConclusion = paragraphs.some(p => 
    /therefore|thus|in conclusion|finally|to summarize/i.test(p)
  );
  const questionCount = (text.match(/\?/g) || []).length;
  
  // Negative divergence indicators: premature closure / over-compression
  const conclusionCount = (text.match(/therefore|thus|in conclusion|finally|to summarize|in summary/gi) || []).length;
  const avgParagraphLength = text.length / Math.max(paragraphs.length, 1);
  const hasMultipleConclusionsShortContent = conclusionCount >= 2 && avgParagraphLength < 100;
  const excessiveSummarization = conclusionCount > paragraphs.length * 0.3;
  
  // Detect over-compression: multiple conclusions in short content or excessive summarization
  if (hasMultipleConclusionsShortContent || excessiveSummarization) {
    // Return negative value proportional to over-compression severity
    return -Math.min(0.3 + (conclusionCount * 0.15), 0.8);
  }
  
  // Positive divergence: unresolved expansion
  return hasConclusion ? 0.2 : Math.min(0.3 + (questionCount * 0.1), 0.8);
}

function detectPotential(paragraphs: string[]): number {
  const potentialMarkers = paragraphs.filter(p =>
    /could|might|perhaps|possibly|future work|TODO|TBD/i.test(p)
  ).length;
  return Math.min(potentialMarkers * 0.15, 1.0);
}

function analyzeCoherence(content: string, thresholds?: Record<string, number>): WaveAnalysis {
  const paragraphs = content.split(/\n\n+/);
  const t = {
    curl_warning: thresholds?.curl_warning ?? 0.3,
    curl_critical: thresholds?.curl_critical ?? 0.6,
    div_warning: thresholds?.div_warning ?? 0.4,
    div_critical: thresholds?.div_critical ?? 0.7,
  };

  const repetitionScore = detectRepetition(paragraphs);
  const expansionScore = detectExpansion(paragraphs);
  const potentialScore = detectPotential(paragraphs);

  const regions: WaveRegion[] = [];

  // Detect high-curl regions (repetition/circularity)
  if (repetitionScore > t.curl_warning) {
    regions.push({
      start: 0,
      end: content.length,
      type: 'high_curl',
      severity: repetitionScore > t.curl_critical ? 'critical' : 'warning',
      description: 'Detected circular or repetitive patterns'
    });
  }

  // Detect positive divergence regions (unresolved expansion)
  if (expansionScore > t.div_warning) {
    regions.push({
      start: 0,
      end: content.length,
      type: 'positive_divergence',
      severity: expansionScore > t.div_critical ? 'critical' : 'warning',
      description: 'Ideas expanding without resolution'
    });
  }

  // Detect negative divergence regions (premature closure/over-compression)
  if (expansionScore < -t.div_warning) {
    regions.push({
      start: 0,
      end: content.length,
      type: 'negative_divergence',
      severity: expansionScore < -t.div_critical ? 'critical' : 'warning',
      description: 'Premature closure or over-compression detected'
    });
  }

  return {
    curl: repetitionScore,
    divergence: expansionScore,
    potential: potentialScore,
    regions,
    coherent: repetitionScore < t.curl_critical && Math.abs(expansionScore) < t.div_critical
  };
}

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
