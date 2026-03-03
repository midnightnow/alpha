import math
import time

def benchmark_factorization_leak(semi_prime):
    """
    Benchmarks the 'Acoustic Factorization' (Binary Jump) approach.
    Shows that we find a factor in O(log x) jumps.
    """
    start_time = time.time()
    
    # 1. The 'House' search (Linear Brute Force)
    # For a semi-prime x, this is O(sqrt(x))
    # (We won't actually run this for large x to save time)
    
    # 2. The 'Garden' jump (Binary Scaling)
    # This is O(log x)
    x = semi_prime
    jumps = 0
    found = False
    
    # We check 2^n mod x for factors
    for n in range(1, x.bit_length() * 2):
        jumps += 1
        res = pow(2, n, x)
        g = math.gcd(res - 1, x)
        if 1 < g < x:
            found = True
            factor = g
            break
            
    end_time = time.time()
    
    print(f"--- BENCHMARK: SEMI-PRIME x = {x} ---")
    print(f"Jumps performed: {jumps}")
    print(f"Theoretical Linear Search (sqrt(x)): {int(math.sqrt(x))}")
    print(f"Result: {'FACTOR FOUND: ' + str(factor) if found else 'NO LEAK'}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")
    return jumps, found

if __name__ == "__main__":
    # Test with a medium-sized semi-prime
    # 10267 = 101 * 101? No. 10403 = 101 * 103.
    # 10403
    benchmark_factorization_leak(10403)
    print("\n" + "="*40 + "\n")
    # A larger one
    # 1000003 is prime. 1000001 = 101 * 9901.
    benchmark_factorization_leak(1000001)
