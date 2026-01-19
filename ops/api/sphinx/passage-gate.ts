/**
 * SPHINX Gate 5: PASSAGE
 * 
 * Final authorization gate - checks all previous gates and context
 * Question: "Should this be allowed through?"
 * 
 * ATOM: ATOM-FEATURE-20260119-006-sphinx-passage-gate
 */

import type { Artifact, GateResult, Evidence, SPHINXGateContext } from './types';

export async function validatePassage(
  _artifact: Artifact,
  context: SPHINXGateContext
): Promise<GateResult> {
  const evidence: Evidence[] = [];
  let passed = true;
  const reasoning: string[] = [];

  // Check 1: All previous gates must pass
  const { previousGates } = context;
  const gateNames = ['origin', 'intent', 'coherence', 'identity'] as const;
  const failedGates: string[] = [];
  
  for (const gateName of gateNames) {
    const gate = previousGates[gateName];
    if (!gate) {
      failedGates.push(`${gateName} (not executed)`);
    } else if (!gate.passed) {
      failedGates.push(`${gateName} (failed)`);
    }
  }

  if (failedGates.length > 0) {
    evidence.push({
      type: 'previous_gates_failed',
      description: 'One or more previous gates failed',
      value: failedGates,
      severity: 'critical',
    });
    reasoning.push(`FAIL: Previous gates failed: ${failedGates.join(', ')}`);
    passed = false;
    
    return {
      passed,
      evidence,
      reasoning: reasoning.join('; '),
      timestamp: new Date().toISOString(),
      gateName: 'PASSAGE',
    };
  }

  evidence.push({
    type: 'all_gates_passed',
    description: 'All previous security gates passed',
    value: true,
    severity: 'info',
  });
  reasoning.push('All previous gates: PASS');

  // Check 2: Context-specific requirements
  const contextRules = context.options.context;
  if (contextRules) {
    // Check required permissions
    const requiredPermissions = contextRules.requiredPermissions as string[] | undefined;
    const grantedPermissions = contextRules.grantedPermissions as string[] | undefined;
    
    if (requiredPermissions && grantedPermissions) {
      const missingPermissions = requiredPermissions.filter(
        perm => !grantedPermissions.includes(perm)
      );
      
      if (missingPermissions.length > 0) {
        evidence.push({
          type: 'insufficient_permissions',
          description: 'Required permissions not granted',
          value: missingPermissions,
          severity: 'critical',
        });
        reasoning.push(`FAIL: Missing permissions: ${missingPermissions.join(', ')}`);
        passed = false;
      } else {
        evidence.push({
          type: 'permissions_sufficient',
          description: 'All required permissions granted',
          value: true,
          severity: 'info',
        });
        reasoning.push('Permissions: OK');
      }
    }

    // Check environment constraints
    const allowedEnvironments = contextRules.allowedEnvironments as string[] | undefined;
    const currentEnvironment = contextRules.environment as string | undefined;
    
    if (allowedEnvironments && currentEnvironment) {
      if (!allowedEnvironments.includes(currentEnvironment)) {
        evidence.push({
          type: 'environment_not_allowed',
          description: 'Current environment not in allowed list',
          value: { current: currentEnvironment, allowed: allowedEnvironments },
          severity: 'critical',
        });
        reasoning.push(`FAIL: Environment '${currentEnvironment}' not allowed`);
        passed = false;
      } else {
        evidence.push({
          type: 'environment_allowed',
          description: 'Environment check passed',
          value: currentEnvironment,
          severity: 'info',
        });
        reasoning.push(`Environment: ${currentEnvironment} (allowed)`);
      }
    }

    // Check rate limiting or quotas
    const rateLimit = contextRules.rateLimit as { current: number; max: number } | undefined;
    if (rateLimit) {
      if (rateLimit.current >= rateLimit.max) {
        evidence.push({
          type: 'rate_limit_exceeded',
          description: 'Rate limit exceeded',
          value: rateLimit,
          severity: 'critical',
        });
        reasoning.push(`FAIL: Rate limit exceeded (${rateLimit.current}/${rateLimit.max})`);
        passed = false;
      } else {
        evidence.push({
          type: 'rate_limit_ok',
          description: 'Within rate limits',
          value: rateLimit,
          severity: 'info',
        });
        reasoning.push(`Rate limit: ${rateLimit.current}/${rateLimit.max}`);
      }
    }
  }

  // Check 3: Final authorization decision
  const explicitAuthorization = context.options.context?.authorized as boolean | undefined;
  if (explicitAuthorization !== undefined) {
    if (!explicitAuthorization) {
      evidence.push({
        type: 'explicit_denial',
        description: 'Explicit authorization denied',
        value: false,
        severity: 'critical',
      });
      reasoning.push('FAIL: Explicit authorization denied');
      passed = false;
    } else {
      evidence.push({
        type: 'explicit_authorization',
        description: 'Explicit authorization granted',
        value: true,
        severity: 'info',
      });
      reasoning.push('Explicit authorization: granted');
    }
  }

  if (passed) {
    reasoning.push('PASSAGE: GRANTED');
  }

  return {
    passed,
    evidence,
    reasoning: reasoning.join('; '),
    timestamp: new Date().toISOString(),
    gateName: 'PASSAGE',
  };
}
