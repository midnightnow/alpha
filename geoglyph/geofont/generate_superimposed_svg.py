import math
import argparse

def generate_superimposed_svg(filename):
    svg_content = [
        f'<svg width="600" height="600" viewBox="-300 -300 600 600" xmlns="http://www.w3.org/2000/svg">',
        f'  <defs>',
        f'    <style>',
        f'      .hebrew {{ stroke: #D2B48C; fill: #D2B48C; }}',
        f'      .greek {{ stroke: #4682B4; fill: #4682B4; }}',
        f'      .latin {{ stroke: #2E8B57; fill: #2E8B57; }}',
        f'      .axis {{ stroke: #e0e0e0; stroke-width: 0.5; stroke-dasharray: 4,4; }}',
        f'      .lock {{ fill: rgba(255, 215, 0, 0.3); stroke: #DAA520; stroke-width: 1.5; }}',
        f'      text {{ font-family: sans-serif; font-size: 10px; text-anchor: middle; dominant-baseline: middle; }}',
        f'    </style>',
        f'  </defs>',
    ]
    
    # Radii
    base_r = 150
    latin_r = base_r * 1.0
    greek_r = base_r * (13/12)
    hebrew_r = base_r * (13/11)

    # Background Circles
    svg_content.append(f'  <!-- Concentric Tracks -->')
    svg_content.append(f'  <circle cx="0" cy="0" r="{latin_r}" fill="none" class="latin" stroke-width="0.5" stroke-dasharray="2,2"/>')
    svg_content.append(f'  <circle cx="0" cy="0" r="{greek_r}" fill="none" class="greek" stroke-width="0.5" stroke-dasharray="2,2"/>')
    svg_content.append(f'  <circle cx="0" cy="0" r="{hebrew_r}" fill="none" class="hebrew" stroke-width="0.5" stroke-dasharray="2,2"/>')

    # Draw Triple Locks (Background Highlight)
    # The locks at ~30 deg and ~330 deg
    svg_content.append('  <!-- Nodal Triple Locks Highlight -->')
    # Lock 1 (~30.14°)
    # Sector arc roughly 30 deg +/- 2.5 deg
    a1_rad_start = math.radians(27.5 - 90)
    a1_rad_end = math.radians(32.5 - 90)
    x1_s = math.cos(a1_rad_start) * (hebrew_r + 20)
    y1_s = math.sin(a1_rad_start) * (hebrew_r + 20)
    x1_e = math.cos(a1_rad_end) * (hebrew_r + 20)
    y1_e = math.sin(a1_rad_end) * (hebrew_r + 20)
    svg_content.append(f'  <path d="M 0 0 L {x1_s} {y1_s} A {hebrew_r+20} {hebrew_r+20} 0 0 1 {x1_e} {y1_e} Z" class="lock"/>')

    # Lock 2 (~329.86°)
    a2_rad_start = math.radians(327.5 - 90)
    a2_rad_end = math.radians(332.5 - 90)
    x2_s = math.cos(a2_rad_start) * (hebrew_r + 20)
    y2_s = math.sin(a2_rad_start) * (hebrew_r + 20)
    x2_e = math.cos(a2_rad_end) * (hebrew_r + 20)
    y2_e = math.sin(a2_rad_end) * (hebrew_r + 20)
    svg_content.append(f'  <path d="M 0 0 L {x2_s} {y2_s} A {hebrew_r+20} {hebrew_r+20} 0 0 1 {x2_e} {y2_e} Z" class="lock"/>')

    # Helper function to generate nodes
    def draw_nodes(nodes, r, css_class, label_prefix, alphabet):
        for i in range(nodes):
            angle_deg = i * (360 / nodes)
            angle_rad = math.radians(angle_deg - 90)
            x = math.cos(angle_rad) * r
            y = math.sin(angle_rad) * r
            
            # Draw line to node
            svg_content.append(f'  <line x1="0" y1="0" x2="{x}" y2="{y}" class="axis" />')
            # Draw node circle
            svg_content.append(f'  <circle cx="{x}" cy="{y}" r="3" class="{css_class}" />')
            
            # Label
            lx = math.cos(angle_rad) * (r + 12)
            ly = math.sin(angle_rad) * (r + 12)
            
            svg_content.append(f'  <text x="{lx}" y="{ly}" class="{css_class}">{alphabet[i*2] if i*2 < len(alphabet) else ""}</text>')

    # Alphabets mapping roughly first char for visual anchor
    hebrew_alpha = "אבגדהוזחטיכלמנסעפצקרשת"
    greek_alpha = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
    latin_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    draw_nodes(11, hebrew_r, "hebrew", "H", hebrew_alpha)
    draw_nodes(12, greek_r, "greek", "G", greek_alpha)
    draw_nodes(13, latin_r, "latin", "L", latin_alpha)

    # North Pole Sync Reference
    svg_content.append(f'  <line x1="0" y1="0" x2="0" y2="-{hebrew_r+30}" stroke="#000" stroke-width="1.5" />')
    svg_content.append(f'  <text x="0" y="-{hebrew_r+40}" fill="#000" font-weight="bold">THE APEX / NODE 0 (Perfect Synchronization)</text>')

    # Lock Annotations
    svg_content.append(f'  <text x="{math.cos(math.radians(30-90))*(hebrew_r+35)}" y="{math.sin(math.radians(30-90))*(hebrew_r+35)}" fill="#DAA520" font-weight="bold" font-size="12px">TRIPLE LOCK (30.1°)</text>')
    svg_content.append(f'  <text x="{math.cos(math.radians(330-90))*(hebrew_r+35)}" y="{math.sin(math.radians(330-90))*(hebrew_r+35)}" fill="#DAA520" font-weight="bold" font-size="12px">TRIPLE LOCK (329.9°)</text>')

    # Legend
    svg_content.append(f'  <g transform="translate(-280, 230)">')
    svg_content.append(f'    <text x="0" y="0" style="text-anchor:start;font-size:14px;font-weight:bold;">REFRACTIVE SCALING MAP</text>')
    svg_content.append(f'    <circle cx="5" cy="20" r="4" class="latin" /> <text x="15" y="20" class="latin" style="text-anchor:start;">Latin (13-Node, Scale 1.0)</text>')
    svg_content.append(f'    <circle cx="5" cy="35" r="4" class="greek" /> <text x="15" y="35" class="greek" style="text-anchor:start;">Greek (12-Node, Scale 1.083)</text>')
    svg_content.append(f'    <circle cx="5" cy="50" r="4" class="hebrew" /> <text x="15" y="50" class="hebrew" style="text-anchor:start;">Hebrew (11-Node, Scale 1.182)</text>')
    svg_content.append(f'    <rect x="-1" y="61" width="12" height="12" class="lock" /> <text x="15" y="67" fill="#B8860B" style="text-anchor:start;">Universal Convergence Zones</text>')
    svg_content.append(f'  </g>')

    svg_content.append('</svg>')
    
    with open(filename, "w") as f:
        f.write("\n".join(svg_content))
    print(f"SVG generated: {filename}")

if __name__ == "__main__":
    generate_superimposed_svg("/Users/midnight/dev/geofont/superimposed_wheels.svg")
