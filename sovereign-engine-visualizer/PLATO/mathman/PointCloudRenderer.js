
/**
 * PointCloudRenderer.js
 * Phase 4: Volumetric Materialization of the Oracle Grid
 * 
 * Lofts the 2D H3 Hexagonal Mesh into a 3D Point Cloud.
 * Z-Axis = Karma Coherence (High Stagnation = Low Z, High Flow = High Z)
 */

class PointCloudRenderer {
    constructor(containerId, origins) {
        this.container = document.getElementById(containerId);
        this.origins = origins;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.domElement.style.position = 'absolute';
        this.renderer.domElement.style.top = '0';
        this.renderer.domElement.style.left = '0';
        this.renderer.domElement.style.pointerEvents = 'none'; // Let clicks pass through to UI
        this.renderer.domElement.id = 'three-canvas';

        // Check if canvas already exists to avoid duplicates
        if (!document.getElementById('three-canvas')) {
            this.container.appendChild(this.renderer.domElement);
        }

        this.points = null;
        this.geometry = null;

        // Camera Positioning (Isometric-ish)
        this.camera.position.z = 20;
        this.camera.position.y = -10;
        this.camera.rotation.x = 0.5;

        this.clock = new THREE.Clock();

        // Fog for depth cues (Auric Mucus Fog)
        this.scene.fog = new THREE.FogExp2(0x0a0a12, 0.02);

        this.animate = this.animate.bind(this);
    }

    /**
     * Updates the Point Cloud based on the current H3 Grid State
     * @param {Array} hexData Array of { hex, density, intensity }
     */
    updateCloud(hexData) {
        if (this.points) {
            this.scene.remove(this.points);
            this.geometry.dispose();
        }

        const vertices = [];
        const colors = [];
        const sizes = [];

        const colorFlow = new THREE.Color(0x00f2ff); // Cyber Blue (Flow)
        const colorStagnation = new THREE.Color(0xff4400); // Rust (Stagnation)

        hexData.forEach(data => {
            const { hex, density } = data;

            // MATH: H3 Geo -> 3D Vector
            // We use the H3 center as the (x,y) anchor
            const hexCenter = h3.cellToLatLng(hex);
            const scale = 0.5; // Scale to fit camera view

            // Z-AXIS LOFTING: The Core Physics
            // High Density (Mucus) = Low Z (Sink)
            // Low Density (Flow) = High Z (Loft)
            // Range: -5.0 to +5.0
            const z = (0.5 - density) * 10.0;

            const x = (hexCenter[1]) * scale * 2.0; // Longitude -> X
            const y = (hexCenter[0]) * scale * 2.0; // Latitude -> Y

            vertices.push(x, y, z);

            // COLOR MAPPING
            // Lerp between Rust and Cyber based on density
            const mixedColor = colorFlow.clone().lerp(colorStagnation, density);
            colors.push(mixedColor.r, mixedColor.g, mixedColor.b);

            // SIZE MAPPING
            // Stagnant nodes are heavy/large, Flow nodes are light/small
            sizes.push(density * 0.5 + 0.1);
        });

        this.geometry = new THREE.BufferGeometry();
        this.geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        this.geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        this.geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));

        // Shader Material for Glowing Points
        const material = new THREE.PointsMaterial({
            size: 0.5,
            vertexColors: true,
            map: this.createSprite(),
            blending: THREE.AdditiveBlending,
            depthTest: false,
            transparent: true,
            opacity: 0.8
        });

        this.points = new THREE.Points(this.geometry, material);
        this.scene.add(this.points);
    }

    createSprite() {
        const canvas = document.createElement('canvas');
        canvas.width = 32;
        canvas.height = 32;
        const context = canvas.getContext('2d');
        const gradient = context.createRadialGradient(16, 16, 0, 16, 16, 16);
        gradient.addColorStop(0, 'rgba(255,255,255,1)');
        gradient.addColorStop(0.2, 'rgba(255,255,255,0.8)');
        gradient.addColorStop(0.5, 'rgba(255,255,255,0.2)');
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        context.fillStyle = gradient;
        context.fillRect(0, 0, 32, 32);
        const texture = new THREE.Texture(canvas);
        texture.needsUpdate = true;
        return texture;
    }

    animate() {
        requestAnimationFrame(this.animate);

        // Gentle Rotation (The Universe Spins)
        if (this.points) {
            this.points.rotation.z += 0.001;
        }

        this.renderer.render(this.scene, this.camera);
    }

    start() {
        this.animate();
    }
}

// Global Export
window.PointCloudRenderer = PointCloudRenderer;
