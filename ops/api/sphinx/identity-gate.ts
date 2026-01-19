/**
 * SPHINX Gate 4: IDENTITY
 * 
 * Validates that artifact matches its declared type
 * Question: "Is this what it claims to be?"
 * 
 * ATOM: ATOM-FEATURE-20260119-005-sphinx-identity-gate
 */

import type { Artifact, GateResult, Evidence, SPHINXOptions } from './types';

export async function validateIdentity(
  artifact: Artifact,
  _options?: SPHINXOptions
): Promise<GateResult> {
  const evidence: Evidence[] = [];
  let passed = true;
  const reasoning: string[] = [];

  // Check 1: Type declaration
  const declaredType = artifact.type;
  if (!declaredType) {
    evidence.push({
      type: 'type_missing',
      description: 'No declared type',
      value: null,
      severity: 'critical',
    });
    reasoning.push('FAIL: No type declared');
    passed = false;
    
    return {
      passed,
      evidence,
      reasoning: reasoning.join('; '),
      timestamp: new Date().toISOString(),
      gateName: 'IDENTITY',
    };
  }

  evidence.push({
    type: 'type_declared',
    description: 'Artifact declares its type',
    value: declaredType,
    severity: 'info',
  });
  reasoning.push(`Declared type: ${declaredType}`);

  // Check 2: Content matches type
  const content = artifact.content;
  const typeValidations: Record<string, (content: string) => boolean> = {
    markdown: (c) => /^#|\n#|^-|\n-|\[.*\]\(.*\)/.test(c),
    json: (c) => {
      try {
        JSON.parse(c);
        return true;
      } catch {
        return false;
      }
    },
    yaml: (c) => /^[\w-]+:\s|^\s+-\s/.test(c),
    typescript: (c) => /\bfunction\b|\bconst\b|\blet\b|\binterface\b|\btype\b/.test(c),
    javascript: (c) => /\bfunction\b|\bconst\b|\blet\b|\bvar\b/.test(c),
    python: (c) => /\bdef\b|\bclass\b|\bimport\b/.test(c),
    html: (c) => /<[a-z][\s\S]*>/i.test(c),
  };

  const normalizedType = declaredType.toLowerCase().replace(/[^a-z]/g, '');
  const validator = typeValidations[normalizedType];
  
  if (validator) {
    const matches = validator(content);
    if (matches) {
      evidence.push({
        type: 'type_content_match',
        description: 'Content matches declared type',
        value: true,
        severity: 'info',
      });
      reasoning.push('Content structure matches declared type');
    } else {
      evidence.push({
        type: 'type_content_mismatch',
        description: 'Content does not match declared type',
        value: false,
        severity: 'warning',
      });
      reasoning.push('WARNING: Content structure inconsistent with declared type');
    }
  } else {
    evidence.push({
      type: 'type_validation_unavailable',
      description: 'No validator available for this type',
      value: declaredType,
      severity: 'info',
    });
  }

  // Check 3: Metadata consistency
  const expectedFields = artifact.metadata?.expectedFields as string[] | undefined;
  if (expectedFields) {
    const missingFields = expectedFields.filter(field => !(field in artifact.metadata!));
    if (missingFields.length > 0) {
      evidence.push({
        type: 'missing_metadata_fields',
        description: 'Expected metadata fields are missing',
        value: missingFields,
        severity: 'warning',
      });
      reasoning.push(`Missing fields: ${missingFields.join(', ')}`);
    } else {
      evidence.push({
        type: 'metadata_complete',
        description: 'All expected metadata fields present',
        value: true,
        severity: 'info',
      });
      reasoning.push('Metadata complete');
    }
  }

  // Check 4: Interface contracts (if specified)
  const requiredInterface = artifact.metadata?.requiredInterface as Record<string, string> | undefined;
  if (requiredInterface) {
    const interfaceChecks: string[] = [];
    for (const [method, _signature] of Object.entries(requiredInterface)) {
      const regex = new RegExp(`\\b${method}\\s*[(:=]`, 'i');
      if (regex.test(content)) {
        interfaceChecks.push(`${method}: found`);
      } else {
        interfaceChecks.push(`${method}: MISSING`);
        passed = false;
      }
    }
    
    evidence.push({
      type: 'interface_contract_check',
      description: 'Required interface contract validation',
      value: interfaceChecks,
      severity: passed ? 'info' : 'critical',
    });
    reasoning.push(`Interface checks: ${interfaceChecks.join(', ')}`);
  }

  return {
    passed,
    evidence,
    reasoning: reasoning.join('; '),
    timestamp: new Date().toISOString(),
    gateName: 'IDENTITY',
  };
}
