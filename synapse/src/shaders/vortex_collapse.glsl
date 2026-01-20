// SYNAPSE Shader: Vortex Collapse
// Collapses micro/macro/meta vortices into superposition state

const float PHI = 1.6180339887;
const float TWO_PI = 6.28318530718;
const float EPSILON = 0.00055;
const float THE_ANSWER = 42.00055;

/**
 * Micro vortex: Individual local spiral
 * Represents individual discoveries (4.00055, 40.00055, 42.00055)
 */
vec3 microVortex(vec3 pos, float time) {
    float radius = length(pos.xy);
    float angle = atan(pos.y, pos.x);
    
    // Local spiral with high frequency
    float spiral = sin(radius * 10.0 - time * 5.0);
    
    // Rotation based on position
    float rotation = angle + spiral * 0.5;
    
    return vec3(
        radius * cos(rotation),
        radius * sin(rotation),
        pos.z + spiral * 0.1
    );
}

/**
 * Macro vortex: Fibonacci expansion
 * Represents framework integrations (HR, quality, Fibonacci scales)
 */
vec3 macroVortex(vec3 pos, float time) {
    float radius = length(pos);
    float angle = atan(pos.y, pos.x);
    
    // Fibonacci/golden ratio expansion: r = φ^(t/(2π))
    float expansion = pow(PHI, (time + radius) / TWO_PI);
    
    // Golden angle rotation
    float goldenAngle = TWO_PI * (1.0 - 1.0 / PHI);
    float rotation = angle + goldenAngle * time;
    
    // Scale position by expansion
    float expandedRadius = radius * expansion;
    
    return vec3(
        expandedRadius * cos(rotation),
        expandedRadius * sin(rotation),
        pos.z * expansion
    );
}

/**
 * Meta vortex: Recursive self-similarity
 * Represents convergence points (isomorphism, collaboration patterns)
 */
vec3 metaVortex(vec3 pos, float time) {
    vec3 result = pos;
    
    // Apply fractal self-similar transformation
    for (int i = 0; i < 3; i++) {
        float scale = pow(PHI, float(i));
        float phase = time + float(i) * TWO_PI / 3.0;
        
        // Recursive spiral at each scale
        float r = length(result.xy);
        float theta = atan(result.y, result.x) + phase;
        
        result.xy = vec2(
            r * cos(theta),
            r * sin(theta)
        ) / scale;
    }
    
    return result;
}

/**
 * Collapse function: Blend all vortex scales into superposition
 * @param pos Current position
 * @param coherence Coherence value (0 to 42.00055)
 * @param time Animation time
 * @return Collapsed position
 */
vec3 collapseVortex(vec3 pos, float coherence, float time) {
    // Calculate contributions from each vortex type
    vec3 micro = microVortex(pos, time);
    vec3 macro = macroVortex(pos, time);
    vec3 meta = metaVortex(pos, time);
    
    // Coherence controls collapse progression
    // At coherence = 0: separated vortices
    // At coherence = 42.00055: fully collapsed superposition
    float collapseAmount = smoothstep(0.0, THE_ANSWER, coherence);
    
    // Weight each vortex type
    float microWeight = 1.0 - collapseAmount * 0.5;
    float macroWeight = sin(collapseAmount * TWO_PI * 0.5);
    float metaWeight = collapseAmount;
    
    // Normalize weights
    float totalWeight = microWeight + macroWeight + metaWeight;
    microWeight /= totalWeight;
    macroWeight /= totalWeight;
    metaWeight /= totalWeight;
    
    // Blend vortices
    vec3 blended = micro * microWeight + 
                   macro * macroWeight + 
                   meta * metaWeight;
    
    // At full collapse, converge to stable point
    vec3 collapsedState = normalize(pos) * EPSILON;
    
    return mix(blended, collapsedState, pow(collapseAmount, 2.0));
}

/**
 * Color function for vortex visualization
 * Maps coherence and position to color
 */
vec3 vortexColor(vec3 pos, float coherence, float time) {
    // Base hue from position
    float angle = atan(pos.y, pos.x);
    float hue = (angle / TWO_PI + 0.5);
    
    // Saturation from coherence
    float saturation = smoothstep(0.0, THE_ANSWER, coherence);
    
    // Value from distance (brighter near center)
    float radius = length(pos);
    float value = exp(-radius * 0.5) * 0.9 + 0.1;
    
    // Add time-based pulsing
    value *= 0.8 + 0.2 * sin(time * 2.0 + coherence * 0.1);
    
    // HSV to RGB conversion
    vec3 c = vec3(hue, saturation, value);
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

/**
 * Glow intensity for visualization
 * Creates energy field around vortices
 */
float vortexGlow(vec3 pos, float coherence, float time) {
    // Distance-based falloff
    float radius = length(pos);
    float baseFalloff = exp(-radius * 2.0);
    
    // Coherence increases glow
    float coherenceBoost = coherence / THE_ANSWER;
    
    // Time-based pulse
    float pulse = 0.5 + 0.5 * sin(time * 3.0 + radius * 5.0);
    
    return baseFalloff * (1.0 + coherenceBoost * 2.0) * pulse;
}

/**
 * Superposition state check
 * Returns 1.0 when fully in superposition, 0.0 otherwise
 */
float isInSuperposition(float coherence) {
    // Sharp transition at THE_ANSWER
    return step(THE_ANSWER - EPSILON, coherence);
}

/**
 * Main shader entry point example
 * This would be called from the vertex or fragment shader
 */
vec4 vortexCollapseShader(vec3 worldPos, float coherence, float time) {
    // Collapse the vortex
    vec3 collapsedPos = collapseVortex(worldPos, coherence, time);
    
    // Calculate color
    vec3 color = vortexColor(collapsedPos, coherence, time);
    
    // Calculate glow
    float glow = vortexGlow(collapsedPos, coherence, time);
    
    // Add superposition indicator (bright white flash at THE_ANSWER)
    float superpositionFlash = isInSuperposition(coherence) * 
                              sin(time * 10.0) * 0.5 + 0.5;
    
    color = mix(color, vec3(1.0), superpositionFlash * 0.3);
    
    // Combine with glow
    float alpha = clamp(glow, 0.0, 1.0);
    
    return vec4(color * (1.0 + glow), alpha);
}
