/**
 * SpiralSafe API Integration Tests
 * Tests all endpoints including new session, stats, and logdy handlers
 *
 * Run: npm test
 */

import { describe, it, expect } from 'vitest';

const API_BASE = process.env.SPIRALSAFE_API_BASE || 'https://api.spiralsafe.org';
const API_KEY = process.env.SPIRALSAFE_API_KEY || 'test-key';

const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': API_KEY
};

describe('SpiralSafe API', () => {

  describe('Health Check', () => {
    it('should return healthy status', async () => {
      const res = await fetch(`${API_BASE}/api/health`);
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data.status).toBe('healthy');
      expect(data.checks.d1).toBe(true);
      expect(data.checks.kv).toBe(true);
      expect(data.checks.r2).toBe(true);
    });
  });

  describe('Wave Analysis', () => {
    it('should analyze content coherence', async () => {
      const res = await fetch(`${API_BASE}/api/wave/analyze`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          content: 'This is a test document. It has clear structure. Therefore, it should be coherent.'
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data).toHaveProperty('curl');
      expect(data).toHaveProperty('divergence');
      expect(data).toHaveProperty('coherent');
    });

    it('should return thresholds', async () => {
      const res = await fetch(`${API_BASE}/api/wave/thresholds`);
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data).toHaveProperty('curl');
      expect(data).toHaveProperty('divergence');
    });
  });

  describe('Bump Markers', () => {
    let bumpId: string;

    it('should create a bump marker', async () => {
      const res = await fetch(`${API_BASE}/api/bump/create`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          type: 'SYNC',
          from: 'test-suite',
          to: 'api',
          state: 'testing',
          context: { test: true }
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(201);
      expect(data).toHaveProperty('id');
      expect(data.type).toBe('SYNC');
      bumpId = data.id;
    });

    it('should list pending bumps', async () => {
      const res = await fetch(`${API_BASE}/api/bump/pending`);
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(Array.isArray(data)).toBe(true);
    });

    it('should resolve a bump', async () => {
      if (!bumpId) return;

      const res = await fetch(`${API_BASE}/api/bump/resolve/${bumpId}`, {
        method: 'PUT',
        headers
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data.resolved).toBe(true);
    });
  });

  describe('AWI Permission Grants', () => {
    let grantId: string;

    it('should request an AWI grant', async () => {
      const res = await fetch(`${API_BASE}/api/awi/request`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          intent: 'Test grant for integration testing',
          scope: {
            resources: ['test:*'],
            actions: ['read', 'write']
          },
          level: 2,
          ttl_seconds: 300
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(201);
      expect(data).toHaveProperty('id');
      expect(data.level).toBe(2);
      grantId = data.id;
    });

    it('should verify a grant', async () => {
      if (!grantId) return;

      const res = await fetch(`${API_BASE}/api/awi/verify`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          grant_id: grantId,
          action: 'read'
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data.valid).toBe(true);
    });
  });

  describe('Context Storage', () => {
    const _contextId: string = "";

    it('should store context', async () => {
      const res = await fetch(`${API_BASE}/api/context/store`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          domain: 'test',
          content: { test: true, timestamp: Date.now() },
          signals: {
            use_when: ['testing'],
            avoid_when: ['production']
          }
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(201);
      expect(data).toHaveProperty('id');
      expect(data.domain).toBe('test');
      contextId = data.id;
    });

    it('should query contexts', async () => {
      const res = await fetch(`${API_BASE}/api/context/query?domain=test`);
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(Array.isArray(data)).toBe(true);
    });
  });

  describe('Session Management', () => {
    let sessionId: string;

    it('should start a session', async () => {
      const res = await fetch(`${API_BASE}/api/session/start`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          user: 'test-user',
          device: 'test-runner',
          context: { test: true }
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(201);
      expect(data).toHaveProperty('id');
      expect(data.status).toBe('active');
      sessionId = data.id;
    });

    it('should send heartbeat', async () => {
      if (!sessionId) return;

      const res = await fetch(`${API_BASE}/api/session/heartbeat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          session_id: sessionId,
          status: 'active'
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data).toHaveProperty('last_heartbeat');
    });

    it('should list active sessions', async () => {
      const res = await fetch(`${API_BASE}/api/session/active`);
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(Array.isArray(data)).toBe(true);
    });

    it('should end session', async () => {
      if (!sessionId) return;

      const res = await fetch(`${API_BASE}/api/session/end/${sessionId}`, {
        method: 'DELETE',
        headers
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data.status).toBe('offline');
    });
  });

  describe('Stats Dashboard', () => {
    it('should return stats', async () => {
      const res = await fetch(`${API_BASE}/api/stats`);
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data).toHaveProperty('period');
      expect(data).toHaveProperty('metrics');
      expect(data.metrics).toHaveProperty('wave_analyses');
      expect(data.metrics).toHaveProperty('active_sessions');
    });
  });

  describe('Logdy Integration', () => {
    it('should forward logs', async () => {
      const res = await fetch(`${API_BASE}/api/logdy/forward`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          level: 'info',
          message: 'Test log from integration suite',
          context: { test: true },
          source: 'vitest'
        })
      });
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(data.logged).toBe(true);
    });

    it('should get recent logs', async () => {
      const res = await fetch(`${API_BASE}/api/logdy/recent`);
      const data = await res.json() as Record<string, unknown>;

      expect(res.status).toBe(200);
      expect(Array.isArray(data)).toBe(true);
    });
  });

  describe('Rate Limiting', () => {
    it('should include rate limit headers', async () => {
      const res = await fetch(`${API_BASE}/api/health`);

      expect(res.headers.get('X-RateLimit-Limit')).toBeTruthy();
      expect(res.headers.get('X-RateLimit-Remaining')).toBeTruthy();
    });
  });

  describe('Authentication', () => {
    it('should reject write without API key', async () => {
      const res = await fetch(`${API_BASE}/api/bump/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'SYNC' })
      });

      expect(res.status).toBe(401);
    });
  });

});
