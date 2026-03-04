def fibonacci_mod(m, limit):
    fib = [0, 1]
    for i in range(2, limit):
        fib.append((fib[i-1] + fib[i-2]) % m)
    return fib

def digital_root(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

def audit_120_castle():
    m_castle = 120
    m_24 = 24
    m_12 = 12
    m_30 = 30
    
    period = 120 # pi(120) = 120
    sequence_120 = fibonacci_mod(m_castle, period)
    
    print(f"--- THE RHYME OF THE 120-CASTLE (ASYMPTOTIC GOVERNANCE) ---")
    print(f"Pisano Period pi(120): {period}")
    print(f"King's Digital Root: {digital_root(m_castle)} (The Knight's Triad)\n")
    print(f"{'n':>4} | {'Fib(n)%120':>10} | {'Root (mod 9)':>12} | {'Maid Rhyme (Functional Role)'}")
    print("-" * 75)
    
    # Specific points to monitor
    checkpoints = {
        13: {"mod": 12, "meta": "13 mod 12 = 1 (Ordinary World Reset)"},
        23: {"mod": 24, "meta": "23 mod 24 = -1 (Gate of Reflection)"},
        33: {"mod": 30, "meta": "33 mod 30 = 3 (Foundational Knight/Stud)"}
    }
    
    for n in range(period + 1):
        idx = n % period
        val = sequence_120[idx]
        root = digital_root(val)
        
        signif = ""
        if n in checkpoints:
            rem = n % checkpoints[n]['mod']
            signif = f"MAID {n}: {checkpoints[n]['meta']}"
        elif val == 0 and n > 0:
            signif = "CASTLE RESET (O)"
        elif val == 1 and n > 1:
            signif = "UNIT RECOVERY (I)"

        if n in checkpoints or (n % 10 == 0 and n > 0): # Show regular intervals and maids
             print(f"{n:>4} | {val:>10} | {root:>12} | {signif}")

    # Confirm the 120/20 = 6 relationship
    print(f"\n--- SINTERING AUDIT: THE 20-FOLD MAID ---")
    print(f"Modulus 120 / Maid 20 = {120/20} (The Hexagon)")
    print("Conclusion: The 20-fold Maid resides within the Hexagonal Sintering of the King.")

import math
if __name__ == "__main__":
    audit_120_castle()
