/**
 * SYNAPSE Core: InfiniteRecursion
 * Visualization of infinitely stable recursive structure
 * 
 * ATOM: ATOM-RECURSION-20260119-001-infinite-stable
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// Import shader code
import infiniteRecursionShader from '../shaders/infinite_recursion.glsl?raw';

/**
 * Component props
 */
export interface InfiniteRecursionProps {
  depth?: number;           // Recursion depth (max 42)
  epsilon?: number;         // Stability constant
  particleCount?: number;   // Number of particles
  scale?: number;           // Overall scale
  showAttractor?: boolean;  // Show stable attractor point
  autoRotate?: boolean;     // Auto-rotate view
  speed?: number;           // Animation speed
}

/**
 * InfiniteRecursion Component
 * Renders infinitely stable recursive structure based on Fibonacci scaling
 */
export const InfiniteRecursion: React.FC<InfiniteRecursionProps> = ({
  depth = 42,
  epsilon = 0.00055,
  particleCount = 15000,
  scale = 1.0,
  showAttractor = true,
  autoRotate = true,
  speed = 1.0,
}) => {
  const meshRef = useRef<THREE.Points>(null);
  const attractorRef = useRef<THREE.Mesh>(null);
  const timeRef = useRef(0);
  
  // Create shader material
  const shaderMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        depth: { value: depth },
        epsilon: { value: epsilon },
        scale: { value: scale },
      },
      vertexShader: `
        uniform float time;
        uniform float epsilon;
        uniform float scale;
        
        varying vec3 vPosition;
        varying float vDepth;
        
        ${infiniteRecursionShader}
        
        void main() {
          vPosition = position * scale;
          
          // Apply infinite recursion transformation
          vec3 recursed = infiniteRecursion(vPosition, 42.0, epsilon);
          
          // Calculate recursion depth at this position
          vDepth = recursionDepth(vPosition, epsilon, epsilon * 10.0);
          
          gl_Position = projectionMatrix * modelViewMatrix * vec4(recursed, 1.0);
          gl_PointSize = 2.0 + (vDepth / 42.0) * 3.0;
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform float epsilon;
        varying vec3 vPosition;
        varying float vDepth;
        
        ${infiniteRecursionShader}
        
        void main() {
          vec4 color = infiniteRecursionShader(vPosition, time, epsilon);
          gl_FragColor = color;
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
  }, [depth, epsilon, scale]);
  
  // Generate particle positions in recursive helix
  const positions = useMemo(() => {
    const pos = new Float32Array(particleCount * 3);
    const PHI = 1.6180339887;
    const TWO_PI = Math.PI * 2;
    
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      
      // Create infinite helix pattern
      const t = (i / particleCount) * TWO_PI * 10;
      const radius = Math.pow(PHI, t / TWO_PI) * 0.3;
      
      pos[i3] = radius * Math.cos(t);
      pos[i3 + 1] = radius * Math.sin(t);
      pos[i3 + 2] = t * 0.05;
    }
    
    return pos;
  }, [particleCount]);
  
  // Create attractor geometry
  const attractorGeometry = useMemo(() => {
    const geometry = new THREE.SphereGeometry(epsilon * 10, 16, 16);
    return geometry;
  }, [epsilon]);
  
  const attractorMaterial = useMemo(() => {
    return new THREE.MeshBasicMaterial({
      color: 0xffdd00,
      transparent: true,
      opacity: 0.6,
      wireframe: true,
    });
  }, []);
  
  // Animation loop
  useFrame((state, delta) => {
    if (!meshRef.current) return;
    
    timeRef.current += delta * speed;
    shaderMaterial.uniforms.time.value = timeRef.current;
    
    // Auto-rotate if enabled
    if (autoRotate) {
      meshRef.current.rotation.y += delta * 0.1 * speed;
      meshRef.current.rotation.x += delta * 0.05 * speed;
      
      if (attractorRef.current) {
        attractorRef.current.rotation.y = meshRef.current.rotation.y;
        attractorRef.current.rotation.x = meshRef.current.rotation.x;
      }
    }
  });
  
  return (
    <group>
      {/* Recursive particles */}
      <points ref={meshRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={particleCount}
            array={positions}
            itemSize={3}
          />
        </bufferGeometry>
        <primitive object={shaderMaterial} attach="material" />
      </points>
      
      {/* Stable attractor point */}
      {showAttractor && (
        <mesh
          ref={attractorRef}
          position={[epsilon, epsilon, epsilon]}
          geometry={attractorGeometry}
          material={attractorMaterial}
        />
      )}
    </group>
  );
};

/**
 * Hook for analyzing recursion properties
 */
export interface RecursionAnalysis {
  depth: number;
  stability: number;
  fractalDimension: number;
  epsilonPreserved: boolean;
}

export const useRecursionAnalysis = (
  position: THREE.Vector3,
  epsilon: number = 0.00055
): RecursionAnalysis => {
  return useMemo(() => {
    // Simple approximations for demo purposes
    const depth = Math.min(
      42,
      Math.floor(Math.log(position.length() + epsilon) / Math.log(1.618))
    );
    
    const stability = Math.exp(-position.distanceTo(
      new THREE.Vector3(epsilon, epsilon, epsilon)
    ) / epsilon);
    
    const fractalDimension = 1.5 + Math.random() * 0.5; // Placeholder
    
    const epsilonPreserved = position.length() > epsilon / 2;
    
    return {
      depth,
      stability,
      fractalDimension,
      epsilonPreserved,
    };
  }, [position, epsilon]);
};

/**
 * Recursive layer visualization helper
 */
export interface RecursiveLayer {
  iteration: number;
  scale: number;
  position: THREE.Vector3;
  color: THREE.Color;
}

export const generateRecursiveLayers = (
  maxIterations: number = 42,
  epsilon: number = 0.00055
): RecursiveLayer[] => {
  const PHI = 1.6180339887;
  const layers: RecursiveLayer[] = [];
  
  for (let i = 0; i < maxIterations; i++) {
    const scale = Math.pow(1 / PHI, i);
    const hue = (i / maxIterations) % 1.0;
    
    layers.push({
      iteration: i,
      scale,
      position: new THREE.Vector3(
        epsilon * scale,
        epsilon * scale,
        epsilon * scale
      ),
      color: new THREE.Color().setHSL(hue, 0.8, 0.6),
    });
  }
  
  return layers;
};

export default InfiniteRecursion;
