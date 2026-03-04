import math

class IcositetragonMapper:
    """
    Maps structural integers onto the 24-point Icositetragon (Counting House)
    to determine whether they land on Prime Moduli (King's nodes) or 
    Composite/Divisible nodes (Maid's/Structural nodes).
    
    Register 1 (Math Bedrock):
    - 24-Modulus isolates primes > 3 into 8 specific residue classes.
    - These 8 classes are coprime to 24.
    """

    def __init__(self):
        self.modulus = 24
        self.prime_moduli = {1, 5, 7, 11, 13, 17, 19, 23}
        self.maid_nodes = {3, 6, 9, 12, 15, 18, 21, 24} # Multiples of 3 (digital root markers)
        self.even_nodes = {2, 4, 8, 10, 14, 16, 20, 22} # Non-3 evens

    def map_value(self, value: int):
        """Maps an integer value to its position on the 24-wheel."""
        # Map onto 1 to 24, where 0 mod 24 is represented as 24
        node = value % self.modulus
        if node == 0:
            node = 24
            
        return node

    def identify_node(self, node: int) -> str:
        """Categorizes the node into the Platonic structure."""
        if node in self.prime_moduli:
            return "KING'S NODE (Prime Residue Class - Cohort of the 8)"
        elif node in self.maid_nodes:
            return "MAID'S NODE (Multiple of 3 / Digital Root Anchor)"
        elif node in self.even_nodes:
            return "STRUCTURAL NODE (Even / Non-Prime)"
        else:
            return "UNKNOWN (Error in mapping)"

    def analyze_interference(self, root_a: int, root_b: int) -> dict:
        """
        Analyzes the modulo 24 positions and the interference (difference/sum).
        """
        node_a = self.map_value(root_a)
        node_b = self.map_value(root_b)
        
        diff = abs(root_a - root_b)
        node_diff = self.map_value(diff)
        
        return {
            f"Root {root_a}": {
                "Position": node_a,
                "Degrees": (360 / 24) * node_a,
                "Category": self.identify_node(node_a)
            },
            f"Root {root_b}": {
                "Position": node_b,
                "Degrees": (360 / 24) * node_b,
                "Category": self.identify_node(node_b)
            },
            f"Interference (Delta {diff})": {
                "Position": node_diff,
                "Degrees": (360 / 24) * node_diff,
                "Category": self.identify_node(node_diff)
            }
        }

if __name__ == "__main__":
    mapper = IcositetragonMapper()
    
    # Testing the proposed "Root 42" and "Root 51"
    print("--- Register 1 Verification: Root 42 & Root 51 ---")
    results = mapper.analyze_interference(42, 51)
    
    for key, data in results.items():
        print(f"\n{key}:")
        print(f"  Mod 24 Node: {data['Position']}")
        print(f"  Angle:       {data['Degrees']}°")
        print(f"  Identity:    {data['Category']}")
