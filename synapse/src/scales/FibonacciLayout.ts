/**
 * SYNAPSE Scales: Fibonacci Layout
 * Layout algorithms for positioning entities in Fibonacci patterns
 */

import { fibonacciLayout, generateFibonacciSpiral, GOLDEN_ANGLE } from '../utils/fibonacci';
import { Scale, getFibonacciNumber } from '../types/scales';
import { Vector3D } from '../types/entities';

/**
 * Layout configuration
 */
export interface LayoutConfig {
  scale: Scale;
  baseRadius: number;
  verticalSpacing: number;
  clusterRadius: number;
}

/**
 * Layout result for an entity
 */
export interface LayoutPosition {
  entityId: string;
  position: Vector3D;
  scale: Scale;
  localIndex: number;
}

/**
 * Generate Fibonacci spiral layout for entities at a given scale
 */
export function layoutEntitiesOnSpiral(
  entityIds: string[],
  config: LayoutConfig
): LayoutPosition[] {
  const count = entityIds.length;
  const positions: LayoutPosition[] = [];
  
  for (let i = 0; i < count; i++) {
    const angle = i * GOLDEN_ANGLE;
    const radius = config.baseRadius * Math.sqrt(i + 1);
    const z = i * config.verticalSpacing;
    
    positions.push({
      entityId: entityIds[i],
      position: {
        x: radius * Math.cos(angle),
        y: radius * Math.sin(angle),
        z,
      },
      scale: config.scale,
      localIndex: i,
    });
  }
  
  return positions;
}

/**
 * Hierarchical layout: position clusters in outer spiral,
 * members within each cluster in inner spiral
 */
export function layoutHierarchical(
  clusters: Map<string, string[]>,  // clusterId -> member entityIds
  config: LayoutConfig
): Map<string, LayoutPosition> {
  const allPositions = new Map<string, LayoutPosition>();
  
  const clusterIds = Array.from(clusters.keys());
  const clusterPositions = layoutEntitiesOnSpiral(clusterIds, config);
  
  // Position each cluster
  clusterPositions.forEach((clusterPos, clusterIndex) => {
    const members = clusters.get(clusterPos.entityId) || [];
    
    // Layout members around cluster center
    const memberConfig: LayoutConfig = {
      ...config,
      baseRadius: config.clusterRadius,
    };
    
    const memberPositions = layoutEntitiesOnSpiral(members, memberConfig);
    
    // Offset by cluster position
    memberPositions.forEach(memberPos => {
      allPositions.set(memberPos.entityId, {
        ...memberPos,
        position: {
          x: clusterPos.position.x + memberPos.position.x,
          y: clusterPos.position.y + memberPos.position.y,
          z: clusterPos.position.z + memberPos.position.z,
        },
      });
    });
    
    // Add cluster center position
    allPositions.set(clusterPos.entityId, clusterPos);
  });
  
  return allPositions;
}

/**
 * Force-directed layout with Fibonacci initial positions
 * Combines golden ratio aesthetics with force-based optimization
 */
export interface ForceConfig {
  repulsion: number;
  attraction: number;
  iterations: number;
  damping: number;
}

export function layoutForceDirected(
  entityIds: string[],
  edges: Array<{ source: string; target: string; strength: number }>,
  initialConfig: LayoutConfig,
  forceConfig: ForceConfig
): Map<string, LayoutPosition> {
  // Start with Fibonacci positions
  const initialPositions = layoutEntitiesOnSpiral(entityIds, initialConfig);
  const positions = new Map<string, LayoutPosition>();
  const velocities = new Map<string, Vector3D>();
  
  initialPositions.forEach(pos => {
    positions.set(pos.entityId, pos);
    velocities.set(pos.entityId, { x: 0, y: 0, z: 0 });
  });
  
  // Iterate force simulation
  for (let iter = 0; iter < forceConfig.iterations; iter++) {
    const forces = new Map<string, Vector3D>();
    
    // Initialize forces
    entityIds.forEach(id => {
      forces.set(id, { x: 0, y: 0, z: 0 });
    });
    
    // Repulsion between all pairs
    entityIds.forEach(id1 => {
      entityIds.forEach(id2 => {
        if (id1 === id2) return;
        
        const pos1 = positions.get(id1)!.position;
        const pos2 = positions.get(id2)!.position;
        
        const dx = pos1.x - pos2.x;
        const dy = pos1.y - pos2.y;
        const dz = pos1.z - pos2.z;
        const dist2 = dx * dx + dy * dy + dz * dz + 0.01; // Avoid division by zero
        const dist = Math.sqrt(dist2);
        
        const force = forceConfig.repulsion / dist2;
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        const fz = (dz / dist) * force;
        
        const f1 = forces.get(id1)!;
        f1.x += fx;
        f1.y += fy;
        f1.z += fz;
      });
    });
    
    // Attraction along edges
    edges.forEach(edge => {
      const pos1 = positions.get(edge.source)?.position;
      const pos2 = positions.get(edge.target)?.position;
      
      if (!pos1 || !pos2) return;
      
      const dx = pos2.x - pos1.x;
      const dy = pos2.y - pos1.y;
      const dz = pos2.z - pos1.z;
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      
      const force = forceConfig.attraction * edge.strength * dist;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      const fz = (dz / dist) * force;
      
      const f1 = forces.get(edge.source)!;
      const f2 = forces.get(edge.target)!;
      
      f1.x += fx;
      f1.y += fy;
      f1.z += fz;
      
      f2.x -= fx;
      f2.y -= fy;
      f2.z -= fz;
    });
    
    // Update velocities and positions
    entityIds.forEach(id => {
      const force = forces.get(id)!;
      const velocity = velocities.get(id)!;
      const pos = positions.get(id)!;
      
      // Update velocity with damping
      velocity.x = (velocity.x + force.x) * forceConfig.damping;
      velocity.y = (velocity.y + force.y) * forceConfig.damping;
      velocity.z = (velocity.z + force.z) * forceConfig.damping;
      
      // Update position
      pos.position.x += velocity.x;
      pos.position.y += velocity.y;
      pos.position.z += velocity.z;
    });
  }
  
  return positions;
}

/**
 * Scale-aware layout: adjust parameters based on Fibonacci scale
 */
export function getScaleAwareConfig(scale: Scale): LayoutConfig {
  const fibNumber = getFibonacciNumber(scale);
  
  return {
    scale,
    baseRadius: Math.log(fibNumber + 1) * 2,
    verticalSpacing: 0.1 * Math.log(fibNumber + 1),
    clusterRadius: 0.5 * Math.log(fibNumber + 1),
  };
}

/**
 * Circular packing layout
 * Pack circles (entities) without overlap using Fibonacci spacing
 */
export function layoutCircularPacking(
  entityIds: string[],
  radii: Map<string, number>,
  containerRadius: number
): Map<string, Vector3D> {
  const positions = new Map<string, Vector3D>();
  
  entityIds.forEach((id, i) => {
    const angle = i * GOLDEN_ANGLE;
    const radius = radii.get(id) || 0.5;
    
    // Start from Fibonacci spiral position
    const r = containerRadius * Math.sqrt(i / entityIds.length);
    
    positions.set(id, {
      x: r * Math.cos(angle),
      y: r * Math.sin(angle),
      z: 0,
    });
  });
  
  // Simple collision resolution
  const iterations = 50;
  for (let iter = 0; iter < iterations; iter++) {
    let moved = false;
    
    entityIds.forEach((id1, i) => {
      entityIds.slice(i + 1).forEach(id2 => {
        const pos1 = positions.get(id1)!;
        const pos2 = positions.get(id2)!;
        const r1 = radii.get(id1) || 0.5;
        const r2 = radii.get(id2) || 0.5;
        
        const dx = pos2.x - pos1.x;
        const dy = pos2.y - pos1.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const minDist = r1 + r2;
        
        if (dist < minDist && dist > 0) {
          const overlap = minDist - dist;
          const moveX = (dx / dist) * overlap * 0.5;
          const moveY = (dy / dist) * overlap * 0.5;
          
          pos1.x -= moveX;
          pos1.y -= moveY;
          pos2.x += moveX;
          pos2.y += moveY;
          
          moved = true;
        }
      });
    });
    
    if (!moved) break;
  }
  
  return positions;
}
