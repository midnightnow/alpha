import math

def calculate_stairwell_clearance(pier_side):
    """Calculates clearance for infrastructure around a square pier in a round hole."""
    # The pier is the square peg
    # The clearance is the irrational path around it
    radius_of_hole = (pier_side * 1.41421356) / 2
    opportunity_gap = radius_of_hole - (pier_side / 2)
    
    return f"Available space for 'Hotel' infrastructure: {opportunity_gap:.4f} units per quadrant."

if __name__ == "__main__":
    print(calculate_stairwell_clearance(1))
