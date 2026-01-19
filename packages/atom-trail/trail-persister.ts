/**
 * ATOM Trail Persister
 * Core implementation for logging, querying, and managing the ATOM trail
 * 
 * ATOM: ATOM-PERSISTER-20260119-001-trail-logging-system
 */

import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';
import {
  ATOMEntry,
  ATOMQueryFilters,
  ATOMGraph,
  ATOMGraphNode,
  ATOMExportFormat,
  ATOMStats
} from './types.js';

const DEFAULT_TRAIL_PATH = '.spiralsafe/atom-trail.jsonl';

/**
 * Ensures the trail directory exists
 */
function ensureTrailDirectory(trailPath: string): void {
  const dir = path.dirname(trailPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * Generates a unique ID for an ATOM entry
 */
function generateATOMId(): string {
  return `atom-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
}

/**
 * Log a decision with full context to the ATOM trail
 * 
 * @param entry - The ATOM entry to log (without timestamp)
 * @param trailPath - Optional custom path to the trail file
 * @returns Promise resolving to the logged entry with timestamp and ID
 */
export async function logATOM(
  entry: Omit<ATOMEntry, 'timestamp'>,
  trailPath: string = DEFAULT_TRAIL_PATH
): Promise<ATOMEntry> {
  ensureTrailDirectory(trailPath);
  
  const fullEntry: ATOMEntry = {
    ...entry,
    timestamp: new Date().toISOString(),
    id: entry.id || generateATOMId()
  };
  
  // Append to JSON Lines file
  const line = JSON.stringify(fullEntry) + '\n';
  await fs.promises.appendFile(trailPath, line, 'utf-8');
  
  return fullEntry;
}

/**
 * Query the ATOM trail with filters
 * 
 * @param filters - Query filters
 * @param trailPath - Optional custom path to the trail file
 * @returns Promise resolving to array of matching ATOM entries
 */
export async function queryATOM(
  filters: ATOMQueryFilters = {},
  trailPath: string = DEFAULT_TRAIL_PATH
): Promise<ATOMEntry[]> {
  if (!fs.existsSync(trailPath)) {
    return [];
  }
  
  const content = await fs.promises.readFile(trailPath, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.length > 0);
  
  let entries: ATOMEntry[] = lines.map(line => JSON.parse(line));
  
  // Apply filters
  if (filters.vortexId) {
    entries = entries.filter(e => e.vortexId === filters.vortexId);
  }
  
  if (filters.outcome) {
    entries = entries.filter(e => e.outcome === filters.outcome);
  }
  
  if (filters.startTime) {
    const startDate = new Date(filters.startTime);
    entries = entries.filter(e => new Date(e.timestamp) >= startDate);
  }
  
  if (filters.endTime) {
    const endDate = new Date(filters.endTime);
    entries = entries.filter(e => new Date(e.timestamp) <= endDate);
  }
  
  if (filters.minCoherence !== undefined) {
    const minCoherence = filters.minCoherence;
    entries = entries.filter(e => 
      e.coherenceScore !== undefined && e.coherenceScore >= minCoherence
    );
  }
  
  if (filters.maxCoherence !== undefined) {
    const maxCoherence = filters.maxCoherence;
    entries = entries.filter(e => 
      e.coherenceScore !== undefined && e.coherenceScore <= maxCoherence
    );
  }
  
  // Apply pagination
  const offset = filters.offset || 0;
  const limit = filters.limit || entries.length;
  
  return entries.slice(offset, offset + limit);
}

/**
 * Visualize ATOM trail as a decision graph
 * 
 * @param vortexId - The vortex to visualize
 * @param trailPath - Optional custom path to the trail file
 * @returns Promise resolving to an ATOM graph
 */
export async function visualizeATOM(
  vortexId: string,
  trailPath: string = DEFAULT_TRAIL_PATH
): Promise<ATOMGraph> {
  const entries = await queryATOM({ vortexId }, trailPath);
  
  const nodes = new Map<string, ATOMGraphNode>();
  const roots: string[] = [];
  
  // Build graph nodes
  entries.forEach(entry => {
    const id = entry.id || generateATOMId();
    nodes.set(id, {
      id,
      entry,
      children: [],
      parent: undefined
    });
  });
  
  // Link parent-child relationships based on context.parentId if present
  entries.forEach(entry => {
    const id = entry.id || '';
    const parentId = entry.context.parentId as string | undefined;
    
    if (parentId && nodes.has(parentId)) {
      const node = nodes.get(id);
      const parentNode = nodes.get(parentId);
      if (node && parentNode) {
        node.parent = parentId;
        parentNode.children.push(id);
      }
    } else {
      // No parent, so it's a root
      if (id) {
        roots.push(id);
      }
    }
  });
  
  return {
    nodes,
    roots,
    vortexId
  };
}

/**
 * Export ATOM trail in various formats
 * 
 * @param format - Export format (json, csv, markdown)
 * @param filters - Optional filters for what to export
 * @param trailPath - Optional custom path to the trail file
 * @returns Promise resolving to formatted string
 */
export async function exportATOM(
  format: ATOMExportFormat,
  filters: ATOMQueryFilters = {},
  trailPath: string = DEFAULT_TRAIL_PATH
): Promise<string> {
  const entries = await queryATOM(filters, trailPath);
  
  switch (format) {
    case 'json':
      return JSON.stringify(entries, null, 2);
    
    case 'csv':
      return exportCSV(entries);
    
    case 'markdown':
      return exportMarkdown(entries);
    
    default:
      throw new Error(`Unsupported export format: ${format}`);
  }
}

/**
 * Export entries as CSV
 */
function exportCSV(entries: ATOMEntry[]): string {
  if (entries.length === 0) {
    return 'timestamp,vortexId,decision,outcome,coherenceScore,fibonacciWeight\n';
  }
  
  const header = 'timestamp,vortexId,decision,outcome,coherenceScore,fibonacciWeight\n';
  const rows = entries.map(e => {
    const escaped = (s: string) => `"${s.replace(/"/g, '""')}"`;
    return [
      escaped(e.timestamp),
      escaped(e.vortexId),
      escaped(e.decision),
      escaped(e.outcome),
      e.coherenceScore?.toString() || '',
      e.fibonacciWeight?.toString() || ''
    ].join(',');
  });
  
  return header + rows.join('\n');
}

/**
 * Export entries as Markdown
 */
function exportMarkdown(entries: ATOMEntry[]): string {
  if (entries.length === 0) {
    return '# ATOM Trail Export\n\nNo entries found.\n';
  }
  
  let md = '# ATOM Trail Export\n\n';
  md += `**Total Entries:** ${entries.length}\n\n`;
  md += '---\n\n';
  
  entries.forEach((entry, index) => {
    md += `## Entry ${index + 1}: ${entry.decision}\n\n`;
    md += `- **Timestamp:** ${entry.timestamp}\n`;
    md += `- **Vortex:** ${entry.vortexId}\n`;
    md += `- **Outcome:** ${entry.outcome}\n`;
    
    if (entry.coherenceScore !== undefined) {
      md += `- **Coherence Score:** ${(entry.coherenceScore * 100).toFixed(1)}%\n`;
    }
    
    if (entry.fibonacciWeight !== undefined) {
      md += `- **Priority:** ${entry.fibonacciWeight}\n`;
    }
    
    md += `\n**Rationale:**\n${entry.rationale}\n\n`;
    
    if (Object.keys(entry.context).length > 0) {
      md += `**Context:**\n\`\`\`json\n${JSON.stringify(entry.context, null, 2)}\n\`\`\`\n\n`;
    }
    
    md += '---\n\n';
  });
  
  return md;
}

/**
 * Get statistics about the ATOM trail
 * 
 * @param trailPath - Optional custom path to the trail file
 * @returns Promise resolving to ATOM statistics
 */
export async function getATOMStats(
  trailPath: string = DEFAULT_TRAIL_PATH
): Promise<ATOMStats> {
  const entries = await queryATOM({}, trailPath);
  
  if (entries.length === 0) {
    return {
      totalEntries: 0,
      successCount: 0,
      failureCount: 0,
      pendingCount: 0,
      avgCoherenceScore: 0,
      vortexBreakdown: {},
      timeRange: { earliest: '', latest: '' }
    };
  }
  
  const successCount = entries.filter(e => e.outcome === 'success').length;
  const failureCount = entries.filter(e => e.outcome === 'failure').length;
  const pendingCount = entries.filter(e => e.outcome === 'pending').length;
  
  const coherenceScores = entries
    .map(e => e.coherenceScore)
    .filter((s): s is number => s !== undefined);
  
  const avgCoherenceScore = coherenceScores.length > 0
    ? coherenceScores.reduce((sum, s) => sum + s, 0) / coherenceScores.length
    : 0;
  
  const vortexBreakdown: Record<string, number> = {};
  entries.forEach(e => {
    vortexBreakdown[e.vortexId] = (vortexBreakdown[e.vortexId] || 0) + 1;
  });
  
  const timestamps = entries.map(e => e.timestamp).sort();
  
  return {
    totalEntries: entries.length,
    successCount,
    failureCount,
    pendingCount,
    avgCoherenceScore,
    vortexBreakdown,
    timeRange: {
      earliest: timestamps[0],
      latest: timestamps[timestamps.length - 1]
    }
  };
}

/**
 * Generate a Mermaid diagram for the ATOM graph
 * 
 * @param graph - The ATOM graph to visualize
 * @returns Mermaid diagram as a string
 */
export function generateMermaidDiagram(graph: ATOMGraph): string {
  let mermaid = 'graph TD\n';
  
  graph.nodes.forEach((node, id) => {
    const entry = node.entry;
    const label = `${entry.decision.substring(0, 30)}${entry.decision.length > 30 ? '...' : ''}`;
    const outcome = entry.outcome === 'success' ? '✓' : entry.outcome === 'failure' ? '✗' : '⋯';
    const coherence = entry.coherenceScore !== undefined 
      ? ` (${(entry.coherenceScore * 100).toFixed(0)}%)`
      : '';
    
    mermaid += `  ${id}["${outcome} ${label}${coherence}"]\n`;
    
    // Add edges to children
    node.children.forEach(childId => {
      mermaid += `  ${id} --> ${childId}\n`;
    });
  });
  
  return mermaid;
}
