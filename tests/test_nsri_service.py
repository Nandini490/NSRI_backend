import sys
import os

# Add the root directory to sys.path so we can import services
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.nsri_service import NSRIService


def test_sai_both_probabilities():
    """SAI with both WESAD and MMASH probabilities available."""
    print("\n--- Test: SAI with both probabilities ---")
    service = NSRIService()
    result = service.calculate_sai(0.7, 0.5)
    expected = 60.0  # (0.7 + 0.5) / 2 * 100
    print(f"  Input: wesad=0.7, mmash=0.5")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_sai_only_wesad():
    """SAI with only WESAD probability available."""
    print("\n--- Test: SAI with only WESAD ---")
    service = NSRIService()
    result = service.calculate_sai(0.85, None)
    expected = 85.0  # 0.85 / 1 * 100
    print(f"  Input: wesad=0.85, mmash=None")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_sai_only_mmash():
    """SAI with only MMASH probability available."""
    print("\n--- Test: SAI with only MMASH ---")
    service = NSRIService()
    result = service.calculate_sai(None, 0.3)
    expected = 30.0  # 0.3 / 1 * 100
    print(f"  Input: wesad=None, mmash=0.3")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_sai_no_probabilities():
    """SAI returns None when no probabilities are provided."""
    print("\n--- Test: SAI with no probabilities ---")
    service = NSRIService()
    result = service.calculate_sai(None, None)
    print(f"  Input: wesad=None, mmash=None")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_sai_zero_probabilities():
    """SAI correctly handles zero probabilities (not the same as None)."""
    print("\n--- Test: SAI with zero probabilities ---")
    service = NSRIService()
    result = service.calculate_sai(0.0, 0.0)
    expected = 0.0
    print(f"  Input: wesad=0.0, mmash=0.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_sai_max_probabilities():
    """SAI correctly handles maximum probabilities."""
    print("\n--- Test: SAI with max probabilities ---")
    service = NSRIService()
    result = service.calculate_sai(1.0, 1.0)
    expected = 100.0
    print(f"  Input: wesad=1.0, mmash=1.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_sai_rounding():
    """SAI rounds to exactly 2 decimal places."""
    print("\n--- Test: SAI rounding ---")
    service = NSRIService()
    result = service.calculate_sai(0.333, 0.666)
    expected = 49.95  # (0.333 + 0.666) / 2 * 100 = 49.95
    print(f"  Input: wesad=0.333, mmash=0.666")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_pri_normal():
    """PRI with normal normalised inputs."""
    print("\n--- Test: PRI normal calculation ---")
    service = NSRIService()
    result = service.calculate_pri(0.8, 0.3)
    # PRI = 0.6 * 0.8 + 0.4 * (1 - 0.3) = 0.48 + 0.28 = 0.76
    expected = 76.0
    print(f"  Input: hrv=0.8, resting_hr=0.3")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_pri_missing_hrv():
    """PRI returns None when HRV is missing."""
    print("\n--- Test: PRI with missing HRV ---")
    service = NSRIService()
    result = service.calculate_pri(None, 0.5)
    print(f"  Input: hrv=None, resting_hr=0.5")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_pri_missing_resting_hr():
    """PRI returns None when resting HR is missing."""
    print("\n--- Test: PRI with missing resting HR ---")
    service = NSRIService()
    result = service.calculate_pri(0.7, None)
    print(f"  Input: hrv=0.7, resting_hr=None")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_pri_both_missing():
    """PRI returns None when both inputs are missing."""
    print("\n--- Test: PRI with both missing ---")
    service = NSRIService()
    result = service.calculate_pri(None, None)
    print(f"  Input: hrv=None, resting_hr=None")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_pri_boundary_zeros():
    """PRI when both normalised inputs are 0."""
    print("\n--- Test: PRI boundary (both zero) ---")
    service = NSRIService()
    result = service.calculate_pri(0.0, 0.0)
    # PRI = 0.6 * 0.0 + 0.4 * (1 - 0.0) = 0.0 + 0.4 = 0.4
    expected = 40.0
    print(f"  Input: hrv=0.0, resting_hr=0.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_pri_boundary_ones():
    """PRI when both normalised inputs are 1."""
    print("\n--- Test: PRI boundary (both one) ---")
    service = NSRIService()
    result = service.calculate_pri(1.0, 1.0)
    # PRI = 0.6 * 1.0 + 0.4 * (1 - 1.0) = 0.6 + 0.0 = 0.6
    expected = 60.0
    print(f"  Input: hrv=1.0, resting_hr=1.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_pri_rounding():
    """PRI rounds to exactly 2 decimal places."""
    print("\n--- Test: PRI rounding ---")
    service = NSRIService()
    result = service.calculate_pri(0.333, 0.777)
    # PRI = 0.6 * 0.333 + 0.4 * (1 - 0.777)
    #     = 0.1998 + 0.4 * 0.223
    #     = 0.1998 + 0.0892
    #     = 0.289
    expected = round((0.6 * 0.333 + 0.4 * (1 - 0.777)) * 100, 2)
    print(f"  Input: hrv=0.333, resting_hr=0.777")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_rdt_normal():
    """RDT with normal inputs and external stress."""
    print("\n--- Test: RDT normal calculation with external stress ---")
    service = NSRIService()
    result = service.calculate_rdt(0.8, 0.3, 50.0)
    # RDT = [0.3 * (1 - 0.8) + 0.2 * 0.3 + 0.5 * (50/100)] * 100
    #     = [0.3 * 0.2 + 0.2 * 0.3 + 0.5 * 0.5] * 100
    #     = [0.06 + 0.06 + 0.25] * 100
    #     = 0.37 * 100 = 37.0
    expected = 37.0
    print(f"  Input: hrv=0.8, resting_hr=0.3, external_stress=50.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_rdt_with_no_external_stress():
    """RDT with external stress = 0 (no environmental stress)."""
    print("\n--- Test: RDT with no external stress ---")
    service = NSRIService()
    result = service.calculate_rdt(0.8, 0.3, 0.0)
    # RDT = [0.3 * (1 - 0.8) + 0.2 * 0.3 + 0.5 * 0] * 100
    #     = [0.06 + 0.06 + 0] * 100
    #     = 0.12 * 100 = 12.0
    expected = 12.0
    print(f"  Input: hrv=0.8, resting_hr=0.3, external_stress=0.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_rdt_with_max_external_stress():
    """RDT with external stress = 100 (maximum environmental stress)."""
    print("\n--- Test: RDT with max external stress ---")
    service = NSRIService()
    result = service.calculate_rdt(0.8, 0.3, 100.0)
    # RDT = [0.3 * (1 - 0.8) + 0.2 * 0.3 + 0.5 * (100/100)] * 100
    #     = [0.06 + 0.06 + 0.5] * 100
    #     = 0.62 * 100 = 62.0
    expected = 62.0
    print(f"  Input: hrv=0.8, resting_hr=0.3, external_stress=100.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_rdt_external_stress_none():
    """RDT with external stress = None (defaults to 0)."""
    print("\n--- Test: RDT with external stress None (defaults to 0) ---")
    service = NSRIService()
    result = service.calculate_rdt(0.8, 0.3, None)
    # Should default to 0 external stress
    # RDT = [0.3 * (1 - 0.8) + 0.2 * 0.3 + 0] * 100 = 12.0
    expected = 12.0
    print(f"  Input: hrv=0.8, resting_hr=0.3, external_stress=None")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_rdt_missing_hrv():
    """RDT returns None when HRV is missing."""
    print("\n--- Test: RDT with missing HRV ---")
    service = NSRIService()
    result = service.calculate_rdt(None, 0.5, 50.0)
    print(f"  Input: hrv=None, resting_hr=0.5, external_stress=50.0")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_rdt_missing_resting_hr():
    """RDT returns None when resting HR is missing."""
    print("\n--- Test: RDT with missing resting HR ---")
    service = NSRIService()
    result = service.calculate_rdt(0.7, None, 50.0)
    print(f"  Input: hrv=0.7, resting_hr=None, external_stress=50.0")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_rdt_boundary_zeros():
    """RDT when all normalized inputs are 0, no external stress."""
    print("\n--- Test: RDT boundary (zeros, no external) ---")
    service = NSRIService()
    result = service.calculate_rdt(0.0, 0.0, 0.0)
    # RDT = [0.3 * (1 - 0) + 0.2 * 0 + 0] * 100 = 0.3 * 100 = 30.0
    expected = 30.0
    print(f"  Input: hrv=0.0, resting_hr=0.0, external_stress=0.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_rdt_boundary_ones():
    """RDT when all normalized inputs are 1, max external stress."""
    print("\n--- Test: RDT boundary (ones, max external) ---")
    service = NSRIService()
    result = service.calculate_rdt(1.0, 1.0, 100.0)
    # RDT = [0.3 * (1 - 1) + 0.2 * 1 + 0.5 * 1] * 100
    #     = [0 + 0.2 + 0.5] * 100 = 0.7 * 100 = 70.0
    expected = 70.0
    print(f"  Input: hrv=1.0, resting_hr=1.0, external_stress=100.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_nsri_all_values():
    """Final NSRI with all three components available."""
    print("\n--- Test: NSRI with all values ---")
    service = NSRIService()
    result = service.calculate_nsri(60.0, 76.0, 37.0)
    # NSRI = 0.4 * 60 + 0.3 * (100 - 76) + 0.3 * 37
    #      = 24 + 0.3 * 24 + 11.1
    #      = 24 + 7.2 + 11.1 = 42.3
    expected = 42.3
    print(f"  Input: sai=60.0, pri=76.0, rdt=37.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_nsri_missing_sai():
    """NSRI returns None when SAI is missing."""
    print("\n--- Test: NSRI with missing SAI ---")
    service = NSRIService()
    result = service.calculate_nsri(None, 76.0, 37.0)
    print(f"  Input: sai=None, pri=76.0, rdt=37.0")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_nsri_missing_pri():
    """NSRI returns None when PRI is missing."""
    print("\n--- Test: NSRI with missing PRI ---")
    service = NSRIService()
    result = service.calculate_nsri(60.0, None, 37.0)
    print(f"  Input: sai=60.0, pri=None, rdt=37.0")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_nsri_missing_rdt():
    """NSRI returns None when RDT is missing."""
    print("\n--- Test: NSRI with missing RDT ---")
    service = NSRIService()
    result = service.calculate_nsri(60.0, 76.0, None)
    print(f"  Input: sai=60.0, pri=76.0, rdt=None")
    print(f"  Expected: None, Got: {result}")
    assert result is None, f"Expected None, got {result}"
    print("  PASSED")


def test_nsri_boundary_zeros():
    """NSRI when all components are 0 (best case - no stress, good recovery, no external)."""
    print("\n--- Test: NSRI boundary (all zeros) ---")
    service = NSRIService()
    result = service.calculate_nsri(0.0, 0.0, 0.0)
    # NSRI = 0.4 * 0 + 0.3 * (100 - 0) + 0.3 * 0
    #      = 0 + 30 + 0 = 30.0
    expected = 30.0
    print(f"  Input: sai=0.0, pri=0.0, rdt=0.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


def test_nsri_boundary_max():
    """NSRI when all components are at maximum (worst case - max stress, poor recovery, max external)."""
    print("\n--- Test: NSRI boundary (max values) ---")
    service = NSRIService()
    result = service.calculate_nsri(100.0, 100.0, 100.0)
    # NSRI = 0.4 * 100 + 0.3 * (100 - 100) + 0.3 * 100
    #      = 40 + 0 + 30 = 70.0
    expected = 70.0
    print(f"  Input: sai=100.0, pri=100.0, rdt=100.0")
    print(f"  Expected: {expected}, Got: {result}")
    assert result == expected, f"Expected {expected}, got {result}"
    print("  PASSED")


if __name__ == "__main__":
    print("=" * 50)
    print("  NSRIService Tests")
    print("=" * 50)

    test_sai_both_probabilities()
    test_sai_only_wesad()
    test_sai_only_mmash()
    test_sai_no_probabilities()
    test_sai_zero_probabilities()
    test_sai_max_probabilities()
    test_sai_rounding()

    test_pri_normal()
    test_pri_missing_hrv()
    test_pri_missing_resting_hr()
    test_pri_both_missing()
    test_pri_boundary_zeros()
    test_pri_boundary_ones()
    test_pri_rounding()

    test_rdt_normal()
    test_rdt_with_no_external_stress()
    test_rdt_with_max_external_stress()
    test_rdt_external_stress_none()
    test_rdt_missing_hrv()
    test_rdt_missing_resting_hr()
    test_rdt_boundary_zeros()
    test_rdt_boundary_ones()

    test_nsri_all_values()
    test_nsri_missing_sai()
    test_nsri_missing_pri()
    test_nsri_missing_rdt()
    test_nsri_boundary_zeros()
    test_nsri_boundary_max()

    print("\n" + "=" * 50)
    print("  All NSRIService tests PASSED!")
    print("=" * 50)

    print("\n" + "=" * 50)
    print("  All NSRIService tests PASSED!")
    print("=" * 50)
