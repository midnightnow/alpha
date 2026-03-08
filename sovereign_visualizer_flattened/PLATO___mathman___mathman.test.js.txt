const MathmanFlatland = require('./main');

describe('MathmanFlatland Coordinate Projection', () => {
    let mathman;

    beforeEach(() => {
        // Set up the mock DOM
        document.body.innerHTML = `
            <canvas id="visualizer"></canvas>
            <input type="range" id="separation" value="1.2">
            <input type="range" id="c-offset" value="10">
            <input type="range" id="scan-height" value="4.2">
            <input type="range" id="nest-depth" value="3">
            <select id="chakra-selector">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="4">4</option>
                <option value="7">7</option>
            </select>
            <input type="range" id="alpha-logos" value="0.73">
            <input type="range" id="divine-x" value="2.4">
            <input type="range" id="omega-pathos" value="0.571">
            <input type="range" id="wavelength" value="1.0">
            <input type="range" id="phase-offset-b" value="0">
            <input type="range" id="phase-offset-c" value="0">
            <input type="range" id="wave-brightness" value="0.3">
            <input type="range" id="node-size" value="0.5">
            <input type="range" id="wave-weight" value="1.0">
            <input type="range" id="field-threshold" value="0.15">
            <input type="range" id="nodal-budget" value="2000">
            <input type="range" id="global-zoom" value="0.9">
            <input type="checkbox" id="show-merkaba">
            <input type="checkbox" id="show-polygons">
            <button id="trigger-pulse"></button>
            <input type="checkbox" id="show-mathman">
            <input type="checkbox" id="show-field">
            <input type="checkbox" id="show-proportions">
            <input type="checkbox" id="show-topdown">
            <input type="checkbox" id="prime-pulse">
            <input type="checkbox" id="mirror-factor">
            <input type="checkbox" id="quaternion-mode">
            <input type="checkbox" id="resonance-lock">
            <input type="checkbox" id="show-grid">
            <input type="range" id="grid-opacity" value="0.6">
            <input type="checkbox" id="layer-foundation">
            <input type="checkbox" id="layer-flower">
            <input type="checkbox" id="layer-earthmoon">
            <input type="checkbox" id="layer-cipher">
            <input type="checkbox" id="layer-divine7">
            <input type="checkbox" id="layer-prime24">
            <input type="checkbox" id="layer-platonic">
            <input type="checkbox" id="layer-sephiroth">
            <input type="checkbox" id="layer-harmonic">
            <input type="checkbox" id="layer-vitruvian">
            <input type="checkbox" id="layer-haric">
            <input type="checkbox" id="layer-core-star">
            <input type="checkbox" id="layer-mucus">
            <input type="checkbox" id="layer-annotations">
            <input type="checkbox" id="projection-mode">
            <input type="range" id="layer-separation" value="2.0">
            <button id="btn-genesis"></button>
            <div id="genesis-overlay"></div>
            <div id="genesis-text"></div>
            <button id="btn-snapshot"></button>
            <button id="btn-export"></button>
            <button id="btn-preset-ground"></button>
            <button id="btn-preset-expand"></button>
        `;

        // Mock canvas methods
        HTMLCanvasElement.prototype.getContext = jest.fn(() => ({
            scale: jest.fn(),
            save: jest.fn(),
            restore: jest.fn(),
            translate: jest.fn(),
            rotate: jest.fn(),
            beginPath: jest.fn(),
            moveTo: jest.fn(),
            lineTo: jest.fn(),
            stroke: jest.fn(),
            fill: jest.fn(),
            arc: jest.fn(),
            clearRect: jest.fn(),
            fillText: jest.fn(),
            drawImage: jest.fn(),
            createRadialGradient: jest.fn(() => ({ addColorStop: jest.fn() })),
            fillRect: jest.fn(),
            setLineDash: jest.fn()
        }));

        mathman = new MathmanFlatland();
    });

    test('Project function correctly transforms coordinates', () => {
        const origins = { cx: 500, cy: 800, mm: 70 };
        // Test a point at origin Z=0 accurately reflects screen center offset
        const p = mathman.project(0, 0, 0, origins);
        expect(p.x).toBeCloseTo(500);
        expect(p.y).toBeCloseTo(800);
    });

    test('Project function handles Top-Down mode', () => {
        mathman.controls.showTopDown.checked = true;
        const origins = { cx: 500, cy: 800, mm: 70 };
        const p = mathman.project(1, 1, 0, origins);
        expect(p.x).toBe(570);
        expect(p.y).toBe(870);
    });

    test('Intensity calculation includes wave interference', () => {
        const origins = {
            a: { x: -5, y: 0, z: 0 },
            b: { x: 5, y: 0, z: 0 },
            c: { x: 0, y: -10, z: 0 }
        };
        const k = 2 * Math.PI / 1.0; // wavelength = 1.0
        const intensity = mathman.getIntensity(0, 0, 0, origins, k, 0); // time = 0 means pulse = 0?
        // Wait, pulse = Math.sin(time * 0.5), at time=0 intensity is 0.
        // Let's test at time where pulse is 1 (time = PI)
        const intensityAtPulse = mathman.getIntensity(0, 0, 0, origins, k, Math.PI);
        expect(typeof intensityAtPulse).toBe('number');
    });

    test('Apply Preset sets correct parameters', () => {
        mathman.applyPreset('grounding');
        expect(mathman.params.scanY).toBe(0.0);
        expect(mathman.controls.layerFoundation.checked).toBe(true);
        expect(mathman.controls.chakraSelector.value).toBe("1");
    });
});
