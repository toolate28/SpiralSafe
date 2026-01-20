// SYNAPSE Shader: Fibonacci Spiral
// Generates golden ratio spiral in 3D space

const float PHI = 1.6180339887;
const float TWO_PI = 6.28318530718;

/**
 * Calculate point on Fibonacci spiral
 * @param t Parameter along spiral
 * @param scale Base scale factor
 * @return 3D position on spiral
 */
vec3 fibonacciSpiral(float t, float scale) {
    // Golden ratio exponential expansion: r = φ^(t/(2π))
    float radius = pow(PHI, t / TWO_PI) * scale;
    float theta = t;
    float z = t * 0.1; // Vertical lift
    
    return vec3(
        radius * cos(theta),
        radius * sin(theta),
        z
    );
}

/**
 * Calculate tangent vector at point on spiral
 */
vec3 fibonacciTangent(float t, float scale) {
    float radius = pow(PHI, t / TWO_PI) * scale;
    float dr_dt = radius * log(PHI) / TWO_PI;
    float theta = t;
    
    return normalize(vec3(
        dr_dt * cos(theta) - radius * sin(theta),
        dr_dt * sin(theta) + radius * cos(theta),
        0.1
    ));
}

/**
 * Fibonacci sphere point (sunflower seed pattern)
 * Uniform distribution on sphere using golden angle
 */
vec3 fibonacciSphere(float index, float totalPoints, float radius) {
    float goldenAngle = TWO_PI * (1.0 - 1.0 / PHI);
    
    float y = 1.0 - (index / (totalPoints - 1.0)) * 2.0;
    float radiusAtY = sqrt(1.0 - y * y);
    float theta = index * goldenAngle;
    
    return vec3(
        cos(theta) * radiusAtY,
        y,
        sin(theta) * radiusAtY
    ) * radius;
}

/**
 * Calculate spiral color based on position
 * Maps position to hue using golden angle
 */
vec3 spiralColor(float t) {
    float goldenAngle = TWO_PI * (1.0 - 1.0 / PHI);
    float hue = mod(t * goldenAngle, TWO_PI) / TWO_PI;
    
    // HSV to RGB
    vec3 c = vec3(hue, 0.8, 0.9);
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

/**
 * Spiral glow effect
 * Intensity falls off with distance from spiral
 */
float spiralGlow(vec3 pos, float t, float scale, float time) {
    vec3 spiralPoint = fibonacciSpiral(t, scale);
    float dist = length(pos - spiralPoint);
    
    // Pulsing glow
    float pulse = 0.5 + 0.5 * sin(time * 2.0 + t);
    
    return exp(-dist * 5.0) * pulse;
}

/**
 * Archimedean spiral (for comparison/layout)
 * Linear growth instead of exponential
 */
vec3 archimedeanSpiral(float t, float scale) {
    float radius = t * scale / TWO_PI;
    float theta = t;
    
    return vec3(
        radius * cos(theta),
        radius * sin(theta),
        t * 0.05
    );
}
