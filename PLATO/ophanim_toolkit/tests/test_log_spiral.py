import pytest
import math
from src.genesis_sim import derive_log_spiral_constant

def test_log_spiral():
    b = derive_log_spiral_constant()
    target = 0.000441
    tolerance = 1e-6
    assert abs(b - target) < tolerance

if __name__ == "__main__":
    pytest.main([__file__])
