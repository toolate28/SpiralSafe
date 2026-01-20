/**
 * SYNAPSE Utilities: Hindmarsh-Rose Neural Dynamics
 * Integration of HR equations for quality control visualization
 */

import {
  NeuralState,
  NeuralMode,
  HRParameters,
  DEFAULT_HR_PARAMS,
  detectNeuralMode,
} from '../types/neural';

/**
 * Create initial neural state
 */
export function createInitialState(
  x: number = -1.6,
  y: number = 0,
  z: number = 0
): NeuralState {
  return {
    x,
    y,
    z,
    mode: NeuralMode.RESTING,
    timestamp: Date.now(),
  };
}

/**
 * Hindmarsh-Rose differential equations
 * dx/dt = y - ax³ + bx² - z + I
 * dy/dt = c - dx² - y
 * dz/dt = r(s(x - x_rest) - z)
 */
export function hrDerivatives(
  state: NeuralState,
  params: HRParameters = DEFAULT_HR_PARAMS
): { dx: number; dy: number; dz: number } {
  const { x, y, z } = state;
  const { I, a, b, c, d, r, s, x_rest } = params;
  
  const dx = y - a * x * x * x + b * x * x - z + I;
  const dy = c - d * x * x - y;
  const dz = r * (s * (x - x_rest) - z);
  
  return { dx, dy, dz };
}

/**
 * Integrate HR system one step using Runge-Kutta 4th order
 */
export function integrateHR(
  state: NeuralState,
  dt: number,
  params: HRParameters = DEFAULT_HR_PARAMS
): NeuralState {
  // RK4 integration
  const k1 = hrDerivatives(state, params);
  
  const state2 = {
    ...state,
    x: state.x + k1.dx * dt / 2,
    y: state.y + k1.dy * dt / 2,
    z: state.z + k1.dz * dt / 2,
  };
  const k2 = hrDerivatives(state2, params);
  
  const state3 = {
    ...state,
    x: state.x + k2.dx * dt / 2,
    y: state.y + k2.dy * dt / 2,
    z: state.z + k2.dz * dt / 2,
  };
  const k3 = hrDerivatives(state3, params);
  
  const state4 = {
    ...state,
    x: state.x + k3.dx * dt,
    y: state.y + k3.dy * dt,
    z: state.z + k3.dz * dt,
  };
  const k4 = hrDerivatives(state4, params);
  
  // Combine weighted derivatives
  const newX = state.x + (dt / 6) * (k1.dx + 2 * k2.dx + 2 * k3.dx + k4.dx);
  const newY = state.y + (dt / 6) * (k1.dy + 2 * k2.dy + 2 * k3.dy + k4.dy);
  const newZ = state.z + (dt / 6) * (k1.dz + 2 * k2.dz + 2 * k3.dz + k4.dz);
  
  const newState: NeuralState = {
    x: newX,
    y: newY,
    z: newZ,
    mode: detectNeuralMode({ ...state, x: newX, y: newY, z: newZ }),
    timestamp: state.timestamp + dt * 1000,
  };
  
  return newState;
}

/**
 * Simulate HR dynamics for a duration
 */
export function simulateHR(
  initialState: NeuralState,
  duration: number,
  dt: number = 0.01,
  params: HRParameters = DEFAULT_HR_PARAMS
): NeuralState[] {
  const states: NeuralState[] = [initialState];
  let currentState = initialState;
  
  const steps = Math.floor(duration / dt);
  
  for (let i = 0; i < steps; i++) {
    currentState = integrateHR(currentState, dt, params);
    states.push(currentState);
  }
  
  return states;
}

/**
 * Detect spikes in neural time series
 */
export function detectSpikes(
  states: NeuralState[],
  threshold: number = 0.5
): number[] {
  const spikeIndices: number[] = [];
  
  for (let i = 1; i < states.length - 1; i++) {
    const prev = states[i - 1].x;
    const curr = states[i].x;
    const next = states[i + 1].x;
    
    // Peak detection: curr > neighbors and above threshold
    if (curr > prev && curr > next && curr > threshold) {
      spikeIndices.push(i);
    }
  }
  
  return spikeIndices;
}

/**
 * Calculate inter-spike intervals
 */
export function calculateISI(
  states: NeuralState[],
  spikeIndices: number[],
  dt: number = 0.01
): number[] {
  const isis: number[] = [];
  
  for (let i = 1; i < spikeIndices.length; i++) {
    const interval = (spikeIndices[i] - spikeIndices[i - 1]) * dt;
    isis.push(interval);
  }
  
  return isis;
}

/**
 * Map quality metric to HR input current
 * Low quality → low I → resting/sparse firing
 * Medium quality → medium I → regular spiking
 * High quality → high I → bursting
 */
export function qualityToHRInput(quality: number): number {
  // quality in [0, 1]
  // I in [0, 5] for typical HR dynamics
  const clampedQuality = Math.max(0, Math.min(1, quality));
  
  // Map: 0 -> 0.5 (sub-threshold), 0.5 -> 2.5 (spiking), 1 -> 4.5 (bursting)
  return 0.5 + clampedQuality * 4.0;
}

/**
 * Map coherence to HR parameters
 * High coherence → more regular dynamics
 * Low coherence → more chaotic
 */
export function coherenceToHRParams(coherence: number): HRParameters {
  const baseParams = { ...DEFAULT_HR_PARAMS };
  
  // Adjust input based on coherence
  baseParams.I = 1.0 + coherence * 2.5;
  
  // High coherence → stronger recovery (more regular)
  baseParams.c = 0.8 + coherence * 0.4;
  
  // Low coherence → weaker adaptation (more chaotic)
  baseParams.r = 0.01 - coherence * 0.004;
  
  return baseParams;
}

/**
 * Create HR parameters for different entity types
 */
export function entityTypeToHRParams(entityType: string): HRParameters {
  const params = { ...DEFAULT_HR_PARAMS };
  
  switch (entityType) {
    case 'user':
      // Human: moderate dynamics
      params.I = 2.5;
      params.r = 0.006;
      break;
      
    case 'function':
    case 'file':
      // Code: faster dynamics
      params.I = 3.0;
      params.r = 0.01;
      break;
      
    case 'team':
    case 'department':
      // Groups: slower, more stable
      params.I = 2.0;
      params.r = 0.003;
      break;
      
    case 'organization':
    case 'enterprise':
      // Large systems: very slow adaptation
      params.I = 1.5;
      params.r = 0.001;
      break;
      
    default:
      // Use defaults
      break;
  }
  
  return params;
}

/**
 * Calculate average firing rate
 */
export function calculateFiringRate(
  states: NeuralState[],
  dt: number = 0.01
): number {
  const spikes = detectSpikes(states);
  const duration = states.length * dt;
  
  return spikes.length / duration;
}

/**
 * Determine neural mode from firing pattern
 */
export function classifyFiringPattern(
  states: NeuralState[],
  dt: number = 0.01
): NeuralMode {
  const spikes = detectSpikes(states);
  
  if (spikes.length === 0) {
    return NeuralMode.RESTING;
  }
  
  const isis = calculateISI(states, spikes, dt);
  
  if (isis.length < 2) {
    return NeuralMode.SPIKING;
  }
  
  // Check ISI variability
  const meanISI = isis.reduce((a, b) => a + b, 0) / isis.length;
  const variance = isis.reduce((sum, isi) => sum + Math.pow(isi - meanISI, 2), 0) / isis.length;
  const cv = Math.sqrt(variance) / meanISI; // Coefficient of variation
  
  if (cv > 0.5) {
    return NeuralMode.CHAOTIC; // High variability
  } else if (cv < 0.2) {
    return NeuralMode.BURSTING; // Regular pattern
  } else {
    return NeuralMode.SPIKING; // Moderate variability
  }
}
