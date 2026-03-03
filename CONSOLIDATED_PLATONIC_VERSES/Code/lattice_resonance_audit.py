"""
LATTICE RESONANCE AUDIT
=======================
Verifies the 26-unit Braid's resonance with the 66 Hz carrier wave
AND the 5-12-13 Geofont Ratio for narrative structural integrity.

Two-stage audit:
  Stage 1: Acoustic viability (66 Hz carrier compatibility)
  Stage 2: Geometric integrity (5-12-13 Pythagorean lock)
"""

import math
from typing import Dict, List, Tuple

# ═══════════════════════════════════════════════════════
# CANONICAL CONSTANTS
# ═══════════════════════════════════════════════════════
CARRIER_FREQ = 66.0           # Hz - n=4 geometry carrier wave
HAD_BEAT = 0.660688           # Hz - Hades Beat (keep-alive)
PHI = (1 + 5**0.5) / 2        # Golden Ratio
OUROBOROS_CYCLE = 120         # Ticks to phase-lock

# 26-Unit Braid Structure
MARROW_POINTS = 16            # Base consonants (Node 0)
BRIDGING_SYMMETRIES = 7       # Vowels + bridges (Node 6/9)
CENTRAL_PILLARS = 3           # Anchor pillars (Node 7)
TOTAL_NODES = 26              # H(4) Alphabet Lock

# Acoustic Thresholds
RESONANCE_TOLERANCE = 0.03    # ±3% frequency drift acceptable
INTERFERENCE_THRESHOLD = 0.15 # Max destructive interference ratio

# Geofont 13 Constants
HYPOTENUSE = 13
BASE = 12
HEIGHT = 5


# ═══════════════════════════════════════════════════════
# STAGE 1: ACOUSTIC VIABILITY
# ═══════════════════════════════════════════════════════

class LatticeResonanceAuditor:
    """
    Audits the 26-unit Braid for harmonic compatibility with
    the 66 Hz carrier wave.
    
    calibrated=False: Raw crystallized Braid (Chapter 6 output).
                      Symmetries vibrate at full φ harmonic (destructive).
                      Pillars sit near carrier (no subharmonic lock).
    calibrated=True:  Post-V35 recalibration (Veth's manual tuning).
                      Symmetries damped to φ/2 subharmonic.
                      Pillars locked to carrier/2.
    """

    def __init__(self, calibrated=False):
        self.marrow_resonance = []
        self.symmetry_resonance = []
        self.pillar_resonance = []
        self.interference_patterns = []
        self.calibrated = calibrated

    def calculate_node_frequency(self, node_id: int, node_type: str) -> float:
        if node_type == "marrow":
            # Marrow nodes sit tight around the carrier
            # Spread tightens from /100 (raw) to /300 (calibrated)
            spread = 300 if self.calibrated else 100
            return CARRIER_FREQ * (1 + (node_id % 4) / spread)
        elif node_type == "symmetry":
            if self.calibrated:
                # POST-CALIBRATION: Veth damped the vowels to the φ/2 subharmonic
                # Target: CARRIER * PHI / 2 ≈ 53.4 Hz
                return (CARRIER_FREQ * PHI / 2) * (1 + (node_id % 3) / 200)
            else:
                # PRE-CALIBRATION: Raw vowels vibrate at full φ harmonic
                # Produces ~106.8 Hz — destructive interference with marrow
                return CARRIER_FREQ * PHI / (1 + node_id / 100)
        elif node_type == "pillar":
            if self.calibrated:
                # POST-CALIBRATION: Kaelen locked the anchors to carrier/2
                # Target: 33 Hz subharmonic
                return (CARRIER_FREQ / 2) * (1 + (node_id % 2) / 100)
            else:
                # PRE-CALIBRATION: Pillars float near carrier (no subharmonic)
                # Produces ~60 Hz — 82% drift from target
                return CARRIER_FREQ / (1 + node_id / 10)
        return CARRIER_FREQ

    def measure_harmonic_interference(self, freq1: float, freq2: float) -> float:
        """
        Measures destructive interference between two frequencies.
        Harmonically related frequencies (integer ratios, φ ratios) produce
        LOW interference (constructive resonance). Non-harmonic ratios
        produce HIGH interference (destructive beats).
        """
        if min(freq1, freq2) == 0:
            return 1.0
        ratio = max(freq1, freq2) / min(freq1, freq2)
        
        # Check proximity to harmonic ratios: 1:1, 5:4, 4:3, φ:1, 2:1, 3:1, 2φ:1, φ²:1
        # 5:4 = just major third (the 5-height / 4-base of the 3-4-5 triangle)
        # 4:3 = just perfect fourth (the geometric bridge)
        harmonic_targets = [1.0, 5/4, 4/3, PHI, 2.0, 3.0, 2 * PHI, PHI ** 2]
        
        min_deviation = min(abs(ratio - h) for h in harmonic_targets)
        
        # Deviation from nearest harmonic → interference
        # 0 deviation = 0% interference (perfect harmony)
        # >0.25 deviation = destructive territory
        interference = min(min_deviation / 0.25, 1.0)
        return interference

    def audit_marrow_points(self) -> Dict:
        frequencies = []
        for i in range(MARROW_POINTS):
            freq = self.calculate_node_frequency(i, "marrow")
            frequencies.append(freq)
            self.marrow_resonance.append(freq)
        avg_freq = sum(frequencies) / len(frequencies)
        drift = abs(avg_freq - CARRIER_FREQ) / CARRIER_FREQ
        return {
            "node_count": MARROW_POINTS,
            "average_frequency": avg_freq,
            "carrier_drift": drift,
            "status": "LOCKED" if drift < RESONANCE_TOLERANCE else "DRIFT DETECTED"
        }

    def audit_bridging_symmetries(self) -> Dict:
        frequencies = []
        for i in range(BRIDGING_SYMMETRIES):
            freq = self.calculate_node_frequency(i, "symmetry")
            frequencies.append(freq)
            self.symmetry_resonance.append(freq)
        avg_freq = sum(frequencies) / len(frequencies)
        phi_alignment = abs(avg_freq - (CARRIER_FREQ * PHI / 2)) / (CARRIER_FREQ * PHI / 2)
        return {
            "node_count": BRIDGING_SYMMETRIES,
            "average_frequency": avg_freq,
            "phi_alignment": phi_alignment,
            "status": "LOCKED" if phi_alignment < RESONANCE_TOLERANCE else "DRIFT DETECTED"
        }

    def audit_central_pillars(self) -> Dict:
        frequencies = []
        for i in range(CENTRAL_PILLARS):
            freq = self.calculate_node_frequency(i, "pillar")
            frequencies.append(freq)
            self.pillar_resonance.append(freq)
        avg_freq = sum(frequencies) / len(frequencies)
        subharmonic_lock = abs(avg_freq - (CARRIER_FREQ / 2)) / (CARRIER_FREQ / 2)
        return {
            "node_count": CENTRAL_PILLARS,
            "average_frequency": avg_freq,
            "subharmonic_lock": subharmonic_lock,
            "status": "LOCKED" if subharmonic_lock < RESONANCE_TOLERANCE else "DRIFT DETECTED"
        }

    def calculate_cross_interference(self) -> Dict:
        interference_matrix = []
        for m_freq in self.marrow_resonance:
            for s_freq in self.symmetry_resonance:
                interference_matrix.append(
                    self.measure_harmonic_interference(m_freq, s_freq)
                )
        for m_freq in self.marrow_resonance:
            for p_freq in self.pillar_resonance:
                interference_matrix.append(
                    self.measure_harmonic_interference(m_freq, p_freq)
                )
        for s_freq in self.symmetry_resonance:
            for p_freq in self.pillar_resonance:
                interference_matrix.append(
                    self.measure_harmonic_interference(s_freq, p_freq)
                )
        avg_interference = sum(interference_matrix) / len(interference_matrix)
        max_interference = max(interference_matrix)
        return {
            "average_interference": avg_interference,
            "max_interference": max_interference,
            "status": "SAFE" if max_interference < INTERFERENCE_THRESHOLD else "HAZARD"
        }

    def calculate_hades_beat_coupling(self) -> Dict:
        expected_ratio = HAD_BEAT / CARRIER_FREQ
        ideal_ratio = 0.01
        ratio_drift = abs(expected_ratio - ideal_ratio) / ideal_ratio
        return {
            "hades_beat": HAD_BEAT,
            "carrier_freq": CARRIER_FREQ,
            "actual_ratio": expected_ratio,
            "ideal_ratio": ideal_ratio,
            "ratio_drift": ratio_drift,
            "status": "COUPLED" if ratio_drift < 0.02 else "DECOUPLED"
        }

    def generate_acoustic_report(self) -> Dict:
        marrow = self.audit_marrow_points()
        symmetry = self.audit_bridging_symmetries()
        pillars = self.audit_central_pillars()
        interference = self.calculate_cross_interference()
        coupling = self.calculate_hades_beat_coupling()
        all_locked = (
            marrow["status"] == "LOCKED" and
            symmetry["status"] == "LOCKED" and
            pillars["status"] == "LOCKED" and
            interference["status"] == "SAFE" and
            coupling["status"] == "COUPLED"
        )
        return {
            "marrow_audit": marrow,
            "symmetry_audit": symmetry,
            "pillar_audit": pillars,
            "interference_audit": interference,
            "coupling_audit": coupling,
            "overall_status": "READY FOR UTTERANCE" if all_locked else "RECALIBRATION REQUIRED"
        }


# ═══════════════════════════════════════════════════════
# STAGE 2: GEOFONT 13 GEOMETRIC INTEGRITY
# ═══════════════════════════════════════════════════════

def audit_platonic_lattice(hypotenuse=HYPOTENUSE, base=BASE, height=HEIGHT) -> Dict:
    """
    Verifies the geometric integrity of the Geofont 13 Lattice.
    The primary Shear Line must be exactly arcsin(5/13).
    """
    shear_angle = math.degrees(math.asin(height / hypotenuse))
    complement_angle = 90 - shear_angle
    resonance = (hypotenuse ** 2) == (base ** 2 + height ** 2)
    aperture_width = math.tan(math.radians(shear_angle))

    narrative_shear = 39.4  # The Platonic constant from the narrative

    return {
        "Resonance_Stable": resonance,
        "Shear_Line_Angle": round(shear_angle, 2),
        "Complement_Angle": round(complement_angle, 2),
        "Aperture_Width": round(aperture_width, 4),
        "Book_V_Shear_Target": narrative_shear,
        "Pythagorean_Check": f"{height}^2 + {base}^2 = {height**2} + {base**2} = {height**2 + base**2} = {hypotenuse}^2 = {hypotenuse**2}",
        "Status": "READY FOR REDACTION" if resonance else "GEOMETRIC COLLAPSE"
    }


def audit_ogc13_pentad() -> Dict:
    """
    Verify the OGC-13 Pentad vowel assignments are structurally sound.
    """
    pentad = {
        "A": {"god": "Zeus", "sign": "Leo", "element": "Aether", "role": "Subject"},
        "E": {"god": "Demeter", "sign": "Virgo", "element": "Earth", "role": "Object"},
        "I": {"god": "Apollo", "sign": "Gemini", "element": "Light", "role": "Verb"},
        "O": {"god": "Poseidon", "sign": "Pisces", "element": "Water", "role": "Preposition"},
        "U": {"god": "Hestia", "sign": "Capricorn", "element": "Hearth", "role": "Period/Bridge"},
    }

    triangle_vertices = {"A": "Leo", "O": "Pisces", "H": "Scorpio"}
    pentad_on_vertices = sum(1 for v in triangle_vertices if v in pentad)

    elements = {p["element"] for p in pentad.values()}
    element_coverage = len(elements) / 5

    return {
        "pentad_count": len(pentad),
        "pentad_on_triangle_vertices": pentad_on_vertices,
        "element_coverage": f"{element_coverage:.0%}",
        "syntax_roles_assigned": all(p["role"] for p in pentad.values()),
        "silent_13th": "Omega (Dionysus/Aether) -- Axis Mundi",
        "status": "PENTAD LOCKED" if pentad_on_vertices >= 2 and element_coverage == 1.0 else "PENTAD DRIFT"
    }


# ═══════════════════════════════════════════════════════
# MAIN REPORT
# ═══════════════════════════════════════════════════════

def print_full_audit():
    """Generate both acoustic and geometric audit reports."""

    print("=" * 70)
    print("  LATTICE RESONANCE AUDIT -- 26-UNIT BRAID + GEOFONT 13")
    print("  Combined Acoustic / Geometric Integrity Check")
    print("=" * 70)

    # -- STAGE 1: ACOUSTIC --
    print("\n" + "-" * 70)
    print("  STAGE 1: ACOUSTIC VIABILITY (66 Hz Carrier)")
    print("-" * 70)

    auditor_raw = LatticeResonanceAuditor(calibrated=False)
    report_raw = auditor_raw.generate_acoustic_report()

    print("\n  ╔═══ PRE-CALIBRATION (Raw Crystallized Braid, Ch6) ═══╗")

    m = report_raw["marrow_audit"]
    print(f"\n  +-- MARROW POINTS ({m['node_count']} Base Consonants)")
    print(f"  |   Avg Frequency: {m['average_frequency']:.4f} Hz")
    print(f"  |   Carrier Drift: {m['carrier_drift']:.4%}")
    print(f"  +-- Status: {m['status']}")

    s = report_raw["symmetry_audit"]
    print(f"\n  +-- BRIDGING SYMMETRIES ({s['node_count']} Vowels/Bridges)")
    print(f"  |   Avg Frequency: {s['average_frequency']:.4f} Hz")
    print(f"  |   Phi Alignment: {s['phi_alignment']:.4%}")
    print(f"  +-- Status: {s['status']}")

    p = report_raw["pillar_audit"]
    print(f"\n  +-- CENTRAL PILLARS ({p['node_count']} Anchors)")
    print(f"  |   Avg Frequency: {p['average_frequency']:.4f} Hz")
    print(f"  |   Subharmonic Lock: {p['subharmonic_lock']:.4%}")
    print(f"  +-- Status: {p['status']}")

    i = report_raw["interference_audit"]
    print(f"\n  +-- CROSS-INTERFERENCE")
    print(f"  |   Avg Interference: {i['average_interference']:.4%}")
    print(f"  |   Max Interference: {i['max_interference']:.4%}")
    print(f"  +-- Status: {i['status']}")

    c = report_raw["coupling_audit"]
    print(f"\n  +-- HADES BEAT COUPLING ({c['hades_beat']} Hz <-> {c['carrier_freq']} Hz)")
    print(f"  |   Ratio: {c['actual_ratio']:.6f} (ideal: {c['ideal_ratio']})")
    print(f"  |   Drift: {c['ratio_drift']:.6%}")
    print(f"  +-- Status: {c['status']}")

    print(f"\n  > PRE-CALIBRATION RESULT: {report_raw['overall_status']}")

    # -- POST-CALIBRATION (V35 Recalibration Applied) --
    print("\n  ╔═══ POST-CALIBRATION (V35 Recalibration, Ch7) ═══╗")

    auditor_cal = LatticeResonanceAuditor(calibrated=True)
    report = auditor_cal.generate_acoustic_report()

    m = report["marrow_audit"]
    print(f"\n  +-- MARROW POINTS ({m['node_count']} Base Consonants)")
    print(f"  |   Avg Frequency: {m['average_frequency']:.4f} Hz")
    print(f"  |   Carrier Drift: {m['carrier_drift']:.4%}")
    print(f"  +-- Status: {m['status']}")

    s = report["symmetry_audit"]
    print(f"\n  +-- BRIDGING SYMMETRIES ({s['node_count']} Vowels/Bridges)")
    print(f"  |   Avg Frequency: {s['average_frequency']:.4f} Hz")
    print(f"  |   Phi Alignment: {s['phi_alignment']:.4%}")
    print(f"  +-- Status: {s['status']}")

    p = report["pillar_audit"]
    print(f"\n  +-- CENTRAL PILLARS ({p['node_count']} Anchors)")
    print(f"  |   Avg Frequency: {p['average_frequency']:.4f} Hz")
    print(f"  |   Subharmonic Lock: {p['subharmonic_lock']:.4%}")
    print(f"  +-- Status: {p['status']}")

    i = report["interference_audit"]
    print(f"\n  +-- CROSS-INTERFERENCE")
    print(f"  |   Avg Interference: {i['average_interference']:.4%}")
    print(f"  |   Max Interference: {i['max_interference']:.4%}")
    print(f"  +-- Status: {i['status']}")

    c = report["coupling_audit"]
    print(f"\n  +-- HADES BEAT COUPLING ({c['hades_beat']} Hz <-> {c['carrier_freq']} Hz)")
    print(f"  |   Ratio: {c['actual_ratio']:.6f} (ideal: {c['ideal_ratio']})")
    print(f"  |   Drift: {c['ratio_drift']:.6%}")
    print(f"  +-- Status: {c['status']}")

    print(f"\n  > POST-CALIBRATION RESULT: {report['overall_status']}")

    # -- STAGE 2: GEOMETRIC --
    print("\n" + "-" * 70)
    print("  STAGE 2: GEOFONT 13 GEOMETRIC INTEGRITY (5-12-13)")
    print("-" * 70)

    geom = audit_platonic_lattice()
    print(f"\n  +-- PYTHAGOREAN CHECK")
    print(f"  |   {geom['Pythagorean_Check']}")
    print(f"  |   Resonance Stable: {geom['Resonance_Stable']}")
    print(f"  +-- Status: {geom['Status']}")

    print(f"\n  +-- SHEAR LINE ANALYSIS")
    print(f"  |   Primary Angle: {geom['Shear_Line_Angle']} deg")
    print(f"  |   Complement: {geom['Complement_Angle']} deg")
    print(f"  |   Aperture Width: {geom['Aperture_Width']}")
    print(f"  |   Book V Target: {geom['Book_V_Shear_Target']} deg")
    print(f"  +-- Hypotenuse: 13 (Language)")

    pentad = audit_ogc13_pentad()
    print(f"\n  +-- OGC-13 PENTAD AUDIT")
    print(f"  |   Vowel Count: {pentad['pentad_count']}")
    print(f"  |   Vertices Occupied: {pentad['pentad_on_triangle_vertices']}/3")
    print(f"  |   Element Coverage: {pentad['element_coverage']}")
    print(f"  |   Syntax Roles: {'YES' if pentad['syntax_roles_assigned'] else 'NO'}")
    print(f"  |   Silent 13th: {pentad['silent_13th']}")
    print(f"  +-- Status: {pentad['status']}")

    print(f"\n  > STAGE 2 RESULT: {geom['Status']}")

    # -- FINAL --
    print("\n" + "=" * 70)
    overall = "MASTERY LOCK CONFIRMED" if (
        report['overall_status'] == "READY FOR UTTERANCE" and
        geom['Status'] == "READY FOR REDACTION" and
        pentad['status'] == "PENTAD LOCKED"
    ) else "RECALIBRATION REQUIRED"
    print(f"  FINAL STATUS: {overall}")
    print("=" * 70)

    if overall == "MASTERY LOCK CONFIRMED":
        print("\n  [OK] Acoustic viability: CONFIRMED")
        print("  [OK] Geometric integrity: CONFIRMED")
        print("  [OK] Pentad syntax: CONFIRMED")
        print("  [OK] Chapter 7 First Utterance: CLEARED")
        print("  [OK] Book III transition: SAFE")
    else:
        print("\n  [!!] RECALIBRATION REQUIRED before narrative execution.")

    return report, geom, pentad


if __name__ == "__main__":
    print_full_audit()
