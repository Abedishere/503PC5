"""
Air Quality Server - MCP-compliant server for air pollution data
Following OpenAI Agents SDK patterns with function tools
Uses OpenWeather Air Pollution API
"""

import asyncio
import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import httpx


class AirQuality(BaseModel):
    """Air quality data"""
    aqi: int = Field(description="Air Quality Index (1-5, where 1=Good, 5=Very Poor)")
    co: float = Field(description="Carbon monoxide (μg/m³)")
    no: float = Field(description="Nitrogen monoxide (μg/m³)")
    no2: float = Field(description="Nitrogen dioxide (μg/m³)")
    o3: float = Field(description="Ozone (μg/m³)")
    so2: float = Field(description="Sulphur dioxide (μg/m³)")
    pm2_5: float = Field(description="Fine particles matter (μg/m³)")
    pm10: float = Field(description="Coarse particulate matter (μg/m³)")
    nh3: float = Field(description="Ammonia (μg/m³)")
    timestamp: datetime = Field(description="Data timestamp")

    @property
    def aqi_description(self) -> str:
        """Get AQI description"""
        descriptions = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        return descriptions.get(self.aqi, "Unknown")

    @property
    def health_recommendation(self) -> str:
        """Get health recommendation based on AQI"""
        recommendations = {
            1: "Air quality is satisfactory, and air pollution poses little or no risk.",
            2: "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.",
            3: "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
            4: "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.",
            5: "Health alert: The risk of health effects is increased for everyone."
        }
        return recommendations.get(self.aqi, "No recommendation available")


class AirQualityForecast(BaseModel):
    """Air quality forecast"""
    timestamp: datetime
    aqi: int
    pm2_5: float
    pm10: float
    o3: float


class AirQualityServer:
    """
    MCP-compliant Air Quality Server
    Provides air pollution data and forecasts
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Air Quality Server

        Args:
            api_key: OpenWeather API key
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is required")

        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.session = None

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session"""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=30.0)
        return self.session

    async def _get_coordinates(self, location: str) -> tuple:
        """Helper to get coordinates from location name"""
        session = await self._get_session()
        params = {
            "q": location,
            "appid": self.api_key,
            "limit": 1
        }

        try:
            response = await session.get(
                "http://api.openweathermap.org/geo/1.0/direct",
                params=params
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError(f"Location '{location}' not found")

            return data[0]["lat"], data[0]["lon"]
        except httpx.HTTPStatusError as e:
            raise Exception(f"Geocoding failed: {e.response.status_code} - {e.response.text}")

    async def get_current_air_quality(
        self,
        location: str = None,
        latitude: float = None,
        longitude: float = None
    ) -> AirQuality:
        """
        Get current air quality data

        Args:
            location: City name (e.g., "Beijing", "Delhi")
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Current air quality data

        Example:
            >>> air_quality = await server.get_current_air_quality(location="Beijing")
            >>> print(f"AQI: {air_quality.aqi} ({air_quality.aqi_description})")
            >>> print(f"PM2.5: {air_quality.pm2_5} μg/m³")
        """
        # Get coordinates if location provided
        if location and not (latitude and longitude):
            latitude, longitude = await self._get_coordinates(location)
        elif latitude is None or longitude is None:
            raise ValueError("Either location or (latitude, longitude) must be provided")

        session = await self._get_session()

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key
        }

        try:
            response = await session.get(
                f"{self.base_url}/air_pollution",
                params=params
            )
            response.raise_for_status()
            data = response.json()

            pollution_data = data["list"][0]
            components = pollution_data["components"]

            return AirQuality(
                aqi=pollution_data["main"]["aqi"],
                co=components["co"],
                no=components["no"],
                no2=components["no2"],
                o3=components["o3"],
                so2=components["so2"],
                pm2_5=components["pm2_5"],
                pm10=components["pm10"],
                nh3=components["nh3"],
                timestamp=datetime.fromtimestamp(pollution_data["dt"])
            )

        except httpx.HTTPStatusError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {e}")

    async def get_air_quality_forecast(
        self,
        location: str = None,
        latitude: float = None,
        longitude: float = None,
        hours: int = 24
    ) -> List[AirQualityForecast]:
        """
        Get air quality forecast

        Args:
            location: City name
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            hours: Number of hours to forecast (max 120)

        Returns:
            List of air quality forecasts

        Example:
            >>> forecasts = await server.get_air_quality_forecast(location="Delhi", hours=48)
            >>> for forecast in forecasts[:5]:
            ...     print(f"{forecast.timestamp}: AQI {forecast.aqi}")
        """
        # Get coordinates if location provided
        if location and not (latitude and longitude):
            latitude, longitude = await self._get_coordinates(location)
        elif latitude is None or longitude is None:
            raise ValueError("Either location or (latitude, longitude) must be provided")

        session = await self._get_session()

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key
        }

        try:
            response = await session.get(
                f"{self.base_url}/air_pollution/forecast",
                params=params
            )
            response.raise_for_status()
            data = response.json()

            forecasts = []
            for item in data["list"][:hours]:
                components = item["components"]
                forecasts.append(AirQualityForecast(
                    timestamp=datetime.fromtimestamp(item["dt"]),
                    aqi=item["main"]["aqi"],
                    pm2_5=components["pm2_5"],
                    pm10=components["pm10"],
                    o3=components["o3"]
                ))

            return forecasts

        except httpx.HTTPStatusError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {e}")

    async def get_pollution_history(
        self,
        location: str = None,
        latitude: float = None,
        longitude: float = None,
        start_timestamp: int = None,
        end_timestamp: int = None
    ) -> List[AirQuality]:
        """
        Get historical air pollution data

        Args:
            location: City name
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            start_timestamp: Start time (Unix timestamp)
            end_timestamp: End time (Unix timestamp)

        Returns:
            List of historical air quality data

        Example:
            >>> import time
            >>> end = int(time.time())
            >>> start = end - 86400  # 24 hours ago
            >>> history = await server.get_pollution_history(
            ...     location="London",
            ...     start_timestamp=start,
            ...     end_timestamp=end
            ... )
        """
        # Get coordinates if location provided
        if location and not (latitude and longitude):
            latitude, longitude = await self._get_coordinates(location)
        elif latitude is None or longitude is None:
            raise ValueError("Either location or (latitude, longitude) must be provided")

        if start_timestamp is None or end_timestamp is None:
            raise ValueError("start_timestamp and end_timestamp are required")

        session = await self._get_session()

        params = {
            "lat": latitude,
            "lon": longitude,
            "start": start_timestamp,
            "end": end_timestamp,
            "appid": self.api_key
        }

        try:
            response = await session.get(
                f"{self.base_url}/air_pollution/history",
                params=params
            )
            response.raise_for_status()
            data = response.json()

            history = []
            for item in data["list"]:
                components = item["components"]
                history.append(AirQuality(
                    aqi=item["main"]["aqi"],
                    co=components["co"],
                    no=components["no"],
                    no2=components["no2"],
                    o3=components["o3"],
                    so2=components["so2"],
                    pm2_5=components["pm2_5"],
                    pm10=components["pm10"],
                    nh3=components["nh3"],
                    timestamp=datetime.fromtimestamp(item["dt"])
                ))

            return history

        except httpx.HTTPStatusError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {e}")

    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None


# Function tools for OpenAI Agents SDK
async def get_air_quality(location: str = None, latitude: float = None, longitude: float = None) -> str:
    """
    Get current air quality data (OpenAI Agents SDK tool)

    Args:
        location: City name (e.g., "Beijing", "Delhi")
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        JSON string with air quality data
    """
    server = AirQualityServer()
    try:
        air_quality = await server.get_current_air_quality(
            location=location,
            latitude=latitude,
            longitude=longitude
        )

        return str({
            "aqi": air_quality.aqi,
            "aqi_description": air_quality.aqi_description,
            "pm2_5": air_quality.pm2_5,
            "pm10": air_quality.pm10,
            "o3": air_quality.o3,
            "no2": air_quality.no2,
            "health_recommendation": air_quality.health_recommendation
        })
    finally:
        await server.close()


async def get_pollution_forecast(location: str = None, latitude: float = None, longitude: float = None, hours: int = 24) -> str:
    """
    Get air quality forecast (OpenAI Agents SDK tool)

    Args:
        location: City name
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        hours: Number of hours to forecast

    Returns:
        JSON string with air quality forecast
    """
    server = AirQualityServer()
    try:
        forecasts = await server.get_air_quality_forecast(
            location=location,
            latitude=latitude,
            longitude=longitude,
            hours=hours
        )

        formatted = []
        aqi_descriptions = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

        for f in forecasts:
            formatted.append({
                "time": f.timestamp.strftime("%Y-%m-%d %H:%M"),
                "aqi": f.aqi,
                "aqi_description": aqi_descriptions.get(f.aqi, "Unknown"),
                "pm2_5": f.pm2_5,
                "pm10": f.pm10
            })

        return str({"forecast_hours": len(formatted), "forecasts": formatted})
    finally:
        await server.close()
