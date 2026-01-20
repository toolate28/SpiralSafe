/**
 * SYNAPSE Utilities: Coherence
 * 42.00055 framework calculations
 */

import {
  CoherenceMetrics,
  ThreePhaseVector,
  calculateOverallCoherence,
} from '../types/coherence';

/** The coherence threshold: 42.00055% */
export const COHERENCE_THRESHOLD = 0.4200055;

/** Quantum foam epsilon */
export const EPSILON = 0.00055;

/** Icosahedral structure: V + E = 42 */
export const ICOSAHEDRAL_VE = 42;

/**
 * Create default coherence metrics
 */
export function createDefaultCoherence(): CoherenceMetrics {
  return {
    overall: EPSILON,
    curl: 0,
    potential: EPSILON,
    dispersion: 0,
    epsilon: EPSILON,
    timestamp: Date.now(),
  };
}

/**
 * Calculate coherence from three-phase components
 */
export function calculateCoherence(
  curl: number,
  potential: number,
  dispersion: number
): CoherenceMetrics {
  const overall = calculateOverallCoherence(curl, potential, dispersion, EPSILON);
  
  return {
    overall,
    curl,
    potential,
    dispersion,
    epsilon: EPSILON,
    timestamp: Date.now(),
  };
}

/**
 * Interpolate between two coherence states
 */
export function interpolateCoherence(
  a: CoherenceMetrics,
  b: CoherenceMetrics,
  t: number
): CoherenceMetrics {
  const clamp = (x: number) => Math.max(0, Math.min(1, x));
  const lerp = (x: number, y: number, t: number) => x + (y - x) * t;
  
  return {
    overall: lerp(a.overall, b.overall, t),
    curl: clamp(lerp(a.curl, b.curl, t)),
    potential: clamp(lerp(a.potential, b.potential, t)),
    dispersion: clamp(lerp(a.dispersion, b.dispersion, t)),
    epsilon: EPSILON,
    timestamp: Date.now(),
  };
}

/**
 * Calculate coherence gradient (rate of change)
 */
export function coherenceGradient(
  current: CoherenceMetrics,
  previous: CoherenceMetrics
): number {
  const dt = (current.timestamp - previous.timestamp) / 1000; // seconds
  if (dt <= 0) return 0;
  
  return (current.overall - previous.overall) / dt;
}

/**
 * Normalize three-phase vector to sum to 1
 */
export function normalizeThreePhase(vector: ThreePhaseVector): ThreePhaseVector {
  const sum = vector.curl + vector.potential + vector.dispersion;
  if (sum === 0) {
    return { curl: 0, potential: 1, dispersion: 0 }; // Default to potential
  }
  
  return {
    curl: vector.curl / sum,
    potential: vector.potential / sum,
    dispersion: vector.dispersion / sum,
  };
}

/**
 * Calculate three-phase vector from entity relationships
 * - Curl: cyclic dependencies
 * - Potential: incomplete connections
 * - Dispersion: scattered/weak connections
 */
export function analyzeRelationshipCoherence(
  entityCount: number,
  relationships: Array<{ source: string; target: string; strength: number }>
): ThreePhaseVector {
  if (entityCount === 0 || relationships.length === 0) {
    return { curl: 0, potential: 1, dispersion: 0 };
  }
  
  // Build adjacency for cycle detection
  const adjacency = new Map<string, Set<string>>();
  relationships.forEach(rel => {
    if (!adjacency.has(rel.source)) {
      adjacency.set(rel.source, new Set());
    }
    adjacency.get(rel.source)!.add(rel.target);
  });
  
  // Detect cycles (curl)
  let cycleCount = 0;
  const visited = new Set<string>();
  const recStack = new Set<string>();
  
  const hasCycle = (node: string): boolean => {
    visited.add(node);
    recStack.add(node);
    
    const neighbors = adjacency.get(node) || new Set();
    for (const neighbor of neighbors) {
      if (!visited.has(neighbor)) {
        if (hasCycle(neighbor)) return true;
      } else if (recStack.has(neighbor)) {
        cycleCount++;
        return true;
      }
    }
    
    recStack.delete(node);
    return false;
  };
  
  adjacency.forEach((_, node) => {
    if (!visited.has(node)) {
      hasCycle(node);
    }
  });
  
  const curl = Math.min(1, cycleCount / Math.max(1, entityCount * 0.1));
  
  // Calculate average relationship strength (potential vs dispersion)
  const avgStrength = relationships.reduce((sum, r) => sum + r.strength, 0) / relationships.length;
  
  // Strong connections = high potential
  // Weak connections = high dispersion
  const potential = avgStrength;
  const dispersion = 1 - avgStrength;
  
  return normalizeThreePhase({ curl, potential, dispersion });
}

/**
 * Map coherence value to color
 * Low coherence = red/orange, threshold = green, high = blue
 */
export function coherenceToColor(coherence: number): { r: number; g: number; b: number } {
  const normalized = Math.max(0, Math.min(1, coherence));
  
  if (normalized < COHERENCE_THRESHOLD) {
    // Below threshold: red to orange to yellow
    const t = normalized / COHERENCE_THRESHOLD;
    return {
      r: 1,
      g: t * 0.8,
      b: 0,
    };
  } else {
    // Above threshold: green to cyan to blue
    const t = (normalized - COHERENCE_THRESHOLD) / (1 - COHERENCE_THRESHOLD);
    return {
      r: 0,
      g: 1 - t * 0.5,
      b: t,
    };
  }
}

/**
 * Calculate coherence decay over time
 * Without maintenance, coherence drifts toward epsilon
 */
export function applyCoherenceDecay(
  coherence: CoherenceMetrics,
  deltaTime: number,
  decayRate: number = 0.001
): CoherenceMetrics {
  const decay = Math.exp(-decayRate * deltaTime);
  const targetValue = EPSILON;
  
  return {
    overall: targetValue + (coherence.overall - targetValue) * decay,
    curl: coherence.curl * decay,
    potential: targetValue + (coherence.potential - targetValue) * decay,
    dispersion: coherence.dispersion + (1 - decay) * 0.1, // Entropy increases
    epsilon: EPSILON,
    timestamp: Date.now(),
  };
}

/**
 * Combine multiple coherence metrics (e.g., from different subsystems)
 */
export function combineCoherence(metrics: CoherenceMetrics[]): CoherenceMetrics {
  if (metrics.length === 0) {
    return createDefaultCoherence();
  }
  
  const sum = metrics.reduce(
    (acc, m) => ({
      overall: acc.overall + m.overall,
      curl: acc.curl + m.curl,
      potential: acc.potential + m.potential,
      dispersion: acc.dispersion + m.dispersion,
    }),
    { overall: 0, curl: 0, potential: 0, dispersion: 0 }
  );
  
  const n = metrics.length;
  return {
    overall: sum.overall / n,
    curl: sum.curl / n,
    potential: sum.potential / n,
    dispersion: sum.dispersion / n,
    epsilon: EPSILON,
    timestamp: Date.now(),
  };
}
