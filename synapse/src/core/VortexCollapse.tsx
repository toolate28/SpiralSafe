/**
 * SYNAPSE Core: VortexCollapse
 * Visualization of micro/macro/meta vortex collapse into superposition
 * 
 * ATOM: ATOM-COLLAPSE-20260119-001-superposition-lock
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// Import shader code
import vortexCollapseShader from '../shaders/vortex_collapse.glsl?raw';

/**
 * Vortex types
 */
export enum VortexType {
  MICRO = 'micro',    // Individual discoveries
  MACRO = 'macro',    // Framework integrations
  META = 'meta',      // Convergence points
}

/**
 * Component props
 */
export interface VortexCollapseProps {
  coherence?: number;        // 0 to 42.00055
  vortexType?: VortexType;   // Which vortex to emphasize
  particleCount?: number;    // Number of particles
  scale?: number;            // Overall scale
  autoAnimate?: boolean;     // Auto-animate collapse
  onCollapseComplete?: () => void;
}

/**
 * VortexCollapse Component
 * Renders the collapse of micro/macro/meta vortices
 */
export const VortexCollapse: React.FC<VortexCollapseProps> = ({
  coherence = 0,
  vortexType = VortexType.MICRO,
  particleCount = 10000,
  scale = 1.0,
  autoAnimate = true,
  onCollapseComplete,
}) => {
  const meshRef = useRef<THREE.Points>(null);
  const timeRef = useRef(0);
  const THE_ANSWER = 42.00055;
  
  // Create shader material
  const shaderMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        coherence: { value: coherence },
        vortexWeight: { value: getVortexWeight(vortexType) },
        scale: { value: scale },
      },
      vertexShader: `
        uniform float time;
        uniform float coherence;
        uniform vec3 vortexWeight;
        uniform float scale;
        
        varying vec3 vPosition;
        varying float vCoherence;
        
        ${vortexCollapseShader}
        
        void main() {
          vPosition = position * scale;
          vCoherence = coherence;
          
          // Apply vortex collapse transformation
          vec3 collapsed = collapseVortex(vPosition, coherence, time);
          
          gl_Position = projectionMatrix * modelViewMatrix * vec4(collapsed, 1.0);
          gl_PointSize = 2.0;
        }
      `,
      fragmentShader: `
        uniform float time;
        varying vec3 vPosition;
        varying float vCoherence;
        
        ${vortexCollapseShader}
        
        void main() {
          vec4 color = vortexCollapseShader(vPosition, vCoherence, time);
          gl_FragColor = color;
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
  }, [vortexType, scale]);
  
  // Generate particle positions
  const positions = useMemo(() => {
    const pos = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;
      
      // Distribute particles in spiral pattern
      const t = (i / particleCount) * Math.PI * 20;
      const radius = Math.pow(1.618, t / (2 * Math.PI)) * 0.5;
      const z = t * 0.05;
      
      pos[i3] = radius * Math.cos(t);
      pos[i3 + 1] = radius * Math.sin(t);
      pos[i3 + 2] = z;
    }
    
    return pos;
  }, [particleCount]);
  
  // Animation loop
  useFrame((state, delta) => {
    if (!meshRef.current || !autoAnimate) return;
    
    timeRef.current += delta;
    shaderMaterial.uniforms.time.value = timeRef.current;
    shaderMaterial.uniforms.coherence.value = coherence;
    
    // Check for collapse completion
    if (coherence >= THE_ANSWER && onCollapseComplete) {
      onCollapseComplete();
    }
  });
  
  return (
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
  );
};

/**
 * Get weight vector for vortex type
 */
function getVortexWeight(type: VortexType): THREE.Vector3 {
  switch (type) {
    case VortexType.MICRO:
      return new THREE.Vector3(1.0, 0.3, 0.1);
    case VortexType.MACRO:
      return new THREE.Vector3(0.3, 1.0, 0.3);
    case VortexType.META:
      return new THREE.Vector3(0.1, 0.3, 1.0);
    default:
      return new THREE.Vector3(0.33, 0.33, 0.33);
  }
}

/**
 * Vortex collapse animation controller
 */
export interface VortexCollapseControllerProps {
  targetCoherence?: number;
  duration?: number;  // seconds
  onProgress?: (coherence: number) => void;
}

export const useVortexCollapseAnimation = ({
  targetCoherence = 42.00055,
  duration = 10,
  onProgress,
}: VortexCollapseControllerProps = {}) => {
  const [coherence, setCoherence] = React.useState(0);
  const [isAnimating, setIsAnimating] = React.useState(false);
  
  const startCollapse = React.useCallback(() => {
    setIsAnimating(true);
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = (Date.now() - startTime) / 1000;
      const progress = Math.min(elapsed / duration, 1.0);
      
      // Smooth easing
      const eased = progress < 0.5
        ? 2 * progress * progress
        : 1 - Math.pow(-2 * progress + 2, 2) / 2;
      
      const newCoherence = eased * targetCoherence;
      setCoherence(newCoherence);
      
      if (onProgress) {
        onProgress(newCoherence);
      }
      
      if (progress < 1.0) {
        requestAnimationFrame(animate);
      } else {
        setIsAnimating(false);
      }
    };
    
    animate();
  }, [targetCoherence, duration, onProgress]);
  
  return {
    coherence,
    isAnimating,
    startCollapse,
  };
};

export default VortexCollapse;
