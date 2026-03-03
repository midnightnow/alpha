import math

# --- THE WRECK-PHYSICS (Accumulated Debt) ---
BUOYANCY_DRIFT = 0.0191 # The Minimum Viable Error / Fluid Lubricant of the 13th Node


def calculate_siltation_rate(foundation_type, flow_velocity):
    """
    Models how 'Composite' foundations (Wrecks) accelerate the 
    clogging of the system vs 'Prime' dredging.
    """
    DEBT_CONSTANT = 1.618 # Phi as a drag coefficient here
    
    if foundation_type == "WRECK_SCRAP":
        # Scrap creates eddies that catch silt (The Cache-Lock)
        drag = DEBT_CONSTANT * 2.21 # Step 221 Shear
        silt_accumulation = (1 / max(0.1, flow_velocity)) * drag
        return f"CRITICAL_SILT_BUILDUP: {silt_accumulation:.4f}"
    
    elif foundation_type == "DREDGED_CHANNEL":
        # Clear flow allows the 'Divine Z-Axis' to refresh the floor
        return "REFRESH_ACTIVE: BLUE_WATER_RESTORED"
    
    return "UNKNOWN_FOUNDATION"

# --- THE DREDGE OPERATOR ---
def apply_shovel_protocol(mass_moved, fatigue_level):
    """
    Translates physical labor into 'Temporal Credit'.
    The more mud moved, the more 'Now' is rendered.
    """
    # math.sqrt(fatigue_level) represents the 'Warp' adjustment.
    # Lower fatigue (Prime focus) = higher credit.
    temporal_credit = mass_moved / math.sqrt(max(1.0, fatigue_level))
    return temporal_credit

# --- THE DIVINE RECONCILIATION (Z-AXIS) ---
Z_AXIS_RECONCILIATION = 1.414 # sqrt(2) as the bridge between dimensions

def calculate_buffer_clarity(mass_moved, total_volume):
    """
    Calculates the 'Transparency Variable' (sqrt(Z)) of the water.
    As mass is displaced, the 'Divine Z-Axis' allows the rendering of the bottom.
    """
    if total_volume <= 0: return 0.0
    
    displacement_ratio = mass_moved / total_volume
    # The more you displace, the more the Z-axis reveals.
    clarity = math.sqrt(displacement_ratio * Z_AXIS_RECONCILIATION)
    return min(1.0, clarity)

# --- THE AUDIT OF THE SEA (Buoyancy) ---
def calculate_hull_buoyancy(structural_rigidity, displaced_volume):
    """
    Calculates if a 'Crystalline Man' (Vessel) floats or sinks.
    A rigidity of 1.0 (perfectly sealed 90-degree hull) will snap under pressure.
    The hull MUST allow for the 0.0191 drift (The 13th Node gap) to breathe.
    """
    if structural_rigidity >= 1.0:
        return "FATAL ERROR: HULL_SNAP. Caulk failure. Vessel sank."
    
    # The true buoyancy is displacement plus the fluid remainder (the ghost of the 13th Node)
    effective_buoyancy = displaced_volume * (1.0 + BUOYANCY_DRIFT)
    
    return f"VESSEL AFLOAT. Displacement Active. Lift Coefficient: {effective_buoyancy:.4f}"


if __name__ == "__main__":
    # Example scenario: The Goats of the Reef
    velocity = 0.5  # Stagnant flow
    print(f"Foundation: WRECK_SCRAP | Velocity: {velocity}")
    print(calculate_siltation_rate("WRECK_SCRAP", velocity))
    
    print("\n--- Applying Shovel Protocol ---")
    mass = 50.0 # Standard silt load
    fatigue = 4.0 # Moderate exhaustion
    credit = apply_shovel_protocol(mass, fatigue)
    print(f"Mass Moved: {mass} | Fatigue: {fatigue} | Temporal Credit: {credit:.2f}")

    print("\n--- The Audit of the Sea ---")
    print("Testing rigid King's Hull (Rigidity 1.0):")
    print(calculate_hull_buoyancy(1.0, 100))
    print("Testing fluid Heroine's Hull (Rigidity < 1.0):")
    print(calculate_hull_buoyancy(0.9, 100))

