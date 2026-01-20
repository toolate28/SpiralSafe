/**
 * SYNAPSE Hook: useSuperposition
 * React hook for quantum superposition state management
 */

import { useState, useCallback, useEffect } from 'react';
import { SuperpositionState, Entity } from '../types/entities';

/**
 * Hook configuration
 */
export interface UseSuperpositionConfig {
  collapseAnimationDuration?: number;
  decoherenceRate?: number;
}

/**
 * Collapse event
 */
export interface CollapseEvent {
  entityId: string;
  observedState: string;
  timestamp: number;
}

/**
 * Hook return value
 */
export interface UseSuperpositionResult {
  superpositions: Map<string, SuperpositionState>;
  getSuperposition: (entityId: string) => SuperpositionState | undefined;
  createSuperposition: (entity: Entity, states: Map<string, number>) => void;
  observe: (entityId: string) => string | null;
  isCollapsing: (entityId: string) => boolean;
  collapseProgress: (entityId: string) => number;
  reset: (entityId: string) => void;
  resetAll: () => void;
  collapseHistory: CollapseEvent[];
}

/**
 * useSuperposition hook
 * Manages quantum superposition states and collapse animations
 */
export function useSuperposition(config: UseSuperpositionConfig = {}): UseSuperpositionResult {
  const {
    collapseAnimationDuration = 1000, // ms
    decoherenceRate = 0.001,
  } = config;
  
  const [superpositions, setSuperpositions] = useState<Map<string, SuperpositionState>>(
    new Map()
  );
  const [collapsingEntities, setCollapsingEntities] = useState<Map<string, number>>(
    new Map() // entityId -> collapse start time
  );
  const [collapseProgress, setCollapseProgressState] = useState<Map<string, number>>(
    new Map() // entityId -> progress [0, 1]
  );
  const [collapseHistory, setCollapseHistory] = useState<CollapseEvent[]>([]);
  
  // Animate collapses
  useEffect(() => {
    if (collapsingEntities.size === 0) return;
    
    const animate = () => {
      const now = Date.now();
      const newProgress = new Map<string, number>();
      const stillCollapsing = new Map<string, number>();
      
      collapsingEntities.forEach((startTime, entityId) => {
        const elapsed = now - startTime;
        const progress = Math.min(1, elapsed / collapseAnimationDuration);
        
        // Ease in-out cubic
        const eased = progress < 0.5
          ? 4 * progress * progress * progress
          : 1 - Math.pow(-2 * progress + 2, 3) / 2;
        
        newProgress.set(entityId, eased);
        
        if (progress < 1) {
          stillCollapsing.set(entityId, startTime);
        } else {
          // Collapse complete - finalize state
          setSuperpositions(prev => {
            const updated = new Map(prev);
            const state = updated.get(entityId);
            if (state && !state.collapsed) {
              updated.set(entityId, { ...state, collapsed: true });
            }
            return updated;
          });
        }
      });
      
      setCollapseProgressState(newProgress);
      setCollapsingEntities(stillCollapsing);
      
      if (stillCollapsing.size > 0) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }, [collapsingEntities, collapseAnimationDuration]);
  
  // Apply decoherence over time
  useEffect(() => {
    const interval = setInterval(() => {
      setSuperpositions(prev => {
        const updated = new Map(prev);
        
        prev.forEach((state, entityId) => {
          if (state.collapsed) return;
          
          // Gradually reduce probability spread (decoherence)
          const newProbs = new Map(state.probabilities);
          let maxProb = 0;
          let maxState = '';
          
          newProbs.forEach((prob, stateName) => {
            if (prob > maxProb) {
              maxProb = prob;
              maxState = stateName;
            }
          });
          
          // Increase max probability, decrease others
          newProbs.forEach((prob, stateName) => {
            if (stateName === maxState) {
              newProbs.set(stateName, Math.min(1, prob + decoherenceRate));
            } else {
              newProbs.set(stateName, Math.max(0, prob - decoherenceRate / (newProbs.size - 1)));
            }
          });
          
          updated.set(entityId, { ...state, probabilities: newProbs });
        });
        
        return updated;
      });
    }, 100); // Update every 100ms
    
    return () => clearInterval(interval);
  }, [decoherenceRate]);
  
  const getSuperposition = useCallback((entityId: string) => {
    return superpositions.get(entityId);
  }, [superpositions]);
  
  const createSuperposition = useCallback((
    entity: Entity,
    states: Map<string, number>
  ) => {
    // Normalize probabilities
    const total = Array.from(states.values()).reduce((sum, p) => sum + p, 0);
    const normalized = new Map<string, number>();
    
    states.forEach((prob, state) => {
      normalized.set(state, prob / total);
    });
    
    const superposition: SuperpositionState = {
      entity,
      probabilities: normalized,
      collapsed: false,
    };
    
    setSuperpositions(prev => new Map(prev).set(entity.id, superposition));
  }, []);
  
  const observe = useCallback((entityId: string): string | null => {
    const state = superpositions.get(entityId);
    if (!state || state.collapsed) return null;
    
    // Measure: collapse to definite state based on probabilities
    const rand = Math.random();
    let cumulative = 0;
    let selectedState = '';
    
    for (const [stateName, prob] of state.probabilities) {
      cumulative += prob;
      if (rand < cumulative) {
        selectedState = stateName;
        break;
      }
    }
    
    // Start collapse animation
    setCollapsingEntities(prev => new Map(prev).set(entityId, Date.now()));
    
    // Update superposition state
    setSuperpositions(prev => {
      const updated = new Map(prev);
      updated.set(entityId, {
        ...state,
        observedState: selectedState,
      });
      return updated;
    });
    
    // Record in history
    setCollapseHistory(prev => [
      ...prev,
      {
        entityId,
        observedState: selectedState,
        timestamp: Date.now(),
      },
    ]);
    
    return selectedState;
  }, [superpositions]);
  
  const isCollapsing = useCallback((entityId: string) => {
    return collapsingEntities.has(entityId);
  }, [collapsingEntities]);
  
  const getCollapseProgress = useCallback((entityId: string) => {
    return collapseProgress.get(entityId) || 0;
  }, [collapseProgress]);
  
  const reset = useCallback((entityId: string) => {
    setSuperpositions(prev => {
      const updated = new Map(prev);
      const state = updated.get(entityId);
      if (state) {
        updated.set(entityId, {
          ...state,
          collapsed: false,
          observedState: undefined,
        });
      }
      return updated;
    });
    
    setCollapsingEntities(prev => {
      const updated = new Map(prev);
      updated.delete(entityId);
      return updated;
    });
  }, []);
  
  const resetAll = useCallback(() => {
    setSuperpositions(new Map());
    setCollapsingEntities(new Map());
    setCollapseProgressState(new Map());
    setCollapseHistory([]);
  }, []);
  
  return {
    superpositions,
    getSuperposition,
    createSuperposition,
    observe,
    isCollapsing,
    collapseProgress: getCollapseProgress,
    reset,
    resetAll,
    collapseHistory,
  };
}

/**
 * useEntanglement hook
 * Manage entangled entity pairs
 */
export interface EntanglementPair {
  entity1Id: string;
  entity2Id: string;
  correlationStrength: number;
}

export function useEntanglement() {
  const [entanglements, setEntanglements] = useState<EntanglementPair[]>([]);
  
  const createEntanglement = useCallback((
    entity1Id: string,
    entity2Id: string,
    strength: number = 1
  ) => {
    setEntanglements(prev => [
      ...prev,
      {
        entity1Id,
        entity2Id,
        correlationStrength: strength,
      },
    ]);
  }, []);
  
  const breakEntanglement = useCallback((entity1Id: string, entity2Id: string) => {
    setEntanglements(prev =>
      prev.filter(e =>
        !(e.entity1Id === entity1Id && e.entity2Id === entity2Id) &&
        !(e.entity1Id === entity2Id && e.entity2Id === entity1Id)
      )
    );
  }, []);
  
  const getEntangled = useCallback((entityId: string): string[] => {
    return entanglements
      .filter(e => e.entity1Id === entityId || e.entity2Id === entityId)
      .map(e => e.entity1Id === entityId ? e.entity2Id : e.entity1Id);
  }, [entanglements]);
  
  return {
    entanglements,
    createEntanglement,
    breakEntanglement,
    getEntangled,
  };
}
