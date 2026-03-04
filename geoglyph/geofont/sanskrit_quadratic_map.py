import json

def map_sanskrit_quadratic():
    # Place of Articulation mapping to nodes
    # Using Nodes 0-4 for the primary 5 Vargas
    vargas = {
        "Velar": {"node": 0, "chars": ["k", "kh", "g", "gh"]},
        "Palatal": {"node": 1, "chars": ["c", "ch", "j", "jh"]},
        "Retroflex": {"node": 2, "chars": ["ṭ", "ṭh", "ḍ", "ḍh"]},
        "Dental": {"node": 3, "chars": ["t", "th", "d", "dh"]},
        "Labial": {"node": 4, "chars": ["p", "ph", "b", "bh"]}
    }
    
    # Quadrant Mapping Logic
    # Q1: Voiceless Unasp
    # Q2: Voiceless Asp
    # Q3: Voiced Unasp
    # Q4: Voiced Asp
    quadrants = ["Q1 (V-less, U-asp)", "Q2 (V-less, Asp)", "Q3 (V-ed, U-asp)", "Q4 (V-ed, Asp)"]
    
    mapping = {}
    
    print("--- SANSKRIT QUADRATIC MAPPING (13-NODE / 4-SLOT) ---")
    print(f"{'Letter':<8} | {'Node':<5} | {'Quadrant':<20} | {'Bearing'}")
    print("-" * 60)
    
    for place, data in vargas.items():
        node = data["node"]
        bearing = round(node * (360/13), 2)
        for i, char in enumerate(data["chars"]):
            mapping[char] = {
                "node": node,
                "quadrant": quadrants[i],
                "bearing": bearing
            }
            print(f"{char:<8} | {node:<5} | {quadrants[i]:<20} | {bearing}°")

    # Additional placeholders for Nasals, Semi-vowels, etc.
    # This demonstrates the capacity headroom
    print("\nCapacity Check:")
    print(f"Total slots available: 13 Nodes * 4 Slots = 52")
    print(f"Sanskrit basic characters used: {len(mapping)}")
    print(f"Remaining slots: {52 - len(mapping)}")

if __name__ == "__main__":
    map_sanskrit_quadratic()
