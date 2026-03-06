export enum GlyphType {
    STRUT = 'STRUT',
    LOOP = 'LOOP',
    HINGE = 'HINGE',
    ACTUATOR = 'ACTUATOR'
}

export interface GlyphProperties {
    type: GlyphType;
    lift: number;
    rigidity: number;
}

export const MECHANICAL_ALPHABET: Record<string, GlyphProperties> = {
    // === STRUTS (Vectors): Linear momentum carriers ===
    "t": { type: GlyphType.STRUT, lift: 0.5, rigidity: 0.9 },
    "l": { type: GlyphType.STRUT, lift: 0.5, rigidity: 0.8 },
    "z": { type: GlyphType.STRUT, lift: 0.5, rigidity: 0.85 },
    "d": { type: GlyphType.STRUT, lift: 0.5, rigidity: 0.9 },
    "k": { type: GlyphType.STRUT, lift: 0.5, rigidity: 0.85 },
    "m": { type: GlyphType.STRUT, lift: 0.5, rigidity: 0.75 },
    "n": { type: GlyphType.STRUT, lift: 0.5, rigidity: 0.7 },

    // === LOOPS (Vowels/Rotors): Buoyancy expanders ===
    "o": { type: GlyphType.LOOP, lift: 1.2, rigidity: 0.2 },
    "e": { type: GlyphType.LOOP, lift: 1.2, rigidity: 0.3 },
    "a": { type: GlyphType.LOOP, lift: 1.2, rigidity: 0.25 },
    "u": { type: GlyphType.LOOP, lift: 1.2, rigidity: 0.3 },
    "i": { type: GlyphType.LOOP, lift: 1.2, rigidity: 0.28 },
    "y": { type: GlyphType.LOOP, lift: 1.0, rigidity: 0.35 },

    // === HINGES (Fricatives/Joiners): Coherence dampers ===
    "j": { type: GlyphType.HINGE, lift: 0.8, rigidity: 0.4 },
    "s": { type: GlyphType.HINGE, lift: 0.8, rigidity: 0.35 },
    "x": { type: GlyphType.HINGE, lift: 0.8, rigidity: 0.5 },
    "f": { type: GlyphType.HINGE, lift: 0.8, rigidity: 0.38 },
    "v": { type: GlyphType.HINGE, lift: 0.8, rigidity: 0.42 },
    "h": { type: GlyphType.HINGE, lift: 0.7, rigidity: 0.3 },
    "w": { type: GlyphType.HINGE, lift: 0.9, rigidity: 0.45 },

    // === ACTUATORS (Stops/Force): Rigidity clampers ===
    "b": { type: GlyphType.ACTUATOR, lift: 1.5, rigidity: 0.6 },
    "p": { type: GlyphType.ACTUATOR, lift: 1.5, rigidity: 0.55 },
    "r": { type: GlyphType.ACTUATOR, lift: 1.5, rigidity: 0.6 },
    "g": { type: GlyphType.ACTUATOR, lift: 1.4, rigidity: 0.65 },
    "c": { type: GlyphType.ACTUATOR, lift: 1.5, rigidity: 0.7 },
    "q": { type: GlyphType.ACTUATOR, lift: 1.6, rigidity: 0.75 }
};

export const calculatePhoneticTorque = (word: string) => {
    const cleanWord = word.toLowerCase().replace(/[^a-z]/g, '');
    let totalTorque = 0;
    let totalRigidity = 0;
    let count = 0;

    for (const char of cleanWord) {
        const glyph = MECHANICAL_ALPHABET[char];
        if (glyph) {
            totalTorque += glyph.lift * glyph.rigidity;
            totalRigidity += glyph.rigidity;
            count++;
        }
    }

    const avgRigidity = count > 0 ? totalRigidity / count : 0;

    // Classify word
    let structuralClass = 'VAPOR';
    if (avgRigidity > 0.7) structuralClass = 'STONE';
    else if (avgRigidity > 0.5) structuralClass = 'HYBRID';
    else if (avgRigidity > 0.3) structuralClass = 'FIELD';

    return {
        totalTorque,
        avgRigidity,
        structuralClass,
        glyphCount: count
    };
};
