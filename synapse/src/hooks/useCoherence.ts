/**
 * SYNAPSE Hook: useCoherence
 * React hook for coherence calculation and tracking
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { CoherenceMetrics } from '../types/coherence';
import {
  createDefaultCoherence,
  calculateCoherence,
  interpolateCoherence,
  coherenceGradient,
  applyCoherenceDecay,
  analyzeRelationshipCoherence,
  COHERENCE_THRESHOLD,
} from '../utils/coherence';
import { Relationship } from '../types/entities';

/**
 * Hook configuration
 */
export interface UseCoherenceConfig {
  initialCoherence?: CoherenceMetrics;
  decayRate?: number;
  updateInterval?: number;
  autoDecay?: boolean;
}

/**
 * Hook return value
 */
export interface UseCoherenceResult {
  coherence: CoherenceMetrics;
  isCoherent: boolean;
  gradient: number;
  history: CoherenceMetrics[];
  setCoherence: (metrics: CoherenceMetrics) => void;
  updateFromComponents: (curl: number, potential: number, dispersion: number) => void;
  updateFromRelationships: (entityCount: number, relationships: Relationship[]) => void;
  reset: () => void;
}

/**
 * useCoherence hook
 * Manages coherence state with optional decay
 */
export function useCoherence(config: UseCoherenceConfig = {}): UseCoherenceResult {
  const {
    initialCoherence = createDefaultCoherence(),
    decayRate = 0.001,
    updateInterval = 100, // ms
    autoDecay = false,
  } = config;
  
  const [coherence, setCoherenceState] = useState<CoherenceMetrics>(initialCoherence);
  const [history, setHistory] = useState<CoherenceMetrics[]>([initialCoherence]);
  
  // Apply decay over time
  useEffect(() => {
    if (!autoDecay) return;
    
    const interval = setInterval(() => {
      setCoherenceState(prev => {
        const decayed = applyCoherenceDecay(prev, updateInterval / 1000, decayRate);
        setHistory(h => [...h.slice(-99), decayed]); // Keep last 100
        return decayed;
      });
    }, updateInterval);
    
    return () => clearInterval(interval);
  }, [autoDecay, updateInterval, decayRate]);
  
  const setCoherence = useCallback((metrics: CoherenceMetrics) => {
    setCoherenceState(metrics);
    setHistory(prev => [...prev.slice(-99), metrics]);
  }, []);
  
  const updateFromComponents = useCallback((
    curl: number,
    potential: number,
    dispersion: number
  ) => {
    const newCoherence = calculateCoherence(curl, potential, dispersion);
    setCoherence(newCoherence);
  }, [setCoherence]);
  
  const updateFromRelationships = useCallback((
    entityCount: number,
    relationships: Relationship[]
  ) => {
    const threePhase = analyzeRelationshipCoherence(entityCount, relationships);
    updateFromComponents(threePhase.curl, threePhase.potential, threePhase.dispersion);
  }, [updateFromComponents]);
  
  const reset = useCallback(() => {
    const initial = createDefaultCoherence();
    setCoherenceState(initial);
    setHistory([initial]);
  }, []);
  
  // Derived values
  const isCoherent = coherence.overall >= COHERENCE_THRESHOLD;
  const gradient = history.length > 1 
    ? coherenceGradient(coherence, history[history.length - 2])
    : 0;
  
  return {
    coherence,
    isCoherent,
    gradient,
    history,
    setCoherence,
    updateFromComponents,
    updateFromRelationships,
    reset,
  };
}

/**
 * useCoherenceAnimation hook
 * Animates coherence transition between two states
 */
export function useCoherenceAnimation(
  from: CoherenceMetrics,
  to: CoherenceMetrics,
  duration: number = 1000 // ms
): CoherenceMetrics {
  const [current, setCurrent] = useState<CoherenceMetrics>(from);
  const [startTime] = useState<number>(Date.now());
  
  useEffect(() => {
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const t = Math.min(1, elapsed / duration);
      
      // Ease in-out
      const eased = t < 0.5
        ? 2 * t * t
        : 1 - Math.pow(-2 * t + 2, 2) / 2;
      
      const interpolated = interpolateCoherence(from, to, eased);
      setCurrent(interpolated);
      
      if (t < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }, [from, to, duration, startTime]);
  
  return current;
}

/**
 * useCoherenceThreshold hook
 * Track when coherence crosses the 42.00055 threshold
 */
export function useCoherenceThreshold(coherence: CoherenceMetrics): {
  justCrossed: boolean;
  direction: 'up' | 'down' | null;
} {
  const [prevCoherent, setPrevCoherent] = useState<boolean>(
    coherence.overall >= COHERENCE_THRESHOLD
  );
  const [justCrossed, setJustCrossed] = useState(false);
  const [direction, setDirection] = useState<'up' | 'down' | null>(null);
  
  useEffect(() => {
    const isCoherent = coherence.overall >= COHERENCE_THRESHOLD;
    
    if (isCoherent !== prevCoherent) {
      setJustCrossed(true);
      setDirection(isCoherent ? 'up' : 'down');
      setPrevCoherent(isCoherent);
      
      // Reset flag after a delay
      const timeout = setTimeout(() => {
        setJustCrossed(false);
        setDirection(null);
      }, 1000);
      
      return () => clearTimeout(timeout);
    }
  }, [coherence.overall, prevCoherent]);
  
  return { justCrossed, direction };
}
