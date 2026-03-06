const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// --- Constants & Configuration ---
const SQRT_42 = 6.4807406984;

const CROWN_STATION_PRESET = {
    id: 'preset-crown-sahasrara',
    name: 'Crown Station (Sahasrara)',
    description: 'Optimized for integration-phase resonance at Y: 7.0. Represents the convergence of physical, mental, and spiritual interference maxima.',
    parameters: {
        scanHeight: 7.0,        // Crown anatomical station
        wavelength: 1.0,
        originSeparation: 12.0,
        originCOffset: 12.0,
        intensityThreshold: 0.30,
        rationalCoefficient: 0.73,   // Fine-structure damping (Logos)
        organicCoefficient: 0.571,   // Heptagonal modulation (Pathos)
        geometryScale: SQRT_42,     // Substantiation baseline
        resonanceLock: true
    },
    citation: 'Brennan, B. A. (1993). Light Emerging. Ch. 7; Hecht, E. (2002). Optics. Ch. 9.'
};

// --- Physics Engine ---
function computeSnapshot(params) {
    const {
        originSeparation, originCOffset, wavelength,
        scanHeight, intensityThreshold
    } = params;

    const k = (2 * Math.PI) / wavelength;
    // Assuming 0 phase for standard atlas sweep unless specified
    const phiRad = 0;
    const psiRad = 0;

    const Ax = -originSeparation / 2;
    const Bx = originSeparation / 2;
    const Cy = originCOffset;

    const nodes = [];
    const resolution = 0.2; // Higher resolution for atlas (0.2mm step)

    // Scan 20x20mm field centered at Y=7.0
    for (let my = scanHeight - 5; my <= scanHeight + 5; my += resolution) {
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
                nodes.push({
                    id: crypto.randomUUID(),
                    x: Number(mx.toFixed(3)),
                    y: Number(my.toFixed(3)),
                    intensity: Number(absI.toFixed(4)),
                    classification: totalI > 0 ? 'constructive' : 'destructive',
                    anatomicalRegion: 'Crown'
                });
            }
        }
    }
    return nodes;
}

// --- Sweep Runner ---
async function runCrownStationSweep() {
    const SWEEP_DIR = './samples/crown_atlas';
    if (!fs.existsSync(SWEEP_DIR)) fs.mkdirSync(SWEEP_DIR, { recursive: true });

    console.log("Starting Crown Station (Sahasrara) Resonance Lock Atlas Sweep...");

    // Sweep through a range of wavelengths specifically for the Crown station
    const lambdaRange = [0.85, 0.9, 0.95, 1.0, 1.05, 1.1];

    for (const lambda of lambdaRange) {
        const params = { ...CROWN_STATION_PRESET.parameters, wavelength: lambda };
        console.log(`Generating Crown Atlas: λ=${lambda}mm...`);

        const nodes = computeSnapshot(params);
        const outputFile = path.join(SWEEP_DIR, `crown_resonance_L${lambda}.jsonld`);

        const dataset = {
            "@context": "https://schema.org",
            "@type": "Dataset",
            "name": `Crown Station Resonance Atlas (λ=${lambda})`,
            "description": CROWN_STATION_PRESET.description,
            "citation": CROWN_STATION_PRESET.citation,
            "parameters": params,
            "nodalData": nodes,
            "metadata": {
                "timestamp": new Date().toISOString(),
                "engine": "Mathman Crown-Atlas-v1.0",
                "station": "Crown (Y=7.0)"
            }
        };

        fs.writeFileSync(outputFile, JSON.stringify(dataset, null, 2));

        // Also export a simplified CSV for figure plotting
        const csvFile = path.join(SWEEP_DIR, `crown_resonance_L${lambda}.csv`);
        const csvHeader = "ID,X_mm,Y_mm,Intensity,Classification\n";
        const csvRows = nodes.map(n => `${n.id},${n.x},${n.y},${n.intensity},${n.classification}`).join('\n');
        fs.writeFileSync(csvFile, csvHeader + csvRows);

        console.log(`  Success: Exported ${nodes.length} nodes to ${outputFile} and .csv`);
    }

    console.log(`Crown Station Atlas Sweep Complete. Data saved to ${SWEEP_DIR}.`);
}

runCrownStationSweep();
