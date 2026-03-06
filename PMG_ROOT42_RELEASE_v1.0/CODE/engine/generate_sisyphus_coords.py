import json
import math

def generate_sisyphus_coords():
    # 156-tick pulse mapped to the 93-point solid coordinates
    # The "Cheat Sheet" for escaping the material hill
    coords = []
    
    # Structural Constants
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    for tick in range(156):
        # The rolling snake expansion logic
        r = (tick % 24) + 1
        theta = (tick / 156) * (2 * math.pi)
        z = math.sin(tick * (42 * math.pi / 180)) * math.sqrt(42)
        
        is_stud = tick in primes
        is_vitrified = (tick % 13 == 0)
        
        # Base coordinates
        x_raw = r * math.cos(theta)
        y_raw = r * math.sin(theta)
        z_raw = z
        
        # Enforce Integers-Only for Vitrified/Studs
        if is_stud or is_vitrified:
            x = float(round(x_raw))
            y = float(round(y_raw))
            z = float(round(z_raw))
        else:
            x = round(x_raw, 6)
            y = round(y_raw, 6)
            z = round(z_raw, 6)
            
        point = {
            "tick": tick,
            "x": x,
            "y": y,
            "z": z,
            "label": f"Node_{tick}",
            "status": "Vitrified" if is_vitrified else "Savage"
        }
        
        if is_stud:
            point["class"] = "Power_Glyph_Stud"
            point["tension"] = "MAXIMUM"
        
        coords.append(point)

    archive = {
        "header": "SISYPHUS COORDINATES 156",
        "topology": "93_POINT_SOLID",
        "modulus": 24,
        "clutch_value": math.sqrt(42),
        "vacuum_debt": -1/12,
        "coordinates": coords
    }
    
    output_path = "/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/UI_VISOR/assets/sisyphus_coordinates_156.veth"
    with open(output_path, "w") as f:
        json.dump(archive, f, indent=4)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_sisyphus_coords()
