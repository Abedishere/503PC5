"""
Tests for Air Quality Server
"""

import pytest
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from weather_servers.air_quality_server import AirQualityServer, get_air_quality, get_pollution_forecast

# Load environment variables from .env file
load_dotenv()


class TestAirQualityServer:
    """Test cases for AirQualityServer"""

    @pytest.fixture
    def server(self):
        """Create a test server instance"""
        return AirQualityServer()

    @pytest.mark.asyncio
    async def test_get_current_air_quality_by_location(self, server):
        """Test getting current air quality by location name"""
        result = await server.get_current_air_quality(location="Beijing")

        assert result is not None
        assert 1 <= result.aqi <= 5
        assert isinstance(result.pm2_5, float)
        assert isinstance(result.pm10, float)
        assert result.aqi_description in ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
        assert result.health_recommendation is not None

        await server.close()

    @pytest.mark.asyncio
    async def test_get_current_air_quality_by_coordinates(self, server):
        """Test getting current air quality by coordinates"""
        result = await server.get_current_air_quality(latitude=39.9042, longitude=116.4074)

        assert result is not None
        assert isinstance(result.co, float)
        assert isinstance(result.no2, float)
        assert isinstance(result.o3, float)

        await server.close()

    @pytest.mark.asyncio
    async def test_get_air_quality_forecast(self, server):
        """Test getting air quality forecast"""
        results = await server.get_air_quality_forecast(location="Delhi", hours=24)

        assert results is not None
        assert len(results) > 0
        assert len(results) <= 24

        # Check first forecast
        first = results[0]
        assert 1 <= first.aqi <= 5
        assert isinstance(first.pm2_5, float)
        assert isinstance(first.timestamp, datetime)

        await server.close()

    @pytest.mark.asyncio
    async def test_aqi_description_property(self, server):
        """Test AQI description property"""
        result = await server.get_current_air_quality(location="London")

        # Test that description matches AQI value
        descriptions = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        expected_description = descriptions[result.aqi]
        assert result.aqi_description == expected_description

        await server.close()

    @pytest.mark.asyncio
    async def test_invalid_location(self, server):
        """Test error handling for invalid location"""
        with pytest.raises(Exception):
            await server.get_current_air_quality(location="InvalidCityXYZ123")

        await server.close()

    @pytest.mark.asyncio
    async def test_no_parameters(self, server):
        """Test error when no location provided"""
        with pytest.raises(ValueError):
            await server.get_current_air_quality()

        await server.close()


class TestAirQualityFunctionTools:
    """Test cases for SDK function tools"""

    @pytest.mark.asyncio
    async def test_get_air_quality_tool(self):
        """Test get_air_quality SDK tool"""
        result = await get_air_quality(location="Beijing")

        assert result is not None
        assert isinstance(result, str)
        assert "aqi" in result
        assert "pm2_5" in result
        assert "health_recommendation" in result

    @pytest.mark.asyncio
    async def test_get_pollution_forecast_tool(self):
        """Test get_pollution_forecast SDK tool"""
        result = await get_pollution_forecast(location="Delhi", hours=24)

        assert result is not None
        assert isinstance(result, str)
        assert "forecast_hours" in result
        assert "forecasts" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
