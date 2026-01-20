// SYNAPSE Shader: Quantum Reservoir Computing
// Visualization of QRC quantum states and dynamics

/**
 * Convert complex amplitude to color
 * Phase -> hue, magnitude -> brightness
 */
vec3 complexToColor(vec2 amplitude) {
    float magnitude = length(amplitude);
    float phase = atan(amplitude.y, amplitude.x);
    
    // Map phase [-π, π] to hue [0, 1]
    float hue = (phase + 3.14159265) / (2.0 * 3.14159265);
    
    // HSV to RGB with saturation based on magnitude
    vec3 hsv = vec3(hue, 0.8, magnitude);
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(hsv.xxx + K.xyz) * 6.0 - K.www);
    return hsv.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), hsv.y);
}

/**
 * Visualize qubit state on Bloch sphere
 * |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
 */
vec3 blochSphere(float theta, float phi, float radius) {
    return vec3(
        radius * sin(theta) * cos(phi),
        radius * sin(theta) * sin(phi),
        radius * cos(theta)
    );
}

/**
 * Quantum interference pattern
 * Two-state superposition visualization
 */
float quantumInterference(vec3 pos, vec2 amplitude1, vec2 amplitude2, float time) {
    // Extract phases
    float phase1 = atan(amplitude1.y, amplitude1.x);
    float phase2 = atan(amplitude2.y, amplitude2.x);
    
    // Relative phase
    float deltaPhase = phase2 - phase1;
    
    // Interference term
    float mag1 = length(amplitude1);
    float mag2 = length(amplitude2);
    
    // Spatial wave
    float k = 10.0;
    float wave = mag1 * mag1 + mag2 * mag2 + 
                 2.0 * mag1 * mag2 * cos(k * length(pos) + deltaPhase - time);
    
    return wave;
}

/**
 * Entanglement visualization
 * Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
 */
vec3 entanglementPattern(vec3 pos, vec3 qubit1Pos, vec3 qubit2Pos, float time) {
    vec3 midpoint = (qubit1Pos + qubit2Pos) * 0.5;
    vec3 direction = normalize(qubit2Pos - qubit1Pos);
    
    // Distance to connection line
    vec3 toMid = pos - midpoint;
    float alongLine = dot(toMid, direction);
    vec3 perpendicular = toMid - direction * alongLine;
    float distToLine = length(perpendicular);
    
    // Helical entanglement pattern
    float helixAngle = alongLine * 10.0 + time;
    float helixRadius = 0.2;
    float helixIntensity = exp(-pow(distToLine - helixRadius, 2.0) * 20.0);
    
    // Color shift with phase
    float phase = helixAngle + time;
    vec3 color = vec3(
        0.5 + 0.5 * cos(phase),
        0.5 + 0.5 * cos(phase + 2.094),  // 2π/3
        0.5 + 0.5 * cos(phase + 4.189)   // 4π/3
    );
    
    return color * helixIntensity;
}

/**
 * Decoherence effect
 * Gradual loss of quantum coherence
 */
float decoherence(float initialCoherence, float time, float rate) {
    return initialCoherence * exp(-rate * time);
}

/**
 * Measurement collapse animation
 * Superposition -> definite state
 */
vec4 measurementCollapse(
    vec3 pos,
    vec3 collapseCenter,
    float progress,
    vec3 superpositionColor
) {
    float dist = length(pos - collapseCenter);
    
    // Wave front of collapse
    float collapseFront = progress * 5.0;
    float frontWidth = 0.5;
    
    // Before front: superposition (blurred)
    // After front: definite state (sharp)
    float collapsed = smoothstep(collapseFront - frontWidth, collapseFront, dist);
    
    // Intensity pulse at wave front
    float pulse = exp(-pow(dist - collapseFront, 2.0) / (frontWidth * frontWidth));
    
    vec3 definiteColor = vec3(1.0, 0.8, 0.2); // Gold for measured state
    vec3 color = mix(superpositionColor, definiteColor, collapsed);
    
    float intensity = 1.0 - progress * 0.5 + pulse * 0.5;
    
    return vec4(color * intensity, intensity);
}

/**
 * Reservoir dynamics visualization
 * Show evolution of quantum state over time
 */
vec3 reservoirDynamics(vec3 pos, float time, int nQubits) {
    vec3 color = vec3(0.0);
    
    // Each qubit contributes oscillating component
    for (int i = 0; i < 8; i++) {
        if (i >= nQubits) break;
        
        float freq = float(i + 1) * 2.0;
        float phase = float(i) * 0.785398; // π/4
        
        vec3 offset = vec3(cos(phase), sin(phase), 0.0) * 0.5;
        vec3 localPos = pos - offset;
        
        // Oscillating Gaussian
        float oscillation = sin(freq * time + phase);
        float intensity = exp(-dot(localPos, localPos) * 3.0);
        
        // Color based on qubit index
        vec3 qubitColor = vec3(
            0.5 + 0.5 * cos(phase),
            0.5 + 0.5 * sin(phase),
            0.5 + 0.5 * cos(phase + 1.57)
        );
        
        color += qubitColor * intensity * (0.5 + 0.5 * oscillation);
    }
    
    return color / float(nQubits);
}

/**
 * Fidelity visualization
 * Distance between two quantum states
 */
float fidelityField(vec3 pos, vec3 state1Center, vec3 state2Center, float fidelity) {
    // Two Gaussians with overlap proportional to fidelity
    float g1 = exp(-dot(pos - state1Center, pos - state1Center) * 5.0);
    float g2 = exp(-dot(pos - state2Center, pos - state2Center) * 5.0);
    
    // Overlap region
    float overlap = min(g1, g2);
    
    // Color intensity based on fidelity
    return mix(g1 + g2 - overlap, overlap, fidelity);
}

/**
 * Energy visualization (circuit depth)
 * Higher energy = more complex dynamics
 */
vec3 energyVisualization(vec3 pos, float energy, float time) {
    // Energy as ripples
    float rippleFreq = energy * 0.1;
    float ripple = sin(length(pos) * rippleFreq - time * 2.0);
    
    // Color: low energy = blue, high energy = red
    float normalizedEnergy = clamp(energy / 100.0, 0.0, 1.0);
    vec3 coldColor = vec3(0.0, 0.5, 1.0);
    vec3 hotColor = vec3(1.0, 0.3, 0.0);
    vec3 color = mix(coldColor, hotColor, normalizedEnergy);
    
    return color * (0.7 + 0.3 * ripple);
}

/**
 * Substrate-specific visualization
 */
vec3 substrateVisualization(vec3 pos, int substrate, float time) {
    // substrate: 0=single_qubit, 1=jc_pairs, 2=oscillator, 3=bose_hubbard, 4=aquila
    
    if (substrate == 0) {
        // Single qubit: simple Bloch sphere
        float dist = length(pos);
        return vec3(0.5, 0.7, 1.0) * exp(-pow(dist - 1.0, 2.0) * 10.0);
    }
    
    if (substrate == 1 || substrate == 2) {
        // JC pairs / Oscillators: coupled oscillators
        float osc1 = sin(length(pos - vec3(-0.5, 0.0, 0.0)) * 5.0 - time);
        float osc2 = sin(length(pos - vec3(0.5, 0.0, 0.0)) * 5.0 - time * 1.3);
        return vec3(0.7, 0.4, 0.9) * (0.5 + 0.5 * osc1 * osc2);
    }
    
    if (substrate == 3) {
        // Bose-Hubbard: lattice pattern
        vec3 latticePos = floor(pos * 3.0) / 3.0;
        float lattice = exp(-dot(pos - latticePos, pos - latticePos) * 20.0);
        return vec3(0.4, 0.8, 0.5) * lattice;
    }
    
    if (substrate == 4) {
        // Aquila: Rydberg atom array
        float hexPattern = 0.0;
        for (int i = -2; i <= 2; i++) {
            for (int j = -2; j <= 2; j++) {
                vec2 hexPos = vec2(float(i), float(j) * 0.866);
                float dist = length(pos.xy - hexPos);
                hexPattern += exp(-dist * dist * 10.0);
            }
        }
        return vec3(0.9, 0.7, 0.3) * hexPattern;
    }
    
    return vec3(0.5);
}

/**
 * QRC-HR hybrid visualization
 * Quantum reservoir controlling Hindmarsh-Rose dynamics
 */
vec3 qrcHRHybrid(vec3 pos, float qrcCoherence, float hrX, float time) {
    // QRC coherence modulates HR activity
    float hrIntensity = qrcCoherence * (0.5 + 0.5 * tanh(hrX));
    
    // Pulsing based on HR state
    float pulse = smoothstep(0.5, 1.0, hrX) * sin(time * 50.0);
    
    // Color transition: quantum blue -> neural purple
    vec3 quantumColor = vec3(0.3, 0.7, 1.0);
    vec3 neuralColor = vec3(0.8, 0.3, 0.9);
    vec3 color = mix(quantumColor, neuralColor, hrIntensity);
    
    float field = exp(-dot(pos, pos) * 2.0) * (1.0 + pulse * 0.3);
    
    return color * field;
}
