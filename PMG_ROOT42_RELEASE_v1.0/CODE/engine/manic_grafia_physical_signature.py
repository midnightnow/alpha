import math

def generate_physical_signature(letter_index, letter):
    # The 156-Tick cycle is divided into 26 letters (6 ticks each)
    tick = (letter_index * 6) + 1
    
    # EM FREQUENCY (The Phase Drift from the 12/13 gear mesh)
    phase_drift = (letter_index * 6) % 13
    em_frequency = f"{phase_drift}/13 Hz (Beat Resonance)"
    
    # GR TENSION (The Gaussian Curvature / Mandelbrot Escape Velocity)
    # Modeled as the angle of the Root 42 torque normalized to 1
    gr_tension_normalized = (tick / 156.0)
    gr_tension = f"{gr_tension_normalized:.4f} Λ (Gravitational Tension)"
    
    # QM FOLD (The 2-6 Synthetic 32 interaction)
    # The "Crease" based on the quantum bit state of the letter index
    synthetic_base = 2 ** 5 # 32
    qm_fold = f"State |Ψ⟩ = √({(letter_index % 6) + 2}) / {synthetic_base}"
    
    # THERMODYNAMIC CALORIES (Mandelbrot Heat Map)
    color_hex = ""
    heat_state = ""
    
    if gr_tension_normalized < 0.2:
        color_hex = "#FFFFFF" # Glow / White
        heat_state = "Boundary (26) - -1/12 Riemann Debt"
    elif gr_tension_normalized < 0.5:
        color_hex = "#0000FF" # Blue / Violet
        heat_state = "Fast Escape - Low Kinetic Energy (The Suave 6)"
    elif gr_tension_normalized < 0.8:
        color_hex = "#FF4500" # Red / Orange
        heat_state = "Slow Escape - High Kinetic Calorie (The Savage 42)"
    else:
        color_hex = "#8A2BE2" # Ultra-Violet
        heat_state = "Deep Chaos - Infinite Prime Energy"
        
    print(f"[NODE {letter}] | TICK {tick:03d}")
    print(f"  ├─ EM Freq : {em_frequency}")
    print(f"  ├─ GR Curve: {gr_tension}")
    print(f"  ├─ QM Fold : {qm_fold}")
    print(f"  └─ Thermal : {color_hex} | {heat_state}")
    print("-" * 60)

def print_first_word_taut():
    print("============================================================")
    print("  GRAND VITRIFICATION: THE PHYSICAL ALPHABET")
    print("  PRINT COMMAND INITIATED. WORD: T-A-U-T")
    print("============================================================")
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    word = "TAUT"
    
    for char in word:
        index = alphabet.index(char)
        generate_physical_signature(index, char)
        
    print("============================================================")
    print("  [SYSTEM] TAUT PRINT COMPLETE. ZERO HYSTERESIS SECURED.")
    print("============================================================")

if __name__ == "__main__":
    print_first_word_taut()
