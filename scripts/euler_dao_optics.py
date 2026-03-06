import numpy as np
import plotly.graph_objects as go

# 1. The Euler Metric: 1 + e + e + 1 ≈ 6.436
EULER_SPAN = 1 + np.e + np.e + 1 

def generate_fractal_camera_obscura():
    steps = 94 # 0 to 93
    s_vals = np.arange(steps)
    
    # +5 modulo 24 stepping for the Twin Snakes
    theta_step = 5 * (2 * np.pi / 24)
    theta_1 = s_vals * theta_step
    theta_2 = theta_1 + np.pi # Left vs Right Eye (Phase shift)
    
    # Base Radius: Pinches at 13 (Alpha/e loop crossover), peaks between 13 and 93
    base_R = np.zeros(steps)
    for i in range(steps):
        if i <= 13:
            base_R[i] = np.cos((np.pi / 2) * (i / 13))
        else:
            base_R[i] = np.sin(np.pi * (i - 13) / 80)

    fig = go.Figure()

    # Create frames for 10^n scaling (Adding 'O' Loops)
    scales = [0, 1, 2]
    scale_names = ["n=0: The Eye (Micro)", "n=1: The Vitruvian Man (Meso)", "n=2: The Ideal Globe (Macro)"]
    
    for n in scales:
        # The 10^n Multiplier applied to the Euler Span
        R = base_R * EULER_SPAN * (10**n)
        Z = s_vals * (EULER_SPAN / 93) * (10**n) # Scale depth proportionally
        
        # Snake 1 (Alpha / a / e loop)
        x1, y1 = R * np.cos(theta_1), R * np.sin(theta_1)
        # Snake 2 (Inverse loop)
        x2, y2 = R * np.cos(theta_2), R * np.sin(theta_2)
        
        visible = (n == 0) # Only first scale visible by default
        
        fig.add_trace(go.Scatter3d(
            x=x1, y=y1, z=Z, mode='lines',
            line=dict(color='red', width=4),
            name=f'Left Optic Tract (Scale {10**n})',
            visible=visible
        ))
        fig.add_trace(go.Scatter3d(
            x=x2, y=y2, z=Z, mode='lines',
            line=dict(color='cyan', width=4),
            name=f'Right Optic Tract (Scale {10**n})',
            visible=visible
        ))
        
        # Chiasm Pinch (The 'M' / crossing of the 'alpha')
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[Z[13]], mode='markers+text',
            marker=dict(size=8, color='yellow', symbol='diamond'),
            text=[f'Chiasm (s=13)<br>Radius: 0'],
            visible=visible, name='Optic Chiasm'
        ))
        
        # Pineal Convergence (The 'O' culmination)
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[Z[93]], mode='markers+text',
            marker=dict(size=12, color='gold'),
            text=[f'Pineal (s=93)<br>Max Z: {Z[93]:.1f}'],
            visible=visible, name='Pineal Gland'
        ))

    # Create Slider for 10^n (Adding 'O' loops)
    steps_slider = []
    traces_per_step = 4
    
    for i, name in enumerate(scale_names):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": f"The Camera Obscura Topology | {name} | R_max = {EULER_SPAN * (10**i):.1f}"}],
            label=f"10^{i}"
        )
        # Toggle visibility for the specific scale
        for j in range(traces_per_step):
            step["args"][0]["visible"][i * traces_per_step + j] = True
        steps_slider.append(step)

    sliders = [dict(
        active=0, currentvalue={"prefix": "Topological Scale: "},
        pad={"t": 50}, steps=steps_slider
    )]

    fig.update_layout(
        sliders=sliders,
        title=f"The Camera Obscura Topology | {scale_names[0]} | R_max = {EULER_SPAN:.1f}",
        scene=dict(
            xaxis=dict(title="Lateral (X)", backgroundcolor="rgb(10,10,15)"),
            yaxis=dict(title="Vertical (Y)", backgroundcolor="rgb(10,10,15)"),
            zaxis=dict(title="Progression (Z)", backgroundcolor="rgb(10,10,15)"),
            bgcolor='rgb(5, 5, 10)'
        ),
        paper_bgcolor='rgb(5, 5, 10)', font=dict(color='white')
    )
    
    fig.show()

if __name__ == "__main__":
    generate_fractal_camera_obscura()
