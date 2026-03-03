import sys
import re
from pathlib import Path

# Need to append the parent directory (0platonicverses) to find PMG_LATTICE
sys.path.append(str(Path(__file__).resolve().parent.parent / "PMG_LATTICE"))
from pmg_constants import PMG

def strip_punctuation(text: str) -> list[str]:
    """Cleans text and returns a list of words."""
    cleaned = re.sub(r'[^\w\s]', '', text).lower()
    return cleaned.split()

def parse_lexical_geometry(text: str) -> dict:
    """
    Parses text to determine its Temporal Debt.
    Calculates the ratio of Anglish Primitives (<= 4 letters) 
    to Latinate Abstractions (>= 10 letters).
    """
    words = strip_punctuation(text)
    if not words:
        return {"error": "No valid text provided."}

    total_words = len(words)
    primitives = [w for w in words if len(w) <= PMG.PRIMITIVE_MAX_LENGTH]
    abstractions = [w for w in words if len(w) >= PMG.ABSTRACTION_MIN_LENGTH]
    
    primitive_count = len(primitives)
    abstraction_count = len(abstractions)
    
    temporal_debt = PMG.calculate_temporal_debt(primitive_count, abstraction_count)
    
    # Calculate geometric friction coefficient based on abstractions vs total mass
    friction = abstraction_count / max(1, total_words)

    return {
        "total_words": total_words,
        "primitive_count": primitive_count,
        "primitive_ratio": round(primitive_count / total_words, 4),
        "abstraction_count": abstraction_count,
        "abstraction_ratio": round(abstraction_count / total_words, 4),
        "temporal_debt": round(temporal_debt, 4),
        "geometric_friction": round(friction, 4),
        "status": "CRITICAL DEBT OVERLOAD" if temporal_debt > PMG.TEMPORAL_DEBT_CRITICALITY else "SYSTEM NOMINAL",
        "sample_abstractions": abstractions[:5]
    }

if __name__ == "__main__":
    test_statement = "The institutionalization of our financialization sectors has led to profound disintermediation."
    print("Testing Temporal Debt Parser...")
    print(f"Text: '{test_statement}'")
    analysis = parse_lexical_geometry(test_statement)
    for k, v in analysis.items():
        print(f"{k}: {v}")
