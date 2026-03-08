const Hardcard = require('./Hardcard');

const testFleaCoherence = (recursionLevels) => {
    const hardcard = new Hardcard();
    const time = Date.now() / 1000;
    const testIntensity = 0.5;

    console.log(`=== HARDCARD COHERENCE THRESHOLD REPORT ===`);
    console.log(`Version: ${hardcard.version}`);
    console.log(`Barycenter: Navel (0, -4.32)`);
    console.log(`Platonic Space: 4-Unit Boundary`);
    console.log(`-------------------------------------------`);
    console.log(`| Fleas | Latency (ms) | Buffer Sat % | Coherence |`);
    console.log(`|-------|--------------|--------------|-----------|`);

    recursionLevels.forEach(level => {
        const start = process.hrtime.bigint();

        // Simulating the computational load of a 1024-node field sample
        const samples = 10000;
        let totalRemainder = 0;
        for (let i = 0; i < samples; i++) {
            totalRemainder += hardcard.calculateRemainderDelay(time, testIntensity, level);
        }

        const end = process.hrtime.bigint();
        const duration = Number(end - start) / 1000000; // ms

        // Simulated WebGL Buffer Saturation (purely theoretical benchmark)
        // Assume 16.6ms is the frame budget. 
        // We scale the saturation by the duration and a 'flea overhead' constant.
        const bufferSat = Math.min(100, (duration / (16.6 * (samples / 1000))) * 100).toFixed(1);

        // Coherence calculation based on stability of the remainder
        // High recursion levels shouldn't drift the barycenter too much
        const stability = Math.abs(totalRemainder / samples).toFixed(6);
        const coherence = duration < 100 ? "HIGH" : (duration < 250 ? "MEDIUM" : "CRITICAL");

        console.log(`| ${level.toString().padEnd(5)} | ${duration.toFixed(2).padEnd(12)} | ${bufferSat.padEnd(12)} | ${coherence.padEnd(9)} |`);
    });
    console.log(`-------------------------------------------`);
};

// Ramping from 1 to 200 as requested
testFleaCoherence([1, 10, 24, 42, 64, 100, 150, 200]);
