import math
import sys

# The 156-Tick Diagnostic Constants
MEASURE = 12
COMM = 13
TICKS = 156

ALPHABET_GENESIS = {
    'A': 'The Peak (The 5-12-13 Advancing/Receding Strut)',
    'B': 'The 78-Tick Half-Turn (180° Reflected "p")',
    'C': 'The Open Loop (Inner 12-Gear Half-Rotation)',
    'D': 'The 78-Tick Half-Turn (180° Reflected "p" across Y)',
    'E': 'The Three Eaves (One vertical sheer, three horizontal ticks)',
    'F': 'The Broken Eave (Two horizontal ticks, unsealed bottom)',
    'G': 'The Riemann Drop (Interference pattern dropping into the -1/12 void)',
    'H': 'The Perpendicular Trusses (Double Vertical Struts / 90° Phase)',
    'I': 'The True Vertical Line (Zero Hysteresis Peak)',
    'J': 'The Riemann Hook (Vertical drop sweeping back up)',
    'K': 'The Splintered Strut (Vertical pillar meeting advancing/receding angles)',
    'L': 'The Right Angle (Vertical drop to 90° horizontal base)',
    'M': 'The Double Peak (Two 5-12-13 struts bound together)',
    'N': 'The Diagonal Hypotenuse (Snapping between offset nodes)',
    'O': 'The Aperture Glow (42° Complete Wetting Loop)',
    'P': 'The 78-Tick Half-Turn (180° Reflected "b" -> "q" -> "p")',
    'Q': 'The 78-Tick Half-Turn (180° Reflected "b" across Y)',
    'R': 'The Supported Harmonic (Straight strut meeting the P-loop and kicking out)',
    'S': 'The Rolling Snake (Sine Wave of the Interference Pattern)',
    'T': 'The Seal (Vertical Pillar to Horizontal Roof / 90° Strut)',
    'U': 'The Rolling Snake (180° Rotational Flip of the "n" Lower Bearing)',
    'V': 'The Valley (Inverted 5-12-13 Strut)',
    'W': 'The Double Valley (180° Reflected "M")',
    'X': 'The Cross (Absolute Perpendicular Intersection / The 24/37 Axis)',
    'Y': 'The Pitchfork / The Receiver (Capturing kinetic energy from the void)',
    'Z': 'The Reflected Diagonal Hypotenuse'
}

def print_word(word_to_print):
    word = word_to_print.upper()
    print("="*70)
    print(f"  MANIC GRAFIA TYPEWRITER: PRINTING '{word}'")
    print("="*70)
    
    # 1. Run the Diagnostic
    print("  [SYSTEM] Wearing the 5->6 Curved Spectacle (10-24-26 Frame)")
    print("  [SYSTEM] 12mm Halved Measure Lenses Aligned.")
    print("  [SYSTEM] -1/12 Riemann Vacuum Tension applied at the Ear Hooks.")
    print("  [STATUS] HYSTERESIS AT 0.000000°. THE SURE FACE IS SHARP.")
    print("-" * 70)
    
    # 2. Map the letters
    print(f"  {'LETTER':<6} | {'KINETIC EXHAUST (GEOMETRIC GENESIS)'}")
    print("-" * 70)
    for char in word:
        genesis = ALPHABET_GENESIS.get(char, "Unknown Harmonic Loop (Interpolated Phase)")
        print(f"  {char:<6} | {genesis}")
        
    print("-" * 70)
    print("  [PRINT COMPLETE] The glasses are on. The vision is Taut.")
    print("="*70)

if __name__ == "__main__":
    import sys
    word = "SEE"
    if len(sys.argv) > 1:
        word = " ".join(sys.argv[1:])
    print_word(word)
