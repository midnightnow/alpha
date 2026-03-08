
import math

def calculate_gematria(word):
    return sum(ord(c.lower()) - 96 for c in word if c.isalpha())

def analyze_animal_fit(name):
    val = calculate_gematria(name)
    mod24 = val % 24
    angle = (mod24 * 15) % 360
    
    # Compass mapping
    if angle == 0: direction = "NORTH (Anchor)"
    elif angle == 90: direction = "EAST (Flow)"
    elif angle == 180: direction = "SOUTH (Sub-Ordinance)"
    elif angle == 270: direction = "WEST (Foundational 7)"
    elif 0 < angle < 90: direction = "NORTH-EAST (Organic Start)"
    elif 90 < angle < 180: direction = "SOUTH-EAST (Apex Flight)"
    elif 180 < angle < 270: direction = "SOUTH-WEST (Breeding/Transcendence)"
    else: direction = "NORTH-WEST (The Hunt)"
    
    # 7-Ordinance check
    is_master_key_factor = 420 % val == 0 if val != 0 else False
    
    print(f"ANIMAL: {name.upper()}")
    print(f"Gematria: {val}")
    print(f"Angle on 24-Wheel: {angle}°")
    print(f"Compass Fit: {direction}")
    print(f"Master Key Factor: {'YES (420/' + str(val) + ')' if is_master_key_factor else 'NO'}")
    print("-" * 30)

if __name__ == "__main__":
    zoo = ["cat", "dog", "mice", "bee", "fish", "bird", "queen", "wolf", "kitten"]
    print("--- THE PYRAMID ZOO: COMPASS AUDIT ---")
    for animal in zoo:
        analyze_animal_fit(animal)
