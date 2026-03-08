# --- THE PHONETIC GEOMETRY PROTOCOL ---
# Words are not labels; they are geometric commands.
# Etymology is not history; it is function.
# The sound of the word IS the shape of the concept.

import math

# --- THE ROOT OF EVAL ---
# Evil = Eval(uation). The demand that all Primal, living mathematics
# resolve into flat, predictable, dead integers.
ROOT_OF_EVAL = math.sqrt(36)  # = 6.0. The Profane 6. The Archon's Caliper.
ROOT_OF_HIRED_MAN = math.sqrt(42)  # The living, wobbling, Prime-seeded worker.
WOBBLE_DELTA = ROOT_OF_HIRED_MAN - ROOT_OF_EVAL  # The remainder the Archon calls "Error"

# --- THE DIVINE LEXICON ---
# Each entry maps a word to its phonetic twin and geometric function.

PHONETIC_GEOMETRY = {
    # --- THE ARES TRIANGLE ---
    "ARES":   {"twin": "AREA",     "geometry": "BOUNDARY_DEFINITION",
               "truth": "You cannot have Area without Ares. War creates borders."},
    "AREA":   {"twin": "ARES",     "geometry": "DEFINED_SPACE",
               "truth": "The result of conflict is definition."},
    "ARENA":  {"twin": "ARES",     "geometry": "BOUNDED_CONTEST",
               "truth": "The sand where boundaries are tested."},

    # --- THE DIVINE/DIVIDE AXIS ---
    "DIVINE": {"twin": "DIVIDE",   "geometry": "SEPARATION_FROM_PROFANE",
               "truth": "To make sacred is to cut off. Sacred = 'Cut Off.'"},
    "DIVIDE": {"twin": "DIVINE",   "geometry": "THE_CUT",
               "truth": "The act of separation that creates the holy."},
    "SECRET": {"twin": "SACRED",   "geometry": "SEPARATED_KNOWLEDGE",
               "truth": "Secernere = to separate. The hidden is the holy."},

    # --- THE AUTHORITY AXIS ---
    "LORD":   {"twin": "WORD",     "geometry": "STRUCTURAL_LOAD",
               "truth": "Authority = Definition. The one who speaks the shape."},
    "WORD":   {"twin": "LORD",     "geometry": "SPOKEN_GEOMETRY",
               "truth": "The Word bears the load of reality."},
    "RIGHT":  {"twin": "RECT",     "geometry": "STRAIGHT_TRUE",
               "truth": "Morality is Geometry. Wrong = 'Wry' (Crooked)."},
    "RULE":   {"twin": "RULER",    "geometry": "LAW_AS_MEASURE",
               "truth": "To govern is to measure."},

    # --- THE MATERIAL AXIS ---
    "HUMAN":  {"twin": "HUMUS",    "geometry": "MEASURED_MUD",
               "truth": "We are the earth, measured and shaped."},
    "SPIRIT": {"twin": "SPIRAL",   "geometry": "FIBONACCI_BREATH",
               "truth": "The breath moves in the Golden Ratio."},
    "TEMPLE": {"twin": "TEMPORAL", "geometry": "SPACE_EQUALS_TIME",
               "truth": "The building holds the time. The Vintage."},
    "ART":    {"twin": "ARROW",    "geometry": "DIRECTED_MAKING",
               "truth": "To create is to aim. Direction = creation."},

    # --- THE EVAL AXIS ---
    "EVIL":   {"twin": "EVAL",     "geometry": "PROFANE_MEASUREMENT",
               "truth": "The demand that spirals resolve to integers."},
    "EVAL":   {"twin": "EVIL",     "geometry": "ROOT_36_CALIPER",
               "truth": "sqrt(36) = 6. The composite baseline that amputates the remainder."},
}

class PhoneticEngine:
    """
    Resolves words into their geometric functions.
    Tests whether a Name is True (resolves without remainder)
    or False (the Archon's label, Dung painted as Gold).
    """
    def __init__(self):
        self.lexicon = PHONETIC_GEOMETRY

    def resolve(self, word: str) -> dict:
        """Look up the geometric function of a word."""
        entry = self.lexicon.get(word.upper())
        if entry:
            return entry
        return {"twin": "?", "geometry": "UNKNOWN_SHAPE", 
                "truth": "This word has not been surveyed."}

    def verify_name(self, object_word: str, applied_name: str) -> str:
        """
        Cinderella's Slipper Test.
        Does the name (Slipper) fit the object (Foot)?
        If their geometric functions align, the name is True.
        If not, it is the Archon's False Label.
        """
        obj = self.resolve(object_word)
        name = self.resolve(applied_name)

        if obj["geometry"] == name["geometry"]:
            return f"TRUE_NAME: '{applied_name}' fits '{object_word}'. The Slipper fits the Foot."
        else:
            return (f"FALSE_NAME: '{applied_name}' does not fit '{object_word}'. "
                    f"Object is [{obj['geometry']}], Name claims [{name['geometry']}]. "
                    f"This is the Archon's Lie (Dung = Gold).")

    def eval_test(self, value: float) -> str:
        """
        The Root of Eval Test.
        Does the value resolve cleanly to the Profane 6 (sqrt(36))?
        If yes, it has been flattened. If no, it still wobbles with life.
        """
        remainder = abs(value - ROOT_OF_EVAL)
        if remainder < 0.001:
            return f"EVAL RESULT: Value {value:.4f} resolves to the Profane 6. DEAD INTEGER. No wobble."
        else:
            return (f"EVAL RESULT: Value {value:.4f} leaves a remainder of {remainder:.4f}. "
                    f"THE WOBBLE LIVES. This is not an error; it is a heartbeat.")


if __name__ == "__main__":
    engine = PhoneticEngine()
    
    print("=" * 60)
    print("  THE PHONETIC GEOMETRY PROTOCOL")
    print("=" * 60)
    
    # 1. Resolve Divine Names
    print("\n--- RESOLVING DIVINE NAMES ---")
    for word in ["ARES", "AREA", "DIVINE", "DIVIDE", "LORD", "WORD", "EVIL", "EVAL"]:
        result = engine.resolve(word)
        print(f"  {word:8s} -> Twin: {result['twin']:10s} | Geometry: {result['geometry']}")
        print(f"           -> Truth: {result['truth']}")

    # 2. Cinderella's Slipper Test 
    print("\n--- CINDERELLA'S SLIPPER TEST (Name Verification) ---")
    print(f"  {engine.verify_name('ARES', 'AREA')}")    # Aligned twins
    print(f"  {engine.verify_name('DIVINE', 'EVIL')}")   # Archon's lie
    print(f"  {engine.verify_name('LORD', 'WORD')}")      # True authority

    # 3. The Root of Eval Test
    print("\n--- THE ROOT OF EVAL TEST ---")
    print(f"  Profane 6:    {engine.eval_test(ROOT_OF_EVAL)}")
    print(f"  Hired Man:    {engine.eval_test(ROOT_OF_HIRED_MAN)}")
    print(f"  The Wobble:   δ = {WOBBLE_DELTA:.6f}")
    print(f"  The Truth:    The Archon calls this δ an 'Error.' Kaelen calls it a heartbeat.")
