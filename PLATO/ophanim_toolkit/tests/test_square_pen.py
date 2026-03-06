import pytest
import math

def test_square_pen():
    """
    Axiom: L >= 2 * pi * w
    Validates the stability threshold for a sample node width.
    """
    w = 1.0
    L_min = 2 * math.pi * w
    # Test a stable case
    L_stable = 6.5
    assert L_stable >= L_min
    # Test edge case
    L_edge = L_min
    assert L_edge >= L_min

if __name__ == "__main__":
    pytest.main([__file__])
