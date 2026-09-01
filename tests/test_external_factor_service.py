import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.external_factor_service import ExternalFactorService
from unittest.mock import patch, MagicMock


def test_weather_to_stress_extreme_cold():
    """Test weather stress calculation for extreme cold."""
    print("\n--- Test: Weather stress - extreme cold ---")
    service = ExternalFactorService()
    
    weather_data = {
        "main": {"temp": -35},
        "weather": [{"main": "snow"}],
        "wind": {"speed": 5}
    }
    
    stress = service._weather_to_stress(weather_data)
    # Extreme cold (40) + snow (20) = 60
    expected = 60.0
    print(f"  Input: temp=-35°C, snow, light wind")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


def test_weather_to_stress_thunderstorm():
    """Test weather stress calculation for thunderstorm."""
    print("\n--- Test: Weather stress - thunderstorm ---")
    service = ExternalFactorService()
    
    weather_data = {
        "main": {"temp": 20},
        "weather": [{"main": "Thunderstorm"}],
        "wind": {"speed": 18}
    }
    
    stress = service._weather_to_stress(weather_data)
    # Mild temp (5) + thunderstorm (40) + strong wind (15) = 60
    expected = 60.0
    print(f"  Input: temp=20°C, thunderstorm, strong wind (18 m/s)")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


def test_weather_to_stress_ideal():
    """Test weather stress calculation for ideal weather."""
    print("\n--- Test: Weather stress - ideal conditions ---")
    service = ExternalFactorService()
    
    weather_data = {
        "main": {"temp": 22},
        "weather": [{"main": "Clear"}],
        "wind": {"speed": 2}
    }
    
    stress = service._weather_to_stress(weather_data)
    # Mild temp (5) + clear (0) + calm wind (0) = 5
    expected = 5.0
    print(f"  Input: temp=22°C, clear, calm (2 m/s)")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


def test_aqi_to_stress_good():
    """Test AQI stress calculation for good air quality."""
    print("\n--- Test: AQI stress - good quality ---")
    service = ExternalFactorService()
    
    aqi_data = {
        "status": "ok",
        "data": {"aqi": 35}  # Good AQI
    }
    
    stress = service._aqi_to_stress(aqi_data)
    # (35/50) * 10 = 7.0
    expected = 7.0
    print(f"  Input: AQI=35 (good)")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


def test_aqi_to_stress_hazardous():
    """Test AQI stress calculation for hazardous air quality."""
    print("\n--- Test: AQI stress - hazardous ---")
    service = ExternalFactorService()
    
    aqi_data = {
        "status": "ok",
        "data": {"aqi": 350}  # Hazardous
    }
    
    stress = service._aqi_to_stress(aqi_data)
    # Should be capped at 95 for values > 300
    expected = 95.0
    print(f"  Input: AQI=350 (hazardous)")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


def test_alerts_to_stress_no_alerts():
    """Test alert stress calculation with no emergency news."""
    print("\n--- Test: Alert stress - no critical news ---")
    service = ExternalFactorService()
    
    news_data = {
        "articles": [
            {"title": "Sports team wins championship", "description": "Great victory"},
            {"title": "Weather expected to improve", "description": "Sunny days ahead"}
        ]
    }
    
    stress = service._alerts_to_stress(news_data)
    # No critical keywords, should return baseline
    expected = 5.0
    print(f"  Input: Non-critical news articles")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


def test_alerts_to_stress_with_emergency():
    """Test alert stress calculation with emergency news."""
    print("\n--- Test: Alert stress - with emergency ---")
    service = ExternalFactorService()
    
    news_data = {
        "articles": [
            {"title": "Emergency Alert: Major Earthquake Strikes", "description": "Multiple killed in disaster"},
            {"title": "Hurricane Emergency: Evacuations ordered", "description": "Critical alert for residents"}
        ]
    }
    
    stress = service._alerts_to_stress(news_data)
    # Multiple critical keywords, should be higher
    print(f"  Input: Critical emergency articles")
    print(f"  Expected: > 30, Got: {stress}")
    assert stress > 30
    print("  PASSED")


def test_disasters_to_stress_no_disasters():
    """Test disaster stress calculation with no active disasters."""
    print("\n--- Test: Disaster stress - no active disasters ---")
    service = ExternalFactorService()
    
    xml_content = """<?xml version="1.0"?>
    <rss>
        <channel>
            <title>GDACS</title>
        </channel>
    </rss>"""
    
    stress = service._disasters_to_stress(xml_content)
    # No items
    expected = 5.0
    print(f"  Input: No disaster items in feed")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


def test_disasters_to_stress_multiple():
    """Test disaster stress calculation with active disasters."""
    print("\n--- Test: Disaster stress - multiple active ---")
    service = ExternalFactorService()
    
    xml_content = """<?xml version="1.0"?>
    <rss>
        <channel>
            <item><title>Earthquake</title></item>
            <item><title>Flood</title></item>
            <item><title>Hurricane</title></item>
        </channel>
    </rss>"""
    
    stress = service._disasters_to_stress(xml_content)
    # 3 items: 5 + (3 * 10) = 35, but capped at 100
    expected = 35.0
    print(f"  Input: 3 active disaster items")
    print(f"  Expected: {expected}, Got: {stress}")
    assert stress == expected
    print("  PASSED")


@patch('httpx.Client')
def test_get_weather_stress_success(mock_client_class):
    """Test weather API call with mocked response."""
    print("\n--- Test: Get weather stress - mocked API ---")
    
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "main": {"temp": 25},
        "weather": [{"main": "Clouds"}],
        "wind": {"speed": 8}
    }
    mock_client.__enter__.return_value.get.return_value = mock_response
    mock_client_class.return_value = mock_client
    
    service = ExternalFactorService()
    service.weather_api_key = "test_key"
    
    stress = service.get_weather_stress(40.7128, -74.0060)
    
    print(f"  Mocked API call successful")
    print(f"  Got stress score: {stress}")
    assert stress is not None
    print("  PASSED")


@patch('httpx.Client')
def test_get_aqi_stress_failure(mock_client_class):
    """Test AQI API failure handling."""
    print("\n--- Test: Get AQI stress - API failure ---")
    
    mock_client = MagicMock()
    mock_client.__enter__.return_value.get.side_effect = Exception("Connection timeout")
    mock_client_class.return_value = mock_client
    
    service = ExternalFactorService()
    service.aqi_api_key = "test_key"
    
    stress = service.get_aqi_stress(40.7128, -74.0060)
    
    print(f"  API call failed gracefully")
    print(f"  Result: {stress} (expected None)")
    assert stress is None
    print("  PASSED")


def test_calculate_external_stress_score_no_data():
    """Test composite stress calculation with no data available."""
    print("\n--- Test: Composite stress - no data available ---")
    
    service = ExternalFactorService()
    # Clear API keys to prevent real calls
    service.weather_api_key = ""
    service.aqi_api_key = ""
    service.news_api_key = ""
    service.disaster_api_key = ""
    
    stress = service.calculate_external_stress_score(
        latitude=40.7128,
        longitude=-74.0060,
        use_weather=True,
        use_aqi=True,
        use_alerts=True,
        use_disasters=True
    )
    
    print(f"  No API keys configured")
    print(f"  Result: {stress} (expected None)")
    assert stress is None
    print("  PASSED")


if __name__ == "__main__":
    print("=" * 50)
    print("  External Factor Service Tests")
    print("=" * 50)

    test_weather_to_stress_extreme_cold()
    test_weather_to_stress_thunderstorm()
    test_weather_to_stress_ideal()
    
    test_aqi_to_stress_good()
    test_aqi_to_stress_hazardous()
    
    test_alerts_to_stress_no_alerts()
    test_alerts_to_stress_with_emergency()
    
    test_disasters_to_stress_no_disasters()
    test_disasters_to_stress_multiple()
    
    test_get_weather_stress_success()
    test_get_aqi_stress_failure()
    
    test_calculate_external_stress_score_no_data()

    print("\n" + "=" * 50)
    print("  All External Factor Service tests PASSED!")
    print("=" * 50)
