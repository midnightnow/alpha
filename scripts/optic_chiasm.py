import numpy as np
import plotly.graph_objects as go

def generate_visual_geometry():
    steps = 94 # 0 through 93
    s_vals = np.arange(steps)
    
    # Radius function: 
    # From eyes (s=0) to Chiasm (s=13), radius decreases to 0
    # From Chiasm (s=13) to Pineal (s=93), radius swells (Brain/Tracts) and returns to 0
    R = np.zeros(steps)
    for i in range(steps):
        if i <= 13:
            R[i] = 3.0 * np.cos((np.pi / 2) * (i / 13))
        else:
            R[i] = 5.0 * np.sin(np.pi * (i - 13) / 80)
            
    # Theta function: +5 modulo 24 progression
    # 5 steps on a 24-wheel = 5 * (2*pi / 24) radians per step
    theta_step = 5 * (2 * np.pi / 24)
    theta_1 = s_vals * theta_step
    theta_2 = theta_1 + np.pi # Second snake offset by 12 steps (180 degrees)
    
    # Calculate 3D coordinates
    # Snake 1 (Left Eye / Red)
    x1 = R * np.cos(theta_1)
    y1 = R * np.sin(theta_1)
    z1 = s_vals
    
    # Snake 2 (Right Eye / Blue)
    x2 = R * np.cos(theta_2)
    y2 = R * np.sin(theta_2)
    z2 = s_vals

    fig = go.Figure()

    # Draw Snake 1
    fig.add_trace(go.Scatter3d(
        x=x1, y=y1, z=z1, mode='lines+markers',
        marker=dict(size=3, color='red'),
        line=dict(color='red', width=4),
        name='+5 Progression (Left Eye)'
    ))

    # Draw Snake 2
    fig.add_trace(go.Scatter3d(
        x=x2, y=y2, z=z2, mode='lines+markers',
        marker=dict(size=3, color='cyan'),
        line=dict(color='cyan', width=4),
        name='+10 Offset Progression (Right Eye)'
    ))

    # Optic Chiasm (M, step 13)
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[13], mode='markers+text',
        marker=dict(size=10, color='yellow', symbol='diamond'),
        text=['Optic Chiasm (s=13, M)'], textposition="middle right",
        name='The Crossing'
    ))

    # Pineal Gland (Third Eye, step 93)
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[93], mode='markers+text',
        marker=dict(size=15, color='gold'),
        text=['Pineal Gland (s=93)'], textposition="top center",
        name='Apollonian Seed'
    ))
    
    # Eye Orbits (Visual field origins, step 0)
    fig.add_trace(go.Scatter3d(
        x=[x1[0], x2[0]], y=[y1[0], y2[0]], z=[0, 0], mode='markers',
        marker=dict(size=12, color='white', line=dict(color='black', width=2)),
        name='Eyes (s=0)'
    ))

    fig.update_layout(
        title="Hero 93: Optic Chiasm & The Twin Snakes",
        scene=dict(
            xaxis_title="Lateral Spatial Dimension",
            yaxis_title="Vertical Spatial Dimension",
            zaxis_title="Progression Step (s=0 to 93)",
            bgcolor='rgb(10, 10, 15)'
        ),
        paper_bgcolor='rgb(10, 10, 15)',
        font=dict(color='white')
    )

    fig.show()

if __name__ == "__main__":
    generate_visual_geometry()
