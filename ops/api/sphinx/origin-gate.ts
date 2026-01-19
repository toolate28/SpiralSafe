/**
 * SPHINX Gate 1: ORIGIN
 * 
 * Validates the source and provenance of an artifact
 * Question: "Where did this come from?"
 * 
 * ATOM: ATOM-FEATURE-20260119-002-sphinx-origin-gate
 */

import type { Artifact, GateResult, Evidence, SPHINXOptions } from './types';

export async function validateOrigin(
  artifact: Artifact,
  options?: SPHINXOptions
): Promise<GateResult> {
  const evidence: Evidence[] = [];
  let passed = true;
  const reasoning: string[] = [];

  // Check 1: Source repository/origin
  if (artifact.source) {
    evidence.push({
      type: 'source_present',
      description: 'Artifact has declared source',
      value: artifact.source,
      severity: 'info',
    });
    reasoning.push(`Source declared: ${artifact.source}`);
  } else {
    evidence.push({
      type: 'source_missing',
      description: 'Artifact has no declared source',
      value: null,
      severity: 'warning',
    });
    reasoning.push('No source declared - origin uncertain');
    passed = false;
  }

  // Check 2: Author identity
  if (artifact.author) {
    evidence.push({
      type: 'author_present',
      description: 'Artifact has declared author',
      value: artifact.author,
      severity: 'info',
    });
    reasoning.push(`Author: ${artifact.author}`);
  } else {
    evidence.push({
      type: 'author_missing',
      description: 'Artifact has no declared author',
      value: null,
      severity: 'warning',
    });
    reasoning.push('No author declared');
  }

  // Check 3: Digital signature (if present)
  if (artifact.signature) {
    // In a real implementation, we would verify the signature here
    // For now, we just check for presence
    evidence.push({
      type: 'signature_present',
      description: 'Artifact has digital signature',
      value: true,
      severity: 'info',
    });
    reasoning.push('Digital signature present (verification not implemented)');
  }

  // Check 4: ATOM trail reference
  const atomTrailRef = artifact.metadata?.atomTrail as string | undefined;
  if (atomTrailRef) {
    evidence.push({
      type: 'atom_trail_reference',
      description: 'Artifact references ATOM trail',
      value: atomTrailRef,
      severity: 'info',
    });
    reasoning.push(`ATOM trail reference: ${atomTrailRef}`);
  } else {
    evidence.push({
      type: 'atom_trail_missing',
      description: 'No ATOM trail reference',
      value: null,
      severity: 'info',
    });
  }

  return {
    passed,
    evidence,
    reasoning: reasoning.join('; '),
    timestamp: new Date().toISOString(),
    gateName: 'ORIGIN',
  };
}
