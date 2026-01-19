/**
 * ATOM (Auditable Trail Of Modifications) Types
 * Core TypeScript interfaces for the ATOM logging system
 * 
 * ATOM: ATOM-TYPES-20260119-001-atom-entry-interfaces
 */

/**
 * Core ATOM entry structure
 * Every decision in the system is logged with this structure
 */
export interface ATOMEntry {
  /** ISO 8601 timestamp when the decision was made */
  timestamp: string;
  
  /** Which vortex/system component generated this decision */
  vortexId: string;
  
  /** What was decided (the actual decision or action taken) */
  decision: string;
  
  /** Why the decision was made (AI reasoning, human input, etc.) */
  rationale: string;
  
  /** Outcome of the decision */
  outcome: 'success' | 'failure' | 'pending';
  
  /** WAVE coherence score at decision time (0-1 scale) */
  coherenceScore?: number;
  
  /** Priority using Fibonacci sequence (1,1,2,3,5,8,13...) */
  fibonacciWeight?: number;
  
  /** Relevant state and context information */
  context: Record<string, unknown>;
  
  /** Optional cryptographic proof for verification */
  signature?: string;
  
  /** Unique identifier for this ATOM entry */
  id?: string;
}

/**
 * Filters for querying the ATOM trail
 */
export interface ATOMQueryFilters {
  /** Filter by vortex ID */
  vortexId?: string;
  
  /** Filter by outcome status */
  outcome?: 'success' | 'failure' | 'pending';
  
  /** Start of time range (ISO 8601) */
  startTime?: string;
  
  /** End of time range (ISO 8601) */
  endTime?: string;
  
  /** Minimum coherence score (0-1) */
  minCoherence?: number;
  
  /** Maximum coherence score (0-1) */
  maxCoherence?: number;
  
  /** Limit number of results */
  limit?: number;
  
  /** Offset for pagination */
  offset?: number;
}

/**
 * Graph node representing an ATOM entry in visualization
 */
export interface ATOMGraphNode {
  id: string;
  entry: ATOMEntry;
  children: string[];
  parent?: string;
}

/**
 * Full ATOM decision graph for visualization
 */
export interface ATOMGraph {
  nodes: Map<string, ATOMGraphNode>;
  roots: string[];
  vortexId: string;
}

/**
 * Export format options
 */
export type ATOMExportFormat = 'json' | 'csv' | 'markdown';

/**
 * Statistics about the ATOM trail
 */
export interface ATOMStats {
  totalEntries: number;
  successCount: number;
  failureCount: number;
  pendingCount: number;
  avgCoherenceScore: number;
  vortexBreakdown: Record<string, number>;
  timeRange: {
    earliest: string;
    latest: string;
  };
}
