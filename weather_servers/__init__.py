"""
Weather Servers Package
MCP-compliant weather services using OpenWeather API (Free Tier)
"""

from .forecast_server import WeatherForecastServer, get_current_weather, get_forecast, get_daily_summary
from .air_quality_server import AirQualityServer, get_air_quality, get_pollution_forecast

__all__ = [
    'WeatherForecastServer',
    'AirQualityServer',
    'get_current_weather',
    'get_forecast',
    'get_daily_summary',
    'get_air_quality',
    'get_pollution_forecast'
]