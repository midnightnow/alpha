import { NodeData } from '../utils/coordinateLoader';

export interface RatioEntry {
    pair: [number, number];
    radialRatio: number;
    angularDist: number;
}

export const generateRatioLookup = (nodes: NodeData[]): RatioEntry[] => {
    const table: RatioEntry[] = [];
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const n1 = nodes[i]!;
            const n2 = nodes[j]!;

            // Radial lengths from origin
            const d1 = Math.sqrt(n1.x ** 2 + n1.y ** 2 + n1.z ** 2);
            const d2 = Math.sqrt(n2.x ** 2 + n2.y ** 2 + n2.z ** 2);

            // Protect against division by zero (Node 1 is at origin)
            const minD = Math.min(d1, d2);
            const maxD = Math.max(d1, d2);
            const radialRatio = minD > 0 ? maxD / minD : maxD;

            // Angular distance (dot product of unit vectors)
            const v1 = [n1.x, n1.y, n1.z];
            const v2 = [n2.x, n2.y, n2.z];
            const dot = (v1[0]! * v2[0]! + v1[1]! * v2[1]! + v1[2]! * v2[2]!) / (d1 * d2);
            const angularDist = Math.acos(Math.max(-1, Math.min(1, dot))) * (180 / Math.PI);

            table.push({
                pair: [n1.NodeID, n2.NodeID],
                radialRatio,
                angularDist
            });
        }
    }
    return table;
};
