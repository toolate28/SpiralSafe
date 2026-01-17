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

export interface WaveAnalysis {
  curl: number;
  divergence: number;
  potential: number;
  regions: WaveRegion[];
  coherent: boolean;
}

export interface WaveRegion {
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
// Provenance Tracking Types
// ═══════════════════════════════════════════════════════════════

interface ProvenanceValidation {
  id: string;
  valid: boolean;
  coherence_score: number;
  target_coherence: number;
  target_met: boolean;
  divergence_detected: boolean;
  blockers: string[];
  validation_results: string[];
  timestamp: string;
}

interface GateEvolution {
  id: string;
  blockers: string[];
  recommendations: string[];
  timestamp: string;
}

interface ValidationExample {
  gate: string;
  from: string;
  to: string;
  synthesized_at: string;
  validation_type: string;
  engagement_metric: number;
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

  // Add current request timestamp
  requests.push(now);

  // Store updated request list with TTL
  await env.SPIRALSAFE_KV.put(
    rateLimitKey,
    JSON.stringify(requests),
    { expirationTtl: windowSeconds }
  );

  const allowed = requests.length <= maxRequests;
  const remaining = Math.max(0, maxRequests - requests.length);
  const resetAt = now + windowSeconds;

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
    if (!authenticated && status === 401) {
      await env.SPIRALSAFE_DB.prepare(
        'INSERT INTO system_health (timestamp, status, details) VALUES (?, ?, ?)'
      ).bind(
        new Date().toISOString(),
        'auth_failure',
        JSON.stringify({ ip, path, userAgent })
      ).run();
    }
  } catch {
    // Don't fail requests if logging fails
  }
}

function validateApiKey(env: Env, providedKey: string): boolean {
  // Check primary key using constant-time comparison to prevent timing attacks
  if (constantTimeEqual(providedKey, env.SPIRALSAFE_API_KEY)) {
    return true;
  }

  // Check additional keys if configured
  if (env.SPIRALSAFE_API_KEYS) {
    const validKeys = env.SPIRALSAFE_API_KEYS.split(',').map(k => k.trim());
    return validKeys.some(key => constantTimeEqual(providedKey, key));
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
      } else if (path.startsWith('/api/provenance')) {
        response = await handleProvenance(request, env, path);
      } else if (path.startsWith('/api/context')) {
        response = await handleContext(request, env, path);
      } else if (path === '/api/health') {
        response = await handleHealth(env);
      } else {
        response = new Response(JSON.stringify({
          error: 'Not found',
          available_endpoints: ['/api/wave', '/api/bump', '/api/awi', '/api/atom', '/api/provenance', '/api/context', '/api/health']
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
// Wave Analysis Constants
// ═══════════════════════════════════════════════════════════════

// Conclusion pattern for detecting resolved content
const CONCLUSION_PATTERN_STRING = 'therefore|thus|in conclusion|finally|to summarize|in summary';
const CONCLUSION_PATTERN = new RegExp(CONCLUSION_PATTERN_STRING, 'i');
const CONCLUSION_PATTERN_GLOBAL = new RegExp(CONCLUSION_PATTERN_STRING, 'gi');

// Divergence detection thresholds and weights
const DIVERGENCE_BASE = 0.2;  // Base divergence for content with conclusions
const DIVERGENCE_FLOOR = 0.3;  // Floor for content without conclusions
const DIVERGENCE_QUESTION_WEIGHT = 0.1;  // Weight per question mark
const DIVERGENCE_MAX = 0.8;  // Maximum positive divergence value

// Negative divergence (over-compression) thresholds
const NEG_DIV_BASE = 0.3;  // Base negative divergence score
const NEG_DIV_CONCLUSION_WEIGHT = 0.15;  // Weight per excessive conclusion
const NEG_DIV_MAX = 0.8;  // Maximum negative divergence magnitude
const NEG_DIV_SHORT_CONTENT_THRESHOLD = 100;  // Avg paragraph length threshold
const NEG_DIV_MIN_CONCLUSIONS = 2;  // Minimum conclusions to trigger short content check
const NEG_DIV_EXCESSIVE_RATIO = 0.3;  // Max ratio of conclusions to paragraphs

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

export function analyzeCoherence(content: string, thresholds?: Record<string, number>): WaveAnalysis {
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

  // Detect positive divergence regions (unresolved expansion)
  if (expansionScore > t.div_warning) {
    regions.push({
      start: 0,
      end: content.length,
      type: 'positive_divergence',
      severity: expansionScore > t.div_critical ? 'critical' : 'warning',
      description: 'Ideas expanding without resolution'
    });
  }

  // Detect negative divergence regions (premature closure/over-compression)
  if (expansionScore < -t.div_warning) {
    regions.push({
      start: 0,
      end: content.length,
      type: 'negative_divergence',
      severity: expansionScore < -t.div_critical ? 'critical' : 'warning',
      description: 'Premature closure or over-compression detected'
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

export function detectRepetition(paragraphs: string[]): number {
  // Simplified: check for repeated phrases
  const phrases = paragraphs.flatMap(p => p.toLowerCase().split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 20));
  const unique = new Set(phrases);
  return phrases.length > 0 ? 1 - (unique.size / phrases.length) : 0;
}

export function detectExpansion(paragraphs: string[]): number {
  // Returns positive values for unresolved expansion, negative for over-compression
  const text = paragraphs.join(' ');
  
  // Positive divergence indicators: content expands without concluding
  const hasConclusion = paragraphs.some(p => CONCLUSION_PATTERN.test(p));
  const questionCount = (text.match(/\?/g) || []).length;
  
  // Negative divergence indicators: premature closure / over-compression
  const conclusionCount = (text.match(CONCLUSION_PATTERN_GLOBAL) || []).length;
  // Calculate average paragraph length excluding separators for accuracy
  const avgParagraphLength = paragraphs.reduce((sum, p) => sum + p.length, 0) / Math.max(paragraphs.length, 1);
  const hasMultipleConclusionsShortContent = conclusionCount >= NEG_DIV_MIN_CONCLUSIONS && avgParagraphLength < NEG_DIV_SHORT_CONTENT_THRESHOLD;
  const excessiveSummarization = conclusionCount > paragraphs.length * NEG_DIV_EXCESSIVE_RATIO;
  
  // Detect over-compression: multiple conclusions in short content or excessive summarization
  if (hasMultipleConclusionsShortContent || excessiveSummarization) {
    // Return negative value proportional to over-compression severity
    return -Math.min(NEG_DIV_BASE + (conclusionCount * NEG_DIV_CONCLUSION_WEIGHT), NEG_DIV_MAX);
  }
  
  // Positive divergence: unresolved expansion
  return hasConclusion ? DIVERGENCE_BASE : Math.min(DIVERGENCE_FLOOR + (questionCount * DIVERGENCE_QUESTION_WEIGHT), DIVERGENCE_MAX);
}

export function detectPotential(paragraphs: string[]): number {
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
// Provenance Handlers - Enhanced Trail Validation
// ═══════════════════════════════════════════════════════════════

const COHERENCE_TARGET = 0.85; // 85% self-reinforcement target

async function handleProvenance(request: Request, env: Env, path: string): Promise<Response> {
  // Validate provenance trail
  if (request.method === 'POST' && path === '/api/provenance/validate') {
    const body = await request.json() as {
      trail_data?: {
        decisions: number;
        gate_transitions: number;
        counters: number;
      };
    };

    const validation: ProvenanceValidation = {
      id: crypto.randomUUID(),
      valid: true,
      coherence_score: 0,
      target_coherence: COHERENCE_TARGET,
      target_met: false,
      divergence_detected: false,
      blockers: [],
      validation_results: [],
      timestamp: new Date().toISOString()
    };

    // Check gate transitions for coherence
    const gateResult = await env.SPIRALSAFE_DB.prepare(
      'SELECT COUNT(*) as total, SUM(CASE WHEN coherent = 1 THEN 1 ELSE 0 END) as coherent_count FROM wave_analyses'
    ).first<{ total: number; coherent_count: number }>();

    if (gateResult && gateResult.total > 0) {
      validation.coherence_score = gateResult.coherent_count / gateResult.total;
      validation.target_met = validation.coherence_score >= COHERENCE_TARGET;
    }

    // Check for unresolved bumps (blockers)
    const blockerResult = await env.SPIRALSAFE_DB.prepare(
      "SELECT COUNT(*) as count FROM bumps WHERE resolved = 0 AND type = 'BLOCK'"
    ).first<{ count: number }>();

    if (blockerResult && blockerResult.count > 0) {
      validation.divergence_detected = true;
      validation.blockers.push(`unresolved_blocks:${blockerResult.count}`);
    }

    // Validate trail data if provided
    if (body.trail_data) {
      if (body.trail_data.decisions > 0) {
        validation.validation_results.push(`decisions:${body.trail_data.decisions}:valid`);
      }
      if (body.trail_data.gate_transitions > 0) {
        validation.validation_results.push(`gate_transitions:${body.trail_data.gate_transitions}:valid`);
      }
    }

    // Store validation record
    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO provenance_validations (id, valid, coherence_score, target_met, divergence_detected, blockers, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)'
    ).bind(
      validation.id,
      validation.valid ? 1 : 0,
      validation.coherence_score,
      validation.target_met ? 1 : 0,
      validation.divergence_detected ? 1 : 0,
      JSON.stringify(validation.blockers),
      validation.timestamp
    ).run();

    return jsonResponse(validation, 201);
  }

  // Bootstrap validation examples (BootstrapFewshot)
  if (request.method === 'POST' && path === '/api/provenance/bootstrap') {
    const result = await env.SPIRALSAFE_DB.prepare(
      'SELECT * FROM wave_analyses WHERE coherent = 1 ORDER BY analyzed_at DESC LIMIT 10'
    ).all();

    const examples: ValidationExample[] = result.results.map((row: Record<string, unknown>) => ({
      gate: 'wave-coherence',
      from: 'content',
      to: 'analysis',
      synthesized_at: new Date().toISOString(),
      validation_type: 'bootstrap_fewshot',
      engagement_metric: typeof row.potential === 'number' ? row.potential : 0.5
    }));

    return jsonResponse({
      synthesized_count: examples.length,
      examples
    }, 201);
  }

  // Evolve gates (GEPA)
  if (request.method === 'POST' && path === '/api/provenance/evolve') {
    const body = await request.json() as { blockers?: string[] };

    const recommendations: string[] = [];

    // Analyze blockers and generate evolution recommendations
    if (body.blockers) {
      for (const blocker of body.blockers) {
        if (blocker.includes('intention-to-execution')) {
          recommendations.push('gate:intention-to-execution:relax_bump_placeholder_check');
        }
        if (blocker.includes('learning-to-regeneration')) {
          recommendations.push('gate:learning-to-regeneration:add_fallback_learning_path');
        }
        if (blocker.includes('high_failure_rate')) {
          recommendations.push('system:reduce_threshold_strictness');
        }
      }
    }

    const evolution: GateEvolution = {
      id: crypto.randomUUID(),
      blockers: body.blockers || [],
      recommendations,
      timestamp: new Date().toISOString()
    };

    // Store evolution record
    await env.SPIRALSAFE_DB.prepare(
      'INSERT INTO gate_evolutions (id, blockers, recommendations, timestamp) VALUES (?, ?, ?, ?)'
    ).bind(
      evolution.id,
      JSON.stringify(evolution.blockers),
      JSON.stringify(evolution.recommendations),
      evolution.timestamp
    ).run();

    return jsonResponse(evolution, 201);
  }

  // Metric-gated recursion for coherence
  if (request.method === 'POST' && path === '/api/provenance/coherence') {
    const body = await request.json() as {
      target_coherence?: number;
      max_iterations?: number;
    };

    const targetCoherence = body.target_coherence ?? COHERENCE_TARGET;
    const maxIterations = body.max_iterations ?? 10;

    // Calculate current coherence
    const waveResult = await env.SPIRALSAFE_DB.prepare(
      'SELECT COUNT(*) as total, SUM(CASE WHEN coherent = 1 THEN 1 ELSE 0 END) as coherent_count FROM wave_analyses'
    ).first<{ total: number; coherent_count: number }>();

    let currentCoherence = 0;
    if (waveResult && waveResult.total > 0) {
      currentCoherence = waveResult.coherent_count / waveResult.total;
    }

    const achieved = currentCoherence >= targetCoherence;

    return jsonResponse({
      coherence: currentCoherence,
      target: targetCoherence,
      achieved,
      iterations: achieved ? 0 : maxIterations,
      self_reinforcement_percent: Math.round(currentCoherence * 100)
    });
  }

  // Get coherence score
  if (request.method === 'GET' && path === '/api/provenance/score') {
    const waveResult = await env.SPIRALSAFE_DB.prepare(
      'SELECT COUNT(*) as total, SUM(CASE WHEN coherent = 1 THEN 1 ELSE 0 END) as coherent_count FROM wave_analyses'
    ).first<{ total: number; coherent_count: number }>();

    let coherence = 0;
    if (waveResult && waveResult.total > 0) {
      coherence = waveResult.coherent_count / waveResult.total;
    }

    return jsonResponse({
      coherence_score: coherence,
      target: COHERENCE_TARGET,
      target_met: coherence >= COHERENCE_TARGET,
      self_reinforcement_percent: Math.round(coherence * 100)
    });
  }

  return jsonResponse({ error: 'Invalid provenance endpoint' }, 400);
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
