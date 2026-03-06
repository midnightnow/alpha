import pytest
from src.category_mapper import calculate_shear_angle, validate_shear_alignment

def test_shear_angle():
    theta = calculate_shear_angle()
    assert validate_shear_alignment(theta), f"Shear Angle {theta} failed PMG tolerance (39.47 +/- 0.00585)"

if __name__ == "__main__":
    pytest.main([__file__])
