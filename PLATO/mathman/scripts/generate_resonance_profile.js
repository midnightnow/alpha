const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// --- Constants & Configuration ---
const SQRT_42 = 6.4807406984;
const SQRT_51 = 7.1414284285;

const ANATOMICAL_LEVELS = [
    { id: 1, name: "Root (Coccyx)", y: 0.0 },
    { id: 2, name: "Sacral (Pubic)", y: 1.2 },
    { id: 3, name: "Solar Plexus (T12)", y: 4.2 },
    { id: 4, name: "Heart (T5)", y: 4.8 },
    { id: 5, name: "Throat (C3)", y: 5.8 },
    { id: 6, name: "Brow (Center Head)", y: 6.5 },
    { id: 7, name: "Crown (Top Head)", y: 7.0 },
];

const DEFAULT_PARAMS = {
    originSeparation: 12.0,
    originCOffset: 12.0,
    scanHeight: 4.2,
    wavelength: 1.0,
    phasePhi: 0,
    phasePsi: 0,
    intensityThreshold: 0.15,
    geometryScale: SQRT_42
};

// --- Physics Engine ---
function computeSnapshot(params) {
    const {
        originSeparation, originCOffset, wavelength,
        phasePhi, phasePsi, scanHeight,
        intensityThreshold
    } = params;

    const k = (2 * Math.PI) / wavelength;
    const phiRad = (phasePhi * Math.PI) / 180;
    const psiRad = (phasePsi * Math.PI) / 180;

    const Ax = -originSeparation / 2;
    const Bx = originSeparation / 2;
    const Cy = originCOffset;

    const nodes = [];
    const resolution = 0.5;

    for (let my = -10; my <= 10; my += resolution) {
        for (let mx = -10; mx <= 10; mx += resolution) {
            const da = Math.sqrt(Math.pow(mx - Ax, 2) + Math.pow(my - 0, 2) + Math.pow(scanHeight, 2));
            const db = Math.sqrt(Math.pow(mx - Bx, 2) + Math.pow(my - 0, 2) + Math.pow(scanHeight, 2));
            const dc = Math.sqrt(Math.pow(mx - 0, 2) + Math.pow(my - Cy, 2) + Math.pow(scanHeight, 2));

            const valA = Math.cos(k * da);
            const valB = Math.cos(k * db + phiRad);
            const valC = Math.cos(k * dc + psiRad);

            const totalI = (valA + valB + valC) / 3;
            const absI = Math.abs(totalI);

            if (absI > intensityThreshold) {
                const region = ANATOMICAL_LEVELS.reduce((prev, curr) => {
                    return (Math.abs(curr.y - my) < Math.abs(prev.y - my) ? curr : prev);
                });

                nodes.push({
                    id: crypto.randomUUID(),
                    x: Number(mx.toFixed(3)),
                    y: Number(my.toFixed(3)),
                    intensity: Number(absI.toFixed(4)),
                    classification: totalI > 0 ? 'constructive' : 'destructive',
                    anatomicalRegion: region.name
                });
            }
        }
    }
    return nodes.sort((a, b) => b.intensity - a.intensity).slice(0, 5000);
}

// --- CLI Handlers ---
function main() {
    const args = process.argv.slice(2);
    const params = { ...DEFAULT_PARAMS };
    let outputFile = 'output.jsonld';

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--wavelength') params.wavelength = parseFloat(args[++i]);
        if (args[i] === '--height') params.scanHeight = parseFloat(args[++i]);
        if (args[i] === '--output') outputFile = args[++i];
    }

    console.log(`Generating profile: λ=${params.wavelength}mm, Y=${params.scanHeight}mm...`);
    const nodes = computeSnapshot(params);

    const dataset = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": `Mathman Profile (λ=${params.wavelength})`,
        "parameters": params,
        "nodalData": nodes,
        "metadata": {
            "timestamp": new Date().toISOString(),
            "engine": "Mathman v2.1.0-cli"
        }
    };

    fs.writeFileSync(outputFile, JSON.stringify(dataset, null, 2));
    console.log(`Success: Exported ${nodes.length} nodes to ${outputFile}`);
}

main();
