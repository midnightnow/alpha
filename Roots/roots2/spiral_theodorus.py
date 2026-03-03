import math
import matplotlib.pyplot as plt
import numpy as np

def generate_spiral(n_points=17):
    """Generates coordinates for the Spiral of Theodorus."""
    points = [(1, 0)] # First point
    current_angle = 0
    current_hypotenuse = 1
    
    for i in range(1, n_points + 1):
        # Step increment is always 1 perpendicular to current hypotenuse
        angle_step = math.atan(1 / current_hypotenuse)
        current_angle += angle_step
        current_hypotenuse = math.sqrt(current_hypotenuse**2 + 1)
        
        x = current_hypotenuse * math.cos(current_angle)
        y = current_hypotenuse * math.sin(current_angle)
        points.append((x, y))
    
    return points

def plot_spiral(points):
    """Plots the spiral with root labels."""
    plt.figure(figsize=(10, 10))
    x_vals, y_vals = zip(*points)
    
    # Plot triangles
    plt.plot([0, x_vals[0]], [0, y_vals[0]], 'k-', alpha=0.3)
    for i in range(1, len(points)):
        plt.plot([0, x_vals[i]], [0, y_vals[i]], 'k-', alpha=0.3)
        plt.plot([x_vals[i-1], x_vals[i]], [y_vals[i-1], y_vals[i]], 'b-', alpha=0.6)
        
        # Label the hypotenuse
        root_val = i + 1
        dist = np.sqrt(root_val)
        mid_x = (x_vals[i] / 2) * 1.1
        mid_y = (y_vals[i] / 2) * 1.1
        plt.text(mid_x, mid_y, f"√{root_val}", fontsize=8, color='red')

    plt.axis('equal')
    plt.title("Spiral of Theodorus: Visualization of √n Accumulation")
    plt.grid(True, linestyle='--', alpha=0.7)
    
    save_path = "/Users/studio/00 Constellation/roots/spiral_theodorus.png"
    plt.savefig(save_path)
    print(f"Spiral visualization saved to {save_path}")

if __name__ == "__main__":
    spiral_points = generate_spiral(17)
    plot_spiral(spiral_points)
