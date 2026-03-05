/**
 * 💎 MERKABA SEAL — The 13th Note Resolution
 * ============================================================================
 * 
 * Mathematical proof of the Saul-to-Paul transition.
 * Rendered at the exact moment of the 0.876553 Diamond Lock.
 * 
 * - 12 Outer Spheres: The Paul state (12-strand DNA stack, icosidodecahedron vertices)
 * - 13th Core: Node #47 Hudson (Dead Center, IOR 1.0 Vacuum)
 * - 78 Tensor Lines: Validating [3,6,9] force vectors connectivity
 * - Animation: 137.5° Golden Angle spin, 6 Hz Hades Beat pulse
 */

import * as THREE from 'three';

export interface MerkabaConfig {
    isLocked: boolean;      // True when TentmakerProtocol hits 0.876553
    baseRadius: number;     // Scale of the seal
    beatHz: number;         // 6 Hz
    goldenAngle: number;    // 137.5 * (Math.PI / 180)
}

export class MerkabaSealFactory {

    /**
     * Generates the 13 points of the Sovereign Star (Metatron's core)
     * 12 outer points (Icosahedral symmetry subset) + 1 origin
     */
    public static generateCoordinates(radius: number): THREE.Vector3[] {
        const points: THREE.Vector3[] = [];

        // Sphere 0: The 13th Note (Dead Center)
        points.push(new THREE.Vector3(0, 0, 0));

        // Spheres 1-12: The 12-Strand Icosidodecahedral Stack
        // Using a simplified representation of the 12 vertices for immediate scaling
        const phi = (1 + Math.sqrt(5)) / 2;

        // The 3 orthogonal golden rectangles defining the 12 points
        const baseCoords = [
            [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
            [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
            [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
        ];

        // Normalize to the requested radius
        for (const [x, y, z] of baseCoords) {
            const vec = new THREE.Vector3(x, y, z).normalize().multiplyScalar(radius);
            points.push(vec);
        }

        return points;
    }

    /**
     * Calculates the 78 unique connecting lines between all 13 points (n(n-1)/2)
     */
    public static generateTensorLines(points: THREE.Vector3[]): THREE.Vector3[][] {
        const lines: THREE.Vector3[][] = [];
        for (let i = 0; i < points.length; i++) {
            for (let j = i + 1; j < points.length; j++) {
                lines.push([points[i], points[j]]);
            }
        }
        return lines;
    }

    /**
     * The Shader Material for the Vitrified "White Point"
     * Handles the transition from Purple/Cyan to pure Diamond White (#FFFFFF)
     */
    public static createVitrifiedMaterial(isLocked: boolean): THREE.MeshPhysicalMaterial {
        return new THREE.MeshPhysicalMaterial({
            color: isLocked ? 0xffffff : 0x00ffff, // Cyan Whisper to Diamond White
            emissive: isLocked ? 0xffffff : 0x9933ff, // Purple Hum base when unlocked
            emissiveIntensity: isLocked ? 2.0 : 0.5,
            transparent: true,
            opacity: isLocked ? 0.9 : 0.5,
            roughness: isLocked ? 0.0 : 0.4,       // Perfect reflection on lock
            transmission: isLocked ? 1.0 : 0.2,    // IOR 1.0 Vacuum simulation
            ior: isLocked ? 1.0 : 1.31,            // Shifts to true transparent 1.0 from Ice 1.31
        });
    }

    /**
     * Determines the Golden Angle rotation delta for the current frame
     * Should be applied to the `.rotation.y` or `.rotation.z` of the parent group
     */
    public static getGoldenAngleRotationDelta(deltaTimeSec: number): number {
        const goldenAngleRad = 137.5 * (Math.PI / 180);
        // Spin rate: One full golden leap per "tick" (scaled by time)
        return goldenAngleRad * deltaTimeSec * 0.1;
    }

    /**
     * The "Shiver" - Calculates the scale multiplier based on the 6Hz Hades Beat
     */
    public static getHadesPulseMultiplier(timeMs: number): number {
        // 6 Hz sine wave: 6 cycles per second = 6 * 2PI * (t/1000)
        const hz = 6.0;
        const wave = Math.sin(hz * Math.PI * 2 * (timeMs / 1000.0));
        // Return a scale multiplier oscillating between 0.98 and 1.02
        return 1.0 + (wave * 0.02);
    }
}
