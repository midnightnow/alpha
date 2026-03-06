import numpy as np
import matplotlib.pyplot as plt

def visualize_root_fields(max_val=10):
    """Visualizes sqrt(n) as expanding field gradients."""
    x = np.linspace(-max_val, max_val, 400)
    y = np.linspace(-max_val, max_val, 400)
    X, Y = np.meshgrid(x, y)
    Z = np.sqrt(np.sqrt(X**2 + Y**2)) # Double sqrt to accentuate gradient logic

    plt.figure(figsize=(12, 10))
    cp = plt.contourf(X, Y, Z, levels=20, cmap='magma')
    plt.colorbar(cp, label='Field Intensity (relative to √√r)')
    
    # Plot discrete integer radii circles for comparison
    for r in range(1, 5):
        circle = plt.Circle((0, 0), r**2, color='white', fill=False, linestyle='--', alpha=0.5)
        plt.gca().add_patch(circle)
        plt.text(0, r**2 + 0.1, f"r={r}^2", color='white', fontsize=10, ha='center')

    plt.title("Geometric Field Gradients: Resonating Square Roots")
    plt.axis('equal')
    
    save_path = "/Users/studio/00 Constellation/roots/root_fields.png"
    plt.savefig(save_path)
    print(f"Field gradient visualization saved to {save_path}")

if __name__ == "__main__":
    visualize_root_fields(25)
