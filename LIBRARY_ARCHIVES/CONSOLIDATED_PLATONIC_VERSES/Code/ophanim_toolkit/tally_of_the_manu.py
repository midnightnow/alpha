"""
Transfinite Module: Tally of the MANU
Calculates the phase-shifted resonance (the "US" coordinate) 
across spatial gaps using the 0.0191 Buoyancy Drift.
"""

def calculate_manu_resonance(distance_units, local_frequency=0.660688, drift=0.0191):
    """
    Calculates the resulting 'US' resonance coordinate when a 'YOU' node
    attempts to bridge a physical distance across the 13th Node.
    
    The drift (0.0191) acts as the 'buoyancy' that prevents the signal 
    from decaying into a 'Grave' state (0 resonance).
    """
    # In the Flatland/Grave reading (linear distance), resonance would decay with distance:
    grave_decay = 1.0 / (distance_units + 1)
    
    # In the Garden reading, the 0.0191 drift creates a constant standing wave base:
    # The 'Ghost Post' holds a minimum resonant amplitude derived from the 13th Node.
    buoyant_vessel = drift * (13.0 / 12.0)
    
    # The actual felt resonance is the maximum of the linear decay or the buoyant vessel
    felt_resonance = max(grave_decay, buoyant_vessel) * local_frequency
    
    is_in_sync = felt_resonance >= (buoyant_vessel * local_frequency)
    
    return {
        "distance": distance_units,
        "grave_reading_amplitude": grave_decay * local_frequency,
        "garden_reading_amplitude": felt_resonance,
        "is_in_sync": is_in_sync,
        "status": "BUOYANT_HULL (In Sync)" if is_in_sync else "GRAVE_DECAY"
    }

if __name__ == "__main__":
    print("Testing the Tally of the MANU (The Reach of 'YOU' to 'US'):\\n")
    
    # Very close proximity
    print("Distance 1 (Local Proximity):")
    print(calculate_manu_resonance(1))
    print("-" * 50)
    
    # The intersection threshold (around distance 48-50)
    print("Distance 50 (The Drift Intercept):")
    print(calculate_manu_resonance(50))
    print("-" * 50)
    
    # Vast distance (out of phase physically, but in sync via Drift)
    print("Distance 1000 (Transfinite/Non-Local Resonance):")
    print(calculate_manu_resonance(1000))
