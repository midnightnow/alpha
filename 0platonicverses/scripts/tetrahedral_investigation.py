import numpy as np

def calculate_tetrahedron_properties(a, b, c):
    """
    Calculates properties of a tetrahedron with edges a, b, c meeting at a right-angled vertex.
    a = 5 (Number)
    b = 12 (Time)
    c = 13 (Information)
    """
    # Coordinates
    O = np.array([0, 0, 0])
    A = np.array([a, 0, 0])
    B = np.array([0, b, 0])
    C = np.array([0, 0, c])
    
    # Volume
    volume = (a * b * c) / 6.0
    
    # Other edges
    e_ab = np.sqrt(a**2 + b**2)
    e_bc = np.sqrt(b**2 + c**2)
    e_ca = np.sqrt(c**2 + a**2)
    
    # Faces
    area_oab = 0.5 * a * b
    area_obc = 0.5 * b * c
    area_oca = 0.5 * c * a
    
    # The "Information Face" ABC
    # Using Heron's formula for area of ABC
    s = (e_ab + e_bc + e_ca) / 2.0
    area_abc = np.sqrt(s * (s - e_ab) * (s - e_bc) * (s - e_ca))
    
    # Circumradius R of this tetrahedron
    # For a trirectangular tetrahedron (orthogonal edges at one vertex):
    # R = 0.5 * sqrt(a^2 + b^2 + c^2)
    R = 0.5 * np.sqrt(a**2 + b**2 + c**2)
    R2 = R**2
    
    print(f"--- Tetrahedron (a={a}, b={b}, c={c}) ---")
    print(f"Volume: {volume}")
    print(f"Edges: {a}, {b}, {c}, {e_ab:.4f}, {e_bc:.4f}, {e_ca:.4f}")
    print(f"Face ABC Area: {area_abc:.4f}")
    print(f"Circumradius R: {R:.4f}")
    print(f"R^2: {R2:.4f}")
    
    # Search for the 42 factor
    # Is it Volume / something?
    # R2 / 1? (42.25)
    # Area_abc / something?
    
    # Cayley-Menger Determinant for Volume
    # Det = 288 * V^2
    det_v = 288 * (volume**2)
    print(f"Cayley-Menger Det (288*V^2): {det_v}")
    
    # Relation to 42
    print(f"R2 / 42.25: {R2/42.25}")
    print(f"Volume / 130: {volume/130}") # Since 130 = 13 * 10
    
    # User's Hint: 42.25 = (5^2 + 12^2 + 13^2) / 8
    # Which is exactly (25 + 144 + 169) / 8 = 338 / 8 = 42.25
    
if __name__ == "__main__":
    calculate_tetrahedron_properties(5, 12, 13)
