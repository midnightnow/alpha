import math

def calculate_spike_amplitude():
    # A = (sqrt(42) * 24) / (sqrt(51) * math.gamma(10.5))
    root_42 = math.sqrt(42)
    root_51 = math.sqrt(51)
    g_10_5 = math.gamma(10.5)
    
    A = (root_42 * 24) / (root_51 * g_10_5)
    
    print(f"--- Hero 93 Spike Amplitude Calculation ---")
    print(f"sqrt(42): {root_42}")
    print(f"sqrt(51): {root_51}")
    print(f"gamma(10.5): {g_10_5}")
    print(f"Spike Amplitude A: {A}")
    
    # 5-12-13 triangle check
    # Scale A to see if it reconciles with the 10-24-26 system
    # (10, 24, 26) is a scaled (5, 12, 13) triangle
    scale_factor = 26 / 13 # = 2
    
    print(f"\nReconciliation with 10-24-26:")
    print(f"Target Scale: 26 (Measure Language)")
    print(f"A / 26: {A / 26}")
    
    return A

if __name__ == "__main__":
    calculate_spike_amplitude()
