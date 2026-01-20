/**
 * SYNAPSE Utilities: Fibonacci
 * Golden ratio calculations and spiral generation
 */

/** Golden ratio φ = (1 + √5) / 2 */
export const PHI = (1 + Math.sqrt(5)) / 2;

/** Golden ratio conjugate φ̂ = (1 - √5) / 2 */
export const PHI_CONJUGATE = (1 - Math.sqrt(5)) / 2;

/**
 * Calculate nth Fibonacci number using Binet's formula
 * F(n) = (φⁿ - φ̂ⁿ) / √5
 */
export function fibonacci(n: number): number {
  if (n < 0) return 0;
  if (n === 0) return 0;
  if (n === 1) return 1;
  
  const sqrt5 = Math.sqrt(5);
  return Math.round((Math.pow(PHI, n) - Math.pow(PHI_CONJUGATE, n)) / sqrt5);
}

/**
 * Generate Fibonacci sequence up to n terms
 */
export function fibonacciSequence(n: number): number[] {
  if (n <= 0) return [];
  if (n === 1) return [0];
  
  const sequence = [0, 1];
  for (let i = 2; i < n; i++) {
    sequence.push(sequence[i - 1] + sequence[i - 2]);
  }
  
  return sequence;
}

/**
 * 3D Fibonacci spiral point
 * Parametric equation with golden ratio expansion
 */
export interface SpiralPoint {
  x: number;
  y: number;
  z: number;
  angle: number;
  radius: number;
}

/**
 * Calculate point on Fibonacci spiral
 * @param t - Parameter [0, ∞)
 * @param scale - Base scale factor
 * @param verticalLift - Z-axis lift per revolution
 */
export function fibonacciSpiralPoint(
  t: number,
  scale: number = 1,
  verticalLift: number = 0.1
): SpiralPoint {
  // Golden ratio spiral: r = φ^(t/(2π)) * scale
  const radius = Math.pow(PHI, t / (2 * Math.PI)) * scale;
  const angle = t;
  const z = t * verticalLift;
  
  return {
    x: radius * Math.cos(angle),
    y: radius * Math.sin(angle),
    z,
    angle,
    radius,
  };
}

/**
 * Generate array of spiral points
 */
export function generateFibonacciSpiral(
  count: number,
  scale: number = 1,
  revolutions: number = 3
): SpiralPoint[] {
  const points: SpiralPoint[] = [];
  const maxT = revolutions * 2 * Math.PI;
  const step = maxT / count;
  
  for (let i = 0; i < count; i++) {
    const t = i * step;
    points.push(fibonacciSpiralPoint(t, scale));
  }
  
  return points;
}

/**
 * Calculate golden angle (≈137.5°)
 * Used for optimal packing in sunflowers, etc.
 */
export const GOLDEN_ANGLE = 2 * Math.PI * (1 - 1 / PHI);

/**
 * Fibonacci sphere point (sunflower seed pattern)
 * Distributes points uniformly on sphere using golden angle
 */
export function fibonacciSpherePoint(
  index: number,
  totalPoints: number,
  radius: number = 1
): { x: number; y: number; z: number } {
  const y = 1 - (index / (totalPoints - 1)) * 2;
  const radiusAtY = Math.sqrt(1 - y * y);
  const theta = index * GOLDEN_ANGLE;
  
  return {
    x: Math.cos(theta) * radiusAtY * radius,
    y: y * radius,
    z: Math.sin(theta) * radiusAtY * radius,
  };
}

/**
 * Generate Fibonacci sphere points
 */
export function generateFibonacciSphere(
  count: number,
  radius: number = 1
): Array<{ x: number; y: number; z: number }> {
  const points = [];
  for (let i = 0; i < count; i++) {
    points.push(fibonacciSpherePoint(i, count, radius));
  }
  return points;
}

/**
 * Find nearest Fibonacci number to target
 */
export function nearestFibonacci(target: number): number {
  if (target <= 0) return 0;
  if (target === 1) return 1;
  
  let a = 0;
  let b = 1;
  
  while (b < target) {
    const next = a + b;
    a = b;
    b = next;
  }
  
  // Return closest
  const diffB = Math.abs(b - target);
  const diffA = Math.abs(a - target);
  
  return diffB < diffA ? b : a;
}

/**
 * Check if number is Fibonacci
 */
export function isFibonacci(n: number): boolean {
  if (n < 0) return false;
  
  // A number is Fibonacci iff one of (5n²+4) or (5n²-4) is a perfect square
  const check1 = 5 * n * n + 4;
  const check2 = 5 * n * n - 4;
  
  const isPerfectSquare = (x: number) => {
    const sqrt = Math.sqrt(x);
    return sqrt === Math.floor(sqrt);
  };
  
  return isPerfectSquare(check1) || isPerfectSquare(check2);
}

/**
 * Golden ratio spiral layout positions
 * Arranges N entities in Fibonacci spiral pattern
 */
export function fibonacciLayout(
  entityCount: number,
  baseRadius: number = 1
): Array<{ x: number; y: number; z: number; index: number }> {
  const positions = [];
  
  for (let i = 0; i < entityCount; i++) {
    const t = i * GOLDEN_ANGLE;
    const radius = baseRadius * Math.sqrt(i + 1);  // Archimedean-like growth
    
    positions.push({
      x: radius * Math.cos(t),
      y: radius * Math.sin(t),
      z: 0,  // Can add z-variation for 3D
      index: i,
    });
  }
  
  return positions;
}
