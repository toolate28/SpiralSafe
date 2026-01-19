/**
 * SPHINX Gateway - Security Gate Framework
 * 
 * Main orchestrator for the 5 security gates:
 * 1. ORIGIN - Where did this come from?
 * 2. INTENT - What is this trying to do?
 * 3. COHERENCE - Does this make sense internally?
 * 4. IDENTITY - Is this what it claims to be?
 * 5. PASSAGE - Should this be allowed through?
 * 
 * ATOM: ATOM-FEATURE-20260119-007-sphinx-gateway
 */

import type {
  Artifact,
  GateResult,
  GateValidator,
  SPHINXOptions,
  SPHINXResult,
  SPHINXGateContext,
} from './types';
import { validateOrigin } from './origin-gate';
import { validateIntent } from './intent-gate';
import { validateCoherence } from './coherence-gate';
import { validateIdentity } from './identity-gate';
import { validatePassage } from './passage-gate';

export class SPHINXGateway {
  private customGates: Map<string, GateValidator> = new Map();
  private atomLogger?: (entry: AtomLogEntry) => Promise<string>;

  constructor(atomLogger?: (entry: AtomLogEntry) => Promise<string>) {
    this.atomLogger = atomLogger;
  }

  /**
   * Validate an artifact through all SPHINX gates
   * Gates execute sequentially and short-circuit on failure
   */
  async validate(artifact: Artifact, options?: SPHINXOptions): Promise<SPHINXResult> {
    const startTime = Date.now();
    const result: SPHINXResult = {
      artifact,
      gates: {
        origin: null,
        intent: null,
        coherence: null,
        identity: null,
        passage: null,
      },
      overallPassed: false,
      atomTrail: [],
      timestamp: new Date().toISOString(),
    };

    const skipGates = options?.skipGates || [];
    
    try {
      // Gate 1: ORIGIN
      if (!skipGates.includes('origin')) {
        result.gates.origin = await validateOrigin(artifact, options);
        result.atomTrail.push(await this.logGate(result.gates.origin, artifact));
        
        if (!result.gates.origin.passed) {
          result.failedAt = 'origin';
          return result;
        }
      }

      // Gate 2: INTENT
      if (!skipGates.includes('intent')) {
        result.gates.intent = await validateIntent(artifact, options);
        result.atomTrail.push(await this.logGate(result.gates.intent, artifact));
        
        if (!result.gates.intent.passed) {
          result.failedAt = 'intent';
          return result;
        }
      }

      // Gate 3: COHERENCE
      if (!skipGates.includes('coherence')) {
        result.gates.coherence = await validateCoherence(artifact, options);
        result.atomTrail.push(await this.logGate(result.gates.coherence, artifact));
        
        if (!result.gates.coherence.passed) {
          result.failedAt = 'coherence';
          return result;
        }
      }

      // Gate 4: IDENTITY
      if (!skipGates.includes('identity')) {
        result.gates.identity = await validateIdentity(artifact, options);
        result.atomTrail.push(await this.logGate(result.gates.identity, artifact));
        
        if (!result.gates.identity.passed) {
          result.failedAt = 'identity';
          return result;
        }
      }

      // Gate 5: PASSAGE
      if (!skipGates.includes('passage')) {
        const gateContext: SPHINXGateContext = {
          artifact,
          options: options || {},
          previousGates: result.gates,
        };
        
        result.gates.passage = await validatePassage(artifact, gateContext);
        result.atomTrail.push(await this.logGate(result.gates.passage, artifact));
        
        if (!result.gates.passage.passed) {
          result.failedAt = 'passage';
          return result;
        }
      }

      // All gates passed
      result.overallPassed = true;
      
      // Log final success
      if (this.atomLogger) {
        const successId = await this.atomLogger({
          actor: 'sphinx-gateway',
          decision: 'All SPHINX gates passed',
          rationale: `Artifact ${artifact.id} validated successfully in ${Date.now() - startTime}ms`,
          outcome: JSON.stringify({ overallPassed: true }),
        });
        result.atomTrail.push(successId);
      }

    } catch (error) {
      // Log error
      if (this.atomLogger) {
        const errorId = await this.atomLogger({
          actor: 'sphinx-gateway',
          decision: 'SPHINX validation error',
          rationale: error instanceof Error ? error.message : String(error),
          outcome: JSON.stringify({ error: true }),
        });
        result.atomTrail.push(errorId);
      }
      throw error;
    }

    return result;
  }

  /**
   * Validate a single gate independently
   */
  async validateGate(gateName: string, artifact: Artifact, options?: SPHINXOptions): Promise<GateResult> {
    // Check for custom gate first
    const customValidator = this.customGates.get(gateName);
    if (customValidator) {
      return customValidator(artifact, options);
    }

    // Standard gates
    switch (gateName.toLowerCase()) {
      case 'origin':
        return validateOrigin(artifact, options);
      case 'intent':
        return validateIntent(artifact, options);
      case 'coherence':
        return validateCoherence(artifact, options);
      case 'identity':
        return validateIdentity(artifact, options);
      case 'passage': {
        // Passage gate requires context from previous gates
        // For standalone validation, we create an empty context
        const gateContext: SPHINXGateContext = {
          artifact,
          options: options || {},
          previousGates: {},
        };
        return validatePassage(artifact, gateContext);
      }
      default:
        throw new Error(`Unknown gate: ${gateName}`);
    }
  }

  /**
   * Register a custom gate validator
   */
  registerCustomGate(name: string, validator: GateValidator): void {
    this.customGates.set(name, validator);
  }

  /**
   * Get list of available gates (standard + custom)
   */
  getAvailableGates(): string[] {
    const standardGates = ['origin', 'intent', 'coherence', 'identity', 'passage'];
    const customGateNames = Array.from(this.customGates.keys());
    return [...standardGates, ...customGateNames];
  }

  /**
   * Log a gate result to ATOM trail
   */
  private async logGate(gateResult: GateResult, artifact: Artifact): Promise<string> {
    if (!this.atomLogger) {
      return `${gateResult.gateName}-${Date.now()}`; // Fallback ID
    }

    const logId = await this.atomLogger({
      actor: 'sphinx-gateway',
      decision: `Gate ${gateResult.gateName}: ${gateResult.passed ? 'PASS' : 'FAIL'}`,
      rationale: gateResult.reasoning,
      outcome: JSON.stringify({
        passed: gateResult.passed,
        evidence: gateResult.evidence,
        artifactId: artifact.id,
      }),
    });

    return logId;
  }
}

// ATOM log entry interface
interface AtomLogEntry {
  actor: string;
  decision: string;
  rationale: string;
  outcome: string;
}

// Re-export types for convenience
export * from './types';
export { validateOrigin } from './origin-gate';
export { validateIntent } from './intent-gate';
export { validateCoherence } from './coherence-gate';
export { validateIdentity } from './identity-gate';
export { validatePassage } from './passage-gate';
