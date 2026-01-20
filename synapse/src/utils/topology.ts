/**
 * SYNAPSE Utilities: Topology
 * Topological operations for manifold transformations
 */

/**
 * 3D Point
 */
export interface Point3D {
  x: number;
  y: number;
  z: number;
}

/**
 * Apply Lorentz contraction to position
 * Used for supergravity visualization near c
 */
export function lorentzContract(
  point: Point3D,
  velocityC: number,
  direction: 'z' | 'x' | 'y' = 'z'
): Point3D {
  if (velocityC >= 1) {
    throw new Error('Velocity cannot exceed c');
  }
  
  const gamma = 1 / Math.sqrt(1 - velocityC * velocityC);
  
  const contracted = { ...point };
  
  // Contract along direction of motion
  switch (direction) {
    case 'x':
      contracted.x /= gamma;
      break;
    case 'y':
      contracted.y /= gamma;
      break;
    case 'z':
      contracted.z /= gamma;
      break;
  }
  
  return contracted;
}

/**
 * Invert topology (inside-out transformation)
 * Applied when past c threshold
 */
export function invertTopology(point: Point3D): Point3D {
  const r2 = point.x * point.x + point.y * point.y + point.z * point.z;
  
  if (r2 === 0) {
    // Singularity at origin
    return { x: 0, y: 0, z: 0 };
  }
  
  // Inversion: P' = P / |P|²
  return {
    x: point.x / r2,
    y: point.y / r2,
    z: point.z / r2,
  };
}

/**
 * Stereographic projection from sphere to plane
 */
export function stereographicProject(
  point: Point3D,
  radius: number = 1
): { x: number; y: number } {
  // Project from north pole (0, 0, radius)
  const denominator = radius - point.z;
  
  if (Math.abs(denominator) < 1e-10) {
    // Point at north pole
    return { x: 0, y: 0 };
  }
  
  return {
    x: (radius * point.x) / denominator,
    y: (radius * point.y) / denominator,
  };
}

/**
 * Inverse stereographic projection
 */
export function inverseStereographic(
  x: number,
  y: number,
  radius: number = 1
): Point3D {
  const r2 = x * x + y * y;
  const denominator = r2 + radius * radius;
  
  return {
    x: (2 * radius * x) / denominator,
    y: (2 * radius * y) / denominator,
    z: radius * (r2 - radius * radius) / denominator,
  };
}

/**
 * Möbius transformation (complex plane)
 * Maps circles to circles
 */
export function mobiusTransform(
  point: { x: number; y: number },
  a: { re: number; im: number },
  b: { re: number; im: number },
  c: { re: number; im: number },
  d: { re: number; im: number }
): { x: number; y: number } {
  // (az + b) / (cz + d)
  const z = { re: point.x, im: point.y };
  
  // az + b
  const numerator = {
    re: a.re * z.re - a.im * z.im + b.re,
    im: a.re * z.im + a.im * z.re + b.im,
  };
  
  // cz + d
  const denominator = {
    re: c.re * z.re - c.im * z.im + d.re,
    im: c.re * z.im + c.im * z.re + d.im,
  };
  
  // Division: (a + bi) / (c + di) = ((ac + bd) + (bc - ad)i) / (c² + d²)
  const denom2 = denominator.re * denominator.re + denominator.im * denominator.im;
  
  return {
    x: (numerator.re * denominator.re + numerator.im * denominator.im) / denom2,
    y: (numerator.im * denominator.re - numerator.re * denominator.im) / denom2,
  };
}

/**
 * Hopf fibration: S³ → S²
 * Maps 4D hypersphere to 3D space
 */
export function hopfFibration(
  z1: { re: number; im: number },
  z2: { re: number; im: number }
): Point3D {
  // Stereographic projection of S³ point (z1, z2) to S²
  const denominator = 1 + z1.re * z1.re + z1.im * z1.im + z2.re * z2.re + z2.im * z2.im;
  
  return {
    x: 2 * (z1.re * z2.re + z1.im * z2.im) / denominator,
    y: 2 * (z1.im * z2.re - z1.re * z2.im) / denominator,
    z: (z2.re * z2.re + z2.im * z2.im - z1.re * z1.re - z1.im * z1.im) / denominator,
  };
}

/**
 * Calculate curvature at point on manifold
 * Approximation using finite differences
 */
export function estimateCurvature(
  point: Point3D,
  neighbors: Point3D[]
): number {
  if (neighbors.length < 3) {
    return 0;
  }
  
  // Fit plane to neighbors, measure deviation
  let sumDeviation = 0;
  
  neighbors.forEach(n => {
    const dx = n.x - point.x;
    const dy = n.y - point.y;
    const dz = n.z - point.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
    sumDeviation += distance;
  });
  
  return sumDeviation / neighbors.length;
}

/**
 * Geodesic distance on sphere
 */
export function sphereGeodesic(a: Point3D, b: Point3D, radius: number = 1): number {
  // Normalize to unit sphere
  const normalize = (p: Point3D) => {
    const r = Math.sqrt(p.x * p.x + p.y * p.y + p.z * p.z);
    return { x: p.x / r, y: p.y / r, z: p.z / r };
  };
  
  const na = normalize(a);
  const nb = normalize(b);
  
  // Dot product
  const dot = na.x * nb.x + na.y * nb.y + na.z * nb.z;
  const angle = Math.acos(Math.max(-1, Math.min(1, dot)));
  
  return radius * angle;
}

/**
 * Exponential map: tangent space → manifold
 * Maps velocity vector to point on manifold
 */
export function exponentialMap(
  basePoint: Point3D,
  tangentVector: Point3D,
  t: number
): Point3D {
  // Simple implementation: geodesic in direction of tangent
  return {
    x: basePoint.x + tangentVector.x * t,
    y: basePoint.y + tangentVector.y * t,
    z: basePoint.z + tangentVector.z * t,
  };
}

/**
 * Parallel transport vector along curve
 * Maintains "parallelness" in curved space
 */
export function parallelTransport(
  vector: Point3D,
  fromPoint: Point3D,
  toPoint: Point3D
): Point3D {
  // Simplified: project vector onto tangent space at toPoint
  // For sphere: subtract radial component
  
  const normalize = (p: Point3D) => {
    const r = Math.sqrt(p.x * p.x + p.y * p.y + p.z * p.z);
    return r === 0 ? { x: 0, y: 0, z: 0 } : { x: p.x / r, y: p.y / r, z: p.z / r };
  };
  
  const normal = normalize(toPoint);
  const dot = vector.x * normal.x + vector.y * normal.y + vector.z * normal.z;
  
  return {
    x: vector.x - dot * normal.x,
    y: vector.y - dot * normal.y,
    z: vector.z - dot * normal.z,
  };
}
