
def get_prime_address_table():
    """
    Returns the L1 Prime Sieve: A-Z mapping to Prime Addresses (Pn)
    and their 24-wheel signal status.
    """
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101
    ]
    prime_lanes = {1, 5, 7, 11, 13, 17, 19, 23}
    
    table = {}
    for i in range(1, 27):
        char = chr(i + 64)
        p_addr = primes[i-1]
        residue = i % 24
        if residue == 0: residue = 24
        is_signal = residue in prime_lanes
        table[char] = {
            "ordinal": i,
            "residue": residue,
            "is_signal": is_signal,
            "prime_address": p_addr,
            "reciprocal": round(1/p_addr, 6)
        }
    return table

def scan_word(word):
    """
    Scans a word and identifies Prime Signal letters vs Silt.
    """
    table = get_prime_address_table()
    word = word.upper()
    print(f"WORD SCAN: {word}")
    print("-" * 30)
    
    signal_product = 1
    for char in word:
        if char in table:
            data = table[char]
            status = "✅ [SIGNAL]" if data["is_signal"] else "❌ [SILT]"
            print(f"{char} ({data['ordinal']:2}) | Mod 24: {data['residue']:2} | {status} | P: {data['prime_address']:3}")
            if data["is_signal"]:
                signal_product *= data["prime_address"]
    
    print("-" * 30)
    print(f"SIGNAL PRODUCT: {signal_product}")
    return signal_product

if __name__ == "__main__":
    prime_ordinal_mapping()
    
    # Test Word: MAID
    scan_word("MAID")
    
    # Test Word: MADE
    scan_word("MADE")
