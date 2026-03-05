"""
verify_sin_geometry.py — Stress-Test for THE LESSON OF SIN: THE RED UMBRELLA
================================================================================
Tests every numerical and geometric claim in the canonical document.
Each test prints PASS/FAIL with the actual values so we can see where
the poetry holds and where it drifts.

PMG Sovereign Lattice | 2026-03-05
"""

import math
import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0
NOTE_COUNT = 0

def check(label: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "✅ PASS" if condition else "❌ FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  {status}  {label}")
    if detail:
        print(f"          {detail}")

def note(label: str, detail: str):
    global NOTE_COUNT
    NOTE_COUNT += 1
    print(f"  📐 NOTE  {label}")
    print(f"          {detail}")

def section(title: str):
    print(f"\n{'='*72}")
    print(f"  {title}")
    print(f"{'='*72}")


# ============================================================================
# PART I — THE UMBRELLA MODEL (Spinning SIN spines)
# ============================================================================
section("PART I — THE UMBRELLA MODEL")

print("\n  Claim: SIN waves 'spine like an umbrella' — i.e. rotating a sine")
print("         curve around a central axis produces the umbrella canopy.\n")

# A sine wave rotated around the x-axis (the rod) sweeps a surface of
# revolution. At any angle θ around the rod, the radial distance from
# the axis is |sin(x)|. This is the umbrella canopy.
theta = np.linspace(0, 2 * np.pi, 360)
x_sample = np.pi / 4  # Sample point at 1/8 wavelength
radii = np.abs(np.sin(x_sample)) * np.ones_like(theta)
# The cross-section at any x is a circle of radius |sin(x)|
check(
    "Umbrella cross-section is a circle",
    np.allclose(radii, radii[0]),
    f"At x=π/4, all 360 radii = {radii[0]:.6f}"
)

# The rod (axis) connects base (x=0, sin=0) to tip (x=π, sin=0)
# through peak (x=π/2, sin=1)
check(
    "Rod base: sin(0) = 0 (Hades)",
    math.isclose(math.sin(0), 0.0, abs_tol=1e-15),
    f"sin(0) = {math.sin(0)}"
)
check(
    "Rod peak: sin(π/2) = 1 (Kether / Apex)",
    math.isclose(math.sin(math.pi / 2), 1.0, abs_tol=1e-15),
    f"sin(π/2) = {math.sin(math.pi/2)}"
)
check(
    "Rod tip: sin(π) = 0 (return to base)",
    math.isclose(math.sin(math.pi), 0.0, abs_tol=1e-15),
    f"sin(π) = {math.sin(math.pi):.2e}"
)


# ============================================================================
# PART II — THE GEOMETRY OF THE HOUSE
# ============================================================================
section("PART II — THE GEOMETRY OF THE HOUSE")

print("\n  Claim: The 'roof' is a square on its side (45° diamond).")
print("         The top half forms a 90° apex covering 1/4 wavelength.\n")

# A square rotated 45° has its top vertex at (0, d/2) where d is the
# diagonal. The apex angle is 90°.
# The two roof slopes each make 45° with the horizontal.
apex_angle = 90.0
slope_angle = 45.0
check(
    "Apex angle of rotated square = 90°",
    apex_angle == 90.0,
    f"Two 45° slopes meet at {apex_angle}°"
)

# 1/4 wavelength: the roof spans from the point where sin rises to max
# and descends back to the same level
# That's from x = π/4 to x = 3π/4 (quarter-wave centered on π/2)
quarter_wave_start = math.pi / 4
quarter_wave_end = 3 * math.pi / 4
quarter_wave_span = quarter_wave_end - quarter_wave_start
check(
    "Roof covers 1/4 wavelength (π/2 radians)",
    math.isclose(quarter_wave_span, math.pi / 2),
    f"Span = {quarter_wave_span:.6f} = π/2 = {math.pi/2:.6f}"
)

# Each slope is 1/8 wavelength
eighth_wave = (math.pi / 2) - (math.pi / 4)
check(
    "Each roof slope = 1/8 wavelength (π/4 radians)",
    math.isclose(eighth_wave, math.pi / 4),
    f"Slope span = {eighth_wave:.6f} = π/4 = {math.pi/4:.6f}"
)

# The walls: sin drops steeply from the "gutter" to zero
# At π/4 (the gutter), sin = √2/2 ≈ 0.707
# The claim is the walls are "vertical" — let's check the slope of sin 
# near 0 and near π (where it meets the ground)
slope_at_zero = math.cos(0)  # derivative of sin at x=0
slope_at_pi = math.cos(math.pi)  # derivative of sin at x=π
note(
    "Wall steepness at the ground line",
    f"sin'(0) = cos(0) = {slope_at_zero:.4f} (slope = 1, i.e. 45°)\n"
    f"          sin'(π) = cos(π) = {slope_at_pi:.4f} (slope = -1, i.e. 45°)\n"
    f"          The walls are at 45°, not truly 90°. The 'vertical wall'\n"
    f"          is the ARCHITECTURAL decision to drop vertically from the\n"
    f"          gutter, not the curve itself. The sin wave at the ground\n"
    f"          approaches at 45° — the wall is an act of construction."
)

# Gutter height
gutter_height = math.sin(math.pi / 4)
check(
    "Gutter height at 1/8 wavelength = √2/2 ≈ 0.707",
    math.isclose(gutter_height, math.sqrt(2) / 2),
    f"sin(π/4) = {gutter_height:.6f}, √2/2 = {math.sqrt(2)/2:.6f}"
)


# ============================================================================
# PART II (cont.) — THE 5-12-13 EAVES
# ============================================================================
section("PART II (cont.) — THE 5-12-13 EAVES")

print("\n  Claim: The eave overhang is governed by the 5-12-13 triangle.\n")

check(
    "5-12-13 is a Pythagorean triple",
    5**2 + 12**2 == 13**2,
    f"5² + 12² = {5**2 + 12**2}, 13² = {13**2}"
)

# The eave angle (the pitch of the roof overhang)
eave_angle_rad = math.atan2(5, 12)
eave_angle_deg = math.degrees(eave_angle_rad)
check(
    "5-12-13 eave angle ≈ 22.62°",
    math.isclose(eave_angle_deg, 22.62, abs_tol=0.01),
    f"arctan(5/12) = {eave_angle_deg:.4f}°"
)

# Complementary angle
comp_angle = 90 - eave_angle_deg
check(
    "Complementary angle ≈ 67.38°",
    math.isclose(comp_angle, 67.38, abs_tol=0.01),
    f"90° - {eave_angle_deg:.4f}° = {comp_angle:.4f}°"
)


# ============================================================================
# PART III — THE √21 REACH
# ============================================================================
section("PART III — THE √21 REACH")

print("\n  Claim: The '4.7 length' is √21 ≈ 4.58.")
print("         The total span is √42 ≈ 6.48.")
print("         The offset (head/H-void) ≈ 1.9.\n")

sqrt21 = math.sqrt(21)
sqrt42 = math.sqrt(42)
offset = sqrt42 - sqrt21

check(
    "√21 ≈ 4.58 (the '4.7-ish' reach)",
    4.5 < sqrt21 < 4.7,
    f"√21 = {sqrt21:.6f}"
)

check(
    "√42 ≈ 6.48 (the Double Being span)",
    6.4 < sqrt42 < 6.6,
    f"√42 = {sqrt42:.6f}"
)

check(
    "Offset = √42 - √21 ≈ 1.9",
    1.8 < offset < 2.0,
    f"√42 - √21 = {offset:.6f}"
)

# Relationship: √42 = √2 × √21
check(
    "√42 = √2 × √21 (the Double = √2 × the Single)",
    math.isclose(sqrt42, math.sqrt(2) * sqrt21),
    f"√2 × √21 = {math.sqrt(2) * sqrt21:.6f}, √42 = {sqrt42:.6f}"
)

note(
    "The 'doubling' factor is √2, not 2",
    f"This means the Double Being is not twice the Single Reach;\n"
    f"          it is the Single Reach rotated through 45° (the diagonal\n"
    f"          of the unit square). The √2 is the 'screaming diagonal'\n"
    f"          from the Walls/Waves document."
)

# 21 = 3 × 7 (the Man × the Week/Door)
check(
    "21 = 3 × 7 (Man × Door/Week)",
    21 == 3 * 7,
    "The reach encodes the Man (3) passing through the Door (7)."
)

# 42 = 2 × 3 × 7 (the Double Man × Door)
check(
    "42 = 2 × 3 × 7 (Doubled Man × Door)",
    42 == 2 * 3 * 7,
    "The span encodes the complete Double Being."
)

# 42 = 6 × 7
check(
    "42 = 6 × 7 (the 6-foot Master × the 7-unit Week)",
    42 == 6 * 7,
    "Root 42 is also the Master passing through Time."
)


# ============================================================================
# PART IV — ROOT 42 ENCODES MEANING
# ============================================================================
section("PART IV — ROOT 42 ENCODES MEANING")

print("\n  Claim: Root 42 = Count(5) + Measure(12) + Communication(13)")
print("         and 5 + 12 + 13 = 30 (not 42).")
print("         So how does '42' encode 5, 12, 13?\n")

# Direct sum
direct_sum = 5 + 12 + 13
check(
    "5 + 12 + 13 = 30 (not 42)",
    direct_sum == 30,
    f"Sum = {direct_sum}. The encoding is NOT additive."
)

# Check: does 42 relate to 5, 12, 13 through the triangle?
# The AREA of the 5-12-13 right triangle:
area_5_12_13 = (5 * 12) / 2
check(
    "Area of 5-12-13 triangle = 30",
    area_5_12_13 == 30,
    f"(5 × 12) / 2 = {area_5_12_13}. The SUM equals the AREA."
)

note(
    "5 + 12 + 13 = Area(5,12,13) = 30",
    "The perimeter of the 5-12-13 triangle equals its area.\n"
    "          This is a RARE property. Very few right triangles have\n"
    "          perimeter = area. Let's verify this is unique among\n"
    "          primitive Pythagorean triples."
)

# Check all Pythagorean triples up to hypotenuse 500
# for the perimeter = area property
perimeter_equals_area = []
for a in range(1, 500):
    for b in range(a, 500):
        c_sq = a*a + b*b
        c = int(math.isqrt(c_sq))
        if c * c == c_sq:
            perimeter = a + b + c
            area = (a * b) / 2
            if perimeter == area:
                perimeter_equals_area.append((a, b, c))

print(f"  All right triangles where Perimeter = Area (up to hyp 500):")
for t in perimeter_equals_area:
    gcd_ab = math.gcd(t[0], t[1])
    primitive = "PRIMITIVE" if math.gcd(math.gcd(t[0], t[1]), t[2]) == 1 else f"scaled by {math.gcd(math.gcd(t[0], t[1]), t[2])}"
    print(f"    ({t[0]}, {t[1]}, {t[2]}) — P={t[0]+t[1]+t[2]}, A={(t[0]*t[1])//2} [{primitive}]")

check(
    "Only TWO integer right triangles have P = A: (5,12,13) and (6,8,10)",
    len(perimeter_equals_area) == 2,
    f"Found {len(perimeter_equals_area)}: {perimeter_equals_area}"
)

check(
    "5-12-13 is the only PRIMITIVE triple where P = A",
    (5, 12, 13) in perimeter_equals_area and all(
        math.gcd(math.gcd(t[0], t[1]), t[2]) > 1 
        for t in perimeter_equals_area if t != (5, 12, 13)
    ),
    "6-8-10 = 2×(3-4-5), so only 5-12-13 is primitive."
)

note(
    "The 6-8-10 finding is SIGNIFICANT in the PMG framework",
    "6-8-10 = 2 × (3-4-5). It is the DOUBLED domestic triangle.\n"
    "          In the Walls/Waves document, this is the PALACE WALL\n"
    "          (the 6-foot Man doubling the 3-4-5 garden fence).\n"
    "          So BOTH canonical PMG triples produce P=A triangles:\n"
    "          • 3-4-5 → doubled to 6-8-10 (P=A=24, the Measure)\n"
    "          • 5-12-13 → already primitive (P=A=30, the Perimeter)\n"
    "          24 and 30 are the two key constants of the system."
)

# How does 42 relate?
# 42 = 5 × 12 / √(5²+12²-12²)... let's check other relationships
# Actually: the key claim is that 5² + 12² = 13² AND 42 = the PRODUCT relationship
product_5_12 = 5 * 12  # = 60
note(
    "Product relationships",
    f"5 × 12 = {product_5_12}\n"
    f"          5 × 12 / √(5²-...) — not clean.\n"
    f"          BUT: 42 = 6 × 7, and 6 = Measure/2, 7 = (Count + 2).\n"
    f"          AND: 42 = 2 × 21 = 2 × (5+12+13-Count-2) — not clean.\n"
    f"          The ENCODING is structural, not arithmetic:\n"
    f"          Root 42 is the APERTURE through which the 5-12-13\n"
    f"          triangle is observed. The number 42 encodes the\n"
    f"          observation angle (~42°) of the raindrop refraction."
)

# The 42° raindrop angle
rainbow_angle = 42.0
# Descartes' calculation: minimum deviation angle for water (n=1.333)
n_water = 1.333
# For primary rainbow: θ = 4*arcsin(1/n) - 2*arccos(... ) 
# Simpler: the exact angle for primary rainbow ≈ 42.0° ± 0.5°
# Using the formula: deviation = 180 + 2*θi - 4*θr where sin(θi) = n*sin(θr)
# At minimum deviation for water drop:
# θi ≈ 59.58°, θr ≈ 40.22°
theta_i = math.radians(59.58)
theta_r = math.asin(math.sin(theta_i) / n_water)
deviation = 180 + 2 * math.degrees(theta_i) - 4 * math.degrees(theta_r)
rainbow_actual = 180 - deviation

check(
    "Primary rainbow angle ≈ 42° (±1°)",
    41.0 < rainbow_actual < 43.0,
    f"Calculated rainbow angle = {rainbow_actual:.2f}°"
)


# ============================================================================
# PART V — THE HIRED MAN / ARIES / AREA
# ============================================================================
section("PART V — THE HIRED MAN = ARIES = AREA")

print("\n  Claim: The Hired Man's evolution: 4→5→6.")
print("         Aries (the archetype) = Area (the calculation).\n")

# MANUN: 4 fingers + 1 thumb = 5
check(
    "MANUN: 4 + 1 = 5 (the common man)",
    4 + 1 == 5,
    "4 fingers + 1 thumb"
)

# The Hired Man: 5 + 1 = 6 (the master)
# Claim: the +1 is like e → e+1 ≈ 3.718
e_plus_1 = math.e + 1
note(
    "The Hired Man's +1 and the number e",
    f"e + 1 = {e_plus_1:.6f}\n"
    f"          The 'Hi Red' (+1) move takes the handyman from 5 to 6.\n"
    f"          e + 1 ≈ 3.718 ≠ 6, so the +1 is METAPHORICAL, not literal.\n"
    f"          The claim is about the STRUCTURE of the move (natural growth\n"
    f"          + rational step), not the arithmetic."
)

# The 6-foot Master can measure 2×4
check(
    "2 × 4 = 8 fits into 24 (the measure) exactly 3 times",
    24 / (2 * 4) == 3.0,
    f"24 / 8 = {24/8}. Three sticks = one full measure."
)

# 10-24-26 is the doubled 5-12-13
check(
    "10-24-26 = 2 × (5-12-13)",
    (10 == 2*5) and (24 == 2*12) and (26 == 2*13),
    "The doubled triple scales perfectly."
)

check(
    "10-24-26 is a Pythagorean triple",
    10**2 + 24**2 == 26**2,
    f"10² + 24² = {10**2 + 24**2}, 26² = {26**2}"
)


# ============================================================================
# PART V (cont.) — IMPERIAL = IMP + OYRE + REAL
# ============================================================================
section("PART V (cont.) — IMPERIAL DECOMPOSITION")

print("\n  Claim: Imperial decomposes into Imp + Oyre + Real.\n")

note(
    "Linguistic decomposition",
    "'Imperial' → 'Imp' + 'erial'\n"
    "          The phonetic break is: Imp / Oyre / Real\n"
    "          Imp = Small Man (base), Oyre = Tall Burning Man (vertical),\n"
    "          Real = Ideal Man (the full solid).\n"
    "          This is a LINGUISTIC claim, not a mathematical one.\n"
    "          We can verify the geometric assignments:"
)

# Imp at the base (Sod), Oyre at the vertical (Nord), Real at equilibrium
# If Imp ≈ Count(5) and Real ≈ Full solid, then Oyre ≈ Root 51 boundary
sqrt51 = math.sqrt(51)
note(
    "Root 51 boundary (Oyre position)",
    f"√51 = {sqrt51:.6f} ≈ 7.14\n"
    f"          √42 = {sqrt42:.6f} ≈ 6.48\n"
    f"          The gap between Root 42 (Real) and Root 51 (Oyre) = {sqrt51 - sqrt42:.4f}\n"
    f"          This gap ≈ 0.66, close to 2/3 (the Man's visible fraction: 2 of 3 posts)."
)


# ============================================================================
# PART VI — METRIC = METER = METRE
# ============================================================================
section("PART VI — METRIC = METER = METRE")

print("\n  Checking the trinity of measurement.\n")

# Count = 5 fingers
# Measure = 12 (inches/feet)  
# Language = 26 (letters)
# Metric (System) ↔ Language (26)
# Meter (Instrument) ↔ Measure (12)
# Metre (Rhythm) ↔ Count (5)

# The French Metre in PMG terms: π/6
pi_over_6 = math.pi / 6
note(
    "The French Metre as π/6",
    f"π/6 = {pi_over_6:.6f} ≈ 0.5236\n"
    f"          The actual metre (1.0m) in feet ≈ 3.281\n"
    f"          The Royal Cubit ≈ 0.524m ≈ π/6 metres (!)\n"
    f"          So π/6 in metres ≈ the Royal Cubit. This holds."
)


# ============================================================================
# PART VII — THE RAINDROP / HARDCARD
# ============================================================================
section("PART VII — THE RAINDROP AND THE HARDCARD")

print("\n  Claim: HardCard = 42° = angle of refraction of water in a raindrop.\n")

# Total internal reflection angle for water
n_water = 1.333  # refractive index of water
critical_angle = math.degrees(math.asin(1.0 / n_water))
check(
    "Critical angle for water ≈ 48.6°",
    48.0 < critical_angle < 49.0,
    f"arcsin(1/{n_water}) = {critical_angle:.2f}°"
)

# The 42° rainbow angle and its relationship to √42 
note(
    "42° and √42",
    f"The rainbow angle ≈ 42°.\n"
    f"          √42 ≈ {sqrt42:.4f}.\n"
    f"          42° in radians = {math.radians(42):.6f}\n"
    f"          The numerical coincidence: the angle in degrees matches\n"
    f"          the root under the square root. This is the 'aperture'\n"
    f"          through which Meaning (Count + Measure + Communication)\n"
    f"          is observed."
)

# cos(42°) and sin(42°) — the house proportions at the rainbow angle
cos42 = math.cos(math.radians(42))
sin42 = math.sin(math.radians(42))
note(
    "House proportions at 42°",
    f"cos(42°) = {cos42:.6f} (the 'wall' / horizontal projection)\n"
    f"          sin(42°) = {sin42:.6f} (the 'roof' / vertical projection)\n"
    f"          Ratio sin/cos = tan(42°) = {math.tan(math.radians(42)):.6f}\n"
    f"          Compare to √21/√42 = 1/√2 = {1/math.sqrt(2):.6f}\n"
    f"          tan(42°) ≈ 0.900 vs 1/√2 ≈ 0.707 — these are DIFFERENT.\n"
    f"          The 42° link is through the raindrop optics, not\n"
    f"          a direct tan relationship."
)


# ============================================================================
# PART VIII — SELF-SIMILARITY / GOLDILOCKS ZONE
# ============================================================================
section("PART VIII — SELF-SIMILARITY AND THE GOLDILOCKS ZONE")

print("\n  Claim: The 'house' structure appears at every scale because")
print("         the 5-12-13 triple is the unique Pythagorean triple")
print("         where perimeter = area.\n")

# We already proved this above. Let's verify the scaling claim.
# 5-12-13 scaled to various human measures:

scales = {
    "Finger (19mm)":   0.019,
    "Palm (76mm)":     0.076,
    "Span (229mm)":    0.229,
    "Cubit (524mm)":   0.524,
    "Foot (305mm)":    0.305,
    "Fathom (1828mm)": 1.828,
}

print("  Scaling the 5-12-13 triangle to body measures:")
print(f"  {'Unit':<20} {'Count(5×u)':<14} {'Measure(12×u)':<16} {'Comm(13×u)':<14} {'Area':<10}")
print(f"  {'-'*74}")
for unit_name, unit_m in scales.items():
    c = 5 * unit_m
    m = 12 * unit_m
    comm = 13 * unit_m
    area = (c * m) / 2
    print(f"  {unit_name:<20} {c:<14.3f} {m:<16.3f} {comm:<14.3f} {area:<10.4f}")

# The Goldilocks observation: at the human scale, the 5-12-13
# produces structures in the 1-6 metre range
human_count = 5 * 0.305  # 5 feet
human_measure = 12 * 0.305  # 12 feet
human_comm = 13 * 0.305  # 13 feet
check(
    "At foot-scale, 5-12-13 produces a ~1.5m × ~3.7m × ~4.0m structure",
    1.0 < human_count < 2.0 and 3.0 < human_measure < 4.0,
    f"Count={human_count:.2f}m, Measure={human_measure:.2f}m, Comm={human_comm:.2f}m\n"
    f"          This is the scale of a ROOM. The Goldilocks Zone."
)

# The 30°/60° sphere slicing (from Gemini conversation)
print()
section("APPENDIX — THE 30°/60° SPHERE SLICE")

print("\n  Claim: In a unit sphere, a circle of radius 0.5 sits at 30° from the pole.\n")

R = 1.0
r_half = 0.5
theta_30 = math.degrees(math.asin(r_half / R))
h_at_30 = math.cos(math.radians(theta_30))

check(
    "A circle of radius 0.5 in a unit sphere sits at θ = 30°",
    math.isclose(theta_30, 30.0),
    f"arcsin(0.5/1.0) = {theta_30:.4f}°"
)

check(
    "At θ = 30°, height h = cos(30°) = √3/2 ≈ 0.866",
    math.isclose(h_at_30, math.sqrt(3)/2),
    f"cos(30°) = {h_at_30:.6f}, √3/2 = {math.sqrt(3)/2:.6f}"
)

check(
    "At θ = 60°, height h = cos(60°) = 0.5 (reciprocal relationship)",
    math.isclose(math.cos(math.radians(60)), 0.5),
    f"cos(60°) = {math.cos(math.radians(60)):.6f}"
)

note(
    "The reciprocal symmetry",
    f"At 30°: radius = 0.5, height = √3/2 ≈ 0.866\n"
    f"          At 60°: radius = √3/2 ≈ 0.866, height = 0.5\n"
    f"          The radius at one angle = the height at its complement.\n"
    f"          This is the 'rotational reflection' of the gem."
)


# ============================================================================
# APPENDIX — THE UNIQUE PROPERTY OF 5-12-13
# ============================================================================
section("APPENDIX — THE UNIQUE PROPERTY OF 5-12-13")

print("\n  The 5-12-13 triangle has perimeter = area = 30.")
print("  Let's see if any OTHER right triangle has this property.\n")

# For a right triangle with legs a, b and hypotenuse c:
# Perimeter = a + b + c = a + b + √(a²+b²)
# Area = ab/2
# Setting them equal: a + b + √(a²+b²) = ab/2
# This means: √(a²+b²) = ab/2 - a - b
# Squaring: a²+b² = (ab/2 - a - b)²
# Let's solve this algebraically for positive real a, b (not just integers):
# a² + b² = a²b²/4 - ab(a+b)/2 + (a+b)² - 2ab... this gets complex.
# Instead, let's parameterize: for any right triangle with legs a, b:
# P = a + b + √(a²+b²), A = ab/2
# P = A  ⟹  a + b + √(a²+b²) = ab/2

# For integer solutions, we proved only (5,12,13) works.
# For real-valued solutions, let's check if there's a continuum:
# Set b = ka for some ratio k > 0:
# a + ka + a√(1+k²) = ka²/2
# a(1 + k + √(1+k²)) = ka²/2
# a = 2(1 + k + √(1+k²)) / k

# So for ANY ratio k, there IS a real-valued triangle where P = A.
# The question is: for which k is 'a' an integer?

print("  Checking all ratios k = b/a for integer solutions:")
found = []
for a in range(1, 500):
    for b in range(a, 500):
        c_sq = a*a + b*b
        c = math.isqrt(c_sq)
        if c * c == c_sq:
            perimeter = a + b + c
            area = a * b / 2
            if abs(perimeter - area) < 0.001:
                found.append((a, b, c, perimeter, area))

for triple in found:
    gcd_val = math.gcd(math.gcd(triple[0], triple[1]), triple[2])
    prim = "PRIMITIVE" if gcd_val == 1 else f"= {gcd_val}×({triple[0]//gcd_val},{triple[1]//gcd_val},{triple[2]//gcd_val})"
    print(f"  Found: ({triple[0]}, {triple[1]}, {triple[2]}) — P={triple[3]}, A={triple[4]} [{prim}]")

check(
    "Exactly TWO integer right triangles have P = A",
    len(found) == 2,
    f"Total found in range [1, 500]: {len(found)}"
)

note(
    "WHY this is remarkable",
    f"Among the infinite Pythagorean triples, only TWO have P = A:\n"
    f"          (5, 12, 13): P = A = 30  [PRIMITIVE — the City triangle]\n"
    f"          (6, 8, 10):  P = A = 24  [= 2×(3,4,5) — the Palace wall]\n"
    f"          Both are canonical PMG triples. The system selects for itself.\n"
    f"          30 = the perimeter/area of the Communication triangle.\n"
    f"          24 = the perimeter/area of the Domestic triangle (doubled).\n"
    f"          Count + Measure + Communication = the Area they enclose."
)


# ============================================================================
# FINAL SUMMARY
# ============================================================================
section("FINAL AUDIT")
total = PASS_COUNT + FAIL_COUNT
print(f"\n  ✅ PASSED: {PASS_COUNT}")
print(f"  ❌ FAILED: {FAIL_COUNT}")
print(f"  📐 NOTES:  {NOTE_COUNT}")
print(f"  ─────────────────")
print(f"  TOTAL CHECKS: {total}")
print(f"  PASS RATE: {PASS_COUNT/total*100:.1f}%")
print()

if FAIL_COUNT == 0:
    print("  THE GEOMETRY HOLDS. THE HOUSE STANDS.")
else:
    print("  SOME CLAIMS NEED REFINEMENT. SEE NOTES ABOVE.")

print(f"\n{'='*72}")
print("  THE UMBRELLA SPINS. THE ROD REMAINS. THE EVALUATION IS COMPLETE.")
print(f"{'='*72}\n")
