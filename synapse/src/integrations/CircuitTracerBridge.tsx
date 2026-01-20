/**
 * SYNAPSE Integration: CircuitTracerBridge
 * Bridge to Anthropic's Circuit Tracer for neural interpretability
 * 
 * Maps neural circuit structures to SYNAPSE entities:
 * - Attention heads → Superposition clouds
 * - Layer flow → Fibonacci helix
 * - Feature directions → Coherence vectors
 * 
 * ATOM: ATOM-ISOMORPHISM-20260119-001-unified-circuit
 */

import { Entity, EntityType, Relationship, RelationType, Vector3D } from '../types/entities';
import { CoherenceMetrics } from '../types/coherence';
import { NeuralState } from '../types/neural';
import { Scale } from '../types/scales';

/**
 * Neural circuit from Circuit Tracer
 */
export interface NeuralCircuit {
  id: string;
  name: string;
  layers: NeuralLayer[];
  connections: NeuralConnection[];
  attentionHeads: AttentionHead[];
  featureDirections: FeatureDirection[];
}

/**
 * Layer in neural network
 */
export interface NeuralLayer {
  id: string;
  index: number;
  neurons: number;
  activationPattern: number[];
}

/**
 * Connection between layers
 */
export interface NeuralConnection {
  source: string;  // Layer ID
  target: string;  // Layer ID
  weights: number[][];
  strength: number;
}

/**
 * Attention head in transformer
 */
export interface AttentionHead {
  id: string;
  layer: number;
  head: number;
  querySample: number[];
  keySample: number[];
  valueSample: number[];
  attentionWeights: number[][];
}

/**
 * Feature direction discovered by Circuit Tracer
 */
export interface FeatureDirection {
  id: string;
  name: string;
  direction: number[];
  magnitude: number;
  interpretation: string;
}

/**
 * Convert neural circuit to SYNAPSE entities
 */
export class CircuitTracerBridge {
  /**
   * Convert entire circuit to entity graph
   */
  static convertCircuit(circuit: NeuralCircuit): {
    entities: Entity[];
    relationships: Relationship[];
  } {
    const entities: Entity[] = [];
    const relationships: Relationship[] = [];
    
    // Convert layers to entities
    circuit.layers.forEach((layer, index) => {
      const entity = this.convertLayer(layer, index, circuit.layers.length);
      entities.push(entity);
    });
    
    // Convert attention heads to superposition entities
    circuit.attentionHeads.forEach((head) => {
      const entity = this.convertAttentionHead(head, circuit.layers.length);
      entities.push(entity);
    });
    
    // Convert feature directions to coherence vectors
    circuit.featureDirections.forEach((feature) => {
      const entity = this.convertFeatureDirection(feature);
      entities.push(entity);
    });
    
    // Convert connections to relationships
    circuit.connections.forEach((conn) => {
      const relationship = this.convertConnection(conn);
      relationships.push(relationship);
    });
    
    return { entities, relationships };
  }
  
  /**
   * Convert neural layer to entity
   */
  private static convertLayer(
    layer: NeuralLayer,
    index: number,
    totalLayers: number
  ): Entity {
    const PHI = 1.6180339887;
    
    // Position in Fibonacci helix
    const t = (index / totalLayers) * Math.PI * 2;
    const radius = Math.pow(PHI, t / (2 * Math.PI));
    
    const position: Vector3D = {
      x: radius * Math.cos(t),
      y: radius * Math.sin(t),
      z: t * 0.5,
    };
    
    // Calculate coherence from activation pattern
    const coherence = this.calculateLayerCoherence(layer);
    
    // Neural state
    const neural: NeuralState = {
      x: this.averageActivation(layer.activationPattern),
      y: this.activationVariance(layer.activationPattern),
      z: 0.00055,  // Epsilon
      mode: 'tonic',
      burstCount: 0,
      lastBurst: 0,
    };
    
    return {
      id: layer.id,
      name: `Layer ${layer.index}`,
      type: EntityType.MODULE,
      scale: this.layerToScale(index, totalLayers),
      position,
      coherence,
      neural,
      metadata: {
        neurons: layer.neurons,
        index: layer.index,
      },
    };
  }
  
  /**
   * Convert attention head to superposition entity
   */
  private static convertAttentionHead(
    head: AttentionHead,
    totalLayers: number
  ): Entity {
    // Attention heads are curl (entanglement)
    const curl = this.calculateAttentionCurl(head.attentionWeights);
    
    // Position around the layer
    const layerT = (head.layer / totalLayers) * Math.PI * 2;
    const headAngle = (head.head / 12) * Math.PI * 2;  // Assume 12 heads
    
    const position: Vector3D = {
      x: Math.cos(layerT + headAngle) * 2,
      y: Math.sin(layerT + headAngle) * 2,
      z: layerT * 0.5,
    };
    
    const coherence: CoherenceMetrics = {
      curl,
      potential: this.calculatePotential(head.querySample, head.keySample),
      dispersion: this.calculateDispersion(head.valueSample),
      timestamp: Date.now(),
    };
    
    const neural: NeuralState = {
      x: curl,
      y: coherence.potential,
      z: coherence.dispersion,
      mode: 'bursting',
      burstCount: Math.floor(curl * 100),
      lastBurst: Date.now(),
    };
    
    return {
      id: head.id,
      name: `Attention ${head.layer}.${head.head}`,
      type: EntityType.CONCEPT,
      scale: Scale.NODE,
      position,
      coherence,
      neural,
      metadata: {
        layer: head.layer,
        head: head.head,
        type: 'attention',
      },
    };
  }
  
  /**
   * Convert feature direction to coherence vector entity
   */
  private static convertFeatureDirection(feature: FeatureDirection): Entity {
    // Feature directions are potential (superposition basis states)
    const potential = feature.magnitude;
    
    // Position based on direction (PCA-style)
    const position: Vector3D = {
      x: feature.direction[0] || 0,
      y: feature.direction[1] || 0,
      z: feature.direction[2] || 0,
    };
    
    const coherence: CoherenceMetrics = {
      curl: 0.1,  // Low curl (stable feature)
      potential,
      dispersion: 0.0001,  // Optimal dispersion
      timestamp: Date.now(),
    };
    
    const neural: NeuralState = {
      x: potential,
      y: 0,
      z: 0.00055,
      mode: 'tonic',
      burstCount: 0,
      lastBurst: 0,
    };
    
    return {
      id: feature.id,
      name: feature.name,
      type: EntityType.CONCEPT,
      scale: Scale.NODE,
      position,
      coherence,
      neural,
      metadata: {
        interpretation: feature.interpretation,
        magnitude: feature.magnitude,
        type: 'feature',
      },
    };
  }
  
  /**
   * Convert connection to relationship
   */
  private static convertConnection(conn: NeuralConnection): Relationship {
    return {
      id: `${conn.source}-${conn.target}`,
      source: conn.source,
      target: conn.target,
      type: RelationType.CALLS,
      strength: conn.strength,
      coherenceContribution: conn.strength > 0.5 ? 0.1 : -0.1,
    };
  }
  
  /**
   * Helper: Calculate curl from attention weights
   */
  private static calculateAttentionCurl(weights: number[][]): number {
    // Attention curl = measure of circulation in attention pattern
    let curl = 0;
    for (let i = 0; i < weights.length; i++) {
      for (let j = 0; j < weights[i].length; j++) {
        const nextI = (i + 1) % weights.length;
        const nextJ = (j + 1) % weights[i].length;
        curl += weights[i][j] * (weights[nextI][j] - weights[i][nextJ]);
      }
    }
    return Math.abs(curl) / (weights.length * weights[0].length);
  }
  
  /**
   * Helper: Calculate potential from query/key
   */
  private static calculatePotential(query: number[], key: number[]): number {
    let dot = 0;
    for (let i = 0; i < Math.min(query.length, key.length); i++) {
      dot += query[i] * key[i];
    }
    return Math.abs(dot) / Math.min(query.length, key.length);
  }
  
  /**
   * Helper: Calculate dispersion from value vector
   */
  private static calculateDispersion(value: number[]): number {
    const mean = value.reduce((a, b) => a + b, 0) / value.length;
    const variance = value.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / value.length;
    return Math.sqrt(variance);
  }
  
  /**
   * Helper: Calculate layer coherence
   */
  private static calculateLayerCoherence(layer: NeuralLayer): CoherenceMetrics {
    return {
      curl: this.activationVariance(layer.activationPattern) * 0.5,
      potential: this.averageActivation(layer.activationPattern),
      dispersion: this.activationVariance(layer.activationPattern),
      timestamp: Date.now(),
    };
  }
  
  /**
   * Helper: Average activation
   */
  private static averageActivation(pattern: number[]): number {
    return pattern.reduce((a, b) => a + b, 0) / pattern.length;
  }
  
  /**
   * Helper: Activation variance
   */
  private static activationVariance(pattern: number[]): number {
    const mean = this.averageActivation(pattern);
    const variance = pattern.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / pattern.length;
    return Math.sqrt(variance);
  }
  
  /**
   * Helper: Map layer index to scale
   */
  private static layerToScale(index: number, total: number): Scale {
    const ratio = index / total;
    if (ratio < 0.2) return Scale.NODE;
    if (ratio < 0.4) return Scale.TEAM;
    if (ratio < 0.6) return Scale.ORG;
    if (ratio < 0.8) return Scale.ENTERPRISE;
    return Scale.NATION;
  }
}

export default CircuitTracerBridge;
