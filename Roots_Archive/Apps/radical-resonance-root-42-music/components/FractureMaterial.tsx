import * as THREE from 'three';
import { shaderMaterial } from '@react-three/drei';
import { extend } from '@react-three/fiber';

// --- SHADER CODE ---

const vertexShader = `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  
  uniform float uTime;
  uniform float uDistortion;
  uniform float uAudioLow;
  
  // Simplex noise function
  vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 permute(vec4 x) { return mod289(((x*34.0)+1.0)*x); }
  vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }
  
  float snoise(vec3 v) {
    const vec2  C = vec2(1.0/6.0, 1.0/3.0) ;
    const vec4  D = vec4(0.0, 0.5, 1.0, 2.0);
    
    // First corner
    vec3 i  = floor(v + dot(v, C.yyy) );
    vec3 x0 = v - i + dot(i, C.xxx) ;
    
    // Other corners
    vec3 g = step(x0.yzx, x0.xyz);
    vec3 l = 1.0 - g;
    vec3 i1 = min( g.xyz, l.zxy );
    vec3 i2 = max( g.xyz, l.zxy );
    
    vec3 x1 = x0 - i1 + C.xxx;
    vec3 x2 = x0 - i2 + C.yyy; // 2.0*C.x = 1/3 = C.y
    vec3 x3 = x0 - D.yyy;      // -1.0+3.0*C.x = -0.5 = -D.y
    
    // Permutations
    i = mod289(i); 
    vec4 p = permute( permute( permute( 
               i.z + vec4(0.0, i1.z, i2.z, 1.0 ))
             + i.y + vec4(0.0, i1.y, i2.y, 1.0 )) 
             + i.x + vec4(0.0, i1.x, i2.x, 1.0 ));
             
    // Gradients: 7x7 points over a square, mapped onto an octahedron.
    // The ring size 17*17 = 289 is close to a multiple of 49 (49*6 = 294)
    float n_ = 0.142857142857; // 1.0/7.0
    vec3  ns = n_ * D.wyz - D.xzx;
    
    vec4 j = p - 49.0 * floor(p * ns.z * ns.z);  //  mod(p,7*7)
    
    vec4 x_ = floor(j * ns.z);
    vec4 y_ = floor(j - 7.0 * x_ );    // mod(j,N)
    
    vec4 x = x_ *ns.x + ns.yyyy;
    vec4 y = y_ *ns.x + ns.yyyy;
    vec4 h = 1.0 - abs(x) - abs(y);
    
    vec4 b0 = vec4( x.xy, y.xy );
    vec4 b1 = vec4( x.zw, y.zw );
    
    vec4 s0 = floor(b0)*2.0 + 1.0;
    vec4 s1 = floor(b1)*2.0 + 1.0;
    vec4 sh = -step(h, vec4(0.0));
    
    vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy ;
    vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww ;
    
    vec3 p0 = vec3(a0.xy,h.x);
    vec3 p1 = vec3(a0.zw,h.y);
    vec3 p2 = vec3(a1.xy,h.z);
    vec3 p3 = vec3(a1.zw,h.w);
    
    //Normalise gradients
    vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2, p2), dot(p3,p3)));
    p0 *= norm.x;
    p1 *= norm.y;
    p2 *= norm.z;
    p3 *= norm.w;
    
    // Mix final noise value
    vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 42.0 * dot( m*m, vec4( dot(p0,x0), dot(p1,x1), 
                                  dot(p2,x2), dot(p3,x3) ) );
  }

  void main() {
    vUv = uv;
    vNormal = normal;
    vPosition = position;
    
    // Displacement based on audio low freq (kick)
    float displacement = snoise(position * 2.0 + uTime * 0.5) * (uAudioLow * 0.5 + uDistortion * 0.2);
    
    vec3 newPosition = position + normal * displacement;
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
  }
`;

const fragmentShader = `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  
  uniform float uTime;
  uniform float uAudioHigh;
  uniform float uAudioMid;
  uniform float uFracture; // 0.0 to 1.0
  uniform float uDistortion; // Overpack Delta Proxy
  uniform float uResolution; // 0.0 (Interference) to 1.0 (Resolution)
  uniform sampler2D uLogoTexture;
  uniform float uHasLogo;
  
  // Voronoi / Cellular Noise
  vec2 hash2( vec2 p ) {
      return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
  }

  float voronoi( in vec2 x ) {
      vec2 n = floor(x);
      vec2 f = fract(x);
      float m = 8.0;
      for( int j=-1; j<=1; j++ )
      for( int i=-1; i<=1; i++ ) {
          vec2 g = vec2( float(i), float(j) );
          vec2 o = hash2( n + g );
          o = 0.5 + 0.5*sin( uTime + 6.2831*o );
          vec2 r = g + o - f;
          float d = dot(r,r);
          if( d<m ) m=d;
      }
      return m;
  }

  void main() {
    // Base color (Deep Void Blue/Purple)
    vec3 baseColor = vec3(0.02, 0.0, 0.05);
    
    // Voronoi Pattern for Fracture Lines
    float v = voronoi(vUv * (10.0 + uFracture * 20.0) + uTime * 0.1);
    float edge = smoothstep(0.05, 0.02, v);
    
    // --- MAX COOPER REFRACTOR LOGIC ---
    // Chromatic Aberration driven by Overpack Delta (uDistortion)
    // Optimized: Use derivatives to approximate offset instead of re-calculating Voronoi 3 times
    
    float separation = uDistortion * 0.05; // Scale factor
    
    // Calculate gradients of the voronoi field
    float dx = dFdx(v);
    float dy = dFdy(v);
    
    // Approximate R and B channels using the gradient
    // v(uv + offset) ~= v(uv) + grad(v) . offset
    // We offset R by +separation in X, and B by -separation in X
    
    float vR = v + dx * separation * 100.0; // Scale up gradient effect
    float vG = v;
    float vB = v - dx * separation * 100.0;
    
    vec3 abberationColor = vec3(
        smoothstep(0.05, 0.02, vR),
        smoothstep(0.05, 0.02, vG),
        smoothstep(0.05, 0.02, vB)
    );
    
    // "Purple Hum" Bioluminescent Glow
    // Reacts to Mid frequencies (Wobble)
    float wobble = uAudioMid * 2.0 + 0.5;
    vec3 glowColor = vec3(0.6, 0.2, 1.0);
    
    // Mix based on fracture intensity
    vec3 finalColor = mix(baseColor, glowColor * abberationColor, uFracture * 0.8 + 0.2);
    
    // --- LOGO INJECTION ---
    if (uHasLogo > 0.5) {
        // Distort UV for logo based on fracture/distortion
        float shear = uDistortion * 0.05; // Scale with distortion
        vec2 distortedUV = vUv + vec2(sin(vUv.y * 10.0 + uTime) * shear, 0.0);
        
        vec4 logo = texture2D(uLogoTexture, distortedUV);
        
        // Logo glows with "Purple Hum"
        vec3 purpleCore = vec3(0.6, 0.2, 1.0);
        
        // Pulse with 66Hz (approx)
        float pulse = 1.0 + 0.5 * sin(uTime * 66.0);
        
        // Emission intensity increases with fracture
        float emissionIntensity = logo.r * (uFracture * 2.0 + 0.5) * pulse; // Use red channel as mask
        
        finalColor += purpleCore * emissionIntensity;
    }
    
    // Add "Sparkle" from High Freqs
    float sparkle = step(0.98, fract(sin(dot(vUv, vec2(12.9898, 78.233))) * 43758.5453 + uTime * 10.0));
    finalColor += vec3(1.0) * sparkle * uAudioHigh;
    
    // Add Rim Light effect
    float rim = 1.0 - dot(vNormal, vec3(0.0, 0.0, 1.0));
    finalColor += vec3(0.5, 0.8, 1.0) * pow(rim, 4.0) * 0.5;

    gl_FragColor = vec4(finalColor, 0.8); // Slightly transparent
  }
`;

const FractureMaterial = shaderMaterial(
  {
    uTime: 0,
    uDistortion: 0,
    uAudioLow: 0,
    uAudioMid: 0,
    uAudioHigh: 0,
    uFracture: 0,
    uLogoTexture: null,
    uHasLogo: 0
  },
  vertexShader,
  fragmentShader
);

extend({ FractureMaterial });

export { FractureMaterial };
