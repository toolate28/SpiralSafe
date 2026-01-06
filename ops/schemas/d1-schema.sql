-- ═══════════════════════════════════════════════════════════════
-- SpiralSafe D1 Database Schema
-- Coherence engine persistent storage layer
-- ═══════════════════════════════════════════════════════════════

-- Wave Analysis Records
-- Tracks coherence measurements over time
CREATE TABLE IF NOT EXISTS wave_analyses (
    id TEXT PRIMARY KEY,
    content_hash TEXT NOT NULL,
    curl REAL NOT NULL,
    divergence REAL NOT NULL,
    potential REAL NOT NULL,
    coherent INTEGER NOT NULL DEFAULT 0,
    analyzed_at TEXT NOT NULL,
    source TEXT,
    metadata TEXT -- JSON
);

CREATE INDEX idx_wave_coherent ON wave_analyses(coherent);
CREATE INDEX idx_wave_analyzed ON wave_analyses(analyzed_at);
CREATE INDEX idx_wave_content ON wave_analyses(content_hash);

-- Bump Markers
-- Handoff and routing audit trail
CREATE TABLE IF NOT EXISTS bumps (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL CHECK (type IN ('WAVE', 'PASS', 'PING', 'SYNC', 'BLOCK')),
    from_agent TEXT NOT NULL,
    to_agent TEXT NOT NULL,
    state TEXT NOT NULL,
    context TEXT, -- JSON
    timestamp TEXT NOT NULL,
    resolved INTEGER NOT NULL DEFAULT 0,
    resolved_at TEXT,
    resolution_notes TEXT
);

CREATE INDEX idx_bump_resolved ON bumps(resolved);
CREATE INDEX idx_bump_type ON bumps(type);
CREATE INDEX idx_bump_agents ON bumps(from_agent, to_agent);
CREATE INDEX idx_bump_timestamp ON bumps(timestamp);

-- AWI Permission Grants
-- Authorization-With-Intent audit trail
CREATE TABLE IF NOT EXISTS awi_grants (
    id TEXT PRIMARY KEY,
    intent TEXT NOT NULL,
    scope TEXT NOT NULL, -- JSON: {resources, actions, time_limit, impact_limit}
    level INTEGER NOT NULL CHECK (level BETWEEN 0 AND 4),
    granted_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    granted_by TEXT,
    revoked INTEGER NOT NULL DEFAULT 0,
    revoked_at TEXT
);

CREATE INDEX idx_awi_level ON awi_grants(level);
CREATE INDEX idx_awi_expires ON awi_grants(expires_at);
CREATE INDEX idx_awi_revoked ON awi_grants(revoked);

-- AWI Audit Log
-- Every permission verification attempt
CREATE TABLE IF NOT EXISTS awi_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_id TEXT NOT NULL,
    action TEXT NOT NULL,
    resource TEXT,
    result TEXT NOT NULL CHECK (result IN ('success', 'denied', 'error', 'expired')),
    timestamp TEXT NOT NULL,
    details TEXT,
    FOREIGN KEY (grant_id) REFERENCES awi_grants(id)
);

CREATE INDEX idx_awi_audit_grant ON awi_audit(grant_id);
CREATE INDEX idx_awi_audit_result ON awi_audit(result);
CREATE INDEX idx_awi_audit_time ON awi_audit(timestamp);

-- Atoms (ATOM Task Units)
-- Minimal verifiable work units
CREATE TABLE IF NOT EXISTS atoms (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    molecule TEXT NOT NULL,
    compound TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'in_progress', 'blocked', 'complete', 'verified')),
    verification TEXT NOT NULL, -- JSON: {criteria, automated}
    dependencies TEXT NOT NULL, -- JSON: {requires, blocks}
    assignee TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT,
    verified_at TEXT,
    verification_evidence TEXT
);

CREATE INDEX idx_atom_status ON atoms(status);
CREATE INDEX idx_atom_molecule ON atoms(molecule);
CREATE INDEX idx_atom_compound ON atoms(compound);
CREATE INDEX idx_atom_assignee ON atoms(assignee);

-- Molecules (ATOM Task Groups)
-- Collections of atoms forming sub-goals
CREATE TABLE IF NOT EXISTS molecules (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    compound TEXT NOT NULL,
    description TEXT,
    success_criteria TEXT, -- JSON array
    created_at TEXT NOT NULL,
    completed_at TEXT
);

CREATE INDEX idx_molecule_compound ON molecules(compound);

-- Compounds (ATOM Projects)
-- Full project containers
CREATE TABLE IF NOT EXISTS compounds (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    goal TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('planning', 'active', 'paused', 'complete', 'archived')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_compound_status ON compounds(status);

-- Context Units
-- .context.yaml storage index
CREATE TABLE IF NOT EXISTS contexts (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    signals TEXT, -- JSON: {use_when, avoid_when}
    invariants TEXT, -- JSON array
    stored_at TEXT NOT NULL,
    updated_at TEXT,
    r2_path TEXT -- Reference to full content in R2
);

CREATE INDEX idx_context_domain ON contexts(domain);

-- SAIF Investigations
-- Systematic Analysis and Issue Fixing records
CREATE TABLE IF NOT EXISTS saif_investigations (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    phase TEXT NOT NULL CHECK (phase IN ('symptom', 'analysis', 'hypothesis', 'intervention', 'verification', 'documentation')),
    symptoms TEXT, -- JSON array
    analysis TEXT,
    hypotheses TEXT, -- JSON array with confidence scores
    selected_hypothesis TEXT,
    intervention TEXT,
    verification_result TEXT,
    documentation_ref TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    resolved_at TEXT
);

CREATE INDEX idx_saif_phase ON saif_investigations(phase);

-- UnifiedComms Message Log
-- Cross-channel communication audit
CREATE TABLE IF NOT EXISTS unified_messages (
    id TEXT PRIMARY KEY,
    channel TEXT NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
    content_hash TEXT NOT NULL,
    bump_marker TEXT, -- If message contains H&&S markers
    timestamp TEXT NOT NULL,
    metadata TEXT -- JSON: channel-specific data
);

CREATE INDEX idx_unified_channel ON unified_messages(channel);
CREATE INDEX idx_unified_timestamp ON unified_messages(timestamp);
CREATE INDEX idx_unified_bump ON unified_messages(bump_marker);

-- Agent Registry
-- Known agents for bump.md routing
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('human', 'ai', 'service', 'tool')),
    capabilities TEXT, -- JSON array
    endpoints TEXT, -- JSON: {channel: endpoint}
    created_at TEXT NOT NULL,
    last_seen TEXT
);

CREATE INDEX idx_agent_type ON agents(type);

-- ═══════════════════════════════════════════════════════════════
-- Views for Common Queries
-- ═══════════════════════════════════════════════════════════════

-- Active work summary
CREATE VIEW IF NOT EXISTS v_active_work AS
SELECT 
    c.name as compound,
    m.name as molecule,
    a.name as atom,
    a.status,
    a.assignee,
    a.updated_at
FROM atoms a
JOIN molecules m ON a.molecule = m.id
JOIN compounds c ON a.compound = c.id
WHERE a.status IN ('pending', 'in_progress', 'blocked')
ORDER BY a.updated_at DESC;

-- Pending bumps requiring attention
CREATE VIEW IF NOT EXISTS v_pending_bumps AS
SELECT 
    b.*,
    af.name as from_name,
    at.name as to_name
FROM bumps b
LEFT JOIN agents af ON b.from_agent = af.id
LEFT JOIN agents at ON b.to_agent = at.id
WHERE b.resolved = 0
ORDER BY b.timestamp DESC;

-- Recent coherence issues
CREATE VIEW IF NOT EXISTS v_coherence_issues AS
SELECT *
FROM wave_analyses
WHERE coherent = 0
ORDER BY analyzed_at DESC
LIMIT 100;

-- AWI grants expiring soon (within 1 hour)
CREATE VIEW IF NOT EXISTS v_expiring_grants AS
SELECT *
FROM awi_grants
WHERE revoked = 0
AND datetime(expires_at) <= datetime('now', '+1 hour')
AND datetime(expires_at) > datetime('now')
ORDER BY expires_at;
