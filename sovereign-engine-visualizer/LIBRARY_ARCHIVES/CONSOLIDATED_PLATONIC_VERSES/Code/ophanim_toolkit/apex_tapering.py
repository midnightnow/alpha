import math

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def calculate_apex_tapering(limit=10000, step=1000):
    """
    Calculates the 'Apex Tapering' of the 24-Wheel:
    The density of 'Singing Birds' (Primes) within the 8 Prime Lanes over time.
    """
    mod = 24
    prime_lanes = [1, 5, 7, 11, 13, 17, 19, 23]
    
    results = []
    
    current_primes_in_lanes = 0
    total_in_lanes = 0
    
    for x in range(1, limit + 1):
        node = x % mod
        if node in prime_lanes:
            total_in_lanes += 1
            if is_prime(x):
                current_primes_in_lanes += 1
        
        if x % step == 0:
            density = current_primes_in_lanes / total_in_lanes if total_in_lanes > 0 else 0
            results.append((x, density))
            
    return results

if __name__ == "__main__":
    limit = 100000
    step = 5000
    tapering = calculate_apex_tapering(limit, step)
    
    print(f"--- APEX TAPERING AUDIT (Mod 24) ---")
    print(f"{'Limit':>10} | {'Prime Density in Lanes':>25}")
    print("-" * 40)
    for x, d in tapering:
        print(f"{x:>10} | {d:>25.6f}")
    
    print("\nResult: The Prime Density in the 8 Lanes narrows as the number line ascends.")
    print("This is the 'Tapering of the Pyramid' towards the Apex (1).")
