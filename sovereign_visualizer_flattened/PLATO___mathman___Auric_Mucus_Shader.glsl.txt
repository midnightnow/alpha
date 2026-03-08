// Auric_Mucus_Shader.glsl
// Purpose: Visualize Biofield Coherence based on PMG Physics
// Uniforms: Passed from JS Resonance Engine

uniform float u_time;
uniform float u_haric_phase;       // The 26-Vector: Intent/Lift
uniform float u_auric_density;     // The 24-Vector: Measure/Weight
uniform float u_physical_ground;   // The 10-Vector: Number/Position
uniform float u_field_remainder;   // Biquadratic Error (Hades Gap)
uniform float u_unfold_progress;   // 0.0 -> 1.0 (Pedestal Construction)

// Spinal Cadence Uniforms
uniform float u_stations[7];       // Chakra Altitudes
uniform int u_multiplicity[7];     // Nodal Split Count (1-2-1-4-1-2-1)

varying vec2 vUv;

// PMG Invariants
const float UNITY_THRESHOLD = 0.8254;
const float HADES_SLACK = 0.005566;
const float VITRIFICATION_LIMIT = 0.9999;
const float HADES_GAP = 0.12354;

// Color Palette
const vec3 COLOR_VAPOR = vec3(0.0, 0.8, 1.0);     // Cyan Jitter
const vec3 COLOR_STONE = vec3(0.9, 0.9, 0.95);    // Healthy Physical
const vec3 COLOR_GOLD = vec3(1.0, 0.84, 0.0);     // Sintered Resonance
const vec3 COLOR_MUCUS = vec3(0.4, 0.4, 0.45);    // Stagnant/Destructive

void main() {
    vec2 p = vUv * 2.0 - 1.0;
    float y = vUv.y * 8.0; // Scale to 8-unit octave

    // 1. MULTIPLICITY SIEVE
    int m = 1;
    float station_influence = 0.0;
    for(int i = 0; i < 7; i++) {
        float dist = abs(y - u_stations[i]);
        if(dist < 0.25) {
            m = u_multiplicity[i];
            station_influence = smoothstep(0.25, 0.0, dist);
        }
    }

    // 2. NODAL SPLIT (The Phonetic Torque)
    float pattern = cos(p.x * float(m) * 10.0 + u_time * 2.0);
    
    // 3. HINGE UNFOLD (Geometric Sieve)
    // Only lift if progress covers this altitude
    float lift_mask = step(y, u_unfold_progress * 8.0);
    
    // 4. FIELD STABILITY (Vapor vs Stone)
    float is_sintered = step(u_field_remainder, HADES_GAP);
    vec3 base_color = mix(COLOR_VAPOR, COLOR_GOLD, is_sintered);

    // 5. Calculate Local Coherence
    float coherence = (u_haric_phase * u_physical_ground) / (u_auric_density + HADES_SLACK);

    vec3 final_color;
    float alpha;

    if (is_sintered > 0.5) {
        // ✅ STONE STATE
        float glow = smoothstep(UNITY_THRESHOLD, 0.95, coherence);
        final_color = mix(COLOR_GOLD, vec3(1.0), glow);
        alpha = (0.6 + (glow * 0.4)) * lift_mask;
    } else {
        // 🌫 VAPOR STATE (Wobble)
        float wobble = sin(u_time * 30.0 + p.x * 20.0) * u_field_remainder * 0.5;
        final_color = COLOR_VAPOR;
        alpha = 0.4 + wobble;
    }

    // Apply Nodal Highlight
    float node_highlight = smoothstep(0.8, 1.0, pattern) * station_influence;
    final_color += vec3(node_highlight);

    gl_FragColor = vec4(final_color, alpha);
}
