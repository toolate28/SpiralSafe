// SYNAPSE Shader: Supergravity
// Visualization of approaching speed of light and topology inversion

const float C = 1.0; // Speed of light (normalized)

/**
 * Lorentz contraction along velocity direction
 * γ = 1/√(1 - v²/c²)
 * @param pos Position vector
 * @param velocity_c Velocity as fraction of c [0, 1)
 * @return Contracted position
 */
vec3 lorentzContract(vec3 pos, float velocity_c) {
    if (velocity_c >= 0.9999) {
        // At c: topology inversion
        return invertTopology(pos);
    }
    
    // Lorentz factor
    float gamma = 1.0 / sqrt(1.0 - velocity_c * velocity_c);
    
    // Contract along z-axis (direction of motion)
    vec3 contracted = pos;
    contracted.z /= gamma;
    
    return contracted;
}

/**
 * Topology inversion (inside-out)
 * Applied when exceeding c threshold
 * @param pos Position vector
 * @return Inverted position
 */
vec3 invertTopology(vec3 pos) {
    float r2 = dot(pos, pos);
    
    if (r2 < 0.0001) {
        // Avoid singularity at origin
        return pos;
    }
    
    // Inversion through unit sphere: P' = P / |P|²
    return pos / r2;
}

/**
 * Time dilation effect
 * t' = t / γ
 */
float timeDilation(float time, float velocity_c) {
    if (velocity_c >= 0.9999) return 0.0;
    
    float gamma = 1.0 / sqrt(1.0 - velocity_c * velocity_c);
    return time / gamma;
}

/**
 * Relativistic Doppler shift for color
 * Blue-shift approaching, red-shift receding
 */
vec3 dopplerShift(vec3 baseColor, float velocity_c, float angle) {
    // angle: 0 = approaching, π = receding
    
    float beta = velocity_c;
    float doppler = sqrt((1.0 - beta) / (1.0 + beta));
    
    if (angle < 1.57) { // Approaching (< π/2)
        doppler = 1.0 / doppler; // Blue shift
    }
    
    // Shift hue
    return baseColor * doppler;
}

/**
 * Gravitational lensing effect
 * Light bending near massive objects
 */
vec3 gravitationalLens(vec3 pos, vec3 massCenter, float mass) {
    vec3 direction = pos - massCenter;
    float distance = length(direction);
    
    if (distance < 0.001) return pos;
    
    // Schwarzschild radius (simplified)
    float rs = 2.0 * mass;
    
    // Deflection angle
    float deflection = 4.0 * mass / distance;
    
    // Perpendicular direction
    vec3 tangent = normalize(cross(direction, vec3(0.0, 0.0, 1.0)));
    
    return pos + tangent * deflection;
}

/**
 * Event horizon visualization
 * Nothing escapes beyond this point
 */
float eventHorizon(vec3 pos, vec3 center, float mass) {
    float distance = length(pos - center);
    float rs = 2.0 * mass; // Schwarzschild radius
    
    if (distance < rs) {
        return 0.0; // Inside event horizon - no light escapes
    }
    
    // Brightness falls off approaching horizon
    return smoothstep(rs, rs * 2.0, distance);
}

/**
 * Spiral tightening as approaching c
 * At threshold: spiral collapses to point
 */
vec3 spiralTightening(vec3 spiralPos, float velocity_c, float coherence) {
    float threshold = 0.4200055; // 42.00055% coherence
    
    if (coherence < threshold) {
        return spiralPos;
    }
    
    // Tightening factor increases near c
    float tightness = velocity_c * velocity_c;
    
    // Compress spiral radially
    float r = length(spiralPos.xy);
    float theta = atan(spiralPos.y, spiralPos.x);
    
    float newR = r * (1.0 - tightness);
    
    return vec3(
        newR * cos(theta),
        newR * sin(theta),
        spiralPos.z * (1.0 - tightness * 0.5)
    );
}

/**
 * Isomorphism break visualization
 * Discrete → continuous boundary fractures at c
 */
vec4 isomorphismBreak(vec3 pos, float velocity_c, float time) {
    if (velocity_c < 0.99) {
        return vec4(1.0); // Normal space
    }
    
    // Fracture pattern
    float fracture = sin(pos.x * 50.0 + time * 5.0) * 
                     cos(pos.y * 50.0 - time * 3.0) *
                     sin(pos.z * 50.0 + time * 4.0);
    
    // Intensity increases near c
    float intensity = (velocity_c - 0.99) * 100.0;
    
    // Chromatic aberration colors
    vec3 color = vec3(
        1.0 - fracture * 0.5,
        0.5 + fracture * 0.3,
        0.5 - fracture * 0.3
    );
    
    return vec4(color, intensity);
}

/**
 * Supergravity field strength
 * Increases dramatically near c
 */
float supergravityStrength(float velocity_c) {
    if (velocity_c >= 0.9999) return 1000.0; // Infinite at c
    
    // γ - 1 gives field strength
    float gamma = 1.0 / sqrt(1.0 - velocity_c * velocity_c);
    return gamma - 1.0;
}

/**
 * Coordinate singularity at c
 * Spacetime coordinates become ill-defined
 */
bool isCoordinateSingular(float velocity_c) {
    return velocity_c >= 0.9999;
}
