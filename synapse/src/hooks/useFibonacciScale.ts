/**
 * SYNAPSE Hook: useFibonacciScale
 * React hook for managing Fibonacci scale transitions
 */

import { useState, useCallback, useEffect } from 'react';
import {
  Scale,
  ScaleTransition,
  getNextScale,
  getPreviousScale,
  SCALE_INFO,
} from '../types/scales';

/**
 * Hook configuration
 */
export interface UseScaleConfig {
  initialScale?: Scale;
  minScale?: Scale;
  maxScale?: Scale;
  animationDuration?: number;
}

/**
 * Hook return value
 */
export interface UseScaleResult {
  currentScale: Scale;
  targetScale: Scale;
  isTransitioning: boolean;
  transitionProgress: number;
  scaleInfo: typeof SCALE_INFO[Scale];
  canZoomIn: boolean;
  canZoomOut: boolean;
  zoomIn: () => void;
  zoomOut: () => void;
  setScale: (scale: Scale) => void;
  history: ScaleTransition[];
}

/**
 * useFibonacciScale hook
 * Manages current visualization scale and transitions
 */
export function useFibonacciScale(config: UseScaleConfig = {}): UseScaleResult {
  const {
    initialScale = Scale.TEAM,
    minScale = Scale.NODE,
    maxScale = Scale.NOOSPHERE,
    animationDuration = 1000, // ms
  } = config;
  
  const [currentScale, setCurrentScale] = useState<Scale>(initialScale);
  const [targetScale, setTargetScale] = useState<Scale>(initialScale);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [transitionProgress, setTransitionProgress] = useState(0);
  const [history, setHistory] = useState<ScaleTransition[]>([]);
  
  // Animate transition
  useEffect(() => {
    if (currentScale === targetScale) {
      setIsTransitioning(false);
      setTransitionProgress(0);
      return;
    }
    
    setIsTransitioning(true);
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(1, elapsed / animationDuration);
      
      // Ease in-out
      const eased = progress < 0.5
        ? 2 * progress * progress
        : 1 - Math.pow(-2 * progress + 2, 2) / 2;
      
      setTransitionProgress(eased);
      
      if (progress >= 1) {
        setCurrentScale(targetScale);
        setIsTransitioning(false);
        setTransitionProgress(0);
      } else {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }, [currentScale, targetScale, animationDuration]);
  
  const zoomIn = useCallback(() => {
    const next = getNextScale(currentScale);
    if (next && next <= maxScale) {
      setTargetScale(next);
      setHistory(prev => [
        ...prev,
        {
          from: currentScale,
          to: next,
          direction: 'zoom_in',
          timestamp: Date.now(),
        },
      ]);
    }
  }, [currentScale, maxScale]);
  
  const zoomOut = useCallback(() => {
    const prev = getPreviousScale(currentScale);
    if (prev && prev >= minScale) {
      setTargetScale(prev);
      setHistory(h => [
        ...h,
        {
          from: currentScale,
          to: prev,
          direction: 'zoom_out',
          timestamp: Date.now(),
        },
      ]);
    }
  }, [currentScale, minScale]);
  
  const setScale = useCallback((scale: Scale) => {
    if (scale >= minScale && scale <= maxScale) {
      setTargetScale(scale);
      setHistory(prev => [
        ...prev,
        {
          from: currentScale,
          to: scale,
          direction: scale > currentScale ? 'zoom_in' : 'zoom_out',
          timestamp: Date.now(),
        },
      ]);
    }
  }, [currentScale, minScale, maxScale]);
  
  const canZoomIn = getNextScale(currentScale) !== null && 
                    (getNextScale(currentScale) || 0) <= maxScale;
  const canZoomOut = getPreviousScale(currentScale) !== null &&
                     (getPreviousScale(currentScale) || 0) >= minScale;
  
  const scaleInfo = SCALE_INFO[currentScale];
  
  return {
    currentScale,
    targetScale,
    isTransitioning,
    transitionProgress,
    scaleInfo,
    canZoomIn,
    canZoomOut,
    zoomIn,
    zoomOut,
    setScale,
    history,
  };
}

/**
 * useScaleAdaptive hook
 * Automatically adjust scale based on entity count
 */
export function useScaleAdaptive(entityCount: number): Scale {
  const [scale, setScale] = useState<Scale>(Scale.NODE);
  
  useEffect(() => {
    // Find appropriate scale for entity count
    const scales = Object.values(Scale).filter(v => typeof v === 'number') as number[];
    const sorted = scales.sort((a, b) => a - b);
    
    let bestScale = Scale.NODE;
    for (const s of sorted) {
      if (entityCount <= s) {
        bestScale = s as Scale;
        break;
      }
    }
    
    setScale(bestScale);
  }, [entityCount]);
  
  return scale;
}

/**
 * useScaleInfo hook
 * Get detailed information about current scale
 */
export function useScaleInfo(scale: Scale) {
  return SCALE_INFO[scale];
}
