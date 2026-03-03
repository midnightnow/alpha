import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

def generate_93_nodes():
    """
    Generates the 93-node matrix for the PMG Axiomatic Genesis.
    - 12 Vertices (Icosahedron)
    - 20 Face Centroids (Dodecahedron Vertices) 
    - 60 Edge Points (2 per edge, Golden Section)
    - 1 Center Point (Axis Mundi)
    
    Scaled to 'God Scale' where 1 unit = 1 inch (representing 1 foot at 1/12 scale).
    Standard Spine radius = 6.0 units.
    """
    phi = (1 + np.sqrt(5)) / 2
    
    # Scale factor S to ensure vertex radius is 6.0
    # Radius = sqrt(1 + phi^2) * S
    R_target = 6.0
    S = R_target / np.sqrt(1 + phi**2)
    
    # 1. 12 Vertices of the Icosahedron
    vertices = []
    for i in [-1, 1]:
        for j in [-phi, phi]:
            vertices.append([0, i * S, j * S])
            vertices.append([i * S, j * S, 0])
            vertices.append([j * S, 0, i * S])
    vertices = np.array(vertices)
    
    # 2. 20 Face Centroids
    # Find faces by checking which vertices are distanced by edge length
    # Edge length L = 2 * S
    edge_len = 2 * S
    faces = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            for k in range(j + 1, len(vertices)):
                d1 = np.linalg.norm(vertices[i] - vertices[j])
                d2 = np.linalg.norm(vertices[j] - vertices[k])
                d3 = np.linalg.norm(vertices[k] - vertices[i])
                # Precision check for equilateral faces
                if np.allclose([d1, d2, d3], edge_len, atol=1e-5):
                    face_centroid = (vertices[i] + vertices[j] + vertices[k]) / 3
                    # Avoid duplicates
                    if not any(np.allclose(face_centroid, f, atol=1e-5) for f in faces):
                        faces.append(face_centroid)
    faces = np.array(faces)

    # 3. 60 Edge Points (2 per edge)
    # Using the Golden Ratio for subdivision
    edges = []
    edge_nodes = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            dist = np.linalg.norm(vertices[i] - vertices[j])
            if np.allclose(dist, edge_len, atol=1e-5):
                # Golden Section points
                # P1 = V1 + (V2-V1)/phi
                # P2 = V2 + (V1-V2)/phi
                p1 = vertices[i] + (vertices[j] - vertices[i]) * (1/phi)
                p2 = vertices[j] + (vertices[i] - vertices[j]) * (1/phi)
                edge_nodes.append(p1)
                edge_nodes.append(p2)
                edges.append((i, j))
    edge_nodes = np.array(edge_nodes)

    # 4. Center Point
    center = np.array([[0, 0, 0]])

    all_nodes = {
        "Vertices": vertices,
        "Faces": faces,
        "EdgeNodes": edge_nodes,
        "Center": center
    }
    
    return all_nodes

def plot_nodes(nodes):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plotting each group with specific colors
    ax.scatter(nodes["Vertices"][:,0], nodes["Vertices"][:,1], nodes["Vertices"][:,2], c='blue', s=100, label='Vertices (12)')
    ax.scatter(nodes["Faces"][:,0], nodes["Faces"][:,1], nodes["Faces"][:,2], c='gold', s=80, label='Faces (20)')
    ax.scatter(nodes["EdgeNodes"][:,0], nodes["EdgeNodes"][:,1], nodes["EdgeNodes"][:,2], c='green', s=40, label='Edge Nodes (60)')
    ax.scatter(nodes["Center"][:,0], nodes["Center"][:,1], nodes["Center"][:,2], c='red', s=150, label='Axis Mundi (1)')
    
    ax.set_title("The 93-Node Matrix (1/12 God Scale)")
    ax.set_xlabel("X (inches)")
    ax.set_ylabel("Y (inches)")
    ax.set_zlabel("Z (inches)")
    ax.legend()
    
    # Equal aspect ratio
    max_range = 6.5
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    plt.savefig("/Users/studio/Sovereign/0platonicverses/93_node_matrix_visualization.png")
    print("Visualization saved to 93_node_matrix_visualization.png")
    plt.show()

if __name__ == "__main__":
    nodes = generate_93_nodes()
    
    # Export coordinates to JSON for the Appendix
    export_data = {
        "metadata": {
            "total_nodes": 93,
            "scale": "1/12 God Scale (1 unit = 1 inch)",
            "radius_spine": 6.0,
            "phi": (1 + np.sqrt(5)) / 2
        },
        "coordinates": {
            "vertices": nodes["Vertices"].tolist(),
            "faces": nodes["Faces"].tolist(),
            "edge_nodes": nodes["EdgeNodes"].tolist(),
            "center": nodes["Center"].tolist()
        }
    }
    
    with open("/Users/studio/Sovereign/0platonicverses/93_NODE_COORDINATES.json", "w") as f:
        json.dump(export_data, f, indent=4)
    
    print("Coordinates exported to 93_NODE_COORDINATES.json")
    
    # Print summary
    print(f"Nodes generated: {len(nodes['Vertices']) + len(nodes['Faces']) + len(nodes['EdgeNodes']) + len(nodes['Center'])}")
    
    # Optional plot
    try:
        plot_nodes(nodes)
    except Exception as e:
        print(f"Could not generate plot: {e}")
