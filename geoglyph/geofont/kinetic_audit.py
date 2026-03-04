import matplotlib.pyplot as plt
import numpy as np

# Alphabet and Mapping
# Node 0-12
# Pairs (CCW, CW)
mapping = [
    ('A', 'B'), # 0
    ('C', 'D'), # 1
    ('E', 'F'), # 2
    ('G', 'H'), # 3
    ('I', 'J'), # 4
    ('K', 'L'), # 5
    ('M', 'N'), # 6
    ('O', 'P'), # 7
    ('Q', 'R'), # 8
    ('S', 'T'), # 9
    ('U', 'V'), # 10
    ('W', 'X'), # 11
    ('Y', 'Z')  # 12
]

# Kinetic Classification Weights
# T (Torque) = 1.0
# D (Damping) = -1.0
# V (Vector) = 0.0
# B (Bipolar) = 0.5
weights = {
    'A': 0.0, 'B': 0.5, 'C': 1.0, 'D': 0.5,
    'E': -1.0, 'F': -1.0, 'G': 1.0, 'H': -1.0,
    'I': -1.0, 'J': 1.0, 'K': 0.0, 'L': -1.0,
    'M': 0.0, 'N': 0.0, 'O': 1.0, 'P': 0.5,
    'Q': 1.0, 'R': 0.5, 'S': 1.0, 'T': -1.0,
    'U': 1.0, 'V': 0.0, 'W': 0.0, 'X': 0.0,
    'Y': 0.0, 'Z': 0.0
}

# Calculate Net Kinetic Energy per Node
energies = []
for ccw, cw in mapping:
    # We treat CCW as positive torque and CW as... wait.
    # Actually, both can contribute to "Kinetic Density".
    # Let's measure absolute "Curvature Energy" vs "Damping Density".
    curvature = (abs(weights[ccw]) if weights[ccw] > 0 else 0) + (abs(weights[cw]) if weights[cw] > 0 else 0)
    damping = (abs(weights[ccw]) if weights[ccw] < 0 else 0) + (abs(weights[cw]) if weights[cw] < 0 else 0)
    energies.append((curvature, damping))

# Visualization
nodes = np.arange(13)
curvatures = [e[0] for e in energies]
dampings = [e[1] for e in energies]

plt.figure(figsize=(10, 6))
plt.bar(nodes, curvatures, label='Curvature (Torque)', alpha=0.7, color='blue')
plt.bar(nodes, dampings, label='Damping (Static)', alpha=0.7, color='red', bottom=curvatures)

plt.title('Kinetic Energy Distribution (Model 2)')
plt.xlabel('Node Index')
plt.ylabel('Kinetic Weight')
plt.xticks(nodes)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('/Users/midnight/dev/geofont/kinetic_distribution.png')
print("Kinetic distribution map generated.")
