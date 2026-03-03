/**
 * Vitrification Shader — The Oracle Lens
 * 
 * Implements:
 * 1. The 5-6-7 Wave Stack (Resonance/Chorus/Null)
 * 2. The Optical Pinch (Parabolic focus at Hades Gap)
 * 3. Obsidian Phase Shift (Vitrification based on Salience)
 */

uniform float uTime;
uniform float uSalience; // From Perception.py
uniform vec3 uH3Residency; // 3-bit chunk color mapping
varying vec2 vUv;
varying vec3 vPosition;

void main() {
    // 1. The 5-6-7 Wave Stack
    // Wave 5 (Warning), 6 (Chorus), 7 (Null)
    float wave5 = sin(vPosition.x * 5.0 + uTime * 0.66);
    float wave6 = cos(vPosition.y * 6.0 + uTime * 0.90);
    float wave7 = tan(vPosition.z * 7.0 + uTime * 0.12); // The Hades Gap Torsion

    // 2. The Optical Pinch (Parabolic Lens)
    float distance = length(vUv - 0.5);
    float lens = pow(distance, 2.0) * uSalience;
    
    // 3. Vitrification (Obsidian Shift)
    // As salience increases, the surface "glasses" into obsidian.
    float glassFactor = smoothstep(0.1237, 0.9074, uSalience);
    vec3 obsidian = vec3(0.02, 0.02, 0.03); // Deep PMG obsidian
    vec3 clay = vec3(0.4, 0.3, 0.2);       // Raw clay state
    
    vec3 finalColor = mix(clay, obsidian, glassFactor);
    finalColor += uH3Residency * 0.1; // Sub-surface glow from H3 bits
    
    gl_FragColor = vec4(finalColor + (wave5 * wave6 * wave7 * lens * 0.05), 1.0);
}
