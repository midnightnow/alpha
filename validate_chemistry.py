def calculate_points(v_seq, h_seq):
    points = 0
    for v_bit in v_seq:
        for h_bit in h_seq:
            if v_bit == '1' and h_bit == '1':
                points += 1
    return points

def test_vet_canon():
    """
    V = 010 (1 active bar)
    E = 111 (3 active bars)
    T = 100 (1 active bar)
    Total = 5 active bars.
    Rotated Interference: 5x5 = 25?
    Wait, user canon:
    "V (0-1-0): 1 Active Bar (The Spine) -- Actually user said V is 0-1-0."
    "E (1-1-1): 3 Active Bars + Spine."
    "T (1-0-0): 1 Active Bar + Spine."
    "Total Active Bars: 5. Total Spines: 3. Intersection Points: 5 x 3 = 15. Rotational Reflection (x2): 15 x 2 = 30."
    """
    v = '010'
    e = '111'
    t = '100'
    seq = [v, e, t]
    total = sum(calculate_points(v_bit, h_bit) for v_bit in seq for h_bit in seq)
    print(f"Canon VET x VET points (V=010, E=111, T=100) -> {total}")

def test_h2a():
    """
    H is 3x3 matrix. Parallel vertical bars (1, 1) and middle bridge.
    H = [
      ['1', '0', '1'], # Top
      ['1', '1', '1'], # Middle
      ['1', '0', '1']  # Bottom
    ]
    A is Convergent. Diagonal legs and horizontal binder.
    A = [
      ['0', '1', '0'], # Top (Apex)
      ['1', '1', '1'], # Middle (Binder)
      ['1', '0', '1']  # Bottom (Legs)
    ]
    """
    h = [
      ['1', '0', '1'],
      ['1', '1', '1'],
      ['1', '0', '1']
    ]
    
    a = [
      ['0', '1', '0'],
      ['1', '1', '1'],
      ['1', '0', '1']
    ]
    
    # Let's count active bits (Unbroken) in H and A
    h_active = sum(bit == '1' for row in h for bit in row)
    a_active = sum(bit == '1' for row in a for bit in row)
    print(f"H active bits: {h_active} (Expected 7 for Bridge: 2 vertical * 3 + 1 middle)")
    print(f"A active bits: {a_active} (Expected 6 for Apex: 1 top + 3 middle + 2 bottom)")
    
    # Testing H2A molecule
    # H + H + A interference
    # Let's say we chain them vertically and spin them 90 degrees.
    molecule_seq = [h, h, a]
    
    # 9x3 matrix
    flat_v = []
    for letter in molecule_seq:
        for row in letter:
            flat_v.append(row)
            
    # flat_h is flat_v rotated 90 degrees?
    
test_vet_canon()
test_h2a()
