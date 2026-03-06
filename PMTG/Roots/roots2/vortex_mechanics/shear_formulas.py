import math
import json

def calculate_shear_metrics(angular_velocity_rad_s, unit_side=1.0):
    """
    Calculates the tangential velocity delta for a rotating square.
    
    Args:
        angular_velocity_rad_s (float): Angular velocity in radians per second (omega).
        unit_side (float): Side length of the square.
        
    Returns:
        dict: Metrics of the centrifugal shear.
    """
    radius_midpoint = unit_side / 2.0
    radius_corner = (unit_side * math.sqrt(2)) / 2.0
    
    velocity_midpoint = angular_velocity_rad_s * radius_midpoint
    velocity_corner = angular_velocity_rad_s * radius_corner
    
    velocity_delta = velocity_corner - velocity_midpoint
    percentage_delta = (velocity_delta / velocity_midpoint) * 100
    
    # Harmonic check: Is the corner hitting a root_2 multiple of the center's effective radius?
    harmonic_ratio = velocity_corner / velocity_midpoint
    
    return {
        "Angular_Velocity_omega": angular_velocity_rad_s,
        "Radius_Midpoint": round(radius_midpoint, 4),
        "Radius_Corner": round(radius_corner, 4),
        "Velocity_Midpoint": round(velocity_midpoint, 4),
        "Velocity_Corner": round(velocity_corner, 4),
        "Velocity_Delta": round(velocity_delta, 4),
        "Percentage_Increase": round(percentage_delta, 2),
        "Harmonic_Ratio": round(harmonic_ratio, 6),
        "Status": "Shear_Active" if harmonic_ratio >= math.sqrt(2) else "Sub_Critical"
    }

if __name__ == "__main__":
    # Example: Rotating at 1 rad/s
    metrics = calculate_shear_metrics(1.0)
    print(json.dumps(metrics, indent=2))
