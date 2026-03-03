def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_primes(limit):
    return [i for i in range(2, limit + 1) if is_prime(i)]

def find_superprimes(limit):
    primes = get_primes(limit)
    superprimes = []
    for i, p in enumerate(primes):
        if is_prime(i + 1):
            superprimes.append(p)
    return superprimes

if __name__ == "__main__":
    print("Superprime Analysis")
    sp = find_superprimes(1000)
    print(f"Superprimes up to 1000: {sp}")
    if 42 in sp:
        print("42 is a superprime!")
    else:
        print("42 is NOT a superprime, but it is a Harmonic Anchor.")
