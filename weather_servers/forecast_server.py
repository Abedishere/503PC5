"""
Weather Forecast Server - MCP-compliant server for weather forecasts
Following OpenAI Agents SDK patterns with function tools
Uses OpenWeather API for real weather data
"""

import asyncio
import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import httpx


class CurrentWeather(BaseModel):
    """Current weather conditions"""
    temperature: float = Field(description="Temperature in Celsius")
    feels_like: float = Field(description="Feels like temperature in Celsius")
    humidity: int = Field(description="Humidity percentage")
    pressure: int = Field(description="Atmospheric pressure in hPa")
    wind_speed: float = Field(description="Wind speed in m/s")
    wind_direction: int = Field(description="Wind direction in degrees")
    description: str = Field(description="Weather description")
    icon: str = Field(description="Weather icon code")
    clouds: int = Field(description="Cloudiness percentage")
    visibility: Optional[int] = Field(None, description="Visibility in meters")
    timestamp: datetime = Field(description="Time of data calculation")


class HourlyForecast(BaseModel):
    """Hourly weather forecast"""
    timestamp: datetime
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    description: str
    pop: float = Field(description="Probability of precipitation (0-1)")
    clouds: int


class DailyForecast(BaseModel):
    """Daily weather forecast"""
    date: datetime
    temp_min: float = Field(description="Minimum temperature")
    temp_max: float = Field(description="Maximum temperature")
    temp_day: float = Field(description="Day temperature")
    temp_night: float = Field(description="Night temperature")
    humidity: int
    wind_speed: float
    description: str
    pop: float = Field(description="Probability of precipitation (0-1)")
    uvi: Optional[float] = Field(None, description="UV index")


class WeatherForecastServer:
    """
    MCP-compliant Weather Forecast Server
    Provides current weather, hourly, and daily forecasts
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Weather Forecast Server

        Args:
            api_key: OpenWeather API key
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is required")

        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = None

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session"""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=30.0)
        return self.session

    async def get_current_weather(
        self,
        location: str = None,
        latitude: float = None,
        longitude: float = None
    ) -> CurrentWeather:
        """
        Get current weather conditions

        Args:
            location: City name (e.g., "London", "New York,US")
            latitude: Latitude coordinate (alternative to location)
            longitude: Longitude coordinate (required if latitude provided)

        Returns:
            Current weather data

        Example:
            >>> weather = await server.get_current_weather(location="London")
            >>> print(f"Temperature: {weather.temperature}°C")
        """
        session = await self._get_session()

        params = {
            "appid": self.api_key,
            "units": "metric"
        }

        if location:
            params["q"] = location
        elif latitude is not None and longitude is not None:
            params["lat"] = latitude
            params["lon"] = longitude
        else:
            raise ValueError("Either location or (latitude, longitude) must be provided")

        try:
            response = await session.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            data = response.json()

            return CurrentWeather(
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                wind_speed=data["wind"]["speed"],
                wind_direction=data["wind"].get("deg", 0),
                description=data["weather"][0]["description"],
                icon=data["weather"][0]["icon"],
                clouds=data["clouds"]["all"],
                visibility=data.get("visibility"),
                timestamp=datetime.fromtimestamp(data["dt"])
            )
        except httpx.HTTPStatusError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: missing key {e}")

    async def get_forecast(
        self,
        location: str = None,
        latitude: float = None,
        longitude: float = None
    ) -> List[HourlyForecast]:
        """
        Get 3-hour interval weather forecast (Free tier: 5 days, 3-hour step)

        Args:
            location: City name
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            List of 3-hour interval forecasts (up to 40 data points = 5 days)

        Example:
            >>> forecasts = await server.get_forecast(location="Paris")
            >>> for forecast in forecasts[:3]:
            ...     print(f"{forecast.timestamp}: {forecast.temperature}°C")
        """
        session = await self._get_session()

        # Use forecast API (5 day / 3 hour forecast - free tier)
        params = {
            "appid": self.api_key,
            "units": "metric"
        }

        if location:
            params["q"] = location
        elif latitude is not None and longitude is not None:
            params["lat"] = latitude
            params["lon"] = longitude
        else:
            raise ValueError("Either location or (latitude, longitude) must be provided")

        try:
            response = await session.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            data = response.json()

            forecasts = []
            for item in data["list"]:
                forecasts.append(HourlyForecast(
                    timestamp=datetime.fromtimestamp(item["dt"]),
                    temperature=item["main"]["temp"],
                    feels_like=item["main"]["feels_like"],
                    humidity=item["main"]["humidity"],
                    pressure=item["main"]["pressure"],
                    wind_speed=item["wind"]["speed"],
                    description=item["weather"][0]["description"],
                    pop=item.get("pop", 0.0),
                    clouds=item["clouds"]["all"]
                ))

            return forecasts
        except httpx.HTTPStatusError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: missing key {e}")

    async def get_daily_summary(
        self,
        location: str = None,
        latitude: float = None,
        longitude: float = None
    ) -> List[DailyForecast]:
        """
        Get daily weather summary (aggregated from 3-hour forecast data)
        Free tier: 5 days maximum

        Args:
            location: City name
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            List of daily summaries (up to 5 days)

        Example:
            >>> forecasts = await server.get_daily_summary(location="Tokyo")
            >>> for forecast in forecasts:
            ...     print(f"{forecast.date.date()}: {forecast.temp_min}-{forecast.temp_max}°C")
        """
        session = await self._get_session()

        params = {
            "appid": self.api_key,
            "units": "metric"
        }

        if location:
            params["q"] = location
        elif latitude is not None and longitude is not None:
            params["lat"] = latitude
            params["lon"] = longitude
        else:
            raise ValueError("Either location or (latitude, longitude) must be provided")

        try:
            # Use forecast API and aggregate by day
            response = await session.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            data = response.json()

            # Group by day and aggregate
            daily_data = {}
            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"]).date()
                if date not in daily_data:
                    daily_data[date] = []
                daily_data[date].append(item)

            forecasts = []
            for date, items in list(daily_data.items()):
                temps = [item["main"]["temp"] for item in items]
                day_items = [item for item in items if 6 <= datetime.fromtimestamp(item["dt"]).hour <= 18]
                night_items = [item for item in items if datetime.fromtimestamp(item["dt"]).hour < 6 or datetime.fromtimestamp(item["dt"]).hour > 18]

                forecasts.append(DailyForecast(
                    date=datetime.combine(date, datetime.min.time()),
                    temp_min=min(temps),
                    temp_max=max(temps),
                    temp_day=sum(temps) / len(temps) if day_items else sum(temps) / len(temps),
                    temp_night=sum(item["main"]["temp"] for item in night_items) / len(night_items) if night_items else temps[0],
                    humidity=int(sum(item["main"]["humidity"] for item in items) / len(items)),
                    wind_speed=sum(item["wind"]["speed"] for item in items) / len(items),
                    description=items[len(items)//2]["weather"][0]["description"],
                    pop=max(item.get("pop", 0.0) for item in items),
                    uvi=None  # Not available in free tier
                ))

            return forecasts
        except httpx.HTTPStatusError as e:
            raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: missing key {e}")

    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None


# Function tools for OpenAI Agents SDK
async def get_current_weather(location: str = None, latitude: float = None, longitude: float = None) -> str:
    """
    Get current weather conditions (OpenAI Agents SDK tool)

    Args:
        location: City name (e.g., "London", "New York,US")
        latitude: Latitude coordinate (optional, alternative to location)
        longitude: Longitude coordinate (required if latitude provided)

    Returns:
        JSON string with current weather data
    """
    server = WeatherForecastServer()
    try:
        weather = await server.get_current_weather(location=location, latitude=latitude, longitude=longitude)
        return str({
            "temperature": weather.temperature,
            "feels_like": weather.feels_like,
            "humidity": weather.humidity,
            "description": weather.description,
            "wind_speed": weather.wind_speed,
            "pressure": weather.pressure,
            "clouds": weather.clouds
        })
    finally:
        await server.close()


async def get_forecast(location: str = None, latitude: float = None, longitude: float = None) -> str:
    """
    Get 3-hour interval weather forecast for 5 days (OpenAI Agents SDK tool)

    Args:
        location: City name
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        JSON string with 3-hour forecast data
    """
    server = WeatherForecastServer()
    try:
        forecasts = await server.get_forecast(location=location, latitude=latitude, longitude=longitude)
        formatted = []
        for f in forecasts:
            formatted.append({
                "time": f.timestamp.strftime("%Y-%m-%d %H:%M"),
                "temperature": f.temperature,
                "description": f.description,
                "precipitation_probability": f.pop
            })
        return str(formatted)
    finally:
        await server.close()


async def get_daily_summary(location: str = None, latitude: float = None, longitude: float = None) -> str:
    """
    Get daily weather summary for 5 days (OpenAI Agents SDK tool)

    Args:
        location: City name
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        JSON string with daily summary data
    """
    server = WeatherForecastServer()
    try:
        forecasts = await server.get_daily_summary(location=location, latitude=latitude, longitude=longitude)
        formatted = []
        for f in forecasts:
            formatted.append({
                "date": f.date.strftime("%Y-%m-%d"),
                "temp_min": f.temp_min,
                "temp_max": f.temp_max,
                "description": f.description,
                "precipitation_probability": f.pop,
                "humidity": f.humidity
            })
        return str(formatted)
    finally:
        await server.close()