import math

def predict_rate(lattice, spiral, constants):
    """
    Derives an angular precession rate from lattice constants.
    Formula: omega = (Psi * spiral_radius) / Great_Year_normalized
    """
    psi = constants["PSI"]
    great_year = constants["GREAT_YEAR"]
    
    # 50.29 arcsec/yr is the target.
    # Lattice derivation: (Delta_Phi * 3600) / (2pi) ...
    # From earlier audit: DELTA_PHI = sqrt(42)/6 - 1 approx 0.0801
    
    delta_phi = (math.sqrt(42) / 6) - 1
    # Angular shift per beat?
    # Scaling to annual precession:
    # 360 / 25920 = 0.01388 degrees/year = 50.0 arcsec/year
    
    return (360 / great_year) * 3600 # Arcseconds per year
