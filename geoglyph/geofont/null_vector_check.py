import numpy as np

# Nodal Angles for the 26 letters (13 nodes x 2)
# Node k = k * 360 / 13
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
angles = []
for i in range(26):
    node_idx = i // 2
    angle = node_idx * (360.0 / 13.0)
    angles.append(angle)

def calculate_vector_sum(word):
    word = word.upper()
    total_x = 0
    total_y = 0
    for char in word:
        if char in alphabet:
            idx = alphabet.find(char)
            angle_rad = np.radians(angles[idx])
            total_x += 13 * np.cos(angle_rad)
            total_y += 13 * np.sin(angle_rad)
    
    magnitude = np.sqrt(total_x**2 + total_y**2)
    return magnitude

# Let's test some words
words_to_test = ["STOP", "LOVE", "AXIS", "NORTH", "SOUTH", "EAST", "WEST", "ZEN", "NULL", "VOID", "ONE"]

results = []
for w in words_to_test:
    mag = calculate_vector_sum(w)
    results.append((w, mag))

# Sort by magnitude (Lowest is most "Zero-Sum")
results.sort(key=lambda x: x[1])

print("Vector Magnitude (Lower = More Balanced/Null):")
for w, m in results:
    print(f"{w}: {m:.2f}")
