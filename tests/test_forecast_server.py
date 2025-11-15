"""
Tests for Weather Forecast Server
"""

import pytest
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from weather_servers.forecast_server import WeatherForecastServer, get_current_weather, get_forecast, get_daily_summary

# Load environment variables from .env file
load_dotenv()


class TestWeatherForecastServer:
    """Test cases for WeatherForecastServer"""

    @pytest.fixture
    def server(self):
        """Create a test server instance"""
        return WeatherForecastServer()

    @pytest.mark.asyncio
    async def test_get_current_weather_by_location(self, server):
        """Test getting current weather by location name"""
        result = await server.get_current_weather(location="London")

        assert result is not None
        assert isinstance(result.temperature, float)
        assert isinstance(result.humidity, int)
        assert result.description is not None
        assert isinstance(result.timestamp, datetime)

        await server.close()

    @pytest.mark.asyncio
    async def test_get_current_weather_by_coordinates(self, server):
        """Test getting current weather by coordinates"""
        result = await server.get_current_weather(latitude=51.5074, longitude=-0.1278)

        assert result is not None
        assert isinstance(result.temperature, float)
        assert result.feels_like is not None

        await server.close()

    @pytest.mark.asyncio
    async def test_get_forecast(self, server):
        """Test getting 3-hour interval forecast"""
        results = await server.get_forecast(location="Tokyo")

        assert results is not None
        assert len(results) > 0
        assert len(results) <= 40  # 5 days * 8 (3-hour intervals)

        # Check first forecast
        first = results[0]
        assert isinstance(first.temperature, float)
        assert isinstance(first.timestamp, datetime)
        assert 0 <= first.pop <= 1  # Probability of precipitation

        await server.close()

    @pytest.mark.asyncio
    async def test_get_daily_summary(self, server):
        """Test getting daily weather summary"""
        results = await server.get_daily_summary(location="Paris")

        assert results is not None
        assert len(results) > 0
        assert len(results) <= 6  # ~5 days (can be 6 due to 3-hour intervals)

        # Check first day
        first = results[0]
        assert isinstance(first.temp_min, float)
        assert isinstance(first.temp_max, float)
        assert first.temp_min <= first.temp_max

        await server.close()

    @pytest.mark.asyncio
    async def test_invalid_location(self, server):
        """Test error handling for invalid location"""
        with pytest.raises(Exception):
            await server.get_current_weather(location="InvalidCityXYZ123")

        await server.close()

    @pytest.mark.asyncio
    async def test_no_parameters(self, server):
        """Test error when no location provided"""
        with pytest.raises(ValueError):
            await server.get_current_weather()

        await server.close()


class TestForecastFunctionTools:
    """Test cases for SDK function tools"""

    @pytest.mark.asyncio
    async def test_get_current_weather_tool(self):
        """Test get_current_weather SDK tool"""
        result = await get_current_weather(location="London")

        assert result is not None
        assert isinstance(result, str)
        assert "temperature" in result
        assert "description" in result

    @pytest.mark.asyncio
    async def test_get_forecast_tool(self):
        """Test get_forecast SDK tool"""
        result = await get_forecast(location="Tokyo")

        assert result is not None
        assert isinstance(result, str)
        assert "time" in result
        assert "temperature" in result

    @pytest.mark.asyncio
    async def test_get_daily_summary_tool(self):
        """Test get_daily_summary SDK tool"""
        result = await get_daily_summary(location="Paris")

        assert result is not None
        assert isinstance(result, str)
        assert "date" in result
        assert "temp_min" in result
        assert "temp_max" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
