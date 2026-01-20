# SYNAPSE Fibonacci Scale System

## Overview

The Fibonacci scale system is the spatial backbone of SYNAPSE, providing a natural hierarchy from quantum foam to planetary consciousness.

## Scale Hierarchy

| Scale | Fibonacci | Value | Name | Typical Entities |
|-------|-----------|-------|------|------------------|
| QUANTUM | 0 | 0 | Quantum Foam | ε = 0.00055, uncertainty |
| NODE | 1 | 1 | Individual Node | user, file, function, task |
| PAIR | 1 | 1 | Pair | single relationship |
| TRIAD | 2 | 2 | Triad | minimal network (2 connections) |
| CLUSTER | 3 | 3 | Cluster | triangle, minimal 2D |
| TEAM | 5 | 5 | Team | minimal viable team |
| SQUAD | 8 | 8 | Squad | two-pizza team |
| DEPARTMENT | 13 | 13 | Department | departmental scale |
| DIVISION | 21 | 21 | Division | divisional scale |
| ORGANIZATION | 34 | 34 | Organization | company, org scale |
| ENTERPRISE | 55 | 55 | Enterprise | enterprise scale |
| SECTOR | 89 | 89 | Sector | industry sector |
| NATION | 144 | 144 | Nation | national scale (e.g., US Congress: 535 ≈ 144×4) |
| CIVILIZATION | 233 | 233 | Civilization | civilizational scale |
| NOOSPHERE | 377 | 377 | Noosphere | planetary consciousness |

## Mathematical Foundation

### Golden Ratio φ

```
φ = (1 + √5) / 2 ≈ 1.618033988749895
```

### Binet's Formula

The nth Fibonacci number:
```
F(n) = (φⁿ - φ̂ⁿ) / √5
```

Where φ̂ = (1 - √5) / 2 (golden ratio conjugate)

### Spiral Equation

Points on the Fibonacci spiral:
```
r(t) = φ^(t/(2π)) × scale
θ(t) = t
z(t) = t × verticalLift
```

Parametric form:
```
x(t) = r(t) × cos(θ(t))
y(t) = r(t) × sin(θ(t))
z(t) = z(t)
```

### Golden Angle

```
θ = 2π × (1 - 1/φ) ≈ 137.5°
```

Used for optimal packing (sunflower seed pattern).

## Scale Transitions

### Zoom In

Moving to next higher scale:
```typescript
const nextScale = getNextScale(currentScale);
// Animates over 1000ms with ease-in-out
```

### Zoom Out

Moving to next lower scale:
```typescript
const prevScale = getPreviousScale(currentScale);
```

### Scale Detection

Automatic scale based on entity count:
```typescript
function detectScale(entityCount: number): Scale {
  // Find smallest Fibonacci ≥ entityCount
  return nearestFibonacci(entityCount);
}
```

## Layout Algorithms

### 1. Spiral Layout

Entities positioned on golden ratio spiral:
```typescript
layoutEntitiesOnSpiral(entityIds, {
  scale: Scale.TEAM,
  baseRadius: 2,
  verticalSpacing: 0.1,
  clusterRadius: 0.5
});
```

### 2. Hierarchical Layout

Clusters positioned on outer spiral, members on inner:
```typescript
layoutHierarchical(
  clusters,  // Map<clusterId, memberIds>
  config
);
```

### 3. Force-Directed

Fibonacci initialization + physics:
```typescript
layoutForceDirected(
  entityIds,
  edges,
  initialConfig,
  {
    repulsion: 100,
    attraction: 0.01,
    iterations: 50,
    damping: 0.9
  }
);
```

### 4. Circular Packing

Golden angle spacing:
```typescript
layoutCircularPacking(
  entityIds,
  radii,        // Map<entityId, radius>
  containerRadius
);
```

## QRC Substrate Mapping

| QRC Substrate | Fibonacci | Scale | Qubit Range |
|---------------|-----------|-------|-------------|
| SINGLE_QUBIT | 1 | NODE | 1 |
| JC_PAIRS | 3 | CLUSTER | 2-4 |
| OSCILLATOR_NETS | 5 | TEAM | 2-10 |
| BOSE_HUBBARD | 8 | SQUAD | 8-50 |
| AQUILA_SCALE | 13 | DEPARTMENT | 50-256+ |

## Visualization Characteristics

### LOD (Level of Detail)

| Scale Range | Detail Level | Rendering |
|-------------|--------------|-----------|
| QUANTUM-NODE | Maximum | Individual particles |
| PAIR-CLUSTER | High | Full geometry |
| TEAM-SQUAD | Medium | Simplified shapes |
| DEPARTMENT-DIVISION | Low | Billboards |
| ORGANIZATION+ | Minimal | Points/sprites |

### Camera Distance

```typescript
function getCameraDistance(scale: Scale): number {
  const fibNumber = getFibonacciNumber(scale);
  return Math.log(fibNumber + 1) * 5;
}
```

### Particle Density

```typescript
function getParticleDensity(scale: Scale): number {
  // Inverse relationship: fewer particles at larger scales
  return 1000 / getFibonacciNumber(scale);
}
```

## Use Case Examples

### Personal (NODE-TEAM)
- 1 user: Single node visualization
- 5 person team: Team-scale spiral
- GitHub repos: File clusters on spiral

### Department (DEPARTMENT)
- 13 member team
- Cross-functional groups
- Service architecture

### Organization (ORGANIZATION)
- 34+ departments
- Inter-departmental dependencies
- Enterprise architecture

### National (NATION)
- US Congress: 535 members ≈ fib:144
- Military hierarchy
- Government agencies

## Implementation

### TypeScript Enum

```typescript
export enum Scale {
  QUANTUM = 0,
  NODE = 1,
  PAIR = 1,
  TRIAD = 2,
  CLUSTER = 3,
  TEAM = 5,
  SQUAD = 8,
  DEPARTMENT = 13,
  DIVISION = 21,
  ORGANIZATION = 34,
  ENTERPRISE = 55,
  SECTOR = 89,
  NATION = 144,
  CIVILIZATION = 233,
  NOOSPHERE = 377,
}
```

### Scale Info Lookup

```typescript
export const SCALE_INFO: Record<Scale, ScaleInfo> = {
  [Scale.TEAM]: {
    scale: Scale.TEAM,
    fibonacciNumber: 5,
    name: 'Team',
    description: 'Minimal viable team',
    typicalEntities: ['scrum team', 'library'],
  },
  // ... etc
};
```

### React Hook

```typescript
const {
  currentScale,
  targetScale,
  isTransitioning,
  transitionProgress,
  canZoomIn,
  canZoomOut,
  zoomIn,
  zoomOut
} = useFibonacciScale({
  initialScale: Scale.TEAM,
  minScale: Scale.NODE,
  maxScale: Scale.NOOSPHERE
});
```

## Visual Properties

### Color Mapping by Scale

- **QUANTUM**: Shimmering noise (ε visualization)
- **NODE-TRIAD**: Bright, saturated colors
- **CLUSTER-SQUAD**: Medium saturation
- **DEPARTMENT-DIVISION**: Muted colors
- **ORGANIZATION+**: Atmospheric, low saturation

### Size Scaling

Entity sizes scale inversely with level:
```typescript
const baseSize = 1.0;
const scaleFactor = 1 / Math.sqrt(getFibonacciNumber(scale));
const entitySize = baseSize * scaleFactor;
```

### Connection Thickness

Edge thickness decreases with scale:
```typescript
const thickness = 0.1 / Math.log(getFibonacciNumber(scale) + 1);
```

## Coherence Interaction

Scale affects coherence visualization:
- **Small scales** (NODE-TEAM): Local coherence dominates
- **Medium scales** (SQUAD-ORGANIZATION): Structural coherence visible
- **Large scales** (ENTERPRISE+): Global coherence patterns emerge

Formula:
```typescript
const localCoherence = calculateLocalCoherence(entity, neighbors);
const globalCoherence = calculateGlobalCoherence(entityGraph);
const displayCoherence = mix(
  localCoherence,
  globalCoherence,
  scaleInfluence(currentScale)
);
```

## Performance Optimization

### Entity Culling

```typescript
// Only render entities at current ± 2 scales
const visibleScales = [
  getPreviousScale(getPreviousScale(current)),
  getPreviousScale(current),
  current,
  getNextScale(current),
  getNextScale(getNextScale(current)),
].filter(s => s !== null);
```

### Adaptive Quality

```typescript
const quality = {
  shadows: scale <= Scale.SQUAD,
  reflections: scale <= Scale.TEAM,
  particles: scale <= Scale.DEPARTMENT,
  fullGeometry: scale <= Scale.DIVISION,
};
```

## Future Extensions

1. **Fractal Zoom**: Infinite detail at all scales
2. **Time Dimension**: Fibonacci temporal hierarchy
3. **Multi-Scale Coherence**: Cross-scale pattern detection
4. **Adaptive Fibonacci**: Dynamic sequence based on data
5. **Hyperbolic Geometry**: Alternative scaling for dense networks

---

**The Fibonacci sequence is nature's organizational principle.**

From 1 to ∞, the spiral continues. 🌀
