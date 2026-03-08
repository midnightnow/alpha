import math

# A quick script to verify word mass distribution according to the 3-4-5 harmonic weight
# If we have 20 chapters, how do we distribute them?
# Let's say Total Mass = 20 chapters. 
# 3+4+5 = 12 units of "weight".
# 20 / 12 = 1.666 chapters per unit.
# Masculine (3) = 5 chapters
# Feminine (4) = 6.6 chapters
# Transcendent/Diagonal (5) = 8.3 chapters
# Let's write out the logic.

total_units = 12
weights = {
    "Masculine (3) - Structural Tension": 3,
    "Feminine (4) - The Home/Enclosure": 4,
    "Diagonal/Journey (5) - The Expansion": 5,
    "Hidden Meaning (7) - Contextual Override": 7
}

print("--- Harmonic Weight Distribution (Base 12) ---")
for name, w in weights.items():
    perc = (w / total_units) * 100
    print(f"{name}: {w} units ({perc:.1f}%)")

