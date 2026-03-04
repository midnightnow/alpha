const core = require('./dist/index.js');

console.log("--- @platonic/core Verification ---");
console.log("Packing Constant (ρ):", core.PACKING_CONSTANT);
console.log("Hades Gap (Ψ):", core.HADES_GAP);
console.log("Shear Angle (θ):", core.SHEAR_ANGLE_DEG);
console.log("Beat Frequency (β):", core.BEAT_FREQUENCY);
console.log("Overpack Delta (δ):", core.OVERPACK_DELTA);

if (Math.abs(core.PACKING_CONSTANT - Math.sqrt(14 / 17)) < 1e-10) {
    console.log("✓ Geometry verified: 14/17 ratio holds.");
} else {
    console.error("❌ Geometry mismatch!");
}
