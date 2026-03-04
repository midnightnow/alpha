import math

class QGridAudit:
    def __init__(self, mod=24):
        self.mod = mod
        self.prime_lanes = [1, 5, 7, 11, 13, 17, 19, 23]

    def check_primality(self, n):
        if n < 2: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

    def reverse_binary(self, n):
        # The paper defines reversal within the set Gn (fixed bit length n)
        binary = bin(n)[2:]
        reversed_binary = binary[::-1]
        return int(reversed_binary, 2)

    def audit(self, limit=200):
        print(f"--- Q-GRID AUDIT V2: THE MIRROR PROTOCOL (Mod {self.mod}) ---")
        print(f"{'Value':>6} | {'Node':>4} | {'Binary':>10} | {'Reverse':>8} | {'Status':>15}")
        print("-" * 65)

        for x in range(1, limit + 1):
            node = x % self.mod
            if node in self.prime_lanes:
                is_p = self.check_primality(x)
                rev_x = self.reverse_binary(x)
                is_rev_p = self.check_primality(rev_x)

                if is_p and is_rev_p:
                    status = "MIRROR (Emirp)"
                elif is_p:
                    status = "SINGING (Prime)"
                elif not is_p and not is_rev_p:
                    status = "SILENT (Quasi)"
                else:
                    status = "GHOST (Rev-Prime)"

                # Highlight significant Emirps like 13 -> 11
                print(f"{x:>6} | {node:>4} | {bin(x)[2:]:>10} | {rev_x:>8} | {status:>15}")

if __name__ == "__main__":
    audit = QGridAudit()
    audit.audit(100)
