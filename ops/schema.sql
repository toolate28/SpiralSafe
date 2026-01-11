-- SpiralSafe Database Schema
-- Version: 3.0.0-quantum
-- Database: Cloudflare D1 (SQLite)
-- H&&S:WAVE Protocol | From the constraints, gifts. From the spiral, safety.

-- ============================================================================
-- Table 1: wave_analyses
-- Purpose: Store H&&S:WAVE protocol coherence analysis results
-- ============================================================================
CREATE TABLE IF NOT EXISTS wave_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_hash TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    curl REAL NOT NULL,              -- Repetition metric (0.0 - 1.0)
    divergence REAL NOT NULL,        -- Expansion metric (0.0 - 1.0)
    potential REAL NOT NULL,         -- Undeveloped ideas metric (0.0 - 1.0)
    coherence_score REAL NOT NULL,   -- Overall coherence (0.0 - 1.0)
    coherent BOOLEAN NOT NULL,       -- TRUE if score >= 0.70
    analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT                    -- JSON: additional analysis data
);

CREATE INDEX IF NOT EXISTS idx_wave_analyses_hash ON wave_analyses(content_hash);
CREATE INDEX IF NOT EXISTS idx_wave_analyses_coherent ON wave_analyses(coherent);
CREATE INDEX IF NOT EXISTS idx_wave_analyses_timestamp ON wave_analyses(analyzed_at);

-- ============================================================================
-- Table 2: bumps
-- Purpose: State transition markers for cross-platform handoffs
-- ============================================================================
CREATE TABLE IF NOT EXISTS bumps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bump_id TEXT NOT NULL UNIQUE,
    source_platform TEXT NOT NULL,   -- e.g., "claude-code", "web-ui"
    target_platform TEXT,            -- Where this is going
    state TEXT NOT NULL,             -- "pending", "acknowledged", "completed"
    data TEXT NOT NULL,              -- JSON: payload being transferred
    context_ref TEXT,                -- Reference to related context
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    metadata TEXT                    -- JSON: additional bump data
);

CREATE INDEX IF NOT EXISTS idx_bumps_id ON bumps(bump_id);
CREATE INDEX IF NOT EXISTS idx_bumps_state ON bumps(state);
CREATE INDEX IF NOT EXISTS idx_bumps_source ON bumps(source_platform);
CREATE INDEX IF NOT EXISTS idx_bumps_created ON bumps(created_at);

-- ============================================================================
-- Table 3: awi_grants
-- Purpose: Authority-With-Intent permission scaffolding
-- ============================================================================
CREATE TABLE IF NOT EXISTS awi_grants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_id TEXT NOT NULL UNIQUE,
    authority TEXT NOT NULL,         -- Who grants authority (e.g., "ptolemy")
    intent TEXT NOT NULL,            -- Purpose of authority
    scope TEXT NOT NULL,             -- What's covered (JSON array)
    level INTEGER NOT NULL,          -- 0-4: visibility, readonly, limited_write, full_write, admin
    granted_to TEXT,                 -- Who receives authority (user/system)
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    revoked_at DATETIME,
    metadata TEXT                    -- JSON: additional grant data
);

CREATE INDEX IF NOT EXISTS idx_awi_grants_id ON awi_grants(grant_id);
CREATE INDEX IF NOT EXISTS idx_awi_grants_authority ON awi_grants(authority);
CREATE INDEX IF NOT EXISTS idx_awi_grants_level ON awi_grants(level);
CREATE INDEX IF NOT EXISTS idx_awi_grants_expires ON awi_grants(expires_at);

-- ============================================================================
-- Table 4: awi_audit
-- Purpose: Audit trail for AWI grant operations and authentication failures
-- ============================================================================
CREATE TABLE IF NOT EXISTS awi_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,        -- "grant_created", "grant_used", "grant_revoked", "auth_failed"
    grant_id TEXT,                   -- Reference to awi_grants.grant_id
    authority TEXT,
    action TEXT NOT NULL,            -- What was attempted
    result TEXT NOT NULL,            -- "success", "denied", "failed"
    ip_address TEXT,
    user_agent TEXT,
    request_details TEXT,            -- JSON: full request context
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_awi_audit_event ON awi_audit(event_type);
CREATE INDEX IF NOT EXISTS idx_awi_audit_grant ON awi_audit(grant_id);
CREATE INDEX IF NOT EXISTS idx_awi_audit_result ON awi_audit(result);
CREATE INDEX IF NOT EXISTS idx_awi_audit_ip ON awi_audit(ip_address);
CREATE INDEX IF NOT EXISTS idx_awi_audit_timestamp ON awi_audit(timestamp);

-- ============================================================================
-- Table 5: atoms
-- Purpose: Task orchestration with dependency tracking
-- ============================================================================
CREATE TABLE IF NOT EXISTS atoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atom_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    state TEXT NOT NULL,             -- "pending", "in_progress", "blocked", "completed", "failed"
    dependencies TEXT,               -- JSON array: [atom_id1, atom_id2, ...]
    verification_criteria TEXT,      -- JSON: how to verify completion
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    completed_at DATETIME,
    verified_at DATETIME,
    metadata TEXT                    -- JSON: additional atom data
);

CREATE INDEX IF NOT EXISTS idx_atoms_id ON atoms(atom_id);
CREATE INDEX IF NOT EXISTS idx_atoms_state ON atoms(state);
CREATE INDEX IF NOT EXISTS idx_atoms_created ON atoms(created_at);

-- ============================================================================
-- Table 6: contexts
-- Purpose: Hierarchical context storage with Merkle tree verification
-- ============================================================================
CREATE TABLE IF NOT EXISTS contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    context_id TEXT NOT NULL UNIQUE,
    parent_id TEXT,                  -- Reference to parent context_id
    name TEXT NOT NULL,
    content TEXT NOT NULL,           -- Context data or R2 reference
    content_hash TEXT NOT NULL,      -- SHA-256 of content
    merkle_root TEXT,                -- Merkle root including all children
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,                   -- JSON: additional context data
    FOREIGN KEY (parent_id) REFERENCES contexts(context_id)
);

CREATE INDEX IF NOT EXISTS idx_contexts_id ON contexts(context_id);
CREATE INDEX IF NOT EXISTS idx_contexts_parent ON contexts(parent_id);
CREATE INDEX IF NOT EXISTS idx_contexts_hash ON contexts(content_hash);
CREATE INDEX IF NOT EXISTS idx_contexts_merkle ON contexts(merkle_root);

-- ============================================================================
-- Table 7: system_health
-- Purpose: System monitoring and health checks
-- ============================================================================
CREATE TABLE IF NOT EXISTS system_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component TEXT NOT NULL,         -- "api", "database", "kv", "r2", "auth"
    status TEXT NOT NULL,            -- "healthy", "degraded", "down"
    response_time_ms INTEGER,
    error_message TEXT,
    checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT                    -- JSON: additional health data
);

CREATE INDEX IF NOT EXISTS idx_system_health_component ON system_health(component);
CREATE INDEX IF NOT EXISTS idx_system_health_status ON system_health(status);
CREATE INDEX IF NOT EXISTS idx_system_health_timestamp ON system_health(checked_at);

-- ============================================================================
-- Sample Data (Optional - for development/testing)
-- ============================================================================

-- Example WAVE analysis
INSERT OR IGNORE INTO wave_analyses (content_hash, content, curl, divergence, potential, coherence_score, coherent)
VALUES (
    'sample_hash_001',
    'From the constraints, gifts. From the spiral, safety.',
    0.08,
    0.28,
    0.45,
    0.89,
    1
);

-- Example AWI grant
INSERT OR IGNORE INTO awi_grants (grant_id, authority, intent, scope, level, granted_to)
VALUES (
    'grant_ptolemy_001',
    'ptolemy',
    'System administration and deployment',
    '["api", "database", "auth", "deployment"]',
    4,  -- admin level
    'ptolemy@spiralsafe.org'
);

-- Example ATOM session
INSERT OR IGNORE INTO atoms (atom_id, name, description, state, dependencies, verification_criteria)
VALUES (
    'atom_deploy_001',
    'Deploy API to production',
    'Deploy SpiralSafe API to Cloudflare Workers',
    'pending',
    '[]',
    '{"health_check": "https://api.spiralsafe.org/health", "expected_status": 200}'
);

-- System health baseline
INSERT OR IGNORE INTO system_health (component, status, response_time_ms)
VALUES
    ('api', 'healthy', 15),
    ('database', 'healthy', 8),
    ('kv', 'healthy', 2),
    ('r2', 'healthy', 12),
    ('auth', 'healthy', 5);

-- ============================================================================
-- Views (Optional - for common queries)
-- ============================================================================

-- Active (non-completed) atoms
CREATE VIEW IF NOT EXISTS active_atoms AS
SELECT * FROM atoms
WHERE state IN ('pending', 'in_progress', 'blocked')
ORDER BY created_at DESC;

-- Failed authentication attempts (last 7 days)
CREATE VIEW IF NOT EXISTS recent_auth_failures AS
SELECT * FROM awi_audit
WHERE event_type = 'auth_failed'
  AND timestamp >= datetime('now', '-7 days')
ORDER BY timestamp DESC;

-- Coherent wave analyses (score >= 0.70)
CREATE VIEW IF NOT EXISTS coherent_analyses AS
SELECT * FROM wave_analyses
WHERE coherent = 1
ORDER BY coherence_score DESC;

-- ============================================================================
-- Database Info
-- ============================================================================

-- To view schema info:
-- SELECT sql FROM sqlite_master WHERE type='table';

-- To view indexes:
-- SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='wave_analyses';

-- To check row counts:
-- SELECT 'wave_analyses' as table_name, COUNT(*) as rows FROM wave_analyses
-- UNION ALL
-- SELECT 'bumps', COUNT(*) FROM bumps
-- UNION ALL
-- SELECT 'awi_grants', COUNT(*) FROM awi_grants
-- UNION ALL
-- SELECT 'awi_audit', COUNT(*) FROM awi_audit
-- UNION ALL
-- SELECT 'atoms', COUNT(*) FROM atoms
-- UNION ALL
-- SELECT 'contexts', COUNT(*) FROM contexts
-- UNION ALL
-- SELECT 'system_health', COUNT(*) FROM system_health;

-- ============================================================================
-- End of Schema
-- ============================================================================
