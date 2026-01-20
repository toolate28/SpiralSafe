/**
 * SYNAPSE Type Definitions: Quantum Reservoir Computing
 * QRC substrate types and quantum state representations
 */

import { Scale } from './scales';
import { CoherenceMetrics } from './coherence';

/**
 * QRC substrate types mapped to Fibonacci scales
 */
export enum QRCSubstrate {
  SINGLE_QUBIT = 'single_qubit',        // fib:1
  JC_PAIRS = 'jc_pairs',                 // fib:3 (Jaynes-Cummings)
  OSCILLATOR_NETS = 'oscillator_nets',   // fib:5
  BOSE_HUBBARD = 'bose_hubbard',        // fib:8 (lattice)
  AQUILA_SCALE = 'aquila_scale',        // fib:13 (Rydberg atoms)
}

/**
 * Map QRC substrate to Fibonacci scale
 */
export const QRC_SUBSTRATE_SCALE: Record<QRCSubstrate, Scale> = {
  [QRCSubstrate.SINGLE_QUBIT]: Scale.NODE,
  [QRCSubstrate.JC_PAIRS]: Scale.CLUSTER,
  [QRCSubstrate.OSCILLATOR_NETS]: Scale.TEAM,
  [QRCSubstrate.BOSE_HUBBARD]: Scale.SQUAD,
  [QRCSubstrate.AQUILA_SCALE]: Scale.DEPARTMENT,
};

/**
 * Quantum state representation
 * |ψ⟩ = α|0⟩ + β|1⟩ for single qubit
 */
export interface QuantumState {
  /** State amplitudes (complex numbers as [real, imag] pairs) */
  amplitudes: Array<[number, number]>;
  
  /** Measurement probabilities */
  probabilities: number[];
  
  /** Coherence (fidelity) metric [0, 1] */
  coherence: number;
  
  /** Timestamp */
  timestamp: number;
}

/**
 * QRC reservoir state
 */
export interface ReservoirState {
  /** Substrate type */
  substrate: QRCSubstrate;
  
  /** Number of qubits/oscillators */
  size: number;
  
  /** Current quantum state */
  quantumState: QuantumState;
  
  /** Input parameters (encoded as rotation angles) */
  inputParams: number[];
  
  /** Circuit depth */
  depth: number;
  
  /** Energy metric (FLOPs) */
  energy: number;
  
  /** Coherence metrics */
  coherence: CoherenceMetrics;
}

/**
 * QRC dynamics over time
 */
export interface ReservoirDynamics {
  states: ReservoirState[];
  startTime: number;
  endTime: number;
  evolutionOperator?: string; // Circuit description
}

/**
 * QRC measurement result
 */
export interface MeasurementResult {
  /** Bitstring -> count */
  counts: Map<string, number>;
  
  /** Total shots */
  shots: number;
  
  /** Most probable outcome */
  mostProbable: string;
  
  /** Entropy of distribution */
  entropy: number;
}

/**
 * Entanglement metrics
 */
export interface EntanglementMetrics {
  /** Von Neumann entropy */
  entropy: number;
  
  /** Entangled pairs */
  pairs: Array<[number, number]>;
  
  /** Entanglement strength [0, 1] */
  strength: number;
}

/**
 * QRC performance metrics
 */
export interface QRCMetrics {
  /** Coherence (fidelity) [0, 1] */
  fidelity: number;
  
  /** Energy consumption (circuit depth proxy) */
  energy: number;
  
  /** Collapse proximity (distance to measurement) */
  collapseProximity: number;
  
  /** Snap-in rate (successful integrations) */
  snapInRate: number;
  
  /** Entanglement metrics */
  entanglement: EntanglementMetrics;
}

/**
 * Calculate probability from complex amplitude
 */
export function amplitudeToProbability(amplitude: [number, number]): number {
  const [re, im] = amplitude;
  return re * re + im * im;
}

/**
 * Calculate probabilities from state amplitudes
 */
export function stateToProbabilities(state: QuantumState): number[] {
  return state.amplitudes.map(amplitudeToProbability);
}

/**
 * Calculate entropy of measurement distribution
 */
export function calculateEntropy(probabilities: number[]): number {
  return -probabilities.reduce((sum, p) => {
    if (p === 0) return sum;
    return sum + p * Math.log2(p);
  }, 0);
}

/**
 * Check if state is in superposition
 */
export function isInSuperposition(state: QuantumState): boolean {
  const probs = stateToProbabilities(state);
  const nonZeroCount = probs.filter(p => p > 1e-10).length;
  return nonZeroCount > 1;
}

/**
 * Calculate state fidelity (coherence metric)
 */
export function calculateFidelity(
  state1: QuantumState,
  state2: QuantumState
): number {
  if (state1.amplitudes.length !== state2.amplitudes.length) {
    return 0;
  }
  
  // Inner product: ⟨ψ₁|ψ₂⟩
  let realSum = 0;
  let imagSum = 0;
  
  for (let i = 0; i < state1.amplitudes.length; i++) {
    const [re1, im1] = state1.amplitudes[i];
    const [re2, im2] = state2.amplitudes[i];
    
    // Complex conjugate multiplication
    realSum += re1 * re2 + im1 * im2;
    imagSum += re1 * im2 - im1 * re2;
  }
  
  // Fidelity = |⟨ψ₁|ψ₂⟩|²
  return realSum * realSum + imagSum * imagSum;
}

/**
 * QRC substrate metadata
 */
export interface SubstrateInfo {
  substrate: QRCSubstrate;
  fibonacciNumber: number;
  name: string;
  description: string;
  qubitRange: [number, number];
  advantages: string[];
}

/**
 * QRC substrate information lookup
 */
export const QRC_SUBSTRATE_INFO: Record<QRCSubstrate, SubstrateInfo> = {
  [QRCSubstrate.SINGLE_QUBIT]: {
    substrate: QRCSubstrate.SINGLE_QUBIT,
    fibonacciNumber: 1,
    name: 'Single Qubit',
    description: 'Minimal quantum reservoir',
    qubitRange: [1, 1],
    advantages: ['Simple', 'Educational', 'Fast simulation'],
  },
  [QRCSubstrate.JC_PAIRS]: {
    substrate: QRCSubstrate.JC_PAIRS,
    fibonacciNumber: 3,
    name: 'Jaynes-Cummings Pairs',
    description: 'Qubit-boson interaction systems',
    qubitRange: [2, 4],
    advantages: ['Time-series processing', 'Tunable coupling', 'Natural ML basis'],
  },
  [QRCSubstrate.OSCILLATOR_NETS]: {
    substrate: QRCSubstrate.OSCILLATOR_NETS,
    fibonacciNumber: 5,
    name: 'Parametric Oscillators',
    description: 'Coupled quantum oscillators',
    qubitRange: [2, 10],
    advantages: ['Dense neuron count', 'Infinite-dimensional', 'Continuous-variable'],
  },
  [QRCSubstrate.BOSE_HUBBARD]: {
    substrate: QRCSubstrate.BOSE_HUBBARD,
    fibonacciNumber: 8,
    name: 'Bose-Hubbard Lattice',
    description: 'Ultracold atoms in optical lattices',
    qubitRange: [8, 50],
    advantages: ['Optimal in ergodic regime', 'No disorder needed', 'Clean testbed'],
  },
  [QRCSubstrate.AQUILA_SCALE]: {
    substrate: QRCSubstrate.AQUILA_SCALE,
    fibonacciNumber: 13,
    name: 'Rydberg Atom Arrays',
    description: 'Neutral atom quantum processors',
    qubitRange: [50, 256],
    advantages: ['Scalable', 'Gradient-free training', 'Native graph structure'],
  },
};
