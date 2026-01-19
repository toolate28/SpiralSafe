/**
 * SPHINX Gate 2: INTENT
 * 
 * Validates that declared purpose matches actual behavior
 * Question: "What is this trying to do?"
 * 
 * ATOM: ATOM-FEATURE-20260119-003-sphinx-intent-gate
 */

import type { Artifact, GateResult, Evidence, SPHINXOptions } from './types';

export async function validateIntent(
  artifact: Artifact,
  _options?: SPHINXOptions
): Promise<GateResult> {
  const evidence: Evidence[] = [];
  let passed = true;
  const reasoning: string[] = [];

  // Check 1: Intent declaration
  const declaredIntent = artifact.metadata?.intent as string | undefined;
  if (!declaredIntent) {
    evidence.push({
      type: 'intent_missing',
      description: 'No declared intent found',
      value: null,
      severity: 'critical',
    });
    reasoning.push('FAIL: No declared intent');
    passed = false;
    
    return {
      passed,
      evidence,
      reasoning: reasoning.join('; '),
      timestamp: new Date().toISOString(),
      gateName: 'INTENT',
    };
  }

  evidence.push({
    type: 'intent_declared',
    description: 'Artifact declares its intent',
    value: declaredIntent,
    severity: 'info',
  });
  reasoning.push(`Declared intent: "${declaredIntent}"`);

  // Check 2: Content analysis for hidden behaviors
  const content = artifact.content.toLowerCase();
  
  // Detect potentially dangerous patterns
  const dangerousPatterns = [
    { pattern: /eval\s*\(/, name: 'eval() usage' },
    { pattern: /exec\s*\(/, name: 'exec() usage' },
    { pattern: /system\s*\(/, name: 'system() call' },
    { pattern: /\.\.\/|\.\.\\/, name: 'path traversal' },
    { pattern: /password|secret|token|api[_-]?key/i, name: 'credential handling' },
  ];

  const detectedPatterns: string[] = [];
  for (const { pattern, name } of dangerousPatterns) {
    if (pattern.test(content)) {
      detectedPatterns.push(name);
    }
  }

  if (detectedPatterns.length > 0) {
    evidence.push({
      type: 'sensitive_patterns_detected',
      description: 'Potentially sensitive operations detected',
      value: detectedPatterns,
      severity: 'warning',
    });
    reasoning.push(`Detected patterns: ${detectedPatterns.join(', ')}`);
    
    // Check if intent mentions these capabilities
    const lowerIntent = declaredIntent.toLowerCase();
    const undeclaredPatterns = detectedPatterns.filter(pattern => {
      // Extract key terms from pattern name (e.g., "eval" from "eval() usage")
      const keyTerms = pattern.toLowerCase().replace(/[()]/g, '').split(/\s+/);
      return !keyTerms.some(term => term.length > 2 && lowerIntent.includes(term));
    });
    
    if (undeclaredPatterns.length > 0) {
      evidence.push({
        type: 'undeclared_capabilities',
        description: 'Sensitive operations not mentioned in intent',
        value: undeclaredPatterns,
        severity: 'warning',
      });
      reasoning.push(`WARNING: Undeclared sensitive operations: ${undeclaredPatterns.join(', ')}`);
      // Fail gate if sensitive operations are undeclared
      passed = false;
    }
  }

  // Check 3: Type vs Intent alignment
  const intentKeywords = ['create', 'read', 'update', 'delete', 'modify', 'analyze', 'validate'];
  const hasActionKeyword = intentKeywords.some(kw => 
    declaredIntent.toLowerCase().includes(kw)
  );

  if (!hasActionKeyword) {
    evidence.push({
      type: 'vague_intent',
      description: 'Intent lacks clear action verb',
      value: declaredIntent,
      severity: 'warning',
    });
    reasoning.push('Intent could be more specific about action');
  }

  return {
    passed,
    evidence,
    reasoning: reasoning.join('; '),
    timestamp: new Date().toISOString(),
    gateName: 'INTENT',
  };
}
