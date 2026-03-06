import json
import math

def calculate_hex(tick):
    # Simplified escape tension color mapping from user prompt
    # Red-shift for high primes, Fade to white for sync nodes
    if tick % 13 == 0:
        return "#FFFFFF"
    
    # Calculate a red-to-yellow gradient based on tick for high tension
    # Higher friction in middle prime regions
    r = 255
    g = int((tick / 156) * 204) # 0 to 204 (approx CC)
    b = 0
    return f"#{r:02X}{g:02X}{b:02X}"

def generate_veth():
    alphabet = []
    for tick in range(156):
        glyph = {
            "tick": tick,
            "em_freq_hz": round((tick % 13) / 13, 4) if tick % 13 != 0 else 0,
            "gr_curvature_l": round(tick * 0.0064, 4),
            "qm_fold": f"√({tick})/32",
            "thermal_hex": calculate_hex(tick),
            "identity": "Vitrified Node"
        }
        
        # Power Glyph Special Labeling
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        if tick in primes:
            glyph["identity"] = "Power Glyph (Prime)"
        
        alphabet.append(glyph)
    
    archive = {
        "header": "HERO 93 SOUL STAR ALPHABET",
        "units": "PMG-156",
        "vacuum_lock": "-1/12",
        "alphabet": alphabet
    }
    
    with open("/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/UI_VISOR/assets/manic_grafia_alphabet_156.veth", "w") as f:
        json.dump(archive, f, indent=4)

if __name__ == "__main__":
    generate_veth()
    print("manic_grafia_alphabet_156.veth generated.")
