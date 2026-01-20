/**
 * SYNAPSE Type Definitions: Entities
 * Defines entity types across the Fibonacci scale hierarchy
 */

import { Scale } from './scales';
import { CoherenceMetrics } from './coherence';
import { NeuralState } from './neural';

/**
 * Base entity in the SYNAPSE visualization
 */
export interface Entity {
  id: string;
  name: string;
  type: EntityType;
  scale: Scale;
  position: Vector3D;
  coherence: CoherenceMetrics;
  neural: NeuralState;
  metadata?: Record<string, unknown>;
}

/**
 * Entity types mapped to their domain
 */
export enum EntityType {
  // Code entities
  FUNCTION = 'function',
  FILE = 'file',
  MODULE = 'module',
  REPOSITORY = 'repository',
  
  // Human entities
  USER = 'user',
  TEAM = 'team',
  DEPARTMENT = 'department',
  ORGANIZATION = 'organization',
  
  // Abstract entities
  CONCEPT = 'concept',
  DECISION = 'decision',
  TASK = 'task',
  ATOM = 'atom',
  
  // System entities
  SERVICE = 'service',
  API = 'api',
  DATABASE = 'database',
  QUEUE = 'queue',
}

/**
 * Relationship between entities
 */
export interface Relationship {
  id: string;
  source: string;  // Entity ID
  target: string;  // Entity ID
  type: RelationType;
  strength: number;  // 0-1
  coherenceContribution: number;  // Can be negative (dispersion)
}

/**
 * Types of relationships
 */
export enum RelationType {
  DEPENDS_ON = 'depends_on',
  CALLS = 'calls',
  IMPORTS = 'imports',
  CONTAINS = 'contains',
  COLLABORATES = 'collaborates',
  REPORTS_TO = 'reports_to',
  ENTANGLED = 'entangled',  // Quantum superposition
}

/**
 * 3D vector for positioning
 */
export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

/**
 * Superposition state for quantum-inspired interactions
 */
export interface SuperpositionState {
  entity: Entity;
  probabilities: Map<string, number>;  // State -> probability
  collapsed: boolean;
  observedState?: string;
}

/**
 * Entity graph for visualization
 */
export interface EntityGraph {
  entities: Map<string, Entity>;
  relationships: Relationship[];
  bounds: {
    min: Vector3D;
    max: Vector3D;
  };
  timestamp: number;
}
