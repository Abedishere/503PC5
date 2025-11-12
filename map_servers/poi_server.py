"""
POI (Points of Interest) Server - MCP-compliant server for place search and discovery
Following OpenAI Agents SDK patterns with function tools
"""

import asyncio
import os
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
import httpx
from enum import Enum


class POICategory(str, Enum):
    """Categories for POI search"""
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    HOTEL = "hotel"
    MUSEUM = "museum"
    PARK = "park"
    SHOPPING = "shopping"
    HOSPITAL = "hospital"
    GAS_STATION = "gas_station"
    ATM = "atm"
    PARKING = "parking"
    TRANSIT = "transit_station"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    LANDMARK = "landmark"


class POIResult(BaseModel):
    """A single point of interest result"""
    name: str
    category: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    price_level: Optional[int] = Field(None, ge=1, le=4)
    phone: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[List[str]] = None
    distance_meters: Optional[float] = None
    description: Optional[str] = None


class POIServer:
    """
    MCP-compliant POI (Points of Interest) Server
    Provides place search, nearby search, and place details
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the POI Server

        Args:
            api_key: API key for POI service (Google Places, Foursquare, etc.)
            base_url: Base URL for POI API
        """
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY", "")
        self.base_url = base_url or "https://maps.googleapis.com/maps/api/place"
        self.session = None

        # Mock database of POIs for demonstration
        self._mock_pois = self._initialize_mock_pois()

    def _initialize_mock_pois(self) -> List[POIResult]:
        """Initialize mock POI database for demonstration"""
        return [
            POIResult(
                name="Central Park",
                category="park",
                latitude=40.7829,
                longitude=-73.9654,
                address="New York, NY 10024",
                rating=4.8,
                description="Iconic urban park with lakes, theaters, playgrounds, and more"
            ),
            POIResult(
                name="Empire State Building",
                category="landmark",
                latitude=40.7484,
                longitude=-73.9857,
                address="350 5th Ave, New York, NY 10118",
                rating=4.7,
                price_level=3,
                website="https://www.esbnyc.com",
                description="Iconic Art Deco skyscraper with observation decks"
            ),
            POIResult(
                name="Joe's Pizza",
                category="restaurant",
                latitude=40.7308,
                longitude=-74.0023,
                address="7 Carmine St, New York, NY 10014",
                rating=4.5,
                price_level=1,
                phone="+1 212-366-1182",
                opening_hours=["Mon-Sun: 10:00 AM - 4:00 AM"],
                description="Classic New York-style pizza joint"
            ),
            POIResult(
                name="The Metropolitan Museum of Art",
                category="museum",
                latitude=40.7794,
                longitude=-73.9632,
                address="1000 5th Ave, New York, NY 10028",
                rating=4.8,
                price_level=2,
                website="https://www.metmuseum.org",
                opening_hours=["Sun-Thu: 10:00 AM - 5:00 PM", "Fri-Sat: 10:00 AM - 9:00 PM"],
                description="One of the world's largest and finest art museums"
            ),
            POIResult(
                name="Starbucks Reserve Roastery",
                category="cafe",
                latitude=40.7411,
                longitude=-73.9897,
                address="61 9th Ave, New York, NY 10011",
                rating=4.6,
                price_level=3,
                opening_hours=["Mon-Sun: 7:00 AM - 11:00 PM"],
                description="Upscale coffee experience with rare roasts"
            ),
            POIResult(
                name="Times Square",
                category="landmark",
                latitude=40.7580,
                longitude=-73.9855,
                address="Manhattan, NY 10036",
                rating=4.4,
                description="Iconic intersection known for bright lights and Broadway theaters"
            ),
            POIResult(
                name="Brooklyn Bridge Park",
                category="park",
                latitude=40.7009,
                longitude=-73.9969,
                address="Brooklyn, NY 11201",
                rating=4.7,
                description="Waterfront park with stunning Manhattan skyline views"
            ),
            POIResult(
                name="Grand Central Terminal",
                category="transit_station",
                latitude=40.7527,
                longitude=-73.9772,
                address="89 E 42nd St, New York, NY 10017",
                rating=4.6,
                description="Historic train station and architectural landmark"
            )
        ]

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session"""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=30.0)
        return self.session

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance using Haversine formula"""
        import math
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

    async def search_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float = 1000,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[POIResult]:
        """
        Search for nearby points of interest

        Args:
            latitude: Center point latitude
            longitude: Center point longitude
            radius_meters: Search radius in meters (default: 1000)
            category: Filter by category (e.g., "restaurant", "museum")
            limit: Maximum number of results (default: 10)

        Returns:
            List of nearby POIs sorted by distance

        Example:
            >>> pois = await server.search_nearby(40.7484, -73.9857, radius_meters=2000, category="restaurant")
            >>> for poi in pois:
            >>>     print(f"{poi.name} - {poi.distance_meters}m away")
        """
        # PLACEHOLDER: Replace with actual API call
        # For Google Places API:
        # session = await self._get_session()
        # params = {
        #     "location": f"{latitude},{longitude}",
        #     "radius": radius_meters,
        #     "type": category,
        #     "key": self.api_key
        # }
        # response = await session.get(f"{self.base_url}/nearbysearch/json", params=params)
        # data = response.json()

        # Use mock data for demonstration
        results = []
        for poi in self._mock_pois:
            # Calculate distance
            distance = self._calculate_distance(
                latitude, longitude,
                poi.latitude, poi.longitude
            )

            # Filter by radius and category
            if distance <= radius_meters:
                if category is None or poi.category == category:
                    poi_copy = poi.model_copy()
                    poi_copy.distance_meters = distance
                    results.append(poi_copy)

        # Sort by distance
        results.sort(key=lambda x: x.distance_meters or float('inf'))

        return results[:limit]

    async def search_text(
        self,
        query: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius_meters: Optional[float] = None,
        limit: int = 10
    ) -> List[POIResult]:
        """
        Search for places using text query

        Args:
            query: Search query (e.g., "pizza near Times Square")
            latitude: Optional center point latitude for proximity bias
            longitude: Optional center point longitude for proximity bias
            radius_meters: Optional search radius
            limit: Maximum number of results

        Returns:
            List of matching POIs

        Example:
            >>> pois = await server.search_text("coffee shops", latitude=40.7484, longitude=-73.9857)
        """
        # PLACEHOLDER: Replace with actual API call
        # For Google Places API:
        # session = await self._get_session()
        # params = {
        #     "query": query,
        #     "key": self.api_key
        # }
        # if latitude and longitude:
        #     params["location"] = f"{latitude},{longitude}"
        #     if radius_meters:
        #         params["radius"] = radius_meters
        # response = await session.get(f"{self.base_url}/textsearch/json", params=params)

        # Use mock data - filter by query keywords
        query_lower = query.lower()
        results = []

        for poi in self._mock_pois:
            # Simple keyword matching
            if (query_lower in poi.name.lower() or
                query_lower in poi.category.lower() or
                (poi.description and query_lower in poi.description.lower())):

                poi_copy = poi.model_copy()

                # Calculate distance if location provided
                if latitude is not None and longitude is not None:
                    distance = self._calculate_distance(
                        latitude, longitude,
                        poi.latitude, poi.longitude
                    )
                    poi_copy.distance_meters = distance

                    # Filter by radius if specified
                    if radius_meters is None or distance <= radius_meters:
                        results.append(poi_copy)
                else:
                    results.append(poi_copy)

        # Sort by distance if location provided, otherwise by rating
        if latitude is not None and longitude is not None:
            results.sort(key=lambda x: x.distance_meters or float('inf'))
        else:
            results.sort(key=lambda x: x.rating or 0, reverse=True)

        return results[:limit]

    async def get_place_details(
        self,
        place_name: str
    ) -> Optional[POIResult]:
        """
        Get detailed information about a specific place

        Args:
            place_name: Name of the place

        Returns:
            Detailed POI information if found

        Example:
            >>> details = await server.get_place_details("Empire State Building")
            >>> print(f"Rating: {details.rating}, Address: {details.address}")
        """
        # PLACEHOLDER: Replace with actual API call
        # Search in mock database
        for poi in self._mock_pois:
            if poi.name.lower() == place_name.lower():
                return poi

        return None

    async def search_by_category(
        self,
        category: str,
        latitude: float,
        longitude: float,
        radius_meters: float = 5000,
        min_rating: Optional[float] = None,
        max_price_level: Optional[int] = None,
        limit: int = 10
    ) -> List[POIResult]:
        """
        Search for places by category with filters

        Args:
            category: POI category (e.g., "restaurant", "hotel")
            latitude: Center point latitude
            longitude: Center point longitude
            radius_meters: Search radius in meters
            min_rating: Minimum rating filter (0-5)
            max_price_level: Maximum price level (1-4)
            limit: Maximum results

        Returns:
            Filtered list of POIs

        Example:
            >>> restaurants = await server.search_by_category(
            >>>     "restaurant", 40.7484, -73.9857,
            >>>     min_rating=4.0, max_price_level=2
            >>> )
        """
        # Get nearby POIs of this category
        results = await self.search_nearby(
            latitude, longitude, radius_meters, category, limit=100
        )

        # Apply filters
        filtered = []
        for poi in results:
            # Rating filter
            if min_rating is not None:
                if poi.rating is None or poi.rating < min_rating:
                    continue

            # Price level filter
            if max_price_level is not None:
                if poi.price_level is not None and poi.price_level > max_price_level:
                    continue

            filtered.append(poi)

        return filtered[:limit]

    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None


# Function tools for OpenAI Agents SDK
async def find_nearby_places(
    latitude: float,
    longitude: float,
    category: str = None,
    radius_meters: float = 1000,
    limit: int = 5
) -> str:
    """
    Find nearby places of interest (OpenAI Agents SDK tool)

    Args:
        latitude: Search center latitude
        longitude: Search center longitude
        category: Optional category filter (restaurant, cafe, museum, etc.)
        radius_meters: Search radius in meters
        limit: Maximum results

    Returns:
        JSON string with nearby places
    """
    server = POIServer()
    results = await server.search_nearby(
        latitude, longitude, radius_meters, category, limit
    )
    await server.close()

    formatted = []
    for poi in results:
        formatted.append({
            "name": poi.name,
            "category": poi.category,
            "address": poi.address,
            "rating": poi.rating,
            "distance_meters": round(poi.distance_meters, 1) if poi.distance_meters else None,
            "description": poi.description
        })

    return str(formatted)


async def search_places_by_text(
    query: str,
    latitude: float = None,
    longitude: float = None,
    limit: int = 5
) -> str:
    """
    Search for places using natural language query (OpenAI Agents SDK tool)

    Args:
        query: Search query (e.g., "best pizza restaurants")
        latitude: Optional location for proximity bias
        longitude: Optional location for proximity bias
        limit: Maximum results

    Returns:
        JSON string with search results
    """
    server = POIServer()
    results = await server.search_text(query, latitude, longitude, limit=limit)
    await server.close()

    formatted = []
    for poi in results:
        formatted.append({
            "name": poi.name,
            "category": poi.category,
            "rating": poi.rating,
            "address": poi.address,
            "price_level": poi.price_level,
            "description": poi.description
        })

    return str(formatted)


async def get_place_info(place_name: str) -> str:
    """
    Get detailed information about a specific place (OpenAI Agents SDK tool)

    Args:
        place_name: Name of the place

    Returns:
        JSON string with place details
    """
    server = POIServer()
    result = await server.get_place_details(place_name)
    await server.close()

    if result is None:
        return str({"error": f"Place '{place_name}' not found"})

    return str({
        "name": result.name,
        "category": result.category,
        "address": result.address,
        "coordinates": f"{result.latitude}, {result.longitude}",
        "rating": result.rating,
        "price_level": result.price_level,
        "phone": result.phone,
        "website": result.website,
        "opening_hours": result.opening_hours,
        "description": result.description
    })
