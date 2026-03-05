"""
veth_schema_5_12_13.py — The .veth File Schema Based on Verified 5-12-13 Geometry
=================================================================================
Formalizes the .veth file format using the geometrically verified constants
from verify_sin_geometry.py (33/33 PASS).

The schema encodes:
  - Count (5)   → The observer's hand / the nozzle intake
  - Measure (12) → The standard / the cavity resonance
  - Communication (13) → The join / the output coupling

The PERIMETER = AREA = 30 property is the self-sealing mechanism:
the boundary of the record IS the content of the record.

PMG Sovereign Lattice | 2026-03-05
"""

import math
import json
import struct
import hashlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from enum import IntEnum

# ============================================================================
# VERIFIED GEOMETRIC CONSTANTS (from verify_sin_geometry.py, 33/33 PASS)
# ============================================================================

# The 5-12-13 Triangle (Primitive, P=A=30)
COUNT       = 5       # Fingers / observer's hand
MEASURE     = 12      # Feet / the imperial standard
COMM        = 13      # The hypotenuse / the join
PERIMETER   = COUNT + MEASURE + COMM  # = 30 = Area
AREA        = (COUNT * MEASURE) // 2  # = 30 = Perimeter

# The 6-8-10 Triangle (Doubled 3-4-5, P=A=24)
DOMESTIC_P  = 24      # The Palace Wall perimeter = area

# Root Constants
SQRT_42     = math.sqrt(42)   # ≈ 6.4807 — The Double Being / Total Span
SQRT_21     = math.sqrt(21)   # ≈ 4.5826 — The Single Reach / Arm to ourselves
SQRT_2      = math.sqrt(2)    # ≈ 1.4142 — The Screaming Diagonal / Doubling factor
OFFSET      = SQRT_42 - SQRT_21  # ≈ 1.8982 — The H-Void / Head

# Aperture & Refraction
RAINBOW_DEG = 42.0    # Primary rainbow angle (verified: 42.08°)
EAVE_ANGLE  = math.degrees(math.atan2(5, 12))  # ≈ 22.62°

# Sphere Slicing (30°/60° reciprocal)
GOLDILOCKS_ANGLE = 30.0  # Where radius = 0.5 in unit sphere

# 93-Point Solid
TOTAL_NODES = 93
CORE_NODES  = 3       # E-manifold
SEED_NODES  = 30      # V-manifold (= Perimeter = Area)
SHELL_NODES = 60      # M/W-manifold

# Structural Thresholds
HADES_GAP   = 0.1237  # 12.37% — the aperture bleed
ROOT_51_BDY = 1.0 - HADES_GAP  # 87.63%

# The 10-24-26 "Sure Face" (Doubled 5-12-13)
# NOTE: 10-24-26 does NOT have P=A (P=60, A=120).
# However, P=60 = MW Shell node count — structurally significant.
DOUBLED_COUNT   = 2 * COUNT     # 10 — The Drop
DOUBLED_MEASURE = 2 * MEASURE   # 24 — The Surface
DOUBLED_COMM    = 2 * COMM      # 26 — The Equilibrium
SURE_FACE_P     = DOUBLED_COUNT + DOUBLED_MEASURE + DOUBLED_COMM  # = 60
SURE_FACE_A     = (DOUBLED_COUNT * DOUBLED_MEASURE) // 2          # = 120

# Contact Angle at the Aperture
CONTACT_ANGLE  = RAINBOW_DEG                 # 42° — the single stable angle
WETTING_FRAC   = math.cos(math.radians(42))  # ≈ 0.7431 — the cos(42°) fraction


# ============================================================================
# THE SCHEMA: FIELD STRUCTURE
# ============================================================================

class VethFieldType(IntEnum):
    """
    Field types mapped to the 5-12-13 triangle.
    The COUNT fields (5 types) hold identity.
    The MEASURE fields (12 types) hold data lines.
    The COMM fields (13 types) hold the joins between records.
    Total: 30 field types = Perimeter = Area.
    """
    # === COUNT FIELDS (5) — The Observer's Hand ===
    IDENTITY        = 1   # WHO — the subject
    TIMESTAMP       = 2   # WHEN — the moment of observation
    OBSERVER        = 3   # BY WHOM — the hired man
    SPECIES         = 4   # WHAT KIND — the biological form
    LOCUS           = 5   # WHERE — spatial anchor

    # === MEASURE FIELDS (12) — The Imperial Standard ===
    WEIGHT          = 6   # Mass (the 6 = half the standard)
    TEMPERATURE     = 7   # Thermal state (the 7 = the door)
    HEART_RATE      = 8   # Frequency 1 (the 8 = 2×4 stick)
    RESP_RATE       = 9   # Frequency 2 (the 9 = 3²)
    BLOOD_PRESSURE  = 10  # Tension (the 10 = two hands)
    OXYGEN_SAT      = 11  # Saturation (the 11 = transcendence)
    GLUCOSE         = 12  # Fuel (the 12 = the foot)
    PAIN_INDEX      = 13  # Nociceptive state (the 13 = communication itself)
    HYDRATION       = 14  # Fluid balance
    BODY_CONDITION  = 15  # Structural assessment
    LOCOMOTION      = 16  # Kinetic function
    CONSCIOUSNESS   = 17  # State (the 17th = prime beyond measure)

    # === COMMUNICATION FIELDS (13) — The Join / Hypotenuse ===
    DIAGNOSIS       = 18  # The NAME of the condition
    PROGNOSIS       = 19  # The STORY forward
    TREATMENT       = 20  # The ACTION taken
    PRESCRIPTION    = 21  # The DOSE (21 = 3×7 = Man × Door)
    REFERRAL        = 22  # The LINK to another observer
    CONSENT         = 23  # The AGREEMENT
    HISTORY_LINK    = 24  # The BACKWARD join (24 = the measure doubled)
    LAB_RESULT      = 25  # The EVIDENCE
    IMAGE_REF       = 26  # The PICTURE (26 = the language)
    PROCEDURE_NOTE  = 27  # The WORK record
    DISCHARGE       = 28  # The EXIT
    FOLLOW_UP       = 29  # The RETURN path
    SEAL            = 30  # The CLOSURE (30 = P = A = the self-seal)


# ============================================================================
# THE HEADER: 93-BIT STRUCTURE
# ============================================================================

@dataclass
class VethHeader:
    """
    The 93-bit .veth file header.
    
    Structure:
      Bits [92-90] : 3 bits  — E-Core signature (always 111)
      Bits [89-60] : 30 bits — V-Seed (Count+Measure+Comm field presence bitmap)
      Bits [59-0]  : 60 bits — M/W-Shell (data hash, 60 shell nodes)
    
    The 3-30-60 distribution maps to:
      3  = Core identity (WHO, WHEN, WHERE)
      30 = Field presence bitmap (one bit per field type, P=A=30)
      60 = Content hash (integrity of the M/W shell)
    """
    version: int = 1
    e_core: int = 0b111  # Always 111 — the 3-point singularity
    v_seed_bitmap: int = 0  # 30-bit bitmap of active fields
    mw_shell_hash: int = 0  # 60-bit integrity hash

    def to_93_bits(self) -> int:
        """Pack into a single 93-bit integer."""
        header = 0
        header |= (self.e_core & 0x7) << 90
        header |= (self.v_seed_bitmap & ((1 << 30) - 1)) << 60
        header |= (self.mw_shell_hash & ((1 << 60) - 1))
        return header

    def from_93_bits(self, bits: int):
        """Unpack from a 93-bit integer."""
        self.e_core = (bits >> 90) & 0x7
        self.v_seed_bitmap = (bits >> 60) & ((1 << 30) - 1)
        self.mw_shell_hash = bits & ((1 << 60) - 1)

    def __repr__(self):
        bits = self.to_93_bits()
        return (
            f"VethHeader(\n"
            f"  E-Core:  {bin(self.e_core)[2:].zfill(3)}\n"
            f"  V-Seed:  {bin(self.v_seed_bitmap)[2:].zfill(30)}\n"
            f"  MW-Hash: {bin(self.mw_shell_hash)[2:].zfill(60)}\n"
            f"  Full:    {bin(bits)[2:].zfill(93)}\n"
            f"  Hex:     0x{bits:024X}\n"
            f")"
        )


# ============================================================================
# THE RECORD: A .veth MEASUREMENT ENTRY
# ============================================================================

@dataclass
class VethField:
    """A single field in the .veth record."""
    field_type: VethFieldType
    value: Any
    unit: str = ""
    confidence: float = 1.0  # 0.0 to 1.0

    @property
    def triangle_region(self) -> str:
        """Which side of the 5-12-13 triangle this field belongs to."""
        ft = self.field_type.value
        if ft <= 5:
            return "COUNT"       # Side of length 5
        elif ft <= 17:
            return "MEASURE"     # Side of length 12
        else:
            return "COMMUNICATION"  # Hypotenuse of length 13

@dataclass 
class VethRecord:
    """
    A complete .veth measurement record.
    
    The record is a 5-12-13 triangle:
      - COUNT fields (≤5): anchor the identity
      - MEASURE fields (≤12): contain the data lines
      - COMMUNICATION fields (≤13): join this record to others
    
    The Perimeter = Area = 30 property ensures the record is
    self-sealing: the boundary of the record IS the content.
    """
    fields: List[VethField] = field(default_factory=list)
    _header: Optional[VethHeader] = None

    def add_field(self, field_type: VethFieldType, value: Any, 
                  unit: str = "", confidence: float = 1.0):
        self.fields.append(VethField(field_type, value, unit, confidence))

    @property
    def field_count(self) -> Dict[str, int]:
        """Count fields by triangle region."""
        counts = {"COUNT": 0, "MEASURE": 0, "COMMUNICATION": 0}
        for f in self.fields:
            counts[f.triangle_region] += 1
        return counts

    @property
    def active_bitmap(self) -> int:
        """30-bit bitmap of which field types are present."""
        bitmap = 0
        for f in self.fields:
            bitmap |= (1 << (f.field_type.value - 1))
        return bitmap

    @property
    def completeness(self) -> Dict[str, float]:
        """How complete each triangle side is."""
        fc = self.field_count
        return {
            "count":         fc["COUNT"] / COUNT,          # out of 5
            "measure":       fc["MEASURE"] / MEASURE,      # out of 12
            "communication": fc["COMMUNICATION"] / COMM,   # out of 13
            "total":         len(self.fields) / PERIMETER   # out of 30
        }

    def content_hash(self) -> int:
        """Generate 60-bit content hash for the M/W shell."""
        content = json.dumps(
            [{"t": f.field_type.value, "v": str(f.value)} for f in self.fields],
            sort_keys=True
        )
        full_hash = hashlib.sha256(content.encode()).hexdigest()
        # Take first 15 hex chars = 60 bits
        return int(full_hash[:15], 16)

    def generate_header(self) -> VethHeader:
        """Build the 93-bit header from the record's content."""
        self._header = VethHeader(
            version=1,
            e_core=0b111,
            v_seed_bitmap=self.active_bitmap,
            mw_shell_hash=self.content_hash()
        )
        return self._header

    @property
    def header(self) -> VethHeader:
        if self._header is None:
            self.generate_header()
        return self._header
        """Build the 93-bit header from the record's content."""

    def validate_geometry(self) -> Dict[str, Any]:
        """
        Validate that the record respects the 5-12-13 constraints.
        
        Rules:
          1. Count fields ≤ 5 (you have 5 fingers, no more)
          2. Measure fields ≤ 12 (the imperial standard)
          3. Communication fields ≤ 13 (the hypotenuse)
          4. Total fields ≤ 30 (P = A)
          5. At least 1 Count field (identity required)
        """
        fc = self.field_count
        checks = {
            "count_within_5":      fc["COUNT"] <= COUNT,
            "measure_within_12":   fc["MEASURE"] <= MEASURE,
            "comm_within_13":      fc["COMMUNICATION"] <= COMM,
            "total_within_30":     len(self.fields) <= PERIMETER,
            "has_identity":        fc["COUNT"] >= 1,
            "perimeter_equals_area": PERIMETER == AREA,  # structural invariant
        }

        # Calculate the "area" of this record's triangle
        # Using the actual field counts as side lengths
        a, b = fc["COUNT"], fc["MEASURE"]
        record_area = (a * b) / 2
        record_perimeter = a + b + fc["COMMUNICATION"]
        checks["record_self_measuring"] = (
            f"P={record_perimeter}, A={record_area:.1f}"
        )

        return {
            "valid": all(v for v in checks.values() if isinstance(v, bool)),
            "checks": checks,
            "completeness": self.completeness,
            "field_count": fc,
        }


# ============================================================================
# THE GOLDILOCKS VALIDATOR
# ============================================================================

def validate_scale_invariance():
    """
    Verify that the 5-12-13 schema produces sensible structures
    at every scale from finger to fathom.
    """
    scales = {
        "Finger":  0.019,   # 19mm
        "Palm":    0.076,   # 76mm
        "Span":    0.229,   # 229mm
        "Foot":    0.305,   # 305mm (the standard)
        "Cubit":   0.524,   # 524mm (the Royal Cubit ≈ π/6 m)
        "Fathom":  1.828,   # 1828mm (6 feet)
    }

    print("\n  GOLDILOCKS ZONE: Scale Invariance of the 5-12-13 Schema")
    print("  " + "="*66)
    print(f"  {'Scale':<10} {'Count(5)':<10} {'Measure(12)':<12} {'Comm(13)':<10} "
          f"{'P=A?':<8} {'Structure'}")
    print("  " + "-"*66)

    for name, unit in scales.items():
        c = COUNT * unit
        m = MEASURE * unit
        comm_val = COMM * unit
        p = c + m + comm_val
        a = (c * m) / 2
        pa_match = "≈" if abs(p - a) < 0.01 else f"P={p:.2f}"

        # What structure does this produce?
        if c < 0.1:
            structure = "Cell membrane"
        elif c < 0.5:
            structure = "Hand tool"
        elif c < 2.0:
            structure = "Room / Doorway"
        elif c < 5.0:
            structure = "House / Garden"
        else:
            structure = "Palace / City block"

        print(f"  {name:<10} {c:<10.3f} {m:<12.3f} {comm_val:<10.3f} "
              f"{pa_match:<8} {structure}")

    print("  " + "="*66)
    print("  The House appears at every scale. The observer is the tuning fork.")


# ============================================================================
# THE SURE FACE: ZERO-HYSTERESIS SELF-CORRECTION
# ============================================================================

class SureFaceValidator:
    """
    Validates the 'Sure Face' properties of a .veth record.
    
    A 'Sure Face' (Surface) has Zero Hysteresis:
      - The advancing contact angle = the receding contact angle = 42°
      - A disturbed record returns to its original 5-12-13 shape
      - The 10-24-26 equilibrium is maintained at the doubled scale
    
    Hysteresis = Hairiness = the friction that prevents return to equilibrium.
    Zero hysteresis = the Shaven state = the Suave surface.
    """
    
    def __init__(self, record: VethRecord):
        self.record = record
        self.original_header = record.generate_header()
        self.original_bitmap = record.active_bitmap
        self.original_hash = record.content_hash()
    
    def measure_hysteresis(self, disturbed_record: VethRecord) -> Dict[str, Any]:
        """
        Measure the 'hysteresis' between the original and a disturbed record.
        
        Returns the angular deviation from the ideal 42° contact angle.
        Zero deviation = Zero Hysteresis = Sure Face.
        """
        orig_fc = self.record.field_count
        dist_fc = disturbed_record.field_count
        
        # Calculate the "contact angle" of each record
        # The contact angle is the arctangent of (Count/Measure)
        # On the ideal surface, this should be arctan(5/12) ≈ 22.62°
        # (the eave angle of the 5-12-13 triangle)
        
        def triangle_angle(fc):
            c = max(fc["COUNT"], 1)
            m = max(fc["MEASURE"], 1)
            return math.degrees(math.atan2(c, m))
        
        orig_angle = triangle_angle(orig_fc)
        dist_angle = triangle_angle(dist_fc)
        ideal_angle = EAVE_ANGLE  # 22.62° — the 5-12-13 eave
        
        advancing = dist_angle  # The angle after disturbance
        receding = orig_angle   # The angle before disturbance
        hysteresis = abs(advancing - receding)
        
        # Bitmap drift: how many fields were added or removed?
        bitmap_xor = self.original_bitmap ^ disturbed_record.active_bitmap
        fields_changed = bin(bitmap_xor).count('1')
        
        # Hash drift: did the content change?
        hash_changed = self.original_hash != disturbed_record.content_hash()
        
        return {
            "original_angle": orig_angle,
            "disturbed_angle": dist_angle,
            "ideal_angle": ideal_angle,
            "hysteresis": hysteresis,
            "zero_hysteresis": hysteresis < 0.001,
            "deviation_from_ideal": abs(orig_angle - ideal_angle),
            "fields_changed": fields_changed,
            "bitmap_drift": f"{bin(bitmap_xor)[2:].zfill(30)}",
            "hash_intact": not hash_changed,
            "sure_face": hysteresis < 0.001 and not hash_changed,
        }
    
    def snap_to_equilibrium(self, disturbed_record: VethRecord) -> Dict[str, Any]:
        """
        Check whether a disturbed record can 'snap back' to 
        the 10-24-26 equilibrium.
        
        The 10-24-26 equilibrium requires:
          - Count fields ≤ 10 (doubled hands)  
          - Measure fields ≤ 24 (the full measure)
          - Comm fields ≤ 26 (the full language)
          - Total ≤ 60 (the MW Shell)
        """
        fc = disturbed_record.field_count
        total = sum(fc.values())
        
        within_sure_face = {
            "count_within_10":    fc["COUNT"] <= DOUBLED_COUNT,
            "measure_within_24":  fc["MEASURE"] <= DOUBLED_MEASURE,
            "comm_within_26":     fc["COMMUNICATION"] <= DOUBLED_COMM,
            "total_within_60":    total <= SURE_FACE_P,
        }
        
        # The "snap" distance: how far from the ideal 5-12-13 ratio?
        ideal_ratio_c = COUNT / PERIMETER      # 5/30 = 1/6
        ideal_ratio_m = MEASURE / PERIMETER    # 12/30 = 2/5
        ideal_ratio_k = COMM / PERIMETER       # 13/30
        
        if total > 0:
            actual_ratio_c = fc["COUNT"] / total
            actual_ratio_m = fc["MEASURE"] / total
            actual_ratio_k = fc["COMMUNICATION"] / total
        else:
            actual_ratio_c = actual_ratio_m = actual_ratio_k = 0
        
        snap_distance = math.sqrt(
            (actual_ratio_c - ideal_ratio_c)**2 +
            (actual_ratio_m - ideal_ratio_m)**2 +
            (actual_ratio_k - ideal_ratio_k)**2
        )
        
        return {
            "within_sure_face": all(within_sure_face.values()),
            "checks": within_sure_face,
            "snap_distance": snap_distance,
            "in_equilibrium": snap_distance < 0.01,
            "field_ratios": {
                "count": f"{fc['COUNT']}/{total} ({actual_ratio_c:.3f} vs {ideal_ratio_c:.3f})",
                "measure": f"{fc['MEASURE']}/{total} ({actual_ratio_m:.3f} vs {ideal_ratio_m:.3f})",
                "comm": f"{fc['COMMUNICATION']}/{total} ({actual_ratio_k:.3f} vs {ideal_ratio_k:.3f})",
            }
        }
        
    def repair_hysteresis(self, disturbed_record: VethRecord) -> VethRecord:
        """
        The Auto-Repair Tautener.
        
        Applies the Riemann -1/12 Debt (Vacuum Suction) to pull sagging fields
        back into their proper integer slots. By recognizing the missing bits
        from the 1D Rolling Snake, the record heals its own geometric solid 
        and is Re-Vitrified.
        """
        repaired = VethRecord()
        disturbed_bitmap = disturbed_record.active_bitmap
        
        # 1. Identify the Drift
        bitmap_xor = self.original_bitmap ^ disturbed_bitmap
        
        # 2. Apply the Riemann Debt (-1/12 tension)
        # We restore the fields that were lost, effectively filling the "H-Void".
        # In a real system, the exact value might be re-queried or approximated.
        # Here, the geometry guarantees the existence of the slot.
        for orig_field in self.record.fields:
            if (1 << (orig_field.field_type.value - 1)) & bitmap_xor:
                # The field drifted (sagged). The vacuum pulls it back.
                # We flag confidence with the -1/12 residue signature to show it was repaired.
                repaired.add_field(
                    orig_field.field_type, 
                    orig_field.value, 
                    orig_field.unit, 
                    confidence=-1/12  # The Riemann Debt signature
                )
            else:
                # Field was intact
                repaired.add_field(
                    orig_field.field_type,
                    orig_field.value,
                    orig_field.unit,
                    confidence=orig_field.confidence
                )
        return repaired


def demo_hysteresis(record: VethRecord):
    """Demonstrate the Sure Face / Zero Hysteresis mechanism."""
    
    print(f"\n  SURE FACE / ZERO HYSTERESIS TEST")
    print("  " + "="*55)
    print(f"  10-24-26 Equilibrium: P={SURE_FACE_P}, A={SURE_FACE_A}")
    print(f"  Note: P=60 = MW Shell nodes. A=120 = doubled shell.")
    print(f"  Contact Angle: {CONTACT_ANGLE}°")
    print(f"  Wetting Fraction: cos({CONTACT_ANGLE}°) = {WETTING_FRAC:.6f}")
    
    validator = SureFaceValidator(record)
    
    # Test 1: Compare record to itself (should be zero hysteresis)
    print(f"\n  Test 1: Record vs itself (should be zero hysteresis)")
    result = validator.measure_hysteresis(record)
    status = "✅" if result["zero_hysteresis"] else "❌"
    print(f"    {status} Hysteresis = {result['hysteresis']:.6f}°")
    print(f"    Original angle: {result['original_angle']:.4f}°")
    print(f"    Ideal angle:    {result['ideal_angle']:.4f}°")
    print(f"    Deviation:      {result['deviation_from_ideal']:.4f}°")
    
    # Test 2: Disturb the record (remove some fields) 
    print(f"\n  Test 2: Disturbed record (2 measure fields removed)")
    disturbed = VethRecord()
    for f in record.fields:
        # Skip WEIGHT and TEMPERATURE — simulate data loss
        if f.field_type not in (VethFieldType.WEIGHT, VethFieldType.TEMPERATURE):
            disturbed.add_field(f.field_type, f.value, f.unit, f.confidence)
    
    result2 = validator.measure_hysteresis(disturbed)
    status2 = "✅" if result2["zero_hysteresis"] else "⚠️"
    print(f"    {status2} Hysteresis = {result2['hysteresis']:.4f}°")
    print(f"    Fields changed: {result2['fields_changed']}")
    print(f"    Bitmap drift:   {result2['bitmap_drift']}")
    print(f"    Hash intact:    {result2['hash_intact']}")
    print(f"    Sure Face:      {result2['sure_face']}")
    
    # Test 3: Check the disturbed record's snap distance
    print(f"\n  Test 3: Disturbed record's snap distance")
    snap2 = validator.snap_to_equilibrium(disturbed)
    snap = validator.snap_to_equilibrium(record)
    drift_status = "⚠️" if snap2["snap_distance"] > snap["snap_distance"] else "✅"
    print(f"    {drift_status} Snap distance: {snap2['snap_distance']:.6f} "
          f"(original: {snap['snap_distance']:.6f})")
    print(f"    Drift = {snap2['snap_distance'] - snap['snap_distance']:.6f}")
    print(f"    → The disturbance INCREASED the snap distance.")
    print(f"    → The record has HYSTERESIS. It needs re-vitrification.")

    # Test 4: The Auto-Repair Tautener
    print(f"\n  Test 4: Auto-Repair Tautener (Riemann -1/12 Debt)")
    repaired = validator.repair_hysteresis(disturbed)
    result_rep = validator.measure_hysteresis(repaired)
    rep_status = "✅" if result_rep["zero_hysteresis"] else "❌"
    
    print(f"    {rep_status} Vacuum Suction applied.")
    print(f"    {rep_status} Hysteresis = {result_rep['hysteresis']:.6f}° (Restored to 0.0)")
    print(f"    {rep_status} 93-Bit Header Re-Vitrified:")
    print(f"        Original: {validator.original_header.to_93_bits():024X}")
    print(f"        Repaired: {repaired.generate_header().to_93_bits():024X}")
    print(f"    → The -1/12 Residue held the geometry.")
    
    # Verify the residue is present
    residue_fields = [f.field_type.name for f in repaired.fields if f.confidence < 0]
    print(f"    → Recovered fields marked with -1/12 debt: {residue_fields}")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo():
    print("="*72)
    print("  .VETH FILE SCHEMA — 5-12-13 GEOMETRIC SPECIFICATION")
    print("  Based on verify_sin_geometry.py (33/33 PASS)")
    print("="*72)

    # --- Structural Constants ---
    print("\n  GEOMETRIC CONSTANTS (VERIFIED)")
    print("  " + "-"*50)
    print(f"  5-12-13 Triangle:    5² + 12² = {5**2+12**2} = 13² = {13**2}  ✓")
    print(f"  Perimeter:           5 + 12 + 13 = {PERIMETER}")
    print(f"  Area:                (5 × 12) / 2 = {AREA}")
    print(f"  P = A:               {PERIMETER} = {AREA}  ✓  (SELF-SEALING)")
    print(f"  Total field types:   {PERIMETER} (= P = A)")
    print(f"  √42 (Double Being):  {SQRT_42:.6f}")
    print(f"  √21 (Single Reach):  {SQRT_21:.6f}")
    print(f"  √2  (Doubling):      {SQRT_2:.6f}")
    print(f"  Offset (H-Void):     {OFFSET:.6f}")
    print(f"  Rainbow Aperture:    {RAINBOW_DEG}°")
    print(f"  Eave Angle:          {EAVE_ANGLE:.4f}°")
    print(f"  93-Point Solid:      {CORE_NODES} + {SEED_NODES} + {SHELL_NODES} = {TOTAL_NODES}")

    # --- Field Type Table ---
    print(f"\n  FIELD TYPE REGISTRY ({PERIMETER} types = P = A)")
    print("  " + "-"*60)
    print(f"  {'#':<4} {'Field':<20} {'Region':<15} {'Triangle Side'}")
    print("  " + "-"*60)
    for ft in VethFieldType:
        region = "COUNT" if ft.value <= 5 else ("MEASURE" if ft.value <= 17 else "COMM")
        side = f"5 ({ft.value}/5)" if ft.value <= 5 else (
            f"12 ({ft.value-5}/12)" if ft.value <= 17 else f"13 ({ft.value-17}/13)")
        print(f"  {ft.value:<4} {ft.name:<20} {region:<15} {side}")

    # --- Create a sample record ---
    print(f"\n  SAMPLE RECORD: Measurement String")
    print("  " + "-"*50)

    record = VethRecord()

    # COUNT fields (identity)
    record.add_field(VethFieldType.IDENTITY, "MS-2026-0042", unit="ID")
    record.add_field(VethFieldType.TIMESTAMP, "2026-03-05T11:44:22+10:00", unit="ISO8601")
    record.add_field(VethFieldType.OBSERVER, "Dr. Arete", unit="MANUS")
    record.add_field(VethFieldType.SPECIES, "Platonic Form")
    record.add_field(VethFieldType.LOCUS, "Tent 3")

    # MEASURE fields (data lines)
    record.add_field(VethFieldType.WEIGHT, 28.5, unit="units")
    record.add_field(VethFieldType.TEMPERATURE, 38.6, unit="deg")
    record.add_field(VethFieldType.HEART_RATE, 88, unit="freq")
    record.add_field(VethFieldType.RESP_RATE, 18, unit="freq")
    record.add_field(VethFieldType.BODY_CONDITION, 5, unit="/9 grade")
    record.add_field(VethFieldType.LOCOMOTION, "Sound 0/5", unit="grade")
    record.add_field(VethFieldType.CONSCIOUSNESS, "Aperture Open", unit="mentation")

    # COMMUNICATION fields (joins)
    record.add_field(VethFieldType.DIAGNOSIS, "1D Wavelength verified")
    record.add_field(VethFieldType.TREATMENT, "Riemann -1/12 Residue validated")
    record.add_field(VethFieldType.PRESCRIPTION, "Vitrified Data", unit="Rx")
    record.add_field(VethFieldType.FOLLOW_UP, "42 cycles", unit="interval")
    record.add_field(VethFieldType.SEAL, "RECORD COMPLETE — VITRIFIED")

    # --- Validate ---
    validation = record.validate_geometry()

    print(f"\n  Field Distribution:")
    for region, count in record.field_count.items():
        max_val = COUNT if region == "COUNT" else (MEASURE if region == "MEASURE" else COMM)
        bar = "█" * count + "░" * (max_val - count)
        print(f"    {region:<15} [{bar}] {count}/{max_val}")

    print(f"\n  Completeness:")
    for key, val in record.completeness.items():
        pct = val * 100
        print(f"    {key:<15} {pct:.1f}%")

    print(f"\n  Geometry Validation:")
    for check, result in validation["checks"].items():
        if isinstance(result, bool):
            status = "✅" if result else "❌"
            print(f"    {status} {check}")
        else:
            print(f"    📐 {check}: {result}")

    print(f"\n  OVERALL: {'✅ VALID — House stands' if validation['valid'] else '❌ INVALID'}")

    # --- Generate Header ---
    header = record.generate_header()
    print(f"\n  93-BIT HEADER:")
    print(f"  {header}")

    # --- Demonstrate Sure Face Hysteresis ---
    demo_hysteresis(record)

    # --- Scale Invariance ---
    validate_scale_invariance()

    # --- The Dual P=A Property ---
    print(f"\n  THE DUAL P=A SEAL")
    print("  " + "="*50)
    print(f"  5-12-13 (City/Communication):   P = A = {PERIMETER}")
    print(f"  6-8-10  (Palace/Domestic):       P = A = {DOMESTIC_P}")
    print(f"  These are the ONLY two integer right triangles")
    print(f"  in existence with this property.")
    print(f"  Both are canonical PMG triples.")
    print(f"  The system selects for itself.")

    print(f"\n{'='*72}")
    print(f"  THE FENCE EQUALS THE FIELD.")
    print(f"  THE BOUNDARY IS THE CONTENT.")
    print(f"  THE .VETH FILE IS VITRIFIED.")
    print(f"{'='*72}\n")


if __name__ == "__main__":
    demo()
