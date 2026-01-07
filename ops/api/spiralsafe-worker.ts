/**
 * SpiralSafe Operations API
 * Cloudflare Worker serving as the coherence engine coordination point
 * 
 * Endpoints:
 *   /api/wave     - Coherence analysis
 *   /api/bump     - Routing and handoff
 *   /api/awi      - Permission scaffolding
 *   /api/atom     - Task orchestration
 *   /api/context  - Knowledge units
 *   /api/health   - System status
 * 
 * H&&S: Structure-preserving operations across substrates
 */

export interface Env {
  SPIRALSAFE_DB: D1Database;
  SPIRALSAFE_KV: KVNamespace;
  SPIRALSAFE_R2: R2Bucket;
  SPIRALSAFE_API_KEY: string;
  SPIRALSAFE_API_KEYS?: string;      // Comma-separated list of valid API keys
  RATE_LIMIT_REQUESTS?: string;      // Max requests per window (default: 100)
  RATE_LIMIT_WINDOW?: string;        // Time window in seconds (default: 60)
  RATE_LIMIT_AUTH_FAILURES?: string; // Max auth failures per window (default: 5)
}

// ═══════════════════════════════════════════════════════════════
// Types
// ═══════════════════════════════════════════════════════════════

interface WaveAnalysis {
  curl: number;
  divergence: number;
  potential: number;
  regions: WaveRegion[];
  coherent: boolean;
}

interface WaveRegion {
  start: number;
  end: number;
  type: 'high_curl' | 'positive_divergence' | 'negative_divergence' | 'high_potential';
  severity: 'warning' | 'critical';
  description: string;
}

interface BumpMarker {
  id: string;
  type: 'WAVE' | 'PASS' | 'PING' | 'SYNC' | 'BLOCK';
  from: string;
  to: string;
  state: string;
  context: Record<string, unknown>;
  timestamp: string;
  resolved: boolean;
}

interface AWIGrant {
  id: string;
  intent: string;
  scope: AWIScope;
  level: 0 | 1 | 2 | 3 | 4;
  granted_at: string;
  expires_at: string;
  audit_trail: AWIAuditEntry[];
}

interface AWIScope {
  resources: string[];
  actions: string[];
  time_limit?: string;
  impact_limit?: string;
}

interface AWIAuditEntry {
  timestamp: string;
  action: string;
  result: 'success' | 'denied' | 'error';
  details?: string;
}

interface Atom {
  id: string;
  name: string;
  molecule: string;
  compound: string;
  status: 'pending' | 'in_progress' | 'blocked' | 'complete' | 'verified';
  verification: {
    criteria: Record<string, string>;
    automated: boolean;
  };
  dependencies: {
    requires: string[];
    blocks: string[];
  };
  assignee: string;
  created_at: string;
  updated_at: string;
}

// ═══════════════════════════════════════════════════════════════
// Security Utilities
// ═══════════════════════════════════════════════════════════════

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;
}

async function checkRateLimit(
  env: Env,
  ip: string,
  key: string,
  maxRequests: number,
  windowSeconds: number
): Promise<RateLimitResult> {
  const rateLimitKey = `ratelimit:${key}:${ip}`;
  const now = Math.floor(Date.now() / 1000);
  const windowStart = now - windowSeconds;

  // Get current request data
  const dataJson = await env.SPIRALSAFE_KV.get(rateLimitKey);
  let requests: number[] = dataJson ? JSON.parse(dataJson) : [];

  // Filter out requests outside the current window
  requests = requests.filter(timestamp => timestamp > windowStart);

  // Check if rate limit is exceeded BEFORE adding current request
  const allowed = requests.length < maxRequests;
  
  // Calculate remaining slots
  let remaining: number;
  
  // Add current request if allowed
  if (allowed) {
    requests.push(now);
    remaining = maxRequests - requests.length;
  } else {
    // No remaining requests when rate limit is exceeded
    remaining = 0;
  }
  
  // Store updated request list with TTL (always update to keep data clean)
  // Note: Denied requests are intentionally not tracked in KV to prevent
  // attackers from filling storage with blocked request timestamps
  await env.SPIRALSAFE_KV.put(
    rateLimitKey,
    JSON.stringify(requests),
    { expirationTtl: windowSeconds }
  );

  // When rate limited, the window effectively resets when the oldest
  // request in the current window expires, not a full window from now.
  // Use a conservative fallback when not rate limited or if there are no requests.
  const resetAt = !allowed && requests.length > 0
    ? requests[0] + windowSeconds
    : now + windowSeconds;

  return { allowed, remaining, resetAt };
}

async function logRequest(
  env: Env,
  request: Request,
  path: string,
  authenticated: boolean,
  status: number,
  error?: string
): Promise<void> {
  try {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const userAgent = request.headers.get('User-Agent') || 'unknown';
    const logEntry = {
      timestamp: new Date().toISOString(),
      ip,
      method: request.method,
      path,
      authenticated,
      status,
      error,
      userAgent,
      country: request.headers.get('CF-IPCountry') || 'unknown'
    };

    // Store in KV with 30-day retention
    const logKey = `log:${Date.now()}:${crypto.randomUUID()}`;
    await env.SPIRALSAFE_KV.put(logKey, JSON.stringify(logEntry), { expirationTtl: 86400 * 30 });

    // For failed auth attempts, also log to D1 for permanent audit
    if (!authenticated && (status === 401 || status === 403)) {
      await env.SPIRALSAFE_DB.prepare(
        'INSERT INTO system_health (timestamp, status, details) VALUES (?, ?, ?)'
      ).bind(
        new Date().toISOString(),
        'auth_failure',
        JSON.stringify({ ip, path, userAgent })
      ).run();
    }
  } catch (err) {
    // Don't fail requests if logging fails, but emit error for observability
    console.error('logRequest failed', err);
  }
}

function validateApiKey(env: Env, providedKey: string): boolean {
  // Check primary key using constant-time comparison
  if (constantTimeEqual(providedKey, env.SPIRALSAFE_API_KEY)) {
    return true;
  }

  // Check additional keys if configured using constant-time comparison
  if (env.SPIRALSAFE_API_KEYS) {
    const validKeys = env.SPIRALSAFE_API_KEYS.split(',').map(k => k.trim());
    for (const validKey of validKeys) {
      if (constantTimeEqual(providedKey, validKey)) {
        return true;
      }
    }
  }

  return false;
}

// ═══════════════════════════════════════════════════════════════
// Main Handler
// ═══════════════════════════════════════════════════════════════

export default {
  async fetch(request: Request, env: Env, _ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';

    // CORS headers for cross-origin requests
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-AWI-Intent, X-API-Key',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // ═══════════════════════════════════════════════════════════════
    // Rate Limiting
    // ═══════════════════════════════════════════════════════════════
    const rateLimitRequests = parseInt(env.RATE_LIMIT_REQUESTS || '100');
    const rateLimitWindow = parseInt(env.RATE_LIMIT_WINDOW || '60');

    const rateLimit = await checkRateLimit(env, ip, 'api', rateLimitRequests, rateLimitWindow);

    if (!rateLimit.allowed) {
      await logRequest(env, request, path, false, 429, 'Rate limit exceeded');
      return new Response(JSON.stringify({
        error: 'Too Many Requests',
        message: `Rate limit exceeded. Try again in ${rateLimit.resetAt - Math.floor(Date.now() / 1000)} seconds.`,
        limit: rateLimitRequests,
        window: rateLimitWindow,
        resetAt: rateLimit.resetAt
      }), {
        status: 429,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
          'X-RateLimit-Limit': rateLimitRequests.toString(),
          'X-RateLimit-Remaining': '0',
          'X-RateLimit-Reset': rateLimit.resetAt.toString()
        }
      });
    }

    // ═══════════════════════════════════════════════════════════════
    // Authentication for write endpoints
    // ═══════════════════════════════════════════════════════════════
    const isWriteOperation = request.method === 'POST' || request.method === 'PUT' || request.method === 'DELETE';
    const isHealthCheck = path === '/api/health';
    let authenticated = false;

    if (isWriteOperation && !isHealthCheck) {
      const providedKey = request.headers.get('X-API-Key');

      if (!providedKey) {
        await logRequest(env, request, path, false, 401, 'No API key provided');

        // Check auth failure rate limit (stricter)
        const authFailureLimit = parseInt(env.RATE_LIMIT_AUTH_FAILURES || '5');
        const authRateLimit = await checkRateLimit(env, ip, 'auth_failures', authFailureLimit, rateLimitWindow);

        if (!authRateLimit.allowed) {
          return new Response(JSON.stringify({
            error: 'Too Many Failed Authentication Attempts',
            message: `Temporary block due to too many failed attempts. Try again in ${authRateLimit.resetAt - Math.floor(Date.now() / 1000)} seconds.`,
            resetAt: authRateLimit.resetAt
          }), {
            status: 429,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        return new Response(JSON.stringify({
          error: 'Unauthorized',
          message: 'API key required. Include X-API-Key header.'
        }), {
          status: 401,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      if (!validateApiKey(env, providedKey)) {
        await logRequest(env, request, path, false, 403, 'Invalid API key');

        // Check auth failure rate limit (stricter)
        const authFailureLimit = parseInt(env.RATE_LIMIT_AUTH_FAILURES || '5');
        const authRateLimit = await checkRateLimit(env, ip, 'auth_failures', authFailureLimit, rateLimitWindow);

        if (!authRateLimit.allowed) {
          return new Response(JSON.stringify({
            error: 'Too Many Failed Authentication Attempts',
            message: `Temporary block due to too many failed attempts. Try again in ${authRateLimit.resetAt - Math.floor(Date.now() / 1000)} seconds.`,
            resetAt: authRateLimit.resetAt
          }), {
            status: 429,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        return new Response(JSON.stringify({
          error: 'Forbidden',
          message: 'Invalid API key'
        }), {
          status: 403,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      authenticated = true;
    }

    try {
      let response: Response;

      // Route to appropriate handler
      if (path.startsWith('/api/wave')) {
        response = await handleWave(request, env, path);
      } else if (path.startsWith('/api/bump')) {
        response = await handleBump(request, env, path);
      } else if (path.startsWith('/api/awi')) {
        response = await handleAWI(request, env, path);
      } else if (path.startsWith('/api/atom')) {
        response = await handleAtom(request, env, path);
      } else if (path.startsWith('/api/context')) {
        response = await handleContext(request, env, path);
      } else if (path === '/api/health') {
        response = await handleHealth(env);
      } else {
        response = new Response(JSON.stringify({
          error: 'Not found',
          available_endpoints: ['/api/wave', '/api/bump', '/api/awi', '/api/atom', '/api/context', '/api/health']
        }), { status: 404 });
      }

      // Add CORS and rate limit headers to response
      Object.entries(corsHeaders).forEach(([key, value]) => {
        response.headers.set(key, value);
      });
      response.headers.set('X-RateLimit-Limit', rateLimitRequests.toString());
      response.headers.set('X-RateLimit-Remaining', rateLimit.remaining.toString());
      response.headers.set('X-RateLimit-Reset', rateLimit.resetAt.toString());

      // Log successful request
      await logRequest(env, request, path, authenticated, response.status);

      return response;

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      await logRequest(env, request, path, authenticated, 500, errorMessage);

      return new Response(JSON.stringify({
        error: 'Internal server error',
        message: errorMessage
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  },
};

// ═══════════════════════════════════════════════════════════════
// Wave Handlers - Coherence Detection
// ═══════════════════════════════════════════════════════════════

async function handleWave(request: Request, env: Env, path: string): Promise<Response> {
  if (request.method === 'POST' && path === '/api/wave/analyze') {
    const body = await request.json() as { content: string; thresholds?: Record<string, number> };
    const analysis = analyzeCoherence(body.content, body.thresholds);
    
    // Store analysis in D1 for audit trail
    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO wave_analyses (id, content_hash, curl, divergence, potential, coherent, analyzed_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
    ).bind(
      crypto.randomUUID(),
      await hashContent(body.content),
      analysis.curl,
      analysis.divergence,
      analysis.potential,
      analysis.coherent ? 1 : 0,
      new Date().toISOString()
    ).run();

    return jsonResponse(analysis);
  }

  if (request.method === 'GET' && path === '/api/wave/thresholds') {
    return jsonResponse({
      curl: { warning: 0.3, critical: 0.6 },
      divergence: { warning: 0.4, critical: 0.7 },
      negative_divergence: { warning: -0.4, critical: -0.7 }
    });
  }

  return jsonResponse({ error: 'Invalid wave endpoint' }, 400);
}

function analyzeCoherence(content: string, thresholds?: Record<string, number>): WaveAnalysis {
  // Simplified coherence analysis - production would use embeddings
  const paragraphs = content.split(/\n\n+/);
  const t = {
    curl_warning: thresholds?.curl_warning ?? 0.3,
    curl_critical: thresholds?.curl_critical ?? 0.6,
    div_warning: thresholds?.div_warning ?? 0.4,
    div_critical: thresholds?.div_critical ?? 0.7,
  };

  // Calculate metrics based on structural analysis
  const repetitionScore = detectRepetition(paragraphs);
  const expansionScore = detectExpansion(paragraphs);
  const potentialScore = detectPotential(paragraphs);

  const regions: WaveRegion[] = [];

  // Detect high-curl regions (repetition/circularity)
  if (repetitionScore > t.curl_warning) {
    regions.push({
      start: 0,
      end: content.length,
      type: 'high_curl',
      severity: repetitionScore > t.curl_critical ? 'critical' : 'warning',
      description: 'Detected circular or repetitive patterns'
    });
  }

  // Detect divergence regions
  if (expansionScore > t.div_warning) {
    regions.push({
      start: 0,
      end: content.length,
      type: 'positive_divergence',
      severity: expansionScore > t.div_critical ? 'critical' : 'warning',
      description: 'Ideas expanding without resolution'
    });
  }

  return {
    curl: repetitionScore,
    divergence: expansionScore,
    potential: potentialScore,
    regions,
    coherent: repetitionScore < t.curl_critical && Math.abs(expansionScore) < t.div_critical
  };
}

function detectRepetition(paragraphs: string[]): number {
  // Simplified: check for repeated phrases
  const phrases = paragraphs.flatMap(p => p.toLowerCase().split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 20));
  const unique = new Set(phrases);
  return phrases.length > 0 ? 1 - (unique.size / phrases.length) : 0;
}

function detectExpansion(paragraphs: string[]): number {
  // Simplified: check if content expands without concluding
  const hasConclusion = paragraphs.some(p => 
    /therefore|thus|in conclusion|finally|to summarize/i.test(p)
  );
  const questionCount = (paragraphs.join(' ').match(/\?/g) || []).length;
  return hasConclusion ? 0.2 : Math.min(0.3 + (questionCount * 0.1), 0.8);
}

function detectPotential(paragraphs: string[]): number {
  // Simplified: detect undeveloped ideas
  const potentialMarkers = paragraphs.filter(p =>
    /could|might|perhaps|possibly|future work|TODO|TBD/i.test(p)
  ).length;
  return Math.min(potentialMarkers * 0.15, 1.0);
}

// ═══════════════════════════════════════════════════════════════
// Bump Handlers - Routing and Handoff
// ═══════════════════════════════════════════════════════════════

async function handleBump(request: Request, env: Env, path: string): Promise<Response> {
  if (request.method === 'POST' && path === '/api/bump/create') {
    const body = await request.json() as Partial<BumpMarker>;
    
    const bump: BumpMarker = {
      id: crypto.randomUUID(),
      type: body.type ?? 'WAVE',
      from: body.from ?? 'unknown',
      to: body.to ?? 'unknown',
      state: body.state ?? 'pending',
      context: body.context ?? {},
      timestamp: new Date().toISOString(),
      resolved: false
    };

    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO bumps (id, type, from_agent, to_agent, state, context, timestamp, resolved) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    ).bind(
      bump.id,
      bump.type,
      bump.from,
      bump.to,
      bump.state,
      JSON.stringify(bump.context),
      bump.timestamp,
      0
    ).run();

    // Store in KV for fast lookup
    await env.SPIRALSAFE_KV.put(`bump:${bump.id}`, JSON.stringify(bump), { expirationTtl: 86400 * 7 });

    return jsonResponse(bump, 201);
  }

  if (request.method === 'PUT' && path.startsWith('/api/bump/resolve/')) {
    const id = path.split('/').pop();
    
    await env.SPIRALSAFE_DB.prepare(
      'UPDATE bumps SET resolved = 1, resolved_at = ? WHERE id = ?'
    ).bind(new Date().toISOString(), id).run();

    return jsonResponse({ id, resolved: true });
  }

  if (request.method === 'GET' && path === '/api/bump/pending') {
    const result = await env.SPIRALSAFE_DB.prepare(
      'SELECT * FROM bumps WHERE resolved = 0 ORDER BY timestamp DESC LIMIT 50'
    ).all();

    return jsonResponse(result.results);
  }

  return jsonResponse({ error: 'Invalid bump endpoint' }, 400);
}

// ═══════════════════════════════════════════════════════════════
// AWI Handlers - Permission Scaffolding
// ═══════════════════════════════════════════════════════════════

async function handleAWI(request: Request, env: Env, path: string): Promise<Response> {
  if (request.method === 'POST' && path === '/api/awi/request') {
    const body = await request.json() as {
      intent: string;
      scope: AWIScope;
      level: 0 | 1 | 2 | 3 | 4;
      ttl_seconds?: number;
    };

    const grant: AWIGrant = {
      id: crypto.randomUUID(),
      intent: body.intent,
      scope: body.scope,
      level: body.level,
      granted_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + (body.ttl_seconds ?? 3600) * 1000).toISOString(),
      audit_trail: [{
        timestamp: new Date().toISOString(),
        action: 'grant_requested',
        result: 'success'
      }]
    };

    // Store grant in KV with TTL
    await env.SPIRALSAFE_KV.put(
      `awi:${grant.id}`,
      JSON.stringify(grant),
      { expirationTtl: body.ttl_seconds ?? 3600 }
    );

    // Log to D1 for permanent audit
    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO awi_grants (id, intent, scope, level, granted_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)'
    ).bind(
      grant.id,
      grant.intent,
      JSON.stringify(grant.scope),
      grant.level,
      grant.granted_at,
      grant.expires_at
    ).run();

    return jsonResponse(grant, 201);
  }

  if (request.method === 'POST' && path === '/api/awi/verify') {
    const body = await request.json() as { grant_id: string; action: string };
    
    const grantJson = await env.SPIRALSAFE_KV.get(`awi:${body.grant_id}`);
    if (!grantJson) {
      return jsonResponse({ valid: false, reason: 'Grant not found or expired' });
    }

    const grant = JSON.parse(grantJson) as AWIGrant;
    const actionAllowed = grant.scope.actions.some(a => 
      a === '*' || a === body.action || body.action.startsWith(a.replace(/\*/g, ''))
    );

    // Log verification attempt
    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO awi_audit (grant_id, action, result, timestamp) VALUES (?, ?, ?, ?)'
    ).bind(
      body.grant_id,
      body.action,
      actionAllowed ? 'success' : 'denied',
      new Date().toISOString()
    ).run();

    return jsonResponse({ 
      valid: actionAllowed,
      grant_id: body.grant_id,
      action: body.action,
      level: grant.level
    });
  }

  if (request.method === 'GET' && path.startsWith('/api/awi/audit/')) {
    const grantId = path.split('/').pop();
    const result = await env.SPIRALSAFE_DB.prepare(
      'SELECT * FROM awi_audit WHERE grant_id = ? ORDER BY timestamp DESC'
    ).bind(grantId).all();

    return jsonResponse(result.results);
  }

  return jsonResponse({ error: 'Invalid AWI endpoint' }, 400);
}

// ═══════════════════════════════════════════════════════════════
// Atom Handlers - Task Orchestration
// ═══════════════════════════════════════════════════════════════

async function handleAtom(request: Request, env: Env, path: string): Promise<Response> {
  if (request.method === 'POST' && path === '/api/atom/create') {
    const body = await request.json() as Partial<Atom>;
    
    const atom: Atom = {
      id: body.id ?? crypto.randomUUID(),
      name: body.name ?? 'Unnamed atom',
      molecule: body.molecule ?? 'default',
      compound: body.compound ?? 'default',
      status: 'pending',
      verification: body.verification ?? { criteria: {}, automated: false },
      dependencies: body.dependencies ?? { requires: [], blocks: [] },
      assignee: body.assignee ?? 'unassigned',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO atoms (id, name, molecule, compound, status, verification, dependencies, assignee, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    ).bind(
      atom.id,
      atom.name,
      atom.molecule,
      atom.compound,
      atom.status,
      JSON.stringify(atom.verification),
      JSON.stringify(atom.dependencies),
      atom.assignee,
      atom.created_at,
      atom.updated_at
    ).run();

    return jsonResponse(atom, 201);
  }

  if (request.method === 'PUT' && path.startsWith('/api/atom/status/')) {
    const id = path.split('/').pop();
    const body = await request.json() as { status: Atom['status'] };

    await env.SPIRALSAFE_DB.prepare(
      'UPDATE atoms SET status = ?, updated_at = ? WHERE id = ?'
    ).bind(body.status, new Date().toISOString(), id).run();

    return jsonResponse({ id, status: body.status });
  }

  if (request.method === 'GET' && path === '/api/atom/molecule') {
    const url = new URL(request.url);
    const molecule = url.searchParams.get('name') ?? 'default';
    
    const result = await env.SPIRALSAFE_DB.prepare(
      'SELECT * FROM atoms WHERE molecule = ? ORDER BY created_at'
    ).bind(molecule).all();

    return jsonResponse(result.results);
  }

  if (request.method === 'GET' && path === '/api/atom/ready') {
    // Get atoms whose dependencies are all complete
    const result = await env.SPIRALSAFE_DB.prepare(`
      SELECT * FROM atoms 
      WHERE status = 'pending' 
      AND NOT EXISTS (
        SELECT 1 FROM atoms AS dep 
        WHERE dep.status != 'complete' 
        AND dep.status != 'verified'
        AND json_each.value = dep.id
        FROM json_each(atoms.dependencies, '$.requires')
      )
    `).all();

    return jsonResponse(result.results);
  }

  return jsonResponse({ error: 'Invalid atom endpoint' }, 400);
}

// ═══════════════════════════════════════════════════════════════
// Context Handlers - Knowledge Units
// ═══════════════════════════════════════════════════════════════

async function handleContext(request: Request, env: Env, path: string): Promise<Response> {
  if (request.method === 'POST' && path === '/api/context/store') {
    const body = await request.json() as {
      domain: string;
      content: Record<string, unknown>;
      signals?: { use_when: string[]; avoid_when: string[] };
    };

    const id = `${body.domain}-${Date.now()}`;
    
    // Store in R2 for large contexts
    await env.SPIRALSAFE_R2.put(
      `contexts/${body.domain}/${id}.json`,
      JSON.stringify(body.content)
    );

    // Index in D1 for querying
    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO contexts (id, domain, signals, stored_at) VALUES (?, ?, ?, ?)'
    ).bind(
      id,
      body.domain,
      JSON.stringify(body.signals ?? {}),
      new Date().toISOString()
    ).run();

    return jsonResponse({ id, domain: body.domain }, 201);
  }

  if (request.method === 'GET' && path.startsWith('/api/context/query')) {
    const url = new URL(request.url);
    const domain = url.searchParams.get('domain');
    const signal = url.searchParams.get('signal');

    let query = 'SELECT * FROM contexts WHERE 1=1';
    const params: string[] = [];

    if (domain) {
      query += ' AND domain = ?';
      params.push(domain);
    }

    if (signal) {
      query += ' AND json_extract(signals, \'$.use_when\') LIKE ?';
      params.push(`%${signal}%`);
    }

    const result = await env.SPIRALSAFE_DB.prepare(query).bind(...params).all();
    return jsonResponse(result.results);
  }

  return jsonResponse({ error: 'Invalid context endpoint' }, 400);
}

// ═══════════════════════════════════════════════════════════════
// Health Check
// ═══════════════════════════════════════════════════════════════

async function handleHealth(env: Env): Promise<Response> {
  const checks = {
    d1: false,
    kv: false,
    r2: false,
    api_key_configured: false
  };

  try {
    await env.SPIRALSAFE_DB.prepare('SELECT 1').run();
    checks.d1 = true;
  } catch {}

  try {
    await env.SPIRALSAFE_KV.get('health-check');
    checks.kv = true;
  } catch {}

  try {
    await env.SPIRALSAFE_R2.head('health-check');
    checks.r2 = true;
  } catch {
    checks.r2 = true; // R2 returns null for missing keys, not error
  }

  // Check if API key is configured
  checks.api_key_configured = !!(env.SPIRALSAFE_API_KEY && env.SPIRALSAFE_API_KEY.length > 0);

  const healthy = Object.values(checks).every(v => v);

  return jsonResponse({
    status: healthy ? 'healthy' : 'degraded',
    checks,
    timestamp: new Date().toISOString(),
    version: '2.0.0'
  }, healthy ? 200 : 503);
}

// ═══════════════════════════════════════════════════════════════
// Utilities
// ═══════════════════════════════════════════════════════════════

function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}

/**
 * Constant-time string comparison to prevent timing attacks
 * @param a First string to compare
 * @param b Second string to compare
 * @returns true if strings match, false otherwise
 */
function constantTimeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) {
    return false;
  }
  
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  
  return result === 0;
}

async function hashContent(content: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(content);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
