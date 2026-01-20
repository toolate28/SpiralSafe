/**
 * SYNAPSE Hook: useHindmarshRose
 * React hook for Hindmarsh-Rose neural dynamics
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  NeuralState,
  HRParameters,
  DEFAULT_HR_PARAMS,
  NeuralMode,
} from '../types/neural';
import {
  createInitialState,
  integrateHR,
  simulateHR,
  detectSpikes,
  calculateFiringRate,
} from '../utils/hindmarsh-rose';

/**
 * Hook configuration
 */
export interface UseHRConfig {
  params?: HRParameters;
  initialState?: NeuralState;
  dt?: number;
  autoStart?: boolean;
}

/**
 * Hook return value
 */
export interface UseHRResult {
  state: NeuralState;
  history: NeuralState[];
  isRunning: boolean;
  firingRate: number;
  spikeCount: number;
  start: () => void;
  stop: () => void;
  reset: () => void;
  setParams: (params: Partial<HRParameters>) => void;
}

/**
 * useHindmarshRose hook
 * Simulates HR neural dynamics with real-time integration
 */
export function useHindmarshRose(config: UseHRConfig = {}): UseHRResult {
  const {
    params = DEFAULT_HR_PARAMS,
    initialState = createInitialState(),
    dt = 0.01,
    autoStart = false,
  } = config;
  
  const [state, setState] = useState<NeuralState>(initialState);
  const [history, setHistory] = useState<NeuralState[]>([initialState]);
  const [isRunning, setIsRunning] = useState(autoStart);
  const [hrParams, setHRParams] = useState<HRParameters>(params);
  
  const animationFrameRef = useRef<number>();
  const lastTimeRef = useRef<number>(Date.now());
  const accumulatorRef = useRef<number>(0);
  
  // Animation loop
  useEffect(() => {
    if (!isRunning) return;
    
    const animate = () => {
      const now = Date.now();
      const elapsed = (now - lastTimeRef.current) / 1000; // Convert to seconds
      lastTimeRef.current = now;
      
      // Accumulate time
      accumulatorRef.current += elapsed;
      
      // Fixed timestep integration
      let newState = state;
      while (accumulatorRef.current >= dt) {
        newState = integrateHR(newState, dt, hrParams);
        accumulatorRef.current -= dt;
      }
      
      setState(newState);
      
      // Update history (keep last 1000 states)
      setHistory(prev => {
        const updated = [...prev, newState];
        return updated.slice(-1000);
      });
      
      animationFrameRef.current = requestAnimationFrame(animate);
    };
    
    animationFrameRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isRunning, state, dt, hrParams]);
  
  const start = useCallback(() => {
    setIsRunning(true);
    lastTimeRef.current = Date.now();
  }, []);
  
  const stop = useCallback(() => {
    setIsRunning(false);
  }, []);
  
  const reset = useCallback(() => {
    setState(initialState);
    setHistory([initialState]);
    accumulatorRef.current = 0;
  }, [initialState]);
  
  const setParams = useCallback((newParams: Partial<HRParameters>) => {
    setHRParams(prev => ({ ...prev, ...newParams }));
  }, []);
  
  // Calculate derived metrics
  const spikeCount = detectSpikes(history).length;
  const firingRate = history.length > 10 ? calculateFiringRate(history, dt) : 0;
  
  return {
    state,
    history,
    isRunning,
    firingRate,
    spikeCount,
    start,
    stop,
    reset,
    setParams,
  };
}

/**
 * useHRAnimation hook
 * Simpler hook for animation-driven HR visualization (no real-time)
 */
export function useHRAnimation(
  duration: number = 10,
  params: HRParameters = DEFAULT_HR_PARAMS
): NeuralState[] {
  const [states, setStates] = useState<NeuralState[]>([]);
  
  useEffect(() => {
    const initial = createInitialState();
    const simulated = simulateHR(initial, duration, 0.01, params);
    setStates(simulated);
  }, [duration, params]);
  
  return states;
}
