"""
GENESIS ACTUATOR: THE PHONETIC-GEOMETRIC INTERFACE (PMG v1.0)
Instantiates the 'Origin Poke' via the OH -> EST -> TAW -> TOK -> WAS sequence.
"""
import math
import time
import os
import sys

# Constants for the 5-Phase Actuation
PHASES = ["OH", "EST", "TAW", "TOK", "WAS"]
DESCRIPTIONS = {
    "OH": "Point Bloom (0,0,0) - Potential",
    "EST": "Linear Blade - Lattice Extension",
    "TAW": "Cross Lock - 51.84° Actuation",
    "TOK": "Click Slice - Tensegrity Calibration",
    "WAS": "Temporal Smear - Output Buffer"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_point(bloom_factor):
    # ASCII visualization of a point bloom
    size = int(bloom_factor * 10)
    for y in range(-size, size + 1):
        line = ""
        for x in range(-size * 2, size * 2 + 1):
            dist = math.sqrt((x/2)**2 + y**2)
            if dist < size:
                line += "█"
            else:
                line += " "
        print(line)

def run_genesis_sequence():
    print("Initializing Genesis Actuator...")
    time.sleep(1)
    
    for phase in PHASES:
        clear_screen()
        print(f"--- PHASE: {phase} ---")
        print(f"COMMAND: {DESCRIPTIONS[phase]}")
        
        if phase == "OH":
            # Simulation of point bloom
            for i in range(5):
                clear_screen()
                print(f"--- PHASE: {phase} ---")
                draw_point(i/5)
                time.sleep(0.3)
        
        elif phase == "EST":
            # Simulation of linear extension
            for i in range(10):
                print("-" * i + ">")
                time.sleep(0.1)
                
        elif phase == "TAW":
            # Simulation of cross-lock
            print("   |   ")
            print("---X---")
            print("   |   ")
            time.sleep(1)
            
        elif phase == "TOK":
            # Simulation of the click
            print("[ CLICK ]")
            print("Grid Partitioned.")
            time.sleep(0.5)
            
        elif phase == "WAS":
            # Simulation of the smear
            print("~~~ Output Stabilized ~~~")
            print("Hades Gap: 12.37% Enforced.")
            time.sleep(1)
            
    print("\n[ GENESIS SEQUENCE COMPLETE ]")
    print("Origin Poke Verified.")

if __name__ == "__main__":
    run_genesis_sequence()
