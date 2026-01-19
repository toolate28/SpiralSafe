/**
 * ATOM Trail Persister
 * 
 * Foundational provenance logging system for all SpiralSafe/QDI decisions.
 * Implements JSON Lines storage for efficient append-only logging.
 * 
 * ATOM: ATOM-FEATURE-20260119-001-atom-trail-persister
 */

import * as fs from 'fs';
import * as path from 'path';

// ═══════════════════════════════════════════════════════════════
// Types
// ═══════════════════════════════════════════════════════════════

export interface ATOMEntry {
  timestamp: string;
  vortexId: string;
  decision: string;
  rationale: string;
  outcome: 'success' | 'failure' | 'pending';
  coherenceScore?: number;
  fibonacciWeight?: number;
  context: Record<string, unknown>;
  signature?: string;
}

export interface QueryOptions {
  vortexId?: string;
  startTime?: string;
  endTime?: string;
  outcome?: 'success' | 'failure' | 'pending';
  minCoherence?: number;
  limit?: number;
}

export interface ExportOptions {
  format: 'json' | 'csv' | 'markdown';
  filter?: QueryOptions;
}

export interface VisualizationData {
  nodes: VisualizationNode[];
  edges: VisualizationEdge[];
  format: 'svg' | 'mermaid';
}

export interface VisualizationNode {
  id: string;
  label: string;
  type: 'decision' | 'vortex' | 'cycle';
  outcome?: 'success' | 'failure' | 'pending';
  coherenceScore?: number;
}

export interface VisualizationEdge {
  from: string;
  to: string;
  label?: string;
}

// ═══════════════════════════════════════════════════════════════
// Core Functions
// ═══════════════════════════════════════════════════════════════

/**
 * Log an ATOM decision to the trail
 */
export async function logATOM(entry: ATOMEntry, trailPath?: string): Promise<void> {
  const filePath = trailPath || path.join(process.cwd(), '.spiralsafe', 'atom-trail.jsonl');
  
  // Ensure directory exists
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Validate entry
  validateEntry(entry);

  // Append to JSONL file
  const line = JSON.stringify(entry) + '\n';
  fs.appendFileSync(filePath, line, 'utf8');
}

/**
 * Query ATOM trail entries
 */
export async function queryATOM(options: QueryOptions = {}, trailPath?: string): Promise<ATOMEntry[]> {
  const filePath = trailPath || path.join(process.cwd(), '.spiralsafe', 'atom-trail.jsonl');

  if (!fs.existsSync(filePath)) {
    return [];
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n').filter((line: string) => line.trim());
  
  let entries = lines.map((line: string) => JSON.parse(line) as ATOMEntry);

  // Apply filters
  if (options.vortexId) {
    entries = entries.filter((e: ATOMEntry) => e.vortexId === options.vortexId);
  }

  if (options.startTime) {
    const startTime = options.startTime;
    entries = entries.filter((e: ATOMEntry) => e.timestamp >= startTime);
  }

  if (options.endTime) {
    const endTime = options.endTime;
    entries = entries.filter((e: ATOMEntry) => e.timestamp <= endTime);
  }

  if (options.outcome) {
    entries = entries.filter((e: ATOMEntry) => e.outcome === options.outcome);
  }

  if (options.minCoherence !== undefined) {
    const minCoherence = options.minCoherence;
    entries = entries.filter((e: ATOMEntry) => (e.coherenceScore ?? 0) >= minCoherence);
  }

  if (options.limit) {
    entries = entries.slice(0, options.limit);
  }

  return entries;
}

/**
 * Export ATOM trail in various formats
 */
export async function exportATOM(options: ExportOptions, trailPath?: string): Promise<string> {
  const entries = await queryATOM(options.filter || {}, trailPath);

  switch (options.format) {
    case 'json':
      return JSON.stringify(entries, null, 2);
    
    case 'csv':
      return entriesToCSV(entries);
    
    case 'markdown':
      return entriesToMarkdown(entries);
    
    default:
      throw new Error(`Unsupported export format: ${options.format}`);
  }
}

/**
 * Generate visualization data for ATOM trail
 */
export async function visualizeATOM(
  format: 'svg' | 'mermaid' = 'mermaid',
  filter?: QueryOptions,
  trailPath?: string
): Promise<VisualizationData> {
  const entries = await queryATOM(filter || {}, trailPath);

  const nodes: VisualizationNode[] = [];
  const edges: VisualizationEdge[] = [];
  const vortexMap = new Map<string, VisualizationNode>();

  // Create vortex nodes
  entries.forEach((entry, index) => {
    if (!vortexMap.has(entry.vortexId)) {
      const vortexNode: VisualizationNode = {
        id: `vortex-${entry.vortexId}`,
        label: `Vortex ${entry.vortexId}`,
        type: 'vortex'
      };
      vortexMap.set(entry.vortexId, vortexNode);
      nodes.push(vortexNode);
    }

    const decisionNode: VisualizationNode = {
      id: `decision-${index}`,
      label: entry.decision.substring(0, 30) + (entry.decision.length > 30 ? '...' : ''),
      type: 'decision',
      outcome: entry.outcome,
      coherenceScore: entry.coherenceScore
    };
    nodes.push(decisionNode);

    edges.push({
      from: `vortex-${entry.vortexId}`,
      to: `decision-${index}`,
      label: entry.outcome
    });
  });

  // Connect sequential decisions
  for (let i = 0; i < entries.length - 1; i++) {
    if (entries[i].vortexId === entries[i + 1].vortexId) {
      edges.push({
        from: `decision-${i}`,
        to: `decision-${i + 1}`,
        label: 'next'
      });
    }
  }

  // Detect 42-cycle patterns (Fibonacci-weighted decisions)
  const cycleNodes = detectCycles(entries);
  cycleNodes.forEach(node => nodes.push(node));

  return {
    nodes,
    edges,
    format
  };
}

/**
 * Get ATOM trail statistics
 */
export async function getTrailStats(trailPath?: string): Promise<{
  totalEntries: number;
  successCount: number;
  failureCount: number;
  pendingCount: number;
  avgCoherenceScore: number;
  vortexCount: number;
  oldestEntry?: string;
  newestEntry?: string;
}> {
  const entries = await queryATOM({}, trailPath);

  if (entries.length === 0) {
    return {
      totalEntries: 0,
      successCount: 0,
      failureCount: 0,
      pendingCount: 0,
      avgCoherenceScore: 0,
      vortexCount: 0
    };
  }

  const vortexes = new Set(entries.map(e => e.vortexId));
  const coherenceScores = entries
    .map(e => e.coherenceScore)
    .filter((score): score is number => score !== undefined);

  return {
    totalEntries: entries.length,
    successCount: entries.filter(e => e.outcome === 'success').length,
    failureCount: entries.filter(e => e.outcome === 'failure').length,
    pendingCount: entries.filter(e => e.outcome === 'pending').length,
    avgCoherenceScore: coherenceScores.length > 0
      ? coherenceScores.reduce((a, b) => a + b, 0) / coherenceScores.length
      : 0,
    vortexCount: vortexes.size,
    oldestEntry: entries[0]?.timestamp,
    newestEntry: entries[entries.length - 1]?.timestamp
  };
}

// ═══════════════════════════════════════════════════════════════
// Helper Functions
// ═══════════════════════════════════════════════════════════════

function validateEntry(entry: ATOMEntry): void {
  if (!entry.timestamp) {
    throw new Error('ATOM entry must have a timestamp');
  }
  if (!entry.vortexId) {
    throw new Error('ATOM entry must have a vortexId');
  }
  if (!entry.decision) {
    throw new Error('ATOM entry must have a decision');
  }
  if (!entry.rationale) {
    throw new Error('ATOM entry must have a rationale');
  }
  if (!['success', 'failure', 'pending'].includes(entry.outcome)) {
    throw new Error('ATOM entry outcome must be success, failure, or pending');
  }
}

function entriesToCSV(entries: ATOMEntry[]): string {
  const headers = [
    'timestamp',
    'vortexId',
    'decision',
    'rationale',
    'outcome',
    'coherenceScore',
    'fibonacciWeight',
    'signature'
  ];

  const rows = entries.map(entry => [
    entry.timestamp,
    entry.vortexId,
    `"${entry.decision.replace(/"/g, '""')}"`,
    `"${entry.rationale.replace(/"/g, '""')}"`,
    entry.outcome,
    entry.coherenceScore?.toString() || '',
    entry.fibonacciWeight?.toString() || '',
    entry.signature || ''
  ]);

  return [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
}

function entriesToMarkdown(entries: ATOMEntry[]): string {
  let markdown = '# ATOM Trail Export\n\n';
  markdown += `Total Entries: ${entries.length}\n\n`;

  entries.forEach((entry, index) => {
    markdown += `## Entry ${index + 1}\n\n`;
    markdown += `- **Timestamp**: ${entry.timestamp}\n`;
    markdown += `- **Vortex ID**: ${entry.vortexId}\n`;
    markdown += `- **Decision**: ${entry.decision}\n`;
    markdown += `- **Rationale**: ${entry.rationale}\n`;
    markdown += `- **Outcome**: ${entry.outcome}\n`;
    if (entry.coherenceScore !== undefined) {
      markdown += `- **Coherence Score**: ${entry.coherenceScore}\n`;
    }
    if (entry.fibonacciWeight !== undefined) {
      markdown += `- **Fibonacci Weight**: ${entry.fibonacciWeight}\n`;
    }
    if (entry.signature) {
      markdown += `- **Signature**: ${entry.signature}\n`;
    }
    markdown += '\n';
  });

  return markdown;
}

function detectCycles(entries: ATOMEntry[]): VisualizationNode[] {
  const cycleNodes: VisualizationNode[] = [];
  
  // Group by vortex
  const vortexGroups = new Map<string, ATOMEntry[]>();
  entries.forEach(entry => {
    const existing = vortexGroups.get(entry.vortexId);
    if (existing) {
      existing.push(entry);
    } else {
      vortexGroups.set(entry.vortexId, [entry]);
    }
  });

  // Detect Fibonacci-weighted 42-cycle patterns
  vortexGroups.forEach((vortexEntries, vortexId) => {
    const fibEntries = vortexEntries.filter(e => e.fibonacciWeight !== undefined);
    
    if (fibEntries.length >= 42) {
      // Found a potential 42-cycle
      cycleNodes.push({
        id: `cycle-${vortexId}`,
        label: `42-Cycle (${vortexId})`,
        type: 'cycle'
      });
    }
  });

  return cycleNodes;
}
