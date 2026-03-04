import matplotlib.pyplot as plt
import numpy as np

# Node definitions and Signal Strength
# 1.0 = High (Curved/Bipolar alignment)
# 0.5 = Moderate (One letter fits, one is noise)
# 0.0 = Low (Rectilinear conflict/Friction)

nodes = np.arange(13)
signal_strength = [
    0.5, # 0: A/B (Medium)
    1.0, # 1: C/D (High - Arcs)
    0.0, # 2: E/F (Low - Friction)
    0.5, # 3: G/H (Medium - Brake)
    1.0, # 4: I/J (High - Pivot)
    0.5, # 5: K/L (Medium)
    0.5, # 6: M/N (Medium)
    1.0, # 7: O/P (High - Southern Lobe)
    1.0, # 8: Q/R (High - Southern Lobe)
    0.7, # 9: S/T (Moderate - The Engine)
    1.0, # 10: U/V (High - Western Gate)
    0.5, # 11: W/X (Medium)
    0.5  # 12: Y/Z (Medium)
]

labels = [
    'A/B', 'C/D', 'E/F', 'G/H', 'I/J', 'K/L', 'M/N', 
    'O/P', 'Q/R', 'S/T', 'U/V', 'W/X', 'Y/Z'
]

# Polar Plot
angles = np.linspace(0, 2 * np.pi, 13, endpoint=False).tolist()
signal_strength += signal_strength[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Draw the 'Spokes'
plt.xticks(angles[:-1], labels, color='grey', size=12)

# Fill the signal area
ax.plot(angles, signal_strength, color='blue', linewidth=2, linestyle='solid')
ax.fill(angles, signal_strength, color='blue', alpha=0.25)

# Highlight the Southern Lobe (Nodes 7-10)
theta_lobe = np.linspace(angles[7], angles[11], 100)
ax.fill_between(theta_lobe, 0, 1.1, color='red', alpha=0.1, label='Southern Lobe (Signal Cluster)')

ax.set_ylim(0, 1.2)
ax.set_title('Vortex-13: Signal-to-Noise Geometry', size=20, y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.savefig('/Users/midnight/dev/geofont/signal_to_noise_map.png')
print("Signal-to-Noise visualization generated.")
