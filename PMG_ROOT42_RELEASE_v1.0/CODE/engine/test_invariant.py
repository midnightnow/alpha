from decimal import Decimal, getcontext
import pytest

from diamond_crystallizer import compute_invariant, load_shell, HADES_GAP

# Fixed precision context for guaranteed identical cross-platform results
getcontext().prec = 28  

EXPECTED_INVARIANT = Decimal("42.000000000")

def test_node_count():
    shell = load_shell("../../ASSETS/hyperdiamond_shell.json")
    assert len(shell) == 93

def test_invariant_exact():
    shell = load_shell("../../ASSETS/hyperdiamond_shell.json")
    invariant = compute_invariant(shell)
    # Binary pass/fail against precision locked Decimal target
    assert invariant == EXPECTED_INVARIANT

def test_hades_gap():
    # Verifying the 12/13.6937 void-to-staff ratio precision
    assert HADES_GAP.quantize(Decimal("0.0001")) == Decimal("0.1237")
