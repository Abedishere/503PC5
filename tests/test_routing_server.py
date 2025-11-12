"""
Unit tests for Routing Server
"""

import pytest
import asyncio
from map_servers.routing_server import RoutingServer, RouteResult, RouteStep


@pytest.mark.asyncio
async def test_calculate_route():
    """Test route calculation between two points"""
    server = RoutingServer()

    # Route from Empire State Building to Central Park
    route = await server.calculate_route(
        origin_lat=40.7484,
        origin_lon=-73.9857,
        dest_lat=40.7829,
        dest_lon=-73.9654,
        mode="driving"
    )

    assert isinstance(route, RouteResult)
    assert route.distance_meters > 0
    assert route.duration_seconds > 0
    assert len(route.steps) > 0
    assert route.mode == "driving"
    assert route.origin == "40.7484, -73.9857"
    assert route.destination == "40.7829, -73.9654"

    await server.close()


@pytest.mark.asyncio
async def test_calculate_route_different_modes():
    """Test route calculation with different transportation modes"""
    server = RoutingServer()

    modes = ["driving", "walking", "cycling", "transit"]

    for mode in modes:
        route = await server.calculate_route(
            40.7484, -73.9857,
            40.7589, -73.9851,
            mode=mode
        )

        assert route.mode == mode
        assert route.distance_meters > 0
        # Walking should generally take longer than driving for same distance
        assert route.duration_seconds > 0

    await server.close()


@pytest.mark.asyncio
async def test_haversine_distance_calculation():
    """Test Haversine distance calculation"""
    server = RoutingServer()

    # Known distance between two points
    # Empire State Building to Central Park is approximately 3.8 km
    distance = server._calculate_haversine_distance(
        40.7484, -73.9857,  # Empire State Building
        40.7829, -73.9654   # Central Park
    )

    assert 3500 < distance < 4500  # Should be around 3800-4000 meters
    assert isinstance(distance, float)

    await server.close()


@pytest.mark.asyncio
async def test_distance_matrix():
    """Test distance matrix calculation"""
    server = RoutingServer()

    origins = [(40.7484, -73.9857), (40.7589, -73.9851)]
    destinations = [(40.7829, -73.9654)]

    matrix = await server.calculate_distance_matrix(origins, destinations)

    assert "distances_meters" in matrix
    assert "durations_seconds" in matrix
    assert len(matrix["distances_meters"]) == len(origins)
    assert len(matrix["distances_meters"][0]) == len(destinations)

    await server.close()


@pytest.mark.asyncio
async def test_route_alternatives():
    """Test getting alternative routes"""
    server = RoutingServer()

    routes = await server.get_route_alternatives(
        40.7484, -73.9857,
        40.7829, -73.9654,
        alternatives=3
    )

    assert len(routes) > 0
    assert len(routes) <= 3
    assert all(isinstance(r, RouteResult) for r in routes)

    # Alternatives should have different distances/durations
    if len(routes) > 1:
        distances = [r.distance_meters for r in routes]
        assert len(set(distances)) > 1  # Not all the same

    await server.close()


@pytest.mark.asyncio
async def test_route_steps():
    """Test route steps are properly formed"""
    server = RoutingServer()

    route = await server.calculate_route(
        40.7484, -73.9857,
        40.7829, -73.9654
    )

    for step in route.steps:
        assert isinstance(step, RouteStep)
        assert step.instruction is not None
        assert step.distance_meters >= 0
        assert step.duration_seconds >= 0
        assert len(step.start_location) == 2
        assert len(step.end_location) == 2

    # Total of steps should approximately equal route total
    total_distance = sum(step.distance_meters for step in route.steps)
    assert abs(total_distance - route.distance_meters) < 1  # Within 1 meter

    await server.close()


def test_route_result_model():
    """Test RouteResult pydantic model"""
    step = RouteStep(
        instruction="Turn left",
        distance_meters=100,
        duration_seconds=30,
        start_location=(40.7484, -73.9857),
        end_location=(40.7490, -73.9860),
        maneuver="turn-left"
    )

    route = RouteResult(
        origin="Start",
        destination="End",
        distance_meters=1000,
        duration_seconds=300,
        steps=[step],
        mode="driving"
    )

    assert route.distance_meters == 1000
    assert route.duration_seconds == 300
    assert len(route.steps) == 1
    assert route.steps[0].instruction == "Turn left"
