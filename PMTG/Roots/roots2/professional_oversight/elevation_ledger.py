import math

def calculate_professional_premium(labor_input):
    """Calculates the Professional Premium of oversight diagonal logic."""
    # The laborer moves in lines (1)
    # The overseer moves in diagonals (sqrt 2)
    elevated_impact = labor_input * math.sqrt(2)
    return {
        "Labor_Value": labor_input,
        "Professional_Value": round(elevated_impact, 4),
        "The_Irrational_Gap": round(elevated_impact - labor_input, 4)
    }

if __name__ == "__main__":
    import json
    print(json.dumps(calculate_professional_premium(1.0), indent=2))
