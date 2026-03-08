import re

class LexicalGeometer:
    """
    The Lexical Geometer measures the 'Temporal Debt' of any given text.
    It identifies the ratio of Anglish Primitives (3-4 letter words)
    to Latinate Abstractions (long, complex words) and computes the 
    geometric friction (δ) generated when the text is executed.
    """
    def __init__(self):
        # The base Tensegrity Constant (Slag Baseline)
        self.TENSEGRITY_CONSTANT = 0.1237
        
        # Max comfortable length for an "Anglish Primitive" polygon
        self.PRIMITIVE_MAX_LEN = 4  
        
        # The start of a "Latinate Abstraction" polyhedron
        self.ABSTRACTION_MIN_LEN = 10 
        
        # The geometric friction weight coefficient for unresolved language
        self.ABSTRACTION_WEIGHT = 0.000585

        # Vortex-13 Constants
        self.VORTEX_NODES = 13
        self.IDEAL_SPACING = 360 / self.VORTEX_NODES  # 27.69 degrees
        self.SLACK_THRESHOLD = 0.60  # The 60% Fit Rule
        self.TORQUE_CONSTANT = 5.1    # The 5.1 degree Torque Constant / Slack Buffer

    def compute_phasic_residue(self, word_metadata: list) -> dict:
        """
        Categorizes metabolic residue of a word's vector chain into:
        - SLACK: Intentional Precession Buffer (The Phasic Constant of Play)
        - SLOP: Angular Overflow (The Slope-Drop)
        - SLAG: Static Information Residue (Hades Gap)
        - SLURRY: Kinetic Lattice Failure (Acidification/Collisions)
        
        Input should be a list of dicts with 'angle', 'resonance', and 'collision' keys.
        """
        if not word_metadata:
            return {"Slack": 0, "Slop": 0, "Slag": 0, "Slurry": 0}

        angles = [v.get('angle', 0) for v in word_metadata]
        resonances = [v.get('resonance', 0) for v in word_metadata]
        collisions = [v.get('collision', 0) for v in word_metadata]

        avg_resonance = sum(resonances) / len(resonances)
        
        # SLACK: Intentional buffer; allows for ductus drift and structural folding.
        # It is the "non-coding region" (Intron) of the alphabet.
        slack = max(0, 1 - avg_resonance) if avg_resonance > self.SLACK_THRESHOLD else (1 - self.SLACK_THRESHOLD)

        # SLOP: The 'Slope-Drop'. Deviation beyond ideal 13-node spacing.
        # Repesents refractive overflow or "Desire Path" flourishes.
        total_span = max(angles) - min(angles) if len(angles) > 1 else 0
        slop = max(0, total_span - self.IDEAL_SPACING)

        # SLAG: Static residue (Hades Gap). Low-resonance letters filling the geometric frame.
        # e.g., the bars of E and F that prevent structural lock.
        slag_count = sum(1 for r in resonances if r < self.SLACK_THRESHOLD)
        slag = (slag_count / len(resonances)) * self.TENSEGRITY_CONSTANT

        # SLURRY: Kinetic failures / Acidification of the lattice.
        # Overlap of CW/CCW vectors at high-tension nodes (e.g., 'th', 'st' locks).
        slurry = sum(collisions) / len(word_metadata) if collisions else 0

        return {
            "Slack": round(slack, 4),
            "Slop": round(slop, 4),
            "Slag": round(slag, 4),
            "Slurry": round(slurry, 4),
            "Resilience_Rating": round(slack / (slag + 0.001), 2) # Ratio of Slack to Slag
        }

    def measure_temporal_debt(self, text: str) -> dict:
        """
        Parses the text, counts words by their phonetic geometry,
        and calculates the resulting Temporal Debt (Long Remainders).
        """
        # Clean text and split by word boundaries
        words = re.findall(r'\b[A-Za-z]+\b', text.lower())
        
        if not words:
            return {"status": "VOID", "message": "No input geometry detected."}

        primitives = []
        abstractions = []
        mid_level_words = []
        
        for w in words:
            length = len(w)
            if length <= self.PRIMITIVE_MAX_LEN:
                primitives.append(w)
            elif length >= self.ABSTRACTION_MIN_LEN:
                abstractions.append(w)
            else:
                mid_level_words.append(w)
                
        total_words = len(words)
        primitive_ratio = len(primitives) / total_words
        abstraction_ratio = len(abstractions) / total_words
        
        # Raw geometric friction
        friction_delta = len(abstractions) * self.ABSTRACTION_WEIGHT
        
        if len(abstractions) > 0:
            temporal_debt = friction_delta * (1 + (len(abstractions) / total_words))
        else:
            temporal_debt = 0.0
            
        # Check for Critical Overflow
        buffer_overflow_warning = temporal_debt > self.TENSEGRITY_CONSTANT
        
        # --- Integration of Phasic Residue (Experimental mapping from lexical length to metabolic state) ---
        # Note: In a full implementation, this would use the MechanicalAlphabet to get actual vectors.
        # For this lexical analysis, we approximate residue based on abstraction density.
        mock_residue = {
            "Slack": round(primitive_ratio * self.TORQUE_CONSTANT / 90, 4),
            "Slop": round(friction_delta * 10, 4),
            "Slag": round(abstraction_ratio * self.TENSEGRITY_CONSTANT, 4),
            "Slurry": 0.01 if buffer_overflow_warning else 0.0
        }
        
        return {
            "total_words": total_words,
            "primitives_count": len(primitives),
            "abstractions_count": len(abstractions),
            "primitive_ratio": round(primitive_ratio, 4),
            "abstraction_ratio": round(abstraction_ratio, 4),
            "geometric_friction_delta": round(friction_delta, 6),
            "temporal_debt": round(temporal_debt, 6),
            "metabolic_residue": mock_residue,
            "system_status": "CRITICAL SLURRY DETECTED" if buffer_overflow_warning else "STABLE (ANGISH BEDROCK)",
            "hades_intervention_required": buffer_overflow_warning
        }

    def validate_braid_topology(self, text: str, is_master=True) -> dict:
        """
        Calculates the topological security of the 'Tresses' across a narrative timeline.
        A 'Miss' (e.g. Node 9 sibilance failure, scattered data) is evaluated. 
        If governed by the Mistress (is_master=True), these Misses are doubled 
        and braided into Language (the 26-unit chart), creating tension rather than error.
        """
        words = re.findall(r'\b[A-Za-z]+\b', text.lower())
        if not words:
            return {"status": "VOID"}

        # Node 9 Sibilance (The 'Miss' / Escaping breath / The Mist)
        sibilants = ['s', 'sh', 'th', 'f', 'v', 'z', 'ch']
        miss_count = 0
        total_phonemes = 0

        for w in words:
            total_phonemes += len(w)
            for phoneme in sibilants:
                miss_count += w.count(phoneme)

        raw_miss_ratio = miss_count / total_phonemes if total_phonemes > 0 else 0

        # The Demeter Function: Doubling the 13-Chord to the 26-Chart
        # The Hired Hand (+1 increment) vs The Master/Mistress (x2 scaler)
        if is_master:
            styled_tress_value = miss_count * 2
            # Braid tension in a 26-unit string. We map the raw ratio to the 0.1237 ideal target.
            braid_tension = (raw_miss_ratio) / self.TENSEGRITY_CONSTANT
            scale_status = "10/24/26 GLOBAL LATTICE (MISTRESS BRAID)"
        else:
            styled_tress_value = miss_count + 1
            braid_tension = (raw_miss_ratio * 2) / self.TENSEGRITY_CONSTANT
            scale_status = "5/12/13 REGIONAL GRID (HIRED HAND)"

        # The Hades Gap Check (12.37% slag residue must be managed by the Braid)
        # Optimal tension is 1.0. A loose braid scatters (Mist), a tight braid vitrifies (Slurry).
        tension_variance = abs(1.0 - braid_tension)
        
        # If the variance is greater than the Tensegrity Constant, the braid fails.
        if tension_variance > self.TENSEGRITY_CONSTANT:
            structural_integrity = "COMPROMISED (MIST SCATTERING/VITRIFICATION)"
        else:
            structural_integrity = "SECURE (TOPOLOGICAL TRESS LOCKED)"

        return {
            "raw_miss_count": miss_count,
            "raw_miss_ratio": round(raw_miss_ratio, 4),
            "styled_tress_value": styled_tress_value,
            "scale_status": scale_status,
            "braid_tension_index": round(braid_tension, 4),
            "structural_integrity": structural_integrity,
            "hades_gap_compliance": tension_variance <= self.TENSEGRITY_CONSTANT
        }

    def audit_h4_alphabet_lock(self, text: str) -> dict:
        """
        Validates the 26-Unit Alphabet Lock mapped from the H(4) Quadrisection.
        16 Base Nodes (Marrow): Consonants representing strict matter.
        7 Symmetries (Braid): Grammatical connectors and rhythmic pivots (vowels/bridges).
        3 Pillars (Loom): The Triad (structural anchors like P, D, M, W).
        Checks if the 10^2 + 24^2 = 26^2 scale is supported by the text's topology.
        """
        words = re.findall(r'\b[A-Za-z]+\b', text.lower())
        if not words:
            return {"status": "VOID (NO GEOMETRY)"}

        # 1. Phonetic extraction maps
        pillar_nodes = ['p', 'd', 'm', 'w', 'x', 'z']
        symmetry_nodes = ['a', 'e', 'i', 'o', 'u', 'y']
        
        base_count = 0
        sym_count = 0
        pillar_count = 0
        
        for w in words:
            for char in w:
                if char in pillar_nodes:
                    pillar_count += 1
                elif char in symmetry_nodes:
                    sym_count += 1
                else:
                    base_count += 1

        total_nodes = base_count + sym_count + pillar_count
        if total_nodes == 0:
            total_nodes = 1

        # 2. Scaling Parity calculation 
        # Evaluate if the text supports the thermodynamic weight of 10^2 + 24^2 = 676
        # by checking if the ratio roughly aligns with 16 : 7 : 3
        # Ideal ratios: Base (16/26=61%), Sym (7/26=27%), Pillars (3/26=12%)
        
        base_ratio = base_count / total_nodes
        sym_ratio = sym_count / total_nodes
        pillar_ratio = pillar_count / total_nodes
        
        # Calculate divergence from ideal
        divergence = abs(base_ratio - 16/26) + abs(sym_ratio - 7/26) + abs(pillar_ratio - 3/26)
        
        # Scaling representation
        hired_man_scale = 100 # 10^2
        mobius_clock = 576    # 24^2
        mastery_lock = hired_man_scale + mobius_clock # 676
        
        lock_status = "LOCKED (26^2 PARITY ACHIEVED)" if divergence < 0.25 else "FRACTURED (SLAG FORMATION)"

        return {
            "total_nodes": total_nodes,
            "base_marrow_count": base_count,
            "symmetry_braid_count": sym_count,
            "pillar_loom_count": pillar_count,
            "base_ratio": round(base_ratio, 4),
            "sym_ratio": round(sym_ratio, 4),
            "pillar_ratio": round(pillar_ratio, 4),
            "geometric_divergence": round(divergence, 4),
            "mastery_scale_target": f"{hired_man_scale} (10^2) + {mobius_clock} (24^2) = {mastery_lock} (26^2)",
            "alphabet_lock_status": lock_status
        }

if __name__ == "__main__":
    geometer = LexicalGeometer()
    
    # Test Phasic Residue calculation directly
    mock_vectors = [
        {'angle': 20.0, 'resonance': 0.85, 'collision': 0},
        {'angle': 45.0, 'resonance': 0.70, 'collision': 1},
        {'angle': 60.0, 'resonance': 0.30, 'collision': 0}, # High Slag letter (E/F)
    ]
    print("--- Phasic Residue Analysis (Word Level) ---")
    print(geometer.compute_phasic_residue(mock_vectors))

    # Test Lexical Analysis
    anglish_text = "I saw the sun in the sky and ran to the man to cut the cord."
    print("\n--- Test 1: Primitives Only (High Slack) ---")
    print(geometer.measure_temporal_debt(anglish_text))
    
    roman_text = "The institutionalization of financialization leads to the disintermediation of socioeconomic relationships."
    print("\n--- Test 2: The Latinate Grid (High Slag/Slurry) ---")
    print(geometer.measure_temporal_debt(roman_text))

    print("\n--- Test 3: Braid Validation (Miss to Mistress) ---")
    breath_heavy_text = "She sells seashells by the seashore, the sweeping mist settling on the system."
    print("Hired Hand (Linear Base):", geometer.validate_braid_topology(breath_heavy_text, is_master=False))
    print("Mistress (Doubled Braid):", geometer.validate_braid_topology(breath_heavy_text, is_master=True))
