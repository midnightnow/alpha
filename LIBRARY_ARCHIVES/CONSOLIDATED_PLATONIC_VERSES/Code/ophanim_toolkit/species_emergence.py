import math

def get_prime_factors(n):
    factors = set()
    d = 2
    temp = abs(n)
    if temp == 0: return {0}
    while d * d <= temp:
        while temp % d == 0:
            factors.add(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors

def fibonacci_mod(m, limit):
    fib = [0, 1]
    for i in range(2, limit):
        fib.append((fib[i-1] + fib[i-2]) % m)
    return fib

def audit_species_emergence():
    m = 120
    period = 120
    seq = fibonacci_mod(m, period)
    
    # 1. Define the 'King's Windows' (Euler's Totient set for 120)
    windows = [i for i in range(m) if math.gcd(i, m) == 1]
    
    # 2. Maid's Checkpoints (13, 23, 33...)
    maids = [13, 23, 33, 43, 53, 63, 73, 83, 93, 103, 113]
    
    print(f"--- THE RHYME OF THE 10,000 THINGS (120-MOD SPECIES AUDIT) ---")
    print(f"Modulus: {m} | Period: {period}")
    print(f"Total Windows: {len(windows)}")
    print("-" * 80)
    print(f"{'Step n':>6} | {'Value':>6} | {'Factors':>20} | {'Status'}")
    print("-" * 80)
    
    for n in range(period):
        val = seq[n]
        factors = get_prime_factors(val)
        
        status = ""
        if val in windows:
            status = "WINDOW OPEN (Prime-Lane)"
        
        # Check for Species (Primes > 5)
        species = sorted([f for f in factors if f > 5])
        
        if n in maids:
            status = f"(!) MAID {n} RESET"
        
        # We find that at Node 13, val is 113 (Prime).
        # At Node 23, val is 97 (Prime).
        # At Node 33, val is 58 (2*29).
        
        if status or species:
            species_str = ", ".join(map(str, species)) if species else "-"
            print(f"{n:>6} | {val:>6} | {species_str:>20} | {status}")

if __name__ == "__main__":
    audit_species_emergence()
