#!/bin/bash

# Mathman Research Sweep Automation
# Generates 10 resonance profiles across the 0.9 to 1.1 lambda spectrum.

SWEEP_DIR="./samples/sweep_results"
mkdir -p "$SWEEP_DIR"

echo "Starting Research Sweep: Wavelength spectrum [0.9 - 1.1]..."

for i in {0..10}
do
    # Calculate lambda: 0.9 + (i * 0.02)
    LAMBDA=$(echo "0.9 + ($i * 0.02)" | bc)
    OUTPUT="$SWEEP_DIR/resonance_profile_L${LAMBDA}.jsonld"
    
    node scripts/generate_resonance_profile.js --wavelength "$LAMBDA" --height 4.2 --output "$OUTPUT"
done

echo "Sweep complete. All profiles saved to $SWEEP_DIR."
