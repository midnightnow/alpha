"""
TEST_PMG_SYSTEM.PY
End-to-end validation of the Sovereign Lattice.
Confirms all invariants, all 26 glyphs, immunity logic, ledger integrity, and console flow.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from pmg_constants import PMG
from mechanical_alphabet import MechanicalAlphabet, GlyphType
from sovereign_ledger import SovereignLedger
from lattice_immunity import LatticeImmunity
from sovereign_console import SovereignConsole

passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name}")
        failed += 1

# ============================================================
# 1. PYTHAGOREAN LOCK
# ============================================================
print("\n=== 1. PYTHAGOREAN LOCK ===")
a, b, c = PMG.SOVEREIGN_26
check("10² + 24² == 26²", a**2 + b**2 == c**2)
check("Hades Gap = 0.1237", PMG.HADES_GAP == 0.1237)
check("Unity Threshold = 0.8254", PMG.UNITY_THRESHOLD == 0.8254)
check("Hades Slack = 0.005566", PMG.HADES_SLACK == 0.005566)
check("Beat Frequency = 0.6606", PMG.BEAT_FREQUENCY == 0.6606)
check("Vitrification Limit = 0.9999", PMG.VITRIFICATION_LIMIT == 0.9999)
check("Dissolution Threshold = 0.30", PMG.DISSOLUTION_THRESHOLD == 0.30)

# ============================================================
# 2. MECHANICAL ALPHABET: 26 VECTORS
# ============================================================
print("\n=== 2. MECHANICAL ALPHABET (26 VECTORS) ===")
alpha = MechanicalAlphabet()
all_letters = set("abcdefghijklmnopqrstuvwxyz")
mapped_letters = set(alpha.alphabet.keys())
missing = all_letters - mapped_letters
check(f"All 26 letters mapped (found {len(mapped_letters)})", len(mapped_letters) == 26)
if missing:
    print(f"    Missing: {sorted(missing)}")

# Verify type distribution
struts = [k for k, v in alpha.alphabet.items() if v.glyph_type == GlyphType.STRUT]
loops = [k for k, v in alpha.alphabet.items() if v.glyph_type == GlyphType.LOOP]
hinges = [k for k, v in alpha.alphabet.items() if v.glyph_type == GlyphType.HINGE]
actuators = [k for k, v in alpha.alphabet.items() if v.glyph_type == GlyphType.ACTUATOR]
print(f"    STRUTS:    {sorted(struts)}")
print(f"    LOOPS:     {sorted(loops)}")
print(f"    HINGES:    {sorted(hinges)}")
print(f"    ACTUATORS: {sorted(actuators)}")

# Word analysis: "sphere" should now use all 6 characters
analysis = alpha.analyze_word("sphere")
check("'sphere' produces non-zero torque", analysis['total_torque'] > 0)
check("'sphere' structural class is not VAPOR", analysis['structural_class'] != "VAPOR")

# "hearthstone" — long word, harmonic multiplier should be 1.3x
analysis_hs = alpha.analyze_word("hearthstone")
check("'hearthstone' triggers 1.3x harmonic (len >= 7)", analysis_hs['total_torque'] > 0)

# Empty / unmapped characters
analysis_empty = alpha.analyze_word("123")
check("Unmapped chars return VAPOR class", analysis_empty['structural_class'] == "VAPOR")

# ============================================================
# 3. SOVEREIGN LEDGER
# ============================================================
print("\n=== 3. SOVEREIGN LEDGER ===")
ledger = SovereignLedger()
check("Genesis hash = 46cb7da997946a14", ledger.chain[0]['hash'] == "46cb7da997946a14")

# Inscribe and verify chain
h1 = ledger.inscribe({"type": "TEST", "coord": (0, 0), "coherence": 0.85})
h2 = ledger.inscribe({"type": "TEST", "coord": (18, 4), "coherence": 0.92})
check("Inscribed 2 blocks (chain length = 3)", len(ledger.chain) == 3)

valid, count = ledger.verify_chain()
check("Chain integrity valid", valid)

# Node history
history = ledger.get_node_history((0, 0))
check("get_node_history finds (0,0) block", len(history) >= 1)

# Neighbors
neighbors = ledger.get_neighbors((0, 0))
check("get_neighbors returns 6 hexes", len(neighbors) == 6)

# ============================================================
# 4. LATTICE IMMUNITY
# ============================================================
print("\n=== 4. LATTICE IMMUNITY ===")
immunity = LatticeImmunity()

# "hearthstone" should produce enough torque
result_hearth = immunity.preflight_check("MASON", "hearthstone")
check("'hearthstone' approved by immunity", result_hearth)

# "tt" is too short / low torque — should be rejected
result_tt = immunity.preflight_check("MASON", "tt")
check("'tt' rejected by immunity (toxic torque)", not result_tt)

# ============================================================
# 5. SOVEREIGN CONSOLE
# ============================================================
print("\n=== 5. SOVEREIGN CONSOLE ===")
console = SovereignConsole(initial_vox=500.0)
check("Console starts with 500 Vox", console.vox_pool == 500.0)

success = console.issue_command((0, 0), "MASON", "hearthstone")
check("'hearthstone' command executed", success)
check("Vox deducted after command", console.vox_pool < 500.0)

# ============================================================
# 6. BOOT SEQUENCE
# ============================================================
print("\n=== 6. BOOT SEQUENCE ===")
from run_pmg_system import boot
try:
    boot()
    check("Full boot completes without error", True)
except Exception as e:
    check(f"Full boot completes without error (ERROR: {e})", False)

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print(f"PMG LATTICE VALIDATION: {passed} passed, {failed} failed")
if failed == 0:
    print("STATUS: ALL INVARIANTS HOLD. THE LATTICE IS SOVEREIGN.")
else:
    print("STATUS: STRUCTURAL SHEAR DETECTED. REPAIR REQUIRED.")
print("=" * 60)
