"""
Unit tests for Geocoding Server
"""

import pytest
import asyncio
from map_servers.geocoding_server import GeocodingServer, GeocodingResult


@pytest.mark.asyncio
async def test_forward_geocode():
    """Test forward geocoding (address to coordinates)"""
    server = GeocodingServer()

    results = await server.forward_geocode("Empire State Building", limit=1)

    assert len(results) > 0
    assert isinstance(results[0], GeocodingResult)
    assert results[0].latitude != 0
    assert results[0].longitude != 0
    assert results[0].confidence >= 0 and results[0].confidence <= 1

    await server.close()


@pytest.mark.asyncio
async def test_reverse_geocode():
    """Test reverse geocoding (coordinates to address)"""
    server = GeocodingServer()

    # Empire State Building coordinates
    result = await server.reverse_geocode(40.7484, -73.9857)

    assert isinstance(result, GeocodingResult)
    assert result.address is not None
    assert len(result.address) > 0
    assert result.latitude == 40.7484
    assert result.longitude == -73.9857

    await server.close()


@pytest.mark.asyncio
async def test_reverse_geocode_invalid_coordinates():
    """Test reverse geocoding with invalid coordinates"""
    server = GeocodingServer()

    # Test invalid latitude
    with pytest.raises(ValueError):
        await server.reverse_geocode(91, 0)

    # Test invalid longitude
    with pytest.raises(ValueError):
        await server.reverse_geocode(0, 181)

    await server.close()


@pytest.mark.asyncio
async def test_batch_geocode():
    """Test batch geocoding multiple addresses"""
    server = GeocodingServer()

    addresses = [
        "Empire State Building",
        "Central Park, New York",
        "Times Square, NYC"
    ]

    results = await server.batch_geocode(addresses)

    assert len(results) == len(addresses)
    for result_list in results:
        assert isinstance(result_list, list)
        if len(result_list) > 0:
            assert isinstance(result_list[0], GeocodingResult)

    await server.close()


@pytest.mark.asyncio
async def test_geocode_with_limit():
    """Test geocoding with result limit"""
    server = GeocodingServer()

    results = await server.forward_geocode("New York", limit=3)

    assert len(results) <= 3

    await server.close()


def test_geocoding_result_model():
    """Test GeocodingResult pydantic model"""
    result = GeocodingResult(
        address="Test Address",
        latitude=40.7484,
        longitude=-73.9857,
        confidence=0.9,
        place_type="building",
        country="USA",
        city="New York"
    )

    assert result.address == "Test Address"
    assert result.latitude == 40.7484
    assert result.longitude == -73.9857
    assert result.confidence == 0.9
    assert result.place_type == "building"


def test_geocoding_result_validation():
    """Test GeocodingResult validation"""
    # Test confidence range validation
    with pytest.raises(Exception):  # Pydantic ValidationError
        GeocodingResult(
            address="Test",
            latitude=0,
            longitude=0,
            confidence=1.5  # Invalid - should be 0-1
        )
