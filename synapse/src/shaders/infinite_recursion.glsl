// SYNAPSE Shader: Infinite Recursion
// Infinitely stable recursion via Fibonacci scaling

const float PHI = 1.6180339887;
const float TWO_PI = 6.28318530718;
const float GOLDEN_ANGLE = 2.39996322972;  // 2π(1 - 1/φ)
const float EPSILON = 0.00055;
const int MAX_ITERATIONS = 42;  // The Answer

/**
 * Single iteration of recursive transformation
 * Scales by golden ratio and rotates by golden angle
 */
vec3 recursiveStep(vec3 pos, int iteration, float epsilon) {
    // Scale down by golden ratio
    vec3 scaled = pos / PHI;
    
    // Rotate by golden angle in XY plane
    float angle = float(iteration) * GOLDEN_ANGLE;
    mat2 rotation = mat2(
        cos(angle), -sin(angle),
        sin(angle), cos(angle)
    );
    scaled.xy = rotation * scaled.xy;
    
    // Add epsilon to prevent collapse to zero
    scaled += epsilon;
    
    return scaled;
}

/**
 * Full infinite recursion
 * Applies recursive steps until convergence
 * @param pos Starting position
 * @param depth Maximum recursion depth (typically 42)
 * @param epsilon Stability constant
 * @return Final converged position
 */
vec3 infiniteRecursion(vec3 pos, float depth, float epsilon) {
    vec3 result = pos;
    int maxIter = int(min(depth, float(MAX_ITERATIONS)));
    
    for (int i = 0; i < MAX_ITERATIONS; i++) {
        if (i >= maxIter) break;
        
        // Apply recursive transformation
        result = recursiveStep(result, i, epsilon);
        
        // Check for convergence
        if (length(result) < epsilon * 10.0) {
            break;
        }
    }
    
    return result;
}

/**
 * Fibonacci spiral in recursive space
 * Each iteration is a layer of the spiral
 */
vec3 fibonacciRecursiveSpiral(float t, float scale, float time) {
    // Base spiral parameters
    float radius = pow(PHI, t / TWO_PI) * scale;
    float theta = t + time;
    
    // Calculate base position
    vec3 basePos = vec3(
        radius * cos(theta),
        radius * sin(theta),
        t * 0.1
    );
    
    // Apply recursive transformation based on parameter
    int iteration = int(mod(t / TWO_PI, float(MAX_ITERATIONS)));
    return recursiveStep(basePos, iteration, EPSILON);
}

/**
 * Recursive self-similarity check
 * Returns how self-similar a position is across scales
 */
float selfSimilarity(vec3 pos, float epsilon) {
    vec3 scaled = pos;
    float similarity = 1.0;
    
    // Check similarity across multiple scales
    for (int i = 0; i < 5; i++) {
        scaled = recursiveStep(scaled, i, epsilon);
        
        // Compare scaled version to original (normalized)
        float diff = length(normalize(scaled) - normalize(pos));
        similarity *= exp(-diff);
    }
    
    return similarity;
}

/**
 * Stable attractor point
 * The fixed point that recursion converges to
 */
vec3 stableAttractor(float epsilon) {
    // The attractor is at the origin, offset by epsilon
    // This is where infinite recursion stabilizes
    return vec3(epsilon, epsilon, epsilon);
}

/**
 * Recursion depth field
 * Visualizes how many iterations needed to reach stability
 */
float recursionDepth(vec3 pos, float epsilon, float threshold) {
    vec3 current = pos;
    float depth = 0.0;
    
    for (int i = 0; i < MAX_ITERATIONS; i++) {
        current = recursiveStep(current, i, epsilon);
        depth += 1.0;
        
        // Check if we've converged
        if (length(current - stableAttractor(epsilon)) < threshold) {
            break;
        }
    }
    
    return depth;
}

/**
 * Fractal dimension estimate
 * Measures how space-filling the recursive structure is
 */
float fractalDimension(vec3 pos, float epsilon) {
    // Use box-counting approach at multiple scales
    float dimension = 0.0;
    vec3 current = pos;
    
    for (int i = 1; i < 6; i++) {
        current = recursiveStep(current, i, epsilon);
        float scale = pow(PHI, float(i));
        float boxes = scale * length(current);
        dimension += log(boxes) / log(scale);
    }
    
    return dimension / 5.0;  // Average across scales
}

/**
 * Color based on recursion properties
 */
vec3 recursionColor(vec3 pos, float depth, float time) {
    // Hue from recursion depth
    float hue = mod(depth / float(MAX_ITERATIONS) + time * 0.1, 1.0);
    
    // Saturation from self-similarity
    float similarity = selfSimilarity(pos, EPSILON);
    float saturation = 0.5 + 0.5 * similarity;
    
    // Value from fractal dimension
    float dimension = fractalDimension(pos, EPSILON);
    float value = 0.3 + 0.7 * (dimension / 3.0);
    
    // HSV to RGB
    vec3 c = vec3(hue, saturation, value);
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

/**
 * Recursive glow field
 * Brightness based on proximity to recursive layers
 */
float recursiveGlow(vec3 pos, float time, float epsilon) {
    float glow = 0.0;
    vec3 current = pos;
    
    // Sum contributions from each recursive layer
    for (int i = 0; i < 10; i++) {
        current = recursiveStep(current, i, epsilon);
        
        // Distance to this layer
        float dist = length(pos - current * pow(PHI, float(i)));
        
        // Pulsing at each layer
        float pulse = 0.5 + 0.5 * sin(time * 2.0 + float(i) * 0.5);
        
        // Add contribution
        glow += exp(-dist * 5.0) * pulse / float(i + 1);
    }
    
    return glow;
}

/**
 * Stability indicator
 * Returns how stable the recursion is (close to attractor)
 */
float stabilityMeasure(vec3 pos, float epsilon) {
    vec3 converged = infiniteRecursion(pos, float(MAX_ITERATIONS), epsilon);
    vec3 attractor = stableAttractor(epsilon);
    
    float distance = length(converged - attractor);
    
    // Stability is inverse of distance (exponential falloff)
    return exp(-distance / epsilon);
}

/**
 * Infinite helix combining recursion and spiral
 */
vec3 infiniteHelix(float t, float radius, float epsilon, float time) {
    // Base helix
    vec3 helix = vec3(
        radius * cos(t),
        radius * sin(t),
        t * 0.1
    );
    
    // Apply recursive scaling
    int iteration = int(t / (TWO_PI / float(MAX_ITERATIONS)));
    helix = recursiveStep(helix, iteration, epsilon);
    
    // Add time-based animation
    float timeFactor = sin(time + t * 0.1);
    helix *= 1.0 + timeFactor * 0.1;
    
    return helix;
}

/**
 * Main shader function
 * Combines all recursive elements
 */
vec4 infiniteRecursionShader(vec3 worldPos, float time, float epsilon) {
    // Calculate recursion depth at this position
    float depth = recursionDepth(worldPos, epsilon, epsilon * 10.0);
    
    // Get color based on recursion properties
    vec3 color = recursionColor(worldPos, depth, time);
    
    // Add recursive glow
    float glow = recursiveGlow(worldPos, time, epsilon);
    
    // Add stability indicator (brighten stable regions)
    float stability = stabilityMeasure(worldPos, epsilon);
    color = mix(color, vec3(1.0, 1.0, 0.8), stability * 0.3);
    
    // Calculate alpha from glow and stability
    float alpha = clamp(glow + stability * 0.5, 0.0, 1.0);
    
    return vec4(color * (1.0 + glow * 0.5), alpha);
}

/**
 * Epsilon preservation check
 * Verifies that epsilon is maintained across recursive steps
 */
bool epsilonPreserved(vec3 pos, float epsilon, float tolerance) {
    vec3 current = pos;
    
    for (int i = 0; i < 10; i++) {
        vec3 next = recursiveStep(current, i, epsilon);
        
        // Check that we're not collapsing to zero
        if (length(next) < epsilon / 2.0) {
            return false;
        }
        
        current = next;
    }
    
    return true;
}
