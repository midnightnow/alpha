import math

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def get_primes(count):
    primes = []
    n = 2
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def analyze_prime_alternating_sum(n_terms_list):
    """
    Calculates the partial sums of the alternating reciprocal primes:
    sum_{n=1}^{N} (-1)^n / p_n
    And estimates the error bounds.
    """
    max_terms = max(n_terms_list)
    primes = get_primes(max_terms)
    
    current_sum = 0.0
    results = {}
    
    for i in range(1, max_terms + 1):
        # We use (-1)^n / p_n. 
        # n=1: -1/2
        # n=2: +1/3
        # n=3: -1/5
        term = ((-1)**i) / primes[i-1]
        current_sum += term
        
        if i in n_terms_list:
            # error after N terms is bounded by the N+1 term
            error_bound = 1.0 / primes[i] if i < max_terms else 1.0 / (max_terms * math.log(max_terms))
            results[i] = (current_sum, error_bound)
            
    return results

if __name__ == "__main__":
    test_points = [10, 100, 1000, 10000]
    print("--- ANALYSIS OF THE ALTERNATING PRIME SUM ---")
    print("S = sum_{n=1}^{N} (-1)^n / p_n")
    print(f"{'N':>6} | {'Partial Sum':>15} | {'Error Bound (1/p_{N+1})':>20}")
    print("-" * 50)
    
    results = analyze_prime_alternating_sum(test_points)
    for n in test_points:
        s, err = results[n]
        print(f"{n:>6} | {s:>15.10f} | {err:>20.10f}")
        
    print("\nOBSERVATION:")
    print("The convergence is extremely slow (logarithmic-harmonic).")
    print("After 10,000 terms, we are only accurate to the 5th decimal place.")
    print("This slow resistance to convergence makes it the 'Stubborn Constant' of the Prime Lattice.")
