import numpy as np
import itertools

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
angles = [ (i // 2) * (360.0 / 13.0) for i in range(26) ]

def get_mag(word):
    tx = 0
    ty = 0
    for c in word:
        idx = alphabet.find(c)
        ar = np.radians(angles[idx])
        tx += 13 * np.cos(ar)
        ty += 13 * np.sin(ar)
    return np.sqrt(tx**2 + ty**2)

# Find 3-letter combinations that are stable
# We'll just check a small set of words or combinations
test_words = ["ZEN", "VOID", "LOVE", "ONE", "AXIS", "SUN", "SEA", "SKY", "GOD", "EYE"]

# Let's try 3-letter combos from common letters
common = "EARIOTNSLCUDPM"
best_null = []
for combo in itertools.combinations(common, 3):
    word = "".join(combo)
    mag = get_mag(word)
    if mag < 5:
        best_null.append((word, mag))

best_null.sort(key=lambda x: x[1])

print("Top 3-Letter Null Combinations (Magnitude < 5):")
for w, m in best_null[:10]:
    print(f"{w}: {m:.2f}")
