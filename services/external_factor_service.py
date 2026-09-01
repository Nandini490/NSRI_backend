"""
External factor service for obtaining environmental stressor data.

Supports:
- Weather conditions
- Air Quality Index (AQI)
- News and emergency alerts
- Flood/disaster alerts

All external data is converted to a 0-100 stress score scale.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ExternalFactorService:
    """Service to fetch and aggregate external environmental stress factors."""

    def __init__(self):
        # API endpoints (configurable via environment variables)
        self.weather_api_key = os.getenv("WEATHER_API_KEY", "")
        self.weather_api_url = os.getenv("WEATHER_API_URL", "https://api.openweathermap.org/data/2.5")

        self.aqi_api_key = os.getenv("AQI_API_KEY", "")
        self.aqi_api_url = os.getenv("AQI_API_URL", "https://api.waqi.info")

        self.news_api_key = os.getenv("NEWS_API_KEY", "")
        self.news_api_url = os.getenv("NEWS_API_URL", "https://newsapi.org/v2")

        self.disaster_api_key = os.getenv("DISASTER_API_KEY", "")
        self.disaster_api_url = os.getenv("DISASTER_API_URL", "https://api.gdacs.org")

    def get_weather_stress(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> Optional[float]:
        """
        Fetch weather data and convert to stress score (0-100).

        Parameters:
        - latitude, longitude: Location coordinates

        Returns:
        - Stress score 0-100 (None if unavailable)
        - Factors: temperature extremes, severe weather, storms, etc.
        """
        if not self.weather_api_key or not latitude or not longitude:
            return None

        try:
            import httpx

            url = f"{self.weather_api_url}/weather"
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.weather_api_key,
                "units": "metric"
            }

            with httpx.Client(timeout=5.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            # Convert weather to stress score
            stress = self._weather_to_stress(data)
            logger.info(f"Weather stress score: {stress}")
            return stress

        except Exception as e:
            logger.warning(f"Failed to fetch weather data: {e}")
            return None

    def get_aqi_stress(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> Optional[float]:
        """
        Fetch Air Quality Index and convert to stress score (0-100).

        Parameters:
        - latitude, longitude: Location coordinates

        Returns:
        - Stress score 0-100 (None if unavailable)
        - Higher AQI = higher stress
        """
        if not self.aqi_api_key or not latitude or not longitude:
            return None

        try:
            import httpx

            # WAQI API uses station approach; use geo coordinates
            url = f"{self.aqi_api_url}/feed/geo:{latitude};{longitude}/"
            params = {"token": self.aqi_api_key}

            with httpx.Client(timeout=5.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            # Convert AQI to stress score
            stress = self._aqi_to_stress(data)
            logger.info(f"AQI stress score: {stress}")
            return stress

        except Exception as e:
            logger.warning(f"Failed to fetch AQI data: {e}")
            return None

    def get_alert_stress(self) -> Optional[float]:
        """
        Fetch news/emergency alerts and convert to stress score (0-100).

        Returns:
        - Stress score 0-100 (None if unavailable)
        - Higher = more critical alerts
        """
        if not self.news_api_key:
            return None

        try:
            import httpx

            url = f"{self.news_api_url}/top-headlines"
            params = {
                "q": "emergency OR alert OR disaster OR flood OR hurricane OR earthquake",
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.news_api_key,
                "pageSize": 5
            }

            with httpx.Client(timeout=5.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            # Convert news alerts to stress score
            stress = self._alerts_to_stress(data)
            logger.info(f"Alert stress score: {stress}")
            return stress

        except Exception as e:
            logger.warning(f"Failed to fetch alert data: {e}")
            return None

    def get_disaster_stress(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> Optional[float]:
        """
        Fetch flood/disaster alerts and convert to stress score (0-100).

        Parameters:
        - latitude, longitude: Location coordinates

        Returns:
        - Stress score 0-100 (None if unavailable)
        - Based on proximity to active disasters
        """
        if not self.disaster_api_key or not latitude or not longitude:
            return None

        try:
            import httpx

            url = f"{self.disaster_api_url}/gdacs/rss"
            params = {
                "category": "flood,earthquake,hurricane,volcano",
                "limit": 10
            }

            with httpx.Client(timeout=5.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                # GDACS returns RSS, parse differently
                # For MVP, treat as simple check
                stress = self._disasters_to_stress(response.text)
                logger.info(f"Disaster stress score: {stress}")
                return stress

        except Exception as e:
            logger.warning(f"Failed to fetch disaster data: {e}")
            return None

    def calculate_external_stress_score(
        self,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        use_weather: bool = True,
        use_aqi: bool = True,
        use_alerts: bool = True,
        use_disasters: bool = True
    ) -> Optional[float]:
        """
        Calculate composite external stress score from all available data sources.

        Parameters:
        - latitude, longitude: Location coordinates
        - use_weather, use_aqi, use_alerts, use_disasters: Enable/disable data sources

        Returns:
        - Composite stress score 0-100 (None if no data available)
        - Averaged from available sources
        """
        scores = []

        if use_weather:
            weather_stress = self.get_weather_stress(latitude, longitude)
            if weather_stress is not None:
                scores.append(weather_stress)

        if use_aqi:
            aqi_stress = self.get_aqi_stress(latitude, longitude)
            if aqi_stress is not None:
                scores.append(aqi_stress)

        if use_alerts:
            alert_stress = self.get_alert_stress()
            if alert_stress is not None:
                scores.append(alert_stress)

        if use_disasters:
            disaster_stress = self.get_disaster_stress(latitude, longitude)
            if disaster_stress is not None:
                scores.append(disaster_stress)

        if not scores:
            logger.info("No external stress data available")
            return None

        # Average all available scores
        composite_score = round(sum(scores) / len(scores), 2)
        logger.info(f"Composite external stress score: {composite_score} (from {len(scores)} sources)")
        return composite_score

    @staticmethod
    def _weather_to_stress(weather_data: dict) -> float:
        """Convert weather API response to stress score (0-100)."""
        try:
            stress = 0.0

            # Temperature stress (extreme cold/heat)
            if "main" in weather_data:
                temp = weather_data["main"].get("temp", 20)
                # -40°C to 60°C range
                if temp < -30 or temp > 50:
                    stress += 40  # Extreme temperature
                elif temp < 0 or temp > 40:
                    stress += 20  # Moderate temperature stress
                else:
                    stress += 5   # Mild stress

            # Weather condition stress
            if "weather" in weather_data and len(weather_data["weather"]) > 0:
                condition = weather_data["weather"][0].get("main", "").lower()
                if condition in ["thunderstorm", "tornado"]:
                    stress += 40
                elif condition in ["rain", "snow", "sleet"]:
                    stress += 20
                elif condition in ["mist", "smoke", "haze", "dust", "fog", "sand", "ash"]:
                    stress += 15
                elif condition == "clouds":
                    stress += 5

            # Wind stress
            if "wind" in weather_data:
                wind_speed = weather_data["wind"].get("speed", 0)  # m/s
                if wind_speed > 15:  # Strong winds
                    stress += 15
                elif wind_speed > 10:
                    stress += 8

            return round(min(stress, 100.0), 2)

        except Exception as e:
            logger.warning(f"Error converting weather data: {e}")
            return 25.0  # Default moderate stress

    @staticmethod
    def _aqi_to_stress(aqi_data: dict) -> float:
        """Convert AQI API response to stress score (0-100)."""
        try:
            if aqi_data.get("status") != "ok":
                return 25.0  # Default if no data

            aqi_value = aqi_data.get("data", {}).get("aqi")
            if aqi_value is None:
                return 25.0

            # AQI scale: 0-50 (good), 51-100 (moderate), 101-150 (unhealthy for sensitive),
            # 151-200 (unhealthy), 201-300 (very unhealthy), 301+ (hazardous)
            if aqi_value <= 50:
                stress = (aqi_value / 50) * 10
            elif aqi_value <= 100:
                stress = 10 + ((aqi_value - 50) / 50) * 20
            elif aqi_value <= 150:
                stress = 30 + ((aqi_value - 100) / 50) * 20
            elif aqi_value <= 200:
                stress = 50 + ((aqi_value - 150) / 50) * 20
            elif aqi_value <= 300:
                stress = 70 + ((aqi_value - 200) / 100) * 20
            else:
                stress = 95.0

            return round(min(stress, 100.0), 2)

        except Exception as e:
            logger.warning(f"Error converting AQI data: {e}")
            return 25.0

    @staticmethod
    def _alerts_to_stress(news_data: dict) -> float:
        """Convert news API response to stress score (0-100)."""
        try:
            articles = news_data.get("articles", [])

            if not articles:
                return 5.0  # No news available, assume moderate baseline

            # Check number and severity of alert articles
            stress = 0.0
            critical_keywords = ["emergency", "alert", "disaster", "death", "killed", "injured", "critical"]

            for article in articles[:5]:  # Check top 5
                title = article.get("title", "").lower()
                description = article.get("description", "").lower()
                content = title + " " + description

                # Count critical keywords
                keyword_count = sum(1 for keyword in critical_keywords if keyword in content)
                if keyword_count > 0:
                    stress += 15 * keyword_count

            # Normalize to 0-100
            if stress == 0:
                # No critical news found, return low baseline
                return 5.0
            
            stress = min(stress / len(articles), 100.0)
            return round(stress, 2)

        except Exception as e:
            logger.warning(f"Error converting alert data: {e}")
            return 5.0

    @staticmethod
    def _disasters_to_stress(xml_content: str) -> float:
        """Convert disaster API response to stress score (0-100)."""
        try:
            # Simple check: count disaster entries in RSS feed
            disaster_count = xml_content.lower().count("<item>")

            if disaster_count == 0:
                return 5.0

            # More disasters = more stress
            stress = min(5.0 + (disaster_count * 10), 100.0)
            return round(stress, 2)

        except Exception as e:
            logger.warning(f"Error converting disaster data: {e}")
            return 5.0


# Singleton instance
external_factor_service = ExternalFactorService()
