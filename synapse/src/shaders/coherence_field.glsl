// SYNAPSE Shader: Coherence Field
// 42.00055 coherence manifold visualization

const float COHERENCE_THRESHOLD = 0.4200055;
const float EPSILON = 0.00055;

/**
 * Map coherence value to color
 * Below threshold: warm colors (red-yellow)
 * Above threshold: cool colors (green-cyan-blue)
 */
vec3 coherenceColor(float coherence) {
    coherence = clamp(coherence, 0.0, 1.0);
    
    if (coherence < COHERENCE_THRESHOLD) {
        // Below threshold: red to orange to yellow
        float t = coherence / COHERENCE_THRESHOLD;
        return vec3(1.0, t * 0.8, 0.0);
    } else {
        // Above threshold: green to cyan to blue
        float t = (coherence - COHERENCE_THRESHOLD) / (1.0 - COHERENCE_THRESHOLD);
        return vec3(0.0, 1.0 - t * 0.5, t);
    }
}

/**
 * Three-phase coherence visualization
 * Curl = red, Potential = green, Dispersion = blue
 */
vec3 threePhaseColor(float curl, float potential, float dispersion) {
    return vec3(curl, potential, dispersion);
}

/**
 * Coherence field gradient
 * Visualize direction of increasing coherence
 */
vec3 coherenceGradient(vec3 pos, float coherenceFunc(vec3)) {
    float h = 0.01;
    
    float c0 = coherenceFunc(pos);
    float cx = coherenceFunc(pos + vec3(h, 0.0, 0.0));
    float cy = coherenceFunc(pos + vec3(0.0, h, 0.0));
    float cz = coherenceFunc(pos + vec3(0.0, 0.0, h));
    
    return vec3(
        (cx - c0) / h,
        (cy - c0) / h,
        (cz - c0) / h
    );
}

/**
 * Coherence field contours
 * Isosurfaces of constant coherence
 */
float coherenceContour(vec3 pos, float targetCoherence, float coherenceFunc(vec3)) {
    float coherence = coherenceFunc(pos);
    float diff = abs(coherence - targetCoherence);
    
    // Sharp line at exact value
    return smoothstep(0.05, 0.0, diff);
}

/**
 * Quantum foam visualization
 * ε = 0.00055 base layer
 */
vec3 quantumFoam(vec3 pos, float time) {
    // High-frequency noise at epsilon scale
    float noise1 = sin(pos.x * 1000.0 + time * 10.0) * 0.5 + 0.5;
    float noise2 = cos(pos.y * 1000.0 - time * 13.0) * 0.5 + 0.5;
    float noise3 = sin(pos.z * 1000.0 + time * 17.0) * 0.5 + 0.5;
    
    float foam = (noise1 + noise2 + noise3) / 3.0;
    
    // Very low intensity - the foam is subtle
    return vec3(foam) * EPSILON * 5.0;
}

/**
 * Coherence threshold boundary
 * Highlight 42.00055% isosurface
 */
vec4 thresholdBoundary(vec3 pos, float coherence, float time) {
    float diff = abs(coherence - COHERENCE_THRESHOLD);
    
    if (diff > 0.05) {
        return vec4(0.0); // Far from boundary
    }
    
    // Pulsing boundary
    float pulse = 0.5 + 0.5 * sin(time * 2.0);
    float intensity = (1.0 - diff / 0.05) * pulse;
    
    // Gold color for the critical threshold
    vec3 color = vec3(1.0, 0.843, 0.0);
    
    return vec4(color * intensity, intensity);
}

/**
 * Curl visualization (circular patterns)
 * Red channel in three-phase
 */
vec3 curlField(vec3 pos, float time) {
    // Rotational field
    vec3 center = vec3(0.0);
    vec3 r = pos - center;
    
    // Circular flow
    vec3 flow = vec3(-r.y, r.x, 0.0);
    float curlStrength = length(flow) * exp(-dot(r, r) * 0.5);
    
    // Animated rotation
    float rotation = sin(atan(r.y, r.x) * 5.0 - time * 2.0);
    
    return vec3(1.0, 0.0, 0.0) * curlStrength * (0.5 + 0.5 * rotation);
}

/**
 * Potential field visualization (gradient patterns)
 * Green channel in three-phase
 */
vec3 potentialField(vec3 pos) {
    // Potential increases toward center
    float dist = length(pos);
    float potential = exp(-dist * 0.5);
    
    return vec3(0.0, potential, 0.0);
}

/**
 * Dispersion field visualization (chaotic patterns)
 * Blue channel in three-phase
 */
vec3 dispersionField(vec3 pos, float time) {
    // High-frequency chaos
    float dispersion = 0.0;
    dispersion += sin(pos.x * 10.0 + time * 3.0);
    dispersion += cos(pos.y * 13.0 - time * 4.0);
    dispersion += sin(pos.z * 17.0 + time * 5.0);
    dispersion = abs(dispersion) / 3.0;
    
    return vec3(0.0, 0.0, dispersion);
}

/**
 * Icosahedral symmetry overlay
 * 42 = V + E for icosahedron
 */
vec3 icosahedralSymmetry(vec3 pos) {
    // Icosahedron has 5-fold symmetry
    float phi = 1.618033988749895; // Golden ratio
    
    // Icosahedral symmetry axes
    vec3 axes[3];
    axes[0] = normalize(vec3(1.0, phi, 0.0));
    axes[1] = normalize(vec3(0.0, 1.0, phi));
    axes[2] = normalize(vec3(phi, 0.0, 1.0));
    
    float symmetry = 0.0;
    for (int i = 0; i < 3; i++) {
        float proj = abs(dot(normalize(pos), axes[i]));
        symmetry = max(symmetry, proj);
    }
    
    // Highlight symmetry axes
    return vec3(symmetry * 0.3);
}

/**
 * Coherence flow visualization
 * Particle trails showing coherence increase/decrease
 */
vec3 coherenceFlow(vec3 pos, vec3 velocity, float coherence) {
    // Flow direction based on coherence gradient
    float speed = length(velocity);
    vec3 direction = normalize(velocity);
    
    // Color based on flow direction and coherence
    vec3 color = coherenceColor(coherence);
    
    // Intensity based on speed
    float intensity = tanh(speed);
    
    return color * intensity;
}

/**
 * Multi-scale coherence visualization
 * Different frequencies for different scales
 */
vec3 multiscaleCoherence(vec3 pos, float time, float scale) {
    vec3 color = vec3(0.0);
    
    // Large scale (slow variation)
    color += coherenceColor(0.5 + 0.3 * sin(length(pos) * scale + time * 0.5));
    
    // Medium scale
    color += coherenceColor(0.5 + 0.2 * sin(length(pos) * scale * 3.0 + time)) * 0.5;
    
    // Fine scale
    color += coherenceColor(0.5 + 0.1 * sin(length(pos) * scale * 10.0 + time * 2.0)) * 0.25;
    
    return color / 1.75; // Normalize
}
