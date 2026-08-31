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

    print("\n" + "=" * 50)
    print("  All NSRIService tests PASSED!")
    print("=" * 50)
