"""
Unit tests for POI (Points of Interest) Server
"""

import pytest
import asyncio
from map_servers.poi_server import POIServer, POIResult, POICategory


@pytest.mark.asyncio
async def test_search_nearby():
    """Test searching for nearby POIs"""
    server = POIServer()

    # Search near Empire State Building
    pois = await server.search_nearby(
        latitude=40.7484,
        longitude=-73.9857,
        radius_meters=5000,
        limit=10
    )

    assert len(pois) > 0
    assert all(isinstance(poi, POIResult) for poi in pois)

    # Results should be sorted by distance
    distances = [poi.distance_meters for poi in pois if poi.distance_meters]
    assert distances == sorted(distances)

    await server.close()


@pytest.mark.asyncio
async def test_search_nearby_with_category():
    """Test searching for nearby POIs with category filter"""
    server = POIServer()

    # Search for restaurants
    restaurants = await server.search_nearby(
        latitude=40.7484,
        longitude=-73.9857,
        radius_meters=3000,
        category="restaurant",
        limit=5
    )

    assert all(poi.category == "restaurant" for poi in restaurants)

    await server.close()


@pytest.mark.asyncio
async def test_search_text():
    """Test text-based place search"""
    server = POIServer()

    results = await server.search_text(
        query="museum",
        latitude=40.7484,
        longitude=-73.9857,
        limit=5
    )

    assert len(results) > 0
    # Should find museum-related results
    assert any("museum" in poi.name.lower() or poi.category == "museum" for poi in results)

    await server.close()


@pytest.mark.asyncio
async def test_search_text_without_location():
    """Test text search without location bias"""
    server = POIServer()

    results = await server.search_text(
        query="park",
        limit=5
    )

    assert len(results) >= 0  # May return 0 if no matches
    # If results exist, should be sorted by rating
    if len(results) > 1:
        ratings = [poi.rating for poi in results if poi.rating]
        assert ratings == sorted(ratings, reverse=True)

    await server.close()


@pytest.mark.asyncio
async def test_get_place_details():
    """Test getting detailed place information"""
    server = POIServer()

    # Get details for a known place in mock data
    details = await server.get_place_details("Empire State Building")

    assert details is not None
    assert isinstance(details, POIResult)
    assert details.name == "Empire State Building"
    assert details.latitude != 0
    assert details.longitude != 0

    await server.close()


@pytest.mark.asyncio
async def test_get_place_details_not_found():
    """Test getting details for non-existent place"""
    server = POIServer()

    details = await server.get_place_details("Nonexistent Place 12345")

    assert details is None

    await server.close()


@pytest.mark.asyncio
async def test_search_by_category_with_filters():
    """Test category search with rating and price filters"""
    server = POIServer()

    # Search for highly-rated affordable restaurants
    results = await server.search_by_category(
        category="restaurant",
        latitude=40.7484,
        longitude=-73.9857,
        radius_meters=5000,
        min_rating=4.0,
        max_price_level=2,
        limit=10
    )

    # Verify filters applied
    for poi in results:
        assert poi.category == "restaurant"
        if poi.rating:
            assert poi.rating >= 4.0
        if poi.price_level:
            assert poi.price_level <= 2

    await server.close()


@pytest.mark.asyncio
async def test_distance_calculation():
    """Test distance calculation between coordinates"""
    server = POIServer()

    # Known distance between Empire State Building and Central Park
    distance = server._calculate_distance(
        40.7484, -73.9857,  # Empire State Building
        40.7829, -73.9654   # Central Park
    )

    assert 3500 < distance < 4500  # Should be around 3800-4000 meters
    assert isinstance(distance, float)

    await server.close()


@pytest.mark.asyncio
async def test_nearby_within_radius():
    """Test that nearby search respects radius"""
    server = POIServer()

    # Small radius - should get fewer results
    small_radius = await server.search_nearby(
        latitude=40.7484,
        longitude=-73.9857,
        radius_meters=1000,
        limit=100
    )

    # Larger radius - should get more results
    large_radius = await server.search_nearby(
        latitude=40.7484,
        longitude=-73.9857,
        radius_meters=10000,
        limit=100
    )

    # All results should be within specified radius
    for poi in small_radius:
        if poi.distance_meters:
            assert poi.distance_meters <= 1000

    for poi in large_radius:
        if poi.distance_meters:
            assert poi.distance_meters <= 10000

    # Larger radius should generally find more places
    assert len(large_radius) >= len(small_radius)

    await server.close()


def test_poi_result_model():
    """Test POIResult pydantic model"""
    poi = POIResult(
        name="Test Place",
        category="restaurant",
        latitude=40.7484,
        longitude=-73.9857,
        address="123 Test St",
        rating=4.5,
        price_level=2,
        phone="+1234567890",
        website="https://example.com",
        opening_hours=["Mon-Fri: 9AM-5PM"],
        distance_meters=500.0,
        description="A test place"
    )

    assert poi.name == "Test Place"
    assert poi.category == "restaurant"
    assert poi.rating == 4.5
    assert 0 <= poi.rating <= 5
    assert 1 <= poi.price_level <= 4


def test_poi_result_validation():
    """Test POIResult validation"""
    # Test invalid rating
    with pytest.raises(Exception):  # Pydantic ValidationError
        POIResult(
            name="Test",
            category="restaurant",
            latitude=0,
            longitude=0,
            rating=6.0  # Invalid - should be 0-5
        )

    # Test invalid price level
    with pytest.raises(Exception):
        POIResult(
            name="Test",
            category="restaurant",
            latitude=0,
            longitude=0,
            price_level=5  # Invalid - should be 1-4
        )


def test_poi_category_enum():
    """Test POICategory enum"""
    assert POICategory.RESTAURANT.value == "restaurant"
    assert POICategory.CAFE.value == "cafe"
    assert POICategory.MUSEUM.value == "museum"
    assert len([c for c in POICategory]) > 10  # Should have many categories
