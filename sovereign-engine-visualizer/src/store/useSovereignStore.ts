import { create } from 'zustand';

const SOVEREIGN_CONSTANTS = {
    PHI: 1.618,
    ZENITH_WEALTH: Math.pow(1.618, 2), // phi squared
    ARCS: {
        DIAMONDS: { start: 14, end: 26 },
        CLUBS: { start: 27, end: 39 },
    },
};

interface SovereignState {
    isSimulating: boolean;
    currentWeek: number;
    arc: 'DIAMONDS' | 'CLUBS' | 'NONE';
    amplitude: number;
    entropy: number;
    lockStatus: number;
    isSealed: boolean;
    hadesValue: number;
    activeArchive: number | null;
    showMergedStream: boolean; // ADDED
    showOpticalOverlay: boolean; // ADDED
    activePayload: any | null; // ADDED
    fractalZoom: number; // 0.0 to 1.0 (ADDED)
    seedResonance: number; // √10 resonance (ADDED)
    worldResonance: number; // 10 resonance (ADDED)
    setHadesValue: (val: number) => void;
    setFractalZoom: (val: number) => void; // (ADDED)
    setActiveArchive: (tick: number | null) => void;
    setShowMergedStream: (val: boolean) => void; // ADDED
    setShowOpticalOverlay: (val: boolean) => void; // ADDED
    ingestPayload: (payload: any) => void; // ADDED
    startSimulation: () => void;
    nextWeek: () => void;
    jumpToZenith: () => void;
}

export const useSovereignStore = create<SovereignState>((set) => ({
    isSimulating: false,
    currentWeek: 0,
    arc: 'NONE',
    amplitude: 0,
    entropy: 100,
    lockStatus: 0,
    isSealed: false,
    hadesValue: 0.037, // Default Operating Temp
    activeArchive: null,
    showMergedStream: true, // Default to merged
    showOpticalOverlay: false, // Default hidden
    activePayload: null,
    fractalZoom: 0.0, // Added
    seedResonance: 0, // Added
    worldResonance: 0, // Added
    setHadesValue: (val) => set({ hadesValue: val }),
    setFractalZoom: (val) => set((state) => {
        const root10 = Math.sqrt(10); // 3.1622
        const manifest10 = 10;
        // Map 0-1 zoom to scale 1-10
        const currentScale = 1 + val * 9;

        const seedResonance = 1 / (1 + Math.abs(currentScale - root10));
        const worldResonance = 1 / (1 + Math.abs(currentScale - manifest10));

        return {
            fractalZoom: val,
            seedResonance,
            worldResonance
        };
    }),
    setActiveArchive: (tick) => set({ activeArchive: tick }),
    setShowMergedStream: (val) => set({ showMergedStream: val }),
    setShowOpticalOverlay: (val) => set({ showOpticalOverlay: val }),
    ingestPayload: (payload) => set({ activePayload: payload, entropy: 93, isSimulating: true }),
    startSimulation: () => set({
        isSimulating: true,
        currentWeek: 14,
        arc: 'DIAMONDS',
        amplitude: 1.0,
        entropy: 42,
        lockStatus: 12,
        isSealed: false
    }),
    nextWeek: () => set((state) => {
        const nextW = (state.currentWeek + 1) % 53;
        const { PHI, ZENITH_WEALTH, ARCS } = SOVEREIGN_CONSTANTS;

        let arc: 'DIAMONDS' | 'CLUBS' | 'NONE' = 'NONE';
        let amp = 0;

        if (nextW >= ARCS.DIAMONDS.start && nextW <= ARCS.DIAMONDS.end) {
            arc = 'DIAMONDS';
            amp = Math.pow(PHI, (nextW - ARCS.DIAMONDS.start) / 6);
        } else if (nextW >= ARCS.CLUBS.start && nextW <= ARCS.CLUBS.end) {
            arc = 'CLUBS';
            const k = nextW - ARCS.CLUBS.start;
            amp = ZENITH_WEALTH * Math.pow(Math.sin((Math.PI * k) / 12), 2);
        }

        const entropy = Math.max(0, 42 - (nextW * 0.8) + (arc === 'CLUBS' ? 5 : 0));
        const lockStatus = Math.min(100, (nextW / 33) * 100);
        const isSealed = nextW === 33;

        return {
            currentWeek: nextW,
            arc,
            amplitude: amp,
            entropy,
            lockStatus,
            isSealed
        };
    }),
    jumpToZenith: () => set({
        currentWeek: 26,
        arc: 'DIAMONDS',
        amplitude: SOVEREIGN_CONSTANTS.ZENITH_WEALTH,
        entropy: 12.37,
        lockStatus: 78.8,
        isSealed: false
    }),
}));
