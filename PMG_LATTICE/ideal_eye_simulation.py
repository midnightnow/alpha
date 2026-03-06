import numpy as np
import scipy.special as sp

def get_platonic_vertices():
    """Returns vertices of the 5 Platonic solids on the unit sphere."""
    # Tetrahedron
    v_tet = np.array([
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ]) / np.sqrt(3)
    
    # Octahedron
    v_oct = np.array([
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ])
    
    # Cube (Hexahedron)
    v_cube = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
    ]) / np.sqrt(3)
    
    # Icosahedron
    phi = (1 + np.sqrt(5)) / 2
    v_ico = np.array([
        [0, 1, phi], [0, 1, -phi], [0, -1, phi], [0, -1, -phi],
        [1, phi, 0], [1, -phi, 0], [-1, phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [phi, 0, -1], [-phi, 0, 1], [-phi, 0, -1]
    ])
    v_ico /= np.linalg.norm(v_ico, axis=1)[:, np.newaxis]
    
    # Dodecahedron
    v_dod = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, 1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, phi], [0, -1/phi, -phi],
        [1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, phi, 0], [-1/phi, -phi, 0],
        [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi]
    ])
    v_dod /= np.linalg.norm(v_dod, axis=1)[:, np.newaxis]
    
    return {
        "tet": v_tet, "oct": v_oct, "cube": v_cube, "ico": v_ico, "dod": v_dod
    }

def project(V, P):
    D = V - P
    a = np.dot(D, D)
    b = 2 * np.dot(P, D)
    c = np.dot(P, P) - 1
    roots = np.roots([a, b, c])
    t = max(roots)
    return P + t * D

def rotate_z(v, theta):
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return np.dot(v, R.T)

def run_simulation():
    P = np.array([0, 0, -1/12.0])
    solids = get_platonic_vertices()
    all_vertices = np.vstack(list(solids.values()))
    
    distinct_points = []
    
    # Simulate 156 ticks with a 5/24 rotation (Rolling Snake)
    for t in range(156):
        theta = (t * 5 * np.pi / 24.0) 
        
        for v in all_vertices:
            v_rot = rotate_z(v, theta)
            v_proj = project(v_rot, P)
            
            # Snap to count distinct points
            v_proj_rounded = np.round(v_proj, 6)
            
            is_new = True
            for dp in distinct_points:
                if np.allclose(v_proj_rounded, dp, atol=1e-5):
                    is_new = False
                    break
            if is_new:
                distinct_points.append(v_proj_rounded)
                
    print(f"Total distinct points found: {len(distinct_points)}")

if __name__ == "__main__":
    run_simulation()
