"""
Routing Server - MCP-compliant server for route calculation and navigation
Following OpenAI Agents SDK patterns with function tools
"""

import asyncio
import math
import os
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
import httpx
from datetime import datetime, timedelta


class RouteStep(BaseModel):
    """A single step in a route"""
    instruction: str
    distance_meters: float
    duration_seconds: float
    start_location: tuple[float, float]  # (lat, lon)
    end_location: tuple[float, float]  # (lat, lon)
    maneuver: Optional[str] = None


class RouteResult(BaseModel):
    """Result from a routing operation"""
    origin: str
    destination: str
    distance_meters: float
    duration_seconds: float
    steps: List[RouteStep]
    mode: str = "driving"
    polyline: Optional[str] = None  # Encoded polyline for map display
    warnings: List[str] = Field(default_factory=list)


class RoutingServer:
    """
    MCP-compliant Routing Server
    Provides route calculation, distance matrix, and navigation services
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the Routing Server

        Args:
            api_key: API key for routing service
            base_url: Base URL for routing API (OSRM, Google, Mapbox, etc.)
        """
        self.api_key = api_key or os.getenv("MAPBOX_API_KEY", "")
        self.base_url = base_url or "http://router.project-osrm.org"
        self.session = None

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session"""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=30.0)
        return self.session

    def _calculate_haversine_distance(
        self,
        lat1: float, lon1: float,
        lat2: float, lon2: float
    ) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371000  # Earth's radius in meters

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    async def calculate_route(
        self,
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        mode: Literal["driving", "walking", "cycling", "transit"] = "driving"
    ) -> RouteResult:
        """
        Calculate a route between two points

        Args:
            origin_lat: Origin latitude
            origin_lon: Origin longitude
            dest_lat: Destination latitude
            dest_lon: Destination longitude
            mode: Transportation mode (driving, walking, cycling, transit)

        Returns:
            Route result with steps and metadata

        Example:
            >>> route = await server.calculate_route(40.7484, -73.9857, 40.7589, -73.9851, "walking")
            >>> print(f"Distance: {route.distance_meters}m, Duration: {route.duration_seconds}s")
        """
        # PLACEHOLDER: Replace with actual API call to OSRM, Google, or Mapbox
        session = await self._get_session()

        # Calculate straight-line distance as fallback
        distance = self._calculate_haversine_distance(
            origin_lat, origin_lon, dest_lat, dest_lon
        )

        # Estimate duration based on mode (rough approximations)
        speed_kmh = {
            "driving": 50,
            "walking": 5,
            "cycling": 15,
            "transit": 30
        }
        duration = (distance / 1000) / speed_kmh.get(mode, 50) * 3600  # seconds

        # MOCK DATA for demonstration
        # In production, replace with actual API call:
        # if self.base_url.startswith("http://router.project-osrm.org"):
        #     # OSRM API call
        #     url = f"{self.base_url}/route/v1/{mode}/{origin_lon},{origin_lat};{dest_lon},{dest_lat}"
        #     params = {"overview": "full", "steps": "true"}
        #     response = await session.get(url, params=params)
        #     data = response.json()

        # Create mock route steps
        steps = [
            RouteStep(
                instruction="Head north on Main Street",
                distance_meters=distance * 0.3,
                duration_seconds=duration * 0.3,
                start_location=(origin_lat, origin_lon),
                end_location=(origin_lat + (dest_lat - origin_lat) * 0.3,
                            origin_lon + (dest_lon - origin_lon) * 0.3),
                maneuver="depart"
            ),
            RouteStep(
                instruction="Turn right onto Broadway",
                distance_meters=distance * 0.5,
                duration_seconds=duration * 0.5,
                start_location=(origin_lat + (dest_lat - origin_lat) * 0.3,
                              origin_lon + (dest_lon - origin_lon) * 0.3),
                end_location=(origin_lat + (dest_lat - origin_lat) * 0.8,
                            origin_lon + (dest_lon - origin_lon) * 0.8),
                maneuver="turn-right"
            ),
            RouteStep(
                instruction="Arrive at destination",
                distance_meters=distance * 0.2,
                duration_seconds=duration * 0.2,
                start_location=(origin_lat + (dest_lat - origin_lat) * 0.8,
                              origin_lon + (dest_lon - origin_lon) * 0.8),
                end_location=(dest_lat, dest_lon),
                maneuver="arrive"
            )
        ]

        result = RouteResult(
            origin=f"{origin_lat}, {origin_lon}",
            destination=f"{dest_lat}, {dest_lon}",
            distance_meters=distance,
            duration_seconds=duration,
            steps=steps,
            mode=mode,
            polyline=f"mock_polyline_{origin_lat}_{dest_lat}",
            warnings=["This is a simulated route. Replace with actual API for production."]
        )

        return result

    async def calculate_distance_matrix(
        self,
        origins: List[tuple[float, float]],
        destinations: List[tuple[float, float]],
        mode: str = "driving"
    ) -> Dict[str, List[List[float]]]:
        """
        Calculate distances and durations between multiple origins and destinations

        Args:
            origins: List of origin coordinates [(lat, lon), ...]
            destinations: List of destination coordinates [(lat, lon), ...]
            mode: Transportation mode

        Returns:
            Dictionary with distance and duration matrices

        Example:
            >>> origins = [(40.7484, -73.9857), (40.7589, -73.9851)]
            >>> destinations = [(40.7614, -73.9776)]
            >>> matrix = await server.calculate_distance_matrix(origins, destinations)
        """
        distances = []
        durations = []

        for origin in origins:
            origin_distances = []
            origin_durations = []

            for destination in destinations:
                route = await self.calculate_route(
                    origin[0], origin[1],
                    destination[0], destination[1],
                    mode
                )
                origin_distances.append(route.distance_meters)
                origin_durations.append(route.duration_seconds)

            distances.append(origin_distances)
            durations.append(origin_durations)

        return {
            "distances_meters": distances,
            "durations_seconds": durations
        }

    async def get_route_alternatives(
        self,
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        alternatives: int = 3
    ) -> List[RouteResult]:
        """
        Get alternative routes between two points

        Args:
            origin_lat: Origin latitude
            origin_lon: Origin longitude
            dest_lat: Destination latitude
            dest_lon: Destination longitude
            alternatives: Number of alternative routes to return

        Returns:
            List of alternative routes

        Example:
            >>> routes = await server.get_route_alternatives(40.7484, -73.9857, 40.7589, -73.9851)
            >>> for i, route in enumerate(routes):
            >>>     print(f"Route {i+1}: {route.distance_meters}m")
        """
        # PLACEHOLDER: In production, query API for actual alternatives
        base_route = await self.calculate_route(
            origin_lat, origin_lon, dest_lat, dest_lon
        )

        # Generate mock alternatives with slight variations
        routes = [base_route]

        for i in range(1, min(alternatives, 3)):
            alt_route = RouteResult(
                origin=base_route.origin,
                destination=base_route.destination,
                distance_meters=base_route.distance_meters * (1 + i * 0.1),
                duration_seconds=base_route.duration_seconds * (1 + i * 0.15),
                steps=base_route.steps,
                mode=base_route.mode,
                polyline=f"{base_route.polyline}_alt_{i}",
                warnings=[f"Alternative route {i+1} (simulated)"]
            )
            routes.append(alt_route)

        return routes

    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None


# Function tools for OpenAI Agents SDK
async def calculate_route_between_points(
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
    mode: str = "driving"
) -> str:
    """
    Calculate a route between two coordinates (OpenAI Agents SDK tool)

    Args:
        origin_lat: Origin latitude
        origin_lon: Origin longitude
        dest_lat: Destination latitude
        dest_lon: Destination longitude
        mode: Transportation mode (driving, walking, cycling, transit)

    Returns:
        JSON string with route information
    """
    server = RoutingServer()
    result = await server.calculate_route(
        origin_lat, origin_lon, dest_lat, dest_lon, mode
    )
    await server.close()

    return str({
        "distance_meters": result.distance_meters,
        "distance_km": round(result.distance_meters / 1000, 2),
        "duration_seconds": result.duration_seconds,
        "duration_minutes": round(result.duration_seconds / 60, 1),
        "mode": result.mode,
        "steps": len(result.steps),
        "warnings": result.warnings
    })


async def get_distance_matrix(
    origins: str,
    destinations: str,
    mode: str = "driving"
) -> str:
    """
    Calculate distances between multiple points (OpenAI Agents SDK tool)

    Args:
        origins: Comma-separated coordinates "lat1,lon1;lat2,lon2"
        destinations: Comma-separated coordinates "lat1,lon1;lat2,lon2"
        mode: Transportation mode

    Returns:
        JSON string with distance matrix
    """
    # Parse coordinates
    origin_coords = [tuple(map(float, coord.split(","))) for coord in origins.split(";")]
    dest_coords = [tuple(map(float, coord.split(","))) for coord in destinations.split(";")]

    server = RoutingServer()
    matrix = await server.calculate_distance_matrix(origin_coords, dest_coords, mode)
    await server.close()

    return str(matrix)
