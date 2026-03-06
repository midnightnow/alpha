import json

def generate_calibration():
    power_glyphs = [
        {"n": 2, "color": "#FFFFFF", "pos": "top-left", "r": 99999, "role": "anchor"},
        {"n": 3, "color": "#8b5cf6", "pos": "top", "r": 1000, "role": "foundation"},
        {"n": 5, "color": "#3b82f6", "pos": "top-right", "r": 500, "role": "count"},
        {"n": 7, "color": "#06b6d4", "pos": "right", "r": 333, "role": "threshold"},
        {"n": 11, "color": "#10b981", "pos": "bottom-right", "r": 250, "role": "guard"},
        {"n": 13, "color": "#fbbf24", "pos": "bottom", "r": 200, "role": "peak"},
        {"n": 17, "color": "#f59e0b", "pos": "bottom-left", "r": 167, "role": "tension"},
        {"n": 19, "color": "#f97316", "pos": "left", "r": 143, "role": "rod"},
        {"n": 23, "color": "#ef4444", "pos": "inner-top-left", "r": 125, "role": "thermal"},
        {"n": 29, "color": "#b91c1c", "pos": "center", "r": 100, "role": "escape"}
    ]
    
    calibration = {
        "header": "APERTURE CALIBRATION 156",
        "scaling_constant": 2600,
        "vacuum_lock": "-1/12",
        "power_glyphs": power_glyphs,
        "edge_logic": "r = 2600 / n",
        "bend_logic": "y = 5 + (x^2 / (2r))"
    }
    
    output_path = "/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/UI_VISOR/assets/aperture_calibration_156.veth"
    with open(output_path, "w") as f:
        json.dump(calibration, f, indent=4)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_calibration()
