import json

with open("/Users/studio/Sovereign/0platonicverses/93_NODE_COORDINATES.json", "r") as f:
    data = json.load(f)

# Node 1-12: vertices
# Node 13-32: faces
# Node 33-92: edge_nodes
# Node 93: center

# Node 78 is the 171 Spark (171 mod 93 = 78)
n78_idx = 78 - 33
coords_78 = data["coordinates"]["edge_nodes"][n78_idx]

print(f"Node 78 (171 Spark) Coordinates: {coords_78}")

# Vowels (A, E, I, O, U) -> (1, 34, 67, 70, 73)
# 1 (A) is a Vertex (1-12)
# 34 (E) is an Edge Node (33-92)
# 67 (I) is an Edge Node (33-92)
# 70 (O) is an Edge Node (33-92)
# 73 (U) is an Edge Node (33-92)
# Wait, the user said vowels map to face centers. Let's re-verify the mapping.
# N = ((m-1)*171) mod 93 + 1
# A (1): (0*171) mod 93 + 1 = 1 (Vertex)
# E (5): (4*171) mod 93 + 1 = 684 mod 93 + 1 = (33 remainder 33) + 1 = 34 (Edge Node)
# I (9): (8*171) mod 93 + 1 = 1368 mod 93 + 1 = (66 remainder 66) + 1 = 67 (Edge Node)
# O (15): (14*171) mod 93 + 1 = 2394 mod 93 + 1 = (69 remainder 69) + 1 = 70 (Edge Node)
# U (21): (20*171) mod 93 + 1 = 3420 mod 93 + 1 = (72 remainder 72) + 1 = 73 (Edge Node)

vowels = {"A": 1, "E": 34, "I": 67, "O": 70, "U": 73}
for v, n in vowels.items():
    if 1 <= n <= 12:
        c = data["coordinates"]["vertices"][n-1]
    elif 13 <= n <= 32:
        c = data["coordinates"]["faces"][n-13]
    elif 33 <= n <= 92:
        c = data["coordinates"]["edge_nodes"][n-33]
    else:
        c = data["coordinates"]["center"][0]
    print(f"Node {n} ({v}) Coordinates: {c}")

# Tetragrammaton YHVH (Y=25, H=8, V=22, H=8)
# Nodes: 13, 82, 58, 82
n13_idx = 13 - 13
coords_13 = data["coordinates"]["faces"][n13_idx]
n82_idx = 82 - 33
coords_82 = data["coordinates"]["edge_nodes"][n82_idx]
n58_idx = 58 - 33
coords_58 = data["coordinates"]["edge_nodes"][n58_idx]

print(f"Node 13 (Y) Coordinates: {coords_13}")
print(f"Node 82 (H) Coordinates: {coords_82}")
print(f"Node 58 (V) Coordinates: {coords_58}")
