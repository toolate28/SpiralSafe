/**
 * SYNAPSE Type Definitions: Scales
 * Fibonacci scale hierarchy from quantum foam to noosphere
 */

/**
 * Fibonacci-based scale hierarchy
 * Each level represents a golden ratio expansion
 */
export enum Scale {
  QUANTUM = 0,        // ε = 0.00055 (quantum foam)
  NODE = 1,           // 1 entity (user, file, function)
  PAIR = 1,           // 1 relationship
  TRIAD = 2,          // 2 connections (minimal network)
  CLUSTER = 3,        // 3 (triangle, minimal 2D)
  TEAM = 5,           // 5 (minimal viable team)
  SQUAD = 8,          // 8 (two-pizza team)
  DEPARTMENT = 13,    // 13 (departmental scale)
  DIVISION = 21,      // 21 (divisional)
  ORGANIZATION = 34,  // 34 (org scale)
  ENTERPRISE = 55,    // 55 (enterprise)
  SECTOR = 89,        // 89 (industry sector)
  NATION = 144,       // 144 (national scale)
  CIVILIZATION = 233, // 233 (civilizational)
  NOOSPHERE = 377,    // 377 (planetary consciousness)
}

/**
 * Scale metadata
 */
export interface ScaleInfo {
  scale: Scale;
  fibonacciNumber: number;
  name: string;
  description: string;
  typicalEntities: string[];
}

/**
 * Scale transition event
 */
export interface ScaleTransition {
  from: Scale;
  to: Scale;
  direction: 'zoom_in' | 'zoom_out';
  timestamp: number;
}

/**
 * Get Fibonacci number for a scale
 */
export function getFibonacciNumber(scale: Scale): number {
  return scale;
}

/**
 * Get next scale up in hierarchy
 */
export function getNextScale(current: Scale): Scale | null {
  const scales = Object.values(Scale).filter(v => typeof v === 'number') as number[];
  const sorted = scales.sort((a, b) => a - b);
  const currentIndex = sorted.indexOf(current);
  
  if (currentIndex === -1 || currentIndex === sorted.length - 1) {
    return null;
  }
  
  return sorted[currentIndex + 1] as Scale;
}

/**
 * Get previous scale down in hierarchy
 */
export function getPreviousScale(current: Scale): Scale | null {
  const scales = Object.values(Scale).filter(v => typeof v === 'number') as number[];
  const sorted = scales.sort((a, b) => a - b);
  const currentIndex = sorted.indexOf(current);
  
  if (currentIndex <= 0) {
    return null;
  }
  
  return sorted[currentIndex - 1] as Scale;
}

/**
 * Scale information lookup
 */
export const SCALE_INFO: Record<Scale, ScaleInfo> = {
  [Scale.QUANTUM]: {
    scale: Scale.QUANTUM,
    fibonacciNumber: 0,
    name: 'Quantum Foam',
    description: 'ε = 0.00055, the base uncertainty layer',
    typicalEntities: ['noise', 'uncertainty', 'epsilon'],
  },
  [Scale.NODE]: {
    scale: Scale.NODE,
    fibonacciNumber: 1,
    name: 'Individual Node',
    description: 'Single entity: user, file, function',
    typicalEntities: ['user', 'file', 'function', 'task'],
  },
  [Scale.PAIR]: {
    scale: Scale.PAIR,
    fibonacciNumber: 1,
    name: 'Pair',
    description: 'Single relationship between entities',
    typicalEntities: ['connection', 'dependency', 'collaboration'],
  },
  [Scale.TRIAD]: {
    scale: Scale.TRIAD,
    fibonacciNumber: 2,
    name: 'Triad',
    description: 'Minimal network with 2 connections',
    typicalEntities: ['small team', 'module trio'],
  },
  [Scale.CLUSTER]: {
    scale: Scale.CLUSTER,
    fibonacciNumber: 3,
    name: 'Cluster',
    description: 'Triangle, minimal 2D structure',
    typicalEntities: ['work group', 'package'],
  },
  [Scale.TEAM]: {
    scale: Scale.TEAM,
    fibonacciNumber: 5,
    name: 'Team',
    description: 'Minimal viable team',
    typicalEntities: ['scrum team', 'library'],
  },
  [Scale.SQUAD]: {
    scale: Scale.SQUAD,
    fibonacciNumber: 8,
    name: 'Squad',
    description: 'Two-pizza team',
    typicalEntities: ['product team', 'service'],
  },
  [Scale.DEPARTMENT]: {
    scale: Scale.DEPARTMENT,
    fibonacciNumber: 13,
    name: 'Department',
    description: 'Departmental scale',
    typicalEntities: ['engineering dept', 'monorepo'],
  },
  [Scale.DIVISION]: {
    scale: Scale.DIVISION,
    fibonacciNumber: 21,
    name: 'Division',
    description: 'Divisional scale',
    typicalEntities: ['business unit', 'platform'],
  },
  [Scale.ORGANIZATION]: {
    scale: Scale.ORGANIZATION,
    fibonacciNumber: 34,
    name: 'Organization',
    description: 'Organizational scale',
    typicalEntities: ['company', 'ecosystem'],
  },
  [Scale.ENTERPRISE]: {
    scale: Scale.ENTERPRISE,
    fibonacciNumber: 55,
    name: 'Enterprise',
    description: 'Enterprise scale',
    typicalEntities: ['corporation', 'industry'],
  },
  [Scale.SECTOR]: {
    scale: Scale.SECTOR,
    fibonacciNumber: 89,
    name: 'Sector',
    description: 'Industry sector',
    typicalEntities: ['tech sector', 'infrastructure'],
  },
  [Scale.NATION]: {
    scale: Scale.NATION,
    fibonacciNumber: 144,
    name: 'Nation',
    description: 'National scale (e.g., US Congress: 535 members)',
    typicalEntities: ['government', 'military', 'national systems'],
  },
  [Scale.CIVILIZATION]: {
    scale: Scale.CIVILIZATION,
    fibonacciNumber: 233,
    name: 'Civilization',
    description: 'Civilizational scale',
    typicalEntities: ['global networks', 'international systems'],
  },
  [Scale.NOOSPHERE]: {
    scale: Scale.NOOSPHERE,
    fibonacciNumber: 377,
    name: 'Noosphere',
    description: 'Planetary consciousness',
    typicalEntities: ['collective intelligence', 'planetary systems'],
  },
};
