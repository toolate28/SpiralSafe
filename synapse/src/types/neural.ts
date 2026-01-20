/**
 * SYNAPSE Type Definitions: Neural Dynamics
 * Hindmarsh-Rose neural model for quality control
 */

/**
 * Hindmarsh-Rose neural state
 * Three coupled differential equations modeling neuron behavior
 */
export interface NeuralState {
  /** Membrane potential (fast variable) */
  x: number;
  
  /** Recovery variable (medium variable) */
  y: number;
  
  /** Adaptation current (slow variable) */
  z: number;
  
  /** Current behavior mode */
  mode: NeuralMode;
  
  /** Timestamp of state */
  timestamp: number;
}

/**
 * Neural behavior modes
 */
export enum NeuralMode {
  /** Stable, low activity */
  RESTING = 'resting',
  
  /** Brief high-amplitude spikes */
  SPIKING = 'spiking',
  
  /** Sustained oscillations */
  BURSTING = 'bursting',
  
  /** Chaotic dynamics */
  CHAOTIC = 'chaotic',
}

/**
 * Hindmarsh-Rose parameters
 */
export interface HRParameters {
  /** External input current */
  I: number;
  
  /** Cubic term coefficient */
  a: number;
  
  /** Quadratic term coefficient */
  b: number;
  
  /** Recovery time scale */
  c: number;
  
  /** Adaptation time scale */
  d: number;
  
  /** Resting potential */
  r: number;
  
  /** Adaptation strength */
  s: number;
  
  /** Reset value */
  x_rest: number;
}

/**
 * Default HR parameters for quality control
 */
export const DEFAULT_HR_PARAMS: HRParameters = {
  I: 3.0,      // Input: external stimulus
  a: 1.0,      // Cubic nonlinearity
  b: 3.0,      // Quadratic term
  c: 1.0,      // Recovery rate
  d: 5.0,      // Adaptation rate
  r: 0.006,    // Slow adaptation time scale
  s: 4.0,      // Adaptation coupling
  x_rest: -1.6, // Resting membrane potential
};

/**
 * Neural state time series
 */
export interface NeuralTimeSeries {
  states: NeuralState[];
  parameters: HRParameters;
  startTime: number;
  endTime: number;
  dt: number;  // Time step
}

/**
 * Classification thresholds for neural modes
 */
export interface ModeThresholds {
  spikeThreshold: number;    // x > threshold = spike
  burstMinSpikes: number;    // Min spikes for burst
  burstMaxInterval: number;  // Max time between spikes in burst
  restingMaxX: number;       // Max x for resting state
}

/**
 * Default mode detection thresholds
 */
export const DEFAULT_MODE_THRESHOLDS: ModeThresholds = {
  spikeThreshold: 0.5,
  burstMinSpikes: 3,
  burstMaxInterval: 50,
  restingMaxX: -0.5,
};

/**
 * Map neural state to visualization color
 */
export interface NeuralColor {
  hue: number;        // 0-360
  saturation: number; // 0-1
  brightness: number; // 0-1
}

/**
 * Convert neural state to HSV color
 */
export function neuralStateToColor(state: NeuralState): NeuralColor {
  // x (membrane potential) -> brightness
  const brightness = 0.5 + 0.5 * Math.tanh(state.x + 0.5);
  
  // y (recovery) -> hue shift
  const hue = (240 - state.y * 60) % 360;  // Blue to purple range
  
  // z (adaptation) -> saturation
  const saturation = 0.8 - state.z * 0.1;
  
  return {
    hue: Math.max(0, Math.min(360, hue)),
    saturation: Math.max(0, Math.min(1, saturation)),
    brightness: Math.max(0, Math.min(1, brightness)),
  };
}

/**
 * Detect current neural mode from state
 */
export function detectNeuralMode(
  state: NeuralState,
  thresholds: ModeThresholds = DEFAULT_MODE_THRESHOLDS
): NeuralMode {
  if (state.x < thresholds.restingMaxX) {
    return NeuralMode.RESTING;
  }
  
  if (state.x > thresholds.spikeThreshold) {
    // Check recent history for burst pattern
    // For now, simplified: high x = spiking
    return NeuralMode.SPIKING;
  }
  
  // Default to chaotic if unclear
  return NeuralMode.CHAOTIC;
}
