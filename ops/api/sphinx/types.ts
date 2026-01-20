/**
 * SPHINX Security Gate Types
 * 
 * Type definitions for the SPHINX gate framework
 * ATOM: ATOM-FEATURE-20260119-001-sphinx-gate-types
 */

export interface Artifact {
  id: string;
  type: string;
  content: string;
  metadata: Record<string, unknown>;
  source?: string;
  author?: string;
  signature?: string;
}

export interface Evidence {
  type: string;
  description: string;
  value: unknown;
  severity?: 'info' | 'warning' | 'critical';
}

export interface GateResult {
  passed: boolean;
  evidence: Evidence[];
  reasoning: string;
  timestamp: string;
  gateName: string;
}

export interface SPHINXResult {
  artifact: Artifact;
  gates: {
    origin: GateResult | null;
    intent: GateResult | null;
    coherence: GateResult | null;
    identity: GateResult | null;
    passage: GateResult | null;
  };
  overallPassed: boolean;
  atomTrail: string[];
  timestamp: string;
  failedAt?: string; // Which gate failed (if any)
}

export interface SPHINXOptions {
  coherenceThreshold?: number; // Default: 80
  skipGates?: string[]; // Skip specific gates for testing
  customValidators?: Record<string, GateValidator>;
  context?: Record<string, unknown>; // Context for passage gate
}

export type GateValidator = (artifact: Artifact, options?: SPHINXOptions) => Promise<GateResult>;

export interface SPHINXGateContext {
  artifact: Artifact;
  options: SPHINXOptions;
  previousGates: Partial<SPHINXResult['gates']>;
}
