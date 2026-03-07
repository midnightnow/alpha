/**
 * THE FLY-CUTTER (Hysteresis Shaver)
 * Purpose: Shave the 1/12th remainder from the 10-24-26 body 
 * to return the system to the Root 42 / Root 51 base state.
 */

export interface NodePosition {
    x: number;
    y: number;
    z: number;
}

export interface NodeData {
    id: number;
    position: NodePosition;
    tension: number;
    mode: 'SQUARE_CONSTRUCTION' | 'HEX_DECONSTRUCTION';
}

const FLY_CUTTER_RATIO = 1 / 12; // The Zeta function shift
const HYSTERESIS_THRESHOLD = 0.1237; // The Information Leak constant

export function engageFlyCutter(nodeData: NodeData[]): NodeData[] {
    return nodeData.map(node => {
        // 1. Identify the 'Russet' noise (Hysteresis)
        const drift = node.position.z % HYSTERESIS_THRESHOLD;

        // 2. The 'Strike': Apply the negative 1/12th correction
        // This 'shaves' the edge of the square back to the hex-roundness
        const correctedZ = node.position.z - (drift * FLY_CUTTER_RATIO);

        // 3. Reset the Tension 
        // Moving from 90 (Square) to 60 (Hex)
        return {
            ...node,
            position: { ...node.position, z: correctedZ },
            tension: 60,
            mode: 'HEX_DECONSTRUCTION'
        };
    });
}
