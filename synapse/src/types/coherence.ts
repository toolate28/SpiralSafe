/**
 * SYNAPSE Type Definitions: Coherence
 * 42.00055 framework for measuring system coherence
 */

/**
 * Core coherence metrics based on 42.00055 framework
 * 42 = Icosahedral V+E (vertices + edges)
 * 0.00055 = Quantum foam epsilon
 */
export interface CoherenceMetrics {
  /** Overall coherence score [0, 1] with target of 42.00055% ≈ 0.4200055 */
  overall: number;
  
  /** Three-phase decomposition */
  curl: number;        // Circular/self-referential patterns [0, 1]
  potential: number;   // Latent structure awaiting development [0, 1]
  dispersion: number;  // Chaotic/divergent patterns [0, 1]
  
  /** Quantum foam floor */
  epsilon: number;     // Base uncertainty = 0.00055
  
  /** Timestamp of measurement */
  timestamp: number;
}

/**
 * Coherence calculation over time series
 */
export interface CoherenceTimeSeries {
  metrics: CoherenceMetrics[];
  startTime: number;
  endTime: number;
  sampleRate: number;  // Hz
}

/**
 * Three-phase coherence vector
 */
export interface ThreePhaseVector {
  curl: number;
  potential: number;
  dispersion: number;
}

/**
 * Coherence field over 3D space
 */
export interface CoherenceField {
  resolution: number;  // Grid resolution
  bounds: {
    minX: number;
    maxX: number;
    minY: number;
    maxY: number;
    minZ: number;
    maxZ: number;
  };
  values: number[][][];  // 3D grid of coherence values
  timestamp: number;
}

/**
 * Calculate overall coherence from three-phase components
 */
export function calculateOverallCoherence(
  curl: number,
  potential: number,
  dispersion: number,
  epsilon: number = 0.00055
): number {
  // High potential = good
  // Low curl = good (less circular reasoning)
  // Low dispersion = good (less chaos)
  // epsilon = quantum foam floor
  
  const rawCoherence = potential - (curl + dispersion) / 2;
  const bounded = Math.max(epsilon, Math.min(1, rawCoherence));
  
  return bounded;
}

/**
 * Check if coherence is at or above the 42.00055 threshold
 */
export function isCoherent(coherence: number): boolean {
  const THRESHOLD = 0.4200055;
  return coherence >= THRESHOLD;
}

/**
 * Calculate distance to coherence threshold
 */
export function coherenceGap(coherence: number): number {
  const THRESHOLD = 0.4200055;
  return THRESHOLD - coherence;
}

/**
 * Approaching speed of light indicator
 * As coherence → 42.00055, returns velocity/c ratio
 */
export function velocityRatio(coherence: number): number {
  const THRESHOLD = 0.4200055;
  const epsilon = 0.00055;
  
  if (coherence < epsilon) return 0;
  if (coherence >= THRESHOLD) {
    // Past threshold: asymptotic approach to c
    const excess = coherence - THRESHOLD;
    const normalized = excess / (1 - THRESHOLD);
    return 0.5 + 0.5 * (1 - Math.exp(-normalized * 5));
  }
  
  // Below threshold: linear approach
  return (coherence - epsilon) / (THRESHOLD - epsilon) * 0.5;
}

/**
 * Supergravity distortion factor
 * At c, gamma → ∞ and isomorphism breaks
 */
export function supergravityFactor(velocityC: number): number {
  if (velocityC >= 0.9999) {
    return Infinity;  // Topology inversion
  }
  
  // Lorentz factor: γ = 1/√(1-v²/c²)
  return 1 / Math.sqrt(1 - velocityC * velocityC);
}

/**
 * Check if topology inversion should occur (past c)
 */
export function shouldInvertTopology(coherence: number): boolean {
  const v_c = velocityRatio(coherence);
  return v_c >= 0.9999;
}
