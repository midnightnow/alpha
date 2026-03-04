import math

def rigorous_audit(x, base=10, jump_base=2):
    """
    Translates graphical observations of (1/x) and 2^n jumps into 
    Group-Theoretic / Modular Algebra notation.
    """
    print(f"--- RIGOROUS AUDIT: x = {x} ---")
    
    # 1. Multiplicative Order of 10 mod x (Decimal Period)
    try:
        ord_10 = math.gcd(10, x) == 1
        if not ord_10:
            print("gcd(10, x) != 1. Period behavior is pre-periodic.")
        
        # Calculate ord_x(10)
        k = 1
        while pow(10, k, x) != 1:
            k += 1
            if k > x: break
        k_10 = k
        print(f"ord_{x}(10) [Decimal Period Length] = {k_10}")
        
        # 2. Multiplicative Order of 2 mod x (Binary Jump Period)
        k = 1
        while pow(2, k, x) != 1:
            k += 1
            if k > x: break
        k_2 = k
        print(f"ord_{x}(2) [Binary Jump Period Length] = {k_2}")
        
        # 3. Chinese Remainder Theorem Decomposition
        # Finding factors for audit purposes
        factors = []
        d = 2
        temp_x = x
        while d * d <= temp_x:
            if temp_x % d == 0:
                factors.append(d)
                while temp_x % d == 0: temp_x //= d
            d += 1
        if temp_x > 1: factors.append(temp_x)
        
        if len(factors) == 2:
            p, q = factors
            print(f"CRT Decomposition: (Z/{x}Z)* ~= (Z/{p}Z)* x (Z/{q}Z)*")
            kp = 1
            while pow(jump_base, kp, p) != 1: kp += 1
            kq = 1
            while pow(jump_base, kq, q) != 1: kq += 1
            print(f"ord_{p}({jump_base}) = {kp}")
            print(f"ord_{q}({jump_base}) = {kq}")
            print(f"lcm({kp}, {kq}) = {math.lcm(kp, kq)} (Matches k_2: {k_2 == math.lcm(kp, kq)})")
            
            # 4. The 'Nodal Spacing' Claim
            # User claims the factors p, q are 'flanked' or revealed by spacings.
            # Let's check for residues near factors in the orbit.
            print("\n4. ANALYZING ORBIT FOR FACTOR-LEAKING RESIDUES:")
            for n in range(k_2):
                res = pow(jump_base, n, x)
                # If gcd(res-1, x) or gcd(res+1, x) gives a factor
                g_minus = math.gcd(res - 1, x)
                g_plus = math.gcd(res + 1, x)
                
                if 1 < g_minus < x or 1 < g_plus < x:
                    print(f"  n={n}: {jump_base}^{n} mod {x} = {res}")
                    if 1 < g_minus < x: print(f"    FOUND FACTOR via gcd(res-1, {x}): {g_minus}")
                    if 1 < g_plus < x: print(f"    FOUND FACTOR via gcd(res+1, {x}): {g_plus}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Small semi-prime test
    rigorous_audit(77) # 7 * 11
