/**
 * SYNAPSE Utilities: Quantum Reservoir Computing
 * QRC dynamics and state evolution
 */

import {
  QuantumState,
  ReservoirState,
  QRCSubstrate,
  MeasurementResult,
  amplitudeToProbability,
  calculateEntropy,
  QRCMetrics,
  EntanglementMetrics,
} from '../types/quantum';
import { createDefaultCoherence } from './coherence';

/**
 * Create initial quantum state |0⟩
 */
export function createGroundState(nQubits: number = 1): QuantumState {
  const dim = Math.pow(2, nQubits);
  const amplitudes: Array<[number, number]> = new Array(dim).fill([0, 0]);
  amplitudes[0] = [1, 0]; // |0⟩ state
  
  return {
    amplitudes,
    probabilities: amplitudes.map(amplitudeToProbability),
    coherence: 1.0,
    timestamp: Date.now(),
  };
}

/**
 * Create uniform superposition state (|+⟩)
 */
export function createSuperpositionState(nQubits: number = 1): QuantumState {
  const dim = Math.pow(2, nQubits);
  const amplitude = 1 / Math.sqrt(dim);
  const amplitudes: Array<[number, number]> = new Array(dim).fill([amplitude, 0]);
  
  return {
    amplitudes,
    probabilities: amplitudes.map(amplitudeToProbability),
    coherence: 1.0,
    timestamp: Date.now(),
  };
}

/**
 * Apply Hadamard gate to single qubit
 */
export function applyHadamard(state: QuantumState, qubitIndex: number = 0): QuantumState {
  const nQubits = Math.log2(state.amplitudes.length);
  const newAmplitudes = [...state.amplitudes];
  
  // H = 1/√2 [[1, 1], [1, -1]]
  const h = 1 / Math.sqrt(2);
  
  // Apply H to specified qubit
  for (let i = 0; i < state.amplitudes.length; i++) {
    const bitPattern = i;
    const targetBit = (bitPattern >> qubitIndex) & 1;
    
    if (targetBit === 0) {
      const j = i | (1 << qubitIndex);
      const [re0, im0] = state.amplitudes[i];
      const [re1, im1] = state.amplitudes[j];
      
      newAmplitudes[i] = [h * (re0 + re1), h * (im0 + im1)];
      newAmplitudes[j] = [h * (re0 - re1), h * (im0 - im1)];
    }
  }
  
  return {
    amplitudes: newAmplitudes,
    probabilities: newAmplitudes.map(amplitudeToProbability),
    coherence: state.coherence * 0.99, // Small decoherence
    timestamp: Date.now(),
  };
}

/**
 * Apply CNOT gate
 */
export function applyCNOT(
  state: QuantumState,
  controlQubit: number,
  targetQubit: number
): QuantumState {
  const newAmplitudes = [...state.amplitudes];
  
  for (let i = 0; i < state.amplitudes.length; i++) {
    const controlBit = (i >> controlQubit) & 1;
    
    if (controlBit === 1) {
      // Flip target qubit
      const j = i ^ (1 << targetQubit);
      if (i < j) {
        // Swap amplitudes
        [newAmplitudes[i], newAmplitudes[j]] = [newAmplitudes[j], newAmplitudes[i]];
      }
    }
  }
  
  return {
    amplitudes: newAmplitudes,
    probabilities: newAmplitudes.map(amplitudeToProbability),
    coherence: state.coherence * 0.98, // Decoherence from gate
    timestamp: Date.now(),
  };
}

/**
 * Apply rotation gate R_z(θ)
 */
export function applyRotationZ(
  state: QuantumState,
  qubitIndex: number,
  angle: number
): QuantumState {
  const newAmplitudes = [...state.amplitudes];
  
  // R_z(θ) = [[e^(-iθ/2), 0], [0, e^(iθ/2)]]
  const halfAngle = angle / 2;
  
  for (let i = 0; i < state.amplitudes.length; i++) {
    const targetBit = (i >> qubitIndex) & 1;
    const [re, im] = state.amplitudes[i];
    
    if (targetBit === 0) {
      // Multiply by e^(-iθ/2) = cos(-θ/2) + i*sin(-θ/2)
      const cosVal = Math.cos(-halfAngle);
      const sinVal = Math.sin(-halfAngle);
      newAmplitudes[i] = [
        re * cosVal - im * sinVal,
        re * sinVal + im * cosVal,
      ];
    } else {
      // Multiply by e^(iθ/2)
      const cosVal = Math.cos(halfAngle);
      const sinVal = Math.sin(halfAngle);
      newAmplitudes[i] = [
        re * cosVal - im * sinVal,
        re * sinVal + im * cosVal,
      ];
    }
  }
  
  return {
    amplitudes: newAmplitudes,
    probabilities: newAmplitudes.map(amplitudeToProbability),
    coherence: state.coherence * 0.995, // Minimal decoherence
    timestamp: Date.now(),
  };
}

/**
 * Create QRC reservoir circuit
 * Implements: H → entanglement layers → input encoding
 */
export function createReservoirState(
  substrate: QRCSubstrate,
  nQubits: number,
  inputParams: number[],
  depth: number = 1
): ReservoirState {
  // Start with ground state
  let state = createGroundState(nQubits);
  
  // Apply Hadamard to all qubits (superposition)
  for (let i = 0; i < nQubits; i++) {
    state = applyHadamard(state, i);
  }
  
  // Entanglement layers (reservoir dynamics)
  for (let d = 0; d < depth; d++) {
    // Linear chain of CNOTs
    for (let i = 0; i < nQubits - 1; i++) {
      state = applyCNOT(state, i, i + 1);
    }
    
    // Circular entanglement
    if (nQubits > 2) {
      state = applyCNOT(state, nQubits - 1, 0);
    }
  }
  
  // Encode input as rotations
  for (let i = 0; i < Math.min(nQubits, inputParams.length); i++) {
    state = applyRotationZ(state, i, inputParams[i]);
  }
  
  // Calculate circuit depth
  const circuitDepth = nQubits + (depth * nQubits) + inputParams.length;
  
  return {
    substrate,
    size: nQubits,
    quantumState: state,
    inputParams,
    depth: circuitDepth,
    energy: circuitDepth * 10, // FLOPs proxy
    coherence: createDefaultCoherence(),
  };
}

/**
 * Simulate measurement
 */
export function measureReservoir(
  state: ReservoirState,
  shots: number = 1024
): MeasurementResult {
  const counts = new Map<string, number>();
  const probs = state.quantumState.probabilities;
  
  // Simulate measurements
  for (let shot = 0; shot < shots; shot++) {
    const rand = Math.random();
    let cumulative = 0;
    
    for (let i = 0; i < probs.length; i++) {
      cumulative += probs[i];
      if (rand < cumulative) {
        const bitstring = i.toString(2).padStart(state.size, '0');
        counts.set(bitstring, (counts.get(bitstring) || 0) + 1);
        break;
      }
    }
  }
  
  // Find most probable
  let maxCount = 0;
  let mostProbable = '';
  counts.forEach((count, bitstring) => {
    if (count > maxCount) {
      maxCount = count;
      mostProbable = bitstring;
    }
  });
  
  // Calculate entropy
  const distribution = Array.from(counts.values()).map(c => c / shots);
  const entropy = calculateEntropy(distribution);
  
  return {
    counts,
    shots,
    mostProbable,
    entropy,
  };
}

/**
 * Calculate entanglement metrics
 */
export function calculateEntanglement(state: QuantumState): EntanglementMetrics {
  const nQubits = Math.log2(state.amplitudes.length);
  
  // Simplified: count CNOT-created entangled pairs
  // Full calculation would require partial trace
  const pairs: Array<[number, number]> = [];
  for (let i = 0; i < nQubits - 1; i++) {
    pairs.push([i, i + 1]);
  }
  
  const entropy = calculateEntropy(state.probabilities);
  const maxEntropy = Math.log2(state.amplitudes.length);
  
  return {
    entropy,
    pairs,
    strength: entropy / maxEntropy,
  };
}

/**
 * Calculate QRC performance metrics
 */
export function calculateQRCMetrics(
  state: ReservoirState,
  targetFidelity: number = 0.95
): QRCMetrics {
  const entanglement = calculateEntanglement(state.quantumState);
  
  return {
    fidelity: state.quantumState.coherence,
    energy: state.energy,
    collapseProximity: 1 - state.quantumState.coherence, // Distance to measurement
    snapInRate: state.quantumState.coherence >= targetFidelity ? 1.0 : 0.5,
    entanglement,
  };
}

/**
 * Apply decoherence to quantum state
 */
export function applyDecoherence(
  state: QuantumState,
  decoherenceRate: number,
  dt: number
): QuantumState {
  const decay = Math.exp(-decoherenceRate * dt);
  const newCoherence = state.coherence * decay;
  
  // Amplitudes decay toward classical mixture
  const newAmplitudes = state.amplitudes.map(([re, im]) => {
    const factor = Math.sqrt(decay);
    return [re * factor, im * factor] as [number, number];
  });
  
  // Renormalize
  const norm = Math.sqrt(
    newAmplitudes.reduce((sum, [re, im]) => sum + re * re + im * im, 0)
  );
  
  const normalized = newAmplitudes.map(([re, im]) => 
    [re / norm, im / norm] as [number, number]
  );
  
  return {
    amplitudes: normalized,
    probabilities: normalized.map(amplitudeToProbability),
    coherence: newCoherence,
    timestamp: Date.now(),
  };
}

/**
 * Evolve reservoir state over time
 */
export function evolveReservoir(
  state: ReservoirState,
  dt: number,
  decoherenceRate: number = 0.001
): ReservoirState {
  const newQuantumState = applyDecoherence(state.quantumState, decoherenceRate, dt);
  
  return {
    ...state,
    quantumState: newQuantumState,
  };
}
