// SYNAPSE Shader: Superposition
// Quantum-inspired superposition state rendering

/**
 * Superposition cloud visualization
 * Renders entity as probability cloud before observation
 * @param pos Position in space
 * @param coherence Coherence value [0, 1]
 * @param time Animation time
 * @return Probability density
 */
float superposition(vec3 pos, float coherence, float time) {
    // Multiple ghost states
    float state1 = sin(pos.x * 10.0 + time) * 0.5 + 0.5;
    float state2 = cos(pos.y * 10.0 - time * 1.3) * 0.5 + 0.5;
    float state3 = sin(pos.z * 10.0 + time * 0.7) * 0.5 + 0.5;
    
    // Combine states
    float combined = state1 * state2 * state3;
    
    // Coherence controls collapse
    // Low coherence = more superposition
    // High coherence = more collapsed
    float collapse = smoothstep(0.0, 1.0, coherence);
    
    return mix(combined, 1.0, collapse);
}

/**
 * Wave function visualization
 * Real and imaginary components
 */
vec2 waveFunction(vec3 pos, float time) {
    float k = 5.0; // Wave number
    float omega = 2.0; // Angular frequency
    
    float phase = k * length(pos) - omega * time;
    
    return vec2(
        cos(phase), // Real part
        sin(phase)  // Imaginary part
    );
}

/**
 * Probability density from wave function
 * P = |ψ|² = Re² + Im²
 */
float probabilityDensity(vec2 waveFunc) {
    return dot(waveFunc, waveFunc);
}

/**
 * Superposition of multiple states
 * Each with different probability amplitude
 */
float superpositionMulti(vec3 pos, float time, int numStates) {
    float total = 0.0;
    
    for (int i = 0; i < 8; i++) {
        if (i >= numStates) break;
        
        float phase = float(i) * 0.785398; // π/4
        float k = 5.0 + float(i) * 0.5;
        
        vec3 offset = vec3(cos(phase), sin(phase), 0.0) * 0.3;
        vec3 displaced = pos - offset;
        
        float state = exp(-dot(displaced, displaced) * 3.0);
        total += state;
    }
    
    return total / float(numStates);
}

/**
 * Collapse animation
 * Smooth transition from superposition to definite state
 * @param progress Collapse progress [0, 1]
 */
float collapseAnimation(vec3 pos, vec3 targetPos, float progress) {
    // Gaussian centered on target
    vec3 diff = pos - targetPos;
    float dist2 = dot(diff, diff);
    
    // Width shrinks during collapse
    float width = 1.0 - 0.9 * progress;
    
    return exp(-dist2 / (width * width));
}

/**
 * Interference pattern
 * Two-state superposition creating fringes
 */
float interference(vec3 pos, vec3 source1, vec3 source2, float time) {
    float k = 10.0;
    
    float phase1 = k * length(pos - source1) - 2.0 * time;
    float phase2 = k * length(pos - source2) - 2.0 * time;
    
    float wave1 = cos(phase1);
    float wave2 = cos(phase2);
    
    // Superposition
    float combined = wave1 + wave2;
    
    // Intensity = |amplitude|²
    return combined * combined / 4.0;
}

/**
 * Entanglement visualization
 * Correlated state between two entities
 */
vec3 entanglementField(vec3 pos, vec3 entity1, vec3 entity2, float time) {
    vec3 midpoint = (entity1 + entity2) * 0.5;
    vec3 direction = normalize(entity2 - entity1);
    
    // Project position onto line between entities
    float projection = dot(pos - midpoint, direction);
    vec3 closest = midpoint + direction * projection;
    
    float distToLine = length(pos - closest);
    
    // Helical pattern along connection
    float helix = sin(projection * 10.0 + time) * cos(projection * 10.0 - time * 0.7);
    
    // Field strength
    float strength = exp(-distToLine * 5.0) * (0.5 + 0.5 * helix);
    
    // Color: purple for entanglement
    return vec3(0.7, 0.3, 0.9) * strength;
}

/**
 * Decoherence effect
 * Gradual loss of quantum properties
 */
float decoherence(float superpositionValue, float decoherenceRate, float time) {
    // Exponential decay of superposition
    float decay = exp(-decoherenceRate * time);
    
    return mix(1.0, superpositionValue, decay);
}
