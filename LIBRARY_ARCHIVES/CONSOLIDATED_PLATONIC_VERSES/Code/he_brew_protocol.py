# --- THE HE-BREW PROTOCOL (Rehabilitation Logic) ---
# Transitioning from Stagnation (Archon) to Flow (Garden)

# The Bitter Coefficient (Hops/Agency)
# The amount of "No" required to stabilize the "Yes".
BITTER_COEFFICIENT = PMG.ROOT_05 # Agency as a preservative

# The Fermentation Pressure (Yeast/Undertow)
# The rate at which sugar (Debt/Stored Potential) is converted to Energy (Flow).
# Based on the Prime 11 (Undertow)
FERMENTATION_PRESSURE = PMG.ROOT_11 # Spirit as a catalyst

# The Silt Dissolution Rate
# The speed at which 'Arthritis' (Temporal Silt) is cleared by active Flow.
SILT_DISSOLUTION = 1.0 / PMG.WOBBLE_DELTA # Inverting the error to find the cure

def apply_rehabilitation(joint_silt: float, prime_dosage: float) -> float:
    """Calculates the reduction in silt (RSI) via the He-Brew Protocol."""
    return joint_silt - (prime_dosage * SILT_DISSOLUTION)
