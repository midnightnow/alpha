import pytest
from src.hado_extension import compute_hades_gap, validate_psi

def test_psi_constant():
    psi = compute_hades_gap()
    assert validate_psi(psi), f"Psi {psi} failed PMG tolerance (0.1237 +/- 0.0001)"

if __name__ == "__main__":
    pytest.main([__file__])
