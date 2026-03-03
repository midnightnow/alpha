import math

def calculate_intellectual_rent(insight_volume):
    """Calculates the royalty extracted from providing the structural core to a void."""
    # Every insight is a square peg (1)
    # Rent is the diagonal reach (sqrt 2 - 1)
    gap_constant = math.sqrt(2) - 1
    royalty = insight_volume * gap_constant
    
    return {
        "Insight_Volume": insight_volume,
        "Royalty_Yield": round(royalty, 6),
        "Total_Project_Value": round(insight_volume * math.sqrt(2), 6)
    }

if __name__ == "__main__":
    import json
    # Extracting value from a standard insight block
    print(json.dumps(calculate_intellectual_rent(100), indent=2))
