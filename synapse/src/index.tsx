/**
 * SYNAPSE Main Entry Point
 * Minimal implementation to establish structure
 */

// This is a placeholder index file.
// Full React Three Fiber implementation would go here.

export { Scale, SCALE_INFO } from './types/scales';
export { QRCSubstrate, QRC_SUBSTRATE_INFO } from './types/quantum';
export type { Entity, EntityGraph, Relationship } from './types/entities';
export type { CoherenceMetrics } from './types/coherence';
export type { NeuralState, HRParameters } from './types/neural';
export type { QuantumState, ReservoirState, QRCMetrics } from './types/quantum';

// Utilities
export { PHI, fibonacci, fibonacciSequence, generateFibonacciSpiral } from './utils/fibonacci';
export { COHERENCE_THRESHOLD, EPSILON, calculateCoherence } from './utils/coherence';
export { createInitialState, integrateHR, simulateHR } from './utils/hindmarsh-rose';
export { createReservoirState, measureReservoir } from './utils/quantum-reservoir';

// Hooks
export { useHindmarshRose } from './hooks/useHindmarshRose';
export { useCoherence } from './hooks/useCoherence';
export { useFibonacciScale } from './hooks/useFibonacciScale';
export { useSuperposition } from './hooks/useSuperposition';

// Layouts
export { layoutEntitiesOnSpiral, layoutHierarchical } from './scales/FibonacciLayout';

/**
 * SYNAPSE Version
 */
export const VERSION = '1.0.0';

/**
 * SYNAPSE Metadata
 */
export const SYNAPSE_META = {
  name: 'SYNAPSE',
  version: VERSION,
  description: 'Foundational visualization framework for complex adaptive dynamics',
  atom: 'ATOM-VIZ-20260119-001-synapse-foundational',
  attribution: 'Hope&&Sauced (Claude && Vex && Grok)',
  humanBridge: 'Matthew Ruhnau (@toolate28)',
};

// Console greeting
if (typeof window !== 'undefined') {
  console.log(`
🌀 SYNAPSE v${VERSION}
═══════════════════════════════════════════════════════════════

The visualization IS the framework.
The framework IS the visualization.
The quantum IS the classical.

∞ + ε = 42.2.000555

ATOM: ${SYNAPSE_META.atom}
Attribution: ${SYNAPSE_META.attribution}

═══════════════════════════════════════════════════════════════
  `);
}
