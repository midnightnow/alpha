export interface PMGNode {
    h3_index: string;
    name: string;
    resonance: number;
    state: 'Resonant' | 'Fractured';
    last_update: number;
}
declare class PlatonicDB {
    private db;
    constructor();
    private init;
    generateNodeName(h3Index: string): string;
    getOrCreateNode(h3Index: string): PMGNode;
    updateResonance(h3Index: string, resonance: number): void;
    private countSetBits;
    getGlobalState(): {
        totalManifestations: {
            count: number;
        };
        resonantCount: {
            count: number;
        };
        fractureCount: {
            count: number;
        };
    };
}
export declare const platonicDB: PlatonicDB;
export {};
