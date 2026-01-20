// SYNAPSE Shader: Hindmarsh-Rose Neural Dynamics
// Visualization of neural quality control patterns

/**
 * Convert HSV to RGB
 */
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

/**
 * Neural pulse visualization from HR state
 * @param x Membrane potential (fast variable)
 * @param y Recovery variable (medium variable)
 * @param z Adaptation current (slow variable)
 * @param time Current time for animations
 * @return RGBA color with intensity
 */
vec4 neuralPulse(float x, float y, float z, float time) {
    // x (membrane potential) -> brightness
    float brightness = 0.5 + 0.5 * tanh(x + 0.5);
    
    // y (recovery) -> hue shift (blue to purple range)
    float hue = 0.6 - y * 0.1;
    hue = clamp(hue, 0.0, 1.0);
    
    // z (adaptation) -> saturation
    float saturation = 0.8 - z * 0.1;
    saturation = clamp(saturation, 0.3, 1.0);
    
    // Spike visualization: rapid brightness burst
    float spike = 0.0;
    if (x > 0.5) {
        spike = smoothstep(0.5, 1.0, x) * abs(sin(time * 50.0));
    }
    
    brightness = clamp(brightness + spike * 0.3, 0.0, 1.0);
    
    vec3 color = hsv2rgb(vec3(hue, saturation, brightness));
    
    return vec4(color, 1.0);
}

/**
 * Spiking neuron particle burst effect
 */
vec3 spikeBurst(vec3 pos, vec3 neuronPos, float x, float time) {
    if (x < 0.5) return vec3(0.0); // No spike
    
    float spikeTime = time - floor(time); // Periodic
    vec3 diff = pos - neuronPos;
    float dist = length(diff);
    
    // Expanding sphere of activity
    float burstRadius = spikeTime * 2.0;
    float burstWidth = 0.3;
    
    float intensity = exp(-pow(dist - burstRadius, 2.0) / (burstWidth * burstWidth));
    intensity *= (1.0 - spikeTime); // Fade out
    
    // Electric blue color
    return vec3(0.3, 0.7, 1.0) * intensity;
}

/**
 * Bursting pattern as wave propagation
 * Sustained oscillations spread outward
 */
vec3 burstingWave(vec3 pos, vec3 sourcePos, float x, float y, float time) {
    vec3 diff = pos - sourcePos;
    float dist = length(diff);
    
    // Check if in bursting regime (x oscillating, y moderate)
    if (x < 0.3 || x > 0.7) return vec3(0.0);
    
    // Wave parameters
    float wavelength = 0.5;
    float speed = 1.0;
    
    // Traveling wave
    float phase = 6.28318 * (dist / wavelength - speed * time);
    float wave = 0.5 + 0.5 * sin(phase);
    
    // Attenuation with distance
    float attenuation = exp(-dist * 0.5);
    
    // Purple for bursting
    return vec3(0.8, 0.3, 0.9) * wave * attenuation;
}

/**
 * Resting state ambient glow
 * Stable low-activity visualization
 */
vec3 restingGlow(vec3 pos, vec3 neuronPos, float z) {
    vec3 diff = pos - neuronPos;
    float dist = length(diff);
    
    // Soft glow around neuron
    float glow = exp(-dist * 3.0);
    
    // z controls glow intensity (adaptation level)
    float intensity = 0.2 + z * 0.1;
    intensity = clamp(intensity, 0.1, 0.5);
    
    // Cyan for resting
    return vec3(0.2, 0.5, 0.6) * glow * intensity;
}

/**
 * Chaotic dynamics visualization
 * Irregular, unpredictable patterns
 */
vec3 chaoticPattern(vec3 pos, float x, float y, float z, float time) {
    // Multiple frequencies creating chaos
    float chaos1 = sin(pos.x * 5.0 + time * x * 10.0);
    float chaos2 = cos(pos.y * 7.0 - time * y * 8.0);
    float chaos3 = sin(pos.z * 6.0 + time * z * 12.0);
    
    float intensity = (chaos1 + chaos2 + chaos3) * 0.333 + 0.5;
    
    // Shifting colors
    float hue = fract(time * 0.5 + intensity);
    vec3 color = hsv2rgb(vec3(hue, 0.7, intensity));
    
    return color * 0.5;
}

/**
 * Neural network connectivity visualization
 * Synapse strength shown as colored connections
 */
vec3 synapseConnection(
    vec3 pos,
    vec3 neuron1Pos,
    vec3 neuron2Pos,
    float strength,
    float time
) {
    // Find closest point on line between neurons
    vec3 direction = neuron2Pos - neuron1Pos;
    float lineLength = length(direction);
    direction = normalize(direction);
    
    float projection = dot(pos - neuron1Pos, direction);
    projection = clamp(projection, 0.0, lineLength);
    
    vec3 closestPoint = neuron1Pos + direction * projection;
    float distToLine = length(pos - closestPoint);
    
    // Connection thickness based on strength
    float thickness = 0.1 * strength;
    float intensity = exp(-distToLine / thickness);
    
    // Pulsing activity along synapse
    float pulse = 0.5 + 0.5 * sin(projection * 10.0 - time * 5.0);
    
    // Color based on strength
    vec3 weakColor = vec3(0.3, 0.3, 0.5);
    vec3 strongColor = vec3(1.0, 0.5, 0.2);
    vec3 color = mix(weakColor, strongColor, strength);
    
    return color * intensity * pulse;
}

/**
 * Adaptive resonance
 * Slow z-variable creates ambient field shift
 */
vec3 adaptiveResonance(vec3 pos, float z, float time) {
    // Very slow oscillation from adaptation
    float resonance = sin(time * 0.1 + z);
    
    // Creates subtle field modulation
    float field = 0.05 * resonance * exp(-length(pos) * 0.1);
    
    return vec3(field * 0.5, field * 0.7, field);
}

/**
 * Quality indicator color mapping
 * Low quality = red, medium = yellow, high = green
 */
vec3 qualityColor(float quality) {
    quality = clamp(quality, 0.0, 1.0);
    
    if (quality < 0.5) {
        // Red to yellow
        float t = quality * 2.0;
        return vec3(1.0, t, 0.0);
    } else {
        // Yellow to green
        float t = (quality - 0.5) * 2.0;
        return vec3(1.0 - t, 1.0, 0.0);
    }
}
