/**
 * SPHINX Gateway Tests
 * 
 * Tests for the SPHINX security gate framework
 * ATOM: ATOM-TEST-20260119-001-sphinx-gates
 */

import { describe, it, expect } from 'vitest';
import { SPHINXGateway } from '../sphinx/gates';
import type { Artifact } from '../sphinx/types';

describe('SPHINX Gateway', () => {
  const createTestArtifact = (overrides?: Partial<Artifact>): Artifact => ({
    id: 'test-artifact-001',
    type: 'markdown',
    content: 'This is test content for validation.',
    metadata: {
      intent: 'Test artifact for validation',
    },
    source: 'test-source',
    author: 'test-author',
    ...overrides,
  });

  describe('Gate 1: ORIGIN', () => {
    it('should pass when artifact has valid source and author', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact();
      
      const result = await gateway.validateGate('origin', artifact);
      
      expect(result.passed).toBe(true);
      expect(result.gateName).toBe('ORIGIN');
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'source_present' })
      );
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'author_present' })
      );
    });

    it('should fail when artifact has no source', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({ source: undefined });
      
      const result = await gateway.validateGate('origin', artifact);
      
      expect(result.passed).toBe(false);
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'source_missing', severity: 'warning' })
      );
    });

    it('should detect ATOM trail reference', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        metadata: {
          atomTrail: 'ATOM-FEATURE-20260119-001',
          intent: 'Test',
        },
      });
      
      const result = await gateway.validateGate('origin', artifact);
      
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'atom_trail_reference' })
      );
    });
  });

  describe('Gate 2: INTENT', () => {
    it('should pass when intent is declared', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        metadata: { intent: 'Analyze and validate document coherence' },
      });
      
      const result = await gateway.validateGate('intent', artifact);
      
      expect(result.passed).toBe(true);
      expect(result.gateName).toBe('INTENT');
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'intent_declared' })
      );
    });

    it('should fail when intent is missing', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        metadata: {},
      });
      
      const result = await gateway.validateGate('intent', artifact);
      
      expect(result.passed).toBe(false);
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'intent_missing', severity: 'critical' })
      );
    });

    it('should detect sensitive patterns in content', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: 'This code uses eval() to execute dynamic code and accesses API_KEY.',
        metadata: { intent: 'Simple text processing' },
      });
      
      const result = await gateway.validateGate('intent', artifact);
      
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'sensitive_patterns_detected' })
      );
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'undeclared_capabilities' })
      );
    });

    it('should not flag sensitive patterns if mentioned in intent', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: 'This code uses eval() to execute dynamic code.',
        metadata: { intent: 'Dynamic code evaluation using eval for plugin system' },
      });
      
      const result = await gateway.validateGate('intent', artifact);
      
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'sensitive_patterns_detected' })
      );
      expect(result.evidence).not.toContainEqual(
        expect.objectContaining({ type: 'undeclared_capabilities' })
      );
    });
  });

  describe('Gate 3: COHERENCE', () => {
    it('should pass when content is coherent', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: `This is a well-structured document.

It explains concepts clearly without circular reasoning.

The ideas flow naturally from introduction to conclusion.

Therefore, this document demonstrates good coherence.`,
      });
      
      const result = await gateway.validateGate('coherence', artifact, {
        coherenceThreshold: 60,
      });
      
      expect(result.passed).toBe(true);
      expect(result.gateName).toBe('COHERENCE');
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'wave_analysis' })
      );
    });

    it('should fail when coherence is below threshold', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: 'repeat repeat repeat repeat repeat same same same same',
      });
      
      const result = await gateway.validateGate('coherence', artifact, {
        coherenceThreshold: 80,
      });
      
      expect(result.passed).toBe(false);
    });

    it('should detect high curl', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: `circular circular circular reasoning reasoning reasoning
circular circular circular reasoning reasoning reasoning
circular circular circular reasoning reasoning reasoning`,
      });
      
      const result = await gateway.validateGate('coherence', artifact);
      
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'high_curl' })
      );
    });
  });

  describe('Gate 4: IDENTITY', () => {
    it('should pass when type matches content', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'markdown',
        content: '# Heading\n\nThis is markdown with [links](http://example.com).',
      });
      
      const result = await gateway.validateGate('identity', artifact);
      
      expect(result.passed).toBe(true);
      expect(result.gateName).toBe('IDENTITY');
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'type_content_match' })
      );
    });

    it('should fail when type is not declared', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({ type: '' });
      
      const result = await gateway.validateGate('identity', artifact);
      
      expect(result.passed).toBe(false);
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'type_missing', severity: 'critical' })
      );
    });

    it('should validate JSON content type', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'json',
        content: '{"key": "value", "array": [1, 2, 3]}',
      });
      
      const result = await gateway.validateGate('identity', artifact);
      
      expect(result.passed).toBe(true);
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'type_content_match' })
      );
    });

    it('should detect missing required interface methods', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'typescript',
        content: 'function otherFunction() { return 42; }',
        metadata: {
          requiredInterface: {
            validate: 'function',
            execute: 'function',
          },
          intent: 'Test',
        },
      });
      
      const result = await gateway.validateGate('identity', artifact);
      
      expect(result.passed).toBe(false);
      expect(result.evidence).toContainEqual(
        expect.objectContaining({ type: 'interface_contract_check' })
      );
    });
  });

  describe('Gate 5: PASSAGE', () => {
    it('should pass when all previous gates passed', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact();
      
      const result = await gateway.validate(artifact, {
        coherenceThreshold: 60,
      });
      
      expect(result.overallPassed).toBe(true);
      expect(result.gates.passage).not.toBeNull();
      expect(result.gates.passage?.passed).toBe(true);
      expect(result.failedAt).toBeUndefined();
    });

    it('should fail when a previous gate failed', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        source: undefined, // Will fail ORIGIN gate
      });
      
      const result = await gateway.validate(artifact);
      
      expect(result.overallPassed).toBe(false);
      expect(result.failedAt).toBe('origin');
      expect(result.gates.passage).toBeNull(); // Never reached
    });

    it('should check context permissions', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact();
      
      const result = await gateway.validate(artifact, {
        coherenceThreshold: 60,
        context: {
          requiredPermissions: ['read', 'write'],
          grantedPermissions: ['read'], // Missing 'write'
        },
      });
      
      expect(result.overallPassed).toBe(false);
      expect(result.failedAt).toBe('passage');
      expect(result.gates.passage?.evidence).toContainEqual(
        expect.objectContaining({ type: 'insufficient_permissions' })
      );
    });

    it('should check environment constraints', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact();
      
      const result = await gateway.validate(artifact, {
        coherenceThreshold: 60,
        context: {
          allowedEnvironments: ['development', 'staging'],
          environment: 'production',
        },
      });
      
      expect(result.overallPassed).toBe(false);
      expect(result.gates.passage?.evidence).toContainEqual(
        expect.objectContaining({ type: 'environment_not_allowed' })
      );
    });
  });

  describe('Full SPHINX Validation', () => {
    it('should execute all gates sequentially', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: `# Test Document

This is a test document with good coherence.

It has proper structure and clear intent.

Therefore, it should pass all validation gates.`,
      });
      
      const result = await gateway.validate(artifact, {
        coherenceThreshold: 60,
      });
      
      expect(result.overallPassed).toBe(true);
      expect(result.gates.origin?.passed).toBe(true);
      expect(result.gates.intent?.passed).toBe(true);
      expect(result.gates.coherence?.passed).toBe(true);
      expect(result.gates.identity?.passed).toBe(true);
      expect(result.gates.passage?.passed).toBe(true);
    });

    it('should short-circuit on first failure', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        metadata: {}, // Missing intent - will fail INTENT gate
      });
      
      const result = await gateway.validate(artifact);
      
      expect(result.overallPassed).toBe(false);
      expect(result.failedAt).toBe('intent');
      expect(result.gates.origin?.passed).toBe(true);
      expect(result.gates.intent?.passed).toBe(false);
      expect(result.gates.coherence).toBeNull(); // Not executed
      expect(result.gates.identity).toBeNull(); // Not executed
      expect(result.gates.passage).toBeNull(); // Not executed
    });

    it('should allow skipping specific gates', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        source: undefined, // Would fail origin
      });
      
      const result = await gateway.validate(artifact, {
        skipGates: ['origin'], // Skip the failing gate
        coherenceThreshold: 60,
      });
      
      expect(result.gates.origin).toBeNull();
      expect(result.gates.intent?.passed).toBe(true);
    });
  });

  describe('Custom Gates', () => {
    it('should allow registering custom gates', () => {
      const gateway = new SPHINXGateway();
      
      gateway.registerCustomGate('custom', async (_artifact) => ({
        passed: true,
        evidence: [],
        reasoning: 'Custom validation',
        timestamp: new Date().toISOString(),
        gateName: 'CUSTOM',
      }));
      
      const gates = gateway.getAvailableGates();
      expect(gates).toContain('custom');
    });

    it('should execute custom gates', async () => {
      const gateway = new SPHINXGateway();
      
      gateway.registerCustomGate('length', async (artifact) => ({
        passed: artifact.content.length > 10,
        evidence: [
          {
            type: 'length_check',
            description: 'Content length validation',
            value: artifact.content.length,
          },
        ],
        reasoning: `Content length: ${artifact.content.length}`,
        timestamp: new Date().toISOString(),
        gateName: 'LENGTH',
      }));
      
      const artifact = createTestArtifact({ content: 'short' });
      const result = await gateway.validateGate('length', artifact);
      
      expect(result.passed).toBe(false);
      expect(result.gateName).toBe('LENGTH');
    });
  });

  describe('ATOM Trail Logging', () => {
    it('should log each gate to ATOM trail', async () => {
      const atomLogs: string[] = [];
      const atomLogger = async (entry: { actor: string; decision: string }) => {
        const id = `atom-${atomLogs.length + 1}`;
        atomLogs.push(`${id}: ${entry.decision}`);
        return id;
      };
      
      const gateway = new SPHINXGateway(atomLogger);
      const _artifact = createTestArtifact();
      
      const result = await gateway.validate(_artifact, {
        coherenceThreshold: 60,
      });
      
      expect(result.atomTrail.length).toBeGreaterThan(0);
      expect(atomLogs.length).toBeGreaterThan(0);
      expect(atomLogs.some(log => log.includes('Gate ORIGIN'))).toBe(true);
      expect(atomLogs.some(log => log.includes('Gate INTENT'))).toBe(true);
    });
  });
});
