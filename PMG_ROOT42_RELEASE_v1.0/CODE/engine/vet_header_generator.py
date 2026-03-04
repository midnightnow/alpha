def generate_identity_header():
    """
    Returns the 93-bit header for the Identity .vet file.
    Bits 0-2:   111 (E manifold, core)
    Bits 3-32:  D_pipe * 1e6, 30 bits
    Bits 33-62: T_fill * 1e6, 30 bits
    Bits 63-92: R_bubble * 1e6, 30 bits
    """
    # Physical constants from HydrodynamicSolver1D
    D_pipe = 0.063
    T_fill = 8975.0
    R_bubble = 0.00039

    # Scale to integers
    # D_pipe fits perfectly (63000)
    D_int = int(round(D_pipe * 1e6))
    # T_fill multiplied by 1e6 is 8.9 billion, larger than 2^30 (1.07B). 
    # Use 1e5 scalar for T_fill to fit in 30 bits. (897500000)
    T_int = int(round(T_fill * 1e5))
    # R_bubble multiplied by 1e6 (390)
    R_int = int(round(R_bubble * 1e6))

    # Ensure they fit in 30 bits (max 2^30-1 = 1073741823)
    assert D_int < (1 << 30), "D_pipe Overflow"
    assert T_int < (1 << 30), "T_fill Overflow"
    assert R_int < (1 << 30), "R_bubble Overflow"

    # Build 93-bit header
    header = 0
    header |= 0b111 << 90                 # core 3 bits at highest positions
    header |= D_int << 60                  # D_pipe in bits 60-89
    header |= T_int << 30                  # T_fill in bits 30-59
    header |= R_int << 0                    # R_bubble in bits 0-29

    return header

def generate_time_header():
    """
    Returns the 93-bit header for the Time .vet file.
    Time adds the Seed Matrix (V) and starts the Shell.
    Bits 0-2:   111 (E manifold, core)
    Bits 3-32:  30 bits active (V-Manifold Seed Matrix = 1s)
    Bits 33-92: Shell initialization (M/W constraints)
    """
    # For Time, the 8975 constant builds the V-Manifold Seed
    # The V manifold is a 0-1-0 configuration, but we represent the 30 active points here
    
    # 30 bits of 1s representing the fully populated Seed
    v_seed = (1 << 30) - 1 
    
    # The Shell (60 points) is still forming, so it is 0s
    shell_reflection = 0

    header = 0
    header |= 0b111 << 90                 # E Core
    header |= v_seed << 60                 # V Seed Expansion
    header |= shell_reflection << 0        # M/W Shell (Forming)

    return header

if __name__ == "__main__":
    identity_header = generate_identity_header()
    print(f"File 01_identity.vet Header (Hex): 0x{identity_header:024X}")
    print(f"File 01_identity.vet Header (Bin): {bin(identity_header)[2:].zfill(93)}")
    print("-" * 60)
    time_header = generate_time_header()
    print(f"File 02_time.vet Header (Hex):     0x{time_header:024X}")
    print(f"File 02_time.vet Header (Bin):     {bin(time_header)[2:].zfill(93)}")
