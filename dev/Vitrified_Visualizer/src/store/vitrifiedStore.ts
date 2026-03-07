import { create } from 'zustand';

interface NodeData {
    NodeID: number;
    x: number;
    y: number;
    z: number;
    SymbolicName: string;
    MythologicalMapping: string;
    sector?: number;
}

interface VitrifiedState {
    nodes: NodeData[];
    selectedNodeId: number | null;
    selectedNodeIds: number[];
    caliperMode: boolean;
    shavedMode: boolean;
    activeMatches: number[][];
    currentEpoch: number;
    globalRotation: number;
    isLoading: boolean;

    setNodes: (nodes: NodeData[]) => void;
    setSelectedNodeId: (id: number | null) => void;
    setSelectedNodeIds: (ids: number[]) => void;
    setCaliperMode: (active: boolean) => void;
    setShavedMode: (active: boolean) => void;
    setActiveMatches: (matches: number[][]) => void;
    setCurrentEpoch: (epoch: number) => void;
    setGlobalRotation: (rotation: number) => void;
    setIsLoading: (isLoading: boolean) => void;
}

export const useVitrifiedStore = create<VitrifiedState>((set) => ({
    nodes: [],
    selectedNodeId: null,
    selectedNodeIds: [],
    caliperMode: false,
    shavedMode: false,
    activeMatches: [],
    currentEpoch: -3300,
    globalRotation: 0,
    isLoading: true,

    setNodes: (nodes) => set({ nodes }),
    setSelectedNodeId: (id) => set({ selectedNodeId: id }),
    setSelectedNodeIds: (ids) => set({ selectedNodeIds: ids }),
    setCaliperMode: (active) => set({ caliperMode: active }),
    setShavedMode: (active) => set({ shavedMode: active }),
    setActiveMatches: (matches) => set({ activeMatches: matches }),
    setCurrentEpoch: (epoch) => set({ currentEpoch: epoch }),
    setGlobalRotation: (rotation) => set({ globalRotation: rotation }),
    setIsLoading: (isLoading) => set({ isLoading }),
}));
