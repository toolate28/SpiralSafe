/**
 * SYNAPSE Integration: QubitSenseBridge
 * Bridge to QubitSense quantum algorithm framework
 * 
 * Maps quantum circuits to SYNAPSE entities:
 * - Qubits → Superposition entities
 * - Gates → Coherence transformations
 * - Measurements → Collapse events
 * 
 * ATOM: ATOM-ISOMORPHISM-20260119-001-unified-circuit
 */

import { Entity, EntityType, Relationship, RelationType, Vector3D } from '../types/entities';
import { CoherenceMetrics } from '../types/coherence';
import { NeuralState } from '../types/neural';
import { Scale } from '../types/scales';

/**
 * Quantum circuit from QubitSense
 */
export interface QuantumCircuit {
  id: string;
  name: string;
  qubits: Qubit[];
  gates: QuantumGate[];
  measurements: Measurement[];
  algorithmType: string;
}

/**
 * Qubit definition
 */
export interface Qubit {
  id: string;
  index: number;
  initialState: ComplexAmplitude[];  // [α, β] for |0⟩ and |1⟩
  currentState: ComplexAmplitude[];
}

/**
 * Complex amplitude
 */
export interface ComplexAmplitude {
  real: number;
  imaginary: number;
}

/**
 * Quantum gate
 */
export interface QuantumGate {
  id: string;
  type: GateType;
  targetQubits: number[];
  controlQubits?: number[];
  parameters?: number[];
  step: number;
}

/**
 * Gate types
 */
export enum GateType {
  HADAMARD = 'H',
  PAULI_X = 'X',
  PAULI_Y = 'Y',
  PAULI_Z = 'Z',
  CNOT = 'CNOT',
  TOFFOLI = 'TOFFOLI',
  ROTATION_X = 'RX',
  ROTATION_Y = 'RY',
  ROTATION_Z = 'RZ',
  PHASE = 'PHASE',
  SWAP = 'SWAP',
}

/**
 * Measurement
 */
export interface Measurement {
  id: string;
  qubitIndex: number;
  basis: 'computational' | 'hadamard';
  result?: 0 | 1;
  probability?: number;
}

/**
 * Convert quantum circuit to SYNAPSE entities
 */
export class QubitSenseBridge {
  /**
   * Convert entire circuit to entity graph
   */
  static convertCircuit(circuit: QuantumCircuit): {
    entities: Entity[];
    relationships: Relationship[];
  } {
    const entities: Entity[] = [];
    const relationships: Relationship[] = [];
    
    // Convert qubits to superposition entities
    circuit.qubits.forEach((qubit) => {
      const entity = this.convertQubit(qubit, circuit.qubits.length);
      entities.push(entity);
    });
    
    // Convert gates to transformation entities
    circuit.gates.forEach((gate) => {
      const entity = this.convertGate(gate, circuit.qubits.length);
      entities.push(entity);
      
      // Create relationships for gate connections
      const gateRels = this.createGateRelationships(gate, circuit.qubits);
      relationships.push(...gateRels);
    });
    
    // Convert measurements to collapse entities
    circuit.measurements.forEach((measurement) => {
      const entity = this.convertMeasurement(measurement);
      entities.push(entity);
    });
    
    // Create entanglement relationships
    const entanglements = this.detectEntanglement(circuit);
    relationships.push(...entanglements);
    
    return { entities, relationships };
  }
  
  /**
   * Convert qubit to superposition entity
   */
  private static convertQubit(qubit: Qubit, totalQubits: number): Entity {
    const PHI = 1.6180339887;
    
    // Position in Fibonacci sphere (sunflower seed pattern)
    const goldenAngle = Math.PI * 2 * (1 - 1 / PHI);
    const y = 1 - (qubit.index / (totalQubits - 1)) * 2;
    const radiusAtY = Math.sqrt(1 - y * y);
    const theta = qubit.index * goldenAngle;
    
    const position: Vector3D = {
      x: Math.cos(theta) * radiusAtY * 3,
      y: y * 3,
      z: Math.sin(theta) * radiusAtY * 3,
    };
    
    // Coherence from quantum state
    const coherence = this.calculateQubitCoherence(qubit);
    
    // Neural state (quantum → neural mapping)
    const neural: NeuralState = {
      x: this.amplitude(qubit.currentState[0]),  // |0⟩ amplitude
      y: this.amplitude(qubit.currentState[1]),  // |1⟩ amplitude
      z: this.purity(qubit.currentState),        // State purity
      mode: this.isSuperposed(qubit) ? 'bursting' : 'tonic',
      burstCount: this.isSuperposed(qubit) ? 1 : 0,
      lastBurst: Date.now(),
    };
    
    return {
      id: qubit.id,
      name: `Qubit ${qubit.index}`,
      type: EntityType.CONCEPT,
      scale: Scale.NODE,
      position,
      coherence,
      neural,
      metadata: {
        index: qubit.index,
        type: 'qubit',
        superposed: this.isSuperposed(qubit),
      },
    };
  }
  
  /**
   * Convert quantum gate to transformation entity
   */
  private static convertGate(gate: QuantumGate, totalQubits: number): Entity {
    // Position between affected qubits
    const avgIndex = gate.targetQubits.reduce((a, b) => a + b, 0) / gate.targetQubits.length;
    const PHI = 1.6180339887;
    const goldenAngle = Math.PI * 2 * (1 - 1 / PHI);
    
    const y = 1 - (avgIndex / (totalQubits - 1)) * 2;
    const radiusAtY = Math.sqrt(1 - y * y);
    const theta = avgIndex * goldenAngle;
    
    const position: Vector3D = {
      x: Math.cos(theta) * radiusAtY * 2,
      y: y * 2,
      z: Math.sin(theta) * radiusAtY * 2,
    };
    
    // Coherence based on gate type
    const coherence = this.calculateGateCoherence(gate);
    
    const neural: NeuralState = {
      x: coherence.potential,
      y: coherence.curl,
      z: coherence.dispersion,
      mode: 'bursting',
      burstCount: gate.targetQubits.length,
      lastBurst: Date.now(),
    };
    
    return {
      id: gate.id,
      name: `${gate.type} Gate`,
      type: EntityType.TASK,
      scale: Scale.NODE,
      position,
      coherence,
      neural,
      metadata: {
        type: gate.type,
        targets: gate.targetQubits,
        controls: gate.controlQubits,
        step: gate.step,
      },
    };
  }
  
  /**
   * Convert measurement to collapse entity
   */
  private static convertMeasurement(measurement: Measurement): Entity {
    const position: Vector3D = {
      x: measurement.qubitIndex * 0.5,
      y: 0,
      z: 0,
    };
    
    const coherence: CoherenceMetrics = {
      curl: 0,  // Measurement destroys curl
      potential: 0,  // Measurement destroys potential
      dispersion: measurement.probability || 1.0,  // Only dispersion remains
      timestamp: Date.now(),
    };
    
    const neural: NeuralState = {
      x: measurement.result !== undefined ? measurement.result : 0.5,
      y: 0,
      z: 0,
      mode: 'tonic',  // After measurement, state is tonic
      burstCount: 0,
      lastBurst: Date.now(),
    };
    
    return {
      id: measurement.id,
      name: `Measure Q${measurement.qubitIndex}`,
      type: EntityType.DECISION,
      scale: Scale.NODE,
      position,
      coherence,
      neural,
      metadata: {
        qubit: measurement.qubitIndex,
        basis: measurement.basis,
        result: measurement.result,
      },
    };
  }
  
  /**
   * Create relationships for gate connections
   */
  private static createGateRelationships(
    gate: QuantumGate,
    qubits: Qubit[]
  ): Relationship[] {
    const relationships: Relationship[] = [];
    
    // Gate acts on target qubits
    gate.targetQubits.forEach((targetIdx) => {
      const qubit = qubits.find(q => q.index === targetIdx);
      if (qubit) {
        relationships.push({
          id: `${gate.id}-${qubit.id}`,
          source: gate.id,
          target: qubit.id,
          type: RelationType.CALLS,
          strength: 1.0,
          coherenceContribution: this.gateCoherenceEffect(gate.type),
        });
      }
    });
    
    // Control qubits
    if (gate.controlQubits) {
      gate.controlQubits.forEach((controlIdx) => {
        const qubit = qubits.find(q => q.index === controlIdx);
        if (qubit) {
          relationships.push({
            id: `${gate.id}-ctrl-${qubit.id}`,
            source: qubit.id,
            target: gate.id,
            type: RelationType.ENTANGLED,
            strength: 1.0,
            coherenceContribution: 0.2,
          });
        }
      });
    }
    
    return relationships;
  }
  
  /**
   * Detect entanglement relationships between qubits
   */
  private static detectEntanglement(circuit: QuantumCircuit): Relationship[] {
    const relationships: Relationship[] = [];
    
    // Find gates that entangle qubits (CNOT, TOFFOLI, etc.)
    circuit.gates.forEach((gate) => {
      if (gate.controlQubits && gate.controlQubits.length > 0) {
        // Create entanglement between control and target
        gate.controlQubits.forEach((controlIdx) => {
          gate.targetQubits.forEach((targetIdx) => {
            const control = circuit.qubits.find(q => q.index === controlIdx);
            const target = circuit.qubits.find(q => q.index === targetIdx);
            
            if (control && target) {
              relationships.push({
                id: `entangle-${control.id}-${target.id}`,
                source: control.id,
                target: target.id,
                type: RelationType.ENTANGLED,
                strength: 0.8,
                coherenceContribution: -0.1,  // Entanglement increases curl
              });
            }
          });
        });
      }
    });
    
    return relationships;
  }
  
  /**
   * Helper: Calculate qubit coherence
   */
  private static calculateQubitCoherence(qubit: Qubit): CoherenceMetrics {
    const amp0 = this.amplitude(qubit.currentState[0]);
    const amp1 = this.amplitude(qubit.currentState[1]);
    
    // Curl from superposition (both states present)
    const curl = 2 * amp0 * amp1;
    
    // Potential from total probability
    const potential = amp0 * amp0 + amp1 * amp1;
    
    // Dispersion from purity
    const purity = this.purity(qubit.currentState);
    const dispersion = 1 - purity;
    
    return {
      curl,
      potential,
      dispersion,
      timestamp: Date.now(),
    };
  }
  
  /**
   * Helper: Calculate gate coherence effect
   */
  private static calculateGateCoherence(gate: QuantumGate): CoherenceMetrics {
    // Different gates have different coherence signatures
    const signatures: Record<string, CoherenceMetrics> = {
      [GateType.HADAMARD]: {
        curl: 0.5,  // Creates superposition
        potential: 1.0,
        dispersion: 0.0001,
        timestamp: Date.now(),
      },
      [GateType.CNOT]: {
        curl: 0.8,  // Creates entanglement
        potential: 0.9,
        dispersion: 0.0002,
        timestamp: Date.now(),
      },
      [GateType.PAULI_X]: {
        curl: 0.0,  // No superposition
        potential: 1.0,
        dispersion: 0.0,
        timestamp: Date.now(),
      },
    };
    
    return signatures[gate.type] || {
      curl: 0.3,
      potential: 0.8,
      dispersion: 0.0001,
      timestamp: Date.now(),
    };
  }
  
  /**
   * Helper: Gate coherence contribution
   */
  private static gateCoherenceEffect(gateType: GateType): number {
    const effects: Record<string, number> = {
      [GateType.HADAMARD]: 0.5,
      [GateType.CNOT]: -0.2,
      [GateType.PAULI_X]: 0.0,
      [GateType.PAULI_Y]: 0.0,
      [GateType.PAULI_Z]: 0.0,
    };
    
    return effects[gateType] || 0.1;
  }
  
  /**
   * Helper: Amplitude of complex number
   */
  private static amplitude(c: ComplexAmplitude): number {
    return Math.sqrt(c.real * c.real + c.imaginary * c.imaginary);
  }
  
  /**
   * Helper: Purity of quantum state
   */
  private static purity(state: ComplexAmplitude[]): number {
    const probs = state.map(c => this.amplitude(c) ** 2);
    return probs.reduce((sum, p) => sum + p * p, 0);
  }
  
  /**
   * Helper: Check if qubit is in superposition
   */
  private static isSuperposed(qubit: Qubit): boolean {
    const amp0 = this.amplitude(qubit.currentState[0]);
    const amp1 = this.amplitude(qubit.currentState[1]);
    
    // Superposed if both amplitudes are significant
    return amp0 > 0.1 && amp1 > 0.1;
  }
}

export default QubitSenseBridge;
