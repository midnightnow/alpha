import { PMG_CONSTANTS } from "../constants";
import * as THREE from "three";

export interface Vertex {
    id: string;
    coordinates: THREE.Vector3;
    resonance: number;
    dimension: number;
}

export interface GeometricLayer {
    dimension: number;
    vertices: Vertex[];
    consistencyHash: string;
    timestamp: number;
}

export interface DriftReport {
    id: string;
    cancellationDepth: number;
    shearDrift: number;
    isStable: boolean;
}

/**
 * MathmanConsistency: The guardian of the escape sequences.
 * Enforces the Non-Decay Principle and cumulative vitrification.
 */
export class MathmanConsistency {
    private registry: Map<number, GeometricLayer> = new Map();

    /**
     * Vitrifies a layer, ensuring no data from previous layers is lost.
     * New layers must be additive (vitrification) rather than destructive (cancellation).
     */
    public vitrifyLayer(dimension: number, vertices: Vertex[]): boolean {
        const previousLayer = this.registry.get(dimension - 1);

        if (previousLayer) {
            const report = this.auditLayerTransition(previousLayer, vertices);
            if (!report.isStable) {
                console.error(`DECAY_DETECTED in Dimension ${dimension}:`, report);
                return false;
            }
        }

        // Apply Hardcard Remainder Logic: Additive resonance instead of decay
        const vitrifiedVertices = vertices.map((v) => ({
            ...v,
            resonance: v.resonance + PMG_CONSTANTS.OVERPACK_DELTA,
            dimension: dimension,
        }));

        const layer: GeometricLayer = {
            dimension,
            vertices: vitrifiedVertices,
            consistencyHash: this.generateConsistencyHash(vitrifiedVertices),
            timestamp: Date.now(),
        };

        this.registry.set(dimension, layer);
        return true;
    }

    /**
     * Generates a hash based on the current vertex state to lock history.
     */
    private generateConsistencyHash(vertices: Vertex[]): string {
        const data = vertices.map(v => `${v.id}:${v.resonance.toFixed(6)}`).join('|');
        // Simple string hash for demonstration; in production use a crypto hash
        let hash = 0;
        for (let i = 0; i < data.length; i++) {
            const char = data.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash |= 0;
        }
        return hash.toString(16);
    }

    /**
     * Audits the transition between dimensions to detect data loss or shear drift.
     */
    private auditLayerTransition(prev: GeometricLayer, current: Vertex[]): { isStable: boolean; issues: string[] } {
        const issues: string[] = [];

        // 1. Vertex Retention Check
        prev.vertices.forEach(p => {
            const exists = current.some(c => c.id === p.id);
            if (!exists) {
                issues.push(`Vertex ${p.id} lost in transition.`);
            }
        });

        // 2. Structural Bracing Check (10-24-26 Alignment)
        const expectedRadii = PMG_CONSTANTS.BRACING_TRIAD;
        current.forEach(v => {
            const dist = v.coordinates.length();
            const layerIdx = v.dimension - 1;
            if (layerIdx >= 0 && layerIdx < 3) {
                const delta = Math.abs(dist - expectedRadii[layerIdx]);
                if (delta > PMG_CONSTANTS.HADES_GAP) {
                    issues.push(`Structural SLOP detected in Layer ${v.dimension}: Drift = ${delta.toFixed(4)}`);
                }
            }
        });

        // 3. Heart Pulse Audit (6.41418066 Range)
        const heartFreq = PMG_CONSTANTS.HEART_FREQUENCY;
        if (Math.abs(heartFreq - 6.41418066) > 0.0001) {
            issues.push(`HEART_DECAY: Pulse frequency ${heartFreq} drifts from bounded sequence.`);
        }

        return {
            isStable: issues.length === 0,
            issues
        };
    }

    public getLayer(dimension: number): GeometricLayer | undefined {
        return this.registry.get(dimension);
    }

    public getFullRegistry(): Map<number, GeometricLayer> {
        return this.registry;
    }
}
