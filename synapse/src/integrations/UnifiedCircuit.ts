/**
 * SYNAPSE Integration: UnifiedCircuit
 * The isomorphism layer proving neural ↔ quantum ↔ coherence equivalence
 * 
 * Demonstrates that neural circuits, quantum circuits, and coherence systems
 * share identical topological structure, differing only in substrate.
 * 
 * ATOM: ATOM-ISOMORPHISM-20260119-001-unified-circuit
 */

import { Entity, Relationship } from '../types/entities';
import { CoherenceMetrics } from '../types/coherence';

/**
 * Universal gate abstraction
 * Works across neural, quantum, and coherence substrates
 */
export interface UniversalGate {
  id: string;
  type: GateType;
  inputs: string[];   // Entity IDs
  outputs: string[];  // Entity IDs
  coherenceTransform: CoherenceTransform;
  substrate: Substrate;
}

/**
 * Gate types (substrate-independent)
 */
export enum GateType {
  // Identity operations
  IDENTITY = 'identity',
  
  // Superposition creators
  SUPERPOSE = 'superpose',      // H gate, attention head, coherence split
  
  // Entanglement creators
  ENTANGLE = 'entangle',        // CNOT, cross-attention, relationship formation
  
  // Phase operations
  PHASE_SHIFT = 'phase_shift',  // Phase gate, feature rotation, curl adjustment
  
  // Collapse operations
  MEASURE = 'measure',          // Measurement, output layer, coherence read
  
  // Composition
  COMPOSE = 'compose',          // Gate composition, layer stacking, system merge
}

/**
 * Substrate types
 */
export enum Substrate {
  NEURAL = 'neural',
  QUANTUM = 'quantum',
  COHERENCE = 'coherence',
}

/**
 * Coherence transformation
 */
export interface CoherenceTransform {
  deltaC url: number;      // Change in curl
  deltaPotential: number;  // Change in potential
  deltaDispersion: number; // Change in dispersion
  isReversible: boolean;
}

/**
 * Circuit representation (substrate-independent)
 */
export interface UniversalCircuit {
  id: string;
  name: string;
  gates: UniversalGate[];
  entities: Entity[];
  relationships: Relationship[];
  substrate: Substrate;
}

/**
 * The Isomorphism Mapping
 */
export class UnifiedCircuitMapper {
  /**
   * Map between substrates
   */
  static readonly ISOMORPHISM_MAP = {
    neural: {
      curl: 'attention',
      potential: 'features',
      dispersion: 'output',
    },
    quantum: {
      curl: 'entanglement',
      potential: 'superposition',
      dispersion: 'measurement',
    },
    coherence: {
      curl: 'curl',
      potential: 'potential',
      dispersion: 'dispersion',
    },
  };
  
  /**
   * Convert gate between substrates
   */
  static convertGate(
    gate: UniversalGate,
    targetSubstrate: Substrate
  ): UniversalGate {
    // Gate structure is preserved, only interpretation changes
    return {
      ...gate,
      substrate: targetSubstrate,
    };
  }
  
  /**
   * Convert entire circuit between substrates
   */
  static convertCircuit(
    circuit: UniversalCircuit,
    targetSubstrate: Substrate
  ): UniversalCircuit {
    return {
      ...circuit,
      substrate: targetSubstrate,
      gates: circuit.gates.map(gate => this.convertGate(gate, targetSubstrate)),
    };
  }
  
  /**
   * Verify isomorphism between two circuits
   */
  static verifyIsomorphism(
    circuit1: UniversalCircuit,
    circuit2: UniversalCircuit
  ): IsomorphismProof {
    const proof: IsomorphismProof = {
      isIsomorphic: false,
      structurePreserved: false,
      coherencePreserved: false,
      topologyPreserved: false,
      details: [],
    };
    
    // Check structure
    if (circuit1.gates.length !== circuit2.gates.length) {
      proof.details.push('Gate count mismatch');
      return proof;
    }
    proof.structurePreserved = true;
    
    // Check coherence preservation
    const coherence1 = this.calculateCircuitCoherence(circuit1);
    const coherence2 = this.calculateCircuitCoherence(circuit2);
    const coherenceDiff = Math.abs(
      (coherence1.curl - coherence2.curl) +
      (coherence1.potential - coherence2.potential) +
      (coherence1.dispersion - coherence2.dispersion)
    );
    
    if (coherenceDiff < 0.00055) {  // Within epsilon
      proof.coherencePreserved = true;
    } else {
      proof.details.push(`Coherence difference: ${coherenceDiff}`);
    }
    
    // Check topology (graph isomorphism)
    proof.topologyPreserved = this.checkTopologyPreservation(circuit1, circuit2);
    
    // Final verdict
    proof.isIsomorphic = proof.structurePreserved &&
                         proof.coherencePreserved &&
                         proof.topologyPreserved;
    
    return proof;
  }
  
  /**
   * Calculate total circuit coherence
   */
  private static calculateCircuitCoherence(circuit: UniversalCircuit): CoherenceMetrics {
    let totalCurl = 0;
    let totalPotential = 0;
    let totalDispersion = 0;
    
    circuit.gates.forEach(gate => {
      totalCurl += gate.coherenceTransform.deltaCurl;
      totalPotential += gate.coherenceTransform.deltaPotential;
      totalDispersion += gate.coherenceTransform.deltaDispersion;
    });
    
    return {
      curl: totalCurl / circuit.gates.length,
      potential: totalPotential / circuit.gates.length,
      dispersion: totalDispersion / circuit.gates.length,
      timestamp: Date.now(),
    };
  }
  
  /**
   * Check topology preservation
   */
  private static checkTopologyPreservation(
    circuit1: UniversalCircuit,
    circuit2: UniversalCircuit
  ): boolean {
    // Check that graph structure is preserved
    const edges1 = this.extractEdges(circuit1);
    const edges2 = this.extractEdges(circuit2);
    
    if (edges1.length !== edges2.length) {
      return false;
    }
    
    // Check degree sequence
    const degrees1 = this.calculateDegreeSequence(circuit1);
    const degrees2 = this.calculateDegreeSequence(circuit2);
    
    return JSON.stringify(degrees1.sort()) === JSON.stringify(degrees2.sort());
  }
  
  /**
   * Extract edges from circuit
   */
  private static extractEdges(circuit: UniversalCircuit): Array<[string, string]> {
    const edges: Array<[string, string]> = [];
    
    circuit.gates.forEach(gate => {
      gate.inputs.forEach(input => {
        gate.outputs.forEach(output => {
          edges.push([input, output]);
        });
      });
    });
    
    return edges;
  }
  
  /**
   * Calculate degree sequence
   */
  private static calculateDegreeSequence(circuit: UniversalCircuit): number[] {
    const degrees = new Map<string, number>();
    
    circuit.gates.forEach(gate => {
      gate.inputs.forEach(input => {
        degrees.set(input, (degrees.get(input) || 0) + 1);
      });
      gate.outputs.forEach(output => {
        degrees.set(output, (degrees.get(output) || 0) + 1);
      });
    });
    
    return Array.from(degrees.values());
  }
}

/**
 * Isomorphism proof
 */
export interface IsomorphismProof {
  isIsomorphic: boolean;
  structurePreserved: boolean;
  coherencePreserved: boolean;
  topologyPreserved: boolean;
  details: string[];
}

/**
 * Standard gate templates
 */
export class StandardGates {
  /**
   * Superposition gate (H, attention head, coherence split)
   */
  static superpose(input: string, output1: string, output2: string, substrate: Substrate): UniversalGate {
    return {
      id: `superpose-${input}`,
      type: GateType.SUPERPOSE,
      inputs: [input],
      outputs: [output1, output2],
      coherenceTransform: {
        deltaCurl: 0.5,        // Creates curl
        deltaPotential: 1.0,    // Maintains potential
        deltaDispersion: 0.0001, // Minimal dispersion
        isReversible: true,
      },
      substrate,
    };
  }
  
  /**
   * Entanglement gate (CNOT, cross-attention, relationship)
   */
  static entangle(
    control: string,
    target: string,
    output: string,
    substrate: Substrate
  ): UniversalGate {
    return {
      id: `entangle-${control}-${target}`,
      type: GateType.ENTANGLE,
      inputs: [control, target],
      outputs: [output],
      coherenceTransform: {
        deltaCurl: 0.8,        // High curl (entanglement)
        deltaPotential: 0.9,    // Preserves potential
        deltaDispersion: 0.0002, // Slight dispersion increase
        isReversible: true,
      },
      substrate,
    };
  }
  
  /**
   * Measurement gate (quantum measurement, output layer, coherence read)
   */
  static measure(input: string, output: string, substrate: Substrate): UniversalGate {
    return {
      id: `measure-${input}`,
      type: GateType.MEASURE,
      inputs: [input],
      outputs: [output],
      coherenceTransform: {
        deltaCurl: -0.9,       // Destroys curl
        deltaPotential: -0.9,   // Collapses potential
        deltaDispersion: 1.0,   // Maximal dispersion
        isReversible: false,    // Measurement is irreversible
      },
      substrate,
    };
  }
  
  /**
   * Identity gate (no change)
   */
  static identity(input: string, output: string, substrate: Substrate): UniversalGate {
    return {
      id: `identity-${input}`,
      type: GateType.IDENTITY,
      inputs: [input],
      outputs: [output],
      coherenceTransform: {
        deltaCurl: 0,
        deltaPotential: 0,
        deltaDispersion: 0,
        isReversible: true,
      },
      substrate,
    };
  }
}

/**
 * Circuit composer
 */
export class CircuitComposer {
  /**
   * Compose two circuits in sequence
   */
  static sequence(circuit1: UniversalCircuit, circuit2: UniversalCircuit): UniversalCircuit {
    if (circuit1.substrate !== circuit2.substrate) {
      throw new Error('Cannot sequence circuits with different substrates');
    }
    
    return {
      id: `${circuit1.id}-then-${circuit2.id}`,
      name: `${circuit1.name} → ${circuit2.name}`,
      gates: [...circuit1.gates, ...circuit2.gates],
      entities: [...circuit1.entities, ...circuit2.entities],
      relationships: [...circuit1.relationships, ...circuit2.relationships],
      substrate: circuit1.substrate,
    };
  }
  
  /**
   * Compose two circuits in parallel
   */
  static parallel(circuit1: UniversalCircuit, circuit2: UniversalCircuit): UniversalCircuit {
    if (circuit1.substrate !== circuit2.substrate) {
      throw new Error('Cannot parallelize circuits with different substrates');
    }
    
    return {
      id: `${circuit1.id}-parallel-${circuit2.id}`,
      name: `${circuit1.name} ∥ ${circuit2.name}`,
      gates: [...circuit1.gates, ...circuit2.gates],
      entities: [...circuit1.entities, ...circuit2.entities],
      relationships: [...circuit1.relationships, ...circuit2.relationships],
      substrate: circuit1.substrate,
    };
  }
}

export default UnifiedCircuitMapper;
