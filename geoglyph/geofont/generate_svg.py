import math

def generate_greek_wheel_svg(filename):
    greek_alphabet = [
        "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ",
        "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω"
    ]
    
    nodes = 12
    radius = 200
    center = 250
    
    svg_content = [
        f'<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">',
        f'  <defs>',
        f'    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">',
        f'      <polygon points="0 0, 10 3.5, 0 7" fill="#666" />',
        f'    </marker>',
        f'  </defs>',
        # Background circles
        f'  <circle cx="{center}" cy="{center}" r="{radius}" fill="none" stroke="#ddd" stroke-width="1" stroke-dasharray="5,5" />',
        f'  <circle cx="{center}" cy="{center}" r="{radius * 0.7}" fill="none" stroke="#eee" stroke-width="1" />',
        f'  <circle cx="{center}" cy="{center}" r="{radius * 0.4}" fill="none" stroke="#eee" stroke-width="1" />'
    ]
    
    # Draw Nodes and Labels
    for i in range(nodes):
        angle_deg = i * (360 / nodes)
        angle_rad = math.radians(angle_deg - 90) # -90 to start at North
        
        x_node = center + radius * math.cos(angle_rad)
        y_node = center + radius * math.sin(angle_rad)
        
        # Draw node line
        svg_content.append(f'  <line x1="{center}" y1="{center}" x2="{x_node}" y2="{y_node}" stroke="#ccc" stroke-width="0.5" />')
        
        # Get pair
        char_ccw = greek_alphabet[i * 2]
        char_cw = greek_alphabet[i * 2 + 1]
        
        # Position for CCW (Teal) - slightly offset to left
        x_ccw = center + (radius + 25) * math.cos(angle_rad - 0.05)
        y_ccw = center + (radius + 25) * math.sin(angle_rad - 0.05)
        
        # Position for CW (Rust) - slightly offset to right
        x_cw = center + (radius + 25) * math.cos(angle_rad + 0.05)
        y_cw = center + (radius + 25) * math.sin(angle_rad + 0.05)
        
        svg_content.append(f'  <text x="{x_ccw}" y="{y_ccw}" font-family="Arial" font-size="16" fill="#2d9a9a" text-anchor="middle">{char_ccw}</text>')
        svg_content.append(f'  <text x="{x_cw}" y="{y_cw}" font-family="Arial" font-size="16" fill="#b94a48" text-anchor="middle">{char_cw}</text>')
        
        # Node index
        x_idx = center + (radius + 50) * math.cos(angle_rad)
        y_idx = center + (radius + 50) * math.sin(angle_rad)
        svg_content.append(f'  <text x="{x_idx}" y="{y_idx}" font-family="Arial" font-size="10" fill="#999" text-anchor="middle">N{i}</text>')

    # Add Legend and Title
    svg_content.append(f'  <text x="{center}" y="30" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle">GREEK 12-NODE "OCTAVE SIEVE"</text>')
    svg_content.append(f'  <text x="{center}" y="50" font-family="Arial" font-size="12" fill="#666" text-anchor="middle">Material Perimeter (24 Vectors)</text>')
    
    svg_content.append(f'  <text x="20" y="470" font-family="Arial" font-size="12" fill="#2d9a9a">Teal: CCW Polarity</text>')
    svg_content.append(f'  <text x="20" y="485" font-family="Arial" font-size="12" fill="#b94a48">Rust: CW Polarity</text>')
    
    svg_content.append('</svg>')
    
    with open(filename, "w") as f:
        f.write("\n".join(svg_content))
    print(f"SVG generated: {filename}")

if __name__ == "__main__":
    generate_greek_wheel_svg("/Users/midnight/dev/geofont/greek_12node_wheel.svg")
