import Papa from 'papaparse';

export interface NodeData {
    NodeID: number;
    x: number;
    y: number;
    z: number;
    SymbolicName: string;
    MythologicalMapping: string;
    sector?: number;
}

export const load93Nodes = async (url: string): Promise<NodeData[]> => {
    return new Promise((resolve, reject) => {
        Papa.parse(url, {
            download: true,
            header: true,
            dynamicTyping: true,
            complete: (results) => {
                const nodes = results.data.filter((d: any) => d.NodeID) as NodeData[];

                // Compute sectors based on angular position (8 sectors = 45 degrees each)
                const nodesWithSectors = nodes.map(node => {
                    // Skip Node 1 (Origin) and Node 93 (Seal) for sector mapping calculation if needed, 
                    // but better to map all based on polar coordinates.
                    const angle = Math.atan2(node.y, node.x) * (180 / Math.PI);
                    const normalizedAngle = angle < 0 ? angle + 360 : angle;
                    const sector = Math.floor(normalizedAngle / 45) + 1;
                    return { ...node, sector };
                });

                resolve(nodesWithSectors);
            },
            error: (err) => {
                reject(err);
            }
        });
    });
};
