/**
 * SPHINX Gate 3: COHERENCE
 * 
 * Validates internal consistency using WAVE analysis
 * Question: "Does this make sense internally?"
 * 
 * ATOM: ATOM-FEATURE-20260119-004-sphinx-coherence-gate
 */

import type { Artifact, GateResult, Evidence, SPHINXOptions } from './types';

// Import WAVE analysis from worker (will be integrated)
// For now, we'll use a simplified version
interface WaveAnalysis {
  curl: number;
  divergence: number;
  potential: number;
  coherent: boolean;
  overall: number;
}

async function analyzeWAVE(content: string, threshold: number): Promise<WaveAnalysis> {
  // Simplified WAVE analysis
  // In production, this would call the full WAVE analysis from spiralsafe-worker
  
  const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
  
  // Calculate curl (repetition)
  const words = content.toLowerCase().split(/\s+/);
  const wordFreq = new Map<string, number>();
  for (const word of words) {
    if (word.length > 3) {
      wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
    }
  }
  const repetitionScore = Array.from(wordFreq.values())
    .filter(count => count > 2)
    .reduce((sum, count) => sum + (count - 2), 0);
  const curl = Math.min(1.0, repetitionScore / Math.max(1, words.length) * 10);
  
  // Calculate divergence (questions vs conclusions)
  const questions = (content.match(/\?/g) || []).length;
  const conclusions = (content.match(/\b(therefore|thus|in conclusion|to summarize|finally)\b/gi) || []).length;
  const divergence = (questions * 0.1) - (conclusions * 0.15);
  
  // Calculate potential (complexity)
  const avgSentenceLength = words.length / Math.max(1, sentences.length);
  const potential = Math.min(1.0, avgSentenceLength / 20);
  
  // Overall coherence score (0-100)
  const overall = Math.max(0, Math.min(100, 
    100 - (curl * 50) - (Math.abs(divergence) * 30) - (potential * 20)
  ));
  
  const coherent = overall >= threshold;
  
  return { curl, divergence, potential, coherent, overall };
}

export async function validateCoherence(
  artifact: Artifact,
  options?: SPHINXOptions
): Promise<GateResult> {
  const evidence: Evidence[] = [];
  const reasoning: string[] = [];
  
  const threshold = options?.coherenceThreshold || 80;
  const waveScore = await analyzeWAVE(artifact.content, threshold);
  
  evidence.push({
    type: 'wave_analysis',
    description: 'WAVE coherence analysis',
    value: waveScore,
    severity: 'info',
  });
  
  reasoning.push(`WAVE score: ${waveScore.overall.toFixed(1)} (threshold: ${threshold})`);
  
  // Check curl
  if (waveScore.curl > 0.4) {
    evidence.push({
      type: 'high_curl',
      description: 'High curl detected - circular reasoning or excessive repetition',
      value: waveScore.curl,
      severity: waveScore.curl > 0.6 ? 'critical' : 'warning',
    });
    reasoning.push(`High curl: ${waveScore.curl.toFixed(2)}`);
  }
  
  // Check divergence
  if (Math.abs(waveScore.divergence) > 0.4) {
    const divergenceType = waveScore.divergence > 0 ? 'positive' : 'negative';
    evidence.push({
      type: `${divergenceType}_divergence`,
      description: waveScore.divergence > 0 
        ? 'Ideas expanding without resolution'
        : 'Premature closure or over-compression',
      value: waveScore.divergence,
      severity: Math.abs(waveScore.divergence) > 0.6 ? 'critical' : 'warning',
    });
    reasoning.push(`${divergenceType} divergence: ${Math.abs(waveScore.divergence).toFixed(2)}`);
  }
  
  // Check potential
  if (waveScore.potential > 0.7) {
    evidence.push({
      type: 'high_potential',
      description: 'High complexity - may need simplification',
      value: waveScore.potential,
      severity: 'info',
    });
    reasoning.push(`High potential: ${waveScore.potential.toFixed(2)}`);
  }
  
  const passed = waveScore.overall >= threshold;
  
  if (!passed) {
    reasoning.push(`FAIL: Coherence score ${waveScore.overall.toFixed(1)} below threshold ${threshold}`);
  } else {
    reasoning.push('PASS: Coherence threshold met');
  }
  
  return {
    passed,
    evidence,
    reasoning: reasoning.join('; '),
    timestamp: new Date().toISOString(),
    gateName: 'COHERENCE',
  };
}
