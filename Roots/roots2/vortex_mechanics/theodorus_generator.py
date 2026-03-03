import math

def generate_vortex_coils(iterations):
    current_hypotenuse = 1 # Start with the unit 1
    spiral_map = []

    for n in range(1, iterations + 1):
        # The next hypotenuse is always the sqrt of (previous_hypotenuse^2 + 1^2)
        next_hypotenuse = math.sqrt(current_hypotenuse**2 + 1)
        spiral_map.append({
            "step": n,
            "radial_extension": next_hypotenuse,
            "phase_angle": math.degrees(math.atan(1/current_hypotenuse))
        })
        current_hypotenuse = next_hypotenuse
        
    return spiral_map

if __name__ == "__main__":
    # Map the first 17 roots (completing the first wrap of the spiral)
    vortex_plan = generate_vortex_coils(17)
    for step in vortex_plan:
        print(f"Step {step['step']}: Radius {step['radial_extension']:.4f}, Angle {step['phase_angle']:.2f}°")
